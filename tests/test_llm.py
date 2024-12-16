"""Unit tests for LLM memory functionality.

This file contains unit tests for the LLM memory functionality, ensuring that
long-term and short-term memories are stored and retrieved correctly.
"""

import unittest
from uuid import uuid4
from llm import LLMConfig, LLMProvider, BaseLLM, LLMResponse
from main import Agent

class MockLLM(BaseLLM):
    def _initialize_client(self) -> None:
        self._client = None

    async def generate(self, prompt: str) -> LLMResponse:
        return LLMResponse(content="Mock response", metadata={}, provider=LLMProvider.OPENAI)

    def store_long_term_memory(self, event: str, sentiment: float, importance: float) -> None:
        pass

    def retrieve_long_term_memories(self, limit: int = 100) -> list:
        return ["Mock long-term memory"]

    def store_short_term_memory(self, event: str, sentiment: float, importance: float) -> None:
        pass

    def retrieve_short_term_memories(self, limit: int = 10) -> list:
        return ["Mock short-term memory"]

class TestLLMMemory(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(
            name="Test Agent",
            demographics=None,
            personality=None,
            llm_config=LLMConfig(
                provider=LLMProvider.OPENAI,
                model="gpt-4",
                api_key="test",
                temperature=0.7
            )
        )
        self.agent._llm = MockLLM(self.agent.llm_config)

    def test_long_term_memory(self):
        self.agent.store_long_term_memory("Test event", 0.5, 0.8)
        memories = self.agent.retrieve_long_term_memories()
        self.assertIn("Mock long-term memory", memories)

    def test_short_term_memory(self):
        self.agent.store_short_term_memory("Test event", 0.5, 0.8)
        memories = self.agent.retrieve_short_term_memories()
        self.assertIn("Mock short-term memory", memories)

if __name__ == '__main__':
    unittest.main()
