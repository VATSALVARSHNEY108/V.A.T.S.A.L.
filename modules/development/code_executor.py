"""
Code Execution Module
Safely execute generated code and show results
"""

import subprocess
import sys
import tempfile
import os
from typing import Dict

def execute_python_code(code: str, timeout: int = 10) -> Dict:
    """
    Execute Python code safely and return output
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
    
    Returns:
        Dict with success, output, and error
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Execution timeout after {timeout} seconds",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "return_code": -1
        }

def execute_javascript_code(code: str, timeout: int = 10) -> Dict:
    """Execute JavaScript code using Node.js"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    except FileNotFoundError:
        return {
            "success": False,
            "output": "",
            "error": "Node.js not installed",
            "return_code": -1
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Execution timeout after {timeout} seconds",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "return_code": -1
        }

def validate_code_safety(code: str, language: str = "python") -> Dict:
    """
    Check if code appears safe to execute
    
    Returns:
        Dict with is_safe flag and warnings
    """
    dangerous_patterns = {
        "python": [
            "import os", "import sys", "import subprocess",
            "exec(", "eval(", "__import__",
            "open(", "file(", "input(",
            "rmdir", "remove", "unlink"
        ],
        "javascript": [
            "require('fs')", "require('child_process')",
            "eval(", "exec(",
            "process.exit"
        ]
    }
    
    patterns = dangerous_patterns.get(language.lower(), [])
    warnings = []
    
    for pattern in patterns:
        if pattern in code:
            warnings.append(f"Potentially dangerous: {pattern}")
    
    return {
        "is_safe": len(warnings) == 0,
        "warnings": warnings,
        "recommendation": "Review before executing" if warnings else "Appears safe"
    }
