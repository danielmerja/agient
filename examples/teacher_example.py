"""
Example of a simulated teacher agent with LLM capabilities.
"""

import asyncio
import os
from typing import Optional, List, Dict
from models.base import Message, MessageContent
from models.environment import Environment
from llm.config import LLMConfig, LLMProvider, LLMResponse
from examples.common import create_agent

def echo_handler(message: Message[MessageContent]) -> None:
    """Simple message handler that prints received messages.
    
    Args:
        message: The message to echo, containing sender, receiver and content
    """
    print(f"Agent {message.receiver} received: {message.content}")

def create_teacher() -> Agent:
    """Create a simulated teacher agent with realistic attributes.
    
    Returns:
        An Agent instance configured with teacher-appropriate traits,
        demographics, and capabilities
    """
    return create_agent(
        name="Teacher Johnson",
        age=40,
        gender="M",
        occupation="Teacher",
        location="New York",
        education_level="MEd",
        income_bracket="Medium",
        openness=0.8,
        conscientiousness=0.9,
        extraversion=0.7,
        agreeableness=0.8,
        neuroticism=0.4,
        capabilities=["teach", "mentor", "evaluate"],
        beliefs={"education_reform": 0.9, "technology_integration": 0.7},
        values={"knowledge": 0.9, "student_success": 0.8}
    )

def create_smart_teacher() -> Agent:
    """Create a teacher agent with LLM capabilities."""
    return create_agent(
        name="Teacher Johnson",
        age=40,
        gender="M",
        occupation="Teacher",
        location="New York",
        education_level="MEd",
        income_bracket="Medium",
        openness=0.8,
        conscientiousness=0.9,
        extraversion=0.7,
        agreeableness=0.8,
        neuroticism=0.4,
        capabilities=["teach", "mentor", "evaluate"],
        beliefs={"education_reform": 0.9, "technology_integration": 0.7},
        values={"knowledge": 0.9, "student_success": 0.8},
        llm_config={
            "provider": "OPENAI",
            "model": "gpt-4",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "temperature": 0.7
        }
    )

async def main() -> None:
    env = Environment()
    teacher = create_smart_teacher()
    
    # Test LLM-powered thinking
    response: Optional[LLMResponse] = await teacher.think(
        "A new educational policy has been proposed that would increase the use of technology in classrooms."
    )
    if response:
        print(f"Teacher's thoughts: {response.content}")
    
    # Test LLM-powered decision making
    decision: str = await teacher.make_decision(
        options=["Support policy", "Oppose policy", "Propose amendments"],
        context={"student_engagement": 0.75, "budget_impact": -0.1}
    )
    print(f"Teacher's decision: {decision}")

    # Demonstrate long-term memory
    teacher.store_long_term_memory("Attended educational conference", sentiment=0.8, importance=0.7)
    teacher.store_long_term_memory("Implemented new teaching strategy", sentiment=0.9, importance=0.8)
    long_term_memories = teacher.retrieve_long_term_memories(limit=2)
    print("Long-term memories:")
    for memory in long term_memories:
        print(f"- {memory}")

    # Demonstrate short-term memory
    teacher.store_short_term_memory("Received new curriculum guidelines", sentiment=0.6, importance=0.5)
    short term_memories = teacher.retrieve_short term_memories(limit=1)
    print("Short-term memories:")
    for memory in short term_memories:
        print(f"- {memory}")

if __name__ == "__main__":
    asyncio.run(main())
