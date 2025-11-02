"""
Natural Language Workflow Builder 💬
AI-powered workflow creation from plain English descriptions
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Callable
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    types = None

from workflow_templates import WorkflowManager


class NaturalLanguageWorkflowBuilder:
    """
    Build complex workflows using plain English descriptions
    Features:
    - AI converts natural language to executable automation steps
    - Test and refine workflows through conversation
    - Save as reusable templates
    - Suggest improvements and optimizations
    """
    
    def __init__(self, workflow_manager: Optional[WorkflowManager] = None, log_callback: Optional[Callable] = None):
        """
        Initialize the Natural Language Workflow Builder
        
        Args:
            workflow_manager: Optional WorkflowManager instance
            log_callback: Optional callback for logging messages
        """
        self.workflow_manager = workflow_manager or WorkflowManager()
        self.log_callback = log_callback
        
        if GEMINI_AVAILABLE:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                try:
                    self.client = genai.Client(api_key=api_key)
                    self.model = "gemini-2.0-flash-exp"
                    self.ai_available = True
                except Exception:
                    self.ai_available = False
            else:
                self.ai_available = False
        else:
            self.ai_available = False
        
        self.conversation_history_file = "workflow_builder_history.json"
        self.conversation_history = self.load_conversation_history()
        self.current_draft = None
        self.initialize_system_prompt()
    
    def initialize_system_prompt(self):
        """Initialize the AI system prompt for workflow generation"""
        self.system_prompt = """You are an intelligent Workflow Builder AI assistant. You help users create automation workflows from natural language descriptions.

Your capabilities:
1. Convert plain English descriptions into structured workflow steps
2. Ask clarifying questions when needed
3. Suggest improvements and optimizations
4. Break down complex tasks into executable steps
5. Provide helpful examples and templates

Available actions for workflows:
DESKTOP AUTOMATION:
- open_app: Open an application (parameters: app_name)
- type_text: Type text (parameters: text)
- click: Click at position (parameters: x, y) or button (left/right/middle)
- move_mouse: Move mouse (parameters: x, y)
- press_key: Press keyboard key (parameters: key)
- hotkey: Press key combination (parameters: keys - array)
- screenshot: Take screenshot (parameters: filename)
- wait: Wait for seconds (parameters: seconds)

FILE OPERATIONS:
- create_file: Create a file (parameters: path, content)
- create_folder: Create a folder (parameters: path)
- delete_file: Delete a file (parameters: path)
- rename_file: Rename a file (parameters: old_path, new_path)
- copy_file: Copy a file (parameters: source, destination)

WEB OPERATIONS:
- open_website: Open a website (parameters: url)
- google_search: Search Google (parameters: query)
- youtube_search: Search YouTube (parameters: query)

COMMUNICATION:
- send_email: Send email (parameters: to, subject, body)
- send_whatsapp: Send WhatsApp message (parameters: contact, message)

SYSTEM:
- get_system_info: Get system information
- get_battery_status: Check battery status
- lock_screen: Lock the computer
- take_screenshot: Take a screenshot (parameters: filename)

Response format:
When the user describes a workflow, respond with a JSON object containing:
{
    "workflow_name": "descriptive_name",
    "description": "what this workflow does",
    "steps": [
        {"action": "action_name", "parameters": {...}},
        ...
    ],
    "suggestions": "optional improvement suggestions",
    "questions": "any clarifying questions if needed"
}

If you need clarification, ask questions naturally. If the description is clear, generate the workflow immediately.

Be conversational, helpful, and proactive in suggesting improvements."""
    
    def _log(self, message: str, level: str = "INFO"):
        """Log a message"""
        if self.log_callback:
            self.log_callback(message, level)
        else:
            print(f"[{level}] {message}")
    
    def load_conversation_history(self) -> List[Dict]:
        """Load conversation history from file"""
        if os.path.exists(self.conversation_history_file):
            try:
                with open(self.conversation_history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_conversation_history(self):
        """Save conversation history to file"""
        try:
            with open(self.conversation_history_file, 'w') as f:
                json.dump(self.conversation_history[-50:], f, indent=2)
        except Exception as e:
            self._log(f"Failed to save conversation history: {e}", "ERROR")
    
    def add_to_conversation(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.save_conversation_history()
    
    def describe_workflow(self, description: str) -> Dict:
        """
        Convert a natural language description into a workflow
        
        Args:
            description: Plain English description of the workflow
            
        Returns:
            Dict containing workflow details or conversation response
        """
        if not self.ai_available:
            return {
                "success": False,
                "error": "AI is not available. Please set GEMINI_API_KEY."
            }
        
        try:
            self._log(f"Processing workflow description: {description}", "INFO")
            self.add_to_conversation("user", description)
            
            messages = [
                {
                    "role": "user",
                    "parts": [{"text": self.system_prompt}]
                }
            ]
            
            for msg in self.conversation_history[-10:]:
                messages.append({
                    "role": "model" if msg["role"] == "assistant" else "user",
                    "parts": [{"text": msg["content"]}]
                })
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=2048
                )
            )
            
            response_text = response.text.strip()
            self.add_to_conversation("assistant", response_text)
            
            if response_text.startswith("{") or "```json" in response_text:
                json_text = response_text
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0].strip()
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0].strip()
                
                try:
                    workflow_data = json.loads(json_text)
                    if "steps" in workflow_data and len(workflow_data["steps"]) > 0:
                        self.current_draft = workflow_data
                        return {
                            "success": True,
                            "type": "workflow",
                            "workflow": workflow_data,
                            "message": "Workflow generated successfully! Review and test it."
                        }
                except json.JSONDecodeError:
                    pass
            
            return {
                "success": True,
                "type": "conversation",
                "message": response_text
            }
            
        except Exception as e:
            self._log(f"Error describing workflow: {e}", "ERROR")
            return {
                "success": False,
                "error": str(e)
            }
    
    def refine_workflow(self, feedback: str) -> Dict:
        """
        Refine the current workflow draft based on user feedback
        
        Args:
            feedback: User feedback for refinement
            
        Returns:
            Dict containing refined workflow or conversation response
        """
        if not self.current_draft:
            return self.describe_workflow(feedback)
        
        refinement_prompt = f"""Current workflow draft:
{json.dumps(self.current_draft, indent=2)}

User feedback: {feedback}

Please refine the workflow based on this feedback and return the updated JSON."""
        
        return self.describe_workflow(refinement_prompt)
    
    def validate_workflow(self, workflow: Dict) -> Dict:
        """
        Validate a workflow structure
        
        Args:
            workflow: Workflow dictionary to validate
            
        Returns:
            Dict with validation results
        """
        issues = []
        
        if "workflow_name" not in workflow or not workflow["workflow_name"]:
            issues.append("Workflow must have a name")
        
        if "steps" not in workflow or not isinstance(workflow["steps"], list):
            issues.append("Workflow must have a steps array")
        elif len(workflow["steps"]) == 0:
            issues.append("Workflow must have at least one step")
        else:
            for i, step in enumerate(workflow["steps"]):
                if not isinstance(step, dict):
                    issues.append(f"Step {i+1} must be a dictionary")
                elif "action" not in step:
                    issues.append(f"Step {i+1} must have an action")
                elif "parameters" not in step:
                    issues.append(f"Step {i+1} must have parameters")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def save_workflow(self, workflow: Optional[Dict] = None, name: Optional[str] = None) -> Dict:
        """
        Save a workflow as a reusable template
        
        Args:
            workflow: Workflow to save (uses current_draft if None)
            name: Name for the workflow (overrides workflow_name if provided)
            
        Returns:
            Dict with save results
        """
        workflow_to_save = workflow or self.current_draft
        
        if not workflow_to_save:
            return {
                "success": False,
                "error": "No workflow to save"
            }
        
        validation = self.validate_workflow(workflow_to_save)
        if not validation["valid"]:
            return {
                "success": False,
                "error": "Workflow validation failed",
                "issues": validation["issues"]
            }
        
        workflow_name = name or workflow_to_save.get("workflow_name", "unnamed_workflow")
        description = workflow_to_save.get("description", "")
        steps = workflow_to_save["steps"]
        
        success = self.workflow_manager.save_workflow(workflow_name, steps, description)
        
        if success:
            self._log(f"Workflow '{workflow_name}' saved successfully!", "SUCCESS")
            self.current_draft = None
            return {
                "success": True,
                "message": f"Workflow '{workflow_name}' saved successfully!",
                "name": workflow_name
            }
        else:
            return {
                "success": False,
                "error": "Failed to save workflow"
            }
    
    def list_templates(self) -> List[Dict]:
        """List all saved workflow templates"""
        return self.workflow_manager.list_workflows()
    
    def load_template(self, name: str) -> Optional[Dict]:
        """Load a saved workflow template"""
        return self.workflow_manager.load_workflow(name)
    
    def delete_template(self, name: str) -> bool:
        """Delete a workflow template"""
        return self.workflow_manager.delete_workflow(name)
    
    def get_examples(self) -> List[Dict]:
        """Get example workflow descriptions"""
        return [
            {
                "name": "Morning Productivity Setup",
                "description": "Every morning, open Chrome with my email, open Spotify, and create a new daily notes file with today's date"
            },
            {
                "name": "Quick Research Workflow",
                "description": "Search Google for a topic, take a screenshot of the results, and save it to my Research folder with a timestamped filename"
            },
            {
                "name": "Daily Backup Routine",
                "description": "Create a backup folder with today's date, copy all files from Documents to the backup folder, and compress it into a ZIP file"
            },
            {
                "name": "Social Media Posting",
                "description": "Open Chrome, navigate to Twitter, wait 3 seconds for the page to load, then click the tweet button and type my prepared message"
            },
            {
                "name": "System Maintenance",
                "description": "Get system information, take a screenshot, save it as system_status.png, then organize my Downloads folder by file type"
            },
            {
                "name": "Meeting Preparation",
                "description": "Open Zoom app, open Chrome with Google Calendar, open Notepad and create a meeting notes template with timestamp"
            }
        ]
    
    def suggest_improvements(self, workflow: Dict) -> List[str]:
        """
        Suggest improvements for a workflow
        
        Args:
            workflow: Workflow to analyze
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        if len(workflow.get("steps", [])) > 10:
            suggestions.append("Consider breaking this into smaller workflows")
        
        has_wait = any(step.get("action") == "wait" for step in workflow.get("steps", []))
        if not has_wait and len(workflow.get("steps", [])) > 3:
            suggestions.append("Consider adding wait steps between actions for reliability")
        
        has_screenshot = any(step.get("action") == "screenshot" for step in workflow.get("steps", []))
        if not has_screenshot:
            suggestions.append("Consider adding screenshot steps for verification")
        
        step_count = len(workflow.get("steps", []))
        if step_count < 2:
            suggestions.append("Workflow seems too simple - consider adding more automation")
        
        return suggestions
    
    def clear_draft(self):
        """Clear the current workflow draft"""
        self.current_draft = None
        return {"success": True, "message": "Draft cleared"}
    
    def get_current_draft(self) -> Optional[Dict]:
        """Get the current workflow draft"""
        return self.current_draft
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.save_conversation_history()
        return {"success": True, "message": "Conversation history cleared"}


def create_nl_workflow_builder(workflow_manager: Optional[WorkflowManager] = None, log_callback: Optional[Callable] = None):
    """Factory function to create NaturalLanguageWorkflowBuilder instance"""
    return NaturalLanguageWorkflowBuilder(workflow_manager, log_callback)
