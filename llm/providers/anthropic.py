
"""Anthropic API integration module.

This module implements the Anthropic-specific LLM provider interface.
"""

import anthropic
from ..base import BaseLLM
from ..config import LLMResponse, LLMProvider

class AnthropicLLM(BaseLLM):
    """Anthropic API integration."""
    
    def _initialize_client(self) -> None:
        """Initialize the Anthropic API client."""
        self._client = anthropic.Anthropic(api_key=self.config.api_key)
    
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate a response using Anthropic's API."""
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