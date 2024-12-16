"""
Demographic attributes of an agent.
"""

from typing import Optional
from pydantic import BaseModel, Field

class Demographics(BaseModel):
    """Demographic attributes of an agent."""
    age: int = Field(
        description="Age in years"
    )
    gender: str = Field(
        description="Gender identity of the agent"
    )
    occupation: str = Field(
        description="Current professional role or occupation"
    )
    location: str = Field(
        description="Geographic location or residence"
    )
    education_level: str = Field(
        description="Highest level of education completed"
    )
    income_bracket: Optional[str] = Field(
        default=None,
        description="Income category or economic status"
    )
