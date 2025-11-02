"""
Self-Operating Coordinator
Orchestrates complex multi-step tasks across all VATSAL modules
Provides intelligent task planning, execution, and monitoring
"""

import os
import json
import time
from typing import Optional, Dict, List, Any, Callable
from datetime import datetime
from pathlib import Path

try:
    from self_operating_integrations import SelfOperatingIntegrationHub
except ImportError:
    SelfOperatingIntegrationHub = None

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None


class TaskCoordinator:
    """
    Coordinates complex tasks across multiple VATSAL modules
    
    Features:
    - AI-powered task decomposition
    - Intelligent module selection
    - Parallel and sequential execution
    - Progress tracking
    - Error recovery and fallback
    - Learning from execution results
    """
    
    def __init__(self, integration_hub: Optional[Any] = None):
        """
        Initialize task coordinator
        
        Args:
            integration_hub: Optional integration hub instance
        """
        self.integration_hub = integration_hub
        if not self.integration_hub and SelfOperatingIntegrationHub:
            self.integration_hub = SelfOperatingIntegrationHub()
        
        # Gemini client for intelligent planning
        self.gemini_client = None
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key and genai:
            self.gemini_client = genai.Client(api_key=api_key)
        
        # Execution state
        self.current_plan: Optional[Dict[str, Any]] = None
        self.execution_history: List[Dict[str, Any]] = []
        self.active_tasks: List[Dict[str, Any]] = []
        
        print("🎯 Task Coordinator initialized")
    
    def plan_task(self, user_goal: str) -> Dict[str, Any]:
        """
        Create intelligent execution plan for user goal
        
        Args:
            user_goal: High-level user objective
            
        Returns:
            Execution plan with steps and module assignments
        """
        print(f"\n🧠 Planning task: {user_goal}")
        
        if not self.gemini_client:
            # Fallback to simple planning
            return self._simple_plan(user_goal)
        
        # AI-powered planning
        planning_prompt = f"""You are an intelligent task planning assistant for a desktop automation system.

User Goal: {user_goal}

Available Modules:
1. **self_operating** - AI vision-based computer control (screen analysis, mouse/keyboard)
   - Best for: Visual navigation, UI interaction, web browsing, clicking elements
   - Capabilities: See screen, click, type, scroll, navigate

2. **comprehensive** - Structured command execution (file ops, system control)
   - Best for: File management, system settings, app launching, structured tasks
   - Capabilities: File operations, system control, predefined actions

3. **vlm** - Virtual Language Model (learning and pattern recognition)
   - Best for: Learning workflows, pattern detection, knowledge building
   - Capabilities: Observe and learn, build knowledge, intelligent decisions

Your task: Break down the user goal into actionable steps and assign each step to the best module.

Output JSON format:
{{
    "goal": "{user_goal}",
    "complexity": "low|medium|high",
    "estimated_duration": "time estimate",
    "steps": [
        {{
            "step_number": 1,
            "description": "Clear description of what to do",
            "module": "self_operating|comprehensive|vlm",
            "parameters": {{}},
            "dependencies": [],
            "critical": true|false,
            "reasoning": "Why this module is best"
        }}
    ],
    "execution_strategy": "sequential|parallel|hybrid",
    "success_criteria": "How to know if goal is achieved"
}}

Guidelines:
- Be specific and actionable with each step
- Choose the most appropriate module for each step
- Mark critical steps that must succeed
- Consider dependencies between steps
- Provide clear success criteria

Output ONLY valid JSON."""

        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=planning_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=2048,
                )
            )
            
            response_text = response.text.strip() if response and response.text else ""
            
            # Clean JSON
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            plan = json.loads(response_text)
            
            print(f"✅ Plan created: {len(plan.get('steps', []))} steps")
            print(f"   Complexity: {plan.get('complexity', 'unknown')}")
            print(f"   Strategy: {plan.get('execution_strategy', 'sequential')}")
            
            self.current_plan = plan
            return plan
            
        except Exception as e:
            print(f"⚠️ AI planning failed: {e}, using fallback")
            return self._simple_plan(user_goal)
    
    def _simple_plan(self, user_goal: str) -> Dict[str, Any]:
        """Simple fallback planning without AI"""
        # Analyze keywords to determine module
        goal_lower = user_goal.lower()
        
        # Determine best module
        if any(keyword in goal_lower for keyword in ["click", "navigate", "browse", "website", "ui", "screen"]):
            module = "self_operating"
            complexity = "medium"
        elif any(keyword in goal_lower for keyword in ["file", "folder", "open", "close", "system"]):
            module = "comprehensive"
            complexity = "low"
        else:
            module = "self_operating"  # Default
            complexity = "low"
        
        plan = {
            "goal": user_goal,
            "complexity": complexity,
            "estimated_duration": "1-2 minutes",
            "steps": [
                {
                    "step_number": 1,
                    "description": user_goal,
                    "module": module,
                    "parameters": {},
                    "dependencies": [],
                    "critical": True,
                    "reasoning": "Single-step task"
                }
            ],
            "execution_strategy": "sequential",
            "success_criteria": "Task completed successfully"
        }
        
        self.current_plan = plan
        return plan
    
    def execute_plan(self, plan: Optional[Dict[str, Any]] = None, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Execute a task plan
        
        Args:
            plan: Execution plan (uses current_plan if None)
            progress_callback: Optional callback for progress updates
            
        Returns:
            Execution results
        """
        if plan is None:
            plan = self.current_plan
        
        if not plan:
            return {
                "success": False,
                "error": "No plan provided or created"
            }
        
        if not self.integration_hub:
            return {
                "success": False,
                "error": "Integration hub not available"
            }
        
        print(f"\n🚀 Executing plan: {plan.get('goal', 'Unknown')}")
        print(f"   Strategy: {plan.get('execution_strategy', 'sequential')}")
        print(f"   Steps: {len(plan.get('steps', []))}")
        print("=" * 60)
        
        start_time = time.time()
        steps = plan.get("steps", [])
        results = []
        overall_success = True
        
        strategy = plan.get("execution_strategy", "sequential")
        
        if strategy == "sequential":
            # Execute steps one by one
            for i, step in enumerate(steps):
                step_num = step.get("step_number", i + 1)
                description = step.get("description", "")
                module = step.get("module", "self_operating")
                critical = step.get("critical", False)
                
                print(f"\n📍 Step {step_num}/{len(steps)}: {description}")
                print(f"   Module: {module}")
                
                # Progress callback
                if progress_callback:
                    progress_callback(step_num, len(steps), description)
                
                # Execute step via integration hub
                step_result = self.integration_hub.execute_with_best_module(
                    description,
                    context={"step_number": step_num, "plan": plan}
                )
                
                results.append(step_result)
                
                # Check result
                if not step_result.get("success", False):
                    print(f"⚠️ Step {step_num} failed")
                    
                    if critical:
                        print(f"❌ Critical step failed - aborting execution")
                        overall_success = False
                        break
                    else:
                        print(f"⚠️ Non-critical step failed - continuing")
                        overall_success = False  # Mark as partial failure but continue
                else:
                    print(f"✅ Step {step_num} completed")
        
        elif strategy == "parallel":
            # Execute all steps in parallel (simplified - would need threading)
            print("⚠️ Parallel execution not yet implemented, using sequential")
            return self.execute_plan(plan, progress_callback)
        
        else:
            # Hybrid - mix of sequential and parallel
            print("⚠️ Hybrid execution not yet implemented, using sequential")
            return self.execute_plan(plan, progress_callback)
        
        # Calculate metrics
        duration = time.time() - start_time
        completed_steps = sum(1 for r in results if r.get("success", False))
        
        execution_result = {
            "success": overall_success,
            "goal": plan.get("goal", ""),
            "total_steps": len(steps),
            "completed_steps": completed_steps,
            "failed_steps": len(results) - completed_steps,
            "duration_seconds": round(duration, 2),
            "results": results,
            "plan": plan
        }
        
        # Store in history
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "result": execution_result
        })
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Execution Summary:")
        print(f"   Goal: {plan.get('goal', '')}")
        print(f"   Status: {'✅ Success' if overall_success else '⚠️ Partial/Failed'}")
        print(f"   Steps: {completed_steps}/{len(steps)} completed")
        print(f"   Duration: {execution_result['duration_seconds']}s")
        print("=" * 60)
        
        return execution_result
    
    def execute_goal(self, user_goal: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Plan and execute a user goal in one call
        
        Args:
            user_goal: User's objective
            progress_callback: Optional progress callback
            
        Returns:
            Execution results
        """
        # Plan
        plan = self.plan_task(user_goal)
        
        # Execute
        result = self.execute_plan(plan, progress_callback)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get coordinator status"""
        return {
            "has_current_plan": self.current_plan is not None,
            "execution_history_size": len(self.execution_history),
            "active_tasks": len(self.active_tasks),
            "integration_hub_available": self.integration_hub is not None,
            "ai_planning_available": self.gemini_client is not None
        }
    
    def save_execution_log(self, filepath: Optional[str] = None) -> str:
        """
        Save execution history to file
        
        Args:
            filepath: Optional custom filepath
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = f"coordinator_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        log_data = {
            "saved_at": datetime.now().isoformat(),
            "status": self.get_status(),
            "current_plan": self.current_plan,
            "execution_history": self.execution_history
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"✅ Execution log saved to: {filepath}")
        return filepath


# Convenience functions

def execute_complex_task(task: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
    """
    Execute a complex task with intelligent planning and coordination
    
    Args:
        task: Task description
        progress_callback: Optional progress callback
        
    Returns:
        Execution results
    """
    coordinator = TaskCoordinator()
    return coordinator.execute_goal(task, progress_callback)


def create_task_coordinator(integration_hub: Optional[Any] = None) -> TaskCoordinator:
    """Create and return a new task coordinator instance"""
    return TaskCoordinator(integration_hub)


if __name__ == "__main__":
    print("=" * 70)
    print("🎯 Self-Operating Task Coordinator")
    print("=" * 70)
    
    coordinator = TaskCoordinator()
    
    print("\n📊 Coordinator Status:")
    status = coordinator.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Task coordinator ready!")
    print("Use coordinator.execute_goal(task) to plan and execute tasks\n")
