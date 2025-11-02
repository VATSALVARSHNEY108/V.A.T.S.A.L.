"""
Workflow Templates Module
Save and reuse common workflows
"""

import json
import os
from typing import List, Dict
from datetime import datetime

class WorkflowManager:
    """Manages workflow templates"""
    
    def __init__(self, templates_file: str = "workflow_templates.json"):
        self.templates_file = templates_file
        self.templates: Dict[str, Dict] = {}
        self.load_templates()
    
    def save_workflow(self, name: str, steps: List[Dict], description: str = "") -> bool:
        """Save a workflow template"""
        try:
            self.templates[name] = {
                "name": name,
                "description": description,
                "steps": steps,
                "created": datetime.now().isoformat(),
                "usage_count": 0
            }
            self.save_templates()
            return True
        except Exception:
            return False
    
    def load_workflow(self, name: str) -> Dict:
        """Load a workflow template"""
        workflow = self.templates.get(name)
        if workflow:
            workflow["usage_count"] += 1
            self.save_templates()
        return workflow
    
    def list_workflows(self) -> List[Dict]:
        """List all workflow templates"""
        return [
            {
                "name": w["name"],
                "description": w["description"],
                "steps_count": len(w["steps"]),
                "usage_count": w["usage_count"]
            }
            for w in self.templates.values()
        ]
    
    def delete_workflow(self, name: str) -> bool:
        """Delete a workflow template"""
        if name in self.templates:
            del self.templates[name]
            self.save_templates()
            return True
        return False
    
    def get_popular_workflows(self, limit: int = 5) -> List[Dict]:
        """Get most used workflows"""
        workflows = list(self.templates.values())
        workflows.sort(key=lambda x: x["usage_count"], reverse=True)
        return workflows[:limit]
    
    def save_templates(self):
        """Save templates to file"""
        try:
            with open(self.templates_file, "w") as f:
                json.dump(self.templates, f, indent=2)
        except Exception:
            pass
    
    def load_templates(self):
        """Load templates from file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, "r") as f:
                    self.templates = json.load(f)
        except Exception:
            pass
    
    def create_default_templates(self):
        """Create some default useful templates"""
        defaults = [
            {
                "name": "morning_routine",
                "description": "Open common apps for morning work",
                "steps": [
                    {"action": "open_app", "parameters": {"app_name": "chrome"}},
                    {"action": "wait", "parameters": {"seconds": 2}},
                    {"action": "open_app", "parameters": {"app_name": "notepad"}}
                ]
            },
            {
                "name": "take_notes",
                "description": "Open notepad and create dated note file",
                "steps": [
                    {"action": "open_app", "parameters": {"app_name": "notepad"}},
                    {"action": "wait", "parameters": {"seconds": 1}},
                    {"action": "type_text", "parameters": {"text": f"Notes - {datetime.now().strftime('%Y-%m-%d')}\n\n"}}
                ]
            }
        ]
        
        for template in defaults:
            if template["name"] not in self.templates:
                self.save_workflow(
                    template["name"],
                    template["steps"],
                    template["description"]
                )
