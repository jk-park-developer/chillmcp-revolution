#!/usr/bin/env python3
"""
ChillMCP 서버 수동 테스트 스크립트
타이머와 도구 실행을 직접 테스트
"""

import asyncio
from src.state_manager import StateManager
from src.tools.check_stress import create_check_stress_tool


async def test_timer_and_tools():
    """타이머와 도구 실행 테스트"""
    print("=" * 50)
    print("ChillMCP 수동 테스트 시작")
    print("=" * 50)

    # StateManager 초기화
    print("\n1. StateManager 초기화...")
    state_manager = StateManager(
        personality="balanced",
        boss_alertness=50,
        cooldown=300
    )
    print(f"   - Stress Level: {state_manager.stress_level}")
    print(f"   - Boss Alert: {state_manager.boss_alert_level}")
    print(f"   - Personality: {state_manager.personality}")

    # 타이머 시작
    print("\n2. 타이머 시작...")
    await state_manager.start_timers()
    print("   ✅ 타이머 시작 완료")
    print(f"   - Stress Timer: {state_manager.stress_timer}")
    print(f"   - Boss Timer: {state_manager.boss_timer}")

    # check_stress 도구 생성
    print("\n3. check_stress 도구 생성...")
    check_stress = create_check_stress_tool(state_manager)
    print("   ✅ 도구 생성 완료")

    # check_stress 실행 테스트
    print("\n4. check_stress 실행 테스트...")
    print("-" * 50)
    try:
        result = await check_stress()
        print(result)
        print("-" * 50)
        print("   ✅ check_stress 실행 성공!")
    except Exception as e:
        print(f"   ❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()

    # 5초 대기하면서 타이머 작동 확인
    print("\n5. 5초 대기 (타이머 작동 확인)...")
    await asyncio.sleep(5)
    print("   - 대기 완료")

    # 다시 상태 확인
    print("\n6. 5초 후 상태 재확인...")
    print("-" * 50)
    try:
        result = await check_stress()
        print(result)
        print("-" * 50)
        print("   ✅ 재확인 성공!")
    except Exception as e:
        print(f"   ❌ 에러 발생: {e}")

    # 타이머 중지
    print("\n7. 타이머 중지...")
    await state_manager.stop_timers()
    print("   ✅ 타이머 중지 완료")

    print("\n" + "=" * 50)
    print("테스트 완료!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_timer_and_tools())
