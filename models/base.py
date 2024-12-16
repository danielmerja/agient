from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Union
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

MessageContent = Union[str, dict]
