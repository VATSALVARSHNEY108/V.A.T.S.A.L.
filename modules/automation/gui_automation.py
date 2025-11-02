import time
import os
import platform
from typing import Any

pyautogui: Any = None
pyperclip: Any = None
GUI_AVAILABLE = False

try:
    import pyautogui
    import pyperclip
    GUI_AVAILABLE = True
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
except Exception as e:
    GUI_AVAILABLE = False
    print(f"⚠️  GUI automation not available in this environment: {e}")
    print("Running in DEMO MODE - commands will be simulated")

class GUIAutomation:
    """Handles all GUI automation tasks using PyAutoGUI"""
    
    def __init__(self):
        self.demo_mode = not GUI_AVAILABLE
        if GUI_AVAILABLE:
            self.screen_width, self.screen_height = pyautogui.size()
            print(f"📺 Screen size detected: {self.screen_width}x{self.screen_height}")
        else:
            self.screen_width, self.screen_height = 1920, 1080
            print(f"📺 Simulated screen size: {self.screen_width}x{self.screen_height}")
        
        self.system = platform.system()
        self.last_folder_suggestions = []  # Store suggestions for last failed folder operation
    
    def _log_demo(self, action: str):
        """Log demo mode actions"""
        if self.demo_mode:
            print(f"  [DEMO] {action}")
    
    def single_click(self, x: int, y: int) -> bool:
        """Simple single click at position"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would click at ({x}, {y})")
                return True
            
            print(f"  🖱️  Clicking at ({x}, {y})")
            pyautogui.click(x, y)
            return True
        except Exception as e:
            print(f"Error clicking: {e}")
            return False
    
    def double_click(self, x: int, y: int) -> bool:
        """Perform a double-click at position"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would double click at ({x}, {y})")
                return True
            
            print(f"  🖱️  Double click at ({x}, {y})")
            pyautogui.moveTo(x, y, duration=0.15)
            time.sleep(0.1)
            pyautogui.click(x, y, clicks=2, interval=0.1)
            return True
        except Exception as e:
            print(f"Error double clicking: {e}")
            return False
    
    def click_at_position(self, x: int, y: int) -> bool:
        """Single click at a specific position - wrapper for clarity"""
        return self.single_click(x, y)
    
    def get_relative_position(self, width_percent: float, height_percent: float) -> tuple:
        """Get screen position based on percentage of screen size"""
        x = int(self.screen_width * width_percent / 100)
        y = int(self.screen_height * height_percent / 100)
        return (x, y)
    
    def focus_browser_address_bar(self) -> bool:
        """Focus the browser's address bar"""
        try:
            if self.demo_mode:
                self._log_demo("Would focus browser address bar")
                return True
            
            print(f"  🌐 Focusing browser address bar...")
            if self.system == "Darwin":
                pyautogui.hotkey('command', 'l')
            else:
                pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"Error focusing address bar: {e}")
            return False
    
    def activate_window(self) -> bool:
        """Click on the window to activate/focus it"""
        try:
            if self.demo_mode:
                self._log_demo("Would activate window")
                return True
            
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            pyautogui.click(center_x, center_y)
            time.sleep(0.2)
            return True
        except Exception as e:
            print(f"Error activating window: {e}")
            return False
    
    def open_application(self, app_name: str) -> bool:
        """Open an application based on the operating system"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would open application: {app_name}")
                return True
            
            if self.system == "Windows":
                pyautogui.press('win')
                time.sleep(0.5)
                pyautogui.write(app_name, interval=0.1)
                time.sleep(0.5)
                pyautogui.press('enter')
            elif self.system == "Darwin":
                pyautogui.hotkey('command', 'space')
                time.sleep(0.5)
                pyautogui.write(app_name, interval=0.1)
                time.sleep(0.5)
                pyautogui.press('enter')
            elif self.system == "Linux":
                pyautogui.hotkey('alt', 'f2')
                time.sleep(0.5)
                pyautogui.write(app_name, interval=0.1)
                time.sleep(0.5)
                pyautogui.press('enter')
            else:
                return False
            
            return True
        except Exception as e:
            print(f"Error opening application: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """Type text with specified interval between keystrokes"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would type: '{text}'")
                return True
            
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            print(f"Error typing text: {e}")
            return False
    
    def paste_text(self, text: str) -> bool:
        """Paste text using clipboard"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would paste: '{text[:50]}...'")
                return True
            
            pyperclip.copy(text)
            time.sleep(0.1)
            if self.system == "Darwin":
                pyautogui.hotkey('command', 'v')
            else:
                pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            return True
        except Exception as e:
            print(f"Error pasting text: {e}")
            return False
    
    def click(self, x: int | None = None, y: int | None = None, button: str = 'left', clicks: int = 1) -> bool:
        """Click at specified position or current position"""
        try:
            if self.demo_mode:
                if x is not None and y is not None:
                    self._log_demo(f"Would click {button} button at ({x}, {y})")
                else:
                    self._log_demo(f"Would click {button} button at current position")
                return True
            
            if x is not None and y is not None:
                if clicks == 1:
                    return self.single_click(x, y)
                else:
                    pyautogui.click(x, y, button=button, clicks=clicks, interval=0.1)
            else:
                pyautogui.click(button=button, clicks=clicks)
            return True
        except Exception as e:
            print(f"Error clicking: {e}")
            return False
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """Move mouse to specified position"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would move mouse to ({x}, {y})")
                return True
            
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            print(f"Error moving mouse: {e}")
            return False
    
    def press_key(self, key: str, presses: int = 1) -> bool:
        """Press a keyboard key"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would press key: {key} ({presses} time(s))")
                return True
            
            pyautogui.press(key, presses=presses, interval=0.1)
            return True
        except Exception as e:
            print(f"Error pressing key: {e}")
            return False
    
    def hotkey(self, *keys) -> bool:
        """Press a combination of keys"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would press hotkey: {'+'.join(keys)}")
                return True
            
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            print(f"Error with hotkey: {e}")
            return False
    
    def screenshot(self, filename: str = "screenshot.png"):
        """
        Take a screenshot and save it
        
        Args:
            filename: Name/path for the screenshot file
            
        Returns:
            Path to the screenshot file on success, None on failure
        """
        try:
            if self.demo_mode:
                self._log_demo(f"Would take screenshot and save as: {filename}")
                return None
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"Screenshot saved as {filename}")
            return filename
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would copy to clipboard: '{text[:50]}...'")
                return True
            
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False
    
    def paste_from_clipboard(self) -> bool:
        """Paste from clipboard"""
        try:
            if self.demo_mode:
                self._log_demo("Would paste from clipboard")
                return True
            
            if self.system == "Darwin":
                pyautogui.hotkey('command', 'v')
            else:
                pyautogui.hotkey('ctrl', 'v')
            return True
        except Exception as e:
            print(f"Error pasting: {e}")
            return False
    
    def get_mouse_position(self) -> tuple:
        """Get current mouse position"""
        if self.demo_mode:
            return (0, 0)
        return pyautogui.position()
    
    def wait(self, seconds: float) -> bool:
        """Wait for specified seconds"""
        try:
            if self.demo_mode:
                self._log_demo(f"Would wait {seconds} seconds")
                time.sleep(0.1)
                return True
            
            time.sleep(seconds)
            return True
        except Exception as e:
            print(f"Error waiting: {e}")
            return False
    
    def get_desktop_path(self) -> str:
        """Get the path to the user's Desktop folder"""
        home = os.path.expanduser("~")
        
        if self.system == "Windows":
            desktop = os.path.join(home, "Desktop")
        elif self.system == "Darwin":
            desktop = os.path.join(home, "Desktop")
        else:
            desktop_path = os.path.join(home, "Desktop")
            if not os.path.exists(desktop_path):
                desktop = home
            else:
                desktop = desktop_path
        
        return desktop
    
    def find_similar_folders(self, folder_name: str, search_path: str, max_suggestions: int = 5):
        """Find folders with similar names using fuzzy matching"""
        try:
            if not os.path.exists(search_path):
                return []
            
            # Get all folders in the directory
            all_items = os.listdir(search_path)
            folders = [item for item in all_items if os.path.isdir(os.path.join(search_path, item))]
            
            if not folders:
                return []
            
            # Normalize search term
            search_lower = folder_name.lower()
            
            # Calculate similarity scores
            suggestions = []
            for folder in folders:
                folder_lower = folder.lower()
                score = 0
                
                # Exact match (case-insensitive)
                if folder_lower == search_lower:
                    score = 100
                # Contains the search term
                elif search_lower in folder_lower:
                    score = 80
                # Search term contains folder name
                elif folder_lower in search_lower:
                    score = 70
                # First letters match
                elif folder_lower.startswith(search_lower[:3] if len(search_lower) >= 3 else search_lower[0]):
                    score = 60
                # Contains any word from search
                else:
                    search_words = search_lower.split()
                    folder_words = folder_lower.split()
                    common_words = set(search_words) & set(folder_words)
                    if common_words:
                        score = 50
                
                if score > 0:
                    suggestions.append((folder, score))
            
            # Sort by score (highest first) and return top suggestions
            suggestions.sort(key=lambda x: x[1], reverse=True)
            return [folder for folder, score in suggestions[:max_suggestions]]
        
        except Exception as e:
            print(f"Error finding similar folders: {e}")
            return []
    
    def open_folder(self, folder_path: str = None, folder_name: str = None) -> bool:
        """
        Open a folder in the file manager
        
        Args:
            folder_path: Full path to the folder
            folder_name: Name of folder (will search in Desktop, Documents, Downloads, Home)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            target_path = None
            self.last_folder_suggestions = []  # Clear previous suggestions
            
            if folder_path:
                target_path = os.path.expanduser(folder_path)
            elif folder_name:
                home = os.path.expanduser("~")
                desktop = self.get_desktop_path()
                
                search_locations = [
                    desktop,
                    os.path.join(home, "Documents"),
                    os.path.join(home, "Downloads"),
                    home,
                    os.path.join(desktop, folder_name),
                    os.path.join(home, "Documents", folder_name),
                    os.path.join(home, "Downloads", folder_name)
                ]
                
                for location in search_locations:
                    if os.path.exists(location):
                        if location.endswith(folder_name) or os.path.basename(location) == folder_name:
                            target_path = location
                            break
                        elif os.path.isdir(os.path.join(location, folder_name)):
                            target_path = os.path.join(location, folder_name)
                            break
                
                if not target_path:
                    # Find suggestions from Desktop first
                    suggestions = self.find_similar_folders(folder_name, desktop)
                    self.last_folder_suggestions = suggestions
                    
                    print(f"⚠️  Folder '{folder_name}' not found in common locations")
                    if suggestions:
                        print(f"   💡 Similar folders on Desktop: {', '.join(suggestions[:3])}")
                    return False
            else:
                target_path = self.get_desktop_path()
            
            if not os.path.exists(target_path):
                print(f"⚠️  Path does not exist: {target_path}")
                return False
            
            if self.demo_mode:
                self._log_demo(f"Would open folder: {target_path}")
                return True
            
            print(f"📂 Opening folder: {target_path}")
            
            import subprocess
            if self.system == "Windows":
                subprocess.Popen(['explorer', target_path])
            elif self.system == "Darwin":
                subprocess.Popen(['open', target_path])
            else:
                subprocess.Popen(['xdg-open', target_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return True
            
        except Exception as e:
            print(f"Error opening folder: {e}")
            return False
    
    def open_desktop_folder(self, folder_name: str = None) -> bool:
        """
        Open a folder on the Desktop or the Desktop itself
        
        Args:
            folder_name: Name of folder on Desktop (None to open Desktop itself)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            desktop_path = self.get_desktop_path()
            self.last_folder_suggestions = []  # Clear previous suggestions
            
            if folder_name:
                target_path = os.path.join(desktop_path, folder_name)
                if not os.path.exists(target_path):
                    # Find similar folders to suggest
                    suggestions = self.find_similar_folders(folder_name, desktop_path)
                    self.last_folder_suggestions = suggestions
                    
                    print(f"⚠️  Folder '{folder_name}' not found on Desktop")
                    print(f"   Searched: {target_path}")
                    if suggestions:
                        print(f"   💡 Did you mean: {', '.join(suggestions[:3])}")
                    return False
            else:
                target_path = desktop_path
            
            if self.demo_mode:
                self._log_demo(f"Would open Desktop folder: {target_path}")
                return True
            
            print(f"📂 Opening Desktop folder: {target_path}")
            
            import subprocess
            if self.system == "Windows":
                subprocess.Popen(['explorer', target_path])
            elif self.system == "Darwin":
                subprocess.Popen(['open', target_path])
            else:
                subprocess.Popen(['xdg-open', target_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return True
            
        except Exception as e:
            print(f"Error opening Desktop folder: {e}")
            return False
