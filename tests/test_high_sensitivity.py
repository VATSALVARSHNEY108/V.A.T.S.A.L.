"""
Test High Sensitivity Voice Assistant
Demonstrates improved voice command sensitivity
"""

from voice_assistant import VoiceAssistant, create_voice_commands_list
import time

def demo_command_callback(command):
    """Demo callback to simulate command processing"""
    print(f"📋 Processing command: {command}")
    
    command_lower = command.lower()
    
    if "chrome" in command_lower or "browser" in command_lower:
        return "Opening Chrome browser"
    elif "screenshot" in command_lower:
        return "Taking screenshot"
    elif "brightness" in command_lower:
        if "increase" in command_lower:
            return "Increasing brightness"
        else:
            return "Decreasing brightness"
    elif "hello" in command_lower or "hi" in command_lower:
        return "Hello! How can I help you?"
    elif "time" in command_lower:
        return f"Current time is {time.strftime('%I:%M %p')}"
    else:
        return "Command received, processing..."

def main():
    print("=" * 70)
    print("🎤 HIGH SENSITIVITY VOICE ASSISTANT")
    print("=" * 70)
    
    assistant = VoiceAssistant(command_callback=demo_command_callback)
    
    # Display current sensitivity settings
    print(assistant.get_sensitivity_info())
    
    print("\n" + "=" * 70)
    print("📝 SENSITIVITY IMPROVEMENTS:")
    print("=" * 70)
    print("✅ Energy Threshold: 300 (was ~4000) - More sensitive to quiet voices")
    print("✅ Pause Threshold: 0.5s (was 0.8s) - Faster phrase detection")
    print("✅ Timeout: 2s continuous / 10s single - Better capture")
    print("✅ Phrase Limit: 8s - Longer commands supported")
    print("✅ Dynamic Adjustment: Enabled - Auto-adapts to noise")
    print("✅ Quick Calibration: 0.3-0.5s - Faster startup")
    
    print("\n" + "=" * 70)
    print("🎚️ AVAILABLE SENSITIVITY LEVELS:")
    print("=" * 70)
    print("  • LOW (2000) - Less sensitive, fewer false triggers")
    print("  • MEDIUM (1000) - Balanced sensitivity")
    print("  • HIGH (300) - Default, very responsive ⭐")
    print("  • ULTRA (100) - Maximum sensitivity")
    
    print("\n💡 To change sensitivity:")
    print("   assistant.set_sensitivity('ultra')")
    
    print("\n📝 Wake Words:")
    wake_words = assistant.get_wake_words()
    for i, word in enumerate(wake_words, 1):
        print(f"   {i}. {word.capitalize()}")
    
    print("\n" + "=" * 70)
    print("🚀 Starting Voice Assistant...")
    print("=" * 70)
    print("\n💡 HOW TO USE:")
    print("   1. Say wake word: 'Oye', 'Bhaiya', or 'Bhaisahb'")
    print("   2. Wait for response: 'Ji, kaho'")
    print("   3. Give your command (can speak softly now!)")
    print("   4. Say 'stop listening' to exit\n")
    
    assistant.listen_continuous()
    
    try:
        while assistant.listening:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Keyboard interrupt detected")
        assistant.stop_listening()
        print("👋 Voice assistant stopped")

if __name__ == "__main__":
    main()
