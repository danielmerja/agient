"""
Example of a simulated senator agent with LLM capabilities.
"""

import asyncio
import os
from typing import Optional, List, Dict
from models.personality import Personality
from models.demographics import Demographics
from models.base import Message, MessageContent
from main import Agent, Environment
from llm.config import LLMConfig, LLMProvider, LLMResponse

def echo_handler(message: Message[MessageContent]) -> None:
    """Simple message handler that prints received messages.
    
    Args:
        message: The message to echo, containing sender, receiver and content
    """
    print(f"Agent {message.receiver} received: {message.content}")

def create_senator() -> Agent:
    """Create a simulated senator agent with realistic attributes.
    
    Returns:
        An Agent instance configured with senator-appropriate traits,
        demographics, and capabilities
    """
    return Agent(
        name="Senator Smith",
        demographics=Demographics(
            age=55,
            gender="F",
            occupation="Senator",
            location="Washington DC",
            education_level="JD",
            income_bracket="High"
        ),
        personality=Personality(
            openness=0.7,
            conscientiousness=0.8,
            extraversion=0.9,
            agreeableness=0.6,
            neuroticism=0.3
        ),
        capabilities=["debate", "negotiate", "public_speaking"],
        beliefs={"climate_change": 0.8, "healthcare_reform": 0.7},
        values={"integrity": 0.9, "public_service": 0.8}
    )

def create_smart_senator() -> Agent:
    """Create a senator agent with LLM capabilities."""
    return Agent(
        name="Senator Smith",
        demographics=Demographics(
            age=55,
            gender="F",
            occupation="Senator",
            location="Washington DC",
            education_level="JD",
            income_bracket="High"
        ),
        personality=Personality(
            openness=0.7,
            conscientiousness=0.8,
            extraversion=0.9,
            agreeableness=0.6,
            neuroticism=0.3
        ),
        capabilities=["debate", "negotiate", "public_speaking"],
        beliefs={"climate_change": 0.8, "healthcare_reform": 0.7},
        values={"integrity": 0.9, "public_service": 0.8},
        llm_config=LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    )

async def main() -> None:
    env = Environment()
    senator = create_smart_senator()
    
    # Test LLM-powered thinking
    response: Optional[LLMResponse] = await senator.think(
        "A new climate bill has been proposed that would increase regulations on coal plants."
    )
    if response:
        print(f"Senator's thoughts: {response.content}")
    
    # Test LLM-powered decision making
    decision: str = await senator.make_decision(
        options=["Support bill", "Oppose bill", "Propose amendments"],
        context={"public_support": 0.65, "economic_impact": -0.2}
    )
    print(f"Senator's decision: {decision}")

    # Demonstrate long-term memory
    senator.store_long_term_memory("Attended climate summit", sentiment=0.9, importance=0.8)
    senator.store_long_term_memory("Debated healthcare reform", sentiment=0.7, importance=0.6)
    long_term_memories = senator.retrieve_long_term_memories(limit=2)
    print("Long-term memories:")
    for memory in long_term_memories:
        print(f"- {memory}")

    # Demonstrate short-term memory
    senator.store_short_term_memory("Received new policy proposal", sentiment=0.5, importance=0.4)
    short_term_memories = senator.retrieve_short_term_memories(limit=1)
    print("Short-term memories:")
    for memory in short_term_memories:
        print(f"- {memory}")

if __name__ == "__main__":
    asyncio.run(main())
