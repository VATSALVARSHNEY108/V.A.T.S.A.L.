#!/bin/bash

echo "🚀 Initializing VATSAL GUI with VNC Desktop Environment..."

# Create necessary directories
mkdir -p ~/.vnc
mkdir -p ~/screenshots

# Create .Xauthority file if it doesn't exist
touch ~/.Xauthority
chmod 600 ~/.Xauthority

# Kill any existing Xvfb processes
pkill -9 Xvfb 2>/dev/null || true
sleep 1

# Set DISPLAY environment variable
export DISPLAY=:0

# Start Xvfb (virtual framebuffer) with better settings for VNC
echo "📺 Starting virtual display (1920x1080)..."
Xvfb :0 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
XVFB_PID=$!
sleep 2

# Check if Xvfb started successfully
if ! ps -p $XVFB_PID > /dev/null; then
    echo "❌ Failed to start Xvfb"
    exit 1
fi

# Generate X11 authentication using mcookie (more reliable than xxd)
echo "🔐 Setting up X11 authentication..."
MCOOKIE=$(mcookie)
xauth add $DISPLAY . $MCOOKIE 2>/dev/null || echo "⚠️  X auth warning (non-fatal)"

# Set up window manager (optional, for better VNC experience)
export XDG_RUNTIME_DIR=/tmp/runtime-$USER
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR

# Disable screen saver and power management
xset s off -dpms 2>/dev/null || true

# Start x11vnc VNC server on port 5900
echo "🔐 Starting VNC server..."
x11vnc -display :0 -forever -shared -rfbport 5900 -nopw &
VNC_PID=$!
sleep 2

# Check if VNC server started successfully
if ! ps -p $VNC_PID > /dev/null; then
    echo "⚠️  VNC server failed to start (non-fatal)"
else
    echo "✅ VNC server running on port 5900"
fi

echo "✅ Virtual desktop ready!"
echo "🤖 Starting VATSAL GUI Application..."
echo ""

# Start the GUI application using the startup script
cd /home/runner/workspace
python start_gui.py

# Cleanup on exit
echo "🛑 Shutting down..."
kill $VNC_PID 2>/dev/null || true
kill $XVFB_PID 2>/dev/null || true
