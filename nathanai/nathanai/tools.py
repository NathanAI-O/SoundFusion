from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class Tool:
    name: str
    description: str
    run: Callable[[str], str]


def echo_tool_factory(prefix: str = "") -> Tool:
    def _run(input_text: str) -> str:
        return f"{prefix}{input_text}"

    return Tool(name="echo", description="Devuelve el mismo texto", run=_run)
