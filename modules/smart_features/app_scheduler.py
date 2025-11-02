"""
App Scheduler Module
Auto-open apps based on schedule, detect idle time, manage heavy apps
"""

import platform
import subprocess
import psutil
import time
from datetime import datetime, timedelta
import json
import os

class AppScheduler:
    def __init__(self):
        self.os = platform.system()
        self.schedule_file = "app_schedule.json"
        self.load_schedule()
        self.idle_threshold = 300  # 5 minutes
        self.heavy_apps = ["chrome", "firefox", "slack", "teams", "zoom"]
    
    def load_schedule(self):
        """Load app schedule configuration"""
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r') as f:
                self.schedule = json.load(f)
        else:
            self.schedule = {
                "morning_routine": {
                    "enabled": True,
                    "time": "09:00",
                    "apps": ["chrome", "vscode", "slack"]
                },
                "work_start": {
                    "enabled": False,
                    "time": "08:30",
                    "apps": ["outlook", "teams", "excel"]
                }
            }
            self.save_schedule()
    
    def save_schedule(self):
        """Save app schedule configuration"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def add_schedule(self, name, time_str, apps_list):
        """Add a new app schedule"""
        self.schedule[name] = {
            "enabled": True,
            "time": time_str,
            "apps": apps_list
        }
        self.save_schedule()
        return f"✅ Schedule '{name}' created for {time_str}"
    
    def open_apps_at_time(self, time_str, apps):
        """Open specific apps at scheduled time"""
        try:
            opened = []
            for app in apps:
                if self.os == "Windows":
                    subprocess.Popen(app, shell=True)
                elif self.os == "Darwin":
                    subprocess.Popen(["open", "-a", app])
                elif self.os == "Linux":
                    subprocess.Popen([app])
                opened.append(app)
                time.sleep(1)
            
            return f"✅ Opened apps: {', '.join(opened)}"
        except Exception as e:
            return f"❌ Failed to open apps: {str(e)}"
    
    def get_idle_time(self):
        """Get system idle time in seconds"""
        try:
            if self.os == "Windows":
                import ctypes
                class LASTINPUTINFO(ctypes.Structure):
                    _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]
                
                lii = LASTINPUTINFO()
                lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
                ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
                millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
                return millis / 1000.0
            elif self.os == "Linux":
                result = subprocess.run(['xprintidle'], capture_output=True, text=True)
                return int(result.stdout) / 1000.0
            else:
                return 0
        except:
            return 0
    
    def detect_idle_and_close_heavy_apps(self):
        """Detect idle time and close heavy apps"""
        try:
            idle_time = self.get_idle_time()
            
            if idle_time > self.idle_threshold:
                closed = []
                for proc in psutil.process_iter(['name', 'memory_info']):
                    try:
                        proc_name = proc.info['name'].lower()
                        for heavy_app in self.heavy_apps:
                            if heavy_app in proc_name:
                                memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                                if memory_mb > 200:
                                    proc.terminate()
                                    closed.append(f"{proc.info['name']} ({memory_mb:.0f}MB)")
                    except:
                        continue
                
                if closed:
                    return f"✅ Closed heavy apps after {idle_time/60:.1f}min idle:\n" + "\n".join(closed)
                else:
                    return f"ℹ️ System idle for {idle_time/60:.1f}min, no heavy apps to close"
            else:
                return f"ℹ️ System active (idle for {idle_time:.0f}s)"
        except Exception as e:
            return f"❌ Failed to detect idle: {str(e)}"
    
    def get_heavy_apps(self):
        """Get list of currently running heavy apps"""
        try:
            heavy = []
            for proc in psutil.process_iter(['name', 'memory_info', 'cpu_percent']):
                try:
                    memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    cpu = proc.info['cpu_percent']
                    
                    if memory_mb > 200 or cpu > 50:
                        heavy.append({
                            "name": proc.info['name'],
                            "memory_mb": round(memory_mb, 1),
                            "cpu_percent": round(cpu, 1)
                        })
                except:
                    continue
            
            heavy.sort(key=lambda x: x['memory_mb'], reverse=True)
            
            if heavy:
                result = "🔥 Heavy Apps Running:\n"
                for app in heavy[:10]:
                    result += f"  • {app['name']}: {app['memory_mb']}MB, {app['cpu_percent']}% CPU\n"
                return result
            else:
                return "✅ No heavy apps detected"
        except Exception as e:
            return f"❌ Failed to get heavy apps: {str(e)}"
    
    def close_app(self, app_name):
        """Close specific application"""
        try:
            closed = 0
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        closed += 1
                except:
                    continue
            
            if closed > 0:
                return f"✅ Closed {closed} instance(s) of {app_name}"
            else:
                return f"ℹ️ {app_name} is not running"
        except Exception as e:
            return f"❌ Failed to close {app_name}: {str(e)}"
    
    def launch_websites(self, urls):
        """Launch multiple websites at once"""
        try:
            for url in urls:
                if not url.startswith('http'):
                    url = 'https://' + url
                
                if self.os == "Windows":
                    subprocess.Popen(['start', url], shell=True)
                elif self.os == "Darwin":
                    subprocess.Popen(['open', url])
                else:
                    subprocess.Popen(['xdg-open', url])
                time.sleep(0.5)
            
            return f"✅ Opened {len(urls)} website(s)"
        except Exception as e:
            return f"❌ Failed to launch websites: {str(e)}"
    
    def create_morning_routine(self, apps, websites):
        """Create a morning routine with apps and websites"""
        self.schedule["morning_routine"] = {
            "enabled": True,
            "time": "09:00",
            "apps": apps,
            "websites": websites
        }
        self.save_schedule()
        return f"✅ Morning routine created with {len(apps)} apps and {len(websites)} websites"

if __name__ == "__main__":
    scheduler = AppScheduler()
    print("App Scheduler Module - Testing")
    print(scheduler.get_heavy_apps())
