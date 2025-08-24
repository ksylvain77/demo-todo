"""
todo app - Core Module
Core business logic

This module contains the core business logic for todo app.
"""

from datetime import datetime
from typing import Dict, Any

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
