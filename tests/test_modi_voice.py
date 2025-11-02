"""
Test Modi-like voice settings
"""
from voice_assistant import VoiceAssistant

print("🎙️ Testing Narendra Modi-like Voice")
print("=" * 60)

# Create new voice assistant with Modi voice
assistant = VoiceAssistant()

print(f"\n✓ Voice type: {assistant.current_voice_type}")
print(f"✓ Speaking rate: {assistant.engine.getProperty('rate')} words/min")
print(f"✓ Volume: {int(assistant.engine.getProperty('volume') * 100)}%")

# Test with Modi-style phrases
print("\n🔊 Testing Modi voice with typical phrases...")
print("\nPhrase 1:")
assistant.speak("Namaskar. Main aapka swagat karta hoon.")

print("\nPhrase 2:")
assistant.speak("Bhaiyon aur behno, aaj hum ek naye Bharat ki ore badh rahe hain.")

print("\nPhrase 3:")
assistant.speak("Mitron, Digital India is the future of our great nation.")

print("\n" + "=" * 60)
print("✅ Test complete!")
print("\nThe voice should sound:")
print("  • Deep and authoritative")
print("  • Slower, measured pace (like Modi's speeches)")
print("  • Hindi/Indian accent")
print("\nRestart your application to use the Modi voice!")
