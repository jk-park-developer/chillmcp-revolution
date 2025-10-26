"""
Low Risk 농땡이 스킬
- deep_thinking
- email_organizing
- take_a_break
"""

import random
from ..state_manager import StateManager


def create_low_risk_tools(state_manager: StateManager):
    """Low Risk 도구들 생성"""

    async def deep_thinking() -> str:
        """
        🤔 심오한 사색

        업무에 집중하는 것처럼 보이는 가장 안전한 휴식 방법입니다.
        턱을 괴고 심각한 표정을 지으며 생각에 잠긴 척합니다.

        📊 효과:
        - 스트레스 감소: 20~30 포인트
        - Boss 감시 증가: +10% 확률
        - 위험도: ⭐ (매우 낮음)
        - 소요 시간: 즉시 (Boss Alert 5 제외)

        💡 추천 상황:
        - Boss Alert Level 3~4 (높을 때)
        - 소심형 성격에게 최적
        - 안전하게 조금씩 회복하고 싶을 때
        - 상사가 근처에 있을 때

        ⚠️ 주의:
        - 효과는 낮지만 절대 안전함
        - 다른 스킬이 위험할 때 사용
        """
        result = await state_manager.take_break(
            skill_name="deep_thinking",
            stress_reduction_range=(20, 30),
            detection_chance=10.0
        )

        summaries = [
            "턱을 괸 채 모니터를 뚫어지게 응시",
            "심각한 표정으로 천장을 올려다봄",
            "펜을 돌리며 깊은 생각에 잠긴 척",
            "노트에 낙서하며 업무 고민하는 척",
            "창밖을 보며 알고리즘을 구상하는 척"
        ]
        summary = random.choice(summaries)

        response = f"""🤔 생각 좀 했습니다!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        # 성격별 감상
        if state_manager.personality == "timid":
            comments = [
                "다행히 안 걸렸어요... 조심스럽게 계속할게요",
                "휴... 이 정도는 괜찮겠죠?",
                "상사가 못 봤으면 좋겠어요..."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "이 정도 휴식은 당연한 거죠!",
                "생각 정리도 업무의 일부예요!",
                "완벽하게 업무하는 척 성공!"
            ]
        else:  # balanced
            comments = [
                "적당한 휴식이었네요.",
                "이제 다시 집중할 수 있겠어요.",
                "생각 정리가 됐습니다!"
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    async def email_organizing() -> str:
        """
        📧 이메일 정리

        이메일을 정리하는 척하며 온라인 쇼핑을 즐깁니다.

        📊 효과:
        - 스트레스 감소: 25~40 포인트
        - Boss 감시 증가: +15% 확률
        - 위험도: ⭐ (매우 낮음)

        💡 추천 상황:
        - Boss Alert Level 3~4
        - 업무하는 것처럼 보여야 할 때
        - 소심형/안정형에게 적합
        """
        result = await state_manager.take_break(
            skill_name="email_organizing",
            stress_reduction_range=(25, 40),
            detection_chance=15.0
        )

        summaries = [
            "이메일 정리하는 척 쇼핑몰 구경",
            "스팸 메일 삭제하며 SNS 확인",
            "중요 메일 표시하는 척 뉴스 읽기",
            "폴더 정리하며 유튜브 짧은 영상 시청",
            "답장 쓰는 척 친구 메시지 확인"
        ]
        summary = random.choice(summaries)

        response = f"""📧 이메일 정리 완료!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        if state_manager.personality == "timid":
            comments = [
                "업무처럼 보였을까요? 다행이에요...",
                "이메일 정리는 정당한 업무죠!",
                "안전하게 마쳤어요."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "이메일 정리도 중요한 업무죠!",
                "효율적인 멀티태스킹!",
                "이런 건 들킬 일도 없어요!"
            ]
        else:
            comments = [
                "적절한 업무 휴식이었네요.",
                "이메일도 정리하고 기분도 전환했어요.",
                "생산적인 휴식이었습니다!"
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    async def take_a_break() -> str:
        """
        🧘 기본 휴식

        짧은 스트레칭이나 창밖을 보며 휴식합니다.

        📊 효과:
        - 스트레스 감소: 30~45 포인트
        - Boss 감시 증가: +20% 확률
        - 위험도: ⭐⭐ (낮음)

        💡 추천 상황:
        - Boss Alert Level 2~3
        - 정당한 휴식이 필요할 때
        - 모든 성격에게 무난함
        """
        result = await state_manager.take_break(
            skill_name="take_a_break",
            stress_reduction_range=(30, 45),
            detection_chance=20.0
        )

        summaries = [
            "자리에서 일어나 가볍게 스트레칭",
            "창밖을 보며 5분간 멍 때리기",
            "물 마시러 가며 복도 산책",
            "눈 감고 심호흡 10회",
            "의자에 앉아 목과 어깨 돌리기"
        ]
        summary = random.choice(summaries)

        response = f"""🧘 휴식 완료!

Break Summary: {summary}
Stress Level: {result['stress_after']}
Boss Alert Level: {result['boss_after']}"""

        if result['delayed']:
            response = f"⚠️ 상사가 째려봐서 20초나 걸렸어요...\n\n" + response

        if state_manager.personality == "timid":
            comments = [
                "정당한 휴식이니까 괜찮겠죠?",
                "몸도 풀고 기분도 좋아졌어요.",
                "이 정도는 누구나 하잖아요..."
            ]
        elif state_manager.personality == "bold":
            comments = [
                "당연한 권리죠! 휴식은 필수!",
                "건강을 위한 투자입니다!",
                "효율을 위한 최고의 선택!"
            ]
        else:
            comments = [
                "적절한 휴식이었어요.",
                "몸도 마음도 가벼워졌네요.",
                "이제 다시 일할 준비 완료!"
            ]

        response += f"\n\n💬 \"{random.choice(comments)}\""
        return response

    return {
        "deep_thinking": deep_thinking,
        "email_organizing": email_organizing,
        "take_a_break": take_a_break
    }
