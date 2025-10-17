from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Protocol, Optional, Iterable

from .tools import Tool


class Provider(Protocol):
    def generate(self, messages: List[Dict[str, str]], model: str, **kwargs: Any) -> str: ...


@dataclass
class Message:
    role: str
    content: str


@dataclass
class NathanAgent:
    provider: Provider
    model: str = "mock"
    system_prompt: Optional[str] = None
    memory: List[Message] = field(default_factory=list)
    tools: List[Tool] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.memory.append(Message(role=role, content=content))

    def build_messages(self, user_message: str) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        for m in self.memory:
            messages.append({"role": m.role, "content": m.content})
        messages.append({"role": "user", "content": user_message})
        return messages

    def chat(self, user_message: str, **kwargs: Any) -> str:
        # naive tool call: if message starts with !tool <input>, run first tool
        if self.tools and user_message.startswith("!tool "):
            tool_input = user_message[len("!tool ") :]
            tool = self.tools[0]
            response = tool.run(tool_input)
        else:
            messages = self.build_messages(user_message)
            response = self.provider.generate(messages=messages, model=self.model, **kwargs)
        self.add_message("user", user_message)
        self.add_message("assistant", response)
        return response
