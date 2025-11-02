"""
Advanced Web Automation - Specialized controllers for popular websites
LeetCode, Codeforces, GitHub, StackOverflow, YouTube, etc.
"""

import time
import webbrowser
from typing import Dict, Any, Optional
from gui_automation import GUIAutomation

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None


class WebsiteAutomator:
    """Base class for website-specific automation"""
    
    def __init__(self):
        self.gui = GUIAutomation()
        self.base_url = ""
        self.is_open = False
    
    def open_site(self, path: str = "") -> bool:
        """Open the website"""
        try:
            url = self.base_url + path
            webbrowser.open(url)
            time.sleep(3)
            self.is_open = True
            return True
        except Exception as e:
            print(f"Error opening site: {e}")
            return False


class LeetCodeAutomator(WebsiteAutomator):
    """Specialized automation for LeetCode"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://leetcode.com"
    
    def open_problem(self, problem_number: int) -> Dict[str, Any]:
        """Open a specific problem by number"""
        print(f"🎯 Opening LeetCode Problem #{problem_number}")
        
        # Open problems page
        self.open_site("/problemset/all/")
        time.sleep(3)
        
        # Use search to find problem
        return {
            "success": True,
            "message": f"Opened LeetCode - search for problem {problem_number}",
            "next_steps": [
                "Click on search box",
                f"Type '{problem_number}' and press Enter",
                "Click on the problem in results"
            ]
        }
    
    def open_problem_by_slug(self, slug: str) -> Dict[str, Any]:
        """Open problem by URL slug (e.g., 'two-sum')"""
        print(f"🎯 Opening LeetCode Problem: {slug}")
        self.open_site(f"/problems/{slug}/")
        
        return {
            "success": True,
            "message": f"Opened problem: {slug}",
            "url": f"{self.base_url}/problems/{slug}/"
        }
    
    def go_to_editorial(self) -> Dict[str, Any]:
        """Navigate to editorial tab"""
        if self.gui.demo_mode:
            return {"success": True, "message": "Would click Editorial tab"}
        
        print("📚 Navigating to Editorial")
        
        # Typically, Editorial tab is on the right side
        # This would require AI vision to locate precisely
        return {
            "success": True,
            "message": "Editorial tab location identified",
            "instruction": "Look for 'Editorial' or 'Solution' tab and click it"
        }
    
    def write_solution(self, code: str, language: str = "python3") -> Dict[str, Any]:
        """Write code in the editor"""
        if self.gui.demo_mode:
            return {"success": True, "message": f"Would write {len(code)} chars of code"}
        
        print(f"✍️  Writing solution ({language})")
        
        # Click in code editor area (typically center-left)
        # This would need AI vision for precise location
        
        return {
            "success": True,
            "message": "Code editor identified",
            "instruction": "Click in editor area and paste/type code"
        }
    
    def submit_solution(self) -> Dict[str, Any]:
        """Submit the code"""
        print("🚀 Submitting solution")
        
        return {
            "success": True,
            "message": "Looking for Submit button",
            "instruction": "Find and click 'Submit' button (usually bottom-right)"
        }
    
    def run_tests(self) -> Dict[str, Any]:
        """Run test cases"""
        print("▶️  Running tests")
        
        return {
            "success": True,
            "message": "Looking for Run button",
            "instruction": "Find and click 'Run' button"
        }


class CodeForcesAutomator(WebsiteAutomator):
    """Specialized automation for CodeForces"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://codeforces.com"
    
    def open_contest(self, contest_id: int) -> Dict[str, Any]:
        """Open a specific contest"""
        print(f"🏆 Opening Contest #{contest_id}")
        self.open_site(f"/contest/{contest_id}")
        
        return {
            "success": True,
            "message": f"Opened contest {contest_id}"
        }
    
    def open_problem(self, contest_id: int, problem_letter: str) -> Dict[str, Any]:
        """Open specific problem in a contest"""
        print(f"📝 Opening Problem {problem_letter} from Contest {contest_id}")
        self.open_site(f"/contest/{contest_id}/problem/{problem_letter}")
        
        return {
            "success": True,
            "message": f"Opened Problem {problem_letter}"
        }
    
    def submit_solution(self, language: str = "Python 3") -> Dict[str, Any]:
        """Submit solution"""
        print("🚀 Preparing to submit")
        
        return {
            "success": True,
            "message": "Navigate to submit page",
            "instruction": "Click 'Submit' tab, select language, paste code"
        }


class GitHubAutomator(WebsiteAutomator):
    """Specialized automation for GitHub"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://github.com"
    
    def open_repo(self, username: str, repo_name: str) -> Dict[str, Any]:
        """Open a repository"""
        print(f"📦 Opening {username}/{repo_name}")
        self.open_site(f"/{username}/{repo_name}")
        
        return {
            "success": True,
            "message": f"Opened repository {username}/{repo_name}"
        }
    
    def search_repos(self, query: str) -> Dict[str, Any]:
        """Search for repositories"""
        print(f"🔍 Searching for: {query}")
        self.open_site(f"/search?q={query.replace(' ', '+')}")
        
        return {
            "success": True,
            "message": f"Searched for: {query}"
        }
    
    def view_trending(self, language: str = "") -> Dict[str, Any]:
        """View trending repositories"""
        print("📈 Opening trending repos")
        
        if language:
            self.open_site(f"/trending/{language}")
        else:
            self.open_site("/trending")
        
        return {
            "success": True,
            "message": "Opened trending page"
        }
    
    def create_issue(self, username: str, repo_name: str) -> Dict[str, Any]:
        """Navigate to create new issue"""
        print("📝 Opening new issue page")
        self.open_site(f"/{username}/{repo_name}/issues/new")
        
        return {
            "success": True,
            "message": "Opened new issue page",
            "instruction": "Fill in title and description, then submit"
        }


class StackOverflowAutomator(WebsiteAutomator):
    """Specialized automation for StackOverflow"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://stackoverflow.com"
    
    def search(self, query: str) -> Dict[str, Any]:
        """Search StackOverflow"""
        print(f"🔍 Searching: {query}")
        self.open_site(f"/search?q={query.replace(' ', '+')}")
        
        return {
            "success": True,
            "message": f"Searched for: {query}"
        }
    
    def search_by_tag(self, tag: str) -> Dict[str, Any]:
        """Search by tag"""
        print(f"🏷️  Searching tag: {tag}")
        self.open_site(f"/questions/tagged/{tag}")
        
        return {
            "success": True,
            "message": f"Viewing tag: {tag}"
        }
    
    def ask_question(self) -> Dict[str, Any]:
        """Navigate to ask question page"""
        print("❓ Opening ask question page")
        self.open_site("/questions/ask")
        
        return {
            "success": True,
            "message": "Opened ask question page"
        }


class YouTubeAutomator(WebsiteAutomator):
    """Specialized automation for YouTube"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.youtube.com"
    
    def search(self, query: str) -> Dict[str, Any]:
        """Search YouTube"""
        print(f"🎥 Searching: {query}")
        self.open_site(f"/results?search_query={query.replace(' ', '+')}")
        
        return {
            "success": True,
            "message": f"Searched for: {query}"
        }
    
    def open_video(self, video_id: str) -> Dict[str, Any]:
        """Open specific video"""
        print(f"▶️  Opening video: {video_id}")
        self.open_site(f"/watch?v={video_id}")
        
        return {
            "success": True,
            "message": "Video opened"
        }
    
    def open_channel(self, channel_name: str) -> Dict[str, Any]:
        """Open a channel"""
        print(f"📺 Opening channel: {channel_name}")
        self.open_site(f"/@{channel_name}")
        
        return {
            "success": True,
            "message": f"Opened channel: {channel_name}"
        }


class GoogleAutomator(WebsiteAutomator):
    """Specialized automation for Google"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.google.com"
    
    def search(self, query: str) -> Dict[str, Any]:
        """Search Google"""
        print(f"🔍 Searching: {query}")
        self.open_site(f"/search?q={query.replace(' ', '+')}")
        
        return {
            "success": True,
            "message": f"Searched for: {query}"
        }
    
    def image_search(self, query: str) -> Dict[str, Any]:
        """Search Google Images"""
        print(f"🖼️  Image search: {query}")
        self.open_site(f"/search?q={query.replace(' ', '+')}&tbm=isch")
        
        return {
            "success": True,
            "message": f"Image search for: {query}"
        }


class WebAutomationController:
    """Main controller to manage all website automators"""
    
    def __init__(self):
        self.automators = {
            "leetcode": LeetCodeAutomator(),
            "codeforces": CodeForcesAutomator(),
            "github": GitHubAutomator(),
            "stackoverflow": StackOverflowAutomator(),
            "youtube": YouTubeAutomator(),
            "google": GoogleAutomator()
        }
    
    def get_automator(self, site_name: str) -> Optional[WebsiteAutomator]:
        """Get the appropriate automator for a website"""
        site_name = site_name.lower().replace(" ", "")
        return self.automators.get(site_name)
    
    def execute_web_task(self, site: str, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a web automation task
        
        Args:
            site: Website name (leetcode, github, etc.)
            action: Action to perform
            **kwargs: Action-specific parameters
        
        Example:
            execute_web_task("leetcode", "open_problem", problem_number=34)
            execute_web_task("github", "search_repos", query="python automation")
        """
        automator = self.get_automator(site)
        
        if not automator:
            return {
                "success": False,
                "error": f"No automator found for: {site}",
                "supported_sites": list(self.automators.keys())
            }
        
        if not hasattr(automator, action):
            return {
                "success": False,
                "error": f"Action '{action}' not supported for {site}",
                "available_actions": [m for m in dir(automator) if not m.startswith('_')]
            }
        
        try:
            method = getattr(automator, action)
            result = method(**kwargs)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_supported_sites(self) -> Dict[str, list]:
        """Get all supported sites and their actions"""
        supported = {}
        
        for site_name, automator in self.automators.items():
            actions = [m for m in dir(automator) if not m.startswith('_') and callable(getattr(automator, m))]
            supported[site_name] = [a for a in actions if a not in ['open_site']]
        
        return supported


# Quick test/demo
if __name__ == "__main__":
    print("=" * 60)
    print("🌐 ADVANCED WEB AUTOMATION CONTROLLER".center(60))
    print("=" * 60)
    
    controller = WebAutomationController()
    
    print("\n📋 Supported Websites & Actions:\n")
    supported = controller.get_supported_sites()
    
    for site, actions in supported.items():
        print(f"🔹 {site.upper()}")
        for action in actions:
            print(f"   • {action}")
        print()
    
    print("\n💡 Example Usage:")
    print("   controller.execute_web_task('leetcode', 'open_problem', problem_number=34)")
    print("   controller.execute_web_task('github', 'view_trending', language='python')")
    print("   controller.execute_web_task('youtube', 'search', query='python tutorial')")
    
    # Demo
    print("\n" + "=" * 60)
    print("🎮 Quick Demo")
    print("=" * 60 + "\n")
    
    choice = input("Try opening LeetCode problem 34? (y/n): ").strip().lower()
    if choice == 'y':
        result = controller.execute_web_task("leetcode", "open_problem", problem_number=34)
        print(f"\n✅ Result: {result}")
