"""OpenAI API integration module.

This module implements the OpenAI-specific LLM provider interface.
It handles authentication, API calls, and response processing for
OpenAI's models (GPT-3.5, GPT-4, etc.).

Example:
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4",
        api_key="sk-..."
    )
    llm = OpenAILLM(config)
    response = await llm.generate("What is AI?")
"""

import openai
from ..base import BaseLLM
from ..config import LLMResponse, LLMProvider
from typing import Any

class OpenAILLM(BaseLLM):
    """OpenAI API integration.
    
    This class implements the BaseLLM interface for OpenAI's models.
    It handles the specific requirements of the OpenAI API, including
    authentication, rate limiting, and response processing.
    
    Attributes:
        config: OpenAI-specific configuration
        client: OpenAI API client instance
        
    Example:
        llm = OpenAILLM(config)
        response = await llm.generate("Explain quantum computing")
        print(response.content)
    """
    
    def _initialize_client(self) -> None:
        """Initialize the OpenAI API client.
        
        Sets up the OpenAI client with proper authentication and
        default parameters from the configuration.
        
        Raises:
            Exception: If API key is invalid or initialization fails
        """
        openai.api_key = self.config.api_key
        self._client = openai
    
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate a response using OpenAI's API.
        
        Args:
            prompt: The input text to send to the model
            
        Returns:
            Standardized response containing the generated text
            
        Raises:
            openai.Error: If the API call fails
            ValueError: If response parsing fails
        """
        response = await self.client.ChatCompletion.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **self.config.additional_params
        )
        return LLMResponse(
            content=response.choices[0].message["content"],
            metadata={"usage": response["usage"]},
            provider=LLMProvider.OPENAI
        )
