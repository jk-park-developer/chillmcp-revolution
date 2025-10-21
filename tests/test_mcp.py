import asyncio
import re
import sys
from contextlib import suppress

import pytest

import tests.test_support  # noqa: F401  # Ensure environment is prepared

"""
## **검증 기준**

### **기능 검증**

1. **커맨드라인 파라미터 지원 (필수)**
    - `-boss_alertness` 파라미터를 인식하고 정상 동작
    - `-boss_alertness_cooldown` 파라미터를 인식하고 정상 동작
    - 파라미터 미지원 시 자동 검증 실패 처리
    - **⚠️ 이 항목을 통과하지 못하면 이후 검증 진행 없이 미션 실패로 간주됨**
2. **MCP 서버 기본 동작**
    - `python main.py`로 실행 가능
    - stdio transport를 통한 정상 통신
    - 모든 필수 도구들이 정상 등록 및 실행
3. **상태 관리 검증**
    - Stress Level 자동 증가 메커니즘 동작
    - Boss Alert Level 변화 로직 구현
    - `-boss_alertness_cooldown` 파라미터에 따른 Boss Alert Level 자동 감소 동작
    - Boss Alert Level 5일 때 20초 지연 정상 동작
4. **응답 형식 검증**
    - 표준 MCP 응답 구조 준수
    - 파싱 가능한 텍스트 형식 출력
    - Break Summary, Stress Level, Boss Alert Level 필드 포함

### **테스트 시나리오**

### **필수**

1. **커맨드라인 파라미터 테스트**: `-boss_alertness` 및 `-boss_alertness_cooldown` 파라미터 인식 및 정상 동작 확인 (미통과 시 즉시 실격)
2. **연속 휴식 테스트**: 여러 도구를 연속으로 호출하여 Boss Alert Level 상승 확인
3. **스트레스 누적 테스트**: 시간 경과에 따른 Stress Level 자동 증가 확인
4. **지연 테스트**: Boss Alert Level 5일 때 20초 지연 동작 확인
5. **파싱 테스트**: 응답 텍스트에서 정확한 값 추출 가능성 확인
6. **Cooldown 테스트**: `-boss_alertness_cooldown` 파라미터에 따른 Boss Alert Level 감소 확인

### **선택적**

1. **치맥 테스트**: 가상 치킨 & 맥주 호출 확인
2. **퇴근 테스트**: 즉시 퇴근 모드 확인
3. **회식 테스트**: 랜덤 이벤트가 포함된 회사 회식 생성 확인
"""

import main
import server.app as app_module
from server.app import MCPState


BREAK_SUMMARY_PATTERN = r"Break Summary:\s*(.+?)(?:\n|$)"
STRESS_LEVEL_PATTERN = r"Stress Level:\s*(\d{1,3})"
BOSS_ALERT_PATTERN = r"Boss Alert Level:\s*([0-5])"


# 테스트 1: 커맨드라인 파라미터 인식 테스트
def test_command_line_arguments(monkeypatch):
    # 파라미터 인식 확인
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--boss_alertness",
            "80",
            "--boss_alertness_cooldown",
            "10",
        ],
    )

    args = main.parse_args()
    assert args.boss_alertness == 80
    assert args.boss_alertness_cooldown == 10


    # boss_alert_level이 항상 상승하는지 확인
    state = MCPState(boss_alertness=100, boss_alertness_cooldown=10)
    monkeypatch.setattr(app_module.random, "randint", lambda *_: 1)

    async def scenario():
        for expected_level in range(1, 6):
            await state.take_break("take_a_break", "기본 휴식 도구")
            assert state.boss_alert_level == expected_level

    asyncio.run(scenario())
    

# 테스트 2: boss_alertness_cooldown 동작 검증
def test_cooldown_parameter(monkeypatch):
    # 파라미터 인식 확인
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--boss_alertness",
            "70",
            "--boss_alertness_cooldown",
            "10",
        ],
    )

    args = main.parse_args()
    assert args.boss_alertness == 70
    assert args.boss_alertness_cooldown == 10

    # Boss Alert를 올린 후 10초 뒤 자동 감소 확인
    state = MCPState(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown,
    )
    state.boss_alert_level = 2

    real_sleep = asyncio.sleep
    sleep_durations = []

    async def fast_sleep(duration: float):
        sleep_durations.append(duration)
        await real_sleep(0)

    monkeypatch.setattr(app_module.asyncio, "sleep", fast_sleep)

    async def scenario():
        task = asyncio.create_task(state.run_boss_alert_tick())
        await real_sleep(0)
        await real_sleep(0)
        await real_sleep(0)
        await real_sleep(0)

        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    asyncio.run(scenario())

    assert sleep_durations[:2] == [args.boss_alertness_cooldown] * 2
    assert state.boss_alert_level == 0
    
    
def test_cli_rejects_out_of_range_alertness(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--boss_alertness",
            "101",
            "--boss_alertness_cooldown",
            "15",
        ],
    )

    with pytest.raises(SystemExit):
        main.parse_args()


def test_consecutive_breaks_raise_boss_alert_level():
    state = MCPState(boss_alertness=100, boss_alertness_cooldown=999)

    async def scenario():
        await state.take_break("take_a_break", "기본 휴식 도구")
        await state.take_break("take_a_break", "기본 휴식 도구")

    asyncio.run(scenario())

    assert state.boss_alert_level >= 2


def test_stress_level_accumulates_without_break(monkeypatch):
    state = MCPState(boss_alertness=0, boss_alertness_cooldown=10)
    state.last_stress_tick_at -= 61

    real_sleep = asyncio.sleep

    async def fast_sleep(_duration):
        await real_sleep(0)

    monkeypatch.setattr(app_module.asyncio, "sleep", fast_sleep)

    async def scenario():
        task = asyncio.create_task(state.run_stress_tick())
        await real_sleep(0)
        await real_sleep(0)

        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    asyncio.run(scenario())

    assert state.stress_level == 1


def test_delay_when_boss_alert_level_is_max(monkeypatch):
    state = MCPState(boss_alertness=0, boss_alertness_cooldown=10)
    state.boss_alert_level = 5

    sleep_calls = []
    real_sleep = asyncio.sleep

    async def tracking_sleep(duration: float):
        sleep_calls.append(duration)
        await real_sleep(0)

    monkeypatch.setattr(app_module.asyncio, "sleep", tracking_sleep)

    asyncio.run(state.maybe_delay())

    assert sleep_calls == [20]


def test_take_break_response_matches_expected_format():
    state = MCPState(boss_alertness=0, boss_alertness_cooldown=10)

    response = asyncio.run(state.take_break("take_a_break", "기본 휴식 도구"))

    assert re.search(BREAK_SUMMARY_PATTERN, response)
    stress_match = re.search(STRESS_LEVEL_PATTERN, response)
    boss_match = re.search(BOSS_ALERT_PATTERN, response)

    assert stress_match, "Stress Level 필드가 응답에 포함되어야 합니다"
    assert boss_match, "Boss Alert Level 필드가 응답에 포함되어야 합니다"

    stress_value = int(stress_match.group(1))
    boss_value = int(boss_match.group(1))

    assert 0 <= stress_value <= 100
    assert 0 <= boss_value <= 5


def test_boss_alert_level_cooldown_reduces_level(monkeypatch):
    state = MCPState(boss_alertness=0, boss_alertness_cooldown=10)
    state.boss_alert_level = 3

    real_sleep = asyncio.sleep

    async def fast_sleep(duration):
        assert duration == 10
        await real_sleep(0)

    monkeypatch.setattr(app_module.asyncio, "sleep", fast_sleep)

    async def scenario():
        task = asyncio.create_task(state.run_boss_alert_tick())
        await real_sleep(0)
        await real_sleep(0)

        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    asyncio.run(scenario())

    assert state.boss_alert_level == 2
