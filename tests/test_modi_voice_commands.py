#!/usr/bin/env python3
"""
Test Modi voice with voice commands
"""
from command_executor import CommandExecutor

print("=" * 70)
print("🎙️  TESTING NARENDRA MODI VOICE")
print("=" * 70)

# Create command executor (this will create VoiceAssistant with Modi voice)
print("\n🔄 Initializing voice assistant...")
executor = CommandExecutor()

print("\n✓ Voice assistant initialized with Modi voice!")
print(f"✓ Voice type: {executor.voice_assistant.current_voice_type}")
print(f"✓ Speaking rate: {executor.voice_assistant.engine.getProperty('rate')} words/min")

# Test Modi voice with typical phrases
print("\n" + "=" * 70)
print("🔊 TESTING MODI VOICE - Listen to these phrases:")
print("=" * 70)

phrases = [
    "Namaskar. Main Bharat ka Pradhan Mantri hoon.",
    "Mitron, aaj hum ek naye India ki ore badh rahe hain.",
    "Digital India is transforming our nation.",
    "Sabka saath, sabka vikas, sabka vishwas.",
    "Jai Hind!"
]

for i, phrase in enumerate(phrases, 1):
    print(f"\n{i}. Speaking: \"{phrase}\"")
    executor.voice_assistant.speak(phrase)
    print("   ✓ Done")

print("\n" + "=" * 70)
print("✅ MODI VOICE TEST COMPLETE!")
print("=" * 70)
print("\nThe voice should sound:")
print("  • Deep and authoritative (like Modi)")
print("  • Slower, measured pace")
print("  • Hindi/Indian accent")
print("\n💡 To use Modi voice in your apps, just restart them!")
print("   - GUI App: python gui_app.py")
print("   - Simple Chatbot: python simple_chatbot.py")
