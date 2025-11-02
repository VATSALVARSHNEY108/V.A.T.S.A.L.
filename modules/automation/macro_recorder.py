"""
🎬 Automation Recording & Macro System
======================================
Record, replay, and manage desktop automation macros for VATSAL.

Features:
- Record mouse clicks, movements, and keyboard actions
- Playback recorded sequences with accurate timing
- Save/load macros to files
- Pre-built templates for common tasks
- Loop support for repeated playback
- Macro management and organization
"""

import json
import time
import os
import threading
from datetime import datetime
from typing import List, Dict, Optional, Callable

try:
    from pynput import keyboard, mouse
    from pynput.keyboard import Key, KeyCode
    from pynput.mouse import Button
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("⚠️ pynput not available - macro recording limited")

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    PYAUTOGUI_AVAILABLE = False
    print(f"⚠️ PyAutoGUI not available: {e}")


class MacroRecorder:
    """
    Advanced macro recorder for desktop automation.
    Records mouse and keyboard events with precise timing.
    """
    
    def __init__(self):
        self.events = []
        self.start_time = None
        self.is_recording = False
        self.is_playing = False
        self.recording_thread = None
        self.playback_thread = None
        self.stop_requested = False
        
        # Controllers for playback
        if PYNPUT_AVAILABLE:
            self.mouse_controller = mouse.Controller()
            self.keyboard_controller = keyboard.Controller()
        
        # Callbacks
        self.on_event_callback = None
        self.on_complete_callback = None
        
        # Storage
        self.macros_dir = "macros"
        os.makedirs(self.macros_dir, exist_ok=True)
    
    def start_recording(self, callback: Optional[Callable] = None):
        """Start recording user actions"""
        if not PYNPUT_AVAILABLE:
            return "Error: pynput library not available"
        
        if self.is_recording:
            return "Already recording"
        
        self.events = []
        self.is_recording = True
        self.stop_requested = False
        self.on_event_callback = callback
        
        def record_thread():
            self.start_time = time.time()
            
            # Create listeners
            mouse_listener = mouse.Listener(
                on_move=self._on_move,
                on_click=self._on_click,
                on_scroll=self._on_scroll
            )
            
            keyboard_listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            
            # Start listening
            mouse_listener.start()
            keyboard_listener.start()
            
            # Wait for stop signal
            while self.is_recording and not self.stop_requested:
                time.sleep(0.1)
            
            # Stop listeners
            mouse_listener.stop()
            keyboard_listener.stop()
            
            self.is_recording = False
        
        self.recording_thread = threading.Thread(target=record_thread, daemon=True)
        self.recording_thread.start()
        
        return f"🔴 Recording started ({len(self.events)} events)"
    
    def stop_recording(self, name: str = None) -> str:
        """Stop recording and optionally save"""
        if not self.is_recording:
            return "Not currently recording"
        
        self.is_recording = False
        self.stop_requested = True
        
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        
        result = f"✅ Recording stopped ({len(self.events)} events)"
        
        if name:
            filename = self.save_macro(name)
            result += f"\n💾 Saved as: {filename}"
        
        return result
    
    def play_macro(self, macro_name: str = None, macro_data: List[Dict] = None, 
                   repeat: int = 1, speed: float = 1.0, callback: Optional[Callable] = None) -> str:
        """
        Play back a recorded macro
        
        Args:
            macro_name: Name of saved macro to play
            macro_data: Direct macro data to play
            repeat: Number of times to repeat
            speed: Playback speed (1.0 = normal, 2.0 = 2x faster, 0.5 = half speed)
            callback: Function to call on completion
        """
        if not PYNPUT_AVAILABLE and not PYAUTOGUI_AVAILABLE:
            return "Error: No automation library available"
        
        if self.is_playing:
            return "Already playing a macro"
        
        # Load macro data
        if macro_name:
            macro_data = self.load_macro(macro_name)
            if not macro_data:
                return f"Error: Macro '{macro_name}' not found"
        
        if not macro_data:
            if not self.events:
                return "Error: No macro data to play"
            macro_data = self.events
        
        self.is_playing = True
        self.stop_requested = False
        self.on_complete_callback = callback
        
        def playback_thread():
            try:
                for iteration in range(repeat):
                    if self.stop_requested:
                        break
                    
                    start_time = time.time()
                    
                    for event in macro_data:
                        if self.stop_requested:
                            break
                        
                        # Wait for correct timing
                        target_time = event['time'] / speed
                        while time.time() - start_time < target_time:
                            time.sleep(0.001)
                        
                        # Execute event
                        self._execute_event(event)
                    
                    if repeat > 1 and iteration < repeat - 1:
                        time.sleep(0.5)  # Brief pause between repeats
                
                self.is_playing = False
                
                if self.on_complete_callback:
                    self.on_complete_callback(f"✅ Playback complete ({len(macro_data)} events, {repeat}x)")
            
            except Exception as e:
                self.is_playing = False
                if self.on_complete_callback:
                    self.on_complete_callback(f"❌ Playback error: {str(e)}")
        
        self.playback_thread = threading.Thread(target=playback_thread, daemon=True)
        self.playback_thread.start()
        
        return f"▶️ Playing macro ({len(macro_data)} events, {repeat}x at {speed}x speed)"
    
    def stop_playback(self) -> str:
        """Stop current macro playback"""
        if not self.is_playing:
            return "No macro currently playing"
        
        self.stop_requested = True
        self.is_playing = False
        
        if self.playback_thread:
            self.playback_thread.join(timeout=2)
        
        return "⏹️ Playback stopped"
    
    def save_macro(self, name: str, description: str = "") -> str:
        """Save current macro to file"""
        if not self.events:
            return None
        
        filename = os.path.join(self.macros_dir, f"{name}.json")
        
        macro_data = {
            'name': name,
            'description': description,
            'created': datetime.now().isoformat(),
            'event_count': len(self.events),
            'duration': self.events[-1]['time'] if self.events else 0,
            'events': self.events
        }
        
        with open(filename, 'w') as f:
            json.dump(macro_data, f, indent=2)
        
        return filename
    
    def load_macro(self, name: str) -> Optional[List[Dict]]:
        """Load macro from file"""
        filename = os.path.join(self.macros_dir, f"{name}.json")
        
        if not os.path.exists(filename):
            return None
        
        try:
            with open(filename, 'r') as f:
                macro_data = json.load(f)
            return macro_data.get('events', [])
        except Exception as e:
            print(f"Error loading macro: {e}")
            return None
    
    def list_macros(self) -> List[Dict]:
        """List all saved macros"""
        macros = []
        
        for filename in os.listdir(self.macros_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.macros_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    macros.append({
                        'name': data.get('name', filename[:-5]),
                        'description': data.get('description', ''),
                        'created': data.get('created', ''),
                        'event_count': data.get('event_count', 0),
                        'duration': data.get('duration', 0),
                        'filename': filename
                    })
                except:
                    pass
        
        return sorted(macros, key=lambda x: x.get('created', ''), reverse=True)
    
    def delete_macro(self, name: str) -> str:
        """Delete a saved macro"""
        filename = os.path.join(self.macros_dir, f"{name}.json")
        
        if not os.path.exists(filename):
            return f"Macro '{name}' not found"
        
        os.remove(filename)
        return f"✅ Deleted macro: {name}"
    
    # Event recording callbacks
    def _on_move(self, x, y):
        """Record mouse movement"""
        if not self.is_recording or not self.start_time:
            return
        
        # Skip excessive move events (record every 100ms max)
        if self.events and self.events[-1]['type'] == 'move':
            if time.time() - self.start_time - self.events[-1]['time'] < 0.1:
                return
        
        event = {
            'type': 'move',
            'time': time.time() - self.start_time,
            'x': x,
            'y': y
        }
        self.events.append(event)
        
        if self.on_event_callback:
            self.on_event_callback(event)
    
    def _on_click(self, x, y, button, pressed):
        """Record mouse click"""
        if not self.is_recording or not self.start_time:
            return
        
        event = {
            'type': 'click',
            'time': time.time() - self.start_time,
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed
        }
        self.events.append(event)
        
        if self.on_event_callback:
            self.on_event_callback(event)
    
    def _on_scroll(self, x, y, dx, dy):
        """Record mouse scroll"""
        if not self.is_recording or not self.start_time:
            return
        
        event = {
            'type': 'scroll',
            'time': time.time() - self.start_time,
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy
        }
        self.events.append(event)
        
        if self.on_event_callback:
            self.on_event_callback(event)
    
    def _on_press(self, key):
        """Record key press"""
        if not self.is_recording or not self.start_time:
            return
        
        event = {
            'type': 'key_press',
            'time': time.time() - self.start_time,
            'key': str(key)
        }
        self.events.append(event)
        
        if self.on_event_callback:
            self.on_event_callback(event)
    
    def _on_release(self, key):
        """Record key release"""
        if not self.is_recording or not self.start_time:
            return
        
        event = {
            'type': 'key_release',
            'time': time.time() - self.start_time,
            'key': str(key)
        }
        self.events.append(event)
        
        if self.on_event_callback:
            self.on_event_callback(event)
    
    # Event playback
    def _execute_event(self, event: Dict):
        """Execute a single macro event"""
        try:
            event_type = event['type']
            
            if event_type == 'move':
                if PYNPUT_AVAILABLE:
                    self.mouse_controller.position = (event['x'], event['y'])
                elif PYAUTOGUI_AVAILABLE:
                    pyautogui.moveTo(event['x'], event['y'], duration=0)
            
            elif event_type == 'click':
                if PYNPUT_AVAILABLE:
                    self.mouse_controller.position = (event['x'], event['y'])
                    button = Button.left if 'left' in event['button'] else Button.right
                    if event['pressed']:
                        self.mouse_controller.press(button)
                    else:
                        self.mouse_controller.release(button)
                elif PYAUTOGUI_AVAILABLE:
                    if event['pressed']:
                        button_str = 'left' if 'left' in event['button'] else 'right'
                        pyautogui.click(event['x'], event['y'], button=button_str)
            
            elif event_type == 'scroll':
                if PYNPUT_AVAILABLE:
                    self.mouse_controller.scroll(event['dx'], event['dy'])
                elif PYAUTOGUI_AVAILABLE:
                    pyautogui.scroll(event['dy'], event['x'], event['y'])
            
            elif event_type in ['key_press', 'key_release']:
                key = self._parse_key(event['key'])
                if key and PYNPUT_AVAILABLE:
                    if event_type == 'key_press':
                        self.keyboard_controller.press(key)
                    else:
                        self.keyboard_controller.release(key)
                elif key and PYAUTOGUI_AVAILABLE and event_type == 'key_press':
                    # PyAutoGUI doesn't have separate press/release
                    pyautogui.press(str(key))
        
        except Exception as e:
            print(f"Error executing event: {e}")
    
    def _parse_key(self, key_str: str):
        """Convert key string back to key object"""
        try:
            if not PYNPUT_AVAILABLE:
                # Return string for PyAutoGUI
                return key_str.replace('Key.', '').replace("'", "")
            
            # Parse for pynput
            if key_str.startswith('Key.'):
                key_name = key_str.split('.')[1]
                return getattr(Key, key_name, None)
            elif key_str.startswith("'") and key_str.endswith("'"):
                return KeyCode.from_char(key_str[1:-1])
            else:
                return KeyCode.from_char(key_str)
        except:
            return None


class MacroTemplates:
    """Pre-built automation templates for common tasks"""
    
    @staticmethod
    def get_templates() -> Dict[str, Dict]:
        """Get all available templates"""
        return {
            'click_sequence': {
                'name': 'Multi-Click Sequence',
                'description': 'Click multiple locations in sequence',
                'category': 'Basic',
                'generator': MacroTemplates.generate_click_sequence
            },
            'form_fill': {
                'name': 'Form Auto-Fill',
                'description': 'Type text in multiple fields',
                'category': 'Productivity',
                'generator': MacroTemplates.generate_form_fill
            },
            'screenshot_capture': {
                'name': 'Screenshot Capture',
                'description': 'Capture screenshots at intervals',
                'category': 'Utility',
                'generator': MacroTemplates.generate_screenshot_sequence
            },
            'window_switch': {
                'name': 'Window Switcher',
                'description': 'Alt+Tab through windows',
                'category': 'Navigation',
                'generator': MacroTemplates.generate_window_switch
            }
        }
    
    @staticmethod
    def generate_click_sequence(positions: List[tuple], delay: float = 1.0) -> List[Dict]:
        """Generate macro for clicking multiple positions"""
        events = []
        current_time = 0
        
        for x, y in positions:
            # Move
            events.append({
                'type': 'move',
                'time': current_time,
                'x': x,
                'y': y
            })
            current_time += 0.2
            
            # Click press
            events.append({
                'type': 'click',
                'time': current_time,
                'x': x,
                'y': y,
                'button': 'Button.left',
                'pressed': True
            })
            current_time += 0.1
            
            # Click release
            events.append({
                'type': 'click',
                'time': current_time,
                'x': x,
                'y': y,
                'button': 'Button.left',
                'pressed': False
            })
            current_time += delay
        
        return events
    
    @staticmethod
    def generate_form_fill(fields: List[tuple]) -> List[Dict]:
        """Generate macro for filling form fields (position, text, tab_after)"""
        events = []
        current_time = 0
        
        for x, y, text, tab_after in fields:
            # Click field
            events.append({'type': 'move', 'time': current_time, 'x': x, 'y': y})
            current_time += 0.2
            events.append({'type': 'click', 'time': current_time, 'x': x, 'y': y, 
                          'button': 'Button.left', 'pressed': True})
            current_time += 0.1
            events.append({'type': 'click', 'time': current_time, 'x': x, 'y': y, 
                          'button': 'Button.left', 'pressed': False})
            current_time += 0.3
            
            # Type text
            for char in text:
                events.append({'type': 'key_press', 'time': current_time, 'key': f"'{char}'"})
                current_time += 0.05
                events.append({'type': 'key_release', 'time': current_time, 'key': f"'{char}'"})
                current_time += 0.05
            
            # Tab to next field
            if tab_after:
                current_time += 0.2
                events.append({'type': 'key_press', 'time': current_time, 'key': 'Key.tab'})
                current_time += 0.1
                events.append({'type': 'key_release', 'time': current_time, 'key': 'Key.tab'})
                current_time += 0.3
        
        return events
    
    @staticmethod
    def generate_screenshot_sequence(count: int = 5, interval: float = 2.0) -> List[Dict]:
        """Generate macro for taking screenshots"""
        events = []
        current_time = 0
        
        for i in range(count):
            # Press Win+PrintScreen
            events.append({'type': 'key_press', 'time': current_time, 'key': 'Key.cmd'})
            current_time += 0.1
            events.append({'type': 'key_press', 'time': current_time, 'key': 'Key.print_screen'})
            current_time += 0.1
            events.append({'type': 'key_release', 'time': current_time, 'key': 'Key.print_screen'})
            current_time += 0.1
            events.append({'type': 'key_release', 'time': current_time, 'key': 'Key.cmd'})
            current_time += interval
        
        return events
    
    @staticmethod
    def generate_window_switch(switches: int = 3) -> List[Dict]:
        """Generate macro for Alt+Tab window switching"""
        events = []
        current_time = 0
        
        # Hold Alt
        events.append({'type': 'key_press', 'time': current_time, 'key': 'Key.alt'})
        current_time += 0.2
        
        for i in range(switches):
            # Press Tab
            events.append({'type': 'key_press', 'time': current_time, 'key': 'Key.tab'})
            current_time += 0.1
            events.append({'type': 'key_release', 'time': current_time, 'key': 'Key.tab'})
            current_time += 0.5
        
        # Release Alt
        events.append({'type': 'key_release', 'time': current_time, 'key': 'Key.alt'})
        
        return events


# Global instance
macro_recorder = MacroRecorder()
macro_templates = MacroTemplates()


if __name__ == '__main__':
    print("🎬 VATSAL Macro Recorder")
    print("=" * 50)
    print(f"pynput available: {PYNPUT_AVAILABLE}")
    print(f"PyAutoGUI available: {PYAUTOGUI_AVAILABLE}")
    print()
    
    if PYNPUT_AVAILABLE:
        print("Commands:")
        print("  1. Record macro")
        print("  2. Play last recording")
        print("  3. List macros")
        print("  4. Play saved macro")
        print("  5. Exit")
        print()
        
        while True:
            choice = input("Select option: ").strip()
            
            if choice == '1':
                print(macro_recorder.start_recording())
                input("Press ENTER to stop recording...")
                print(macro_recorder.stop_recording())
                name = input("Save as (leave empty to skip): ").strip()
                if name:
                    macro_recorder.save_macro(name)
                    print(f"Saved as '{name}'")
            
            elif choice == '2':
                if macro_recorder.events:
                    print(macro_recorder.play_macro())
                    time.sleep(2)
                else:
                    print("No recording available")
            
            elif choice == '3':
                macros = macro_recorder.list_macros()
                if macros:
                    print("\nSaved Macros:")
                    for m in macros:
                        print(f"  - {m['name']}: {m['event_count']} events, {m['duration']:.1f}s")
                else:
                    print("No saved macros")
            
            elif choice == '4':
                name = input("Macro name: ").strip()
                print(macro_recorder.play_macro(macro_name=name))
                time.sleep(2)
            
            elif choice == '5':
                break
    else:
        print("⚠️ pynput not available - recording disabled")
