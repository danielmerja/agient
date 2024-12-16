from typing import Dict, Set
from pydantic import BaseModel, Field

from models.agent import Agent
from models.base import Message, MessageContent

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
