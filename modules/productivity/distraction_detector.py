"""
Distraction Detector - Detects when user is off-task and nudges focus
Uses AI to understand context and detect distractions
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import psutil


class DistractionDetector:
    """Detects and manages user distractions with smart nudging"""
    
    def __init__(self, gemini_model=None):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.distraction_log_file = self.data_dir / "distraction_log.json"
        self.gemini = gemini_model
        
        # Distraction categories
        self.distracting_apps = {
            "social": ["facebook", "instagram", "twitter", "tiktok", "snapchat", "whatsapp"],
            "entertainment": ["youtube", "netflix", "spotify", "twitch", "gaming", "steam"],
            "shopping": ["amazon", "ebay", "shopping", "aliexpress"],
            "news": ["reddit", "news", "cnn", "bbc"],
            "messaging": ["slack", "discord", "telegram", "signal"]
        }
        
        self.productive_apps = {
            "coding": ["vscode", "pycharm", "sublime", "atom", "vim", "jupyter"],
            "office": ["word", "excel", "powerpoint", "docs", "sheets", "slides"],
            "design": ["photoshop", "illustrator", "figma", "sketch"],
            "learning": ["coursera", "udemy", "khan", "duolingo"],
            "work": ["zoom", "teams", "meet", "webex"]
        }
        
        # Tracking variables
        self.current_app = None
        self.app_start_time = None
        self.distraction_threshold = 180  # 3 minutes on distracting app
        self.nudge_cooldown = 300  # Don't nudge more than once per 5 minutes
        self.last_nudge_time = None
        
        # Statistics
        self.distractions_today = 0
        self.total_distraction_time = 0
        self.nudges_sent = 0
    
    def check_current_app(self):
        """Check currently active application"""
        try:
            import platform
            
            if platform.system() == "Windows":
                try:
                    import win32gui
                    import win32process
                    
                    hwnd = win32gui.GetForegroundWindow()
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    
                    process = psutil.Process(pid)
                    app_name = process.name().lower().replace(".exe", "")
                    window_title = win32gui.GetWindowText(hwnd)
                    
                    return {
                        "app": app_name,
                        "title": window_title,
                        "pid": pid
                    }
                except:
                    return {"app": "unknown", "title": "", "pid": 0}
            else:
                return {"app": "system", "title": "", "pid": 0}
        except:
            return {"app": "unknown", "title": "", "pid": 0}
    
    def categorize_app(self, app_name):
        """Categorize app as productive or distracting"""
        app_lower = app_name.lower()
        
        # Check if distracting
        for category, apps in self.distracting_apps.items():
            for dist_app in apps:
                if dist_app in app_lower:
                    return {"type": "distracting", "category": category}
        
        # Check if productive
        for category, apps in self.productive_apps.items():
            for prod_app in apps:
                if prod_app in app_lower:
                    return {"type": "productive", "category": category}
        
        return {"type": "neutral", "category": "other"}
    
    def detect_distraction(self):
        """Detect if user is currently distracted"""
        app_info = self.check_current_app()
        categorization = self.categorize_app(app_info["app"])
        
        if categorization["type"] == "distracting":
            # Track time on this app
            if self.current_app != app_info["app"]:
                self.current_app = app_info["app"]
                self.app_start_time = datetime.now()
            
            time_on_app = (datetime.now() - self.app_start_time).total_seconds()
            
            # Check if exceeded threshold
            if time_on_app > self.distraction_threshold:
                severity = "high" if time_on_app > 600 else "medium"
                
                return {
                    "is_distracted": True,
                    "app": app_info["app"],
                    "title": app_info["title"],
                    "category": categorization["category"],
                    "time_on_app": time_on_app,
                    "severity": severity,
                    "should_nudge": self._should_send_nudge()
                }
        else:
            # Reset tracking
            if categorization["type"] == "productive":
                self.current_app = app_info["app"]
                self.app_start_time = datetime.now()
        
        return {
            "is_distracted": False,
            "app": app_info["app"],
            "category": categorization["category"],
            "type": categorization["type"]
        }
    
    def _should_send_nudge(self):
        """Check if enough time has passed since last nudge"""
        if self.last_nudge_time is None:
            return True
        
        time_since_nudge = (datetime.now() - self.last_nudge_time).total_seconds()
        return time_since_nudge > self.nudge_cooldown
    
    def send_nudge(self, distraction_info):
        """Send a focus nudge to user"""
        self.last_nudge_time = datetime.now()
        self.nudges_sent += 1
        
        app = distraction_info["app"]
        category = distraction_info["category"]
        time_on_app = int(distraction_info["time_on_app"])
        
        nudges = {
            "social": [
                f"⚠️ You've been on {app} for {time_on_app}s. Time to refocus!",
                f"🎯 Social media break over! Let's get back to work.",
                f"💪 {time_on_app} seconds on {category}. Ready to be productive?"
            ],
            "entertainment": [
                f"🎬 Entertainment time: {time_on_app}s. Time to switch back to work!",
                f"⏰ {app} can wait. Your goals can't!",
                f"🚀 You've got work to do. Close {app} and refocus!"
            ],
            "shopping": [
                f"🛒 Shopping later! Work now. ({time_on_app}s on {app})",
                f"💳 Your cart can wait. Your productivity can't!"
            ],
            "news": [
                f"📰 News break over! Back to productive work.",
                f"⚠️ {time_on_app}s on news. Time to create, not just consume!"
            ],
            "messaging": [
                f"💬 Messages can wait. You've been chatting for {time_on_app}s!",
                f"📱 Quick check done. Back to focused work!"
            ]
        }
        
        import random
        nudge_list = nudges.get(category, [f"⚠️ Distraction detected on {app}. Time to refocus!"])
        nudge_message = random.choice(nudge_list)
        
        # Log the distraction
        self._log_distraction(distraction_info, nudge_message)
        
        return {
            "nudge": nudge_message,
            "severity": distraction_info["severity"],
            "action": "close_app" if distraction_info["severity"] == "high" else "notify"
        }
    
    def get_ai_insight(self, distraction_info):
        """Get AI-powered insight about distraction pattern"""
        if not self.gemini:
            return "Enable AI for personalized insights"
        
        try:
            prompt = f"""
            User has been distracted on {distraction_info['app']} ({distraction_info['category']}) 
            for {int(distraction_info['time_on_app'])} seconds.
            
            They've had {self.distractions_today} distractions today.
            
            Provide a SHORT (2 sentences max), motivational nudge to help them refocus.
            Be encouraging but firm.
            """
            
            response = self.gemini.generate_content(prompt)
            return response.text.strip()
        except:
            return "Stay focused! You've got important work to do."
    
    def _log_distraction(self, distraction_info, nudge_sent):
        """Log distraction event"""
        try:
            # Load existing log
            log = []
            if self.distraction_log_file.exists():
                with open(self.distraction_log_file, 'r') as f:
                    log = json.load(f)
            
            # Add new entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "app": distraction_info["app"],
                "category": distraction_info["category"],
                "duration": distraction_info["time_on_app"],
                "severity": distraction_info["severity"],
                "nudge_sent": nudge_sent
            }
            
            log.append(entry)
            
            # Keep last 500 entries
            log = log[-500:]
            
            with open(self.distraction_log_file, 'w') as f:
                json.dump(log, f, indent=2)
            
            self.distractions_today += 1
            self.total_distraction_time += distraction_info["time_on_app"]
            
        except Exception as e:
            print(f"Error logging distraction: {e}")
    
    def get_distraction_stats(self, days=7):
        """Get distraction statistics"""
        try:
            if not self.distraction_log_file.exists():
                return {"success": False, "message": "No distraction data"}
            
            with open(self.distraction_log_file, 'r') as f:
                log = json.load(f)
            
            # Filter recent entries
            cutoff = datetime.now() - timedelta(days=days)
            recent = [
                e for e in log
                if datetime.fromisoformat(e["timestamp"]) > cutoff
            ]
            
            # Calculate stats
            total_distractions = len(recent)
            total_time = sum(e["duration"] for e in recent)
            
            # Category breakdown
            categories = {}
            for entry in recent:
                cat = entry["category"]
                if cat not in categories:
                    categories[cat] = {"count": 0, "time": 0}
                categories[cat]["count"] += 1
                categories[cat]["time"] += entry["duration"]
            
            # Most distracting app
            apps = {}
            for entry in recent:
                app = entry["app"]
                if app not in apps:
                    apps[app] = 0
                apps[app] += entry["duration"]
            
            top_app = max(apps.items(), key=lambda x: x[1])[0] if apps else "None"
            
            return {
                "success": True,
                "days": days,
                "total_distractions": total_distractions,
                "total_time_minutes": total_time / 60,
                "avg_distractions_per_day": total_distractions / days,
                "categories": categories,
                "top_distraction": top_app,
                "nudges_sent": self.nudges_sent
            }
            
        except Exception as e:
            return {"success": False, "message": str(e)}


# Singleton instance
_distraction_detector = None

def get_distraction_detector(gemini_model=None):
    """Get or create distraction detector instance"""
    global _distraction_detector
    if _distraction_detector is None:
        _distraction_detector = DistractionDetector(gemini_model)
    return _distraction_detector


if __name__ == "__main__":
    # Test the detector
    detector = get_distraction_detector()
    
    print("Testing Distraction Detector...")
    result = detector.detect_distraction()
    print(f"\nCurrent status: {json.dumps(result, indent=2)}")
    
    if result["is_distracted"] and result["should_nudge"]:
        nudge = detector.send_nudge(result)
        print(f"\nNudge sent: {nudge['nudge']}")
    
    stats = detector.get_distraction_stats()
    print(f"\nStats: {json.dumps(stats, indent=2)}")
