"""
Productivity Monitor Module
Screen time tracking, distraction blocking, activity logging, smart reminders
"""

import json
import os
import time
import psutil
from datetime import datetime, timedelta
import platform
import subprocess

class ProductivityMonitor:
    def __init__(self):
        # Use shared productivity_data directory
        from pathlib import Path
        self.data_dir = Path(__file__).parent.absolute() / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.activity_log_file = self.data_dir / "activity_log.json"
        self.productivity_config_file = self.data_dir / "productivity_config.json"
        self.screen_time_file = self.data_dir / "screen_time.json"
        
        self.load_activity_log()
        self.load_config()
        self.load_screen_time()
        
        self.distraction_apps = ["chrome", "firefox", "youtube", "facebook", "twitter", "instagram", "reddit", "tiktok"]
        self.productive_apps = ["vscode", "pycharm", "word", "excel", "notion", "sublime"]
    
    def load_activity_log(self):
        """Load activity log"""
        if os.path.exists(self.activity_log_file):
            with open(self.activity_log_file, 'r') as f:
                self.activity_log = json.load(f)
        else:
            self.activity_log = []
    
    def save_activity_log(self):
        """Save activity log"""
        with open(self.activity_log_file, 'w') as f:
            json.dump(self.activity_log, f, indent=2)
    
    def load_config(self):
        """Load productivity configuration"""
        if os.path.exists(self.productivity_config_file):
            with open(self.productivity_config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "block_distractions_enabled": False,
                "block_after_hours": "22:00",
                "reminders": {
                    "water": {"enabled": True, "interval_minutes": 30},
                    "break": {"enabled": True, "interval_minutes": 60},
                    "posture": {"enabled": True, "interval_minutes": 45}
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save productivity configuration"""
        with open(self.productivity_config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_screen_time(self):
        """Load screen time data"""
        if os.path.exists(self.screen_time_file):
            with open(self.screen_time_file, 'r') as f:
                self.screen_time = json.load(f)
        else:
            self.screen_time = {}
    
    def save_screen_time(self):
        """Save screen time data"""
        with open(self.screen_time_file, 'w') as f:
            json.dump(self.screen_time, f, indent=2)
    
    def log_activity(self, activity_type, description):
        """Log an activity"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "description": description
        }
        
        self.activity_log.append(entry)
        
        if len(self.activity_log) > 1000:
            self.activity_log = self.activity_log[-1000:]
        
        self.save_activity_log()
        return f"✅ Activity logged: {description}"
    
    def get_active_window(self):
        """Get currently active window/app"""
        try:
            if platform.system() == "Windows":
                try:
                    import win32gui
                    window = win32gui.GetForegroundWindow()
                    return win32gui.GetWindowText(window)
                except ImportError:
                    return "Windows (win32gui not available)"
            elif platform.system() == "Darwin":
                script = 'tell application "System Events" to get name of first application process whose frontmost is true'
                return subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip()
            elif platform.system() == "Linux":
                return subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname']).decode('utf-8').strip()
        except:
            return "Unknown"
    
    def track_screen_time(self, duration_minutes=60):
        """Track screen time for running apps"""
        print(f"⏱️ Tracking screen time for {duration_minutes} minutes...")
        
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.screen_time:
            self.screen_time[today] = {}
        
        start_time = time.time()
        check_interval = 5
        
        while time.time() - start_time < duration_minutes * 60:
            active_window = self.get_active_window()
            
            if active_window != "Unknown":
                if active_window not in self.screen_time[today]:
                    self.screen_time[today][active_window] = 0
                
                self.screen_time[today][active_window] += check_interval
            
            time.sleep(check_interval)
        
        self.save_screen_time()
        return f"✅ Screen time tracking complete for {duration_minutes} minutes"
    
    def get_screen_time_dashboard(self, days=7):
        """Generate screen time dashboard"""
        try:
            result = f"📊 Screen Time Dashboard (Last {days} days):\n\n"
            
            dates = sorted(self.screen_time.keys(), reverse=True)[:days]
            
            for date in dates:
                day_data = self.screen_time[date]
                total_seconds = sum(day_data.values())
                total_hours = total_seconds / 3600
                
                result += f"📅 {date} - {total_hours:.1f} hours total\n"
                
                sorted_apps = sorted(day_data.items(), key=lambda x: x[1], reverse=True)[:5]
                
                for app, seconds in sorted_apps:
                    hours = seconds / 3600
                    result += f"  • {app}: {hours:.1f}h\n"
                
                result += "\n"
            
            if not dates:
                return "ℹ️ No screen time data available"
            
            return result
        except Exception as e:
            return f"❌ Failed to generate dashboard: {str(e)}"
    
    def block_distractions(self):
        """Block distraction apps"""
        try:
            blocked = []
            
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    for distraction in self.distraction_apps:
                        if distraction in proc_name:
                            proc.terminate()
                            blocked.append(proc.info['name'])
                            break
                except:
                    continue
            
            if blocked:
                return f"✅ Blocked {len(blocked)} distraction(s): {', '.join(set(blocked))}"
            else:
                return "✅ No distractions running"
        except Exception as e:
            return f"❌ Failed to block distractions: {str(e)}"
    
    def enable_focus_mode(self, hours=2):
        """Enable focus mode - block distractions for specified hours"""
        self.config["block_distractions_enabled"] = True
        self.config["focus_until"] = (datetime.now() + timedelta(hours=hours)).isoformat()
        self.save_config()
        
        self.block_distractions()
        
        return f"🎯 Focus mode enabled for {hours} hours. Distractions blocked!"
    
    def disable_focus_mode(self):
        """Disable focus mode"""
        self.config["block_distractions_enabled"] = False
        self.save_config()
        return "✅ Focus mode disabled"
    
    def get_productivity_score(self):
        """Calculate productivity score for today"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            if today not in self.screen_time:
                return "ℹ️ No data for today"
            
            day_data = self.screen_time[today]
            
            productive_time = 0
            distraction_time = 0
            
            for app, seconds in day_data.items():
                app_lower = app.lower()
                
                is_productive = any(prod in app_lower for prod in self.productive_apps)
                is_distraction = any(dist in app_lower for dist in self.distraction_apps)
                
                if is_productive:
                    productive_time += seconds
                elif is_distraction:
                    distraction_time += seconds
            
            total_time = productive_time + distraction_time
            
            if total_time == 0:
                return "ℹ️ Not enough data for today"
            
            score = (productive_time / total_time) * 100
            
            result = f"📈 Productivity Score for Today: {score:.1f}%\n\n"
            result += f"✅ Productive time: {productive_time/3600:.1f} hours\n"
            result += f"⚠️ Distraction time: {distraction_time/3600:.1f} hours\n"
            
            if score >= 70:
                result += "\n🏆 Excellent! Keep up the great work!"
            elif score >= 50:
                result += "\n👍 Good job! Room for improvement."
            else:
                result += "\n💡 Try to minimize distractions."
            
            return result
        except Exception as e:
            return f"❌ Failed to calculate score: {str(e)}"
    
    def send_reminder(self, reminder_type):
        """Send a reminder notification"""
        reminders = {
            "water": "💧 Time to drink water! Stay hydrated.",
            "break": "☕ Take a 5-minute break. Rest your eyes!",
            "posture": "🪑 Check your posture. Sit up straight!",
            "stretch": "🤸 Time to stretch! Move your body.",
            "eyes": "👀 Look away from the screen for 20 seconds."
        }
        
        message = reminders.get(reminder_type, "⏰ Reminder!")
        
        try:
            if platform.system() == "Windows":
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast("Productivity Reminder", message, duration=10)
                except ImportError:
                    print(f"⏰ {message}")
            elif platform.system() == "Darwin":
                subprocess.run(['osascript', '-e', f'display notification "{message}" with title "Productivity Reminder"'])
            elif platform.system() == "Linux":
                subprocess.run(['notify-send', "Productivity Reminder", message])
            
            return f"✅ {message}"
        except:
            return f"ℹ️ {message}"
    
    def generate_daily_summary(self):
        """Generate daily activity summary"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            today_activities = [a for a in self.activity_log if a['timestamp'].startswith(today)]
            
            result = f"📋 Daily Summary for {today}:\n\n"
            result += f"Total activities logged: {len(today_activities)}\n\n"
            
            if today_activities:
                result += "Recent activities:\n"
                for activity in today_activities[-10:]:
                    time = datetime.fromisoformat(activity['timestamp']).strftime("%H:%M")
                    result += f"  [{time}] {activity['description']}\n"
            
            result += "\n" + self.get_productivity_score()
            
            return result
        except Exception as e:
            return f"❌ Failed to generate summary: {str(e)}"

if __name__ == "__main__":
    monitor = ProductivityMonitor()
    print("Productivity Monitor Module - Testing")
    print(monitor.get_screen_time_dashboard())
