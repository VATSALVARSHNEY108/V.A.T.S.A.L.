"""
Script to test and adjust kid voice settings
"""
from voice_assistant import VoiceAssistant

# Create voice assistant
assistant = VoiceAssistant()

print("🎤 Current Settings:")
print(f"  Voice type: {assistant.current_voice_type}")
print(f"  Rate: {assistant.engine.getProperty('rate')} wpm")

# Change to chipmunk voice explicitly
print("\n🔄 Changing to chipmunk (kid) voice...")
result = assistant.change_voice("chipmunk")
print(result)

print("\n🎤 New Settings:")
print(f"  Voice type: {assistant.current_voice_type}")
print(f"  Rate: {assistant.engine.getProperty('rate')} wpm")

# Test the voice
print("\n🔊 Testing kid voice...")
assistant.speak("Hi! This is how I sound like a kid! I talk really fast and my voice is high-pitched!")

print("\n✅ Done! The voice should sound like a kid now.")
