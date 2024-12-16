"""
Agient - A Psychologically-Grounded Agent Simulation Framework
=============================================================

A framework for creating psychologically realistic agent-based simulations
that model human behavior, relationships, and decision-making processes.
"""

from typing import List, Dict, Optional, Callable, Union, TypeVar, Generic, Set
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

from storage import AgentStorage, StoredMemory
from llm import LLMConfig, BaseLLM, create_llm, LLMResponse
from models.personality import Personality
from models.demographics import Demographics
from models.memory import Memory, Goal

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
    metadata: Dict[str, Union[str, float]] = Field(
        default_factory=dict,
        description="Additional message metadata and context"
    )

class Agent(BaseModel):
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
        if self._storage:
            self._storage.store_memory(
                self.id,
                event,
                sentiment,
                importance
            )

    def retrieve_long_term_memories(self, limit: int = 100) -> List[StoredMemory]:
        """Retrieve long-term memories from storage."""
        if self._storage:
            return self._storage.get_memories(self.id, limit)
        return []

    def store_short_term_memory(self, event: str, sentiment: float, importance: float) -> None:
        """Store a short-term memory with emotional context."""
        if self._storage:
            self._storage.store_memory(
                self.id,
                event,
                sentiment,
                importance
            )

    def retrieve_short_term_memories(self, limit: int = 10) -> List[StoredMemory]:
        """Retrieve short-term memories from storage."""
        if self._storage:
            return self._storage.get_memories(self.id, limit)
        return []

class Environment(BaseModel):
    """Enhanced environment with social network support."""
    
    agents: Dict[str, Agent] = Field(default_factory=dict)
    message_history: List[Message] = Field(default_factory=list)

    def register_agent(self, agent: Agent) -> None:
        """Registers an agent in the environment.
        
        Args:
            agent: The agent to register
        """
        self.agents[agent.name] = agent

    def send_message(self, message: Message) -> None:
        """Delivers a message to its intended recipient.
        
        Args:
            message: The message to deliver
        """
        self.message_history.append(message)
        if message.receiver in self.agents:
            self.agents[message.receiver].receive_message(message)

    def broadcast_message(self, sender: str, content: MessageContent) -> None:
        """Broadcasts a message to all agents except the sender.
        
        Args:
            sender: Name of the sending agent
            content: Content to broadcast
        """
        for agent_name in self.agents:
            if agent_name != sender:
                message = Message(sender=sender, receiver=agent_name, content=content)
                self.send_message(message)

    def get_social_network(self, agent_name: str, depth: int = 1) -> Set[str]:
        """Get an agent's social network up to specified depth.
        
        Args:
            agent_name: Name of the agent whose network to explore
            depth: How many connection levels deep to search (default=1)
            
        Returns:
            Set of agent names in the social network
        """
        network = set()
        if agent_name not in self.agents:
            return network
            
        current_depth = 0
        current_level = {agent_name}
        
        while current_depth < depth and current_level:
            next_level = set()
            for name in current_level:
                agent = self.agents[name]
                next_level.update(agent.social_network)
            network.update(next_level)
            current_level = next_level
            current_depth += 1
            
        return network
