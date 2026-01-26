from __future__ import annotations

import asyncio
from typing import Any, Optional

from .base import CompletionConfig
from .providers import build_provider


async def chat_async(
    provider: str,
    api_key: Optional[str],
    question: str,
    *,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    top_p: float = 1.0,
    stop: Optional[list[str]] = None,
    extra: Optional[dict[str, Any]] = None,
) -> str:
    if not model:
        raise ValueError("model parameter is required and cannot be empty")
    
    llm = build_provider(provider, api_key=api_key, base_url=base_url)
    cfg = CompletionConfig(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stop=stop,
        extra=extra or {},
    )
    messages = [{"role": "user", "content": question}]
    return await llm.chat(messages, cfg)


def chat(
    provider: str,
    api_key: Optional[str],
    question: str,
    **kwargs: Any,
) -> str:
    """Synchronous wrapper for chat_async.
    
    Note: If you're already in an async context, use chat_async() directly.
    This function will raise RuntimeError if called within a running event loop.
    """
    try:
        return asyncio.run(chat_async(provider, api_key, question, **kwargs))
    except RuntimeError as e:
        if "already running" in str(e).lower():
            raise RuntimeError(
                "Cannot use synchronous chat() within an async context. "
                "Please use chat_async() instead."
            ) from e
        raise


async def complete_async(
    provider: str,
    api_key: Optional[str],
    prompt: str,
    *,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    top_p: float = 1.0,
    stop: Optional[list[str]] = None,
    extra: Optional[dict[str, Any]] = None,
) -> str:
    if not model:
        raise ValueError("model parameter is required and cannot be empty")
    
    llm = build_provider(provider, api_key=api_key, base_url=base_url)
    cfg = CompletionConfig(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stop=stop,
        extra=extra or {},
    )
    return await llm.complete(prompt, cfg)


def complete(
    provider: str,
    api_key: Optional[str],
    prompt: str,
    **kwargs: Any,
) -> str:
    """Synchronous wrapper for complete_async.
    
    Note: If you're already in an async context, use complete_async() directly.
    This function will raise RuntimeError if called within a running event loop.
    """
    try:
        return asyncio.run(complete_async(provider, api_key, prompt, **kwargs))
    except RuntimeError as e:
        if "already running" in str(e).lower():
            raise RuntimeError(
                "Cannot use synchronous complete() within an async context. "
                "Please use complete_async() instead."
            ) from e
        raise


def list_models(
    provider: str,
    api_key: Optional[str] = None,
    *,
    base_url: Optional[str] = None,
) -> list[str]:
    llm = build_provider(provider, api_key=api_key, base_url=base_url)
    return llm.list_models()


__all__ = [
    "chat_async",
    "chat",
    "complete_async",
    "complete",
    "list_models",
]
