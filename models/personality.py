"""
This module defines the Five Factor Model personality traits for agents.
"""

from pydantic import BaseModel, Field

class Personality(BaseModel):
    """Five Factor Model personality traits."""
    openness: float = Field(
        ge=0, le=1,
        description="Openness to experience - creativity, curiosity, and openness to new ideas"
    )
    conscientiousness: float = Field(
        ge=0, le=1,
        description="Conscientiousness - organization, responsibility, and goal-oriented behavior"
    )
    extraversion: float = Field(
        ge=0, le=1,
        description="Extraversion - sociability, assertiveness, and energy in social situations"
    )
    agreeableness: float = Field(
        ge=0, le=1,
        description="Agreeableness - compassion, cooperation, and consideration for others"
    )
    neuroticism: float = Field(
        ge=0, le=1,
        description="Neuroticism - emotional sensitivity, anxiety, and stress response"
    )
