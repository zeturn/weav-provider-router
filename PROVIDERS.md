# Provider Reference Guide

Quick reference for all supported LLM providers in weav-provider-router.

## Provider Overview

| Provider | Region | Type | Special Auth | Speed | Cost |
|----------|--------|------|--------------|-------|------|
| OpenAI | 🌍 Global | Commercial | API Key | Medium | High |
| Anthropic | 🌍 Global | Commercial | API Key | Medium | High |
| Google | 🌍 Global | Commercial | API Key | Medium | Medium |
| Moonshot | 🇨🇳 China | Commercial | API Key | Medium | Medium |
| Baidu | 🇨🇳 China | Commercial | API Key + Secret | Medium | Low |
| Mistral | 🇪🇺 Europe | Commercial/OSS | API Key | Fast | Medium |
| Groq | 🌍 Global | Inference | API Key | Ultra-Fast | Low |
| Together AI | 🌍 Global | Aggregator | API Key | Fast | Low |
| Cohere | 🌍 Global | Commercial | API Key | Medium | Medium |
| DeepSeek | 🇨🇳 China | Commercial | API Key | Medium | Low |
| Qwen | 🇨🇳 China | Commercial | API Key | Medium | Low |
| Zhipu | 🇨🇳 China | Commercial | API Key | Medium | Low |
| Ollama | 💻 Local | Local | None | Fast | Free |

## Quick Start Examples

### OpenAI (GPT Models)

```python
from weav_provider_router import chat

response = chat(
    provider="openai",
    api_key="sk-...",
    question="Explain quantum computing",
    model="gpt-4"
)
```

**Models**: gpt-4, gpt-4o, gpt-3.5-turbo, o1-preview, o1-mini

### Anthropic (Claude)

```python
response = chat(
    provider="anthropic",
    api_key="sk-ant-...",
    question="Write a poem",
    model="claude-3-5-sonnet-20241022"
)
```

**Models**: claude-3-5-sonnet-20241022, claude-3-opus-20240229, claude-3-haiku-20240307

### Google (Gemini)

```python
response = chat(
    provider="google",
    api_key="AIza...",
    question="What is AI?",
    model="gemini-1.5-pro"
)
```

**Models**: gemini-1.5-pro, gemini-1.5-flash, gemini-pro

### Moonshot (Kimi / 月之暗面)

Long-context Chinese LLM specialist.

```python
response = chat(
    provider="moonshot",
    api_key="sk-...",
    question="总结这篇长文章...",
    model="moonshot-v1-128k"
)
```

**Models**: moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k

**Specialty**: Ultra-long context windows (up to 128K tokens)

### Baidu ERNIE (文心一言)

Chinese enterprise LLM with unique authentication.

```python
from weav_provider_router.providers import build_provider
from weav_provider_router.base import CompletionConfig

# Note: Baidu requires both API key and secret key
llm = build_provider(
    provider="baidu",
    api_key="your-api-key",
    secret_key="your-secret-key"  # Required!
)

config = CompletionConfig(model="ernie-4.0-8k", temperature=0.7)
messages = [{"role": "user", "content": "你好"}]
response = await llm.chat(messages, config)
```

**Models**: ernie-4.0-8k, ernie-3.5-8k, ernie-3.5-128k, ernie-speed-128k, ernie-lite-8k, ernie-tiny-8k

**Special**: Uses OAuth authentication (requires both api_key and secret_key)

### Mistral AI

European AI provider with strong open-source options.

```python
response = chat(
    provider="mistral",
    api_key="...",
    question="Explain machine learning",
    model="mistral-large-latest"
)
```

**Models**: mistral-large-latest, mistral-medium-latest, mistral-small-latest, open-mistral-7b, open-mixtral-8x7b, open-mixtral-8x22b

### Groq

Ultra-fast inference platform (up to 750 tokens/second).

```python
response = chat(
    provider="groq",
    api_key="gsk_...",
    question="Quick answer needed",
    model="llama-3.3-70b-versatile"
)
```

**Models**: llama-3.3-70b-versatile, llama-3.1-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768, gemma2-9b-it

**Specialty**: Extremely fast token generation, ideal for latency-sensitive applications

### Together AI

Multi-model aggregation platform with competitive pricing.

```python
response = chat(
    provider="together",
    api_key="...",
    question="Compare AI models",
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
)
```

**Models**: 
- meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo
- meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo
- mistralai/Mixtral-8x7B-Instruct-v0.1
- Qwen/Qwen2.5-72B-Instruct-Turbo
- deepseek-ai/deepseek-llm-67b-chat

### Cohere

Enterprise-focused LLM provider.

```python
response = chat(
    provider="cohere",
    api_key="...",
    question="Business analysis",
    model="command-r-plus"
)
```

**Models**: command-r-plus, command-r, command, command-light

**Specialty**: Optimized for enterprise use cases, RAG applications

### DeepSeek

Chinese AI provider with strong coding capabilities.

```python
response = chat(
    provider="deepseek",
    api_key="sk-...",
    question="Write Python code",
    model="deepseek-chat"
)
```

**Models**: deepseek-chat, deepseek-coder

### Qwen (通义千问)

Alibaba's multilingual LLM.

```python
response = chat(
    provider="qwen",
    api_key="sk-...",
    question="中英文混合问题",
    model="qwen-max"
)
```

**Models**: qwen-max, qwen-plus, qwen-turbo

### Zhipu (智谱AI)

Chinese AI provider with GLM series models.

```python
response = chat(
    provider="zhipu",
    api_key="...",
    question="智能问答",
    model="glm-4"
)
```

**Models**: glm-4, glm-3-turbo

### Ollama (Local)

Run models locally without API keys.

```python
response = chat(
    provider="ollama",
    api_key=None,  # No API key needed
    question="Local inference",
    model="llama3.2",
    base_url="http://localhost:11434"
)
```

**Models**: Any model installed locally (llama3.2, mistral, codellama, etc.)

**Specialty**: Complete privacy, no internet required, free

## Async Usage

All providers support async operations:

```python
import asyncio
from weav_provider_router import chat_async

async def main():
    response = await chat_async(
        provider="openai",
        api_key="sk-...",
        question="Async question",
        model="gpt-4"
    )
    print(response)

asyncio.run(main())
```

## Streaming

All providers support streaming:

```python
from weav_provider_router.providers import build_provider
from weav_provider_router.base import CompletionConfig

async def stream_example():
    llm = build_provider("openai", api_key="sk-...")
    config = CompletionConfig(model="gpt-4", temperature=0.7)
    messages = [{"role": "user", "content": "Tell me a story"}]
    
    async for chunk in llm.stream(messages, config):
        print(chunk, end="", flush=True)

asyncio.run(stream_example())
```

## Provider Selection Guide

### Choose Based on Use Case

**🚀 Speed Priority**
- **Groq**: 750+ tokens/sec, ultra-fast
- **Ollama**: Local, no network latency
- **Mistral**: Fast European servers

**💰 Cost Optimization**
- **Ollama**: Free (local)
- **DeepSeek/Qwen/Zhipu**: Low-cost Chinese providers
- **Together AI**: Competitive pricing
- **Groq**: Low cost per token

**🌍 Chinese Language**
- **Moonshot**: Long-context Chinese
- **Baidu ERNIE**: Enterprise Chinese
- **Qwen**: Alibaba multilingual
- **Zhipu**: GLM series
- **DeepSeek**: Code + Chinese

**🔒 Privacy**
- **Ollama**: 100% local, no data leaves your machine

**📚 Long Context**
- **Moonshot**: Up to 128K tokens
- **Google Gemini**: Up to 1M tokens
- **Claude 3**: Up to 200K tokens

**💼 Enterprise**
- **Cohere**: Business-optimized
- **Anthropic Claude**: Safety-focused
- **OpenAI**: Industry standard
- **Baidu ERNIE**: Chinese enterprise

**🔧 Development/Code**
- **DeepSeek**: Strong coding model
- **OpenAI GPT-4**: Excellent code gen
- **Ollama**: Local testing

## Dependencies

Most providers use OpenAI-compatible APIs:

```bash
pip install openai  # For: OpenAI, Moonshot, Mistral, Groq, Together AI, DeepSeek, Qwen, Zhipu
pip install anthropic  # For: Anthropic
pip install google-generativeai  # For: Google
pip install httpx  # For: Baidu, Cohere, Ollama
```

Or install all:

```bash
pip install weav-provider-router[all]
```

## API Key Setup

### Get Your API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google**: https://makersuite.google.com/app/apikey
- **Moonshot**: https://platform.moonshot.cn/console/api-keys
- **Baidu**: https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application
- **Mistral**: https://console.mistral.ai/
- **Groq**: https://console.groq.com/keys
- **Together AI**: https://api.together.xyz/settings/api-keys
- **Cohere**: https://dashboard.cohere.com/api-keys
- **DeepSeek**: https://platform.deepseek.com/api_keys
- **Qwen**: https://dashscope.console.aliyun.com/apiKey
- **Zhipu**: https://open.bigmodel.cn/usercenter/apikeys

## Troubleshooting

### Import Errors

If you see "Module not found" errors, install the required package:

```bash
# Most providers
pip install openai

# Anthropic
pip install anthropic

# Google
pip install google-generativeai

# HTTP-based providers (Baidu, Cohere)
pip install httpx
```

### Authentication Errors

**Baidu Special Case**: Requires both api_key AND secret_key:

```python
llm = build_provider("baidu", api_key="...", secret_key="...")
```

### Rate Limits

Different providers have different rate limits. Use exponential backoff or switch providers.

## More Information

See the [main README](README.md) for detailed API documentation and advanced usage patterns.
