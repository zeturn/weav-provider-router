from __future__ import annotations

from typing import Optional, Union

from .base import LLMBase, ImageBase, EmbeddingBase
from .adapters.openai import OpenAIChat
from .adapters.anthropic import AnthropicChat
from .adapters.google import GoogleChat
from .adapters.ollama import OllamaChat
from .adapters.deepseek import DeepSeekChat
from .adapters.qwen import QwenChat
from .adapters.zhipu import ZhipuChat
from .adapters.moonshot import MoonshotChat
from .adapters.baidu import BaiduChat
from .adapters.mistral import MistralChat
from .adapters.groq import GroqChat
from .adapters.together import TogetherChat
from .adapters.cohere import CohereChat
from .adapters.minimax import MiniMaxChat
from .adapters.bytedance import ByteDanceChat
from .adapters.nvidia import NVIDIAChat
from .adapters.openai_image import OpenAIImage
from .adapters.openai_embedding import OpenAIEmbedding


# LLM providers
LLM_PROVIDER_CLASSES = {
    "openai": OpenAIChat,
    "anthropic": AnthropicChat,
    "google": GoogleChat,
    "ollama": OllamaChat,
    "deepseek": DeepSeekChat,
    "qwen": QwenChat,
    "zhipu": ZhipuChat,
    "moonshot": MoonshotChat,
    "baidu": BaiduChat,
    "mistral": MistralChat,
    "groq": GroqChat,
    "together": TogetherChat,
    "cohere": CohereChat,
    "minimax": MiniMaxChat,
    "bytedance": ByteDanceChat,
    "nvidia": NVIDIAChat,
}

# Image generation providers
IMAGE_PROVIDER_CLASSES = {
    "openai": OpenAIImage,
    "dall-e": OpenAIImage,  # Alias
}

# Embedding providers
EMBEDDING_PROVIDER_CLASSES = {
    "openai": OpenAIEmbedding,
}

# Legacy: Keep PROVIDER_CLASSES for backward compatibility
PROVIDER_CLASSES = LLM_PROVIDER_CLASSES


def build_provider(provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs) -> LLMBase:
    """Construct and return an LLM provider adapter instance.
    
    Args:
        provider: Provider name (e.g., 'openai', 'anthropic')
        api_key: API key for authentication
        base_url: Optional custom base URL to override default endpoint
        **kwargs: Additional provider-specific parameters (e.g., secret_key for Baidu, group_id for MiniMax)
    
    Returns:
        LLMBase: Configured provider instance
    """
    p = provider.lower()
    if p not in LLM_PROVIDER_CLASSES:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    cls = LLM_PROVIDER_CLASSES[p]

    # Special cases with unique parameters
    if p == "ollama":
        return cls(base_url=base_url or "http://localhost:11434")  # type: ignore[call-arg]

    if p == "baidu":
        secret_key = kwargs.get("secret_key")
        return cls(api_key=api_key, secret_key=secret_key, base_url=base_url)  # type: ignore[call-arg]
    
    if p == "minimax":
        group_id = kwargs.get("group_id")
        return cls(api_key=api_key, group_id=group_id, base_url=base_url)  # type: ignore[call-arg]

    # All other providers support standard api_key + base_url pattern
    return cls(api_key=api_key, base_url=base_url)  # type: ignore[call-arg]


def build_image_provider(provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs) -> ImageBase:
    """Construct and return an image generation provider adapter instance.
    
    Args:
        provider: Provider name (e.g., 'openai', 'dall-e')
        api_key: API key for authentication
        base_url: Optional custom base URL to override default endpoint
        **kwargs: Additional provider-specific parameters
    
    Returns:
        ImageBase: Configured image provider instance
    """
    p = provider.lower()
    if p not in IMAGE_PROVIDER_CLASSES:
        raise ValueError(f"Unsupported image provider: {provider}")

    cls = IMAGE_PROVIDER_CLASSES[p]
    return cls(api_key=api_key, base_url=base_url)  # type: ignore[call-arg]


def build_embedding_provider(provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs) -> EmbeddingBase:
    """Construct and return an embedding provider adapter instance.
    
    Args:
        provider: Provider name (e.g., 'openai')
        api_key: API key for authentication
        base_url: Optional custom base URL to override default endpoint
        **kwargs: Additional provider-specific parameters
    
    Returns:
        EmbeddingBase: Configured embedding provider instance
    """
    p = provider.lower()
    if p not in EMBEDDING_PROVIDER_CLASSES:
        raise ValueError(f"Unsupported embedding provider: {provider}")

    cls = EMBEDDING_PROVIDER_CLASSES[p]
    return cls(api_key=api_key, base_url=base_url)  # type: ignore[call-arg]


__all__ = [
    "LLM_PROVIDER_CLASSES",
    "IMAGE_PROVIDER_CLASSES",
    "EMBEDDING_PROVIDER_CLASSES",
    "PROVIDER_CLASSES",  # Legacy
    "build_provider",
    "build_image_provider",
    "build_embedding_provider",
]
