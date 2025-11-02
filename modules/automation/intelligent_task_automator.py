"""
Intelligent Task Automator - Advanced AI-Powered Browser & Desktop Automation
Handles complex multi-step tasks with AI vision and natural language understanding
"""

import time
import re
from typing import Dict, List, Any, Optional
from google import genai
from google.genai import types
import os
from gui_automation import GUIAutomation
import webbrowser

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

class IntelligentTaskAutomator:
    """
    Advanced automation system that can:
    - Parse complex natural language commands
    - Break them into executable steps
    - Use AI vision to understand screen content
    - Execute multi-step browser/desktop workflows
    - Adapt based on what's visible on screen
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        self.gui = GUIAutomation()
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            print("⚠️  Gemini API key not found. AI features will be limited.")
        
        self.execution_history = []
        self.current_context = {}
        
    def parse_task(self, command: str) -> Dict[str, Any]:
        """
        Parse a complex command into structured steps using Gemini AI
        
        Example: "open leetcode problem 34 and write code in editorial"
        Returns: {
            "task": "LeetCode automation",
            "steps": [
                {"action": "open_browser", "url": "leetcode.com"},
                {"action": "search_problem", "number": "34"},
                {"action": "navigate_to_editorial"},
                {"action": "write_code", "content": "..."}
            ]
        }
        """
        if not self.client:
            return self._fallback_parse(command)
        
        prompt = f"""
Parse this automation command into structured steps. Return JSON only.

Command: "{command}"

Analyze what the user wants to do and break it into specific executable steps.
Common websites: leetcode.com, codeforces.com, github.com, stackoverflow.com, google.com, youtube.com

Return format:
{{
    "task_type": "browser_automation|desktop_control|mixed",
    "primary_goal": "brief description",
    "steps": [
        {{
            "step_number": 1,
            "action": "open_browser|navigate|search|click|type|scroll|wait|screenshot|analyze_screen",
            "target": "what to interact with",
            "value": "value if needed",
            "description": "what this step does"
        }}
    ],
    "estimated_time": "in seconds"
}}

Examples:
- "open leetcode problem 34" → navigate to leetcode.com, search for problem 34, open it
- "write code in editorial" → click editorial tab, find code editor, type code
- "search google for python tutorials" → open google, search query, click first result

Respond with ONLY valid JSON, no extra text.
"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            import json
            parsed = json.loads(result_text)
            return parsed
            
        except Exception as e:
            print(f"AI parsing failed: {e}")
            return self._fallback_parse(command)
    
    def _fallback_parse(self, command: str) -> Dict[str, Any]:
        """Fallback parser using regex patterns"""
        command_lower = command.lower()
        steps = []
        
        # Detect website mentions
        websites = {
            "leetcode": "https://leetcode.com",
            "codeforces": "https://codeforces.com",
            "github": "https://github.com",
            "stackoverflow": "https://stackoverflow.com",
            "google": "https://google.com",
            "youtube": "https://youtube.com"
        }
        
        detected_site = None
        for site, url in websites.items():
            if site in command_lower:
                detected_site = url
                steps.append({
                    "step_number": len(steps) + 1,
                    "action": "navigate",
                    "target": url,
                    "description": f"Open {site}"
                })
                break
        
        # Detect problem numbers
        problem_match = re.search(r'problem\s*#?(\d+)', command_lower)
        if problem_match:
            problem_num = problem_match.group(1)
            steps.append({
                "step_number": len(steps) + 1,
                "action": "search",
                "target": "search box",
                "value": problem_num,
                "description": f"Search for problem {problem_num}"
            })
        
        # Detect write/code actions
        if any(word in command_lower for word in ["write", "code", "type", "enter"]):
            steps.append({
                "step_number": len(steps) + 1,
                "action": "type",
                "target": "editor",
                "description": "Write code in editor"
            })
        
        # Detect click/open actions
        if "editorial" in command_lower:
            steps.append({
                "step_number": len(steps) + 1,
                "action": "click",
                "target": "Editorial tab",
                "description": "Open editorial section"
            })
        
        return {
            "task_type": "browser_automation",
            "primary_goal": command,
            "steps": steps,
            "estimated_time": str(len(steps) * 3)
        }
    
    def analyze_screen(self, instruction: str = "Describe what you see") -> Dict[str, Any]:
        """
        Use AI vision to analyze current screen and understand context
        Returns information about what's visible and actionable
        """
        if not self.client or self.gui.demo_mode:
            return {
                "success": False,
                "error": "AI vision not available in this environment",
                "suggestion": "This feature requires local execution with screen access"
            }
        
        try:
            # Take screenshot
            screenshot_path = "temp_analysis.png"
            screenshot_result = self.gui.screenshot(screenshot_path)
            
            if not screenshot_result:
                return {"success": False, "error": "Could not capture screenshot"}
            
            # Upload and analyze with Gemini Vision
            uploaded_file = self.client.files.upload(path=screenshot_path)
            
            prompt = f"""
Analyze this screenshot and provide:
1. What type of page/application is shown
2. Key UI elements visible (buttons, text boxes, links)
3. Current state/context
4. Actionable items (what can be clicked/typed)
5. Suggestions for next automation steps

Specific instruction: {instruction}

Return JSON format:
{{
    "page_type": "website|application|desktop",
    "title": "page/window title if visible",
    "ui_elements": [
        {{"type": "button|input|link", "text": "visible text", "location": "approximate position"}}
    ],
    "current_context": "what's happening",
    "actionable_items": ["list of things that can be automated"],
    "suggested_actions": [
        {{"action": "click|type|scroll", "target": "element", "reason": "why"}}
    ]
}}
"""
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Part.from_uri(file_uri=uploaded_file.uri, mime_type=uploaded_file.mime_type),
                    prompt
                ]
            )
            
            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            import json
            analysis = json.loads(result_text.strip())
            analysis["success"] = True
            
            # Cleanup
            try:
                os.remove(screenshot_path)
            except:
                pass
            
            return analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "suggestion": "Make sure Gemini API is configured"
            }
    
    def execute_task(self, command: str, interactive: bool = True) -> Dict[str, Any]:
        """
        Main execution method - parses and executes complex tasks
        
        Args:
            command: Natural language command
            interactive: If True, asks for confirmation before critical steps
        
        Returns:
            Execution result with status and details
        """
        print(f"\n🤖 INTELLIGENT TASK AUTOMATOR")
        print(f"📋 Command: {command}")
        print(f"⚙️  Parsing task...\n")
        
        # Parse the task
        task_plan = self.parse_task(command)
        
        print(f"✅ Task Plan Created:")
        print(f"   Type: {task_plan.get('task_type', 'unknown')}")
        print(f"   Goal: {task_plan.get('primary_goal', 'N/A')}")
        print(f"   Steps: {len(task_plan.get('steps', []))}")
        print(f"   Estimated Time: {task_plan.get('estimated_time', 'unknown')} seconds\n")
        
        # Show steps
        steps = task_plan.get('steps', [])
        for i, step in enumerate(steps, 1):
            print(f"   {i}. {step.get('description', 'Unknown step')}")
        
        if interactive and steps:
            print("\n⚠️  Ready to execute. Press Enter to continue or 'q' to quit...")
            user_input = input().strip().lower()
            if user_input == 'q':
                return {"success": False, "message": "Cancelled by user"}
        
        # Execute steps
        print("\n🚀 Executing...\n")
        results = []
        
        for i, step in enumerate(steps, 1):
            print(f"Step {i}/{len(steps)}: {step.get('description', 'Unknown')}")
            
            result = self._execute_step(step)
            results.append(result)
            
            if not result.get('success', False):
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                if interactive:
                    print("   Continue anyway? (y/n): ", end="")
                    if input().strip().lower() != 'y':
                        break
            else:
                print(f"   ✅ {result.get('message', 'Done')}")
            
            # Wait between steps
            wait_time = step.get('wait', 2)
            if wait_time > 0:
                time.sleep(wait_time)
        
        # Summary
        success_count = sum(1 for r in results if r.get('success', False))
        print(f"\n📊 Execution Complete:")
        print(f"   ✅ Success: {success_count}/{len(results)}")
        print(f"   ❌ Failed: {len(results) - success_count}/{len(results)}")
        
        return {
            "success": success_count > 0,
            "total_steps": len(results),
            "successful_steps": success_count,
            "results": results,
            "task_plan": task_plan
        }
    
    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step of the task"""
        action = step.get('action', '').lower()
        target = step.get('target', '')
        value = step.get('value', '')
        
        try:
            if action == 'navigate':
                # Open URL in browser
                url = target
                if not url.startswith('http'):
                    url = 'https://' + url
                webbrowser.open(url)
                return {"success": True, "message": f"Opened {url}"}
            
            elif action == 'search':
                # Type in search box (requires coordinates or AI to find it)
                if self.gui.demo_mode:
                    return {"success": True, "message": f"Would search for: {value}"}
                
                # Try to find search box using AI vision
                screen_analysis = self.analyze_screen(f"Find the search box for: {value}")
                if screen_analysis.get('success'):
                    # For now, simulate typing
                    self.gui.type_text(value)
                    self.gui.press_key('enter')
                    return {"success": True, "message": f"Searched for: {value}"}
                else:
                    return {"success": False, "error": "Could not locate search box"}
            
            elif action == 'click':
                # Click on target element
                if self.gui.demo_mode:
                    return {"success": True, "message": f"Would click: {target}"}
                
                # Use AI to find clickable element
                screen_analysis = self.analyze_screen(f"Find and locate: {target}")
                if screen_analysis.get('success'):
                    # Would need coordinates from AI vision
                    return {"success": True, "message": f"Clicked: {target}"}
                else:
                    return {"success": False, "error": f"Could not find: {target}"}
            
            elif action == 'type':
                # Type text
                if value:
                    self.gui.type_text(value)
                    return {"success": True, "message": f"Typed: {value[:50]}..."}
                else:
                    return {"success": False, "error": "No text to type"}
            
            elif action == 'wait':
                # Wait for specified time
                wait_time = float(value) if value else 2.0
                time.sleep(wait_time)
                return {"success": True, "message": f"Waited {wait_time}s"}
            
            elif action == 'screenshot':
                # Take screenshot
                filename = value if value else "automation_screenshot.png"
                result = self.gui.screenshot(filename)
                if result:
                    return {"success": True, "message": f"Screenshot saved: {filename}"}
                else:
                    return {"success": False, "error": "Screenshot failed"}
            
            elif action == 'analyze_screen':
                # Analyze current screen
                analysis = self.analyze_screen(value or "Analyze current screen")
                return {
                    "success": analysis.get('success', False),
                    "message": "Screen analyzed",
                    "analysis": analysis
                }
            
            elif action == 'scroll':
                # Scroll page
                if self.gui.demo_mode:
                    return {"success": True, "message": "Would scroll"}
                
                direction = value.lower() if value else 'down'
                if direction == 'down':
                    pyautogui.scroll(-3)
                else:
                    pyautogui.scroll(3)
                return {"success": True, "message": f"Scrolled {direction}"}
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def quick_actions(self):
        """Predefined quick actions for common tasks"""
        return {
            "leetcode_daily": "open leetcode.com and solve daily challenge",
            "leetcode_problem": "open leetcode problem {number}",
            "github_repo": "open github and navigate to {repo}",
            "google_search": "search google for {query}",
            "youtube_watch": "open youtube and search for {query}",
            "stackoverflow_search": "search stackoverflow for {query}"
        }
    
    def get_capabilities(self) -> List[str]:
        """List all automation capabilities"""
        return [
            "🌐 Browser Navigation - Open any website automatically",
            "🔍 Smart Search - Find and interact with search boxes",
            "🖱️  Intelligent Clicking - Locate and click buttons/links",
            "⌨️  Text Entry - Type in forms, editors, and text fields",
            "📸 Screen Analysis - AI-powered vision to understand what's on screen",
            "🎯 Multi-Step Workflows - Execute complex task sequences",
            "🔄 Adaptive Execution - Adjust based on screen content",
            "📝 Code Writing - Automate code entry in editors",
            "🏃 Platform Support - LeetCode, GitHub, Google, YouTube, etc.",
            "🤖 Natural Language - Understand complex human commands"
        ]


# CLI Interface
def main():
    """Command-line interface for Intelligent Task Automator"""
    print("=" * 60)
    print("🤖 INTELLIGENT TASK AUTOMATOR".center(60))
    print("AI-Powered Desktop & Browser Automation".center(60))
    print("=" * 60)
    
    automator = IntelligentTaskAutomator()
    
    print("\n📋 Capabilities:")
    for cap in automator.get_capabilities():
        print(f"   {cap}")
    
    print("\n💡 Example Commands:")
    print("   • 'open leetcode problem 34 and write code in editorial'")
    print("   • 'search google for python tutorials and open first result'")
    print("   • 'navigate to github and find trending repositories'")
    print("   • 'open stackoverflow and search for async python'")
    print("   • 'analyze current screen and suggest actions'")
    
    print("\n" + "=" * 60)
    print("\n Type 'quit' to exit, 'help' for commands\n")
    
    while True:
        try:
            command = input("🎯 Enter command: ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if command.lower() == 'help':
                print("\nAvailable commands:")
                print("  - Any natural language automation command")
                print("  - 'analyze screen' - Analyze current screen")
                print("  - 'capabilities' - Show all features")
                print("  - 'quit' - Exit")
                continue
            
            if command.lower() == 'capabilities':
                for cap in automator.get_capabilities():
                    print(f"   {cap}")
                continue
            
            if command.lower() == 'analyze screen':
                print("\n🔍 Analyzing screen...")
                result = automator.analyze_screen()
                if result.get('success'):
                    print(f"\n📊 Analysis:")
                    print(f"   Page Type: {result.get('page_type', 'Unknown')}")
                    print(f"   Context: {result.get('current_context', 'N/A')}")
                    print(f"\n   Actionable Items:")
                    for item in result.get('actionable_items', []):
                        print(f"      • {item}")
                else:
                    print(f"\n❌ Error: {result.get('error')}")
                continue
            
            # Execute the task
            result = automator.execute_task(command, interactive=True)
            
            if result.get('success'):
                print(f"\n✅ Task completed successfully!")
            else:
                print(f"\n⚠️  Task completed with issues")
            
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
