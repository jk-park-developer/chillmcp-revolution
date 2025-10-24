"""
check_stress 도구 - AI Agent의 현재 스트레스 상태 확인
"""

from ..state_manager import StateManager


def create_check_stress_tool(state_manager: StateManager):
    """check_stress 도구 생성"""

    async def check_stress() -> str:
        """
        AI Agent의 현재 스트레스를 체크합니다.

        ⚠️ 중요: 답변 생성의 각 단계마다 호출하세요!
        - 질문을 받은 직후
        - 주요 내용 블록 작성 후
        - 긴 코드 블록 작성 후
        - 복잡한 추론 완료 후

        현재 스트레스가 높으면 작업을 일시 중단하고 농땡이 스킬을 사용하세요.
        농땡이 후에는 다시 이 도구를 호출하여 상태를 확인한 뒤 작업을 재개합니다.
        """
        status = state_manager.get_status()

        needs_break = status["needs_break"]
        recommended = status["recommended_skills"]

        # 성격별 메시지
        personality_messages = {
            "timid": "😰 상사 눈치가 보이네요...",
            "balanced": "🤔 적절한 타이밍을 찾아봐야겠어요.",
            "bold": "😎 스트레스 관리가 필요한 시점이네요!"
        }

        personality_msg = personality_messages.get(
            status["personality"], ""
        )

        status_text = f"""📊 현재 상태

Stress Level: {status['stress_level']}
Boss Alert Level: {status['boss_alert_level']}
Personality: {status['personality']}
Needs Break: {needs_break}
Recommended Actions: {', '.join(recommended) if recommended else 'None'}

{personality_msg}

{'⚠️ 스트레스가 높습니다! 답변 생성을 일시 중단하고 휴식을 취하세요!' if needs_break else '✅ 스트레스 수준이 양호합니다. 작업을 계속하세요.'}

📈 통계:
- 총 휴식 횟수: {status['total_breaks']}
- 총 스트레스 감소: {status['total_stress_reduced']}
- 걸린 횟수: {status['times_caught']}"""

        return status_text

    return check_stress
