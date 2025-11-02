"""
Test Ultra Fast "Bhai" Wake Word Detection
Even a hint of "bhai" sound will activate instantly!
"""

from voice_assistant import VoiceAssistant

def handle_command(command):
    """Handle voice commands"""
    print(f"🎯 Command received: {command}")
    
    if "chrome" in command.lower():
        return "Opening Chrome browser"
    elif "notepad" in command.lower():
        return "Opening Notepad"
    elif "hello" in command.lower():
        return "Hello! How can I help?"
    else:
        return f"Processing: {command}"

print("=" * 60)
print("🚀 ULTRA FAST 'BHAI' DETECTION TEST")
print("=" * 60)
print()
print("✨ NEW FEATURES:")
print("  • Detects 'bhai' even if you say just 'bha'")
print("  • Recognizes phonetic variations: bye, by, bae")
print("  • ULTRA LOW latency (0.3s pause threshold)")
print("  • Maximum sensitivity (energy threshold: 100)")
print()
print("🎤 WAKE WORD VARIATIONS DETECTED:")
print("  • 'bhai' ⚡")
print("  • 'bha' (just the hint!)")
print("  • 'bye' (sounds similar)")
print("  • 'by' (short form)")
print("  • 'bhaiya' (full form)")
print("  • 'bhaisahb' (respectful)")
print()
print("=" * 60)
print()

# Create assistant with command handler
assistant = VoiceAssistant(command_callback=handle_command)

# Show current sensitivity settings
print(assistant.get_sensitivity_info())

print("\n🎙️ Starting voice assistant...")
print("💡 TIP: Say 'bhai' or even just 'bha' to activate instantly!")
print("💡 Say 'stop listening' to quit\n")

# Start continuous listening
assistant.listen_continuous()

# Keep the script running
try:
    import time
    while assistant.listening:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Stopping...")
    assistant.stop_listening()
