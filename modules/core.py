"""
todo app - Core Module
Core business logic

This module contains the core business logic for todo app.
"""

from datetime import datetime
from typing import Dict, Any, List
import json
import os

def get_status() -> Dict[str, Any]:
    """
    Get the current application status
    
    Returns:
        Dict containing app status information
    """
    return {
        "status": "running",
        "service": "todo_app",
        "version": "0.1.0",
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
    from modules.utils import get_timestamp
    tasks = []
    for idx, desc in enumerate(task_list, 1):
        if validate_input(desc):
            tasks.append({
                "id": idx,
                "description": desc.strip(),
                "created": get_timestamp(),
                "completed": False
            })
    return tasks


TASKS_FILE = "tasks.json"

def save_tasks(tasks: List[Dict[str, Any]]) -> bool:
    """
    Save tasks list to JSON file
    
    Args:
        tasks: List of task dictionaries
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
        return True
    except Exception:
        return False

def load_tasks() -> List[Dict[str, Any]]:
    """
    Load tasks from JSON file
    
    Returns:
        List of task dictionaries, empty list if file doesn't exist
    """
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception:
        return []

def add_task(description: str) -> Dict[str, Any]:
    """
    Add a single task to persistent storage
    
    Args:
        description: Task description
        
    Returns:
        The created task dictionary
    """
    tasks = load_tasks()
    new_id = max([task.get('id', 0) for task in tasks], default=0) + 1
    
    from modules.utils import get_timestamp
    new_task = {
        "id": new_id,
        "description": description.strip(),
        "created": get_timestamp(),
        "completed": False
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

def complete_task(task_id: int) -> bool:
    """
    Mark a task as completed
    
    Args:
        task_id: ID of task to complete
        
    Returns:
        bool: True if task found and completed, False otherwise
    """
    tasks = load_tasks()
    for task in tasks:
        if task.get('id') == task_id:
            task['completed'] = True
            from modules.utils import get_timestamp
            task['completed_at'] = get_timestamp()
            save_tasks(tasks)
            return True
    return False

def delete_task(task_id: int) -> bool:
    """
    Delete a task from storage
    
    Args:
        task_id: ID of task to delete
        
    Returns:
        bool: True if task found and deleted, False otherwise
    """
    tasks = load_tasks()
    original_length = len(tasks)
    tasks = [task for task in tasks if task.get('id') != task_id]
    if len(tasks) < original_length:
        save_tasks(tasks)
        return True
    return False
