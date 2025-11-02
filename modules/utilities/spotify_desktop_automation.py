"""
Spotify Desktop Automation using Keyboard Shortcuts
Controls Spotify desktop app via GUI automation
"""

import time
import platform
from typing import Any

pyautogui: Any = None
PYAUTOGUI_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    print(f"⚠️  PyAutoGUI not available for Spotify automation: {e}")
    print("Spotify desktop automation will run in demo mode")


class SpotifyDesktopAutomation:
    """Control Spotify desktop app using keyboard shortcuts and GUI automation"""
    
    def __init__(self):
        self.demo_mode = not PYAUTOGUI_AVAILABLE
        self.is_windows = platform.system() == "Windows"
        self.is_mac = platform.system() == "Darwin"
        self.is_linux = platform.system() == "Linux"
        
        # Keyboard shortcuts for Spotify
        self.shortcuts = {
            'play_pause': ['space'],
            'next': ['ctrl', 'right'] if not self.is_mac else ['cmd', 'right'],
            'previous': ['ctrl', 'left'] if not self.is_mac else ['cmd', 'left'],
            'volume_up': ['ctrl', 'up'] if not self.is_mac else ['cmd', 'up'],
            'volume_down': ['ctrl', 'down'] if not self.is_mac else ['cmd', 'down'],
            'shuffle': ['ctrl', 's'] if not self.is_mac else ['cmd', 's'],
            'repeat': ['ctrl', 'r'] if not self.is_mac else ['cmd', 'r'],
            'mute': ['ctrl', 'm'] if not self.is_mac else ['cmd', 'm'],
        }
    
    def _press_shortcut(self, shortcut_name):
        """Press a Spotify keyboard shortcut"""
        try:
            if self.demo_mode:
                print(f"  [DEMO] Would press Spotify shortcut: {shortcut_name}")
                return True
                
            keys = self.shortcuts.get(shortcut_name, [])
            if keys:
                pyautogui.hotkey(*keys)
                time.sleep(0.3)
                return True
            return False
        except Exception as e:
            print(f"Error pressing shortcut: {e}")
            return False
    
    def open_spotify(self):
        """Open Spotify application"""
        try:
            if self.is_windows:
                # Try to open Spotify on Windows
                import subprocess
                subprocess.Popen(['spotify.exe'], shell=True)
            elif self.is_mac:
                import subprocess
                subprocess.Popen(['open', '-a', 'Spotify'])
            elif self.is_linux:
                import subprocess
                subprocess.Popen(['spotify'])
            
            time.sleep(2)
            return {"success": True, "message": "🎵 Opening Spotify..."}
        except Exception as e:
            return {"success": False, "message": f"Failed to open Spotify: {str(e)}"}
    
    def play_pause(self):
        """Toggle play/pause"""
        success = self._press_shortcut('play_pause')
        if success:
            return {"success": True, "message": "⏯️ Toggled play/pause"}
        return {"success": False, "message": "Failed to toggle play/pause"}
    
    def pause(self):
        """Pause playback (same as play_pause)"""
        return self.play_pause()
    
    def play(self, uri=None):
        """Play/resume (same as play_pause, ignores URI)"""
        if uri:
            return {"success": False, "message": "Desktop automation doesn't support direct URI playback. Use play_pause instead."}
        return self.play_pause()
    
    def next_track(self):
        """Skip to next track"""
        success = self._press_shortcut('next')
        if success:
            return {"success": True, "message": "⏭️ Next track"}
        return {"success": False, "message": "Failed to skip track"}
    
    def previous_track(self):
        """Go to previous track"""
        success = self._press_shortcut('previous')
        if success:
            return {"success": True, "message": "⏮️ Previous track"}
        return {"success": False, "message": "Failed to go back"}
    
    def volume_up(self, steps=1):
        """Increase volume"""
        for _ in range(steps):
            self._press_shortcut('volume_up')
            time.sleep(0.2)
        return {"success": True, "message": f"🔊 Volume up ({steps} step{'s' if steps > 1 else ''})"}
    
    def volume_down(self, steps=1):
        """Decrease volume"""
        for _ in range(steps):
            self._press_shortcut('volume_down')
            time.sleep(0.2)
        return {"success": True, "message": f"🔉 Volume down ({steps} step{'s' if steps > 1 else ''})"}
    
    def set_volume(self, volume_percent):
        """Set volume approximately (using up/down shortcuts)"""
        # Note: We can't set exact volume with keyboard shortcuts
        # This is a limitation of desktop automation
        return {
            "success": False, 
            "message": f"Desktop mode can't set exact volume. Use 'volume up' or 'volume down' commands instead."
        }
    
    def shuffle(self, state=None):
        """Toggle shuffle mode"""
        success = self._press_shortcut('shuffle')
        if success:
            return {"success": True, "message": "🔀 Toggled shuffle"}
        return {"success": False, "message": "Failed to toggle shuffle"}
    
    def repeat(self, state=None):
        """Toggle repeat mode"""
        success = self._press_shortcut('repeat')
        if success:
            return {"success": True, "message": "🔁 Toggled repeat"}
        return {"success": False, "message": "Failed to toggle repeat"}
    
    def mute(self):
        """Mute/unmute"""
        success = self._press_shortcut('mute')
        if success:
            return {"success": True, "message": "🔇 Toggled mute"}
        return {"success": False, "message": "Failed to toggle mute"}
    
    def search_and_play(self, query):
        """Search for a song and play it using Spotify desktop app"""
        try:
            # Focus on Spotify (if it's already open)
            # Press Ctrl+L to focus on search bar
            search_key = ['ctrl', 'l'] if not self.is_mac else ['cmd', 'l']
            pyautogui.hotkey(*search_key)
            time.sleep(0.5)
            
            # Type the search query
            pyautogui.typewrite(query, interval=0.05)
            time.sleep(1)
            
            # Press Enter to search
            pyautogui.press('enter')
            time.sleep(1)
            
            # Press Enter again to play first result
            pyautogui.press('enter')
            
            return {
                "success": True,
                "message": f"🎵 Searching and playing: {query}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to search: {str(e)}"
            }
    
    def play_track(self, query):
        """Search and play a track"""
        return self.search_and_play(query)
    
    def get_current_track(self):
        """Get current track info - not available in desktop mode"""
        return {
            "success": False,
            "message": "Desktop automation mode cannot read current track info. Check Spotify app directly."
        }
    
    def search(self, query, search_type='track', limit=5):
        """Search - limited in desktop mode"""
        return {
            "success": False,
            "message": f"Desktop mode doesn't support search results. Use 'play [song name]' to search and play directly."
        }
    
    def get_playlists(self, limit=20):
        """Get playlists - not available in desktop mode"""
        return {
            "success": False,
            "message": "Desktop automation mode cannot retrieve playlist info. Open Spotify app to browse playlists."
        }


def create_spotify_desktop_automation():
    """Factory function to create SpotifyDesktopAutomation instance"""
    return SpotifyDesktopAutomation()
