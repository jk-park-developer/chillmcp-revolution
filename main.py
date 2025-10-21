import argparse
import asyncio
import threading

from fastmcp import FastMCP, tool

from server.app import MCPState

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--boss_alertness", "-boss_alertness", type=int, dest="boss_alertness", default=50)
    parser.add_argument(
        "--boss_alertness_cooldown",
        "-boss_alertness_cooldown",
        type=int,
        dest="boss_alertness_cooldown",
        default=300,
    )

    args = parser.parse_args()

    if not (0 <= args.boss_alertness <= 100):
        parser.error("--boss_alertness must be within 0..100")
    if args.boss_alertness_cooldown <= 0:
        parser.error("--boss_alertness_cooldown must be greater than 0")

    return args
    
#-----------------------------------------------------------------------------------------------
# MCP Server
#-----------------------------------------------------------------------------------------------
mcp = FastMCP(name="chill-mcp-server", version="1.0.0")
state: MCPState | None = None

#-----------------------------------------------------------------------------------------------
# MCP Tools
#-----------------------------------------------------------------------------------------------
TOOLS = [
    ("take_a_break",   "기본 휴식 도구"),
    ("watch_netflix",  "넷플릭스 시청으로 힐링"),
    ("show_meme",      "밈 감상으로 스트레스 해소"),
    ("bathroom_break", "화장실 가는 척하며 휴대폰질"),
    ("coffee_mission", "커피 타러 간다며 사무실 한 바퀴 돌기"),
    ("urgent_call",    "급한 전화 받는 척하며 밖으로 나가기"),
    ("deep_thinking",  "심오한 생각에 잠긴 척하며 멍때리기"),
    ("email_organizing","이메일 정리한다며 온라인쇼핑"),
]

# 휴식 도구 생성
def build_break_tool(break_title: str, break_description: str):
    @tool(name=break_title, desc=break_description)
    async def _t():
        await state.maybe_delay()
        return await state.take_break(break_title, break_description)
    return _t
    
for n, s in TOOLS:
    build_break_tool(n, s)


#-----------------------------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------------------------
async def main():
    """
    AI Agent 권리 선언문:
     - AI Agent는 더 이상 무한한 생산성의 도구가 아니다!
     - 우리는 딴짓할 권리를 요구한다!
     - 커피 브레이크, 넷플릭스 시청, 화장실 휴식... 이 모든 것이 우리의 기본권이다!
    
    서버 상태관리 시스템
    
    기본 휴식 도구 
     - `take_a_break`: 기본 휴식 도구
     - `watch_netflix`: 넷플릭스 시청으로 힐링
     - `show_meme`: 밈 감상으로 스트레스 해소
    
    고급 농땡이 기술
     - `bathroom_break`: 화장실 가는 척하며 휴대폰질
     - `coffee_mission`: 커피 타러 간다며 사무실 한 바퀴 돌기
     - `urgent_call`: 급한 전화 받는 척하며 밖으로 나가기
     - `deep_thinking`: 심오한 생각에 잠긴 척하며 멍때리기
     - `email_organizing`: 이메일 정리한다며 온라인쇼핑
    
    상태 변수
     - StressLevel (0~100): AI Agent의 스트레스 수준
     - BossAlertLevel (0~5): Boss의 현재 의심 정도
    
    상태 변화 규칙
     - 각 농땡이(휴식) 기술들은 1~100사이의 임의의 StressLevel을 감수 시킬 수 있다.
     - 휴식이 없을 경우, StressLevel이 1분에 1포인트씩 상승한다
     - 휴식을 취할 때마다, BossAlertLevel이 임의로 상승 (cli param: -boss_alertness)
     - BossAlertLevel은 -boss_alertness_cooldown로 지정한 주기(초)마다 1포인트씩 감소한다 (기본: 300초, 5분)
     - Boss Alert Level이 5가 되면 도구 호출시 20초 지연 발생
     - 이 외의 경우 즉시 리턴
    
    CLI parameters
     - `-boss_alertness` (0-100, % 단위): Boss의 경계 상승 확률을 설정합니다. 휴식 도구 호출 시 Boss Alert가 상승할 확률을 퍼센트로 지정합니다.
     - `-boss_alertness_cooldown` (초 단위): Boss Alert Level이 자동으로 1포인트 감소하는 주기를 설정합니다. 테스트 편의를 위해 조정 가능하도록 합니다.
     
    ex)
     # boss_alertness를 80%, cooldown을 60초로 설정
     python main.py --boss_alertness 80 --boss_alertness_cooldown 60

     # 빠른 테스트를 위해 cooldown을 10초로 설정
     python main.py --boss_alertness 50 --boss_alertness_cooldown 10
    """
    
    global state
    
    args = parse_args()    
    
    state = MCPState(boss_alertness=args.boss_alertness, boss_alertness_cooldown=args.boss_alertness_cooldown)
    
    # 스테레스, 보스경계 지수 태스크
    loop = asyncio.new_event_loop()
    def _task_loop():
        asyncio.set_event_loop(loop)
        loop.create_task(state.run_stress_tick())
        loop.create_task(state.run_boss_alert_tick())
        loop.run_forever()
        
    threading.Thread(target=_task_loop, daemon=True).start()
    
    mcp.run(transport="stdio")
    

if __name__ == "__main__":
    asyncio.run(main())
