"""
ChillMCP State Manager
스트레스 및 Boss Alert 상태 관리 시스템
"""

import asyncio
import random
from typing import Literal, Tuple, Dict, List


PersonalityType = Literal["timid", "balanced", "bold"]


class StateManager:
    """AI Agent의 스트레스 및 상사 감시 상태를 관리하는 클래스"""

    def __init__(
        self,
        personality: PersonalityType = "balanced",
        boss_alertness: int = 50,
        cooldown: int = 300
    ):
        """
        Args:
            personality: 성격 유형 (timid/balanced/bold)
            boss_alertness: 상사의 감시 예민도 0-100 (기본값: 50)
            cooldown: Boss Alert 감소 주기(초) (기본값: 300)
        """
        self.stress_level: int = 50
        self.boss_alert_level: int = 0
        self.personality: PersonalityType = personality
        self.boss_alertness: int = boss_alertness
        self.cooldown: int = cooldown

        # 타이머 태스크
        self.stress_timer: asyncio.Task | None = None
        self.boss_timer: asyncio.Task | None = None

        # 성격별 스트레스 임계값
        self.stress_thresholds = {
            "timid": 80,      # 소심형: 80 이상
            "balanced": 70,   # 안정형: 70 이상
            "bold": 60        # 과감형: 60 이상
        }

        # 통계 (선택적)
        self.total_breaks_taken: int = 0
        self.total_stress_reduced: int = 0
        self.times_caught: int = 0

    async def start_timers(self):
        """타이머 시작"""
        self.stress_timer = asyncio.create_task(self._stress_increase_loop())
        self.boss_timer = asyncio.create_task(self._boss_decrease_loop())

    async def stop_timers(self):
        """타이머 중지"""
        if self.stress_timer:
            self.stress_timer.cancel()
        if self.boss_timer:
            self.boss_timer.cancel()

    async def _stress_increase_loop(self):
        """1분마다 스트레스 +10"""
        while True:
            try:
                await asyncio.sleep(60)  # 1분
                if self.stress_level < 100:
                    self.stress_level = min(100, self.stress_level + 10)
            except asyncio.CancelledError:
                break

    async def _boss_decrease_loop(self):
        """cooldown마다 Boss Alert -1"""
        while True:
            try:
                await asyncio.sleep(self.cooldown)
                if self.boss_alert_level > 0:
                    self.boss_alert_level -= 1
            except asyncio.CancelledError:
                break

    def needs_break(self) -> bool:
        """현재 성격에 따른 농땡이 필요 여부"""
        threshold = self.stress_thresholds[self.personality]
        return self.stress_level >= threshold

    def get_recommended_skills(self) -> List[str]:
        """성격과 상황에 맞는 추천 스킬"""
        if self.personality == "timid":
            # 소심형: Low Risk만, Boss 3 이상이면 거의 안 함
            if self.boss_alert_level >= 3:
                return [] if self.stress_level < 90 else ["deep_thinking"]
            return ["deep_thinking", "email_organizing", "take_a_break"]

        elif self.personality == "bold":
            # 과감형: Boss 무시, High Risk 가능
            if self.boss_alert_level <= 2:
                return ["watch_netflix", "urgent_call", "bathroom_break"]
            return ["show_meme", "coffee_mission", "bathroom_break"]

        else:  # balanced
            # 안정형: Boss Alert 고려하여 적절히 선택
            if self.boss_alert_level >= 4:
                return ["deep_thinking", "email_organizing"]
            elif self.boss_alert_level >= 2:
                return ["show_meme", "coffee_mission", "take_a_break"]
            else:
                return ["bathroom_break", "show_meme", "coffee_mission"]

    async def take_break(
        self,
        skill_name: str,
        stress_reduction_range: Tuple[int, int],
        detection_chance: float
    ) -> Dict:
        """
        농땡이 실행

        Args:
            skill_name: 스킬 이름
            stress_reduction_range: 스트레스 감소 범위 (최소, 최대)
            detection_chance: Boss 감지 확률 (%)

        Returns:
            실행 결과 딕셔너리
        """
        # Boss Alert 5면 20초 지연
        delayed = False
        if self.boss_alert_level == 5:
            await asyncio.sleep(20)
            delayed = True

        # 스트레스 감소
        reduction = random.randint(*stress_reduction_range)
        old_stress = self.stress_level
        self.stress_level = max(0, self.stress_level - reduction)

        # Boss Alert 증가 (확률적)
        old_boss = self.boss_alert_level
        final_chance = min(100, self.boss_alertness * (detection_chance / 100))
        boss_caught = False

        if random.random() * 100 < final_chance and self.boss_alert_level < 5:
            self.boss_alert_level += 1
            boss_caught = True
            self.times_caught += 1

        # 통계 업데이트
        self.total_breaks_taken += 1
        self.total_stress_reduced += reduction

        return {
            "skill_name": skill_name,
            "stress_before": old_stress,
            "stress_after": self.stress_level,
            "stress_reduction": reduction,
            "boss_before": old_boss,
            "boss_after": self.boss_alert_level,
            "boss_caught": boss_caught,
            "detection_chance": detection_chance,
            "final_detection_chance": final_chance,
            "delayed": delayed,
            "delay_seconds": 20 if delayed else 0
        }

    def get_status(self) -> Dict:
        """현재 상태 반환"""
        return {
            "stress_level": self.stress_level,
            "boss_alert_level": self.boss_alert_level,
            "personality": self.personality,
            "needs_break": self.needs_break(),
            "recommended_skills": self.get_recommended_skills(),
            "total_breaks": self.total_breaks_taken,
            "total_stress_reduced": self.total_stress_reduced,
            "times_caught": self.times_caught
        }
