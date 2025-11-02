"""
AI Screen Analyzer & Suggester
Takes a screenshot and provides AI-powered improvement suggestions
"""

import os
from datetime import datetime

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    print(f"⚠️  PyAutoGUI not available: {e}")
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False

from screenshot_analyzer import (
    suggest_improvements,
    analyze_screen_for_errors,
    get_quick_tips,
    analyze_code_on_screen,
    analyze_website_design
)


class ScreenSuggester:
    """Automatically take screenshots and get AI suggestions"""
    
    def __init__(self):
        """Initialize screen suggester"""
        self.screenshots_dir = "screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        print("🤖 AI Screen Suggester ready!")
    
    def take_screenshot(self):
        """
        Take a screenshot and save it.
        
        Returns:
            Path to the screenshot file
        """
        if not PYAUTOGUI_AVAILABLE:
            print(f"  ❌ Screenshot not available in this environment")
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            print(f"  📸 Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"  ❌ Demo mode: Cannot take screenshot ({str(e)})")
            return None
    
    def analyze_and_suggest(self) -> str:
        """
        Take screenshot and get AI improvement suggestions.
        
        Returns:
            AI suggestions as text
        """
        print("\n🔍 Analyzing your screen...")
        
        # Take screenshot
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return "❌ Could not take screenshot (demo mode)"
        
        # Get AI suggestions
        print("  🤖 AI is analyzing the screen...")
        suggestions = suggest_improvements(screenshot_path)
        
        return f"\n📋 AI SUGGESTIONS:\n\n{suggestions}\n\n📸 Screenshot: {screenshot_path}"
    
    def check_for_errors(self) -> str:
        """
        Take screenshot and check for visible errors.
        
        Returns:
            List of detected issues
        """
        print("\n🔍 Checking screen for errors...")
        
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return "❌ Could not take screenshot (demo mode)"
        
        print("  🤖 AI is checking for errors...")
        errors = analyze_screen_for_errors(screenshot_path)
        
        return f"\n🐛 ERROR CHECK:\n\n{errors}\n\n📸 Screenshot: {screenshot_path}"
    
    def get_quick_tips(self) -> str:
        """
        Take screenshot and get 3 quick tips.
        
        Returns:
            Quick actionable tips
        """
        print("\n💡 Getting quick tips...")
        
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return "❌ Could not take screenshot (demo mode)"
        
        print("  🤖 AI is generating tips...")
        tips = get_quick_tips(screenshot_path)
        
        return f"\n💡 QUICK TIPS:\n\n{tips}\n\n📸 Screenshot: {screenshot_path}"
    
    def analyze_code(self) -> str:
        """
        Analyze code visible on screen.
        
        Returns:
            Code analysis and suggestions
        """
        print("\n💻 Analyzing code on screen...")
        
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return "❌ Could not take screenshot (demo mode)"
        
        print("  🤖 AI is reviewing the code...")
        analysis = analyze_code_on_screen(screenshot_path)
        
        return f"\n💻 CODE ANALYSIS:\n\n{analysis}\n\n📸 Screenshot: {screenshot_path}"
    
    def analyze_website(self) -> str:
        """
        Analyze website design on screen.
        
        Returns:
            Design analysis and recommendations
        """
        print("\n🎨 Analyzing website design...")
        
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return "❌ Could not take screenshot (demo mode)"
        
        print("  🤖 AI is reviewing the design...")
        analysis = analyze_website_design(screenshot_path)
        
        return f"\n🎨 WEBSITE ANALYSIS:\n\n{analysis}\n\n📸 Screenshot: {screenshot_path}"


def create_screen_suggester():
    """Factory function to create ScreenSuggester instance"""
    return ScreenSuggester()


# Quick test functions
def quick_suggest():
    """Quick function: Take screenshot and get suggestions"""
    suggester = ScreenSuggester()
    result = suggester.analyze_and_suggest()
    print(result)
    return result


def quick_check_errors():
    """Quick function: Check for errors on screen"""
    suggester = ScreenSuggester()
    result = suggester.check_for_errors()
    print(result)
    return result


def quick_tips():
    """Quick function: Get quick tips"""
    suggester = ScreenSuggester()
    result = suggester.get_quick_tips()
    print(result)
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("🤖 AI Screen Analyzer & Suggester")
    print("=" * 70)
    
    print("\nChoose an option:")
    print("1. 📋 Get improvement suggestions")
    print("2. 🐛 Check for errors")
    print("3. 💡 Get quick tips")
    print("4. 💻 Analyze code on screen")
    print("5. 🎨 Analyze website design")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    suggester = ScreenSuggester()
    
    if choice == "1":
        result = suggester.analyze_and_suggest()
    elif choice == "2":
        result = suggester.check_for_errors()
    elif choice == "3":
        result = suggester.get_quick_tips()
    elif choice == "4":
        result = suggester.analyze_code()
    elif choice == "5":
        result = suggester.analyze_website()
    else:
        print("❌ Invalid choice!")
        exit()
    
    print(result)
    print("\n" + "=" * 70)
