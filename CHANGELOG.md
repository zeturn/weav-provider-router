# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-25

### Added
- Initial release of weav-provider-router
- Support for OpenAI provider
- Support for Anthropic provider
- Support for Google provider
- Support for Ollama provider
- Support for DeepSeek provider
- Support for Qwen provider
- Support for Zhipu provider
- Unified chat and completion API
- Async/await support
- Streaming response support
- Model listing functionality
- Comprehensive test suite
- Full documentation

### Features
- `chat()` and `chat_async()` for synchronous and asynchronous chat
- `complete()` and `complete_async()` for text completion
- `list_models()` for retrieving available models
- `build_provider()` for direct provider instantiation
- Flexible configuration with `CompletionConfig`
- Support for custom API endpoints via `base_url`
- Provider-specific extra parameters support

### Developer Experience
- Type hints for better IDE support
- Pytest-based test suite with unit and integration tests
- Black code formatting
- Ruff linting
- MyPy type checking
- Comprehensive documentation and examples

[Unreleased]: https://github.com/HungryZhao/weav-provider-router/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/HungryZhao/weav-provider-router/releases/tag/v0.1.0
