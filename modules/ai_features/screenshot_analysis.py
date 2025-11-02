import os
import subprocess
import platform
import time
from typing import Optional, Dict, Any, Tuple
from google import genai
import base64
import pyautogui


class ScreenshotAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"⚠️ Could not initialize Gemini: {e}")

    def analyze(self, image_path: str, prompt: str = "Describe what you see in this image") -> str:
        if not self.client:
            return "❌ AI Vision not available - GEMINI_API_KEY not set"

        try:
            with open(image_path, "rb") as f:
                image_data = f.read()

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(image_data).decode()}}
                        ]
                    }
                ]
            )

            return response.text or "Could not analyze image"

        except FileNotFoundError:
            return f"❌ Screenshot file not found: {image_path}"
        except Exception as e:
            return f"❌ Error analyzing screenshot: {str(e)}"

    def suggest_improvements(self, image_path: str) -> str:
        prompt = """Analyze this screenshot and suggest 3-5 actionable improvements:

1. **UI/UX Issues**: Buttons, labels, contrast, accessibility
2. **Design & Layout**: Spacing, alignment, colors, fonts
3. **User Experience**: Navigation, feedback, clarity
4. **Content**: Readability, hierarchy
5. **Technical**: Layout issues, overlaps

Format:
**Suggestion 1: [Title]**
- Issue: [What's wrong]
- Fix: [How to improve]
- Impact: [Why it matters]"""

        return self.analyze(image_path, prompt)

    def find_errors(self, image_path: str) -> str:
        prompt = """Look for errors, bugs, or problems:

1. **Visible Errors**: Error messages, warnings, broken images
2. **Layout Problems**: Overlapping elements, cut-off text
3. **Broken Functionality**: Disabled buttons, missing images
4. **Console Errors**: Any visible error messages
5. **Design Bugs**: Missing styles, wrong colors

List each issue with:
- What: The problem
- Where: Location on screen
- Severity: Critical/High/Medium/Low

If no issues: "No visible errors detected ✅" """

        return self.analyze(image_path, prompt)

    def extract_text(self, image_path: str) -> str:
        return self.analyze(image_path, "Extract all visible text from this image. List each piece of text.")

    def analyze_code(self, image_path: str) -> str:
        prompt = """Analyze the code in this screenshot:

1. Programming language
2. What the code does
3. Any bugs or issues
4. Code quality (1-10)
5. Suggestions for improvement

If no code visible: "No code detected" """

        return self.analyze(image_path, prompt)

    def analyze_design(self, image_path: str) -> str:
        prompt = """Analyze the design/UI:

1. Type of design/interface
2. Color scheme and visual style
3. Layout and composition quality
4. Design suggestions

If no design work: "No design detected" """

        return self.analyze(image_path, prompt)

    def get_quick_tips(self, image_path: str) -> str:
        prompt = "Provide 3 quick, actionable tips about what's shown in this screenshot"
        return self.analyze(image_path, prompt)

    def take_screenshot(self, save_path: str = "screenshots/current_screen.png") -> str:
        try:
            # Create screenshots directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)

            return save_path
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
            return ""

    def detect_app_from_screenshot(self, image_path: str) -> Dict[str, Any]:
        if not self.client:
            return {"app_name": "Unknown", "error": "AI not available"}

        prompt = """Analyze this screenshot and identify the application shown.
        
        Provide a JSON-like response with:
        - app_name: The name of the application (e.g., "Chrome", "Notepad", "Calculator", "VS Code")
        - app_type: Type of app (e.g., "browser", "editor", "media_player", "office")
        - is_fullscreen: Is the app currently in fullscreen mode? (true/false)
        - description: Brief description of what's visible
        
        Be concise and accurate."""

        result = self.analyze(image_path, prompt)

        # Parse the result (basic parsing)
        app_info = {
            "app_name": "Unknown",
            "app_type": "unknown",
            "is_fullscreen": False,
            "description": result
        }

        # Try to extract app name from the response
        result_lower = result.lower()

        # Common apps detection
        apps = {
            "chrome": ["chrome", "google chrome"],
            "firefox": ["firefox", "mozilla"],
            "edge": ["edge", "microsoft edge"],
            "notepad": ["notepad"],
            "code": ["vs code", "visual studio code", "vscode"],
            "calculator": ["calculator", "calc"],
            "vlc": ["vlc", "media player"],
            "spotify": ["spotify"],
            "word": ["word", "microsoft word"],
            "excel": ["excel", "microsoft excel"],
            "powerpoint": ["powerpoint", "microsoft powerpoint"],
        }

        for app, keywords in apps.items():
            for keyword in keywords:
                if keyword in result_lower:
                    app_info["app_name"] = app
                    break

        # Check if fullscreen
        if "fullscreen" in result_lower or "full screen" in result_lower:
            app_info["is_fullscreen"] = True

        return app_info

    def open_app_fullscreen(self, app_name: str, force_fullscreen: bool = True) -> str:
        system = platform.system()

        try:
            # App launch commands for different platforms
            if system == "Windows":
                commands = {
                    "chrome": "start chrome",
                    "firefox": "start firefox",
                    "edge": "start msedge",
                    "notepad": "start notepad",
                    "calculator": "start calc",
                    "code": "start code",
                    "word": "start winword",
                    "excel": "start excel",
                    "powerpoint": "start powerpnt",
                    "vlc": "start vlc",
                    "spotify": "start spotify",
                }
            elif system == "Linux":
                commands = {
                    "chrome": "google-chrome &",
                    "firefox": "firefox &",
                    "edge": "microsoft-edge &",
                    "notepad": "gedit &",
                    "calculator": "gnome-calculator &",
                    "code": "code &",
                    "vlc": "vlc &",
                    "spotify": "spotify &",
                }
            elif system == "Darwin":  # macOS
                commands = {
                    "chrome": "open -a 'Google Chrome'",
                    "firefox": "open -a 'Firefox'",
                    "safari": "open -a 'Safari'",
                    "notepad": "open -a 'TextEdit'",
                    "calculator": "open -a 'Calculator'",
                    "code": "open -a 'Visual Studio Code'",
                    "vlc": "open -a 'VLC'",
                    "spotify": "open -a 'Spotify'",
                }
            else:
                return f"❌ Unsupported operating system: {system}"

            # Get the command for the app
            app_lower = app_name.lower()
            command = commands.get(app_lower)

            if not command:
                return f"❌ Unknown application: {app_name}. Supported apps: {', '.join(commands.keys())}"

            # Launch the application
            if system == "Windows":
                subprocess.Popen(command, shell=True)
            else:
                subprocess.Popen(command, shell=True)

            # Wait for app to open
            time.sleep(2)

            # Force fullscreen if requested
            if force_fullscreen:
                self._make_fullscreen(system)

            return f"✅ {app_name} opened successfully" + (" in fullscreen mode" if force_fullscreen else "")

        except Exception as e:
            return f"❌ Error opening {app_name}: {str(e)}"

    def _make_fullscreen(self, system: str):
        try:
            if system == "Windows":
                # F11 for fullscreen in most apps
                pyautogui.press('f11')
            elif system == "Darwin":  # macOS
                # Control+Command+F for fullscreen on macOS
                pyautogui.hotkey('ctrl', 'command', 'f')
            else:  # Linux
                # F11 for fullscreen in most apps
                pyautogui.press('f11')

            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Could not make fullscreen: {e}")

    def analyze_and_open_fullscreen(self, screenshot_path: Optional[str] = None) -> str:
        # Take screenshot if not provided
        if not screenshot_path:
            screenshot_path = self.take_screenshot()
            if not screenshot_path:
                return "❌ Failed to take screenshot"

        # Detect app from screenshot
        app_info = self.detect_app_from_screenshot(screenshot_path)

        if app_info.get("error"):
            return f"❌ {app_info['error']}"

        app_name = app_info.get("app_name", "Unknown")
        is_fullscreen = app_info.get("is_fullscreen", False)

        # Build response message
        message = f"📸 Screenshot analyzed:\n"
        message += f"   App detected: {app_name}\n"
        message += f"   Currently fullscreen: {'Yes' if is_fullscreen else 'No'}\n\n"

        if app_name == "Unknown":
            message += "❌ Could not identify the application"
            return message

        # Open the app in fullscreen
        result = self.open_app_fullscreen(app_name, force_fullscreen=True)
        message += result

        return message

    def ensure_app_fullscreen(self, app_name: str) -> str:
        print(f"🔍 Ensuring {app_name} is open in fullscreen...")

        # Open the app in fullscreen
        result = self.open_app_fullscreen(app_name, force_fullscreen=True)

        # Wait a bit for the app to fully open and go fullscreen
        time.sleep(1)

        return result

    def control_notepad_fullscreen(self) -> str:
        return self.ensure_app_fullscreen("notepad")

    def control_browser_fullscreen(self, browser: str = "chrome") -> str:
        valid_browsers = ["chrome", "firefox", "edge", "safari"]
        if browser.lower() not in valid_browsers:
            return f"❌ Invalid browser. Choose from: {', '.join(valid_browsers)}"

        return self.ensure_app_fullscreen(browser)

    def control_youtube_fullscreen(self, browser: str = "chrome", youtube_url: str = "https://youtube.com") -> str:
        system = platform.system()

        # First ensure browser is in fullscreen
        result = self.ensure_app_fullscreen(browser)

        # Wait for browser to open
        time.sleep(2)

        # Open YouTube URL
        try:
            if system == "Windows":
                subprocess.Popen(f'start {browser} "{youtube_url}"', shell=True)
            elif system == "Darwin":  # macOS
                subprocess.Popen(f'open -a "{browser}" "{youtube_url}"', shell=True)
            else:  # Linux
                subprocess.Popen(f'{browser} "{youtube_url}" &', shell=True)

            return f"{result}\n✅ YouTube opened in {browser} fullscreen mode"
        except Exception as e:
            return f"{result}\n⚠️ Browser opened but couldn't open YouTube: {str(e)}"


def create_screenshot_analyzer() -> ScreenshotAnalyzer:
    return ScreenshotAnalyzer()


# Standalone functions for backward compatibility
def analyze_screenshot(image_path: str, prompt: str = "Describe what you see") -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.analyze(image_path, prompt)


def suggest_improvements(image_path: str) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.suggest_improvements(image_path)


def analyze_screen_for_errors(image_path: str) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.find_errors(image_path)


def get_quick_tips(image_path: str) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.get_quick_tips(image_path)


def analyze_code_on_screen(image_path: str) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.analyze_code(image_path)


def analyze_website_design(image_path: str) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.analyze_design(image_path)


def open_app_in_fullscreen(app_name: str, force_fullscreen: bool = True) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.open_app_fullscreen(app_name, force_fullscreen)


def detect_app_and_open_fullscreen(screenshot_path: Optional[str] = None) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.analyze_and_open_fullscreen(screenshot_path)


def take_current_screenshot(save_path: str = "screenshots/current_screen.png") -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.take_screenshot(save_path)


def control_notepad_fullscreen() -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.control_notepad_fullscreen()


def control_browser_fullscreen(browser: str = "chrome") -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.control_browser_fullscreen(browser)


def control_youtube_fullscreen(browser: str = "chrome", youtube_url: str = "https://youtube.com") -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.control_youtube_fullscreen(browser, youtube_url)


def ensure_app_fullscreen(app_name: str) -> str:
    analyzer = create_screenshot_analyzer()
    return analyzer.ensure_app_fullscreen(app_name)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python screenshot_analysis.py <command> [args]")
        print("\nCommands:")
        print("  analyze <image_path>              - Analyze a screenshot")
        print("  detect-app <image_path>           - Detect app from screenshot")
        print("  open <app_name>                   - Open app in fullscreen")
        print("  auto-open [screenshot_path]       - Auto-detect and open app")
        print("  screenshot [save_path]            - Take a screenshot")
        sys.exit(1)

    command = sys.argv[1].lower()
    analyzer = create_screenshot_analyzer()

    if command == "analyze" and len(sys.argv) > 2:
        result = analyzer.analyze(sys.argv[2])
        print(result)
    elif command == "detect-app" and len(sys.argv) > 2:
        result = analyzer.detect_app_from_screenshot(sys.argv[2])
        print(f"App detected: {result}")
    elif command == "open" and len(sys.argv) > 2:
        result = analyzer.open_app_fullscreen(sys.argv[2])
        print(result)
    elif command == "auto-open":
        screenshot_path = sys.argv[2] if len(sys.argv) > 2 else None
        result = analyzer.analyze_and_open_fullscreen(screenshot_path)
        print(result)
    elif command == "screenshot":
        save_path = sys.argv[2] if len(sys.argv) > 2 else "screenshots/current_screen.png"
        result = analyzer.take_screenshot(save_path)
        print(f"Screenshot saved to: {result}")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

