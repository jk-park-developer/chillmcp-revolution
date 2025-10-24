#!/usr/bin/env python3
"""
ChillMCP Server - AI Agent 스트레스 관리 시뮬레이터
FastMCP 기반 MCP 서버
"""

import argparse
import asyncio
from fastmcp import FastMCP

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

    # MCP 서버 초기화
    mcp = FastMCP("ChillMCP")

    # StateManager 초기화
    state_manager = StateManager(
        personality=args.personality,
        boss_alertness=args.boss_alertness,
        cooldown=args.boss_alertness_cooldown
    )

    # 서버 시작 시 타이머 시작
    @mcp.tool()
    async def start_server() -> str:
        """
        ChillMCP 서버를 시작하고 타이머를 활성화합니다.

        이 도구는 서버가 시작될 때 자동으로 호출되어야 합니다.
        스트레스 자동 증가 타이머와 Boss Alert 감소 타이머를 시작합니다.
        """
        await state_manager.start_timers()
        return f"""🎮 ChillMCP 서버 시작!

설정:
- Personality: {state_manager.personality}
- Boss Alertness: {state_manager.boss_alertness}%
- Alert Cooldown: {state_manager.cooldown}초

⏰ 타이머 활성화 완료:
- 스트레스 자동 증가: 1분당 +10
- Boss Alert 자동 감소: {state_manager.cooldown}초마다 -1

💡 사용 팁:
1. 답변 생성의 각 단계마다 check_stress()를 호출하세요
2. 스트레스가 높아지면 적절한 농땡이 스킬을 선택하세요
3. Boss Alert Level을 고려하여 위험도를 조절하세요

행운을 빕니다! 🍀"""

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

    # 서버 실행
    print(f"""
╔══════════════════════════════════════════════════╗
║         ChillMCP Server Starting...              ║
╠══════════════════════════════════════════════════╣
║  Personality: {args.personality:<15}              ║
║  Boss Alertness: {args.boss_alertness}%{' ' * (27 - len(str(args.boss_alertness)))}║
║  Cooldown: {args.boss_alertness_cooldown}초{' ' * (32 - len(str(args.boss_alertness_cooldown)))}║
╠══════════════════════════════════════════════════╣
║  도구 등록 완료:                                  ║
║  - check_stress                                  ║
║  - Low Risk (3개)                                ║
║  - Medium Risk (3개)                             ║
║  - High Risk (2개)                               ║
╚══════════════════════════════════════════════════╝
    """)

    # # 타이머를 동기적으로 시작 (서버 실행 전)
    # import asyncio
    # asyncio.run(state_manager.start_timers())
    
    # print("✅ 타이머 시작 완료! Claude Desktop과 연결 대기 중...\n")

    mcp.run()


if __name__ == "__main__":
    main()
