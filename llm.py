
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
import openai
import anthropic
import os
from enum import Enum

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"

class LLMResponse(BaseModel):
    """Standardized LLM response format."""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    provider: LLMProvider

class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: LLMProvider
    model: str
    api_key: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    additional_params: Dict[str, Any] = Field(default_factory=dict)

class BaseLLM(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate response from LLM."""
        pass

class OpenAILLM(BaseLLM):
    """OpenAI API integration."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = openai.OpenAI(api_key=config.api_key)
    
    async def generate(self, prompt: str) -> LLMResponse:
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **self.config.additional_params
        )
        return LLMResponse(
            content=response.choices[0].message.content,
            metadata={"usage": response.usage.dict()},
            provider=LLMProvider.OPENAI
        )

class AnthropicLLM(BaseLLM):
    """Anthropic API integration."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.api_key)
    
    async def generate(self, prompt: str) -> LLMResponse:
        response = await self.client.messages.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **self.config.additional_params
        )
        return LLMResponse(
            content=response.content,
            metadata={},
            provider=LLMProvider.ANTHROPIC
        )

def create_llm(config: LLMConfig) -> BaseLLM:
    """Factory function to create LLM instances."""
    providers = {
        LLMProvider.OPENAI: OpenAILLM,
        LLMProvider.ANTHROPIC: AnthropicLLM,
    }
    return providers[config.provider](config)