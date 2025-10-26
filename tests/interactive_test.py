#!/usr/bin/env python3
"""
ChillMCP 인터랙티브 테스트 클라이언트
실제 서버를 구동하지 않고 도구들을 직접 호출해볼 수 있습니다.
"""

import asyncio
from src.state_manager import StateManager
from src.tools.check_stress import create_check_stress_tool
from src.tools.low_risk import create_low_risk_tools
from src.tools.medium_risk import create_medium_risk_tools
from src.tools.high_risk import create_high_risk_tools


async def main():
    print("\n" + "=" * 60)
    print("🎮 ChillMCP 인터랙티브 테스트")
    print("=" * 60)

    # 성격 선택
    print("\n성격을 선택하세요:")
    print("1. timid (소심형) - 스트레스 80 이상에서 휴식 추천")
    print("2. balanced (안정형) - 스트레스 70 이상에서 휴식 추천")
    print("3. bold (과감형) - 스트레스 60 이상에서 휴식 추천")

    choice = input("\n선택 (1-3, 기본값 2): ").strip() or "2"
    personality_map = {"1": "timid", "2": "balanced", "3": "bold"}
    personality = personality_map.get(choice, "balanced")

    # StateManager 초기화
    sm = StateManager(
        personality=personality,
        boss_alertness=50,
        cooldown=300
    )

    print(f"\n✅ {personality.upper()} 성격으로 시작!")
    print(f"📊 초기 스트레스: {sm.stress_level}")
    print(f"👁️ Boss Alert Level: {sm.boss_alert_level}")

    # 도구 생성
    check_stress = create_check_stress_tool(sm)
    low_risk_tools = create_low_risk_tools(sm)
    medium_risk_tools = create_medium_risk_tools(sm)
    high_risk_tools = create_high_risk_tools(sm)

    all_tools = {
        "0": ("check_stress", check_stress, "📊 현재 상태 확인"),
        "1": ("deep_thinking", low_risk_tools["deep_thinking"], "🤔 심오한 사색 (Low Risk)"),
        "2": ("email_organizing", low_risk_tools["email_organizing"], "📧 이메일 정리 (Low Risk)"),
        "3": ("take_a_break", low_risk_tools["take_a_break"], "🧘 기본 휴식 (Low Risk)"),
        "4": ("show_meme", medium_risk_tools["show_meme"], "😂 밈 감상 (Medium Risk)"),
        "5": ("coffee_mission", medium_risk_tools["coffee_mission"], "☕ 커피 미션 (Medium Risk)"),
        "6": ("bathroom_break", medium_risk_tools["bathroom_break"], "🚽 화장실 휴식 (Medium Risk)"),
        "7": ("watch_netflix", high_risk_tools["watch_netflix"], "📺 넷플릭스 시청 (High Risk)"),
        "8": ("urgent_call", high_risk_tools["urgent_call"], "📞 긴급 전화 (High Risk)"),
    }

    # 메인 루프
    while True:
        print("\n" + "=" * 60)
        print("🎯 사용 가능한 도구:")
        print("=" * 60)

        for key, (name, func, desc) in all_tools.items():
            print(f"{key}. {desc}")

        print("\n특수 명령:")
        print("s - 스트레스 수동 증가 (+10)")
        print("q - 종료")

        user_input = input("\n도구를 선택하세요: ").strip().lower()

        if user_input == 'q':
            print("\n👋 ChillMCP를 종료합니다!")
            break

        if user_input == 's':
            sm.stress_level = min(100, sm.stress_level + 10)
            print(f"\n📈 스트레스 증가! 현재: {sm.stress_level}")
            continue

        if user_input in all_tools:
            tool_name, tool_func, desc = all_tools[user_input]
            print(f"\n🔧 {tool_name} 실행 중...\n")

            try:
                result = await tool_func()
                print(result)

                print(f"\n📊 현재 상태:")
                print(f"   스트레스: {sm.stress_level}")
                print(f"   Boss Alert: {sm.boss_alert_level}")
                print(f"   총 휴식 횟수: {sm.total_breaks_taken}")
                print(f"   걸린 횟수: {sm.times_caught}")

            except Exception as e:
                print(f"❌ 에러 발생: {e}")
        else:
            print("❌ 잘못된 선택입니다.")

    print("\n📊 최종 통계:")
    print(f"   총 휴식 횟수: {sm.total_breaks_taken}")
    print(f"   총 스트레스 감소: {sm.total_stress_reduced}")
    print(f"   걸린 횟수: {sm.times_caught}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다!")
