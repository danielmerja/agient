from typing import List, Dict, Optional, Callable, Union, Set
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

from storage import AgentStorage, StoredMemory
from llm import LLMConfig, BaseLLM, create_llm, LLMResponse
from models.personality import Personality
from models.demographics import Demographics
from models.memory import Memory, Goal
from llm.base import MemoryBase

MessageContent = Union[str, dict]

class Agent(MemoryBase, BaseModel):
    """A simulated person with realistic attributes and behaviors."""
    
    id: UUID = Field(default_factory=uuid4)
    name: str
    demographics: Demographics
    personality: Personality
    
    # Core attributes
    capabilities: List[str] = Field(default_factory=list)
    beliefs: Dict[str, float] = Field(default_factory=dict)
    values: Dict[str, float] = Field(default_factory=dict)
    
    # Social attributes
    relationships: Dict[str, float] = Field(default_factory=dict)
    social_network: Set[str] = Field(default_factory=set)
    influence_score: float = Field(default=0.5)
    
    # Dynamic attributes
    state: Dict[str, MessageContent] = Field(default_factory=dict)
    memories: List[Memory] = Field(default_factory=list)
    goals: List[Goal] = Field(default_factory=list)
    current_focus: Optional[str] = None
    
    message_handler: Optional[Callable[[Message], None]] = None
    _storage: Optional[AgentStorage] = None
    llm_config: Optional[LLMConfig] = None
    _llm: Optional[BaseLLM] = None

    def __init__(self, **data: Union[str, int, float, dict, list, None]):
        super().__init__(**data)
        self._storage = AgentStorage()
        if self.llm_config:
            self._llm = create_llm(self.llm_config)

    def send_message(self, receiver: str, content: MessageContent) -> Message:
        """Send a message influenced by personality and relationship."""
        return Message(
            sender=self.name,
            receiver=receiver,
            content=content,
            metadata={
                "relationship_score": self.relationships.get(receiver, 0),
                "sender_mood": self.state.get("mood", 0)
            }
        )

    def update_memory(self, event: str, sentiment: float, importance: float) -> None:
        """Record a new memory with emotional context."""
        if self._storage:
            self._storage.store_memory(
                self.id,
                event,
                sentiment,
                importance
            )

    def get_recent_memories(self, limit: int = 100) -> List[StoredMemory]:
        """Retrieve recent memories from storage."""
        if self._storage:
            return self._storage.get_memories(self.id, limit)
        return []

    def cleanup_old_memories(self, keep_last: int = 1000) -> int:
        """Remove old memories to free up storage."""
        if self._storage:
            return self._storage.clear_old_memories(self.id, keep_last)
        return 0

    async def think(self, context: str) -> Optional[LLMResponse]:
        """Generate thoughts using LLM based on context and personality."""
        if not self._llm:
            return None
            
        prompt = f"""As {self.name}, with the following traits:
- Personality: {self.personality.dict()}
- Beliefs: {self.beliefs}
- Values: {self.values}
- Current focus: {self.current_focus}

Given this context: {context}

What are your thoughts and how would you respond?"""

        return await self._llm.generate(prompt)

    async def make_decision(self, options: List[str], context: Dict[str, Union[str, float]]) -> str:
        """Make a decision using LLM capabilities."""
        if not self._llm:
            return options[0]  # Default to first option if no LLM
            
        prompt = f"""As {self.name}, given these options:
{'\n'.join(f'- {opt}' for opt in options)}

And this context:
{context}

Which option would you choose and why? Consider your:
- Personality traits
- Current beliefs and values
- Past experiences and goals

Respond with just the chosen option."""

        response = await self._llm.generate(prompt)
        return response.content.strip()

    def update_relationships(self, other_agent: str, interaction_score: float) -> None:
        """Update relationship scores based on interactions.
        
        Args:
            other_agent: Name of the agent to update relationship with
            interaction_score: Score modifier (-1 to 1) for the interaction
        """
        current = self.relationships.get(other_agent, 0)
        self.relationships[other_agent] = max(min(current + interaction_score, 1), -1)

    def set_goal(self, description: str, priority: int, deadline: Optional[datetime] = None) -> None:
        """Add a new goal for the agent to pursue."""
        self.goals.append(Goal(
            description=description,
            priority=priority,
            progress=0,
            deadline=deadline
        ))

    def store_long_term_memory(self, event: str, sentiment: float, importance: float) -> None:
        """Store a long-term memory with emotional context."""
        if self._llm:
            self._llm.store_long_term_memory(event, sentiment, importance)

    def retrieve_long_term_memories(self, limit: int = 100) -> List[str]:
        """Retrieve long-term memories from storage."""
        if self._llm:
            return self._llm.retrieve_long_term_memories(limit)
        return []

    def store_short_term_memory(self, event: str, sentiment: float, importance: float) -> None:
        """Store a short-term memory with emotional context."""
        if self._llm:
            self._llm.store_short_term_memory(event, sentiment, importance)

    def retrieve_short_term_memories(self, limit: int = 10) -> List[str]:
        """Retrieve short-term memories from storage."""
        if self._llm:
            return self._llm.retrieve_short_term_memories(limit)
        return []
