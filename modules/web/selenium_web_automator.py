"""
Selenium Web Automator - Real browser automation that works in Replit
Full integration with AI task parsing and GUI app
"""

import time
import os
from typing import Dict, Any, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from google import genai
from google.genai import types
import json


class SeleniumWebAutomator:
    """
    Advanced web automation using Selenium - Works in Replit cloud!
    
    Features:
    - Real browser control (Chrome headless)
    - AI-powered task parsing
    - Website-specific automation
    - Smart element detection
    - Screenshot capabilities
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
        
        self.execution_log = []
        
    def _find_chrome_executable(self) -> Optional[str]:
        """Find Chrome executable path on Windows/Linux/Mac"""
        import platform
        import os
        
        system = platform.system()
        
        if system == "Windows":
            # Common Windows Chrome paths
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
                os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
            ]
        elif system == "Darwin":  # macOS
            possible_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            ]
        else:  # Linux
            possible_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser",
            ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def initialize_browser(self) -> bool:
        """Initialize Chrome browser with Selenium"""
        try:
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            chrome_options = Options()
            
            # Find Chrome executable
            chrome_path = self._find_chrome_executable()
            if chrome_path:
                chrome_options.binary_location = chrome_path
                print(f"✅ Found Chrome at: {chrome_path}")
            else:
                print("⚠️ Chrome executable not found")
                print("📥 Please install Google Chrome from: https://www.google.com/chrome/")
                raise FileNotFoundError("Chrome browser not installed. Please install Chrome to use YouTube automation features.")
            
            if self.headless:
                chrome_options.add_argument('--headless=new')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            print("✅ Browser initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Browser initialization failed: {e}")
            print(f"💡 Make sure Chrome is installed on your system")
            print(f"💡 Download Chrome from: https://www.google.com/chrome/")
            return False
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                print("🔒 Browser closed")
            except:
                pass
            self.driver = None
    
    def parse_natural_language_task(self, command: str) -> Dict[str, Any]:
        """Parse complex natural language commands using Gemini AI"""
        if not self.client:
            return self._simple_parse(command)
        
        prompt = f"""
Parse this web automation command into structured steps for Selenium.

Command: "{command}"

Return JSON with executable steps. Be specific about selectors.

Format:
{{
    "task_type": "web_automation",
    "target_website": "leetcode|github|google|youtube|stackoverflow|codeforces",
    "steps": [
        {{
            "action": "navigate|find_click|find_type|wait|scroll|screenshot",
            "target": "URL or element description",
            "selector_hints": "keywords to find element",
            "value": "text to type if applicable",
            "description": "what this does"
        }}
    ]
}}

Examples:
- "open leetcode problem 34" → [{{"action":"navigate","target":"https://leetcode.com"}}, {{"action":"find_click","selector_hints":"search box problems"}}, {{"action":"find_type","value":"34"}},...]
- "search github for python" → [{{"action":"navigate","target":"https://github.com"}}, {{"action":"find_click","selector_hints":"search"}}, ...]

Respond with ONLY valid JSON.
"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            result_text = str(response.candidates[0].content.parts[0].text).strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            parsed = json.loads(result_text.strip())
            return parsed
            
        except Exception as e:
            print(f"AI parsing failed: {e}, using simple parser")
            return self._simple_parse(command)
    
    def _simple_parse(self, command: str) -> Dict[str, Any]:
        """Fallback parser for when AI is unavailable"""
        cmd_lower = command.lower()
        steps = []
        target_website = "unknown"
        
        # Detect website
        if "leetcode" in cmd_lower:
            target_website = "leetcode"
            steps.append({"action": "navigate", "target": "https://leetcode.com", "description": "Open LeetCode"})
        elif "github" in cmd_lower:
            target_website = "github"
            steps.append({"action": "navigate", "target": "https://github.com", "description": "Open GitHub"})
        elif "google" in cmd_lower:
            target_website = "google"
            steps.append({"action": "navigate", "target": "https://google.com", "description": "Open Google"})
        elif "youtube" in cmd_lower:
            target_website = "youtube"
            steps.append({"action": "navigate", "target": "https://youtube.com", "description": "Open YouTube"})
        elif "stackoverflow" in cmd_lower:
            target_website = "stackoverflow"
            steps.append({"action": "navigate", "target": "https://stackoverflow.com", "description": "Open StackOverflow"})
        
        # Add search/type steps based on keywords
        import re
        problem_match = re.search(r'problem\s*#?(\d+)', cmd_lower)
        if problem_match:
            steps.append({
                "action": "find_type",
                "selector_hints": "search input box",
                "value": problem_match.group(1),
                "description": f"Search for problem {problem_match.group(1)}"
            })
        
        if "search" in cmd_lower:
            search_terms = cmd_lower.split("search for")
            if len(search_terms) > 1:
                query = search_terms[1].strip()
                steps.append({
                    "action": "find_type",
                    "selector_hints": "search input",
                    "value": query,
                    "description": f"Search for: {query}"
                })
        
        return {
            "task_type": "web_automation",
            "target_website": target_website,
            "steps": steps
        }
    
    def execute_task(self, command: str, interactive: bool = False) -> Dict[str, Any]:
        """
        Execute a complete automation task from natural language
        
        Args:
            command: Natural language command
            interactive: Whether to pause between steps
        
        Returns:
            Execution results
        """
        print(f"\n🤖 SELENIUM WEB AUTOMATOR")
        print(f"📋 Command: {command}")
        
        # Initialize browser if not already
        if not self.driver:
            if not self.initialize_browser():
                return {"success": False, "error": "Failed to initialize browser"}
        
        # Parse the task
        print(f"⚙️  Parsing task with AI...\n")
        task_plan = self.parse_natural_language_task(command)
        
        print(f"✅ Task Plan:")
        print(f"   Website: {task_plan.get('target_website', 'unknown')}")
        print(f"   Steps: {len(task_plan.get('steps', []))}\n")
        
        # Execute steps
        results = []
        steps = task_plan.get('steps', [])
        
        for i, step in enumerate(steps, 1):
            print(f"Step {i}/{len(steps)}: {step.get('description', 'Unknown')}")
            
            result = self._execute_step(step)
            results.append(result)
            
            if not result.get('success'):
                print(f"   ❌ {result.get('error', 'Failed')}")
                if not interactive:
                    break
            else:
                print(f"   ✅ {result.get('message', 'Done')}")
            
            if interactive and i < len(steps):
                input("   Press Enter to continue...")
            
            time.sleep(1)
        
        success_count = sum(1 for r in results if r.get('success'))
        print(f"\n📊 Complete: {success_count}/{len(results)} steps successful")
        
        return {
            "success": success_count > 0,
            "total_steps": len(results),
            "successful_steps": success_count,
            "results": results
        }
    
    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single automation step"""
        action = step.get('action', '').lower()
        
        try:
            if action == 'navigate':
                url = step.get('target', '')
                self.driver.get(url)
                return {"success": True, "message": f"Navigated to {url}"}
            
            elif action == 'find_click':
                hints = step.get('selector_hints', '')
                element = self._smart_find_element(hints)
                if element:
                    element.click()
                    return {"success": True, "message": f"Clicked: {hints}"}
                return {"success": False, "error": f"Could not find: {hints}"}
            
            elif action == 'find_type':
                hints = step.get('selector_hints', '')
                value = step.get('value', '')
                element = self._smart_find_element(hints)
                if element:
                    element.clear()
                    element.send_keys(value)
                    element.send_keys(Keys.RETURN)
                    return {"success": True, "message": f"Typed: {value}"}
                return {"success": False, "error": f"Could not find input: {hints}"}
            
            elif action == 'wait':
                time.sleep(float(step.get('value', 2)))
                return {"success": True, "message": "Wait completed"}
            
            elif action == 'scroll':
                direction = step.get('value', 'down')
                if direction == 'down':
                    self.driver.execute_script("window.scrollBy(0, 500)")
                else:
                    self.driver.execute_script("window.scrollBy(0, -500)")
                return {"success": True, "message": f"Scrolled {direction}"}
            
            elif action == 'screenshot':
                filename = step.get('value', 'automation_screenshot.png')
                self.driver.save_screenshot(filename)
                return {"success": True, "message": f"Screenshot: {filename}"}
            
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _smart_find_element(self, hints: str):
        """Smart element finder using multiple strategies"""
        # Try multiple selector strategies
        strategies = [
            (By.NAME, hints),
            (By.ID, hints),
            (By.CLASS_NAME, hints),
            (By.LINK_TEXT, hints),
            (By.PARTIAL_LINK_TEXT, hints),
        ]
        
        for by, value in strategies:
            try:
                element = self.driver.find_element(by, value)
                if element.is_displayed():
                    return element
            except:
                continue
        
        # Try XPath with text search
        try:
            elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{hints}')]")
            for elem in elements:
                if elem.is_displayed():
                    return elem
        except:
            pass
        
        # Try CSS selector
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, f"input[placeholder*='{hints}' i]")
            return element
        except:
            pass
        
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, f"button:contains('{hints}')")
            return element
        except:
            pass
        
        return None
    
    # Website-specific methods
    
    def leetcode_open_problem(self, problem_number: int) -> Dict[str, Any]:
        """Open a specific LeetCode problem"""
        if not self.driver:
            self.initialize_browser()
        
        try:
            # Go to LeetCode problemset
            self.driver.get("https://leetcode.com/problemset/all/")
            time.sleep(2)
            
            # Find and click search
            search_box = self._smart_find_element("search")
            if search_box:
                search_box.clear()
                search_box.send_keys(str(problem_number))
                time.sleep(1)
                search_box.send_keys(Keys.RETURN)
                time.sleep(2)
                
                return {"success": True, "message": f"Opened problem {problem_number}"}
            
            return {"success": False, "error": "Could not find search box"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def github_search(self, query: str) -> Dict[str, Any]:
        """Search GitHub"""
        if not self.driver:
            self.initialize_browser()
        
        try:
            self.driver.get(f"https://github.com/search?q={query.replace(' ', '+')}")
            time.sleep(2)
            return {"success": True, "message": f"Searched GitHub for: {query}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def google_search(self, query: str) -> Dict[str, Any]:
        """Search Google"""
        if not self.driver:
            self.initialize_browser()
        
        try:
            self.driver.get("https://www.google.com")
            time.sleep(1)
            
            search_box = self._smart_find_element("q")
            if not search_box:
                search_box = self.driver.find_element(By.NAME, "q")
            
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)
            
            return {"success": True, "message": f"Searched Google for: {query}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def youtube_search(self, query: str) -> Dict[str, Any]:
        """Search YouTube"""
        if not self.driver:
            self.initialize_browser()
        
        try:
            self.driver.get(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            time.sleep(2)
            return {"success": True, "message": f"Searched YouTube for: {query}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_page_title(self) -> str:
        """Get current page title"""
        if self.driver:
            return self.driver.title
        return ""
    
    def get_current_url(self) -> str:
        """Get current URL"""
        if self.driver:
            return self.driver.current_url
        return ""
    
    def take_screenshot(self, filename: str = "screenshot.png") -> bool:
        """Take a screenshot"""
        if self.driver:
            try:
                self.driver.save_screenshot(filename)
                return True
            except:
                return False
        return False


# Quick test function
def demo():
    """Demo the automation system"""
    print("=" * 60)
    print("🌐 SELENIUM WEB AUTOMATOR DEMO".center(60))
    print("=" * 60)
    
    automator = SeleniumWebAutomator()
    
    print("\n💡 Example commands you can try:")
    print("   • 'open leetcode and search for problem 34'")
    print("   • 'search github for python automation'")
    print("   • 'search google for machine learning'")
    print("   • 'search youtube for python tutorials'")
    
    command = input("\n🎯 Enter command (or 'quit' to exit): ").strip()
    
    if command.lower() not in ['quit', 'exit', 'q', '']:
        result = automator.execute_task(command, interactive=True)
        
        if result.get('success'):
            print(f"\n✅ Task completed!")
            print(f"📊 Success rate: {result['successful_steps']}/{result['total_steps']}")
            
            # Keep browser open to see result
            input("\nPress Enter to close browser...")
        else:
            print(f"\n❌ Task failed")
    
    automator.close_browser()


if __name__ == "__main__":
    demo()
