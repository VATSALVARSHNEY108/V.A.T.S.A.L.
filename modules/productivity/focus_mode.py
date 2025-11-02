"""
Focus Mode Automation - Automatically blocks distracting apps/websites during deep work
Smart blocking with scheduled focus sessions
"""

import json
import psutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import platform


class FocusModeAutomation:
    """Manages focus mode with app and website blocking"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.focus_config_file = self.data_dir / "focus_mode_config.json"
        self.load_config()
        
        self.is_active = False
        self.session_start = None
        self.blocked_apps_count = 0
        
    def load_config(self):
        """Load focus mode configuration"""
        if self.focus_config_file.exists():
            with open(self.focus_config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "blocked_apps": [
                    "chrome.exe", "firefox.exe", "msedge.exe",
                    "spotify.exe", "steam.exe", "discord.exe",
                    "slack.exe", "teams.exe"
                ],
                "blocked_websites": [
                    "facebook.com", "instagram.com", "twitter.com",
                    "youtube.com", "reddit.com", "tiktok.com",
                    "netflix.com"
                ],
                "allowed_apps": [
                    "vscode.exe", "pycharm64.exe", "sublime_text.exe",
                    "notepad++.exe", "powershell.exe", "cmd.exe"
                ],
                "focus_duration_minutes": 25,
                "auto_block": True,
                "show_notifications": True
            }
            self.save_config()
    
    def save_config(self):
        """Save focus mode configuration"""
        with open(self.focus_config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def start_focus_mode(self, duration_minutes=None):
        """Start focus mode"""
        if self.is_active:
            return {"success": False, "message": "Focus mode already active"}
        
        duration = duration_minutes or self.config["focus_duration_minutes"]
        self.is_active = True
        self.session_start = datetime.now()
        self.session_end = self.session_start + timedelta(minutes=duration)
        
        # Block distracting apps
        blocked = self.block_distracting_apps()
        
        return {
            "success": True,
            "message": f"🎯 Focus mode activated for {duration} minutes",
            "duration_minutes": duration,
            "apps_blocked": blocked["count"],
            "end_time": self.session_end.strftime("%H:%M")
        }
    
    def stop_focus_mode(self):
        """Stop focus mode"""
        if not self.is_active:
            return {"success": False, "message": "Focus mode not active"}
        
        self.is_active = False
        duration = (datetime.now() - self.session_start).total_seconds() / 60
        
        return {
            "success": True,
            "message": "✅ Focus mode ended",
            "duration_minutes": round(duration, 1),
            "started_at": self.session_start.strftime("%H:%M"),
            "ended_at": datetime.now().strftime("%H:%M")
        }
    
    def block_distracting_apps(self):
        """Block apps in the blocked list"""
        blocked = []
        
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name']
                    
                    # Check if app should be blocked
                    if proc_name.lower() in [app.lower() for app in self.config["blocked_apps"]]:
                        # Don't block if it's in allowed list
                        if proc_name.lower() not in [app.lower() for app in self.config["allowed_apps"]]:
                            proc.terminate()
                            blocked.append(proc_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.blocked_apps_count = len(blocked)
            
            return {
                "success": True,
                "count": len(blocked),
                "apps": blocked
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_blocked_app(self, app_name):
        """Add app to block list"""
        if app_name not in self.config["blocked_apps"]:
            self.config["blocked_apps"].append(app_name)
            self.save_config()
            return {"success": True, "message": f"Added {app_name} to block list"}
        return {"success": False, "message": "App already in block list"}
    
    def remove_blocked_app(self, app_name):
        """Remove app from block list"""
        if app_name in self.config["blocked_apps"]:
            self.config["blocked_apps"].remove(app_name)
            self.save_config()
            return {"success": True, "message": f"Removed {app_name} from block list"}
        return {"success": False, "message": "App not in block list"}
    
    def add_blocked_website(self, website):
        """Add website to block list"""
        if website not in self.config["blocked_websites"]:
            self.config["blocked_websites"].append(website)
            self.save_config()
            
            # On Windows, modify hosts file (requires admin)
            if platform.system() == "Windows":
                self._update_hosts_file()
            
            return {"success": True, "message": f"Added {website} to block list"}
        return {"success": False, "message": "Website already blocked"}
    
    def _update_hosts_file(self):
        """Update Windows hosts file to block websites (requires admin)"""
        # Note: This requires administrator privileges
        try:
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            
            # Read current hosts file
            with open(hosts_path, 'r') as f:
                lines = f.readlines()
            
            # Add blocked websites
            for website in self.config["blocked_websites"]:
                entry = f"127.0.0.1 {website}\n"
                if entry not in lines:
                    lines.append(entry)
            
            # Write back (requires admin)
            with open(hosts_path, 'w') as f:
                f.writelines(lines)
            
            return {"success": True}
        except PermissionError:
            return {"success": False, "error": "Requires administrator privileges"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self):
        """Get focus mode status"""
        if not self.is_active:
            return {
                "is_active": False,
                "message": "Focus mode not active"
            }
        
        remaining = (self.session_end - datetime.now()).total_seconds() / 60
        
        return {
            "is_active": True,
            "started_at": self.session_start.strftime("%H:%M"),
            "end_time": self.session_end.strftime("%H:%M"),
            "minutes_remaining": max(0, round(remaining, 1)),
            "apps_blocked": self.blocked_apps_count
        }


# Singleton instance
_focus_mode = None

def get_focus_mode():
    """Get or create focus mode instance"""
    global _focus_mode
    if _focus_mode is None:
        _focus_mode = FocusModeAutomation()
    return _focus_mode
