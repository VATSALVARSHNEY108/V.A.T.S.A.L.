#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import json
from datetime import datetime
import psutil
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vatsal-secret-key-2024')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

connected_clients = 0
system_stats = {
    'cpu': 0,
    'memory': 0,
    'disk': 0,
    'network': {'sent': 0, 'recv': 0}
}

command_history = []
MAX_HISTORY = 100


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/api/health')
def health():
    return {'status': 'online', 'clients': connected_clients, 'time': datetime.now().isoformat()}


@socketio.on('connect')
def handle_connect():
    global connected_clients
    connected_clients += 1
    print(f'✅ Client connected. Total clients: {connected_clients}')
    
    emit('connection_response', {
        'status': 'connected',
        'message': 'Successfully connected to VATSAL WebSocket Server',
        'server_time': datetime.now().isoformat(),
        'client_id': request.sid
    })
    
    emit('system_stats', system_stats)
    
    if command_history:
        emit('command_history', {
            'history': command_history[-10:]
        })


@socketio.on('disconnect')
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    print(f'❌ Client disconnected. Total clients: {connected_clients}')


@socketio.on('ping')
def handle_ping(data):
    emit('pong', {
        'timestamp': datetime.now().isoformat(),
        'received': data
    })


@socketio.on('command_started')
def handle_command_started(data):
    command = data.get('command', '')
    timestamp = data.get('timestamp', datetime.now().isoformat())
    print(f'🚀 Command started: {command}')
    broadcast_command_execution(command, 'started', 'Executing command...')


@socketio.on('command_completed')
def handle_command_completed(data):
    command = data.get('command', '')
    result = data.get('result', '')
    timestamp = data.get('timestamp', datetime.now().isoformat())
    print(f'✅ Command completed: {command}')
    broadcast_command_execution(command, 'completed', result)


@socketio.on('command_failed')
def handle_command_failed(data):
    command = data.get('command', '')
    error = data.get('error', '')
    timestamp = data.get('timestamp', datetime.now().isoformat())
    print(f'❌ Command failed: {command} - {error}')
    broadcast_command_execution(command, 'failed', error)


@socketio.on('notification')
def handle_notification(data):
    title = data.get('title', '')
    message = data.get('message', '')
    level = data.get('level', 'info')
    print(f'🔔 Notification: {title} - {message}')
    broadcast_notification(title, message, level)


@socketio.on('system_event')
def handle_system_event(data):
    event_type = data.get('event_type', '')
    event_data = data.get('data', {})
    print(f'📡 System event: {event_type}')
    broadcast_system_event(event_type, event_data)


@socketio.on('execute_command')
def handle_execute_command(data):
    command = data.get('command', '')
    print(f'📝 Received command from web client: {command}')
    
    broadcast_command_execution(command, 'pending', 'Command received from web client - GUI execution not yet implemented')


def broadcast_command_execution(command, status, result='', metadata=None):
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
    event_data = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'data': data
    }
    
    socketio.emit('system_event', event_data)
    print(f'📡 System Event: {event_type}')


def broadcast_notification(title, message, level='info'):
    notification = {
        'timestamp': datetime.now().isoformat(),
        'title': title,
        'message': message,
        'level': level
    }
    
    socketio.emit('notification', notification)
    print(f'🔔 Notification: {title} - {message}')


def update_system_stats():
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
    stats_thread = threading.Thread(target=update_system_stats, daemon=True)
    stats_thread.start()


class WebSocketBroadcaster:
    
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


if __name__ == '__main__':
    print('🚀 Starting VATSAL WebSocket Server...')
    print('📡 WebSocket enabled with real-time updates')
    print('🌐 Server will be available at http://0.0.0.0:5000')
    print('💡 Connect clients to see live updates!')
    
    start_background_tasks()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
