"""Configuration module for LLM providers and responses.

This module defines the configuration and response models used across
different LLM providers. It ensures type safety and standardization
of LLM interactions.

Example:
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key="sk-...",
        temperature=0.7
    )
"""

from typing import Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum

class LLMProvider(str, Enum):
    """Supported LLM providers.
    
    This enum defines the available LLM providers in the framework.
    Add new providers here to extend framework compatibility.
    """
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"

class LLMResponse(BaseModel):
    """Standardized LLM response format."""
    content: str = Field(
        description="Generated text response from the LLM"
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Response metadata including tokens, timings, and provider-specific info"
    )
    provider: LLMProvider = Field(
        description="Identifier of the LLM provider that generated the response"
    )

class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: LLMProvider = Field(
        description="The LLM provider to use (e.g., OpenAI, Anthropic)"
    )
    model: str = Field(
        description="Model identifier/name to use from the provider"
    )
    api_key: str = Field(
        description="Authentication key for the provider's API"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Controls randomness in response generation (0=deterministic, 1=creative)"
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="Maximum number of tokens to generate in response"
    )
    additional_params: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional provider-specific parameters (e.g., top_p, presence_penalty)"
    )
    long_term_memory_limit: int = Field(
        default=1000,
        description="Maximum number of long-term memories to store"
    )
    short_term_memory_limit: int = Field(
        default=100,
        description="Maximum number of short-term memories to store"
    )
