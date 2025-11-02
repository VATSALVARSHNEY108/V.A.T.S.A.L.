#!/usr/bin/env python3
"""
Web-based VNC Viewer for VATSAL Desktop Automator
Serves noVNC interface and WebSocket proxy on port 5000
"""
import subprocess
import sys

if __name__ == '__main__':
    print("=" * 60)
    print("🖥️  VNC Web Viewer Starting...")
    print("=" * 60)
    print("📺 VNC Server: localhost:5901 (Replit VNC)")
    print("🌐 Web Interface: http://0.0.0.0:5000")
    print("🔌 WebSocket Proxy: Built-in on port 5000")
    print("=" * 60)
    print()
    print("✨ Starting websockify server...")
    print("   Connecting to Replit's built-in VNC server")
    print()
    
    # Use websockify as the main server on port 5000
    # It will serve noVNC files AND proxy WebSocket connections to Replit VNC
    cmd = [
        'websockify',
        '--web', '/tmp/novnc',
        '0.0.0.0:5000',
        'localhost:5901'
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 VNC Web Viewer stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
