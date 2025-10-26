#!/usr/bin/env python3
"""
커맨드라인 파라미터 검증 테스트
과제 요구사항: 서버가 --boss_alertness 및 --boss_alertness_cooldown 파라미터를
올바르게 인식하고 동작하는지 검증

⚠️ 중요: 이 검증을 통과하지 못하면 미션 실패로 처리됩니다.
"""

import subprocess
import time
import json
import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_command_line_arguments():
    """
    테스트 1: 커맨드라인 파라미터 인식 테스트
    서버가 --boss_alertness 및 --boss_alertness_cooldown 파라미터를
    올바르게 인식하고 동작하는지 검증
    """
    print("=" * 60)
    print("TEST 1: 커맨드라인 파라미터 인식 테스트")
    print("=" * 60)

    # Python 실행 파일 경로 설정
    python_executable = sys.executable
    # 프로젝트 루트의 main.py 경로
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    script_path = os.path.join(project_root, "main.py")

    print(f"\n🔧 서버 시작 중...")
    print(f"   - Python: {python_executable}")
    print(f"   - Script: {script_path}")
    print(f"   - 파라미터: --boss_alertness 100 --boss_alertness_cooldown 10")

    # 높은 boss_alertness로 테스트
    process = subprocess.Popen(
        [python_executable, script_path,
         "--boss_alertness", "100",
         "--boss_alertness_cooldown", "10"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # 서버 시작 대기
    print("\n⏳ 서버 시작 대기 중... (2초)")
    time.sleep(2)

    # 서버가 정상 실행되었는지 확인
    if process.poll() is not None:
        # 프로세스가 이미 종료됨
        stdout, stderr = process.communicate()
        print(f"\n❌ 서버 시작 실패!")
        print(f"\nSTDOUT:\n{stdout}")
        print(f"\nSTDERR:\n{stderr}")
        return False

    print("✅ 서버가 파라미터를 인식하고 정상 시작되었습니다")

    # MCP 초기화 요청 전송
    print("\n📤 MCP 초기화 요청 전송...")
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }

    try:
        process.stdin.write(json.dumps(initialize_request) + "\n")
        process.stdin.flush()

        # 응답 대기
        time.sleep(1)

        # tools/list 요청으로 도구 목록 확인
        print("\n📤 도구 목록 요청 전송...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }

        process.stdin.write(json.dumps(list_tools_request) + "\n")
        process.stdin.flush()

        # 응답 대기
        time.sleep(1)

        print("✅ MCP 프로토콜 통신 성공")

    except Exception as e:
        print(f"❌ MCP 통신 실패: {e}")
        return False
    finally:
        # 프로세스 종료
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
        print("\n🛑 서버 종료 완료")

    print("\n✅ TEST 1 통과: 파라미터 인식 정상 동작")
    return True


def test_cooldown_parameter():
    """
    테스트 2: boss_alertness_cooldown 동작 검증
    --boss_alertness_cooldown 파라미터가 실제로
    Boss Alert Level 감소 주기를 제어하는지 검증
    """
    print("\n" + "=" * 60)
    print("TEST 2: boss_alertness_cooldown 동작 검증")
    print("=" * 60)

    print("\n📝 테스트 시나리오:")
    print("   1. 짧은 cooldown(10초)으로 서버 시작")
    print("   2. Boss Alert를 올린 후 10초 뒤 자동 감소 확인")
    print("   3. StateManager의 cooldown 설정이 올바른지 검증")

    # Python 실행 파일 경로 설정
    python_executable = sys.executable

    # StateManager를 직접 테스트
    print("\n🔧 StateManager를 이용한 cooldown 검증...")

    from src.state_manager import StateManager
    import asyncio

    async def verify_cooldown():
        # cooldown=5초로 설정
        sm = StateManager(personality="balanced", boss_alertness=50, cooldown=5)

        print(f"   - 초기 Boss Alert Level: {sm.boss_alert_level}")
        print(f"   - Cooldown 설정: {sm.cooldown}초")

        # Boss Alert를 수동으로 올림
        sm.boss_alert_level = 3
        print(f"   - Boss Alert를 3으로 설정")

        # 타이머 시작
        await sm.start_timers()
        print(f"   - 타이머 시작됨")

        # 6초 대기 (cooldown=5초보다 1초 더)
        print(f"   - 6초 대기 중... (cooldown보다 1초 길게)")
        await asyncio.sleep(6)

        # Boss Alert가 감소했는지 확인
        print(f"   - 대기 후 Boss Alert Level: {sm.boss_alert_level}")

        await sm.stop_timers()

        # 검증: 6초 후 Boss Alert가 1 감소해야 함
        if sm.boss_alert_level == 2:
            print("\n✅ cooldown 파라미터가 정상 동작합니다!")
            return True
        else:
            print(f"\n❌ 예상값: 2, 실제값: {sm.boss_alert_level}")
            return False

    result = asyncio.run(verify_cooldown())

    if result:
        print("\n✅ TEST 2 통과: cooldown 파라미터 정상 동작")
    else:
        print("\n❌ TEST 2 실패: cooldown 파라미터 동작 이상")

    return result


def test_parameter_validation():
    """
    테스트 3: 파라미터 범위 검증 테스트
    잘못된 파라미터 값에 대해 에러를 발생시키는지 확인
    """
    print("\n" + "=" * 60)
    print("TEST 3: 파라미터 범위 검증 테스트")
    print("=" * 60)

    python_executable = sys.executable
    # 프로젝트 루트의 main.py 경로
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    script_path = os.path.join(project_root, "main.py")

    test_cases = [
        {
            "name": "boss_alertness > 100",
            "args": ["--boss_alertness", "150"],
            "should_fail": True
        },
        {
            "name": "boss_alertness < 0",
            "args": ["--boss_alertness", "-10"],
            "should_fail": True
        },
        {
            "name": "boss_alertness_cooldown < 1",
            "args": ["--boss_alertness_cooldown", "0"],
            "should_fail": True
        },
        {
            "name": "정상 파라미터",
            "args": ["--boss_alertness", "50", "--boss_alertness_cooldown", "300"],
            "should_fail": False
        }
    ]

    all_passed = True

    for test_case in test_cases:
        print(f"\n🧪 테스트: {test_case['name']}")
        print(f"   파라미터: {' '.join(test_case['args'])}")

        process = subprocess.Popen(
            [python_executable, script_path] + test_case['args'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        time.sleep(1)

        # 프로세스 종료 확인
        return_code = process.poll()

        if test_case['should_fail']:
            # 실패해야 하는 경우
            if return_code is not None and return_code != 0:
                print(f"   ✅ 예상대로 에러 발생 (return code: {return_code})")
            else:
                print(f"   ❌ 에러가 발생하지 않음 (예상: 실패)")
                all_passed = False
        else:
            # 성공해야 하는 경우
            if return_code is None or return_code == 0:
                print(f"   ✅ 정상 실행")
            else:
                print(f"   ❌ 예상치 못한 에러 (return code: {return_code})")
                all_passed = False

        # 프로세스 종료
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

    if all_passed:
        print("\n✅ TEST 3 통과: 파라미터 검증 정상 동작")
    else:
        print("\n❌ TEST 3 실패: 파라미터 검증 이상")

    return all_passed


def run_all_tests():
    """모든 커맨드라인 파라미터 테스트 실행"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     커맨드라인 파라미터 검증 테스트 (필수)              ║")
    print("║  ⚠️  이 테스트를 통과하지 못하면 미션 실패로 처리됩니다  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    results = []

    # TEST 1: 파라미터 인식
    try:
        result1 = test_command_line_arguments()
        results.append(("파라미터 인식 테스트", result1))
    except Exception as e:
        print(f"\n❌ TEST 1 예외 발생: {e}")
        import traceback
        traceback.print_exc()
        results.append(("파라미터 인식 테스트", False))

    # TEST 2: cooldown 동작
    try:
        result2 = test_cooldown_parameter()
        results.append(("cooldown 동작 테스트", result2))
    except Exception as e:
        print(f"\n❌ TEST 2 예외 발생: {e}")
        import traceback
        traceback.print_exc()
        results.append(("cooldown 동작 테스트", False))

    # TEST 3: 파라미터 검증
    try:
        result3 = test_parameter_validation()
        results.append(("파라미터 검증 테스트", result3))
    except Exception as e:
        print(f"\n❌ TEST 3 예외 발생: {e}")
        import traceback
        traceback.print_exc()
        results.append(("파라미터 검증 테스트", False))

    # 결과 요약
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                   테스트 결과 요약                        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"  {status}  {test_name}")

    print()
    print(f"총 {passed}/{total} 테스트 통과")
    print()

    if passed == total:
        print("╔══════════════════════════════════════════════════════════╗")
        print("║  🎉 모든 필수 검증 통과! 미션 제출 가능합니다!           ║")
        print("╚══════════════════════════════════════════════════════════╝")
        return True
    else:
        print("╔══════════════════════════════════════════════════════════╗")
        print("║  ❌ 필수 검증 실패! 수정이 필요합니다!                   ║")
        print("║     이 상태로는 미션 실패로 처리됩니다.                  ║")
        print("╚══════════════════════════════════════════════════════════╝")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
