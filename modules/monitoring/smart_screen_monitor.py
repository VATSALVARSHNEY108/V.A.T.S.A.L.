"""
👁️ Smart Screen Monitor
Continuously monitors your screen with AI Vision and provides intelligent insights
"""

import time
import os
from datetime import datetime
from gui_automation import GUIAutomation
from screenshot_analyzer import analyze_screenshot
from gemini_controller import get_client
from google.genai import types


class SmartScreenMonitor:
    """AI-powered screen monitoring with intelligent analysis"""
    
    def __init__(self):
        """Initialize smart screen monitor"""
        self.gui = GUIAutomation()
        self.monitoring = False
        self.last_screenshot = None
        self.activity_log = []
        print("👁️ Smart Screen Monitor initialized")
    
    def analyze_current_screen(self, focus: str = "general") -> dict:
        """
        Take screenshot and analyze what's on screen
        
        Args:
            focus: What to analyze - 'general', 'errors', 'productivity', 'code', 'design'
        
        Returns:
            Dict with analysis results
        """
        print("\n📸 Taking screenshot of current screen...")
        screenshot_path = self.gui.screenshot("screen_monitor")
        
        if not screenshot_path:
            return {
                "success": False,
                "message": "❌ Screenshot feature not available in cloud environment.\n\n💡 To use AI screen analysis features, download and run VATSAL locally on your Windows/Mac/Linux computer.\n\nCloud-compatible alternatives:\n• Generate code: 'Write Python code for [task]'\n• AI chat: 'Tell me about [topic]'\n• Data analysis: 'Import CSV file [filename]'\n• File operations: 'Create file [name] with content [text]'"
            }
        
        self.last_screenshot = screenshot_path
        
        if focus == "general":
            prompt = """Analyze this screenshot and describe:
1. What application/website is currently visible
2. What the user appears to be doing
3. Any notable elements or content on screen
4. Overall screen activity summary

Be concise and factual."""
        
        elif focus == "errors":
            prompt = """Analyze this screenshot specifically looking for:
1. Error messages or warnings
2. Red text or error indicators
3. Dialog boxes with issues
4. Any problems or alerts visible

If no errors found, say "No errors detected"."""
        
        elif focus == "productivity":
            prompt = """Analyze this screenshot for productivity insights:
1. What task is the user working on?
2. Is this work-related or personal browsing?
3. Any distractions visible (social media, games, etc.)?
4. Productivity score: 1-10 (10 = highly focused work)

Provide brief, actionable insights."""
        
        elif focus == "code":
            prompt = """Analyze this screenshot looking for code:
1. What programming language is visible?
2. What is the code trying to do?
3. Any obvious bugs or issues in the visible code?
4. Code quality assessment (1-10)

If no code visible, say "No code detected"."""
        
        elif focus == "design":
            prompt = """Analyze this screenshot for design/UI elements:
1. What type of design/interface is visible?
2. Color scheme and visual style
3. Layout and composition quality
4. Design suggestions or improvements (if any)

If no design work visible, say "No design detected"."""
        
        else:
            prompt = f"Analyze this screenshot with focus on: {focus}"
        
        print(f"   🤖 Analyzing screen with AI Vision (focus: {focus})...")
        analysis = analyze_screenshot(screenshot_path, prompt)
        
        if analysis:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "focus": focus,
                "analysis": analysis[:200],
                "screenshot": screenshot_path
            }
            self.activity_log.append(log_entry)
            
            return {
                "success": True,
                "analysis": analysis,
                "screenshot": screenshot_path,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "message": "Failed to analyze screenshot"
            }
    
    def analyze_uploaded_screenshot(self, image_path: str, focus: str = "general") -> dict:
        """
        🆕 CLOUD-COMPATIBLE: Analyze an uploaded screenshot file
        
        This works in Replit! Upload your screenshot and get AI analysis.
        
        Args:
            image_path: Path to the uploaded screenshot file
            focus: What to analyze - 'general', 'errors', 'productivity', 'code', 'design'
        
        Returns:
            Dict with analysis results
        """
        print(f"\n📸 Analyzing uploaded screenshot: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            return {
                "success": False,
                "message": f"❌ File not found: {image_path}\n\n💡 Upload your screenshot to the Replit workspace first!"
            }
        
        # Determine analysis prompt based on focus
        if focus == "general":
            prompt = """Analyze this screenshot and describe:
1. What application/website is currently visible
2. What the user appears to be doing
3. Any notable elements or content on screen
4. Overall screen activity summary

Be concise and factual."""
        
        elif focus == "errors":
            prompt = """Analyze this screenshot specifically looking for:
1. Error messages or warnings
2. Red text or error indicators
3. Dialog boxes with issues
4. Any problems or alerts visible

If no errors found, say "No errors detected"."""
        
        elif focus == "productivity":
            prompt = """Analyze this screenshot for productivity insights:
1. What task is the user working on?
2. Is this work-related or personal browsing?
3. Any distractions visible (social media, games, etc.)?
4. Productivity score: 1-10 (10 = highly focused work)

Provide brief, actionable insights."""
        
        elif focus == "code":
            prompt = """Analyze this screenshot looking for code:
1. What programming language is visible?
2. What is the code trying to do?
3. Any obvious bugs or issues in the visible code?
4. Code quality assessment (1-10)

If no code visible, say "No code detected"."""
        
        elif focus == "design":
            prompt = """Analyze this screenshot for design/UI elements:
1. What type of design/interface is visible?
2. Color scheme and visual style
3. Layout and composition quality
4. Design suggestions or improvements (if any)

If no design work visible, say "No design detected"."""
        
        else:
            prompt = f"Analyze this screenshot with focus on: {focus}"
        
        print(f"   🤖 Analyzing with AI Vision (focus: {focus})...")
        analysis = analyze_screenshot(image_path, prompt)
        
        if analysis and not analysis.startswith("Error"):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "focus": focus,
                "analysis": analysis[:200],
                "screenshot": image_path,
                "type": "uploaded"
            }
            self.activity_log.append(log_entry)
            
            return {
                "success": True,
                "analysis": analysis,
                "screenshot": image_path,
                "timestamp": datetime.now().isoformat(),
                "message": "✅ Screenshot analyzed successfully!"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to analyze screenshot: {analysis}"
            }
    
    def detect_screen_changes(self, interval: int = 5, duration: int = 30) -> dict:
        """
        Monitor screen for changes over time
        
        Args:
            interval: Seconds between screenshots
            duration: Total monitoring duration in seconds
        
        Returns:
            Dict with change detection results
        """
        print(f"\n👁️ Starting screen change detection...")
        print(f"   ⏱️  Interval: {interval}s, Duration: {duration}s")
        
        screenshots = []
        iterations = duration // interval
        
        for i in range(iterations):
            print(f"\n   📸 Screenshot {i+1}/{iterations}")
            screenshot_path = self.gui.screenshot(f"monitor_{i}")
            
            if screenshot_path:
                screenshots.append({
                    "path": screenshot_path,
                    "time": datetime.now().isoformat()
                })
            
            if i < iterations - 1:
                print(f"   ⏳ Waiting {interval} seconds...")
                time.sleep(interval)
        
        print("\n   🤖 Analyzing changes with AI...")
        
        if len(screenshots) < 2:
            return {
                "success": False,
                "message": "Not enough screenshots captured"
            }
        
        try:
            client = get_client()
            
            prompt = f"""I took {len(screenshots)} screenshots over {duration} seconds.
Compare them and describe:
1. What changed on screen during this time?
2. What activity was happening?
3. Was the user actively working or idle?
4. Summary of screen activity

First screenshot: {screenshots[0]['time']}
Last screenshot: {screenshots[-1]['time']}"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=500
                )
            )
            
            changes = response.text.strip()
            
            return {
                "success": True,
                "changes": changes,
                "screenshots": len(screenshots),
                "duration": duration
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error analyzing changes: {str(e)}"
            }
    
    def monitor_for_specific_content(self, target: str, check_interval: int = 10, max_checks: int = 6) -> dict:
        """
        Monitor screen until specific content appears
        
        Args:
            target: What to look for (e.g., "error message", "email notification", "code completion")
            check_interval: Seconds between checks
            max_checks: Maximum number of checks before stopping
        
        Returns:
            Dict with detection results
        """
        print(f"\n👁️ Monitoring for: '{target}'")
        print(f"   🔍 Checking every {check_interval}s (max {max_checks} checks)")
        
        for i in range(max_checks):
            print(f"\n   📸 Check {i+1}/{max_checks}")
            screenshot_path = self.gui.screenshot(f"target_monitor_{i}")
            
            if screenshot_path:
                prompt = f"""Look at this screenshot and determine:
Is there any content related to: "{target}"?

Answer with:
- FOUND: [description of what you found]
- NOT FOUND: [brief description of what's on screen instead]"""
                
                print(f"   🤖 Analyzing...")
                analysis = analyze_screenshot(screenshot_path, prompt)
                
                if analysis and "FOUND:" in analysis.upper():
                    return {
                        "success": True,
                        "found": True,
                        "message": f"✅ Target content found!",
                        "details": analysis,
                        "screenshot": screenshot_path,
                        "checks": i + 1
                    }
            
            if i < max_checks - 1:
                print(f"   ⏳ Not found yet, waiting {check_interval}s...")
                time.sleep(check_interval)
        
        return {
            "success": True,
            "found": False,
            "message": f"Target content '{target}' not detected after {max_checks} checks",
            "checks": max_checks
        }
    
    def get_productivity_insights(self) -> dict:
        """
        Analyze current screen for productivity insights
        
        Returns:
            Dict with productivity analysis
        """
        return self.analyze_current_screen(focus="productivity")
    
    def check_for_errors(self) -> dict:
        """
        Scan screen for error messages or issues
        
        Returns:
            Dict with error detection results
        """
        return self.analyze_current_screen(focus="errors")
    
    def analyze_code_on_screen(self) -> dict:
        """
        Analyze any code visible on screen
        
        Returns:
            Dict with code analysis
        """
        return self.analyze_current_screen(focus="code")
    
    def get_activity_log(self) -> list:
        """Get all recorded activity"""
        return self.activity_log
    
    def clear_activity_log(self):
        """Clear activity log"""
        self.activity_log = []
        return {"success": True, "message": "Activity log cleared"}
    
    def smart_screenshot_with_context(self, question: str) -> dict:
        """
        Take screenshot and answer a specific question about it
        
        Args:
            question: Question to answer about the screen
        
        Returns:
            Dict with answer
        """
        print(f"\n📸 Taking screenshot to answer: '{question}'")
        screenshot_path = self.gui.screenshot("context_screenshot")
        
        if not screenshot_path:
            return {
                "success": False,
                "message": "❌ Screenshot feature not available in cloud environment. This feature requires running VATSAL locally on your desktop."
            }
        
        print("   🤖 AI analyzing and answering...")
        answer = analyze_screenshot(screenshot_path, question)
        
        if answer:
            return {
                "success": True,
                "question": question,
                "answer": answer,
                "screenshot": screenshot_path
            }
        else:
            return {
                "success": False,
                "message": "Failed to get answer"
            }


def create_smart_screen_monitor():
    """Factory function to create smart screen monitor"""
    return SmartScreenMonitor()
