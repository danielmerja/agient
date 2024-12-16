from models.agent import Agent
from models.personality import Personality
from models.demographics import Demographics
from llm.config import LLMConfig, LLMProvider

def create_agent(name: str, age: int, gender: str, occupation: str, location: str, education_level: str, income_bracket: str, openness: float, conscientiousness: float, extraversion: float, agreeableness: float, neuroticism: float, capabilities: list, beliefs: dict, values: dict, llm_config: dict = None) -> Agent:
    """Create a simulated agent with realistic attributes.
    
    Args:
        name: Name of the agent
        age: Age of the agent
        gender: Gender of the agent
        occupation: Occupation of the agent
        location: Location of the agent
        education_level: Education level of the agent
        income_bracket: Income bracket of the agent
        openness: Openness trait score
        conscientiousness: Conscientiousness trait score
        extraversion: Extraversion trait score
        agreeableness: Agreeableness trait score
        neuroticism: Neuroticism trait score
        capabilities: List of capabilities of the agent
        beliefs: Dictionary of beliefs of the agent
        values: Dictionary of values of the agent
        llm_config: Optional dictionary for LLM configuration
    
    Returns:
        An Agent instance configured with the provided attributes
    """
    demographics = Demographics(
        age=age,
        gender=gender,
        occupation=occupation,
        location=location,
        education_level=education_level,
        income_bracket=income_bracket
    )
    
    personality = Personality(
        openness=openness,
        conscientiousness=conscientiousness,
        extraversion=extraversion,
        agreeableness=agreeableness,
        neuroticism=neuroticism
    )
    
    llm_config_obj = None
    if llm_config:
        llm_config_obj = LLMConfig(
            provider=LLMProvider[llm_config["provider"]],
            model=llm_config["model"],
            api_key=llm_config["api_key"],
            temperature=llm_config["temperature"]
        )
    
    return Agent(
        name=name,
        demographics=demographics,
        personality=personality,
        capabilities=capabilities,
        beliefs=beliefs,
        values=values,
        llm_config=llm_config_obj
    )
