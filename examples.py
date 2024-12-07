from main import Agent, Environment, Message, MessageContent, Demographics, Personality
from datetime import datetime, timedelta
from llm import LLMConfig, LLMProvider
import asyncio
import os

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

async def main():
    env = Environment()
    senator = create_smart_senator()
    
    # Test LLM-powered thinking
    response = await senator.think(
        "A new climate bill has been proposed that would increase regulations on coal plants."
    )
    print(f"Senator's thoughts: {response.content}")
    
    # Test LLM-powered decision making
    decision = await senator.make_decision(
        options=["Support bill", "Oppose bill", "Propose amendments"],
        context={"public_support": 0.65, "economic_impact": -0.2}
    )
    print(f"Senator's decision: {decision}")

if __name__ == "__main__":
    asyncio.run(main())