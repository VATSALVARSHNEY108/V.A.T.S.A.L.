#!/usr/bin/env python3
"""
VATSAL - Intelligent Desktop Automator
Combines local automation scripts with minimal Gemini API support.

Purpose:
- Interpret user commands using Gemini for NLU
- Execute all actions locally via Python modules
- No external APIs for system actions
"""

import os
import sys
import json
import time
import platform
import psutil
import subprocess
import pyperclip
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import types

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

try:
    from vatsal_enhanced_modules import (
        ScreenMonitor, AdvancedFileManager, SystemController,
        WindowController, ClipboardManager, AutomationWorkflows
    )
    ENHANCED_MODULES_AVAILABLE = True
except ImportError:
    ENHANCED_MODULES_AVAILABLE = False

load_dotenv()


class VATSALAutomator:
    """Intelligent desktop automator with local execution and AI understanding"""
    
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY required for command understanding")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"
        self.pending_confirmations = []
        
        if PYAUTOGUI_AVAILABLE and pyautogui:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.5
        
    def understand_command(self, user_input: str) -> Dict:
        """Use Gemini ONLY for understanding intent and task decomposition"""
        
        system_prompt = """You are VATSAL's command interpreter. Parse commands into structured actions for LOCAL execution only.

Your ONLY job: Understand intent and decompose complex tasks into simple steps.

Return JSON with this structure:
{
  "intent": "brief intent description",
  "requires_confirmation": true/false,
  "risk_level": "safe/moderate/destructive",
  "actions": [
    {
      "type": "open_app|close_app|click|type|keyboard|mouse|screenshot|file_create|file_delete|file_move|folder_open|process_kill|system_info|system_report|search_files|minimize_all|clipboard_copy|clipboard_paste|lock_screen|shutdown_system|restart_system|cancel_shutdown|wait",
      "params": {}
    }
  ]
}

Action types and parameters:

LOCAL EXECUTION ACTIONS:
- open_app: {"app": "notepad|chrome|explorer|calculator|cmd|etc"}
- close_app: {"app": "name"}
- click: {"button": "left|right|middle", "x": null, "y": null} 
- type: {"text": "string to type"}
- keyboard: {"keys": ["ctrl", "c"]} or {"key": "enter"}
- mouse: {"x": 100, "y": 200}
- screenshot: {"path": "screenshots/name.png"}
- file_create: {"path": "path/file.txt", "content": "text"}
- file_delete: {"path": "path/file.txt"}
- file_move: {"source": "path/file.txt", "dest": "path/new.txt"}
- folder_open: {"path": "C:/Users/Desktop" or "Desktop|Documents|Downloads"}
- process_kill: {"name": "process_name"}
- system_info: {"type": "cpu|memory|disk|battery|processes"}
- system_report: {} (comprehensive system health report)
- search_files: {"directory": "path", "pattern": "*.txt"}
- minimize_all: {} (minimize all windows)
- clipboard_copy: {"text": "text to copy"}
- clipboard_paste: {} (get clipboard content)
- lock_screen: {} (lock computer screen)
- shutdown_system: {"delay_seconds": 10} (shutdown computer with delay)
- restart_system: {"delay_seconds": 10} (restart computer with delay)
- cancel_shutdown: {} (cancel any scheduled shutdown/restart)
- wait: {"seconds": 2}

Examples:

"Open Notepad and type Hello"
{
  "intent": "Open notepad, type text",
  "requires_confirmation": false,
  "risk_level": "safe",
  "actions": [
    {"type": "open_app", "params": {"app": "notepad"}},
    {"type": "wait", "params": {"seconds": 1}},
    {"type": "type", "params": {"text": "Hello"}}
  ]
}

"Delete the old files folder"
{
  "intent": "Delete folder with files",
  "requires_confirmation": true,
  "risk_level": "destructive",
  "actions": [
    {"type": "file_delete", "params": {"path": "old_files"}}
  ]
}

"Show me system info"
{
  "intent": "Display system information",
  "requires_confirmation": false,
  "risk_level": "safe",
  "actions": [
    {"type": "system_info", "params": {"type": "cpu"}},
    {"type": "system_info", "params": {"type": "memory"}},
    {"type": "system_info", "params": {"type": "disk"}}
  ]
}

"Lock the screen"
{
  "intent": "Lock computer screen",
  "requires_confirmation": false,
  "risk_level": "safe",
  "actions": [
    {"type": "lock_screen", "params": {}}
  ]
}

"Shutdown computer"
{
  "intent": "Shutdown computer with 10 second delay",
  "requires_confirmation": true,
  "risk_level": "moderate",
  "actions": [
    {"type": "shutdown_system", "params": {"delay_seconds": 10}}
  ]
}

CRITICAL RULES:
1. NEVER suggest external APIs or online actions
2. ALL actions must be locally executable
3. Mark file deletion/modification as "destructive"
4. Return ONLY valid JSON
5. Keep actions simple and atomic"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                    response_mime_type="application/json"
                )
            )
            
            command_data = json.loads(response.text)
            return command_data
            
        except Exception as e:
            return {
                "intent": "Error understanding command",
                "requires_confirmation": False,
                "risk_level": "safe",
                "actions": [],
                "error": str(e)
            }
    
    def execute_action(self, action: Dict) -> Tuple[bool, str]:
        """Execute a single action locally using Python modules"""
        
        action_type = action.get("type")
        params = action.get("params", {})
        
        try:
            if action_type == "open_app":
                return self._open_application(params.get("app"))
                
            elif action_type == "close_app":
                return self._close_application(params.get("app"))
                
            elif action_type == "click":
                return self._perform_click(params)
                
            elif action_type == "type":
                return self._type_text(params.get("text"))
                
            elif action_type == "keyboard":
                return self._press_keys(params)
                
            elif action_type == "mouse":
                return self._move_mouse(params.get("x"), params.get("y"))
                
            elif action_type == "screenshot":
                return self._take_screenshot(params.get("path"))
                
            elif action_type == "file_create":
                return self._create_file(params.get("path"), params.get("content", ""))
                
            elif action_type == "file_delete":
                return self._delete_file(params.get("path"))
                
            elif action_type == "file_move":
                return self._move_file(params.get("source"), params.get("dest"))
                
            elif action_type == "folder_open":
                return self._open_folder(params.get("path"))
                
            elif action_type == "process_kill":
                return self._kill_process(params.get("name"))
                
            elif action_type == "system_info":
                return self._get_system_info(params.get("type"))
                
            elif action_type == "wait":
                time.sleep(params.get("seconds", 1))
                return True, f"Waited {params.get('seconds', 1)}s"
            
            elif action_type == "search_files" and ENHANCED_MODULES_AVAILABLE:
                return self._search_files_enhanced(params)
            
            elif action_type == "system_report" and ENHANCED_MODULES_AVAILABLE:
                return self._system_report_enhanced()
            
            elif action_type == "minimize_all" and ENHANCED_MODULES_AVAILABLE:
                WindowController.minimize_all_windows()
                return True, "Minimized all windows"
            
            elif action_type == "clipboard_copy" and ENHANCED_MODULES_AVAILABLE:
                ClipboardManager.copy_to_clipboard(params.get("text", ""))
                return True, "Copied to clipboard"
            
            elif action_type == "clipboard_paste" and ENHANCED_MODULES_AVAILABLE:
                text = ClipboardManager.get_from_clipboard()
                return True, f"Clipboard: {text[:100]}"
            
            elif action_type == "lock_screen":
                return self._lock_screen()
            
            elif action_type == "shutdown_system":
                delay = params.get("delay_seconds", 10)
                return self._shutdown_system(delay)
            
            elif action_type == "restart_system":
                delay = params.get("delay_seconds", 10)
                return self._restart_system(delay)
            
            elif action_type == "cancel_shutdown":
                return self._cancel_shutdown()
                
            else:
                return False, f"Unknown action: {action_type}"
                
        except Exception as e:
            return False, f"Error executing {action_type}: {str(e)}"
    
    def _open_application(self, app_name: str) -> Tuple[bool, str]:
        """Open application using subprocess"""
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "paint": "mspaint.exe",
            "wordpad": "write.exe"
        }
        
        app_exec = app_map.get(app_name.lower(), app_name)
        
        try:
            subprocess.Popen(app_exec)
            return True, f"Opened {app_name}"
        except Exception as e:
            return False, f"Failed to open {app_name}: {str(e)}"
    
    def _close_application(self, app_name: str) -> Tuple[bool, str]:
        """Close application by name"""
        try:
            killed = 0
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    killed += 1
            
            if killed > 0:
                return True, f"Closed {killed} instance(s) of {app_name}"
            else:
                return False, f"{app_name} not found"
        except Exception as e:
            return False, f"Error closing {app_name}: {str(e)}"
    
    def _perform_click(self, params: Dict) -> Tuple[bool, str]:
        """Perform mouse click"""
        button = params.get("button", "left")
        x = params.get("x")
        y = params.get("y")
        
        if x is not None and y is not None:
            pyautogui.click(x, y, button=button)
            return True, f"Clicked {button} at ({x}, {y})"
        else:
            pyautogui.click(button=button)
            return True, f"Clicked {button} at current position"
    
    def _type_text(self, text: str) -> Tuple[bool, str]:
        """Type text using pyautogui"""
        if not text:
            return False, "No text provided"
        
        pyautogui.write(text, interval=0.05)
        return True, f"Typed: {text[:50]}{'...' if len(text) > 50 else ''}"
    
    def _press_keys(self, params: Dict) -> Tuple[bool, str]:
        """Press keyboard keys or combinations"""
        if "keys" in params:
            keys = params["keys"]
            pyautogui.hotkey(*keys)
            return True, f"Pressed: {'+'.join(keys)}"
        elif "key" in params:
            key = params["key"]
            pyautogui.press(key)
            return True, f"Pressed: {key}"
        else:
            return False, "No keys specified"
    
    def _move_mouse(self, x: int, y: int) -> Tuple[bool, str]:
        """Move mouse to coordinates"""
        if x is None or y is None:
            return False, "Coordinates required"
        
        pyautogui.moveTo(x, y)
        return True, f"Moved mouse to ({x}, {y})"
    
    def _take_screenshot(self, path: str) -> Tuple[bool, str]:
        """Take screenshot and save"""
        if not path:
            path = f"screenshots/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else "screenshots", exist_ok=True)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return True, f"Screenshot saved: {path}"
    
    def _create_file(self, path: str, content: str) -> Tuple[bool, str]:
        """Create file with content"""
        if not path:
            return False, "File path required"
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, f"Created: {path}"
    
    def _delete_file(self, path: str) -> Tuple[bool, str]:
        """Delete file or folder"""
        if not path:
            return False, "Path required"
        
        path_obj = Path(path)
        
        if path_obj.is_file():
            path_obj.unlink()
            return True, f"Deleted file: {path}"
        elif path_obj.is_dir():
            import shutil
            shutil.rmtree(path)
            return True, f"Deleted folder: {path}"
        else:
            return False, f"Path not found: {path}"
    
    def _move_file(self, source: str, dest: str) -> Tuple[bool, str]:
        """Move or rename file"""
        if not source or not dest:
            return False, "Source and destination required"
        
        import shutil
        shutil.move(source, dest)
        return True, f"Moved: {source} → {dest}"
    
    def _open_folder(self, path: str) -> Tuple[bool, str]:
        """Open folder in file explorer"""
        if not path:
            return False, "Folder path required"
        
        special_folders = {
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "home": os.path.expanduser("~")
        }
        
        folder_path = special_folders.get(path.lower(), path)
        
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
            return True, f"Opened: {folder_path}"
        else:
            return False, f"Folder not found: {path}"
    
    def _kill_process(self, name: str) -> Tuple[bool, str]:
        """Kill process by name"""
        if not name:
            return False, "Process name required"
        
        killed = 0
        for proc in psutil.process_iter(['name']):
            if name.lower() in proc.info['name'].lower():
                proc.kill()
                killed += 1
        
        if killed > 0:
            return True, f"Killed {killed} process(es): {name}"
        else:
            return False, f"Process not found: {name}"
    
    def _get_system_info(self, info_type: str) -> Tuple[bool, str]:
        """Get system information"""
        try:
            if info_type == "cpu":
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                return True, f"CPU: {cpu_percent}% ({cpu_count} cores)"
                
            elif info_type == "memory":
                mem = psutil.virtual_memory()
                return True, f"Memory: {mem.percent}% ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)"
                
            elif info_type == "disk":
                disk = psutil.disk_usage('/')
                return True, f"Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"
                
            elif info_type == "battery":
                battery = psutil.sensors_battery()
                if battery:
                    return True, f"Battery: {battery.percent}% {'(charging)' if battery.power_plugged else '(discharging)'}"
                else:
                    return True, "No battery detected"
                    
            elif info_type == "processes":
                procs = len(list(psutil.process_iter()))
                return True, f"Running processes: {procs}"
                
            else:
                return False, f"Unknown info type: {info_type}"
                
        except Exception as e:
            return False, f"Error getting {info_type}: {str(e)}"
    
    def _search_files_enhanced(self, params: Dict) -> Tuple[bool, str]:
        """Search files using enhanced file manager"""
        try:
            directory = params.get("directory", ".")
            pattern = params.get("pattern", "*")
            files = AdvancedFileManager.search_files(directory, pattern)
            
            if files:
                return True, f"Found {len(files)} files matching '{pattern}'"
            else:
                return True, f"No files found matching '{pattern}'"
        except Exception as e:
            return False, f"Search error: {str(e)}"
    
    def _system_report_enhanced(self) -> Tuple[bool, str]:
        """Get comprehensive system report"""
        try:
            report = SystemController.get_full_system_report()
            
            summary = f"""System Report:
CPU: {report['cpu']['usage_percent']}% ({report['cpu']['count']} cores)
Memory: {report['memory']['percent']}% ({report['memory']['used_gb']}/{report['memory']['total_gb']} GB)
Disk: {report['disk']['percent']}% ({report['disk']['used_gb']}/{report['disk']['total_gb']} GB)
Battery: {report['battery'].get('percent', 'N/A')}%"""
            
            return True, summary
        except Exception as e:
            return False, f"Report error: {str(e)}"
    
    def _lock_screen(self) -> Tuple[bool, str]:
        """Lock the computer screen"""
        try:
            os_type = platform.system()
            if os_type == "Windows":
                subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, check=False)
                return True, "🔒 Screen locked"
            elif os_type == "Darwin":
                subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"], check=False)
                return True, "🔒 Screen locked"
            elif os_type == "Linux":
                subprocess.run(["loginctl", "lock-session"], check=False)
                return True, "🔒 Screen locked"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Failed to lock screen: {str(e)}"
    
    def _shutdown_system(self, delay_seconds: int = 10) -> Tuple[bool, str]:
        """Shutdown the computer"""
        try:
            os_type = platform.system()
            if os_type == "Windows":
                subprocess.Popen(f'shutdown /s /t {delay_seconds}', shell=True)
                return True, f"⚠️ Computer will shutdown in {delay_seconds} seconds"
            elif os_type == "Darwin":
                subprocess.Popen(f'sudo shutdown -h +{delay_seconds//60}', shell=True)
                return True, f"⚠️ Computer will shutdown in {delay_seconds} seconds"
            elif os_type == "Linux":
                subprocess.Popen(f'sudo shutdown -h +{delay_seconds//60}', shell=True)
                return True, f"⚠️ Computer will shutdown in {delay_seconds} seconds"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Failed to shutdown: {str(e)}"
    
    def _restart_system(self, delay_seconds: int = 10) -> Tuple[bool, str]:
        """Restart the computer"""
        try:
            os_type = platform.system()
            if os_type == "Windows":
                subprocess.Popen(f'shutdown /r /t {delay_seconds}', shell=True)
                return True, f"🔄 Computer will restart in {delay_seconds} seconds"
            elif os_type == "Darwin":
                subprocess.Popen(f'sudo shutdown -r +{delay_seconds//60}', shell=True)
                return True, f"🔄 Computer will restart in {delay_seconds} seconds"
            elif os_type == "Linux":
                subprocess.Popen(f'sudo shutdown -r +{delay_seconds//60}', shell=True)
                return True, f"🔄 Computer will restart in {delay_seconds} seconds"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Failed to restart: {str(e)}"
    
    def _cancel_shutdown(self) -> Tuple[bool, str]:
        """Cancel scheduled shutdown or restart"""
        try:
            os_type = platform.system()
            if os_type == "Windows":
                subprocess.run("shutdown /a", shell=True, check=False)
                return True, "✅ Shutdown/restart cancelled"
            elif os_type in ["Darwin", "Linux"]:
                subprocess.run("sudo killall shutdown", shell=True, check=False)
                return True, "✅ Shutdown/restart cancelled"
            else:
                return False, "Unsupported operating system"
        except Exception as e:
            return False, f"Failed to cancel: {str(e)}"
    
    def execute_command(self, user_input: str, confirmation_callback=None) -> str:
        """Main execution flow: understand → confirm → execute
        
        Args:
            user_input: Natural language command
            confirmation_callback: Optional function(intent, risk_level) -> bool for GUI confirmations
        """
        
        command = self.understand_command(user_input)
        
        if "error" in command:
            return f"⚠️ Could not understand: {command['error']}"
        
        intent = command.get("intent", "Unknown intent")
        actions = command.get("actions", [])
        risk_level = command.get("risk_level", "safe")
        
        if not actions:
            return "❌ No actions identified. Please clarify your request."
        
        if command.get("requires_confirmation", False):
            if confirmation_callback:
                if not confirmation_callback(intent, risk_level):
                    return "❌ Action cancelled by user"
            else:
                confirmation = input(f"\n⚠️ This action is {risk_level}: {intent}\nContinue? (yes/no): ").strip().lower()
                if confirmation not in ['yes', 'y']:
                    return "❌ Action cancelled by user"
        
        results = []
        for i, action in enumerate(actions, 1):
            success, message = self.execute_action(action)
            
            if success:
                results.append(f"✓ {message}")
            else:
                results.append(f"✗ {message}")
                break
        
        return "\n".join(results)


def main():
    """CLI for VATSAL Desktop Automator"""
    
    print("=" * 70)
    print("  VATSAL — Intelligent Desktop Automator")
    print("  Local execution • AI understanding")
    print("=" * 70)
    print("\n💡 Examples:")
    print("   • 'Open notepad and type Hello World'")
    print("   • 'Show system info'")
    print("   • 'Take a screenshot'")
    print("   • 'Open Desktop folder'")
    print("\n⚠️  Safety: Destructive actions require confirmation")
    print("=" * 70)
    
    if not os.getenv("GEMINI_API_KEY"):
        print("\n❌ GEMINI_API_KEY not found")
        sys.exit(1)
    
    try:
        vatsal = VATSALAutomator()
        print("\n✅ VATSAL ready\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    while True:
        try:
            command = input("\n🎯 Command: ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye")
                break
            
            result = vatsal.execute_command(command)
            print(f"\n{result}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
