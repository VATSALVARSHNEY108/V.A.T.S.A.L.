#!/usr/bin/env python3
"""
VATSAL Mobile Companion - Integrated Server
Combines WebSocket Server, Mobile API, and Notification Service
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time
import json
from datetime import datetime
import psutil
import os
from dotenv import load_dotenv

from mobile_api import MobileAPI
from mobile_auth import mobile_auth, require_auth, get_client_ip
from notification_service import notification_service

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vatsal-secret-key-2024')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global state
connected_clients = 0
system_stats = {
    'cpu': 0,
    'memory': 0,
    'disk': 0,
    'network': {'sent': 0, 'recv': 0}
}
command_history = []
MAX_HISTORY = 100

# Mobile API instance (will be initialized with command executor later)
mobile_api = None


# ============================================================================
# WebSocket Handlers
# ============================================================================

@socketio.on('connect')
def handle_connect():
    global connected_clients
    connected_clients += 1
    print(f'✅ Client connected. Total clients: {connected_clients}')
    
    socketio.emit('connection_response', {
        'status': 'connected',
        'message': 'Successfully connected to VATSAL Mobile Companion',
        'server_time': datetime.now().isoformat(),
        'client_id': request.sid
    }, room=request.sid)
    
    socketio.emit('system_stats', system_stats, room=request.sid)
    
    if command_history:
        socketio.emit('command_history', {
            'history': command_history[-10:]
        }, room=request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    print(f'❌ Client disconnected. Total clients: {connected_clients}')


@socketio.on('ping')
def handle_ping(data):
    socketio.emit('pong', {
        'timestamp': datetime.now().isoformat(),
        'received': data
    }, room=request.sid)


@socketio.on('command_started')
def handle_command_started(data):
    command = data.get('command', '')
    broadcast_command_execution(command, 'started', 'Executing command...')


@socketio.on('command_completed')
def handle_command_completed(data):
    command = data.get('command', '')
    result = data.get('result', '')
    broadcast_command_execution(command, 'completed', result)
    
    # Send push notification for important commands
    if any(keyword in command.lower() for keyword in ['error', 'failed', 'critical']):
        notification_service.notify_event('command_completed', {
            'command': command,
            'result': result
        }, priority='high')


@socketio.on('command_failed')
def handle_command_failed(data):
    command = data.get('command', '')
    error = data.get('error', '')
    broadcast_command_execution(command, 'failed', error)
    
    # Send push notification for failed commands
    notification_service.notify_event('command_failed', {
        'command': command,
        'error': error
    }, priority='high')


@socketio.on('notification')
def handle_notification(data):
    title = data.get('title', '')
    message = data.get('message', '')
    level = data.get('level', 'info')
    broadcast_notification(title, message, level)


@socketio.on('system_event')
def handle_system_event(data):
    event_type = data.get('event_type', '')
    event_data = data.get('data', {})
    broadcast_system_event(event_type, event_data)


# ============================================================================
# Web Routes - Dashboard & Mobile Interface
# ============================================================================

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')


@app.route('/mobile')
def mobile():
    """Mobile companion interface"""
    return render_template('mobile.html')


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'clients': connected_clients,
        'time': datetime.now().isoformat(),
        'services': {
            'websocket': True,
            'mobile_api': mobile_api is not None,
            'notifications': notification_service is not None
        }
    })


# ============================================================================
# Mobile API Routes (Authentication Required)
# ============================================================================

@app.route('/api/mobile/auth', methods=['POST'])
def authenticate():
    """Authenticate and get token"""
    data = request.get_json()
    pin = data.get('pin')
    device_id = data.get('device_id', get_client_ip())
    
    if not pin:
        return jsonify({
            'success': False,
            'error': 'PIN required'
        }), 400
    
    token_data = mobile_auth.generate_token(device_id, pin)
    
    if not token_data:
        return jsonify({
            'success': False,
            'error': 'Invalid PIN'
        }), 401
    
    return jsonify({
        'success': True,
        **token_data
    })


@app.route('/api/mobile/status', methods=['GET'])
def mobile_status():
    """Get system status (no auth required for status)"""
    if mobile_api:
        return jsonify(mobile_api.get_system_status())
    return jsonify({'success': False, 'error': 'Mobile API not initialized'})


@app.route('/api/mobile/info', methods=['GET'])
def mobile_info():
    """Get app information"""
    if mobile_api:
        return jsonify(mobile_api.get_app_info())
    return jsonify({'success': False, 'error': 'Mobile API not initialized'})


@app.route('/api/mobile/command', methods=['POST'])
@require_auth
def mobile_command():
    """Execute a command"""
    if not mobile_api:
        return jsonify({'success': False, 'error': 'Mobile API not initialized'})
    
    data = request.get_json()
    command = data.get('command')
    
    if not command:
        return jsonify({'success': False, 'error': 'No command provided'}), 400
    
    result = mobile_api.execute_command(command)
    mobile_api.log_activity('command', {'command': command, 'result': result})
    
    # Broadcast via WebSocket
    status = 'completed' if result.get('success') else 'failed'
    broadcast_command_execution(command, status, result.get('result', result.get('error', '')))
    
    return jsonify(result)


@app.route('/api/mobile/quick-actions', methods=['GET'])
def mobile_quick_actions():
    """Get available quick actions"""
    if not mobile_api:
        return jsonify({'success': False, 'error': 'Mobile API not initialized'})
    
    category = request.args.get('category')
    return jsonify(mobile_api.get_quick_actions(category))


@app.route('/api/mobile/quick-action/<action_id>', methods=['POST'])
@require_auth
def mobile_quick_action(action_id):
    """Execute a quick action"""
    if not mobile_api:
        return jsonify({'success': False, 'error': 'Mobile API not initialized'})
    
    result = mobile_api.execute_quick_action(action_id)
    mobile_api.log_activity('quick_action', {'action_id': action_id, 'result': result})
    
    return jsonify(result)


@app.route('/api/mobile/screenshot', methods=['GET'])
@require_auth
def mobile_screenshot():
    """Capture and return screenshot"""
    if not mobile_api:
        return jsonify({'success': False, 'error': 'Mobile API not initialized'})
    
    quality = int(request.args.get('quality', 85))
    max_width = int(request.args.get('max_width', 1920))
    
    result = mobile_api.capture_screenshot(quality, max_width)
    return jsonify(result)


@app.route('/api/mobile/screenshot/cached', methods=['GET'])
def mobile_screenshot_cached():
    """Get cached screenshot"""
    if not mobile_api:
        return jsonify({'success': False, 'error': 'Mobile API not initialized'})
    
    result = mobile_api.get_cached_screenshot()
    return jsonify(result)


@app.route('/api/mobile/voice', methods=['POST'])
@require_auth
def mobile_voice():
    """Execute voice command"""
    if not mobile_api:
        return jsonify({'success': False, 'error': 'Mobile API not initialized'})
    
    data = request.get_json()
    text_command = data.get('text_command')
    
    result = mobile_api.execute_voice_command(text_command=text_command)
    mobile_api.log_activity('voice', {'command': text_command, 'result': result})
    
    return jsonify(result)


@app.route('/api/mobile/activity', methods=['GET'])
@require_auth
def mobile_activity():
    """Get recent activity"""
    if not mobile_api:
        return jsonify({'success': False, 'error': 'Mobile API not initialized'})
    
    limit = int(request.args.get('limit', 20))
    return jsonify(mobile_api.get_recent_activity(limit))


# ============================================================================
# Notification API Routes
# ============================================================================

@app.route('/api/notifications/send', methods=['POST'])
@require_auth
def send_notification():
    """Send push notification"""
    data = request.get_json()
    
    title = data.get('title')
    message = data.get('message')
    priority = data.get('priority', 'normal')
    recipients = data.get('recipients')
    
    result = notification_service.send_push_notification(title, message, priority, recipients)
    return jsonify(result)


@app.route('/api/notifications/status', methods=['GET'])
def notification_status():
    """Get notification service status"""
    return jsonify(notification_service.get_status())


@app.route('/api/notifications/history', methods=['GET'])
@require_auth
def notification_history():
    """Get notification history"""
    limit = int(request.args.get('limit', 20))
    return jsonify(notification_service.get_notification_history(limit))


# ============================================================================
# Broadcasting Functions
# ============================================================================

def broadcast_command_execution(command, status, result='', metadata=None):
    """Broadcast command execution update"""
    event_data = {
        'timestamp': datetime.now().isoformat(),
        'command': command,
        'status': status,
        'result': result,
        'metadata': metadata or {}
    }
    
    command_history.append(event_data)
    if len(command_history) > MAX_HISTORY:
        command_history.pop(0)
    
    socketio.emit('command_update', event_data)
    print(f'📡 Broadcast: {command} - {status}')


def broadcast_system_event(event_type, data):
    """Broadcast system event"""
    event_data = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'data': data
    }
    
    socketio.emit('system_event', event_data)
    print(f'📡 System Event: {event_type}')


def broadcast_notification(title, message, level='info'):
    """Broadcast notification"""
    notification = {
        'timestamp': datetime.now().isoformat(),
        'title': title,
        'message': message,
        'level': level
    }
    
    socketio.emit('notification', notification)
    print(f'🔔 Notification: {title} - {message}')


def update_system_stats():
    """Update and broadcast system stats"""
    global system_stats
    
    while True:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            system_stats = {
                'cpu': round(cpu_percent, 2),
                'memory': round(memory.percent, 2),
                'disk': round(disk.percent, 2),
                'network': {
                    'sent': network.bytes_sent,
                    'recv': network.bytes_recv
                },
                'timestamp': datetime.now().isoformat()
            }
            
            if connected_clients > 0:
                socketio.emit('system_stats', system_stats)
            
            time.sleep(2)
            
        except Exception as e:
            print(f'Error updating system stats: {e}')
            time.sleep(5)


def start_background_tasks():
    """Start background monitoring tasks"""
    stats_thread = threading.Thread(target=update_system_stats, daemon=True)
    stats_thread.start()


# ============================================================================
# Broadcaster Class (for external use)
# ============================================================================

class WebSocketBroadcaster:
    """WebSocket broadcaster for external modules"""
    
    @staticmethod
    def command_started(command):
        broadcast_command_execution(command, 'started', 'Executing command...')
    
    @staticmethod
    def command_completed(command, result):
        broadcast_command_execution(command, 'completed', result)
    
    @staticmethod
    def command_failed(command, error):
        broadcast_command_execution(command, 'failed', str(error))
    
    @staticmethod
    def notify(title, message, level='info'):
        broadcast_notification(title, message, level)
    
    @staticmethod
    def system_event(event_type, data):
        broadcast_system_event(event_type, data)
    
    @staticmethod
    def send_custom_event(event_name, data):
        socketio.emit(event_name, {
            'timestamp': datetime.now().isoformat(),
            'data': data
        })


broadcaster = WebSocketBroadcaster()


def initialize_mobile_api(command_executor):
    """Initialize Mobile API with command executor"""
    global mobile_api
    mobile_api = MobileAPI(command_executor)
    print('✅ Mobile API initialized with command executor')


if __name__ == '__main__':
    print('🚀 Starting VATSAL Mobile Companion Server...')
    print('=' * 60)
    print('📱 Mobile Interface: http://0.0.0.0:5000/mobile')
    print('💻 Desktop Dashboard: http://0.0.0.0:5000')
    
    mobile_pin = os.getenv('MOBILE_PIN', '1234')
    print('🔐 Authentication PIN:', mobile_pin)
    
    if mobile_pin == '1234':
        print('⚠️  WARNING: Using default PIN (1234)!')
        print('⚠️  SECURITY RISK: Change MOBILE_PIN in your .env file!')
        print('⚠️  Add to Replit Secrets: MOBILE_PIN=your-secure-pin')
    
    print('📡 WebSocket enabled with real-time updates')
    print('🔔 Push notifications configured')
    print('=' * 60)
    
    # Initialize mobile API without command executor for standalone mode
    mobile_api = MobileAPI()
    
    start_background_tasks()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
