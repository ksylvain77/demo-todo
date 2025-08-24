#!/usr/bin/env python3
"""
todo app
a todo app

Entry point for the todo app application.
"""

from flask import Flask, jsonify, render_template
import os
import sys
from pathlib import Path

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

# Import your modules here
from modules.core import get_status, input_tasks, load_tasks, add_task, complete_task, delete_task
from modules.utils import get_timestamp, format_response
from flask import request

app = Flask(__name__)

@app.route('/api/tasks', methods=['POST'])
def api_input_tasks():
    """
    Accepts a JSON list of task descriptions OR single task description
    Request body: {"tasks": ["task1", "task2", ...]} OR {"description": "single task"}
    Response: {"status": ..., "timestamp": ..., "data": [task_dicts] OR task_dict}
    """
    if not request.is_json:
        return jsonify(format_response("Invalid or missing JSON", status="error")), 400
    data = request.get_json()
    
    # Handle bulk task creation (original functionality)
    if "tasks" in data:
        tasks = data.get("tasks")
        if not isinstance(tasks, list):
            return jsonify(format_response("'tasks' must be a list", status="error")), 400
        result = input_tasks(tasks)
        return jsonify(format_response(result))
    
    # Handle single task creation (new functionality)
    elif "description" in data:
        description = data.get("description")
        if not description or not isinstance(description, str) or not description.strip():
            return jsonify(format_response("'description' is required and must be non-empty", status="error")), 400
        result = add_task(description)
        return jsonify(format_response(result))
    
    else:
        return jsonify(format_response("Either 'tasks' or 'description' is required", status="error")), 400

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """
    Get all saved tasks from persistent storage
    Response: {"status": ..., "timestamp": ..., "data": [task_dicts]}
    """
    tasks = load_tasks()
    return jsonify(format_response(tasks))

@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def api_complete_task(task_id):
    """
    Mark a task as completed
    Response: {"status": ..., "timestamp": ..., "data": success_boolean}
    """
    result = complete_task(task_id)
    if result:
        return jsonify(format_response({"completed": True}))
    else:
        return jsonify(format_response("Task not found", status="error")), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """
    Delete a task
    Response: {"status": ..., "timestamp": ..., "data": success_boolean}
    """
    result = delete_task(task_id)
    if result:
        return jsonify(format_response({"deleted": True}))
    else:
        return jsonify(format_response("Task not found", status="error")), 404

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "todo_app",
        "timestamp": get_timestamp()
    })

@app.route('/')
def home():
    """Home page with web UI"""
    return render_template('index.html')

@app.route('/api')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        "name": "todo app API",
        "version": "0.2.0",
        "description": "a todo app",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Web UI"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api", "method": "GET", "description": "API documentation"},
            {"path": "/api/tasks", "method": "GET", "description": "Get all tasks"},
            {"path": "/api/tasks", "method": "POST", "description": "Add task(s)"},
            {"path": "/api/tasks/{id}/complete", "method": "PUT", "description": "Complete task"},
            {"path": "/api/tasks/{id}", "method": "DELETE", "description": "Delete task"}
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting todo app on port {port}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"🔍 Health check: http://localhost:5000/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
