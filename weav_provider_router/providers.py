from __future__ import annotations

from typing import Optional

from .base import LLMBase
from .adapters.openai import OpenAIChat
from .adapters.anthropic import AnthropicChat
from .adapters.google import GoogleChat
from .adapters.ollama import OllamaChat
from .adapters.deepseek import DeepSeekChat
from .adapters.qwen import QwenChat
from .adapters.zhipu import ZhipuChat


PROVIDER_CLASSES = {
    "openai": OpenAIChat,
    "anthropic": AnthropicChat,
    "google": GoogleChat,
    "ollama": OllamaChat,
    "deepseek": DeepSeekChat,
    "qwen": QwenChat,
    "zhipu": ZhipuChat,
}


def build_provider(provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None) -> LLMBase:
    """Construct and return a provider adapter instance."""
    p = provider.lower()
    if p not in PROVIDER_CLASSES:
        raise ValueError(f"Unsupported provider: {provider}")

    cls = PROVIDER_CLASSES[p]

    if p == "ollama":
        return cls(base_url=base_url or "http://localhost:11434")  # type: ignore[call-arg]

    if p in {"openai", "deepseek", "qwen", "zhipu"}:
        return cls(api_key=api_key, base_url=base_url)  # type: ignore[call-arg]

    return cls(api_key=api_key)  # type: ignore[call-arg]


__all__ = ["PROVIDER_CLASSES", "build_provider"]
