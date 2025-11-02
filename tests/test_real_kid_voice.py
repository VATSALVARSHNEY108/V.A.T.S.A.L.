"""
Final test for kid voice
"""
from voice_assistant import VoiceAssistant

print("🎤 Testing REAL Kid Voice")
print("=" * 60)

# Create new voice assistant with updated settings
assistant = VoiceAssistant()

print(f"✓ Voice type: {assistant.current_voice_type}")
print(f"✓ Speaking rate: {assistant.engine.getProperty('rate')} words/min")

print("\n🔊 Testing kid voice now...")
assistant.speak("Hello! I am your voice assistant and I sound like a kid now! How do I sound?")

print("\n✅ Test complete!")
print("The voice should sound higher-pitched and faster like a child.")
print("\nRestart your application to use the new kid voice!")
