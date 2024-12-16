"""
Base module for agent communication messages.

This module defines the Message class used for agent-to-agent communication.
"""

from typing import Dict, Optional, Union
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

MessageContent = Union[str, dict]

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
    content: MessageContent = Field(
        description="Content of the message in any supported format"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Time when the message was created"
    )
    metadata: Dict[str, MessageContent] = Field(
        default_factory=dict,
        description="Additional message metadata and context"
    )
