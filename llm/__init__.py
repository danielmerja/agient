from .base import BaseLLM
from .config import LLMConfig, LLMResponse, LLMProvider
from .providers.openai import OpenAILLM
from .providers.anthropic import AnthropicLLM
from .providers.groq import GroqLLM  # Future implementation

def create_llm(config: LLMConfig) -> BaseLLM:
    """Factory function to create LLM instances."""
    providers = {
        LLMProvider.OPENAI: OpenAILLM,
        LLMProvider.ANTHROPIC: AnthropicLLM,
        LLMProvider.GROQ: GroqLLM,  # Future implementation
    }
    return providers[config.provider](config)

__all__ = [
    'BaseLLM',
    'LLMConfig',
    'LLMResponse',
    'LLMProvider',
    'create_llm'
]