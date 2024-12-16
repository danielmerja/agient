"""Anthropic API integration module.

This module implements the Anthropic-specific LLM provider interface.
"""

import anthropic
from ..base import BaseLLM
from ..config import LLMResponse, LLMProvider
from typing import Any

class AnthropicLLM(BaseLLM):
    """Anthropic API integration."""
    
    def _initialize_client(self) -> None:
        """Initialize the Anthropic API client."""
        self._client = anthropic.Anthropic(api_key=self.config.api_key)
    
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate a response using Anthropic's API."""
        response = await self.client.completions.create(
            model=self.config.model,
            prompt=prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **self.config.additional_params
        )
        return LLMResponse(
            content=response.completion,
            metadata={"usage": response.usage},
            provider=LLMProvider.ANTHROPIC
        )
