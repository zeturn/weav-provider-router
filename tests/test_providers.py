"""Unit tests for provider builder and registry."""

import pytest
from weav_provider_router.providers import build_provider, PROVIDER_CLASSES
from weav_provider_router.adapters.openai import OpenAIChat
from weav_provider_router.adapters.anthropic import AnthropicChat
from weav_provider_router.adapters.google import GoogleChat
from weav_provider_router.adapters.ollama import OllamaChat
from weav_provider_router.adapters.deepseek import DeepSeekChat
from weav_provider_router.adapters.qwen import QwenChat
from weav_provider_router.adapters.zhipu import ZhipuChat
from weav_provider_router.adapters.moonshot import MoonshotChat
from weav_provider_router.adapters.baidu import BaiduChat
from weav_provider_router.adapters.mistral import MistralChat
from weav_provider_router.adapters.groq import GroqChat
from weav_provider_router.adapters.together import TogetherChat
from weav_provider_router.adapters.cohere import CohereChat


@pytest.mark.unit
class TestProviderRegistry:
    """Tests for provider registry."""

    def test_all_providers_registered(self):
        """Test that all expected providers are registered."""
        expected_providers = [
            "openai",
            "anthropic",
            "google",
            "ollama",
            "deepseek",
            "qwen",
            "zhipu",
            "moonshot",
            "baidu",
            "mistral",
            "groq",
            "together",
            "cohere",
        ]
        for provider in expected_providers:
            assert provider in PROVIDER_CLASSES

    def test_provider_classes_mapping(self):
        """Test that provider classes are correctly mapped."""
        assert PROVIDER_CLASSES["openai"] == OpenAIChat
        assert PROVIDER_CLASSES["anthropic"] == AnthropicChat
        assert PROVIDER_CLASSES["google"] == GoogleChat
        assert PROVIDER_CLASSES["ollama"] == OllamaChat
        assert PROVIDER_CLASSES["deepseek"] == DeepSeekChat
        assert PROVIDER_CLASSES["qwen"] == QwenChat
        assert PROVIDER_CLASSES["zhipu"] == ZhipuChat
        assert PROVIDER_CLASSES["moonshot"] == MoonshotChat
        assert PROVIDER_CLASSES["baidu"] == BaiduChat
        assert PROVIDER_CLASSES["mistral"] == MistralChat
        assert PROVIDER_CLASSES["groq"] == GroqChat
        assert PROVIDER_CLASSES["together"] == TogetherChat
        assert PROVIDER_CLASSES["cohere"] == CohereChat
        assert PROVIDER_CLASSES["zhipu"] == ZhipuChat


@pytest.mark.unit
class TestBuildProvider:
    """Tests for build_provider function."""

    def test_build_openai_provider(self):
        """Test building OpenAI provider."""
        provider = build_provider("openai", api_key="test-key")
        assert isinstance(provider, OpenAIChat)

    def test_build_openai_with_base_url(self):
        """Test building OpenAI provider with custom base URL."""
        provider = build_provider("openai", api_key="test-key", base_url="https://custom.com")
        assert isinstance(provider, OpenAIChat)

    def test_build_anthropic_provider(self):
        """Test building Anthropic provider."""
        provider = build_provider("anthropic", api_key="test-key")
        assert isinstance(provider, AnthropicChat)

    def test_build_google_provider(self):
        """Test building Google provider."""
        pytest.importorskip("google.generativeai", reason="google-generativeai not installed")
        provider = build_provider("google", api_key="test-key")
        assert isinstance(provider, GoogleChat)

    def test_build_ollama_provider(self):
        """Test building Ollama provider."""
        provider = build_provider("ollama")
        assert isinstance(provider, OllamaChat)

    def test_build_ollama_with_custom_url(self):
        """Test building Ollama provider with custom URL."""
        provider = build_provider("ollama", base_url="http://custom:11434")
        assert isinstance(provider, OllamaChat)

    def test_build_deepseek_provider(self):
        """Test building DeepSeek provider."""
        provider = build_provider("deepseek", api_key="test-key")
        assert isinstance(provider, DeepSeekChat)

    def test_build_qwen_provider(self):
        """Test building Qwen provider."""
        provider = build_provider("qwen", api_key="test-key")
        assert isinstance(provider, QwenChat)

    def test_build_zhipu_provider(self):
        """Test building Zhipu provider."""
        provider = build_provider("zhipu", api_key="test-key")
        assert isinstance(provider, ZhipuChat)

    def test_build_moonshot_provider(self):
        """Test building Moonshot provider."""
        provider = build_provider("moonshot", api_key="test-key")
        assert isinstance(provider, MoonshotChat)

    def test_build_baidu_provider(self):
        """Test building Baidu provider."""
        provider = build_provider("baidu", api_key="test-key", secret_key="test-secret")
        assert isinstance(provider, BaiduChat)

    def test_build_mistral_provider(self):
        """Test building Mistral provider."""
        provider = build_provider("mistral", api_key="test-key")
        assert isinstance(provider, MistralChat)

    def test_build_groq_provider(self):
        """Test building Groq provider."""
        provider = build_provider("groq", api_key="test-key")
        assert isinstance(provider, GroqChat)

    def test_build_together_provider(self):
        """Test building Together AI provider."""
        provider = build_provider("together", api_key="test-key")
        assert isinstance(provider, TogetherChat)

    def test_build_cohere_provider(self):
        """Test building Cohere provider."""
        provider = build_provider("cohere", api_key="test-key")
        assert isinstance(provider, CohereChat)

    def test_case_insensitive_provider_name(self):
        """Test that provider names are case-insensitive."""
        provider1 = build_provider("OpenAI", api_key="test-key")
        provider2 = build_provider("OPENAI", api_key="test-key")
        provider3 = build_provider("openai", api_key="test-key")
        assert all(isinstance(p, OpenAIChat) for p in [provider1, provider2, provider3])

    def test_unsupported_provider_raises_error(self):
        """Test that unsupported provider raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported provider: unknown"):
            build_provider("unknown", api_key="test-key")

    def test_build_provider_without_api_key(self):
        """Test building provider without API key (for Ollama)."""
        provider = build_provider("ollama")
        assert isinstance(provider, OllamaChat)
