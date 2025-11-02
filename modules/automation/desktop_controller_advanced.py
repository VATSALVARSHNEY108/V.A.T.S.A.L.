"""
🖥️ Advanced Desktop Controller - Complete Desktop Control
Full system control including windows, displays, keyboard macros, and system-wide automation
"""

import psutil
import os
import json
import subprocess
import time
from datetime import datetime

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

class AdvancedDesktopController:
    """Comprehensive desktop control for complete system automation"""
    
    def __init__(self):
        self.macro_file = "desktop_macros.json"
        self.macros = self.load_macros()
        
        # PyAutoGUI safety settings
        if PYAUTOGUI_AVAILABLE and pyautogui:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
    
    def load_macros(self):
        """Load saved macros"""
        if os.path.exists(self.macro_file):
            try:
                with open(self.macro_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_macros(self):
        """Save macros"""
        try:
            with open(self.macro_file, 'w') as f:
                json.dump(self.macros, f, indent=2)
        except:
            pass
    
    # ===== WINDOW MANAGEMENT =====
    
    def list_windows(self):
        """List all open windows and applications"""
        output = "\n" + "="*60 + "\n"
        output += "🪟 OPEN WINDOWS & APPLICATIONS\n"
        output += "="*60 + "\n\n"
        
        try:
            windows = []
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                try:
                    info = proc.info
                    windows.append({
                        'pid': info['pid'],
                        'name': info['name'],
                        'uptime': time.time() - info['create_time']
                    })
                except:
                    pass
            
            # Group by name
            app_counts = {}
            for w in windows:
                name = w['name']
                if name not in app_counts:
                    app_counts[name] = []
                app_counts[name].append(w)
            
            # Display
            for app_name in sorted(app_counts.keys()):
                instances = app_counts[app_name]
                output += f"📱 {app_name} ({len(instances)} instance{'s' if len(instances) > 1 else ''})\n"
                for inst in instances[:3]:  # Show max 3
                    uptime_min = int(inst['uptime'] / 60)
                    output += f"   PID: {inst['pid']} - Running: {uptime_min}m\n"
            
            output += "\n" + "="*60 + "\n"
            output += f"Total Applications: {len(app_counts)}\n"
            output += "="*60 + "\n"
            
        except Exception as e:
            output += f"Error listing windows: {str(e)}\n"
        
        return output
    
    def minimize_window(self, app_name):
        """Minimize a window (platform specific)"""
        try:
            if os.name == 'nt':  # Windows
                import win32gui
                import win32con
                
                def callback(hwnd, hwnds):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if app_name.lower() in title.lower():
                            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                            hwnds.append(hwnd)
                    return True
                
                hwnds = []
                win32gui.EnumWindows(callback, hwnds)
                
                if hwnds:
                    return f"✅ Minimized {len(hwnds)} window(s) for '{app_name}'"
                else:
                    return f"❌ No window found for '{app_name}'"
            else:
                # Linux/Mac - use wmctrl if available
                result = subprocess.run(
                    ['wmctrl', '-r', app_name, '-b', 'add,hidden'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return f"✅ Minimized window '{app_name}'"
                else:
                    return f"❌ Could not minimize '{app_name}'. Install wmctrl for window control."
        except Exception as e:
            return f"Error: {str(e)}\nNote: Install pywin32 (Windows) or wmctrl (Linux) for window management"
    
    def maximize_window(self, app_name):
        """Maximize a window"""
        try:
            if os.name == 'nt':  # Windows
                import win32gui
                import win32con
                
                def callback(hwnd, hwnds):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if app_name.lower() in title.lower():
                            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                            hwnds.append(hwnd)
                    return True
                
                hwnds = []
                win32gui.EnumWindows(callback, hwnds)
                
                if hwnds:
                    return f"✅ Maximized {len(hwnds)} window(s) for '{app_name}'"
                else:
                    return f"❌ No window found for '{app_name}'"
            else:
                result = subprocess.run(
                    ['wmctrl', '-r', app_name, '-b', 'add,maximized_vert,maximized_horz'],
                    capture_output=True
                )
                if result.returncode == 0:
                    return f"✅ Maximized window '{app_name}'"
                else:
                    return f"❌ Could not maximize '{app_name}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def close_window(self, app_name):
        """Close a specific window/application"""
        try:
            killed = 0
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name.lower() in proc.info['name'].lower():
                        proc.kill()
                        killed += 1
                except:
                    pass
            
            if killed > 0:
                return f"✅ Closed {killed} instance(s) of '{app_name}'"
            else:
                return f"❌ No application found matching '{app_name}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def switch_to_window(self, app_name):
        """Switch focus to a specific window"""
        try:
            if os.name == 'nt':  # Windows
                import win32gui
                
                def callback(hwnd, hwnds):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if app_name.lower() in title.lower():
                            win32gui.SetForegroundWindow(hwnd)
                            hwnds.append(hwnd)
                            return False  # Stop after first match
                    return True
                
                hwnds = []
                win32gui.EnumWindows(callback, hwnds)
                
                if hwnds:
                    return f"✅ Switched to '{app_name}'"
                else:
                    return f"❌ Window '{app_name}' not found"
            else:
                result = subprocess.run(
                    ['wmctrl', '-a', app_name],
                    capture_output=True
                )
                if result.returncode == 0:
                    return f"✅ Switched to '{app_name}'"
                else:
                    return f"❌ Could not switch to '{app_name}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ===== DISPLAY CONTROL =====
    
    def get_screen_info(self):
        """Get information about displays/monitors"""
        output = "\n" + "="*60 + "\n"
        output += "🖥️ DISPLAY INFORMATION\n"
        output += "="*60 + "\n\n"
        
        try:
            width, height = pyautogui.size()
            output += f"Primary Screen Resolution: {width}x{height}\n"
            output += f"Current Mouse Position: {pyautogui.position()}\n\n"
            
            # Try to get monitor count (platform specific)
            if os.name == 'nt':
                try:
                    import win32api
                    monitors = win32api.EnumDisplayMonitors()
                    output += f"Number of Monitors: {len(monitors)}\n\n"
                    for i, monitor in enumerate(monitors, 1):
                        output += f"Monitor {i}: {monitor[2]}\n"
                except:
                    output += "Install pywin32 for detailed monitor info\n"
            
            output += "\n" + "="*60 + "\n"
        except Exception as e:
            output += f"Error: {str(e)}\n"
        
        return output
    
    # ===== MACRO RECORDING =====
    
    def record_macro(self, macro_name, duration=10):
        """Record mouse and keyboard actions as a macro"""
        output = f"\n🎬 Recording macro '{macro_name}' for {duration} seconds...\n"
        output += "Move your mouse and perform actions now!\n\n"
        
        try:
            start_time = time.time()
            actions = []
            last_pos = pyautogui.position()
            
            while time.time() - start_time < duration:
                current_pos = pyautogui.position()
                
                # Record mouse movements
                if current_pos != last_pos:
                    actions.append({
                        'type': 'move',
                        'x': current_pos.x,
                        'y': current_pos.y,
                        'time': time.time() - start_time
                    })
                    last_pos = current_pos
                
                time.sleep(0.1)
            
            self.macros[macro_name] = actions
            self.save_macros()
            
            output += f"✅ Macro '{macro_name}' recorded with {len(actions)} actions!\n"
        except Exception as e:
            output += f"Error: {str(e)}\n"
        
        return output
    
    def play_macro(self, macro_name, speed=1.0):
        """Play a recorded macro"""
        if macro_name not in self.macros:
            return f"❌ Macro '{macro_name}' not found"
        
        try:
            actions = self.macros[macro_name]
            start_time = time.time()
            
            for action in actions:
                # Wait for the correct time
                target_time = action['time'] / speed
                while time.time() - start_time < target_time:
                    time.sleep(0.01)
                
                if action['type'] == 'move':
                    pyautogui.moveTo(action['x'], action['y'])
                elif action['type'] == 'click':
                    pyautogui.click()
            
            return f"✅ Macro '{macro_name}' played successfully!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def list_macros(self):
        """List all recorded macros"""
        if not self.macros:
            return "📋 No macros recorded yet."
        
        output = "\n" + "="*60 + "\n"
        output += "🎬 RECORDED MACROS\n"
        output += "="*60 + "\n\n"
        
        for name, actions in self.macros.items():
            duration = actions[-1]['time'] if actions else 0
            output += f"• {name} - {len(actions)} actions, {duration:.1f}s duration\n"
        
        output += "\n" + "="*60 + "\n"
        
        return output
    
    #===== ADVANCED AUTOMATION =====
    
    def create_global_shortcut(self, shortcut_name, keys, action):
        """Create a system-wide keyboard shortcut (requires elevated permissions)"""
        # This is a placeholder - actual implementation requires platform-specific libraries
        return f"💡 Global shortcut feature requires platform-specific setup.\n" \
               f"On Windows: Use pywin32 or pynput\n" \
               f"On Linux: Use python-xlib or pynput\n" \
               f"On Mac: Use pyobjc"
    
    def auto_organize_desktop(self):
        """Automatically organize desktop icons"""
        desktop = os.path.expanduser("~/Desktop")
        
        if not os.path.exists(desktop):
            return "❌ Desktop folder not found"
        
        try:
            files = os.listdir(desktop)
            organized = 0
            
            # Create folders by type
            folders = {
                'Images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.md'],
                'Spreadsheets': ['.xls', '.xlsx', '.csv'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
            }
            
            for filename in files:
                filepath = os.path.join(desktop, filename)
                
                if os.path.isfile(filepath):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    
                    for folder, extensions in folders.items():
                        if ext in extensions:
                            folder_path = os.path.join(desktop, folder)
                            os.makedirs(folder_path, exist_ok=True)
                            
                            new_path = os.path.join(folder_path, filename)
                            os.rename(filepath, new_path)
                            organized += 1
                            break
            
            return f"✅ Organized {organized} file(s) on your desktop!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def take_window_screenshot(self, app_name):
        """Take screenshot of a specific window"""
        try:
            # Switch to window first
            self.switch_to_window(app_name)
            time.sleep(0.5)
            
            # Take screenshot
            filename = f"screenshot_{app_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            return f"✅ Screenshot saved as '{filename}'"
        except Exception as e:
            return f"Error: {str(e)}"
