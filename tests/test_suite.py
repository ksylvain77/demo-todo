#!/usr/bin/env python3
"""
todo app - Comprehensive Testing Suite
Template for 4-phase testing methodology
"""

import sys
import os
import requests
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSuite:
    """
    Comprehensive testing suite template following 4-phase methodology:
    Phase 1: Backend Function Testing (MANDATORY)
    Phase 2: API Integration Testing (MANDATORY) 
    Phase 2.5: Data Contract Validation (MANDATORY)
    Phase 3: Frontend Integration Testing (MANDATORY)
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.results = {
            "phase_1_backend": {},
            "phase_2_api": {},
            "phase_2_5_contracts": {},
            "phase_3_frontend": {},
            "summary": {"total_tests": 0, "passed": 0, "failed": 0, "errors": []}
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log test message with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        icon = {"TEST": "🧪", "INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
        print(f"{icon.get(level, 'ℹ️')} [{timestamp}] {message}")
    
    def phase_1_backend_tests(self):
        """Phase 1: Test all backend functions directly"""
        self.log("🔬 PHASE 1: BACKEND FUNCTION TESTING", "TEST")
        self.log("=" * 60)
        
        # DRY configuration - customize for your project
        backend_tests = {
            "core_function": {
                "description": "Test core functionality",
                "module": "modules.core",
                "function": "get_status",
                "assertions": [
                    "assert 'status' in result",
                    "assert result['status'] == 'running'"
                ]
            },
            "input_tasks_basic": {
                "description": "Test input_tasks with a simple list of tasks",
                "module": "modules.core",
                "function": "input_tasks",
                "args": [["Buy milk", "Read book", "Write code"]],
                "assertions": [
                    "assert isinstance(result, list)",
                    "assert len(result) == 3",
                    "assert result[0]['description'] == 'Buy milk'",
                    "assert 'id' in result[1]",
                    "assert result[2]['completed'] == 0"
                ]
            },
            "input_tasks_empty": {
                "description": "Test input_tasks with an empty list",
                "module": "modules.core",
                "function": "input_tasks",
                "args": [[]],
                "assertions": [
                    "assert isinstance(result, list)",
                    "assert len(result) == 0"
                ]
            },
            "input_tasks_invalid": {
                "description": "Test input_tasks with invalid/blank tasks",
                "module": "modules.core",
                "function": "input_tasks",
                "args": [["", None, "  ", "Task"]],
                "assertions": [
                    "assert isinstance(result, list)",
                    "assert len(result) == 1",
                    "assert result[0]['description'] == 'Task'"
                ]
            },
            "save_load_tasks": {
                "description": "Test save_tasks and load_tasks functionality",
                "module": "modules.core",
                "function": "save_tasks",
                "args": [[{"id": 1, "description": "Test task", "completed": False}]],
                "assertions": [
                    "assert result is True"
                ]
            },
            "add_task_test": {
                "description": "Test add_task creates and stores task",
                "module": "modules.core", 
                "function": "add_task",
                "args": ["New test task"],
                "assertions": [
                    "assert isinstance(result, dict)",
                    "assert 'id' in result",
                    "assert result['description'] == 'New test task'",
                    "assert result['completed'] == 0"
                ]
            },
            "complete_task_test": {
                "description": "Test complete_task marks task as done",
                "module": "modules.core",
                "function": "complete_task", 
                "args": [2],
                "assertions": [
                    "assert result is True"
                ]
            },
            "delete_task_test": {
                "description": "Test delete_task removes task",
                "module": "modules.core",
                "function": "delete_task",
                "args": [21], 
                "assertions": [
                    "assert result is True"
                ]
            }
        }
        
        for test_name, test_config in backend_tests.items():
            self.log(f"Testing {test_config['description']}...")
            try:
                module = __import__(test_config['module'], fromlist=[test_config['function']])
                func = getattr(module, test_config['function'])
                args = test_config.get('args', [])
                result = func(*args)
                for assertion in test_config['assertions']:
                    exec(assertion)
                self.results["phase_1_backend"][test_name] = {
                    "success": True,
                    "result": "Test completed successfully",
                    "error": None
                }
                self.log(f"✅ {test_name}: PASSED", "PASS")
            except Exception as e:
                self.results["phase_1_backend"][test_name] = {
                    "success": False,
                    "result": None,
                    "error": str(e)
                }
                self.log(f"❌ {test_name}: FAILED - {e}", "FAIL")
    
    def phase_2_api_tests(self):
        """Phase 2: Test all API endpoints"""
        self.log("\n🌐 PHASE 2: API INTEGRATION TESTING", "TEST")
        self.log("=" * 60)
        
        api_tests = {
            "health_endpoint": {
                "endpoint": "/health",
                "expected_fields": ["status"]
            },
            "input_tasks_endpoint": {
                "endpoint": "/api/tasks",
                "method": "POST",
                "payload": {"tasks": ["Task A", "Task B"]},
                "expected_fields": ["status", "timestamp", "data"],
                "expected_data_length": 2
            },
            "get_tasks_endpoint": {
                "endpoint": "/api/tasks",
                "method": "GET",
                "expected_fields": ["status", "timestamp", "data"]
            },
            "add_single_task_endpoint": {
                "endpoint": "/api/tasks",
                "method": "POST", 
                "payload": {"description": "API test task"},
                "expected_fields": ["status", "timestamp", "data"]
            }
        }
        
        for test_name, test_config in api_tests.items():
            self.log(f"Testing {test_config['endpoint']}...")
            try:
                method = test_config.get("method", "GET")
                url = f"{self.base_url}{test_config['endpoint']}"
                if method == "POST":
                    response = requests.post(url, json=test_config.get("payload", {}), timeout=10)
                else:
                    response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code}")
                data = response.json()
                missing_fields = []
                for field in test_config['expected_fields']:
                    if field not in data:
                        missing_fields.append(field)
                if missing_fields:
                    raise Exception(f"Missing fields: {missing_fields}")
                # Additional checks for /api/tasks
                if test_name == "input_tasks_endpoint":
                    if not isinstance(data["data"], list) or len(data["data"]) != test_config["expected_data_length"]:
                        raise Exception("Returned data list does not match expected length")
                    if data["data"][0]["description"] != "Task A":
                        raise Exception("First task description mismatch")
                self.results["phase_2_api"][test_name] = {
                    "success": True,
                    "endpoint": test_config['endpoint'],
                    "expected_fields": test_config['expected_fields'],
                    "missing_fields": [],
                    "details": f"✅ All {len(test_config['expected_fields'])} fields present"
                }
                self.log(f"✅ {test_config['endpoint']}: PASSED", "PASS")
            except Exception as e:
                self.results["phase_2_api"][test_name] = {
                    "success": False,
                    "endpoint": test_config['endpoint'],
                    "error": str(e)
                }
                self.log(f"❌ {test_config['endpoint']}: FAILED - {e}", "FAIL")
    
    def phase_2_5_contract_validation(self):
        """Phase 2.5: Validate API-Frontend data contracts"""
        self.log("\n🔗 PHASE 2.5: DATA CONTRACT VALIDATION", "TEST")
        self.log("=" * 60)
        
        # Test data contracts between API and frontend
        contract_tests = {
            "main_contract": {
                "api_endpoint": "/health",
                "expected_structure": {
                    "status": "string"
                },
                "frontend_expectations": [
                    "data.status"
                ]
            },
            "input_tasks_contract": {
                "api_endpoint": "/api/tasks",
                "method": "POST",
                "payload": {"tasks": ["Contract Test"]},
                "expected_structure": {
                    "status": "string",
                    "timestamp": "string",
                    "data": "list"
                },
                "frontend_expectations": [
                    "data.data"
                ]
            },
            "get_tasks_contract": {
                "api_endpoint": "/api/tasks",
                "method": "GET",
                "expected_structure": {
                    "status": "string",
                    "timestamp": "string", 
                    "data": "list"
                },
                "frontend_expectations": [
                    "data.data"
                ]
            }
        }
        
        for test_name, test_config in contract_tests.items():
            self.log(f"Validating {test_config['api_endpoint']} contract...")
            
            try:
                method = test_config.get("method", "GET")
                if method == "POST":
                    response = requests.post(f"{self.base_url}{test_config['api_endpoint']}", json=test_config.get("payload", {}), timeout=10)
                else:
                    response = requests.get(f"{self.base_url}{test_config['api_endpoint']}", timeout=10)
                data = response.json()
                # Validate structure
                missing_fields = []
                for field_path, expected_type in test_config['expected_structure'].items():
                    if '.' in field_path:
                        parts = field_path.split('.')
                        current = data
                        for part in parts:
                            if part not in current:
                                missing_fields.append(field_path)
                                break
                            current = current[part]
                    else:
                        if field_path not in data:
                            missing_fields.append(field_path)
                        elif expected_type == "list" and not isinstance(data[field_path], list):
                            missing_fields.append(field_path)
                self.results["phase_2_5_contracts"][test_name] = {
                    "success": len(missing_fields) == 0,
                    "api_endpoint": test_config['api_endpoint'],
                    "missing_fields": missing_fields,
                    "sample_data": {k: str(v)[:50] for k, v in data.items() if k != 'error'}
                }
                if missing_fields:
                    self.log(f"❌ {test_name}: CONTRACT INVALID - Missing: {missing_fields}", "FAIL")
                else:
                    self.log(f"✅ {test_name}: CONTRACT VALID", "PASS")
                
            except Exception as e:
                self.results["phase_2_5_contracts"][test_name] = {
                    "success": False,
                    "error": str(e)
                }
                self.log(f"❌ {test_name}: CONTRACT ERROR - {e}", "FAIL")
    
    def phase_3_frontend_tests(self):
        """Phase 3: Test frontend functionality"""
        self.log("\n🖥️ PHASE 3: FRONTEND INTEGRATION TESTING", "TEST")
        self.log("=" * 60)
        
        # Basic frontend tests - extend with browser automation if needed
        frontend_tests = [
            ("page_load", self._test_page_load),
            ("web_ui_load", self._test_web_ui_load),
            ("playwright_ui", self._test_playwright_ui),
        ]
        
        for test_name, test_func in frontend_tests:
            self.log(f"Testing {test_name}...")
            
            try:
                success, result = test_func()
                
                self.results["phase_3_frontend"][test_name] = {
                    "success": success,
                    "result": result,
                    "error": None if success else result
                }
                
                if success:
                    self.log(f"✅ {test_name}: PASSED", "PASS")
                else:
                    self.log(f"❌ {test_name}: FAILED - {result}", "FAIL")
                    
            except Exception as e:
                self.results["phase_3_frontend"][test_name] = {
                    "success": False,
                    "result": None,
                    "error": str(e)
                }
                self.log(f"❌ {test_name}: ERROR - {e}", "FAIL")
    
    def _test_web_ui_load(self) -> Tuple[bool, str]:
        """Test web UI loads with expected elements"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}"
            
            content = response.text
            required_elements = ["todo app", "Add Task", "taskInput", "loadTasks"]
            missing_elements = [elem for elem in required_elements if elem.lower() not in content.lower()]
            
            if missing_elements:
                return False, f"Missing UI elements: {missing_elements}"
            
            return True, "Web UI loaded with all required elements"
        except Exception as e:
            return False, str(e)

    def _test_playwright_ui(self) -> Tuple[bool, str]:
        """Test web UI with Playwright browser automation"""
        try:
            # Import here to avoid dependency issues if playwright not installed
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Load the page
                page.goto(f"{self.base_url}/")
                
                # Check title
                title = page.title()
                if "Todo App" not in title:
                    return False, f"Wrong title: {title}"
                
                # Check key elements exist
                add_button = page.locator("button:has-text('Add Task')")
                task_input = page.locator("#taskInput")
                
                if not add_button.is_visible():
                    return False, "Add Task button not visible"
                if not task_input.is_visible():
                    return False, "Task input field not visible"
                
                browser.close()
                return True, "Playwright browser test passed"
                
        except ImportError:
            return False, "Playwright not installed"
        except Exception as e:
            return False, str(e)

    def _test_page_load(self) -> Tuple[bool, str]:
        """Test main page loading"""
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                return True, "Main page loaded successfully"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def generate_summary(self):
        """Generate test summary"""
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        errors = []
        
        for phase, tests in self.results.items():
            if phase == "summary":
                continue
                
            for test_name, result in tests.items():
                total_tests += 1
                if result.get("success", False):
                    passed_tests += 1
                else:
                    failed_tests += 1
                    error_msg = result.get("error", "Unknown error")
                    errors.append(f"{phase}.{test_name}: {error_msg}")
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": errors
        }
        
        return total_tests, passed_tests, failed_tests
    
    def run_all_tests(self):
        """Run complete test suite"""
        self.log("🚀 todo app - COMPREHENSIVE TEST SUITE", "TEST")
        self.log("=" * 80)
        self.log(f"Target: {self.base_url}")
        self.log(f"Started: {datetime.now().isoformat()}")
        self.log("")
        
        # Run all phases
        self.phase_1_backend_tests()
        self.phase_2_api_tests()
        self.phase_2_5_contract_validation()
        self.phase_3_frontend_tests()
        
        # Generate summary
        total, passed, failed = self.generate_summary()
        
        self.log("\n📊 FINAL TEST REPORT", "TEST")
        self.log("=" * 80)
        self.log(f"Total Tests: {total}")
        self.log(f"Passed: {passed}", "PASS")
        self.log(f"Failed: {failed}", "FAIL" if failed > 0 else "PASS")
        self.log("")
        
        # Save results
        timestamp = int(datetime.now().timestamp())
        results_file = f"test-results/test_results_{timestamp}.json"
        os.makedirs("test-results", exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.log(f"📄 Detailed report saved: {os.path.abspath(results_file)}")
        self.log(f"🎯 Success Rate: {(passed/total)*100:.1f}%")
        
        if failed == 0:
            self.log("🎉 ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL!", "PASS")
            return True
        else:
            self.log(f"❌ {failed} TESTS FAILED - REVIEW REQUIRED", "FAIL")
            return False

def main():
    """Main test runner"""
    suite = TestSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
