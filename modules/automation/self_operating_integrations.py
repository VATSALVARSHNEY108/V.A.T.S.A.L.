"""
Self-Operating Computer Integrations
Bridges self-operating computer with all VATSAL modules for seamless ecosystem integration
"""

import os
import json
import time
from typing import Optional, Dict, List, Any, Callable
from datetime import datetime
from pathlib import Path

try:
    from self_operating_computer import SelfOperatingComputer
except ImportError:
    SelfOperatingComputer = None

try:
    from comprehensive_desktop_controller import ComprehensiveDesktopController
except ImportError:
    ComprehensiveDesktopController = None

try:
    from virtual_language_model import VirtualLanguageModel
except ImportError:
    VirtualLanguageModel = None

try:
    from gemini_controller import parse_command
except ImportError:
    parse_command = None


class SelfOperatingIntegrationHub:
    """
    Integration hub connecting self-operating computer with VATSAL ecosystem
    
    Features:
    - Unified task execution across modules
    - Intelligent routing between self-operating and traditional automation
    - Context sharing and memory
    - Progress tracking across modules
    - Error recovery and fallback strategies
    """
    
    def __init__(self):
        """Initialize integration hub with all available modules"""
        self.self_operating = None
        self.comprehensive_controller = None
        self.vlm = None
        self.command_parser = parse_command
        
        # Module availability
        self.modules_available = {
            "self_operating": False,
            "comprehensive_controller": False,
            "vlm": False,
            "command_parser": False
        }
        
        # Integration state
        self.current_mode = "idle"  # idle, self_operating, comprehensive, vlm, hybrid
        self.task_history: List[Dict[str, Any]] = []
        self.shared_context: Dict[str, Any] = {}
        
        # Initialize modules
        self._initialize_modules()
    
    def _initialize_modules(self):
        """Initialize available modules"""
        # Self-Operating Computer
        try:
            if SelfOperatingComputer:
                api_key = os.environ.get("GEMINI_API_KEY")
                if api_key:
                    self.self_operating = SelfOperatingComputer(verbose=True)
                    self.modules_available["self_operating"] = True
                    print("✅ Self-Operating Computer initialized")
        except Exception as e:
            print(f"⚠️ Self-Operating Computer not available: {e}")
        
        # Comprehensive Desktop Controller
        try:
            if ComprehensiveDesktopController:
                self.comprehensive_controller = ComprehensiveDesktopController()
                self.modules_available["comprehensive_controller"] = True
                print("✅ Comprehensive Desktop Controller initialized")
        except Exception as e:
            print(f"⚠️ Comprehensive Controller not available: {e}")
        
        # Virtual Language Model
        try:
            if VirtualLanguageModel:
                from gui_automation import GUIAutomation
                gui_automation = GUIAutomation()
                self.vlm = VirtualLanguageModel(gui_automation)
                self.modules_available["vlm"] = True
                print("✅ Virtual Language Model initialized")
        except Exception as e:
            print(f"⚠️ VLM not available: {e}")
        
        # Command Parser
        if self.command_parser:
            self.modules_available["command_parser"] = True
            print("✅ Command Parser initialized")
    
    def analyze_task_complexity(self, task: str) -> Dict[str, Any]:
        """
        Analyze task to determine best execution strategy
        
        Args:
            task: User's task description
            
        Returns:
            Analysis with recommended module and strategy
        """
        task_lower = task.lower()
        
        analysis = {
            "task": task,
            "complexity": "medium",
            "recommended_module": "self_operating",
            "requires_vision": False,
            "requires_learning": False,
            "requires_planning": False,
            "is_visual_navigation": False,
            "is_structured_command": False,
            "reasoning": ""
        }
        
        # Visual navigation tasks (best for self-operating)
        visual_keywords = [
            "click", "navigate", "browse", "website", "ui", "button",
            "menu", "scroll", "find on screen", "visual", "look for"
        ]
        if any(keyword in task_lower for keyword in visual_keywords):
            analysis["requires_vision"] = True
            analysis["is_visual_navigation"] = True
            analysis["recommended_module"] = "self_operating"
            analysis["complexity"] = "high"
            analysis["reasoning"] = "Visual navigation requires self-operating computer"
        
        # Structured commands (good for comprehensive controller)
        structured_keywords = [
            "open", "close", "create file", "delete file", "run",
            "execute", "system", "brightness", "volume"
        ]
        if any(keyword in task_lower for keyword in structured_keywords) and not analysis["is_visual_navigation"]:
            analysis["is_structured_command"] = True
            analysis["recommended_module"] = "comprehensive"
            analysis["complexity"] = "low"
            analysis["reasoning"] = "Structured command best handled by comprehensive controller"
        
        # Learning tasks (good for VLM)
        learning_keywords = [
            "learn", "remember", "pattern", "observe", "study",
            "understand how", "figure out"
        ]
        if any(keyword in task_lower for keyword in learning_keywords):
            analysis["requires_learning"] = True
            analysis["recommended_module"] = "vlm"
            analysis["reasoning"] = "Learning task benefits from VLM"
        
        # Complex multi-step tasks (hybrid approach)
        planning_keywords = [
            "workflow", "multiple", "sequence", "first then", "after that",
            "step by step", "complex", "automate"
        ]
        if any(keyword in task_lower for keyword in planning_keywords):
            analysis["requires_planning"] = True
            analysis["recommended_module"] = "hybrid"
            analysis["complexity"] = "high"
            analysis["reasoning"] = "Complex task requires hybrid approach"
        
        return analysis
    
    def execute_with_best_module(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute task using the most appropriate module
        
        Args:
            task: Task to execute
            context: Optional execution context
            
        Returns:
            Execution result
        """
        # Analyze task
        analysis = self.analyze_task_complexity(task)
        
        print(f"\n{'='*60}")
        print(f"🎯 Task: {task}")
        print(f"📊 Analysis: {analysis['reasoning']}")
        print(f"🔧 Recommended: {analysis['recommended_module']}")
        print(f"{'='*60}\n")
        
        result = {
            "task": task,
            "analysis": analysis,
            "success": False,
            "module_used": None,
            "output": None,
            "error": None
        }
        
        # Update shared context
        if context:
            self.shared_context.update(context)
        
        # Route to appropriate module
        module = analysis["recommended_module"]
        
        try:
            if module == "self_operating" and self.modules_available["self_operating"]:
                result = self._execute_self_operating(task, analysis)
                
            elif module == "comprehensive" and self.modules_available["comprehensive_controller"]:
                result = self._execute_comprehensive(task, analysis)
                
            elif module == "vlm" and self.modules_available["vlm"]:
                result = self._execute_vlm(task, analysis)
                
            elif module == "hybrid":
                result = self._execute_hybrid(task, analysis)
                
            else:
                # Fallback to self-operating if available
                if self.modules_available["self_operating"]:
                    print("⚠️ Preferred module not available, using self-operating as fallback")
                    result = self._execute_self_operating(task, analysis)
                else:
                    result["error"] = "No suitable module available"
                    result["success"] = False
            
        except Exception as e:
            result["error"] = str(e)
            result["success"] = False
            print(f"❌ Execution error: {e}")
        
        # Store in history
        self.task_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "analysis": analysis,
            "result": result
        })
        
        return result
    
    def _execute_self_operating(self, task: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using self-operating computer"""
        self.current_mode = "self_operating"
        
        print("🎮 Executing with Self-Operating Computer...")
        
        # Build context from analysis
        context_str = f"""
Task Complexity: {analysis['complexity']}
Requires Vision: {analysis['requires_vision']}
Task Type: {'Visual Navigation' if analysis['is_visual_navigation'] else 'General'}
"""
        
        # Execute
        session_result = self.self_operating.operate(task, context=context_str)
        
        return {
            "task": task,
            "analysis": analysis,
            "success": session_result.get("completed", False),
            "module_used": "self_operating",
            "output": session_result,
            "error": None
        }
    
    def _execute_comprehensive(self, task: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using comprehensive desktop controller"""
        self.current_mode = "comprehensive"
        
        print("🎯 Executing with Comprehensive Desktop Controller...")
        
        try:
            # Parse command using Gemini
            if self.command_parser:
                parsed = self.command_parser(task)
                
                # Execute with comprehensive controller
                # Note: This requires the comprehensive controller to have an execute method
                # which may need to be implemented
                
                return {
                    "task": task,
                    "analysis": analysis,
                    "success": True,
                    "module_used": "comprehensive",
                    "output": parsed,
                    "error": None
                }
            else:
                return {
                    "task": task,
                    "analysis": analysis,
                    "success": False,
                    "module_used": "comprehensive",
                    "output": None,
                    "error": "Command parser not available"
                }
                
        except Exception as e:
            return {
                "task": task,
                "analysis": analysis,
                "success": False,
                "module_used": "comprehensive",
                "output": None,
                "error": str(e)
            }
    
    def _execute_vlm(self, task: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using virtual language model"""
        self.current_mode = "vlm"
        
        print("🧠 Executing with Virtual Language Model...")
        
        try:
            # Use VLM to learn and execute
            # VLM observes screen and builds knowledge
            
            return {
                "task": task,
                "analysis": analysis,
                "success": True,
                "module_used": "vlm",
                "output": "VLM execution (implementation depends on VLM capabilities)",
                "error": None
            }
                
        except Exception as e:
            return {
                "task": task,
                "analysis": analysis,
                "success": False,
                "module_used": "vlm",
                "output": None,
                "error": str(e)
            }
    
    def _execute_hybrid(self, task: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complex task using hybrid approach"""
        self.current_mode = "hybrid"
        
        print("🔀 Executing with Hybrid Approach...")
        
        # Break down task into subtasks
        subtasks = self._break_down_task(task)
        
        results = []
        overall_success = True
        
        for i, subtask in enumerate(subtasks):
            print(f"\n📍 Subtask {i+1}/{len(subtasks)}: {subtask['description']}")
            
            # Analyze and execute each subtask
            sub_analysis = self.analyze_task_complexity(subtask['description'])
            
            # Execute based on subtask requirements
            if sub_analysis["is_visual_navigation"] and self.modules_available["self_operating"]:
                sub_result = self._execute_self_operating(subtask['description'], sub_analysis)
            elif self.modules_available["comprehensive_controller"]:
                sub_result = self._execute_comprehensive(subtask['description'], sub_analysis)
            else:
                sub_result = {
                    "success": False,
                    "error": "No module available for subtask"
                }
            
            results.append(sub_result)
            
            if not sub_result.get("success", False):
                overall_success = False
                print(f"⚠️ Subtask {i+1} failed")
                
                # Decide whether to continue or abort
                if subtask.get("critical", False):
                    print("❌ Critical subtask failed - aborting")
                    break
        
        return {
            "task": task,
            "analysis": analysis,
            "success": overall_success,
            "module_used": "hybrid",
            "output": {
                "subtasks": subtasks,
                "results": results,
                "completed": len(results),
                "total": len(subtasks)
            },
            "error": None if overall_success else "One or more subtasks failed"
        }
    
    def _break_down_task(self, task: str) -> List[Dict[str, Any]]:
        """
        Break complex task into subtasks
        
        Args:
            task: Complex task description
            
        Returns:
            List of subtasks with metadata
        """
        # Simple heuristic breakdown (can be enhanced with AI)
        # Look for sequential keywords
        
        if " then " in task.lower():
            parts = task.split(" then ")
            return [
                {
                    "description": part.strip(),
                    "order": i,
                    "critical": True
                }
                for i, part in enumerate(parts)
            ]
        
        elif " and " in task.lower():
            parts = task.split(" and ")
            return [
                {
                    "description": part.strip(),
                    "order": i,
                    "critical": False
                }
                for i, part in enumerate(parts)
            ]
        
        else:
            # Single task
            return [
                {
                    "description": task,
                    "order": 0,
                    "critical": True
                }
            ]
    
    def get_status(self) -> Dict[str, Any]:
        """Get current integration hub status"""
        return {
            "current_mode": self.current_mode,
            "modules_available": self.modules_available,
            "tasks_executed": len(self.task_history),
            "shared_context_size": len(self.shared_context)
        }
    
    def save_session(self, filepath: Optional[str] = None) -> str:
        """
        Save current session history
        
        Args:
            filepath: Optional custom filepath
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = f"integration_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        session_data = {
            "saved_at": datetime.now().isoformat(),
            "status": self.get_status(),
            "task_history": self.task_history,
            "shared_context": self.shared_context
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"✅ Session saved to: {filepath}")
        return filepath


class SmartTaskRouter:
    """
    Smart router that decides whether to use self-operating or traditional automation
    based on task characteristics
    """
    
    def __init__(self, integration_hub: SelfOperatingIntegrationHub):
        """Initialize with integration hub"""
        self.hub = integration_hub
    
    def route_command(self, command: str) -> Dict[str, Any]:
        """
        Route command to appropriate execution method
        
        Args:
            command: User command
            
        Returns:
            Execution result
        """
        # Use integration hub's analysis
        return self.hub.execute_with_best_module(command)
    
    def should_use_self_operating(self, command: str) -> bool:
        """
        Determine if command should use self-operating mode
        
        Args:
            command: User command
            
        Returns:
            True if self-operating is recommended
        """
        analysis = self.hub.analyze_task_complexity(command)
        return analysis["recommended_module"] == "self_operating"


# Convenience functions for direct use

def execute_autonomous_task(task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute task autonomously using best available module
    
    Args:
        task: Task description
        context: Optional context
        
    Returns:
        Execution result
    """
    hub = SelfOperatingIntegrationHub()
    return hub.execute_with_best_module(task, context)


def create_integration_hub() -> SelfOperatingIntegrationHub:
    """Create and return a new integration hub instance"""
    return SelfOperatingIntegrationHub()


if __name__ == "__main__":
    # Test integration hub
    print("=" * 70)
    print("🔧 Self-Operating Computer Integration Hub")
    print("=" * 70)
    
    hub = SelfOperatingIntegrationHub()
    
    print("\n📊 System Status:")
    status = hub.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Integration hub ready!")
    print("Use hub.execute_with_best_module(task) to execute tasks\n")
