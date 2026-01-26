"""Base classes and interfaces for LLM providers."""

from __future__ import annotations
from typing import Any, AsyncIterator
from dataclasses import dataclass, field


@dataclass
class CompletionConfig:
    """Configuration for LLM completion requests."""

    model: str
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float = 1.0
    stop: list[str] | None = None
    extra: dict[str, Any] = field(default_factory=dict)


class LLMBase:
    """Base interface for all LLM provider adapters."""

    async def chat(self, messages: list[dict[str, str]], config: CompletionConfig) -> str:
        """
        Send chat messages and get a response.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            config: Completion configuration

        Returns:
            Generated response text
        """
        raise NotImplementedError

    async def complete(self, prompt: str, config: CompletionConfig) -> str:
        """
        Complete a text prompt.

        Args:
            prompt: Text prompt to complete
            config: Completion configuration

        Returns:
            Completed text
        """
        raise NotImplementedError

    async def stream(self, messages: list[dict[str, str]], config: CompletionConfig) -> AsyncIterator[str]:
        """
        Stream chat responses.

        Args:
            messages: List of message dictionaries
            config: Completion configuration

        Yields:
            Text chunks as they arrive
        """
        raise NotImplementedError
        # Make this a generator
        yield ""  # pragma: no cover

    def list_models(self) -> list[str]:
        """
        List available models for this provider.

        Returns:
            List of model identifiers
        """
        raise NotImplementedError


__all__ = ["CompletionConfig", "LLMBase"]
