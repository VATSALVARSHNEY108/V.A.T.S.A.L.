"""
Test script to verify kid voice is working
"""
from voice_assistant import VoiceAssistant

print("🎤 Testing Kid Voice...")
print("-" * 50)

# Create voice assistant (should use kid voice by default)
assistant = VoiceAssistant()

print(f"Current voice type: {assistant.current_voice_type}")
print(f"Voice rate: {assistant.engine.getProperty('rate')} words/minute")
print(f"Voice volume: {int(assistant.engine.getProperty('volume') * 100)}%")

# Test the voice
print("\n🔊 Speaking with kid voice...")
assistant.speak("Hello! I'm your voice assistant with a kid's voice! I speak fast like a chipmunk!")

print("\n✅ Voice test complete!")
print("If you heard a FAST, high-pitched voice, the kid voice is working!")
