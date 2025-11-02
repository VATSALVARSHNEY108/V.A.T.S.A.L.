#!/usr/bin/env python3
"""
Test simple male voice
"""
from voice_assistant import VoiceAssistant

print("=" * 60)
print("🎙️ Testing Male Voice (Simple)")
print("=" * 60)

# Create voice assistant
va = VoiceAssistant()

print(f"\n✓ Voice type: {va.current_voice_type}")
print(f"✓ Speaking rate: {va.engine.getProperty('rate')} wpm")
print(f"✓ Volume: {int(va.engine.getProperty('volume') * 100)}%")

# Test speaking
print("\n🔊 Testing male voice:")
va.speak("Hello, I am your voice assistant with a male voice")
va.speak("This is a man's voice, not a woman's voice")
va.speak("Thank you for using the voice assistant")

print("\n✅ Male voice test complete!")
print("\nThe voice should now be a man's voice (not woman's voice)")
