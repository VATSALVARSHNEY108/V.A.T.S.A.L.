#!/usr/bin/env python3

import socketio
import threading
import time
from datetime import datetime

class WebSocketClient:
    
    def __init__(self, server_url='http://localhost:5000'):
        self.server_url = server_url
        self.sio = socketio.Client(reconnection=True, reconnection_attempts=0, reconnection_delay=1)
        self.connected = False
        self.connect_thread = None
        
        @self.sio.on('connect')
        def on_connect():
            self.connected = True
            print(f'✅ WebSocket Client connected to {self.server_url}')
        
        @self.sio.on('disconnect')
        def on_disconnect():
            self.connected = False
            print(f'❌ WebSocket Client disconnected from {self.server_url}')
        
        @self.sio.on('pong')
        def on_pong(data):
            pass
    
    def connect(self):
        if not self.connected:
            def _connect():
                try:
                    self.sio.connect(self.server_url, wait_timeout=5)
                except Exception as e:
                    print(f'⚠️ WebSocket Client connection failed: {e}')
            
            self.connect_thread = threading.Thread(target=_connect, daemon=True)
            self.connect_thread.start()
    
    def disconnect(self):
        if self.connected:
            try:
                self.sio.disconnect()
            except Exception as e:
                print(f'Error disconnecting WebSocket client: {e}')
    
    def emit(self, event, data):
        if self.connected:
            try:
                self.sio.emit(event, data)
            except Exception as e:
                print(f'Error emitting WebSocket event: {e}')
    
    def command_started(self, command):
        if self.connected:
            self.emit('command_started', {
                'command': command,
                'timestamp': datetime.now().isoformat()
            })
    
    def command_completed(self, command, result):
        if self.connected:
            self.emit('command_completed', {
                'command': command,
                'result': str(result),
                'timestamp': datetime.now().isoformat()
            })
    
    def command_failed(self, command, error):
        if self.connected:
            self.emit('command_failed', {
                'command': command,
                'error': str(error),
                'timestamp': datetime.now().isoformat()
            })
    
    def notify(self, title, message, level='info'):
        if self.connected:
            self.emit('notification', {
                'title': title,
                'message': message,
                'level': level,
                'timestamp': datetime.now().isoformat()
            })
    
    def system_event(self, event_type, data):
        if self.connected:
            self.emit('system_event', {
                'event_type': event_type,
                'data': data,
                'timestamp': datetime.now().isoformat()
            })


ws_client = WebSocketClient()


def get_websocket_client():
    return ws_client
