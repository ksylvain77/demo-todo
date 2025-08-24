"""
todo app - Core Module
Core business logic

This module contains the core business logic for todo app.
"""

from datetime import datetime
from typing import Dict, Any, List
from modules.database import TodoDatabase

# Initialize database connection
db = TodoDatabase()

def get_status() -> Dict[str, Any]:
    """
    Get the current application status
    
    Returns:
        Dict containing app status information
    """
    db_info = db.get_database_info()
    return {
        "status": "running",
        "service": "todo_app",
        "version": "0.2.0",
        "storage": db_info["storage_type"],
        "database_path": db_info["database_path"],
        "tasks": {
            "total": db_info["total_tasks"],
            "completed": db_info["completed_tasks"],
            "pending": db_info["pending_tasks"]
        },
        "uptime": "active",
        "last_updated": "2025-01-01"
    }

def process_data(data: Any) -> Dict[str, Any]:
    """
    Process incoming data (template function)
    
    Args:
        data: Input data to process
        
    Returns:
        Dict containing processed results
    """
    return {
        "processed": True,
        "input_type": type(data).__name__,
        "timestamp": datetime.now().isoformat(),
        "result": f"Processed: {data}"
    }

def validate_input(data: Any) -> bool:
    """
    Validate input data (template function)
    
    Args:
        data: Data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if data is None:
        return False
    if isinstance(data, str) and len(data.strip()) == 0:
        return False
    return True


def input_tasks(task_list: list[str]) -> list[dict[str, Any]]:
    """
    Accepts a list of task descriptions and returns a structured list of tasks.
    Each task is a dict with an id, description, and created timestamp.
    Args:
        task_list: List of task descriptions (strings)
    Returns:
        List of task dicts
    """
    tasks = []
    for desc in task_list:
        if validate_input(desc):
            task = db.add_task(desc.strip())
            tasks.append(task)
    return tasks


def save_tasks(tasks: List[Dict[str, Any]]) -> bool:
    """
    Legacy function for compatibility - now uses database
    
    Args:
        tasks: List of task dictionaries (ignored in new implementation)
        
    Returns:
        bool: Always True as database handles persistence
    """
    # Database automatically persists data, so this is a no-op
    return True

def load_tasks() -> List[Dict[str, Any]]:
    """
    Load tasks from database
    
    Returns:
        List of task dictionaries from database
    """
    return db.get_all_tasks()

def add_task(description: str) -> Dict[str, Any]:
    """
    Add a single task to persistent storage
    
    Args:
        description: Task description
        
    Returns:
        The created task dictionary
    """
    return db.add_task(description.strip())

def complete_task(task_id: int) -> bool:
    """
    Mark a task as completed
    
    Args:
        task_id: ID of task to complete
        
    Returns:
        bool: True if task found and completed, False otherwise
    """
    result = db.complete_task(task_id)
    return result is not None

def delete_task(task_id: int) -> bool:
    """
    Delete a task from storage
    
    Args:
        task_id: ID of task to delete
        
    Returns:
        bool: True if task found and deleted, False otherwise
    """
    return db.delete_task(task_id)
