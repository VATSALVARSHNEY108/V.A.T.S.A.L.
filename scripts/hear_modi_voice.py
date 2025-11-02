#!/usr/bin/env python3
"""
Simple standalone test to hear Modi voice
"""
import pyttsx3

print("🎙️ Modi Voice Test")
print("=" * 50)

# Create NEW engine with Modi settings
engine = pyttsx3.init()

# Get voices
voices = engine.getProperty('voices')

# Use Hindi voice (most Indian-sounding)
hindi_voice = None
for voice in voices:
    if 'hindi' in voice.id.lower() or 'hi' in voice.languages:
        hindi_voice = voice
        print(f"✓ Found Hindi voice: {voice.name}")
        break

if hindi_voice:
    engine.setProperty('voice', hindi_voice.id)
else:
    print("✓ Using default voice")
    engine.setProperty('voice', voices[0].id)

# Modi-style settings
engine.setProperty('rate', 140)  # Slow, deliberate
engine.setProperty('volume', 1.0)  # Full volume

print(f"✓ Rate: {engine.getProperty('rate')} wpm")
print(f"✓ Volume: {int(engine.getProperty('volume') * 100)}%")

print("\n🔊 Listen now:")
print("-" * 50)

# Speak Modi-style phrases
engine.say("Namaskar mitron")
engine.runAndWait()

engine.say("Jai Hind")
engine.runAndWait()

print("\n✅ Done! Did you hear the voice?")
print("If yes, your Modi voice is working!")
print("If no, your system may not have audio output configured.")
