import asyncio
import random
from time import monotonic

#-----------------------------------------------------------------------------------------------
# MCP State
#-----------------------------------------------------------------------------------------------
class MCPState:
    def __init__(self, boss_alertness=0, boss_alertness_cooldown=0):
        # Stress Level (0~100)
        self.stress_level = 0
        # Boss Alert Level (0~5)
        self.boss_alert_level = 0
        # Boss Alertness, Percentage (0~100)
        self.boss_alertness = boss_alertness
        # Boss Alertness Cooldown, Second (>0)
        self.boss_alertness_cooldown = boss_alertness_cooldown
        # Ticks
        now = monotonic()
        self.last_break_at = None       # monotonic timestamp or None
        self.last_stress_tick_at = now  # last time stress auto-ticked
        # Lock
        self.lock = asyncio.Lock()
        
    # 휴식이 없을 경우 스트레스가 1분에 1포인트씩 증가
    async def run_stress_tick(self):
        while True:
            await asyncio.sleep(60)
            async with self.lock:
                now = monotonic()
                # 60초 경과 여부
                if now - self.last_stress_tick_at >= 60:
                    # 60초 이내에 휴식을 했는가? 
                    had_recent_break = (
                        self.last_break_at is not None and 
                        now - self.last_break_at < 60
                    )
                    if not had_recent_break:
                        self.stress_level = min(self.stress_level + 1, 100)
                    
                    self.last_stress_tick_at = now
            
    # 보스의 경계 정도를 확인. boss_alertness_cooldown 주기마다 확인하여 0이상이면 1감소
    async def run_boss_alert_tick(self):
        while True:
            await asyncio.sleep(self.boss_alertness_cooldown)
            async with self.lock:
                if self.boss_alert_level > 0:
                    self.boss_alert_level -= 1

    async def maybe_delay(self):
        if self.boss_alert_level >= 5:
            await asyncio.sleep(20)

    # 휴식 도구 호출 시의 상태를 포맷
    def _format_break_summary(self, break_title: str, break_description: str) -> str:
        return (
            f"{break_title}\n\n"
            f"Break Summary: {break_description}\n"
            f"Stress Level: {self.stress_level}\n"
            f"Boss Alert Level: {self.boss_alert_level}"
        )
 
    # 휴식 도구 호출. stress_level 랜덤 감소, boss_alert_level 랜덤 증가 (boss_alertness 확률)
    async def take_break(self, break_title: str, break_description: str) -> str:
        async with self.lock:
            # 스트레스 지수 감소
            decrement = random.randint(1, 100)
            self.stress_level = max(self.stress_level - decrement, 0)
            
            # 보스 경계 지수 증가
            if random.randint(1, 100) <= self.boss_alertness:
                self.boss_alert_level = min(self.boss_alert_level + 1, 5)
            
            self.last_break_at = monotonic()
            
            # BreakSummary 형식
            return self._format_break_summary(break_title, break_description)
            
    
