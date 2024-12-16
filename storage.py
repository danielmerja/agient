"""
This module handles SQLite storage operations for agent memories.

It provides functionality to store, retrieve, and manage memories
associated with agents in a SQLite database.
"""

import sqlite3
from typing import List
from datetime import datetime
from uuid import UUID
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class StoredMemory:
    """Type-safe memory storage class."""
    id: int
    agent_id: UUID
    timestamp: datetime
    event: str
    sentiment: float
    importance: float

class AgentStorage:
    """Handles SQLite storage operations for agent memories."""
    
    def __init__(self, db_path: str = "agents.db"):
        """Initialize storage with database path."""
        self.db_path = db_path
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(
            self.db_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        """Initialize database schema."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    event TEXT NOT NULL,
                    sentiment REAL NOT NULL CHECK (sentiment >= -1 AND sentiment <= 1),
                    importance REAL NOT NULL CHECK (importance >= 0 AND importance <= 1)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_agent_id 
                ON memories(agent_id)
            """)
            conn.commit()

    def store_memory(self, agent_id: UUID, event: str, sentiment: float, importance: float) -> int:
        """Store a new memory."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO memories (agent_id, timestamp, event, sentiment, importance)
                VALUES (?, ?, ?, ?, ?)
            """, (str(agent_id), datetime.now(), event, sentiment, importance))
            conn.commit()
            return cursor.lastrowid

    def get_memories(self, agent_id: UUID, limit: int = 100) -> List[StoredMemory]:
        """Retrieve agent memories, most recent first."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM memories 
                WHERE agent_id = ? 
                ORDER BY timestamp DESC
                LIMIT ?
            """, (str(agent_id), limit))
            
            return [StoredMemory(
                id=row['id'],
                agent_id=UUID(row['agent_id']),
                timestamp=row['timestamp'],
                event=row['event'],
                sentiment=row['sentiment'],
                importance=row['importance']
            ) for row in cursor.fetchall()]

    def clear_old_memories(self, agent_id: UUID, keep_last: int = 1000) -> int:
        """Remove old memories keeping only the most recent ones."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM memories 
                WHERE agent_id = ? 
                AND id NOT IN (
                    SELECT id FROM memories 
                    WHERE agent_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                )
            """, (str(agent_id), str(agent_id), keep_last))
            conn.commit()
            return cursor.rowcount

    def execute_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query and return the cursor."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor

    def fetch_all(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Fetch all rows for a query."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
