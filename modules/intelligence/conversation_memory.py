"""
Conversation Memory Module
Tracks conversation history and provides context awareness
"""

import json
import os
from datetime import datetime
from typing import List, Dict

class ConversationMemory:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.history: List[Dict] = []
        self.context: Dict = {}
        self.load_history()
    
    def add_command(self, user_input: str, result: Dict, command_dict: Dict = None):
        """Add a command to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "command": command_dict,
            "result": {
                "success": result.get("success"),
                "message": result.get("message", "")[:200]
            }
        }
        
        self.history.append(entry)
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        self.update_context(entry)
        self.save_history()
    
    def update_context(self, entry: Dict):
        """Update context based on recent activity"""
        if entry["result"]["success"]:
            last_action = entry.get("command", {}).get("action", "")
            self.context["last_successful_action"] = last_action
            self.context["last_command"] = entry["user_input"]
            
            if "generated_code" in entry["result"]:
                self.context["last_generated_code"] = entry["result"]["generated_code"][:500]
    
    def get_recent_history(self, count: int = 10) -> List[Dict]:
        """Get recent command history"""
        return self.history[-count:] if self.history else []
    
    def get_context_summary(self) -> str:
        """Get a summary of current context"""
        if not self.history:
            return "No previous commands"
        
        recent = self.get_recent_history(5)
        summary = f"Recent commands ({len(recent)}):\n"
        
        for entry in recent:
            status = "✅" if entry["result"]["success"] else "❌"
            summary += f"  {status} {entry['user_input'][:50]}\n"
        
        return summary
    
    def search_history(self, query: str) -> List[Dict]:
        """Search command history"""
        query_lower = query.lower()
        results = []
        
        for entry in self.history:
            if query_lower in entry["user_input"].lower():
                results.append(entry)
        
        return results
    
    def get_last_code(self) -> str:
        """Get the last generated code"""
        return self.context.get("last_generated_code", "")
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.context = {}
        self.save_history()
    
    def save_history(self):
        """Save history to file"""
        try:
            with open("conversation_history.json", "w") as f:
                json.dump({
                    "history": self.history,
                    "context": self.context
                }, f, indent=2)
        except Exception:
            pass
    
    def load_history(self):
        """Load history from file"""
        try:
            if os.path.exists("conversation_history.json"):
                with open("conversation_history.json", "r") as f:
                    data = json.load(f)
                    self.history = data.get("history", [])[-self.max_history:]
                    self.context = data.get("context", {})
        except Exception:
            pass
    
    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        total_commands = len(self.history)
        successful = sum(1 for e in self.history if e["result"]["success"])
        failed = total_commands - successful
        
        return {
            "total_commands": total_commands,
            "successful": successful,
            "failed": failed,
            "success_rate": f"{(successful/total_commands*100):.1f}%" if total_commands > 0 else "0%"
        }
