from __future__ import annotations

import os
from typing import List, Dict, Any


class MockProvider:
    def generate(self, messages: List[Dict[str, str]], model: str, **kwargs: Any) -> str:
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return f"[mock:{model}] {last_user}"


class OpenAIProvider:
    def __init__(self) -> None:
        try:
            from openai import OpenAI  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "openai package not installed. Install with 'pip install openai'."
            ) from exc
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, messages: List[Dict[str, str]], model: str, **kwargs: Any) -> str:  # pragma: no cover
        # Compatible with the new OpenAI responses API
        completion = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
        return completion.choices[0].message.content or ""
