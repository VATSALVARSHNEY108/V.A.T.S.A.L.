"""
🧪 Sandbox Mode
Safely test automations without affecting the actual system
"""

import os
import json
import shutil
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import subprocess

class SandboxMode:
    """
    Isolated sandbox environment for testing automations safely
    Features:
    - Virtual file system
    - Command logging without execution
    - Undo/rollback capabilities
    - Safe testing environment
    - Execution simulation
    """
    
    def __init__(self):
        self.sandbox_dir = "sandbox_environment"
        self.virtual_fs_dir = os.path.join(self.sandbox_dir, "virtual_fs")
        self.log_file = os.path.join(self.sandbox_dir, "sandbox_log.json")
        self.config_file = os.path.join(self.sandbox_dir, "sandbox_config.json")
        self.session_file = os.path.join(self.sandbox_dir, "current_session.json")
        
        os.makedirs(self.sandbox_dir, exist_ok=True)
        os.makedirs(self.virtual_fs_dir, exist_ok=True)
        
        self.config = self._load_config()
        self.session = self._load_session()
        self.command_log = []
        
        self.sandbox_active = False
        self.safe_commands = ["echo", "ls", "pwd", "cat", "grep", "find", "head", "tail"]
        self.blocked_commands = ["rm -rf", "format", "del /s", "shutdown", "reboot", "kill -9"]
    
    def _load_config(self) -> Dict:
        """Load sandbox configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "allow_file_operations": True,
            "allow_network_operations": False,
            "allow_system_commands": False,
            "log_all_actions": True,
            "auto_rollback_on_error": True,
            "max_session_duration_minutes": 60
        }
    
    def _save_config(self):
        """Save sandbox configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _load_session(self) -> Dict:
        """Load current sandbox session"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "session_id": None,
            "start_time": None,
            "end_time": None,
            "actions_performed": [],
            "status": "inactive"
        }
    
    def _save_session(self):
        """Save current session"""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.session, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def start_sandbox(self, session_name: Optional[str] = None) -> Dict:
        """
        Start a new sandbox session
        
        Args:
            session_name: Optional name for the session
        
        Returns:
            Dict with session info
        """
        try:
            if self.sandbox_active:
                return {
                    "success": False,
                    "message": "Sandbox already active"
                }
            
            session_id = session_name or f"sandbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            session_dir = os.path.join(self.virtual_fs_dir, session_id)
            os.makedirs(session_dir, exist_ok=True)
            
            self.session = {
                "session_id": session_id,
                "start_time": datetime.now().isoformat(),
                "end_time": None,
                "session_dir": session_dir,
                "actions_performed": [],
                "status": "active"
            }
            
            self.sandbox_active = True
            self.command_log = []
            
            self._save_session()
            
            print(f"🧪 Sandbox session started: {session_id}")
            print(f"   Working directory: {session_dir}")
            print(f"   Mode: Safe testing environment")
            
            return {
                "success": True,
                "session_id": session_id,
                "session_dir": session_dir,
                "message": "Sandbox session started successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error starting sandbox: {str(e)}"
            }
    
    def execute_command(self, command: str, simulate: bool = True) -> Dict:
        """
        Execute or simulate a command in sandbox
        
        Args:
            command: Command to execute
            simulate: If True, only simulate (don't actually execute)
        
        Returns:
            Dict with execution result
        """
        if not self.sandbox_active:
            return {
                "success": False,
                "message": "Sandbox not active. Start a session first."
            }
        
        for blocked_cmd in self.blocked_commands:
            if blocked_cmd in command.lower():
                return {
                    "success": False,
                    "message": f"Blocked command detected: {blocked_cmd}",
                    "severity": "critical"
                }
        
        action = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "simulated": simulate,
            "status": "pending"
        }
        
        try:
            if simulate:
                print(f"🎬 SIMULATING: {command}")
                result = f"[SIMULATED] Command would execute: {command}"
                action["status"] = "simulated"
                action["result"] = result
            else:
                if any(safe_cmd in command for safe_cmd in self.safe_commands):
                    print(f"▶️  EXECUTING SAFE: {command}")
                    
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        cwd=self.session["session_dir"]
                    )
                    
                    action["status"] = "executed"
                    action["return_code"] = result.returncode
                    action["stdout"] = result.stdout
                    action["stderr"] = result.stderr
                else:
                    return {
                        "success": False,
                        "message": "Command not in safe list. Use simulate=True or add to safe commands."
                    }
            
            self.command_log.append(action)
            self.session["actions_performed"].append(action)
            self._save_session()
            
            return {
                "success": True,
                "action": action,
                "message": "Command processed successfully"
            }
            
        except subprocess.TimeoutExpired:
            action["status"] = "timeout"
            return {
                "success": False,
                "message": "Command timed out"
            }
        except Exception as e:
            action["status"] = "error"
            action["error"] = str(e)
            return {
                "success": False,
                "message": f"Execution error: {str(e)}"
            }
    
    def create_virtual_file(self, filename: str, content: str) -> Dict:
        """
        Create a file in the sandbox virtual filesystem
        
        Args:
            filename: Name of file to create
            content: File content
        
        Returns:
            Dict with creation result
        """
        if not self.sandbox_active:
            return {
                "success": False,
                "message": "Sandbox not active"
            }
        
        try:
            file_path = os.path.join(self.session["session_dir"], filename)
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            action = {
                "timestamp": datetime.now().isoformat(),
                "action_type": "create_file",
                "filename": filename,
                "file_path": file_path,
                "size": len(content)
            }
            
            self.session["actions_performed"].append(action)
            self._save_session()
            
            print(f"📄 Created virtual file: {filename}")
            
            return {
                "success": True,
                "file_path": file_path,
                "message": f"File created: {filename}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating file: {str(e)}"
            }
    
    def read_virtual_file(self, filename: str) -> Dict:
        """Read a file from the sandbox virtual filesystem"""
        if not self.sandbox_active:
            return {
                "success": False,
                "message": "Sandbox not active"
            }
        
        try:
            file_path = os.path.join(self.session["session_dir"], filename)
            
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"File not found: {filename}"
                }
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            return {
                "success": True,
                "content": content,
                "file_path": file_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading file: {str(e)}"
            }
    
    def list_virtual_files(self) -> Dict:
        """List all files in the sandbox virtual filesystem"""
        if not self.sandbox_active:
            return {
                "success": False,
                "message": "Sandbox not active"
            }
        
        try:
            session_dir = self.session["session_dir"]
            files = []
            
            for root, dirs, filenames in os.walk(session_dir):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, session_dir)
                    
                    stat = os.stat(file_path)
                    files.append({
                        "name": filename,
                        "path": rel_path,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
            
            return {
                "success": True,
                "files": files,
                "count": len(files)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error listing files: {str(e)}"
            }
    
    def get_session_log(self) -> Dict:
        """Get log of all actions in current session"""
        if not self.sandbox_active:
            return {
                "success": False,
                "message": "No active session"
            }
        
        return {
            "success": True,
            "session_id": self.session["session_id"],
            "start_time": self.session["start_time"],
            "actions_count": len(self.session["actions_performed"]),
            "actions": self.session["actions_performed"]
        }
    
    def rollback_session(self) -> Dict:
        """Rollback all changes in current session"""
        if not self.sandbox_active:
            return {
                "success": False,
                "message": "No active session to rollback"
            }
        
        try:
            session_dir = self.session["session_dir"]
            
            if os.path.exists(session_dir):
                shutil.rmtree(session_dir)
                os.makedirs(session_dir, exist_ok=True)
            
            print(f"🔄 Session rolled back: {self.session['session_id']}")
            
            return {
                "success": True,
                "message": "Session rolled back successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Rollback error: {str(e)}"
            }
    
    def end_sandbox(self, keep_session: bool = False) -> Dict:
        """
        End the current sandbox session
        
        Args:
            keep_session: Keep session data after ending
        
        Returns:
            Dict with session summary
        """
        if not self.sandbox_active:
            return {
                "success": False,
                "message": "No active sandbox session"
            }
        
        try:
            self.session["end_time"] = datetime.now().isoformat()
            self.session["status"] = "completed"
            
            summary = {
                "session_id": self.session["session_id"],
                "duration": self._calculate_duration(),
                "actions_performed": len(self.session["actions_performed"]),
                "files_created": len([a for a in self.session["actions_performed"] if a.get("action_type") == "create_file"]),
                "commands_executed": len([a for a in self.session["actions_performed"] if a.get("command")])
            }
            
            self._save_session()
            
            if not keep_session:
                session_dir = self.session["session_dir"]
                if os.path.exists(session_dir):
                    shutil.rmtree(session_dir)
            
            self.sandbox_active = False
            
            print(f"🏁 Sandbox session ended")
            print(f"   Duration: {summary['duration']}")
            print(f"   Actions: {summary['actions_performed']}")
            
            return {
                "success": True,
                "summary": summary,
                "message": "Sandbox session ended successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error ending session: {str(e)}"
            }
    
    def _calculate_duration(self) -> str:
        """Calculate session duration"""
        try:
            start = datetime.fromisoformat(self.session["start_time"])
            end = datetime.fromisoformat(self.session["end_time"]) if self.session["end_time"] else datetime.now()
            
            duration = end - start
            minutes = int(duration.total_seconds() / 60)
            seconds = int(duration.total_seconds() % 60)
            
            return f"{minutes}m {seconds}s"
        except:
            return "Unknown"
    
    def get_sandbox_status(self) -> Dict:
        """Get current sandbox status"""
        return {
            "active": self.sandbox_active,
            "session_id": self.session.get("session_id"),
            "start_time": self.session.get("start_time"),
            "actions_count": len(self.session.get("actions_performed", [])),
            "allow_file_operations": self.config["allow_file_operations"],
            "allow_system_commands": self.config["allow_system_commands"]
        }


if __name__ == "__main__":
    print("🧪 Sandbox Mode")
    print("=" * 50)
    
    sandbox = SandboxMode()
    
    print("\n📊 Sandbox Status:")
    status = sandbox.get_sandbox_status()
    print(f"Active: {status['active']}")
    print(f"Session ID: {status['session_id']}")
    
    print("\n" + "=" * 50)
    print("✅ Sandbox mode ready!")
