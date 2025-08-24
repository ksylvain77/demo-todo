#!/usr/bin/env python3
"""
todo app
a todo app

Entry point for the todo app application.
"""


from flask import Flask, jsonify
import os
import sys
from pathlib import Path


# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

app = Flask(__name__)

# Import your modules here
from modules.core import get_status, input_tasks
from modules.utils import get_timestamp, format_response
from flask import request

@app.route('/api/tasks', methods=['POST'])
def api_input_tasks():
    """
    Accepts a JSON list of task descriptions and returns structured tasks.
    Request body: {"tasks": ["task1", "task2", ...]}
    Response: {"status": ..., "timestamp": ..., "data": [task_dicts]}
    """
    if not request.is_json:
        return jsonify(format_response("Invalid or missing JSON", status="error")), 400
    data = request.get_json()
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        return jsonify(format_response("'tasks' must be a list", status="error")), 400
    result = input_tasks(tasks)
    return jsonify(format_response(result))



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
    """Home endpoint"""
    status = get_status()
    return jsonify({
        "message": "Welcome to todo app",
        "description": "a todo app",
        "status": status,
        "endpoints": {
            "health": "/health",
            "home": "/",
            "api_docs": "/api"
        }
    })

@app.route('/api')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        "name": "todo app API",
        "version": "0.1.0",
        "description": "a todo app",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Home page"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api", "method": "GET", "description": "API documentation"}
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting todo app on port {port}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"🔍 Health check: http://localhost:5000/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
