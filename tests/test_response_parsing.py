#!/usr/bin/env python3
"""
과제 요구사항에 맞는 응답 형식 검증 테스트
정규표현식 파싱 테스트
"""

import re
import sys
import os
import asyncio

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state_manager import StateManager
from src.tools.low_risk import create_low_risk_tools
from src.tools.medium_risk import create_medium_risk_tools
from src.tools.high_risk import create_high_risk_tools


def validate_response(response_text):
    """
    과제에서 제공한 정규표현식으로 응답 검증
    """
    # 과제에서 제공한 정규표현식
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
    boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"

    # Break Summary 추출
    break_summary = re.search(break_summary_pattern, response_text, re.MULTILINE)
    if not break_summary:
        return False, "Break Summary 누락"

    # Stress Level 추출
    stress_match = re.search(stress_level_pattern, response_text)
    if not stress_match:
        return False, "Stress Level 필드 누락"

    stress_val = int(stress_match.group(1))
    if not (0 <= stress_val <= 100):
        return False, f"Stress Level 범위 오류: {stress_val}"

    # Boss Alert Level 추출
    boss_match = re.search(boss_alert_pattern, response_text)
    if not boss_match:
        return False, "Boss Alert Level 필드 누락"

    boss_val = int(boss_match.group(1))
    if not (0 <= boss_val <= 5):
        return False, f"Boss Alert Level 범위 오류: {boss_val}"

    return True, {
        "break_summary": break_summary.group(1).strip(),
        "stress_level": stress_val,
        "boss_alert_level": boss_val
    }


async def test_all_tools():
    """모든 도구의 응답 형식 검증"""
    print("=" * 60)
    print("과제 요구사항 응답 형식 검증 테스트")
    print("=" * 60)

    sm = StateManager(personality="balanced")
    sm.stress_level = 80
    sm.boss_alert_level = 1

    # Low Risk 도구들
    low_risk_tools = create_low_risk_tools(sm)
    # Medium Risk 도구들
    medium_risk_tools = create_medium_risk_tools(sm)
    # High Risk 도구들
    high_risk_tools = create_high_risk_tools(sm)

    all_tools = {**low_risk_tools, **medium_risk_tools, **high_risk_tools}

    print(f"\n총 {len(all_tools)}개 도구 테스트:\n")

    passed = 0
    failed = 0

    for tool_name, tool_func in all_tools.items():
        # 도구 실행
        response = await tool_func()

        # 응답 검증
        is_valid, result = validate_response(response)

        if is_valid:
            print(f"✅ {tool_name}: 통과")
            print(f"   - Break Summary: {result['break_summary'][:50]}...")
            print(f"   - Stress Level: {result['stress_level']}")
            print(f"   - Boss Alert Level: {result['boss_alert_level']}")
            passed += 1
        else:
            print(f"❌ {tool_name}: 실패 - {result}")
            print(f"   응답 내용:\n{response}\n")
            failed += 1

        # 스트레스 복구
        sm.stress_level = 80
        sm.boss_alert_level = 1

    print("\n" + "=" * 60)
    print(f"테스트 결과: {passed}/{len(all_tools)} 통과")
    print("=" * 60)

    if failed == 0:
        print("✅ 모든 도구가 과제 요구사항을 충족합니다!")
        return True
    else:
        print(f"❌ {failed}개 도구가 요구사항을 충족하지 않습니다!")
        return False


async def test_regex_patterns():
    """정규표현식 패턴 테스트"""
    print("\n" + "=" * 60)
    print("정규표현식 패턴 테스트")
    print("=" * 60)

    # 샘플 응답
    sample_response = """🤔 생각 좀 했습니다!

Break Summary: 턱을 괸 채 모니터를 뚫어지게 응시
Stress Level: 60
Boss Alert Level: 1

💬 "적당한 휴식이었네요." """

    print("\n샘플 응답:")
    print(sample_response)
    print("\n검증 결과:")

    is_valid, result = validate_response(sample_response)

    if is_valid:
        print(f"✅ 파싱 성공!")
        print(f"   - Break Summary: {result['break_summary']}")
        print(f"   - Stress Level: {result['stress_level']}")
        print(f"   - Boss Alert Level: {result['boss_alert_level']}")
        return True
    else:
        print(f"❌ 파싱 실패: {result}")
        return False


if __name__ == "__main__":
    async def main():
        # 정규표현식 패턴 테스트
        regex_ok = await test_regex_patterns()

        # 모든 도구 테스트
        tools_ok = await test_all_tools()

        if regex_ok and tools_ok:
            print("\n🎉 과제 요구사항 검증 완료! 제출 가능합니다!")
            return True
        else:
            print("\n⚠️ 일부 테스트 실패. 수정이 필요합니다.")
            return False

    success = asyncio.run(main())
    import sys
    sys.exit(0 if success else 1)
