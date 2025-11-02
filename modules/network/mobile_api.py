#!/usr/bin/env python3
"""
Mobile Companion API for VATSAL
Provides REST API endpoints for mobile control
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import io
import base64
from datetime import datetime
import json
import threading
import time
from PIL import Image
import psutil
from pathlib import Path

# Try to import pyautogui, but handle headless environments
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception as e:
    print(f"⚠️  PyAutoGUI not available in this environment: {e}")
    print("📸 Screenshot functionality will be limited in headless mode")
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None

class MobileAPI:
    def __init__(self, command_executor=None):
        self.command_executor = command_executor
        self.screenshot_cache = None
        self.screenshot_lock = threading.Lock()
        self.quick_actions = self._load_quick_actions()
        
    def _load_quick_actions(self):
        """Load predefined quick actions"""
        return {
            'lock_screen': {
                'name': 'Lock Screen',
                'icon': '🔒',
                'command': 'lock screen',
                'category': 'security'
            },
            'shutdown': {
                'name': 'Shutdown',
                'icon': '⚡',
                'command': 'shutdown computer',
                'category': 'power'
            },
            'volume_up': {
                'name': 'Volume Up',
                'icon': '🔊',
                'command': 'increase volume',
                'category': 'media'
            },
            'volume_down': {
                'name': 'Volume Down',
                'icon': '🔉',
                'command': 'decrease volume',
                'category': 'media'
            },
            'mute': {
                'name': 'Mute',
                'icon': '🔇',
                'command': 'mute audio',
                'category': 'media'
            },
            'take_screenshot': {
                'name': 'Screenshot',
                'icon': '📸',
                'command': 'take screenshot',
                'category': 'capture'
            },
            'open_browser': {
                'name': 'Open Browser',
                'icon': '🌐',
                'command': 'open chrome',
                'category': 'apps'
            },
            'play_music': {
                'name': 'Play Music',
                'icon': '🎵',
                'command': 'play spotify',
                'category': 'media'
            },
            'pause_music': {
                'name': 'Pause Music',
                'icon': '⏸️',
                'command': 'pause music',
                'category': 'media'
            },
            'next_track': {
                'name': 'Next Track',
                'icon': '⏭️',
                'command': 'next song',
                'category': 'media'
            },
            'previous_track': {
                'name': 'Previous Track',
                'icon': '⏮️',
                'command': 'previous song',
                'category': 'media'
            },
            'show_weather': {
                'name': 'Weather',
                'icon': '🌤️',
                'command': 'show weather',
                'category': 'info'
            },
            'focus_mode': {
                'name': 'Focus Mode',
                'icon': '🎯',
                'command': 'start focus mode',
                'category': 'productivity'
            },
            'pomodoro_start': {
                'name': 'Start Pomodoro',
                'icon': '⏱️',
                'command': 'start pomodoro',
                'category': 'productivity'
            },
            'sleep_computer': {
                'name': 'Sleep',
                'icon': '💤',
                'command': 'sleep computer',
                'category': 'power'
            },
            'restart': {
                'name': 'Restart',
                'icon': '🔄',
                'command': 'restart computer',
                'category': 'power'
            }
        }
    
    def get_system_status(self):
        """Get current system status"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            battery = None
            
            try:
                battery_info = psutil.sensors_battery()
                if battery_info:
                    battery = {
                        'percent': battery_info.percent,
                        'plugged': battery_info.power_plugged,
                        'time_left': battery_info.secsleft if battery_info.secsleft != -1 else None
                    }
            except:
                pass
            
            return {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': round(cpu, 2),
                    'memory_percent': round(memory.percent, 2),
                    'memory_used_gb': round(memory.used / (1024**3), 2),
                    'memory_total_gb': round(memory.total / (1024**3), 2),
                    'disk_percent': round(disk.percent, 2),
                    'disk_used_gb': round(disk.used / (1024**3), 2),
                    'disk_total_gb': round(disk.total / (1024**3), 2),
                    'battery': battery
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_command(self, command, source='mobile'):
        """Execute a command from mobile"""
        try:
            if not self.command_executor:
                return {
                    'success': False,
                    'error': 'Command executor not available'
                }
            
            result = self.command_executor.execute_command(command)
            
            return {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'command': command,
                'source': source,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': command
            }
    
    def execute_quick_action(self, action_id):
        """Execute a predefined quick action"""
        if action_id not in self.quick_actions:
            return {
                'success': False,
                'error': f'Unknown action: {action_id}'
            }
        
        action = self.quick_actions[action_id]
        return self.execute_command(action['command'], source='mobile_quick_action')
    
    def get_quick_actions(self, category=None):
        """Get available quick actions"""
        actions = self.quick_actions
        
        if category:
            actions = {
                k: v for k, v in actions.items() 
                if v.get('category') == category
            }
        
        return {
            'success': True,
            'actions': actions,
            'categories': list(set(a['category'] for a in self.quick_actions.values()))
        }
    
    def capture_screenshot(self, quality=85, max_width=1920):
        """Capture and compress screenshot for mobile viewing"""
        if not PYAUTOGUI_AVAILABLE:
            return {
                'success': False,
                'error': 'Screenshot functionality not available in headless environment',
                'demo_mode': True
            }
        
        try:
            with self.screenshot_lock:
                screenshot = pyautogui.screenshot()
                
                if screenshot.width > max_width:
                    ratio = max_width / screenshot.width
                    new_height = int(screenshot.height * ratio)
                    screenshot = screenshot.resize((max_width, new_height), Image.LANCZOS)
                
                buffer = io.BytesIO()
                screenshot.save(buffer, format='JPEG', quality=quality, optimize=True)
                buffer.seek(0)
                
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                self.screenshot_cache = {
                    'timestamp': datetime.now().isoformat(),
                    'image': img_base64,
                    'width': screenshot.width,
                    'height': screenshot.height
                }
                
                return {
                    'success': True,
                    'screenshot': self.screenshot_cache
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_cached_screenshot(self):
        """Get the cached screenshot"""
        if not self.screenshot_cache:
            return self.capture_screenshot()
        
        return {
            'success': True,
            'screenshot': self.screenshot_cache
        }
    
    def execute_voice_command(self, audio_data=None, text_command=None):
        """Execute voice command from mobile"""
        try:
            if text_command:
                return self.execute_command(text_command, source='mobile_voice_text')
            
            if audio_data:
                return {
                    'success': False,
                    'error': 'Audio processing not yet implemented. Use text_command instead.'
                }
            
            return {
                'success': False,
                'error': 'No command provided'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_recent_activity(self, limit=20):
        """Get recent command activity"""
        try:
            activity_file = Path('mobile_activity.json')
            
            if not activity_file.exists():
                return {
                    'success': True,
                    'activity': []
                }
            
            with open(activity_file, 'r') as f:
                activity = json.load(f)
            
            return {
                'success': True,
                'activity': activity[-limit:]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def log_activity(self, activity_type, details):
        """Log mobile activity"""
        try:
            activity_file = Path('mobile_activity.json')
            
            activity = []
            if activity_file.exists():
                with open(activity_file, 'r') as f:
                    activity = json.load(f)
            
            activity.append({
                'timestamp': datetime.now().isoformat(),
                'type': activity_type,
                'details': details
            })
            
            if len(activity) > 1000:
                activity = activity[-1000:]
            
            with open(activity_file, 'w') as f:
                json.dump(activity, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    def get_app_info(self):
        """Get VATSAL app information"""
        return {
            'success': True,
            'app': {
                'name': 'VATSAL Mobile Companion',
                'version': '1.0.0',
                'desktop_app': 'VATSAL AI Desktop Automation',
                'features': [
                    'Remote command execution',
                    'Live screenshot viewing',
                    'Quick action shortcuts',
                    'Voice command support',
                    'System monitoring',
                    'Push notifications',
                    'Real-time updates via WebSocket'
                ]
            }
        }


def create_mobile_app(command_executor=None):
    """Create Flask app for mobile API"""
    app = Flask(__name__)
    CORS(app)
    
    mobile_api = MobileAPI(command_executor)
    
    @app.route('/api/mobile/status', methods=['GET'])
    def status():
        """Get system status"""
        return jsonify(mobile_api.get_system_status())
    
    @app.route('/api/mobile/info', methods=['GET'])
    def info():
        """Get app information"""
        return jsonify(mobile_api.get_app_info())
    
    @app.route('/api/mobile/command', methods=['POST'])
    def execute_command():
        """Execute a command"""
        data = request.get_json()
        command = data.get('command')
        
        if not command:
            return jsonify({'success': False, 'error': 'No command provided'}), 400
        
        result = mobile_api.execute_command(command)
        mobile_api.log_activity('command', {'command': command, 'result': result})
        
        return jsonify(result)
    
    @app.route('/api/mobile/quick-actions', methods=['GET'])
    def get_quick_actions():
        """Get available quick actions"""
        category = request.args.get('category')
        return jsonify(mobile_api.get_quick_actions(category))
    
    @app.route('/api/mobile/quick-action/<action_id>', methods=['POST'])
    def execute_quick_action(action_id):
        """Execute a quick action"""
        result = mobile_api.execute_quick_action(action_id)
        mobile_api.log_activity('quick_action', {'action_id': action_id, 'result': result})
        
        return jsonify(result)
    
    @app.route('/api/mobile/screenshot', methods=['GET'])
    def screenshot():
        """Capture and return screenshot"""
        quality = int(request.args.get('quality', 85))
        max_width = int(request.args.get('max_width', 1920))
        
        result = mobile_api.capture_screenshot(quality, max_width)
        return jsonify(result)
    
    @app.route('/api/mobile/screenshot/cached', methods=['GET'])
    def cached_screenshot():
        """Get cached screenshot"""
        result = mobile_api.get_cached_screenshot()
        return jsonify(result)
    
    @app.route('/api/mobile/voice', methods=['POST'])
    def voice_command():
        """Execute voice command"""
        data = request.get_json()
        text_command = data.get('text_command')
        
        result = mobile_api.execute_voice_command(text_command=text_command)
        mobile_api.log_activity('voice', {'command': text_command, 'result': result})
        
        return jsonify(result)
    
    @app.route('/api/mobile/activity', methods=['GET'])
    def activity():
        """Get recent activity"""
        limit = int(request.args.get('limit', 20))
        return jsonify(mobile_api.get_recent_activity(limit))
    
    return app, mobile_api


if __name__ == '__main__':
    app, api = create_mobile_app()
    print('🚀 Starting VATSAL Mobile API...')
    print('📱 Mobile API available at http://0.0.0.0:5001')
    app.run(host='0.0.0.0', port=5001, debug=False)
