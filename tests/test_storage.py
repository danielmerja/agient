
import unittest
from uuid import uuid4
from datetime import datetime, timedelta
import os
from storage import AgentStorage, StoredMemory

class TestAgentStorage(unittest.TestCase):
    def setUp(self):
        """Create a test database."""
        self.test_db = "test_agents.db"
        self.storage = AgentStorage(self.test_db)
        self.test_agent_id = uuid4()

    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_store_and_retrieve_memory(self):
        """Test basic memory storage and retrieval."""
        memory_id = self.storage.store_memory(
            self.test_agent_id,
            "Test event",
            sentiment=0.5,
            importance=0.8
        )
        
        memories = self.storage.get_memories(self.test_agent_id)
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0].event, "Test event")
        self.assertEqual(memories[0].sentiment, 0.5)
        self.assertEqual(memories[0].importance, 0.8)

    def test_memory_limits(self):
        """Test memory limits and cleanup."""
        # Store 10 memories
        for i in range(10):
            self.storage.store_memory(
                self.test_agent_id,
                f"Event {i}",
                sentiment=0.5,
                importance=0.8
            )
            
        # Keep only 5 most recent
        removed = self.storage.clear_old_memories(self.test_agent_id, keep_last=5)
        memories = self.storage.get_memories(self.test_agent_id)
        
        self.assertEqual(len(memories), 5)
        self.assertEqual(removed, 5)

    def test_invalid_sentiment_range(self):
        """Test sentiment range validation."""
        with self.assertRaises(sqlite3.IntegrityError):
            self.storage.store_memory(
                self.test_agent_id,
                "Invalid sentiment",
                sentiment=1.5,  # Invalid: > 1
                importance=0.5
            )

if __name__ == '__main__':
    unittest.main()