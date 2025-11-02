"""
Test Voice Changing Features
Demo of male, female, robot, chipmunk, and other funny voices!
"""

from voice_assistant import VoiceAssistant
import time

print("=" * 70)
print("🎤 VOICE CHANGING DEMO - FUN VOICES!")
print("=" * 70)
print()

# Create assistant
assistant = VoiceAssistant()

# Test message
test_message = "Hello! I am your voice assistant. This is how I sound!"

print("🎭 Testing different voice styles...\n")

# List all available voices
print("📋 Available Voices on Your System:")
print(assistant.list_voices())
print()

# Test different voice presets
voices_to_test = [
    ("female", "👩 FEMALE VOICE (Default)"),
    ("male", "👨 MALE VOICE"),
    ("robot", "🤖 ROBOT VOICE"),
    ("chipmunk", "🐿️ CHIPMUNK VOICE (High & Fast)"),
    ("deep", "🎙️ DEEP VOICE (Low & Slow)"),
    ("funny", "😂 FUNNY VOICE"),
    ("fast", "⚡ FAST TALKER"),
    ("slow", "🐌 SLOW TALKER")
]

print("🎬 Voice Demo Starting...\n")
print("=" * 70)

for voice_type, description in voices_to_test:
    print(f"\n{description}")
    print("-" * 70)
    
    # Change voice
    result = assistant.change_voice(voice_type)
    print(f"Status: {result}")
    
    # Show current settings
    print(assistant.get_current_voice())
    
    # Speak with this voice
    print("🔊 Speaking...")
    assistant.speak(test_message)
    
    # Brief pause
    time.sleep(1)

print("\n" + "=" * 70)
print("\n🎯 Voice Speed Tests...\n")

# Reset to normal voice
assistant.change_voice("female")

speeds = ["very slow", "slow", "normal", "fast", "very fast", "super fast"]
for speed in speeds:
    print(f"\n⏱️ Testing {speed.upper()} speed...")
    assistant.set_voice_speed(speed)
    assistant.speak(f"This is {speed} speaking speed!")
    time.sleep(0.5)

print("\n" + "=" * 70)
print("\n✅ Voice Demo Complete!")
print()
print("💡 VOICE COMMANDS YOU CAN USE:")
print("   • 'Bhai, change voice to male'")
print("   • 'Bhai, change voice to robot'")
print("   • 'Bhai, change voice to chipmunk' 🐿️")
print("   • 'Bhai, change voice to funny'")
print("   • 'Bhai, speak faster'")
print("   • 'Bhai, speak slower'")
print("   • 'Bhai, list voices'")
print("   • 'Bhai, current voice'")
print()
print("🎉 Have fun with different voices!")
print()
