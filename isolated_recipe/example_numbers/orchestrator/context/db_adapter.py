"""
Simple DB Adapter - IAF0 Framework Storage Component
==================================================
Minimal storage adapter to replace the removed storage module.
Provides basic database/file persistence functionality.
"""

import json
import sqlite3
import os
from pathlib import Path
from typing import Dict, Any, Optional

class DBAdapter:
    """Simple database adapter for context persistence."""
    
    def __init__(self, db_path: str = "./data/iaf0.db"):
        """Initialize database adapter with SQLite backend."""
        self.db_path = Path(db_path)  # Database file path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory
        self._init_db()  # Initialize database schema
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS context_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    version_id TEXT
                )
            """)
            conn.commit()  # Save schema changes
    
    def save_context(self, data: Dict[str, Any], mode: str = "full") -> None:
        """Save context data to database."""
        with sqlite3.connect(self.db_path) as conn:
            for key, value in data.items():
                # Serialize value to JSON string
                value_json = json.dumps(value)
                
                # Insert or update data
                conn.execute("""
                    INSERT OR REPLACE INTO context_data (key, value, version_id)
                    VALUES (?, ?, ?)
                """, (key, value_json, mode))
            
            conn.commit()  # Save changes
    
    def load_context(self, version_id: Optional[str] = None) -> Dict[str, Any]:
        """Load context data from database."""
        with sqlite3.connect(self.db_path) as conn:
            if version_id:
                cursor = conn.execute("""
                    SELECT key, value FROM context_data 
                    WHERE version_id = ?
                """, (version_id,))
            else:
                cursor = conn.execute("""
                    SELECT key, value FROM context_data
                """)
            
            data = {}  # Initialize result dictionary
            for row in cursor.fetchall():
                key, value_json = row
                try:
                    data[key] = json.loads(value_json)  # Deserialize JSON
                except json.JSONDecodeError:
                    data[key] = value_json  # Use raw value if JSON fails
            
            return data
    
    def get_versions(self) -> list:
        """Get list of available versions."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT DISTINCT version_id FROM context_data 
                WHERE version_id IS NOT NULL
                ORDER BY timestamp DESC
            """)
            return [row[0] for row in cursor.fetchall()]
    
    def clear(self) -> None:
        """Clear all data from database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM context_data")
            conn.commit()  # Save changes
    
    def __repr__(self) -> str:
        """String representation of adapter."""
        return f"DBAdapter(db_path={self.db_path})"


# Simple file-based storage for basic persistence
class FileAdapter:
    """Simple file-based storage adapter."""
    
    def __init__(self, storage_dir: str = "./data"):
        """Initialize file adapter."""
        self.storage_dir = Path(storage_dir)  # Storage directory path
        self.storage_dir.mkdir(parents=True, exist_ok=True)  # Create directory
    
    def save_context(self, data: Dict[str, Any], filename: str = "context.json") -> None:
        """Save context data to file."""
        file_path = self.storage_dir / filename
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)  # Save formatted JSON
    
    def load_context(self, filename: str = "context.json") -> Dict[str, Any]:
        """Load context data from file."""
        file_path = self.storage_dir / filename
        if not file_path.exists():
            return {}  # Return empty dict if file doesn't exist
        
        with open(file_path, 'r') as f:
            return json.load(f)  # Load JSON data
    
    def list_files(self) -> list:
        """List all JSON files in storage directory."""
        return [f.name for f in self.storage_dir.glob("*.json")]
    
    def delete_file(self, filename: str) -> None:
        """Delete a storage file."""
        file_path = self.storage_dir / filename
        if file_path.exists():
            file_path.unlink()  # Delete file
    
    def __repr__(self) -> str:
        """String representation of adapter."""
        return f"FileAdapter(storage_dir={self.storage_dir})"