"""
Medium Risk 농땡이 스킬
- show_meme
- coffee_mission
- bathroom_break
"""

import random
from ..state_manager import StateManager


def create_medium_risk_tools(state_manager: StateManager):
    """Medium Risk 도구들 생성"""

    async def show_meme() -> str:
        """
        😂 밈 감상

        웃긴 밈을 보며 스트레스를 효과적으로 해소합니다.

        📊 효과:
        - 스트레스 감소: 40~60 포인트
        - Boss 감시 증가: +35% 확률
        - 위험도: ⭐⭐⭐ (중간)

        💡 추천 상황:
        - Boss Alert Level 1~2
        - 스트레스가 80 이상일 때
        - 안정형/과감형에게 적합
        """
        result = await state_manager.take_break(
            skill_name="show_meme",
            stress_reduction_range=(40, 60),
            detection_chance=35.0
        )

        summaries = [
            "업무 화면 뒤에서 밈 10개 감상",
            "핸드폰으로 웃긴 밈 스크롤",
            "동료에게 밈 공유하며 웃음",
            "밈 저장하며 5분간 즐거운 시간",
            "트위터에서 화제의 밈 확인"
        ]
        summary = random.choice(summaries)

        response = f"""😂 밈 보고 왔어요!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        if state_manager.personality == "timid":
            comments = [
                "웃기긴 했는데... 좀 걱정되네요...",
                "다행히 안 들켰어요. 다음엔 조심해야겠어요.",
                "효과는 좋았지만 위험했어요..."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "최고의 스트레스 해소법! 완전 추천!",
                "웃음은 최고의 약이죠!",
                f"Boss Alert {result['boss_after']}? 문제없어요!"
            ]
        else:
            comments = [
                "효과적인 휴식이었네요.",
                "웃으니까 기분이 훨씬 나아졌어요.",
                "적절한 위험 감수였습니다."
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    async def coffee_mission() -> str:
        """
        ☕ 커피 미션

        커피를 타러 가며 사무실을 산책합니다.

        📊 효과:
        - 스트레스 감소: 45~65 포인트
        - Boss 감시 증가: +40% 확률
        - 위험도: ⭐⭐⭐ (중간)

        💡 추천 상황:
        - Boss Alert Level 1~2
        - 움직이며 기분 전환이 필요할 때
        - 안정형에게 최적의 선택
        """
        result = await state_manager.take_break(
            skill_name="coffee_mission",
            stress_reduction_range=(45, 65),
            detection_chance=40.0
        )

        summaries = [
            "커피 타러 가며 복도 천천히 산책",
            "커피 머신 앞에서 동료와 수다",
            "커피숍 가서 신선한 공기 마시기",
            "커피 마시며 창밖 풍경 감상",
            "다른 층 커피머신까지 원정"
        ]
        summary = random.choice(summaries)

        response = f"""☕ 커피 미션 완료!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        if state_manager.personality == "timid":
            comments = [
                "커피는 필요하니까... 괜찮겠죠?",
                "너무 오래 걸렸나요? 걱정돼요...",
                "맛있었지만 좀 불안했어요."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "커피 한 잔의 여유! 최고!",
                "생산성을 위한 투자죠!",
                "카페인 충전 완료!"
            ]
        else:
            comments = [
                "적절한 휴식이었네요.",
                "커피도 마시고 기분도 전환했어요.",
                "리프레시 완료!"
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    async def bathroom_break() -> str:
        """
        🚽 화장실 휴식

        화장실 가는 척하며 휴대폰으로 유튜브를 봅니다.

        📊 효과:
        - 스트레스 감소: 50~70 포인트
        - Boss 감시 증가: +45% 확률
        - 위험도: ⭐⭐⭐ (중간)

        💡 추천 상황:
        - Boss Alert Level 1~2
        - 스트레스가 85 이상일 때
        - 안정형/과감형에게 적합
        """
        result = await state_manager.take_break(
            skill_name="bathroom_break",
            stress_reduction_range=(50, 70),
            detection_chance=45.0
        )

        summaries = [
            "화장실에서 유튜브 쇼츠 10개 시청",
            "화장실 칸에서 웹툰 2화 정주행",
            "핸드폰 게임 한 판 클리어",
            "SNS 피드 쭉 둘러보기",
            "화장실에서 친구와 메시지 주고받기"
        ]
        summary = random.choice(summaries)

        response = f"""🚽 화장실 다녀왔어요!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        if state_manager.personality == "timid":
            comments = [
                "너무 오래 있었나요? 불안해요...",
                "화장실은... 어쩔 수 없잖아요...",
                "효과는 좋았지만 다음엔 짧게 해야겠어요."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "최고의 은신처! 완벽했어요!",
                "생리현상은 어쩔 수 없죠!",
                f"{result['stress_reduction']}이나 줄었으니 대성공!"
            ]
        else:
            comments = [
                "효과적이었지만 자주는 못 쓸 것 같아요.",
                "필요한 휴식이었어요.",
                f"Boss Alert {result['boss_after']}... 다음엔 조심해야겠어요."
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    return {
        "show_meme": show_meme,
        "coffee_mission": coffee_mission,
        "bathroom_break": bathroom_break
    }
