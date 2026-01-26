from __future__ import annotations

from typing import Any, AsyncIterator

from ..base import CompletionConfig, LLMBase


class DeepSeekChat(LLMBase):
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        try:
            from openai import AsyncOpenAI
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("openai package required. Install it to use DeepSeekChat.") from exc
        base_url = base_url or "https://api.deepseek.com"
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._api_key = api_key
        self._base_url = base_url

    async def chat(self, messages: list[dict[str, str]], config: CompletionConfig) -> str:
        resp = await self._client.chat.completions.create(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens or 1024,
            temperature=config.temperature,
        )
        return resp.choices[0].message.content or ""

    async def complete(self, prompt: str, config: CompletionConfig) -> str:
        return await self.chat([{"role": "user", "content": prompt}], config)

    async def stream(self, messages: list[dict[str, str]], config: CompletionConfig) -> AsyncIterator[str]:
        stream = await self._client.chat.completions.create(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens or 1024,
            temperature=config.temperature,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def list_models(self) -> list[str]:
        """List available DeepSeek models (dynamically fetched)."""
        import json
        from urllib import request as urlrequest
        
        default_models = [
            "deepseek-chat",
            "deepseek-coder",
            "deepseek-reasoner",
        ]
        
        if not self._api_key:
            return default_models
            
        try:
            base_url = self._base_url or "https://api.deepseek.com"
            url = f"{base_url.rstrip('/')}/v1/models"
            req = urlrequest.Request(
                url,
                headers={"Authorization": f"Bearer {self._api_key}"}
            )
            with urlrequest.urlopen(req, timeout=10) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            data = payload.get("data", [])
            models = [
                model_id
                for item in data
                if isinstance(item, dict) and isinstance(model_id := item.get("id"), str)
            ]
            return models if models else default_models
        except Exception:
            return default_models
