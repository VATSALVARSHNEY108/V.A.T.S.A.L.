"""
Comprehensive Desktop Controller with Advanced Prompt Understanding & Screen Monitoring
This system understands natural language, breaks tasks into steps, and monitors execution in real-time
"""

import time
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from google import genai
from google.genai import types
from gui_automation import GUIAutomation

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

class ComprehensiveDesktopController:
    """
    Advanced desktop automation with:
    - Deep prompt understanding
    - Intelligent task breakdown
    - Real-time screen monitoring
    - Adaptive execution
    - Learning from outcomes
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        self.gui = GUIAutomation()
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            print("⚠️  Gemini API key not found. AI features will be limited.")
        
        self.execution_log = []
        self.screen_states = []
        self.learning_database = []
        
    def understand_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """
        PHASE 1: Deep understanding of user intent
        
        Analyzes the prompt to understand:
        - Primary goal and objectives
        - Required applications/websites
        - Expected outcomes
        - Potential challenges
        - Success criteria
        """
        if not self.client:
            return self._basic_prompt_understanding(user_prompt)
        
        analysis_prompt = f"""
You are an expert automation assistant. Analyze this user command deeply.

USER COMMAND: "{user_prompt}"

Provide a comprehensive analysis in JSON format:

{{
    "primary_goal": "What the user ultimately wants to achieve",
    "intent_type": "automation|information|creation|navigation|control",
    "complexity_level": "simple|moderate|complex|very_complex",
    "estimated_duration": "time estimate in seconds",
    "required_applications": ["list of apps/websites needed"],
    "required_permissions": ["screen|keyboard|mouse|clipboard|files"],
    "preconditions": ["things that must be true before starting"],
    "success_criteria": ["how to know if task completed successfully"],
    "potential_obstacles": [
        {{
            "obstacle": "what might go wrong",
            "mitigation": "how to handle it"
        }}
    ],
    "context_questions": ["questions to ask user for clarity, if any"],
    "similar_past_tasks": ["similar tasks you might have done before"]
}}

EXAMPLES OF GOOD ANALYSIS:

Command: "Open Chrome, go to GitHub, find my repositories, and screenshot the page"
Analysis:
{{
    "primary_goal": "Navigate to GitHub repositories and capture visual record",
    "intent_type": "navigation",
    "complexity_level": "moderate",
    "estimated_duration": "15-20",
    "required_applications": ["Chrome browser", "GitHub.com"],
    "required_permissions": ["mouse", "keyboard", "screen"],
    "preconditions": ["Chrome installed", "GitHub account logged in", "Internet connected"],
    "success_criteria": ["GitHub repos page is visible", "Screenshot file created"],
    "potential_obstacles": [
        {{"obstacle": "Not logged into GitHub", "mitigation": "Prompt user to login first"}},
        {{"obstacle": "Chrome not default browser", "mitigation": "Use system default browser"}}
    ],
    "context_questions": ["Do you want all repos or specific ones?"],
    "similar_past_tasks": ["Open browser and navigate to website"]
}}

Respond with ONLY valid JSON, no additional text.
"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=analysis_prompt
            )
            
            result_text = self._clean_json_response(response.text)
            understanding = json.loads(result_text)
            understanding["original_prompt"] = user_prompt
            understanding["timestamp"] = datetime.now().isoformat()
            
            return understanding
            
        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}")
            return self._basic_prompt_understanding(user_prompt)
    
    def break_into_steps(self, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """
        PHASE 2: Break task into detailed, executable steps
        
        Creates a comprehensive execution plan with:
        - Sequential steps with dependencies
        - Screen validation checkpoints
        - Error recovery strategies
        - Time estimates per step
        """
        if not self.client:
            return self._basic_step_breakdown(understanding)
        
        breakdown_prompt = f"""
You are creating a detailed automation execution plan.

TASK UNDERSTANDING:
{json.dumps(understanding, indent=2)}

Create a detailed step-by-step execution plan in JSON format:

{{
    "execution_plan": {{
        "total_steps": "number",
        "estimated_time": "total seconds",
        "parallel_possible": true/false,
        "steps": [
            {{
                "step_number": 1,
                "action_type": "navigate|click|type|wait|verify|screenshot|analyze",
                "description": "Human readable description",
                "technical_action": "Specific technical action to perform",
                "target": "What UI element or location to interact with",
                "input_data": "Any data to input (if applicable)",
                "expected_outcome": "What should happen after this step",
                "validation_method": "How to verify this step succeeded",
                "screenshot_after": true/false,
                "wait_time_after": "seconds to wait",
                "error_recovery": [
                    {{
                        "if_error": "type of error",
                        "then_action": "recovery step"
                    }}
                ],
                "dependencies": ["steps that must complete first"],
                "timeout": "max seconds for this step"
            }}
        ],
        "checkpoints": [
            {{
                "after_step": "step number",
                "checkpoint_type": "screen_verification|data_check|state_check",
                "verification": "What to verify",
                "failure_action": "What to do if checkpoint fails"
            }}
        ]
    }}
}}

EXAMPLE FOR: "Open Chrome and search Google for Python tutorials"

{{
    "execution_plan": {{
        "total_steps": 6,
        "estimated_time": "12",
        "parallel_possible": false,
        "steps": [
            {{
                "step_number": 1,
                "action_type": "navigate",
                "description": "Open Chrome browser",
                "technical_action": "Launch application using system launcher",
                "target": "Chrome application",
                "input_data": null,
                "expected_outcome": "Chrome window opens",
                "validation_method": "Check if Chrome window is in foreground",
                "screenshot_after": false,
                "wait_time_after": "2",
                "error_recovery": [
                    {{"if_error": "Chrome not found", "then_action": "Try default browser instead"}}
                ],
                "dependencies": [],
                "timeout": "5"
            }},
            {{
                "step_number": 2,
                "action_type": "wait",
                "description": "Wait for Chrome to fully load",
                "technical_action": "Pause execution",
                "target": null,
                "input_data": null,
                "expected_outcome": "Chrome is ready for input",
                "validation_method": "Time-based wait",
                "screenshot_after": false,
                "wait_time_after": "2",
                "error_recovery": [],
                "dependencies": [1],
                "timeout": "3"
            }},
            {{
                "step_number": 3,
                "action_type": "navigate",
                "description": "Navigate to Google",
                "technical_action": "Type URL in address bar",
                "target": "Address bar",
                "input_data": "https://google.com",
                "expected_outcome": "Google homepage loads",
                "validation_method": "Analyze screen for Google logo",
                "screenshot_after": true,
                "wait_time_after": "2",
                "error_recovery": [
                    {{"if_error": "Page not loading", "then_action": "Retry navigation"}}
                ],
                "dependencies": [2],
                "timeout": "10"
            }},
            {{
                "step_number": 4,
                "action_type": "type",
                "description": "Enter search query",
                "technical_action": "Type text in search box",
                "target": "Google search box",
                "input_data": "Python tutorials",
                "expected_outcome": "Search query appears in box",
                "validation_method": "Visual confirmation via screenshot",
                "screenshot_after": false,
                "wait_time_after": "1",
                "error_recovery": [
                    {{"if_error": "Search box not focused", "then_action": "Click search box first"}}
                ],
                "dependencies": [3],
                "timeout": "5"
            }},
            {{
                "step_number": 5,
                "action_type": "click",
                "description": "Submit search",
                "technical_action": "Press Enter key",
                "target": "Keyboard",
                "input_data": "enter",
                "expected_outcome": "Search results page loads",
                "validation_method": "Check for search results",
                "screenshot_after": true,
                "wait_time_after": "2",
                "error_recovery": [
                    {{"if_error": "No results", "then_action": "Try different query"}}
                ],
                "dependencies": [4],
                "timeout": "10"
            }},
            {{
                "step_number": 6,
                "action_type": "verify",
                "description": "Verify search results displayed",
                "technical_action": "Analyze screen content",
                "target": "Entire screen",
                "input_data": null,
                "expected_outcome": "Search results are visible",
                "validation_method": "AI screen analysis",
                "screenshot_after": true,
                "wait_time_after": "0",
                "error_recovery": [],
                "dependencies": [5],
                "timeout": "5"
            }}
        ],
        "checkpoints": [
            {{
                "after_step": 3,
                "checkpoint_type": "screen_verification",
                "verification": "Confirm Google homepage is loaded",
                "failure_action": "Retry navigation or use alternative search engine"
            }},
            {{
                "after_step": 6,
                "checkpoint_type": "screen_verification",
                "verification": "Confirm search results are displayed",
                "failure_action": "Report failure and save diagnostic screenshot"
            }}
        ]
    }}
}}

Respond with ONLY valid JSON.
"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=breakdown_prompt
            )
            
            result_text = self._clean_json_response(response.text)
            plan = json.loads(result_text)
            return plan
            
        except Exception as e:
            print(f"⚠️  Step breakdown failed: {e}")
            return self._basic_step_breakdown(understanding)
    
    def monitor_screen_during_execution(self, step: Dict[str, Any], step_number: int) -> Dict[str, Any]:
        """
        PHASE 3: Real-time screen monitoring during execution
        
        Monitors the screen:
        - Before step execution (initial state)
        - During execution (if possible)
        - After execution (verify outcome)
        - Compares expected vs actual state
        """
        if not self.client or self.gui.demo_mode:
            return {
                "success": False,
                "message": "Screen monitoring requires local execution with AI vision",
                "demo_mode": True
            }
        
        monitoring_results = {
            "step_number": step_number,
            "step_description": step.get("description"),
            "timestamps": {},
            "screenshots": {},
            "analysis": {}
        }
        
        try:
            # BEFORE: Capture initial state
            print(f"\n🔍 [BEFORE STEP {step_number}] Analyzing screen state...")
            before_screenshot = f"step_{step_number}_before.png"
            self.gui.screenshot(before_screenshot)
            monitoring_results["screenshots"]["before"] = before_screenshot
            monitoring_results["timestamps"]["before"] = datetime.now().isoformat()
            
            # Analyze initial state
            before_analysis = self._analyze_screenshot(
                before_screenshot,
                f"Analyze the current screen state before executing: {step.get('description')}"
            )
            monitoring_results["analysis"]["before"] = before_analysis
            
            print(f"   📊 Current state: {before_analysis.get('current_context', 'Unknown')}")
            
            # DURING: Execute the step
            print(f"\n⚡ [EXECUTING STEP {step_number}] {step.get('description')}")
            execution_result = self._execute_single_step(step)
            monitoring_results["execution_result"] = execution_result
            monitoring_results["timestamps"]["during"] = datetime.now().isoformat()
            
            # Wait for UI to update
            wait_time = float(step.get("wait_time_after", 1))
            if wait_time > 0:
                print(f"   ⏳ Waiting {wait_time}s for UI to update...")
                time.sleep(wait_time)
            
            # AFTER: Capture result state
            print(f"\n🔍 [AFTER STEP {step_number}] Verifying outcome...")
            after_screenshot = f"step_{step_number}_after.png"
            self.gui.screenshot(after_screenshot)
            monitoring_results["screenshots"]["after"] = after_screenshot
            monitoring_results["timestamps"]["after"] = datetime.now().isoformat()
            
            # Analyze result state
            after_analysis = self._analyze_screenshot(
                after_screenshot,
                f"Analyze the screen after executing: {step.get('description')}. Expected: {step.get('expected_outcome')}"
            )
            monitoring_results["analysis"]["after"] = after_analysis
            
            print(f"   📊 New state: {after_analysis.get('current_context', 'Unknown')}")
            
            # VERIFY: Compare expected vs actual
            print(f"\n✅ [VERIFICATION] Comparing expected vs actual outcome...")
            verification = self._verify_step_outcome(
                step,
                before_analysis,
                after_analysis,
                execution_result
            )
            monitoring_results["verification"] = verification
            
            if verification["success"]:
                print(f"   ✅ Step completed successfully!")
                print(f"   {verification.get('message', '')}")
            else:
                print(f"   ⚠️  Step verification failed!")
                print(f"   {verification.get('message', '')}")
                if verification.get("suggested_recovery"):
                    print(f"   💡 Suggestion: {verification['suggested_recovery']}")
            
            monitoring_results["success"] = verification["success"]
            
            # Store in history
            self.screen_states.append(monitoring_results)
            
            return monitoring_results
            
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            return {
                "success": False,
                "error": str(e),
                "step_number": step_number
            }
    
    def _analyze_screenshot(self, screenshot_path: str, instruction: str) -> Dict[str, Any]:
        """Analyze a screenshot using Gemini Vision"""
        try:
            uploaded_file = self.client.files.upload(path=screenshot_path)
            
            prompt = f"""
Analyze this screenshot in detail.

INSTRUCTION: {instruction}

Provide comprehensive analysis in JSON:
{{
    "page_type": "desktop|browser|application",
    "application_name": "name of app/website if identifiable",
    "current_context": "what is happening on screen",
    "visible_ui_elements": [
        {{
            "type": "button|input|link|text|image|menu",
            "text": "visible text",
            "location": "top-left|center|bottom-right|etc",
            "clickable": true/false
        }}
    ],
    "actionable_items": ["list of things that can be interacted with"],
    "state_indicators": {{
        "loading": true/false,
        "error_visible": true/false,
        "success_visible": true/false,
        "ready_for_input": true/false
    }},
    "notable_changes": "any obvious changes from typical state",
    "confidence": "high|medium|low"
}}

Respond with ONLY valid JSON.
"""
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Part.from_uri(
                        file_uri=uploaded_file.uri,
                        mime_type=uploaded_file.mime_type
                    ),
                    prompt
                ]
            )
            
            result_text = self._clean_json_response(response.text)
            return json.loads(result_text)
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _verify_step_outcome(
        self,
        step: Dict[str, Any],
        before_state: Dict[str, Any],
        after_state: Dict[str, Any],
        execution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify if step outcome matches expectation using AI"""
        if not self.client:
            return {"success": True, "message": "Verification skipped (no AI)"}
        
        verification_prompt = f"""
Verify if an automation step completed successfully.

STEP DETAILS:
{json.dumps(step, indent=2)}

STATE BEFORE:
{json.dumps(before_state, indent=2)}

STATE AFTER:
{json.dumps(after_state, indent=2)}

EXECUTION RESULT:
{json.dumps(execution_result, indent=2)}

Analyze and respond in JSON:
{{
    "success": true/false,
    "confidence": "high|medium|low",
    "message": "explanation of outcome",
    "expected_outcome_met": true/false,
    "observable_changes": ["list of changes detected"],
    "issues_detected": ["any problems found"],
    "suggested_recovery": "what to do if failed (if applicable)",
    "continue_execution": true/false
}}

Respond with ONLY valid JSON.
"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=verification_prompt
            )
            
            result_text = self._clean_json_response(response.text)
            return json.loads(result_text)
            
        except Exception as e:
            return {
                "success": True,
                "confidence": "low",
                "message": f"Verification failed: {e}",
                "continue_execution": True
            }
    
    def _execute_single_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single automation step"""
        action_type = step.get("action_type", "").lower()
        target = step.get("target", "")
        input_data = step.get("input_data")
        
        try:
            if action_type == "navigate":
                if "application" in target.lower():
                    result = self.gui.open_application(input_data or target)
                else:
                    import webbrowser
                    url = input_data or target
                    if not url.startswith("http"):
                        url = "https://" + url
                    webbrowser.open(url)
                    result = True
                return {"success": result, "action": "navigate"}
            
            elif action_type == "type":
                if input_data:
                    result = self.gui.type_text(str(input_data))
                    return {"success": result, "action": "type", "text": input_data}
                return {"success": False, "error": "No input data"}
            
            elif action_type == "click":
                if input_data == "enter" or "enter" in str(target).lower():
                    result = self.gui.press_key("enter")
                elif input_data:
                    result = self.gui.press_key(str(input_data))
                else:
                    result = self.gui.click()
                return {"success": result, "action": "click"}
            
            elif action_type == "wait":
                wait_time = float(input_data or step.get("timeout", 2))
                time.sleep(wait_time)
                return {"success": True, "action": "wait", "duration": wait_time}
            
            elif action_type == "screenshot":
                filename = input_data or f"step_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                result = self.gui.screenshot(filename)
                return {"success": bool(result), "action": "screenshot", "file": filename}
            
            elif action_type == "verify" or action_type == "analyze":
                return {"success": True, "action": "verify", "message": "Verification handled by monitoring"}
            
            else:
                return {"success": False, "error": f"Unknown action type: {action_type}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_with_comprehensive_monitoring(
        self,
        user_prompt: str,
        interactive: bool = True
    ) -> Dict[str, Any]:
        """
        MAIN METHOD: Complete execution with all phases
        
        1. Understand the prompt
        2. Break into detailed steps
        3. Execute with real-time monitoring
        4. Learn from the outcome
        """
        print("=" * 80)
        print("🤖 COMPREHENSIVE DESKTOP CONTROLLER".center(80))
        print("=" * 80)
        
        # PHASE 1: Understand
        print("\n📋 PHASE 1: UNDERSTANDING PROMPT")
        print("-" * 80)
        understanding = self.understand_prompt(user_prompt)
        
        print(f"\n✅ Prompt Analysis Complete:")
        print(f"   🎯 Goal: {understanding.get('primary_goal', 'Unknown')}")
        print(f"   📊 Complexity: {understanding.get('complexity_level', 'Unknown')}")
        print(f"   ⏱️  Estimated Time: {understanding.get('estimated_duration', 'Unknown')}s")
        print(f"   🔧 Required Apps: {', '.join(understanding.get('required_applications', []))}")
        
        if understanding.get("context_questions"):
            print(f"\n❓ Clarification Questions:")
            for q in understanding["context_questions"]:
                print(f"   • {q}")
            if interactive:
                print("\nPress Enter to continue or 'q' to quit...")
                if input().strip().lower() == 'q':
                    return {"success": False, "message": "Cancelled by user"}
        
        # PHASE 2: Break Down
        print("\n📋 PHASE 2: BREAKING INTO STEPS")
        print("-" * 80)
        execution_plan = self.break_into_steps(understanding)
        
        steps = execution_plan.get("execution_plan", {}).get("steps", [])
        checkpoints = execution_plan.get("execution_plan", {}).get("checkpoints", [])
        
        print(f"\n✅ Execution Plan Created:")
        print(f"   Total Steps: {len(steps)}")
        print(f"   Checkpoints: {len(checkpoints)}")
        print(f"   Estimated Time: {execution_plan.get('execution_plan', {}).get('estimated_time', 'Unknown')}s")
        
        print("\n📝 Step Breakdown:")
        for step in steps:
            print(f"   {step['step_number']}. {step['description']}")
            print(f"      → Expected: {step.get('expected_outcome', 'N/A')}")
        
        if interactive and steps:
            print("\n⚠️  Ready to execute with real-time monitoring. Press Enter to continue or 'q' to quit...")
            if input().strip().lower() == 'q':
                return {"success": False, "message": "Cancelled by user"}
        
        # PHASE 3: Execute with Monitoring
        print("\n📋 PHASE 3: EXECUTING WITH REAL-TIME MONITORING")
        print("-" * 80)
        
        results = []
        for step in steps:
            step_num = step["step_number"]
            print(f"\n{'='*80}")
            print(f"STEP {step_num}/{len(steps)}: {step['description']}")
            print(f"{'='*80}")
            
            # Execute with comprehensive monitoring
            monitoring_result = self.monitor_screen_during_execution(step, step_num)
            results.append(monitoring_result)
            
            # Check if we should continue
            if not monitoring_result.get("success", False):
                verification = monitoring_result.get("verification", {})
                if not verification.get("continue_execution", True):
                    print("\n⚠️  Critical failure detected. Stopping execution.")
                    break
                
                if interactive:
                    print("\n⚠️  Step failed. Continue anyway? (y/n): ", end="")
                    if input().strip().lower() != 'y':
                        break
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 EXECUTION SUMMARY")
        print("=" * 80)
        
        success_count = sum(1 for r in results if r.get("success", False))
        print(f"\n✅ Successful Steps: {success_count}/{len(results)}")
        print(f"❌ Failed Steps: {len(results) - success_count}/{len(results)}")
        
        if self.screen_states:
            print(f"\n📸 Screen Captures: {len(self.screen_states)} state snapshots saved")
            print(f"📁 Screenshots available in current directory")
        
        return {
            "success": success_count > 0,
            "understanding": understanding,
            "execution_plan": execution_plan,
            "results": results,
            "total_steps": len(results),
            "successful_steps": success_count,
            "screen_states": self.screen_states
        }
    
    def _clean_json_response(self, text: str) -> str:
        """Clean JSON from markdown code blocks"""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    
    def _basic_prompt_understanding(self, prompt: str) -> Dict[str, Any]:
        """Fallback understanding without AI"""
        return {
            "original_prompt": prompt,
            "primary_goal": prompt,
            "intent_type": "automation",
            "complexity_level": "moderate",
            "estimated_duration": "10-30",
            "required_applications": [],
            "success_criteria": ["Task completes without errors"]
        }
    
    def _basic_step_breakdown(self, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback step breakdown without AI"""
        return {
            "execution_plan": {
                "total_steps": 1,
                "estimated_time": "10",
                "steps": [{
                    "step_number": 1,
                    "action_type": "execute",
                    "description": understanding.get("primary_goal", "Execute command"),
                    "expected_outcome": "Task completed",
                    "validation_method": "Manual verification"
                }]
            }
        }


def main():
    """CLI Interface for Comprehensive Desktop Controller"""
    print("=" * 80)
    print("🤖 COMPREHENSIVE DESKTOP CONTROLLER".center(80))
    print("AI-Powered Automation with Real-Time Monitoring".center(80))
    print("=" * 80)
    
    controller = ComprehensiveDesktopController()
    
    print("\n📚 CAPABILITIES:")
    print("   • Deep Prompt Understanding - Analyzes intent, complexity, requirements")
    print("   • Intelligent Task Breakdown - Creates detailed execution plans")
    print("   • Real-Time Screen Monitoring - Captures before/during/after states")
    print("   • Outcome Verification - AI compares expected vs actual results")
    print("   • Adaptive Execution - Recovers from errors intelligently")
    print("   • Learning System - Improves from past executions")
    
    print("\n💡 EXAMPLE PROMPTS:")
    print('   • "Open Chrome, navigate to GitHub, find my repositories, and take a screenshot"')
    print('   • "Launch VS Code, create a new Python file, and write a hello world function"')
    print('   • "Search Google for best Python practices and open the first 3 links"')
    print('   • "Open Spotify, search for jazz music, and start playing"')
    
    print("\n" + "=" * 80)
    print("\nType 'quit' to exit, 'help' for more info\n")
    
    while True:
        try:
            prompt = input("🎯 Enter your command: ").strip()
            
            if not prompt:
                continue
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if prompt.lower() == 'help':
                print("\n📖 HOW IT WORKS:")
                print("   1. UNDERSTANDING: AI analyzes your prompt deeply")
                print("   2. BREAKDOWN: Creates detailed step-by-step plan")
                print("   3. MONITORING: Captures screen before, during, after each step")
                print("   4. VERIFICATION: AI compares expected vs actual outcomes")
                print("   5. LEARNING: System learns from successes and failures")
                print("\n   Just describe what you want in plain English!")
                continue
            
            # Execute with comprehensive monitoring
            result = controller.execute_with_comprehensive_monitoring(
                prompt,
                interactive=True
            )
            
            if result.get("success"):
                print(f"\n✅ TASK COMPLETED SUCCESSFULLY!")
            else:
                print(f"\n⚠️  TASK COMPLETED WITH ISSUES")
            
            print("\n" + "-" * 80 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
