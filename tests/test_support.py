"""Helpers to prepare the test environment for chill-mcp."""

import sys
from pathlib import Path
from types import ModuleType


def _add_project_root_to_path() -> None:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def _ensure_fastmcp_stub() -> None:
    try:
        import fastmcp as fastmcp_module  # type: ignore
    except ImportError:  # pragma: no cover - exercised only when fastmcp missing
        fastmcp_module = ModuleType("fastmcp")
        sys.modules["fastmcp"] = fastmcp_module

    if not hasattr(fastmcp_module, "FastMCP"):
        class _FastMCPStub:  # pragma: no cover
            def __init__(self, *_, **__):
                pass

            def run(self, *_, **__):
                raise RuntimeError("FastMCP stub should not run during tests")

        fastmcp_module.FastMCP = _FastMCPStub  # type: ignore[attr-defined]

    if not hasattr(fastmcp_module, "tool"):
        def _tool_stub(*_, **__):  # pragma: no cover
            def decorator(func):
                return func

            return decorator

        fastmcp_module.tool = _tool_stub  # type: ignore[attr-defined]


_add_project_root_to_path()
_ensure_fastmcp_stub()
