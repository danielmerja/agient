
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime

class Message(BaseModel):
    """A typed message for agent communication."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for the message"
    )
    sender: str = Field(
        description="Name of the agent sending the message"
    )
    receiver: str = Field(
        description="Name of the agent receiving the message"
    )
    content: Any = Field(
        description="Content of the message in any supported format"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Time when the message was created"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional message metadata and context"
    )

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

class Goal(BaseModel):
    """Agent's goal or objective."""
    description: str = Field(
        description="Detailed description of the goal"
    )
    priority: int = Field(
        ge=1, le=10,
        description="Priority level from 1 (lowest) to 10 (highest)"
    )
    progress: float = Field(
        ge=0, le=1,
        description="Progress towards completion (0-1)"
    )
    deadline: Optional[datetime] = Field(
        default=None,
        description="Target completion date and time"
    )