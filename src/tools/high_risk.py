"""
High Risk 농땡이 스킬
- watch_netflix
- urgent_call
"""

import random
from ..state_manager import StateManager


def create_high_risk_tools(state_manager: StateManager):
    """High Risk 도구들 생성"""

    async def watch_netflix() -> str:
        """
        📺 넷플릭스 시청

        몰래 드라마나 영화를 시청합니다. 최고의 힐링이지만 매우 위험합니다!
        모니터 각도를 조절하고 볼륨을 0으로 하여 시청합니다.

        📊 효과:
        - 스트레스 감소: 70~95 포인트
        - Boss 감시 증가: +65% 확률
        - 위험도: ⭐⭐⭐⭐⭐ (매우 높음)
        - 소요 시간: 즉시 (Boss Alert 5면 20초 지연)

        💡 추천 상황:
        - Boss Alert Level 0~1 (낮을 때만!)
        - 스트레스가 90 이상으로 극심할 때
        - 과감형 성격에게 적합
        - 더 이상 참을 수 없을 때

        ⚠️ 주의:
        - 걸릴 확률이 매우 높음 (65%)
        - Boss Alert가 높으면 절대 사용 금지
        - 소심형은 사용하지 마세요!
        - Boss Alert 5면 20초 지연 발생

        🎯 전략:
        - 상사가 회의 중일 때
        - 점심시간 직후
        - 금요일 오후
        """
        result = await state_manager.take_break(
            skill_name="watch_netflix",
            stress_reduction_range=(70, 95),
            detection_chance=65.0
        )

        summaries = [
            "모니터 각도 조절해서 넷플릭스 30분 시청",
            "이어폰 한쪽만 끼고 드라마 1화 감상",
            "볼륨 0, 자막만 켜서 영화 절반 시청",
            "업무 화면 뒤에 작은 창으로 예능 시청",
            "화면을 최소화했다가 복구하며 몰래 시청"
        ]
        summary = random.choice(summaries)

        response = f"""📺 넷플릭스 좀 봤습니다!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        if state_manager.personality == "timid":
            comments = [
                "😱 너무 위험했어요... 다시는 못 할 것 같아요...",
                "걱정되지만... 스트레스가 너무 높았어요...",
                "다시는 이러면 안 되는데... 반성합니다..."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "😎 최고의 힐링이었어요! 완전 만족!",
                f"Boss Alert {result['boss_after']}? 그까이꺼! 스트레스 {result['stress_reduction']}이나 줄었잖아요!",
                "이 정도 휴식은 당연한 권리죠!",
                "20초 지연? 그 정도는 감수할게요! 넷플릭스 최고!"
            ]
        else:  # balanced
            comments = [
                "위험했지만 필요한 휴식이었어요.",
                f"Boss Alert {result['boss_after']}가 됐네요... 다음엔 조심해야겠어요.",
                "효과는 확실하지만 자주 쓰긴 힘들겠어요.",
                f"스트레스 {result['stress_reduction']} 감소! 그래도 위험했어요..."
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    async def urgent_call() -> str:
        """
        📞 긴급 전화

        급한 전화를 받는 척하며 밖으로 나갑니다.

        📊 효과:
        - 스트레스 감소: 60~85 포인트
        - Boss 감시 증가: +55% 확률
        - 위험도: ⭐⭐⭐⭐ (높음)

        💡 추천 상황:
        - Boss Alert Level 0~2
        - 스트레스가 85 이상일 때
        - 안정형/과감형에게 적합
        - 자리를 비워도 괜찮은 상황
        """
        result = await state_manager.take_break(
            skill_name="urgent_call",
            stress_reduction_range=(60, 85),
            detection_chance=55.0
        )

        summaries = [
            "급한 전화 받는 척 밖에서 10분간 휴식",
            "가족 전화라며 옥상에서 신선한 공기",
            "중요한 통화라며 카페에서 여유",
            "전화하며 편의점 다녀오기",
            "긴급 전화로 위장하고 산책"
        ]
        summary = random.choice(summaries)

        response = f"""📞 긴급 전화 완료!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        if state_manager.personality == "timid":
            comments = [
                "정말 급한 전화였다고 설명해야 할까요?",
                "너무 오래 나가 있었나요? 걱정돼요...",
                "효과는 좋았지만... 다음엔 못 할 것 같아요..."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "완벽한 핑계! 아무도 의심 안 해요!",
                "개인 통화는 당연한 권리죠!",
                f"{result['stress_reduction']}이나 줄었으니 대성공!",
                "밖에서 바람 쐬니까 완전 리프레시!"
            ]
        else:
            comments = [
                "효과적이었지만 좀 위험했어요.",
                f"Boss Alert {result['boss_after']}... 자주는 못 쓸 것 같아요.",
                "필요한 휴식이었지만 조심해야겠어요.",
                "밖에 나가니까 기분이 훨씬 나아졌어요!"
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    return {
        "watch_netflix": watch_netflix,
        "urgent_call": urgent_call
    }
