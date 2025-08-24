#!/usr/bin/env python3
"""
Database module for todo app
Handles SQLite database operations with migration from JSON
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class TodoDatabase:
    """SQLite database handler for todo app"""
    
    def __init__(self, db_path: str = "todo_app.db"):
        self.db_path = db_path
        self.init_database()
        self.migrate_from_json()
    
    def init_database(self):
        """Initialize database with tasks table"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP NULL
                )
            """)
            conn.commit()
    
    def migrate_from_json(self):
        """Migrate existing JSON data to SQLite"""
        json_file = "tasks.json"
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    tasks = json.load(f)
                
                # Check if database is empty
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute("SELECT COUNT(*) FROM tasks")
                    count = cursor.fetchone()[0]
                    
                    if count == 0 and tasks:
                        # Migrate data
                        for task in tasks:
                            conn.execute("""
                                INSERT INTO tasks (id, description, completed, created, completed_at)
                                VALUES (?, ?, ?, ?, ?)
                            """, (
                                task.get('id'),
                                task.get('description'),
                                task.get('completed', False),
                                task.get('created'),
                                task.get('completed_at')
                            ))
                        conn.commit()
                        
                        # Backup original JSON file
                        os.rename(json_file, f"{json_file}.backup")
                        print(f"✅ Migrated {len(tasks)} tasks from JSON to SQLite")
                        
            except Exception as e:
                print(f"⚠️ Migration warning: {e}")
    
    def add_task(self, description: str) -> Dict[str, Any]:
        """Add a new task"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO tasks (description, created)
                VALUES (?, ?)
            """, (description, datetime.now().isoformat()))
            
            task_id = cursor.lastrowid
            conn.commit()
            
            return self.get_task(task_id)
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a single task by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM tasks WHERE id = ?
            """, (task_id,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM tasks ORDER BY created DESC
            """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def complete_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Mark a task as completed"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE tasks 
                SET completed = TRUE, completed_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), task_id))
            
            conn.commit()
            return self.get_task(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM tasks WHERE id = ?
            """, (task_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_tasks,
                    COUNT(CASE WHEN completed = 1 THEN 1 END) as completed_tasks,
                    COUNT(CASE WHEN completed = 0 THEN 1 END) as pending_tasks
                FROM tasks
            """)
            
            stats = cursor.fetchone()
            return {
                "database_path": self.db_path,
                "total_tasks": stats[0],
                "completed_tasks": stats[1],
                "pending_tasks": stats[2],
                "storage_type": "SQLite"
            }
