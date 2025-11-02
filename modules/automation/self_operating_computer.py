"""
Self-Operating Computer - Gemini Vision Edition (Enhanced)
Fully integrated autonomous computer controller with OCR, element detection, and VATSAL ecosystem integration
Inspired by OthersideAI's self-operating-computer but powered by Google Gemini Vision
"""

import os
import json
import time
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any, Callable
from dotenv import load_dotenv

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    # PyAutoGUI safety settings
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ google-genai not available")

load_dotenv()

class SelfOperatingComputer:
    """
    Enhanced autonomous computer controller using Gemini Vision
    Features:
    - AI-powered screen analysis
    - OCR for text extraction
    - Element detection and clicking
    - Mouse and keyboard automation
    - Multi-step task execution
    - Integration with VATSAL ecosystem
    """
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False, log_callback: Optional[Callable] = None):
        """
        Initialize Self-Operating Computer
        
        Args:
            api_key: Gemini API key (optional, reads from env)
            verbose: Enable detailed logging
            log_callback: Optional callback for logging messages
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai package is required. Install with: pip install google-genai")
        
        self.client = genai.Client(api_key=self.api_key)
        self.verbose = verbose
        self.log_callback = log_callback
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.session_history: List[Dict[str, Any]] = []
        self.max_iterations = 30
        self.current_iteration = 0
        self.stop_requested = False
        
        # Get screen dimensions
        screen_width, screen_height = pyautogui.size()
        self.screen_size = {"width": screen_width, "height": screen_height}
        
        # Enhanced system prompt with OCR and element detection
        self.system_prompt = """You are an advanced self-operating computer agent powered by Gemini Vision.

Your task is to accomplish user objectives by viewing the screen and deciding on precise mouse/keyboard actions.

CAPABILITIES:
1. **Screen Vision**: Analyze screenshots to understand UI state
2. **OCR**: Extract text from screen for precise clicking
3. **Element Detection**: Identify buttons, links, input fields
4. **Mouse Control**: Move, click, drag operations
5. **Keyboard Control**: Type text, shortcuts, key combinations
6. **Multi-step Reasoning**: Break complex tasks into steps

OUTPUT FORMAT (JSON):
{
    "thought": "Current observation and reasoning about next action",
    "action": "ACTION_TYPE",
    "parameters": {
        "x": 100,
        "y": 200,
        "text": "example",
        "element": "button name"
    },
    "progress": 25,
    "completed": false,
    "confidence": 0.9
}

AVAILABLE ACTIONS:

1. **click_element** - Click on UI element by description
   Parameters: {"element": "Sign In button", "x": int [optional], "y": int [optional]}
   Use when you can see and describe a clickable element

2. **click_position** - Click at exact coordinates
   Parameters: {"x": int, "y": int, "button": "left|right|middle", "clicks": 1|2}
   Use for precise coordinate-based clicking

3. **type_text** - Type text at current cursor position
   Parameters: {"text": "string to type", "interval": 0.05}
   Use for entering text in input fields

4. **press_key** - Press keyboard key
   Parameters: {"key": "enter|tab|escape|backspace|delete|space|up|down|left|right|..."}
   Common keys: enter, tab, space, backspace, delete, escape

5. **hotkey** - Press key combination
   Parameters: {"keys": ["ctrl", "c"]} or {"keys": ["cmd", "space"]}
   Common: ["ctrl", "c"], ["ctrl", "v"], ["ctrl", "a"], ["alt", "tab"]

6. **move_mouse** - Move cursor to position
   Parameters: {"x": int, "y": int, "duration": 0.3}
   Use before clicking or to hover

7. **scroll** - Scroll the screen
   Parameters: {"direction": "up|down", "amount": 3}
   Amount is number of scroll units (higher = more scrolling)

8. **drag** - Drag from one point to another
   Parameters: {"start_x": int, "start_y": int, "end_x": int, "end_y": int, "duration": 0.5}
   Use for drag operations, selecting text, etc.

9. **wait** - Wait for page/element to load
   Parameters: {"seconds": 2, "reason": "waiting for page load"}
   Use after navigation, clicks, or when content is loading

10. **screenshot_analysis** - Take new screenshot for detailed analysis
    Parameters: {"focus": "specific area to analyze"}
    Use when you need to verify current state

11. **complete** - Mark objective as accomplished
    Parameters: {"summary": "Brief summary of what was accomplished"}
    Use ONLY when objective is fully achieved

DECISION MAKING GUIDELINES:

1. **Accuracy First**: 
   - Carefully analyze screenshot before deciding
   - Use element descriptions when possible (more reliable than coordinates)
   - Verify screen state matches expectations

2. **Screen Coordinates**:
   - Screen size: {screen_width}x{screen_height}
   - Top-left corner is (0, 0)
   - Bottom-right is ({screen_width}, {screen_height})
   - Look carefully at element positions in screenshot

3. **Progressive Actions**:
   - Break complex tasks into small steps
   - Wait after clicks/navigation for pages to load
   - Verify each step before proceeding

4. **Error Recovery**:
   - If action fails, try alternative approach
   - Use screenshot_analysis to understand current state
   - Don't repeat same failing action

5. **Safety**:
   - Never delete important files without confirmation
   - Avoid destructive actions on system
   - If unsure, mark task as needing clarification

6. **Completion**:
   - Set "completed": true ONLY when objective is fully achieved
   - Update "progress" (0-100) to track advancement
   - Set "confidence" (0.0-1.0) in your decision

EXAMPLE DECISION FLOW:
1. Analyze screenshot → Identify target element
2. Choose appropriate action (click_element vs click_position)
3. Execute action
4. Wait if needed for response
5. Take screenshot to verify
6. Continue or complete

Remember: Output ONLY valid JSON, no additional text or explanation.
"""

    def _log(self, message: str, level: str = "INFO"):
        """
        Log messages with timestamp
        
        Args:
            message: Log message
            level: Log level (INFO, WARN, ERROR, SUCCESS)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Icon mapping
        icons = {
            "INFO": "🔍",
            "WARN": "⚠️",
            "ERROR": "❌",
            "SUCCESS": "✅",
            "PROGRESS": "📊"
        }
        icon = icons.get(level, "ℹ️")
        
        formatted_message = f"[{timestamp}] {icon} {message}"
        
        # Print to console
        print(formatted_message)
        
        # Call external log callback if provided (for GUI integration)
        if self.log_callback:
            try:
                self.log_callback(formatted_message, level)
            except Exception as e:
                print(f"Log callback error: {e}")
        
        # Add to session history
        if self.verbose:
            self.session_history.append({
                "timestamp": timestamp,
                "level": level,
                "message": message
            })

    def capture_screen(self) -> str:
        """
        Capture screenshot and save to disk
        
        Returns:
            Path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"screen_{timestamp}.png"
        filepath = self.screenshot_dir / filename
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            self._log(f"Screenshot saved: {filename}", "INFO")
            return str(filepath)
        except Exception as e:
            self._log(f"Screenshot capture failed: {e}", "ERROR")
            raise

    def analyze_screen_and_decide(self, objective: str, screenshot_path: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Use Gemini Vision to analyze screen and decide next action
        
        Args:
            objective: User's goal
            screenshot_path: Path to screenshot
            context: Optional additional context
            
        Returns:
            Decision dictionary with action and parameters
        """
        self._log(f"Analyzing screen... (Iteration {self.current_iteration + 1}/{self.max_iterations})", "PROGRESS")
        
        # Format system prompt with screen size
        formatted_prompt = self.system_prompt.replace(
            "{screen_width}", str(self.screen_size["width"])
        ).replace(
            "{screen_height}", str(self.screen_size["height"])
        )
        
        # Build context from recent history
        iteration_context = ""
        if self.current_iteration > 0 and self.session_history:
            recent_actions = [
                h for h in self.session_history
                if isinstance(h, dict) and 'action' in h
            ][-3:]
            
            if recent_actions:
                iteration_context = f"\n\nRecent actions:\n{json.dumps(recent_actions, indent=2)}"
        
        # Additional context if provided
        extra_context = f"\n\nAdditional context: {context}" if context else ""
        
        # Build user message
        user_message = f"""OBJECTIVE: {objective}

Current iteration: {self.current_iteration + 1}/{self.max_iterations}
Screen resolution: {self.screen_size['width']}x{self.screen_size['height']}
{iteration_context}{extra_context}

Analyze the screenshot and decide the NEXT SINGLE ACTION to accomplish the objective.

IMPORTANT:
- Output ONLY valid JSON
- Choose the most appropriate action
- Be precise with coordinates if using click_position
- Prefer click_element when you can describe the element
- Update progress percentage (0-100)
- Set completed: true ONLY when objective is fully achieved"""

        try:
            # Read screenshot
            with open(screenshot_path, "rb") as img_file:
                image_data = img_file.read()
            
            # Call Gemini Vision
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_bytes(
                                data=image_data,
                                mime_type="image/png"
                            ),
                            types.Part.from_text(text=user_message)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=formatted_prompt,
                    temperature=0.3,
                    max_output_tokens=2048,
                )
            )
            
            # Parse response
            response_text = ""
            if response and hasattr(response, 'text'):
                response_text = response.text.strip()
            else:
                raise ValueError("Empty response from Gemini")
            
            # Clean JSON from markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            decision = json.loads(response_text)
            
            # Validate required fields
            required_fields = ["thought", "action", "parameters"]
            for field in required_fields:
                if field not in decision:
                    raise ValueError(f"Missing required field: {field}")
            
            # Add defaults
            decision.setdefault("progress", 0)
            decision.setdefault("completed", False)
            decision.setdefault("confidence", 0.5)
            
            return decision
            
        except json.JSONDecodeError as e:
            self._log(f"JSON parsing error: {e}", "ERROR")
            self._log(f"Raw response: {response_text[:300] if response_text else 'No response'}...", "ERROR")
            
            # Return safe fallback action
            return {
                "thought": "Failed to parse AI response - waiting to retry",
                "action": "wait",
                "parameters": {"seconds": 2, "reason": "parsing error recovery"},
                "progress": 0,
                "completed": False,
                "confidence": 0.0
            }
            
        except Exception as e:
            self._log(f"Error analyzing screen: {str(e)}", "ERROR")
            
            return {
                "thought": f"Analysis error: {str(e)}",
                "action": "wait",
                "parameters": {"seconds": 2, "reason": "error recovery"},
                "progress": 0,
                "completed": False,
                "confidence": 0.0
            }

    def execute_action(self, decision: Dict[str, Any]) -> bool:
        """
        Execute the decided action
        
        Args:
            decision: Decision dictionary from analyze_screen_and_decide
            
        Returns:
            True if should continue, False if should stop
        """
        action = decision.get("action", "").lower()
        params = decision.get("parameters", {})
        thought = decision.get("thought", "")
        progress = decision.get("progress", 0)
        confidence = decision.get("confidence", 0.5)
        
        # Log decision
        self._log(f"💭 Thought: {thought}", "INFO")
        self._log(f"📊 Progress: {progress}% | Confidence: {confidence:.0%}", "PROGRESS")
        self._log(f"⚡ Action: {action} | Params: {params}", "INFO")
        
        # Store in history
        self.session_history.append({
            "iteration": self.current_iteration,
            "thought": thought,
            "action": action,
            "parameters": params,
            "progress": progress,
            "confidence": confidence
        })
        
        try:
            # Execute based on action type
            if action == "click_element":
                # Click on element by description (use coordinates if provided, otherwise center of screen)
                element = params.get("element", "")
                x = params.get("x", self.screen_size["width"] // 2)
                y = params.get("y", self.screen_size["height"] // 2)
                
                self._log(f"Clicking element: {element} at ({x}, {y})", "INFO")
                pyautogui.click(x, y)
                
            elif action == "click_position":
                x = params.get("x", 0)
                y = params.get("y", 0)
                button = params.get("button", "left")
                clicks = params.get("clicks", 1)
                
                pyautogui.click(x, y, clicks=clicks, button=button)
                
            elif action == "move_mouse":
                x = params.get("x", 0)
                y = params.get("y", 0)
                duration = params.get("duration", 0.3)
                
                pyautogui.moveTo(x, y, duration=duration)
                
            elif action == "type_text":
                text = params.get("text", "")
                interval = params.get("interval", 0.05)
                
                pyautogui.write(text, interval=interval)
                
            elif action == "press_key":
                key = params.get("key", "")
                
                pyautogui.press(key)
                
            elif action == "hotkey":
                keys = params.get("keys", [])
                
                if keys:
                    pyautogui.hotkey(*keys)
                
            elif action == "scroll":
                direction = params.get("direction", "down")
                amount = params.get("amount", 3)
                
                scroll_amount = -amount * 100 if direction == "down" else amount * 100
                pyautogui.scroll(scroll_amount)
                
            elif action == "drag":
                start_x = params.get("start_x", 0)
                start_y = params.get("start_y", 0)
                end_x = params.get("end_x", 0)
                end_y = params.get("end_y", 0)
                duration = params.get("duration", 0.5)
                
                pyautogui.moveTo(start_x, start_y)
                pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
                
            elif action == "wait":
                seconds = params.get("seconds", 1)
                reason = params.get("reason", "general wait")
                
                self._log(f"Waiting {seconds}s: {reason}", "INFO")
                time.sleep(seconds)
                
            elif action == "screenshot_analysis":
                focus = params.get("focus", "general")
                self._log(f"Analyzing: {focus}", "INFO")
                # Screenshot will be taken in next iteration
                time.sleep(0.5)
                
            elif action == "complete":
                summary = params.get("summary", "Objective completed")
                self._log(f"✅ COMPLETED: {summary}", "SUCCESS")
                return False
                
            else:
                self._log(f"Unknown action: {action} - skipping", "WARN")
                time.sleep(0.5)
            
            # Small pause after action
            time.sleep(0.5)
            return True
            
        except Exception as e:
            self._log(f"Error executing action '{action}': {str(e)}", "ERROR")
            time.sleep(1)
            return True

    def operate(self, objective: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Main autonomous operation loop
        
        Args:
            objective: User's goal to accomplish
            context: Optional additional context
            
        Returns:
            Session summary dictionary
        """
        self._log("=" * 70, "INFO")
        self._log("🎯 Starting self-operating mode", "SUCCESS")
        self._log(f"📋 Objective: {objective}", "INFO")
        self._log(f"🖥️  Screen: {self.screen_size['width']}x{self.screen_size['height']}", "INFO")
        self._log("=" * 70, "INFO")
        
        start_time = time.time()
        self.current_iteration = 0
        self.session_history = []
        self.stop_requested = False
        
        try:
            while self.current_iteration < self.max_iterations and not self.stop_requested:
                # Capture current screen state
                screenshot_path = self.capture_screen()
                
                # Analyze and decide
                decision = self.analyze_screen_and_decide(objective, screenshot_path, context)
                
                # Check if AI marked as completed
                if decision.get("completed", False):
                    self._log("✅ Objective marked as completed by AI", "SUCCESS")
                    break
                
                # Execute action
                should_continue = self.execute_action(decision)
                
                if not should_continue:
                    break
                
                self.current_iteration += 1
                self._log("-" * 70, "INFO")
                
            else:
                if self.stop_requested:
                    self._log("🛑 Stopped by user request", "WARN")
                else:
                    self._log(f"⚠️  Reached maximum iterations ({self.max_iterations})", "WARN")
        
        except KeyboardInterrupt:
            self._log("🛑 Stopped by user (Ctrl+C)", "WARN")
        except Exception as e:
            self._log(f"❌ Fatal error: {str(e)}", "ERROR")
            import traceback
            self._log(traceback.format_exc(), "ERROR")
        
        # Calculate summary
        duration = time.time() - start_time
        
        summary = {
            "objective": objective,
            "iterations": self.current_iteration,
            "duration_seconds": round(duration, 2),
            "completed": self.current_iteration < self.max_iterations and not self.stop_requested,
            "stopped_by_user": self.stop_requested,
            "history": self.session_history
        }
        
        # Log summary
        self._log("=" * 70, "INFO")
        self._log("📊 Session Summary:", "INFO")
        self._log(f"   Total iterations: {summary['iterations']}", "INFO")
        self._log(f"   Duration: {summary['duration_seconds']}s", "INFO")
        status = "✅ Completed" if summary['completed'] else "🛑 Stopped" if summary['stopped_by_user'] else "⏸️  Incomplete"
        self._log(f"   Status: {status}", "INFO")
        self._log("=" * 70, "INFO")
        
        return summary

    def operate_with_voice(self) -> Dict[str, Any]:
        """
        Start self-operating mode with voice input for the objective
        
        Returns:
            Session summary dictionary
        """
        try:
            import speech_recognition as sr
        except ImportError:
            self._log("❌ Voice support requires: pip install SpeechRecognition", "ERROR")
            return {
                "objective": "",
                "iterations": 0,
                "duration_seconds": 0,
                "completed": False,
                "error": "SpeechRecognition not installed"
            }
        
        recognizer = sr.Recognizer()
        
        print("\n🎤 Voice Input Mode")
        print("Please state your objective when ready...")
        print("(Listening...)\n")
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            print("🔄 Processing voice input...")
            objective = recognizer.recognize_google(audio)
            
            print(f"\n✅ Understood objective: '{objective}'")
            print("Starting in 3 seconds...\n")
            time.sleep(3)
            
            return self.operate(objective)
            
        except sr.WaitTimeoutError:
            self._log("❌ No speech detected. Please try again.", "ERROR")
            return {"objective": "", "iterations": 0, "duration_seconds": 0, "completed": False, "error": "Timeout"}
        except sr.UnknownValueError:
            self._log("❌ Could not understand audio. Please try again.", "ERROR")
            return {"objective": "", "iterations": 0, "duration_seconds": 0, "completed": False, "error": "Unknown value"}
        except sr.RequestError as e:
            self._log(f"❌ Speech recognition error: {e}", "ERROR")
            return {"objective": "", "iterations": 0, "duration_seconds": 0, "completed": False, "error": str(e)}
        except Exception as e:
            self._log(f"❌ Error: {str(e)}", "ERROR")
            return {"objective": "", "iterations": 0, "duration_seconds": 0, "completed": False, "error": str(e)}

    def stop(self):
        """Request stop of current operation"""
        self.stop_requested = True
        self._log("Stop requested - will halt after current action", "WARN")


def main():
    """CLI interface for self-operating computer"""
    print("=" * 70)
    print("🤖 SELF-OPERATING COMPUTER - Gemini Vision Edition")
    print("=" * 70)
    print("\nAutonomous computer control powered by Google Gemini Vision")
    print("Inspired by OthersideAI's self-operating-computer\n")
    
    try:
        computer = SelfOperatingComputer(verbose=True)
        
        print("Choose input mode:")
        print("1. Text input")
        print("2. Voice input")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            objective = input("\n📝 Enter your objective: ").strip()
            if objective:
                print()
                result = computer.operate(objective)
                
                # Save session log
                save_log = input("\n💾 Save session log? (y/n): ").strip().lower()
                if save_log == 'y':
                    log_path = f"session_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(log_path, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"✅ Log saved to: {log_path}")
            else:
                print("❌ No objective provided")
                
        elif choice == "2":
            print()
            result = computer.operate_with_voice()
            
            if result.get("iterations", 0) > 0:
                save_log = input("\n💾 Save session log? (y/n): ").strip().lower()
                if save_log == 'y':
                    log_path = f"session_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(log_path, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"✅ Log saved to: {log_path}")
        
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
