"""Base module for Language Model (LLM) integrations.

This module provides the abstract base class for all LLM implementations.
It defines the standard interface that all LLM providers must implement.

Example:
    class CustomLLM(BaseLLM):
        def _initialize_client(self) -> None:
            self._client = CustomAPIClient(api_key=self.config.api_key)
        
        async def generate(self, prompt: str) -> LLMResponse:
            response = await self.client.generate(prompt)
            return LLMResponse(content=response.text)
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from .config import LLMConfig, LLMResponse

class BaseLLM(ABC):
    """Abstract base class for LLM provider implementations.
    
    This class defines the standard interface for interacting with different
    LLM providers. Each provider must implement the abstract methods to
    ensure consistent behavior across the framework.
    
    Attributes:
        config (LLMConfig): Configuration for the LLM provider
        _client: Internal API client instance (lazy loaded)
    
    Example:
        class GPT4(BaseLLM):
            async def generate(self, prompt: str) -> LLMResponse:
                return await self.client.complete(prompt)
    """
    
    def __init__(self, config: LLMConfig):
        """Initialize the LLM provider with configuration.
        
        Args:
            config: Configuration object containing API keys and settings
        """
        self.config = config
        self._client: Optional[object] = None

    @abstractmethod
    async def generate(self, prompt: str) -> LLMResponse:
        """Generate a response from the LLM for the given prompt.
        
        Args:
            prompt: The input text to send to the LLM
            
        Returns:
            A standardized response object containing the generated text
            
        Raises:
            Exception: If the API call fails or returns invalid response
        """
        pass

    @abstractmethod
    def _initialize_client(self) -> None:
        """Initialize the API client for the LLM provider.
        
        This method should set up any necessary API clients, authentication,
        and connection pools. It's called lazily when the client is first needed.
        
        Raises:
            Exception: If client initialization fails (e.g., invalid API key)
        """
        pass

    @property
    def client(self) -> object:
        """Lazy initialization of the API client.
        
        Returns:
            The initialized API client instance
            
        Note:
            This property ensures the client is only initialized when first used,
            saving resources and avoiding unnecessary connections.
        """
        if self._client is None:
            self._initialize_client()
        return self._client

    @abstractmethod
    def store_long_term_memory(self, event: str, sentiment: float, importance: float) -> None:
        """Store a long-term memory with emotional context."""
        pass

    @abstractmethod
    def retrieve_long_term_memories(self, limit: int = 100) -> List[str]:
        """Retrieve long-term memories from storage."""
        pass

    @abstractmethod
    def store_short_term_memory(self, event: str, sentiment: float, importance: float) -> None:
        """Store a short-term memory with emotional context."""
        pass

    @abstractmethod
    def retrieve_short_term_memories(self, limit: int = 10) -> List[str]:
        """Retrieve short-term memories from storage."""
        pass
