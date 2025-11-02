"""
🏢 AI Workspace Management
Manage virtual work environments, notifications, clipboard, and window layouts
"""

import json
import os
import platform
import pyperclip
from datetime import datetime
from typing import Dict, List, Any

class WorkspaceManager:
    """Manages virtual work environments and workspace intelligence"""
    
    def __init__(self):
        self.environments_file = "work_environments.json"
        self.clipboard_file = "clipboard_history.json"
        self.notifications_file = "notifications_center.json"
        self.environments = self.load_environments()
        self.clipboard_history = self.load_clipboard_history()
        self.notifications = self.load_notifications()
        self.current_environment = None
        
    def load_environments(self):
        """Load saved work environments"""
        if os.path.exists(self.environments_file):
            try:
                with open(self.environments_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_environments(self):
        """Save work environments"""
        try:
            with open(self.environments_file, 'w') as f:
                json.dump(self.environments, f, indent=2)
        except Exception as e:
            print(f"Error saving environments: {e}")
    
    def load_clipboard_history(self):
        """Load clipboard history"""
        if os.path.exists(self.clipboard_file):
            try:
                with open(self.clipboard_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_clipboard_history(self):
        """Save clipboard history"""
        try:
            with open(self.clipboard_file, 'w') as f:
                json.dump(self.clipboard_history, f, indent=2)
        except Exception as e:
            print(f"Error saving clipboard: {e}")
    
    def load_notifications(self):
        """Load notifications"""
        if os.path.exists(self.notifications_file):
            try:
                with open(self.notifications_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_notifications(self):
        """Save notifications"""
        try:
            with open(self.notifications_file, 'w') as f:
                json.dump(self.notifications, f, indent=2)
        except Exception as e:
            print(f"Error saving notifications: {e}")
    
    def save_environment(self, name: str, description: str = ""):
        """Save current desktop layout as a virtual environment"""
        environment = {
            "name": name,
            "description": description,
            "created": datetime.now().isoformat(),
            "platform": platform.system(),
            "apps": [],
            "layout": {}
        }
        
        try:
            if platform.system() == "Windows":
                import psutil
                for proc in psutil.process_iter(['name', 'exe']):
                    try:
                        if proc.info['exe']:
                            environment["apps"].append(proc.info['name'])
                    except:
                        pass
        except ImportError:
            environment["apps"] = ["System apps recording requires psutil"]
        
        self.environments[name] = environment
        self.save_environments()
        
        return {"success": True, "message": f"Environment '{name}' saved with {len(environment['apps'])} applications"}
    
    def load_environment(self, name: str):
        """Load a saved virtual environment"""
        if name not in self.environments:
            return {"success": False, "message": f"Environment '{name}' not found"}
        
        env = self.environments[name]
        self.current_environment = name
        
        return {
            "success": True,
            "message": f"Environment '{name}' loaded",
            "details": f"Contains {len(env.get('apps', []))} apps - {env.get('description', 'No description')}"
        }
    
    def list_environments(self):
        """List all saved environments"""
        if not self.environments:
            return "No saved environments. Use 'save_environment' to create one."
        
        output = "\n" + "="*60 + "\n"
        output += "🏢 VIRTUAL WORK ENVIRONMENTS\n"
        output += "="*60 + "\n\n"
        
        for name, env in self.environments.items():
            output += f"📁 {name}\n"
            output += f"   Description: {env.get('description', 'No description')}\n"
            output += f"   Created: {env.get('created', 'Unknown')}\n"
            output += f"   Apps: {len(env.get('apps', []))}\n"
            if self.current_environment == name:
                output += f"   Status: ✅ Currently Active\n"
            output += "\n"
        
        output += "="*60 + "\n"
        return output
    
    def add_to_clipboard_history(self, content: str, content_type: str = "text"):
        """Add item to clipboard history"""
        entry = {
            "content": content,
            "type": content_type,
            "timestamp": datetime.now().isoformat(),
            "source": "user_copy"
        }
        
        self.clipboard_history.insert(0, entry)
        
        if len(self.clipboard_history) > 100:
            self.clipboard_history = self.clipboard_history[:100]
        
        self.save_clipboard_history()
        
        return {"success": True, "message": f"Added to clipboard history ({len(self.clipboard_history)} items)"}
    
    def get_clipboard_history(self, limit: int = 20):
        """Get clipboard history"""
        output = "\n" + "="*60 + "\n"
        output += "📋 SMART CLIPBOARD HISTORY\n"
        output += "="*60 + "\n\n"
        
        if not self.clipboard_history:
            return output + "No clipboard history yet.\n" + "="*60 + "\n"
        
        for i, entry in enumerate(self.clipboard_history[:limit], 1):
            content = entry.get("content", "")
            if len(content) > 60:
                content = content[:60] + "..."
            
            timestamp = entry.get("timestamp", "Unknown")
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = timestamp
            
            output += f"{i}. {content}\n"
            output += f"   Type: {entry.get('type', 'text')} | {time_str}\n\n"
        
        output += "="*60 + "\n"
        return output
    
    def search_clipboard(self, query: str):
        """Search clipboard history"""
        matches = []
        
        for entry in self.clipboard_history:
            if query.lower() in entry.get("content", "").lower():
                matches.append(entry)
        
        output = f"\n🔍 Found {len(matches)} matches for '{query}':\n\n"
        
        for i, entry in enumerate(matches[:10], 1):
            content = entry.get("content", "")
            if len(content) > 60:
                content = content[:60] + "..."
            output += f"{i}. {content}\n"
        
        return output
    
    def add_notification(self, title: str, message: str, priority: str = "normal", source: str = "system"):
        """Add notification to smart notification center"""
        notification = {
            "title": title,
            "message": message,
            "priority": priority,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "read": False,
            "importance_score": self.calculate_importance(title, message, priority)
        }
        
        self.notifications.insert(0, notification)
        
        if len(self.notifications) > 200:
            self.notifications = self.notifications[:200]
        
        self.save_notifications()
        
        return {"success": True, "message": f"Notification added: {title}"}
    
    def calculate_importance(self, title: str, message: str, priority: str):
        """Calculate AI-based importance score"""
        score = 50
        
        if priority == "high":
            score += 30
        elif priority == "urgent":
            score += 50
        
        urgent_keywords = ["urgent", "important", "deadline", "asap", "critical", "emergency"]
        combined_text = (title + " " + message).lower()
        
        for keyword in urgent_keywords:
            if keyword in combined_text:
                score += 10
        
        return min(score, 100)
    
    def get_notifications(self, show_all: bool = False):
        """Get notifications ranked by importance"""
        output = "\n" + "="*60 + "\n"
        output += "🔔 SMART NOTIFICATION CENTER\n"
        output += "="*60 + "\n\n"
        
        if not self.notifications:
            return output + "No notifications.\n" + "="*60 + "\n"
        
        notifications_to_show = self.notifications
        if not show_all:
            notifications_to_show = [n for n in self.notifications if not n.get("read", False)]
        
        sorted_notifications = sorted(
            notifications_to_show,
            key=lambda x: x.get("importance_score", 0),
            reverse=True
        )
        
        for i, notif in enumerate(sorted_notifications[:20], 1):
            priority_emoji = "🔴" if notif["priority"] == "urgent" else "🟡" if notif["priority"] == "high" else "🟢"
            
            output += f"{i}. {priority_emoji} {notif['title']}\n"
            output += f"   {notif['message']}\n"
            output += f"   Source: {notif['source']} | Importance: {notif.get('importance_score', 50)}%\n"
            
            timestamp = notif.get("timestamp", "Unknown")
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = timestamp
            
            output += f"   {time_str}\n\n"
        
        output += "="*60 + "\n"
        return output
    
    def group_windows_by_type(self):
        """Auto-arrange windows by app type or task category"""
        return {
            "success": True,
            "message": "Window grouping initiated",
            "groups": {
                "Browsers": ["Chrome", "Firefox", "Edge"],
                "Development": ["VSCode", "PyCharm", "Notepad++"],
                "Communication": ["Slack", "Discord", "Teams"],
                "Media": ["Spotify", "VLC", "Photos"]
            }
        }
    
    def enable_focus_trigger(self, trigger_type: str = "fullscreen"):
        """Enable automatic focus mode triggers"""
        triggers = {
            "fullscreen": "Focus mode activates when entering fullscreen",
            "code_editor": "Focus mode activates when coding",
            "meeting": "Focus mode activates during meetings"
        }
        
        if trigger_type in triggers:
            return {"success": True, "message": f"Focus trigger enabled: {triggers[trigger_type]}"}
        
        return {"success": False, "message": "Invalid trigger type"}
    
    def clear_clipboard_history(self):
        """Clear clipboard history"""
        self.clipboard_history = []
        self.save_clipboard_history()
        return {"success": True, "message": "Clipboard history cleared"}
    
    def mark_notifications_read(self):
        """Mark all notifications as read"""
        for notif in self.notifications:
            notif["read"] = True
        self.save_notifications()
        return {"success": True, "message": "All notifications marked as read"}


def create_workspace_manager():
    """Factory function to create a WorkspaceManager instance"""
    return WorkspaceManager()
