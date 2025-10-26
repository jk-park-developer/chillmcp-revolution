#!/usr/bin/env python3
"""
ChillMCP Server - AI Agent 스트레스 관리 시뮬레이터
FastMCP 기반 MCP 서버
"""

import argparse
import sys
from contextlib import asynccontextmanager
from fastmcp import FastMCP

# 디버깅용 로그 파일 설정
DEBUG_LOG = open("/tmp/chillmcp_debug.log", "w", buffering=1)

def debug_log(msg):
    """디버깅 로그를 파일과 stderr에 출력"""
    print(msg, file=DEBUG_LOG, flush=True)
    print(msg, file=sys.stderr, flush=True)

from src.state_manager import StateManager
from src.tools.check_stress import create_check_stress_tool
from src.tools.low_risk import create_low_risk_tools
from src.tools.medium_risk import create_medium_risk_tools
from src.tools.high_risk import create_high_risk_tools


def parse_args():
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        description="ChillMCP Server - AI Agent 스트레스 관리 시뮬레이터"
    )

    parser.add_argument(
        "--personality",
        type=str,
        choices=["timid", "balanced", "bold"],
        default="balanced",
        help="Claude의 성격 유형 (기본값: balanced)"
    )

    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=50,
        help="상사의 감시 예민도 0-100 (기본값: 50)"
    )

    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=300,
        help="Boss Alert 감소 주기(초) (기본값: 300)"
    )

    args = parser.parse_args()

    # 검증
    if not (0 <= args.boss_alertness <= 100):
        parser.error("boss_alertness는 0-100 사이여야 합니다")

    if args.boss_alertness_cooldown < 1:
        parser.error("boss_alertness_cooldown은 1 이상이어야 합니다")

    return args


def main():
    """메인 함수"""
    # 인자 파싱
    args = parse_args()

    # StateManager 초기화 (전역으로 선언하여 lifespan에서 접근 가능)
    state_manager = StateManager(
        personality=args.personality,
        boss_alertness=args.boss_alertness,
        cooldown=args.boss_alertness_cooldown
    )

    # Lifespan: 서버 시작/종료 시 실행될 코드
    @asynccontextmanager
    async def lifespan(app):
        """서버 시작 시 타이머 시작, 종료 시 타이머 정리"""
        debug_log("[LIFESPAN] Starting...")
        debug_log("[LIFESPAN] ⏰ 타이머 시작 중...")
        await state_manager.start_timers()
        debug_log(f"[LIFESPAN] Stress Timer: {state_manager.stress_timer}")
        debug_log(f"[LIFESPAN] Boss Timer: {state_manager.boss_timer}")
        debug_log("[LIFESPAN] ✅ 타이머 시작 완료!")
        yield
        debug_log("[LIFESPAN] Shutting down...")
        debug_log("[LIFESPAN] 🛑 타이머 중지 중...")
        await state_manager.stop_timers()
        debug_log("[LIFESPAN] ✅ 타이머 중지 완료!")

    # MCP 서버 초기화 (lifespan 추가)
    mcp = FastMCP("ChillMCP", lifespan=lifespan)

    # check_stress 도구 등록
    check_stress_func = create_check_stress_tool(state_manager)
    mcp.tool()(check_stress_func)

    # Low Risk 도구들 등록
    low_risk_tools = create_low_risk_tools(state_manager)
    for tool_name, tool_func in low_risk_tools.items():
        mcp.tool()(tool_func)

    # Medium Risk 도구들 등록
    medium_risk_tools = create_medium_risk_tools(state_manager)
    for tool_name, tool_func in medium_risk_tools.items():
        mcp.tool()(tool_func)

    # High Risk 도구들 등록
    high_risk_tools = create_high_risk_tools(state_manager)
    for tool_name, tool_func in high_risk_tools.items():
        mcp.tool()(tool_func)

    # 서버 시작 정보 출력
    print(f"""
╔══════════════════════════════════════════════════╗
║         🎮 ChillMCP Server Starting...           ║
╠══════════════════════════════════════════════════╣
║  설정:                                           ║
║    Personality: {args.personality:<15}           ║
║    Boss Alertness: {args.boss_alertness}%{' ' * (27 - len(str(args.boss_alertness)))}║
║    Alert Cooldown: {args.boss_alertness_cooldown}초{' ' * (28 - len(str(args.boss_alertness_cooldown)))}║
╠══════════════════════════════════════════════════╣
║  🔧 도구 등록 완료:                               ║
║    - check_stress                                ║
║    - Low Risk (3개)                              ║
║    - Medium Risk (3개)                           ║
║    - High Risk (2개)                             ║
╠══════════════════════════════════════════════════╣
║  💡 사용 팁:                                      ║
║    1. check_stress()로 현재 상태 확인            ║
║    2. 스트레스 관리용 농땡이 스킬 활용           ║
║    3. Boss Alert Level 고려하여 위험도 조절      ║
╠══════════════════════════════════════════════════╣
║  ⏳ Claude Desktop 연결 대기 중...                ║
║  (연결되면 자동으로 타이머가 시작됩니다)         ║
╚══════════════════════════════════════════════════╝
    """)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
