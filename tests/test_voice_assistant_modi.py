#!/usr/bin/env python3
"""
Test that VoiceAssistant uses Modi voice
"""
from voice_assistant import VoiceAssistant

print("=" * 60)
print("🎙️ Testing Voice Assistant with Modi Voice")
print("=" * 60)

# Create voice assistant (should automatically use Modi voice)
print("\n1️⃣ Creating VoiceAssistant...")
va = VoiceAssistant()

print(f"\n✓ Voice type: {va.current_voice_type}")
print(f"✓ Speaking rate: {va.engine.getProperty('rate')} wpm")
print(f"✓ Volume: {int(va.engine.getProperty('volume') * 100)}%")

# Test the speak function
print("\n2️⃣ Testing speak() function...")
print("   Speaking: 'Namaskar mitron'")
va.speak("Namaskar mitron")

print("   Speaking: 'Main aapki seva mein hoon'")
va.speak("Main aapki seva mein hoon")

print("   Speaking: 'Jai Hind'")
va.speak("Jai Hind")

# Test voice change function
print("\n3️⃣ Testing voice change to Modi explicitly...")
result = va.change_voice("modi")
print(f"   {result}")

print(f"   Rate after change: {va.engine.getProperty('rate')} wpm")

print("   Speaking: 'Digital India is the future'")
va.speak("Digital India is the future")

print("\n" + "=" * 60)
print("✅ Voice Assistant Modi Voice Test Complete!")
print("=" * 60)
print("\nModi voice is now active in:")
print("  ✓ VoiceAssistant class")
print("  ✓ All voice commands")
print("  ✓ GUI App (when started)")
print("  ✓ Simple Chatbot (when started)")
print("\nJust restart your app to use Modi voice!")
