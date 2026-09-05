"""
Client LLM abstrait - Permet de switcher entre Claude, OpenAI, etc.
via une simple variable d'environnement.
"""

import os
import json
from typing import Any


class LLMClient:
    """Client unifié pour appeler différents LLM providers."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "anthropic")
        self._client = None
        self._model = None
        self._init_client()

    def _init_client(self):
        if self.provider == "anthropic":
            from anthropic import Anthropic
            self._client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self._model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

        elif self.provider in ("openai", "openai_compatible"):
            from openai import OpenAI
            kwargs = {"api_key": os.getenv("OPENAI_API_KEY")}
            if os.getenv("OPENAI_BASE_URL"):
                kwargs["base_url"] = os.getenv("OPENAI_BASE_URL")
            self._client = OpenAI(**kwargs)
            self._model = os.getenv("OPENAI_MODEL", "gpt-4o")

        else:
            raise ValueError(f"Provider inconnu: {self.provider}")

    def chat(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[dict] | None = None,
        temperature: float = 0.3,
    ) -> dict:
        """
        Envoie un message au LLM et retourne la réponse.
        Gère automatiquement les tool calls si des tools sont fournis.
        """
        if self.provider == "anthropic":
            return self._call_anthropic(system_prompt, user_message, tools, temperature)
        else:
            return self._call_openai(system_prompt, user_message, tools, temperature)

    def _call_anthropic(self, system_prompt, user_message, tools, temperature):
        kwargs = {
            "model": self._model,
            "max_tokens": 4096,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
        if tools:
            kwargs["tools"] = tools

        response = self._client.messages.create(**kwargs)

        result = {"text": "", "tool_calls": []}
        for block in response.content:
            if block.type == "text":
                result["text"] += block.text
            elif block.type == "tool_use":
                result["tool_calls"].append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                })
        return result

    def _call_openai(self, system_prompt, user_message, tools, temperature):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        kwargs = {
            "model": self._model,
            "temperature": temperature,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = [
                {"type": "function", "function": t} for t in tools
            ]

        response = self._client.chat.completions.create(**kwargs)
        choice = response.choices[0]

        result = {"text": choice.message.content or "", "tool_calls": []}
        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                result["tool_calls"].append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "input": json.loads(tc.function.arguments),
                })
        return result


# Singleton
_llm_client = None

def get_llm_client() -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
