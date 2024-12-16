"""
Example of a simulated student agent with LLM capabilities.
"""

import asyncio
import os
from typing import Optional, List, Dict
from models.personality import Personality
from models.demographics import Demographics
from models.base import Message, MessageContent
from main import Agent, Environment
from llm.config import LLMConfig, LLMProvider, LLMResponse

def create_student() -> Agent:
    """Create a simulated student agent with realistic attributes.
    
    Returns:
        An Agent instance configured with student-appropriate traits,
        demographics, and capabilities
    """
    return Agent(
        name="Student Lee",
        demographics=Demographics(
            age=20,
            gender="F",
            occupation="Student",
            location="Boston",
            education_level="Undergraduate",
            income_bracket="Low"
        ),
        personality=Personality(
            openness=0.9,
            conscientiousness=0.7,
            extraversion=0.6,
            agreeableness=0.8,
            neuroticism=0.5
        ),
        capabilities=["study", "research", "collaborate"],
        beliefs={"importance_of_education": 0.9, "environmental_awareness": 0.8},
        values={"knowledge": 0.9, "community": 0.8}
    )

def create_smart_student() -> Agent:
    """Create a student agent with LLM capabilities."""
    return Agent(
        name="Student Lee",
        demographics=Demographics(
            age=20,
            gender="F",
            occupation="Student",
            location="Boston",
            education_level="Undergraduate",
            income_bracket="Low"
        ),
        personality=Personality(
            openness=0.9,
            conscientiousness=0.7,
            extraversion=0.6,
            agreeableness=0.8,
            neuroticism=0.5
        ),
        capabilities=["study", "research", "collaborate"],
        beliefs={"importance_of_education": 0.9, "environmental_awareness": 0.8},
        values={"knowledge": 0.9, "community": 0.8},
        llm_config=LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    )

async def main() -> None:
    env = Environment()
    student = create_smart_student()
    
    # Test LLM-powered thinking
    response: Optional[LLMResponse] = await student.think(
        "A new project has been assigned that requires extensive research on climate change."
    )
    if response:
        print(f"Student's thoughts: {response.content}")
    
    # Test LLM-powered decision making
    decision: str = await student.make_decision(
        options=["Start research", "Form study group", "Seek professor's guidance"],
        context={"deadline": "2 weeks", "complexity": "high"}
    )
    print(f"Student's decision: {decision}")

    # Demonstrate long-term memory
    student.store_long_term_memory("Completed a major project", sentiment=0.8, importance=0.9)
    student.store_long_term_memory("Participated in a community service event", sentiment=0.9, importance=0.7)
    long_term_memories = student.retrieve_long_term_memories(limit=2)
    print("Long-term memories:")
    for memory in long_term_memories:
        print(f"- {memory}")

    # Demonstrate short-term memory
    student.store_short_term_memory("Received new assignment", sentiment=0.6, importance=0.5)
    short_term_memories = student.retrieve_short_term_memories(limit=1)
    print("Short-term memories:")
    for memory in short_term_memories:
        print(f"- {memory}")

if __name__ == "__main__":
    asyncio.run(main())
