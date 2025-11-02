"""
Test Wake Word Voice Assistant
Tests the interactive voice command system with wake words: oye, bhaiya, bhaisahb
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
    print("=" * 60)
    print("🎤 INTERACTIVE VOICE ASSISTANT WITH WAKE WORDS")
    print("=" * 60)
    
    assistant = VoiceAssistant(command_callback=demo_command_callback)
    
    print("\n📝 Wake Words:")
    wake_words = assistant.get_wake_words()
    for i, word in enumerate(wake_words, 1):
        print(f"   {i}. {word.capitalize()}")
    
    print("\n" + create_voice_commands_list())
    
    print("\n" + "=" * 60)
    print("🚀 Starting Interactive Voice Assistant...")
    print("=" * 60)
    print("\n💡 HOW TO USE:")
    print("   1. Say wake word: 'Oye', 'Bhaiya', or 'Bhaisahb'")
    print("   2. Wait for response: 'Ji, kaho'")
    print("   3. Give your command")
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
