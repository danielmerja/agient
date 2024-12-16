"""
Memory and Goal models for agent's memory and goal management.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Memory(BaseModel):
    """Represents an agent's memory."""
    event: str = Field(
        description="Description of the event"
    )
    sentiment: float = Field(
        ge=-1, le=1,
        description="Sentiment score associated with the memory (-1 to 1)"
    )
    importance: float = Field(
        ge=0, le=1,
        description="Importance score of the memory (0 to 1)"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Time when the memory was created"
    )

class Goal(BaseModel):
    """Represents an agent's goal."""
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
