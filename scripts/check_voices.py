"""
Check all available voices on the system
"""
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("🎤 Available Voices on Your System:")
print("=" * 60)

for i, voice in enumerate(voices):
    print(f"\n{i}. {voice.name}")
    print(f"   ID: {voice.id}")
    print(f"   Languages: {voice.languages}")
    print(f"   Gender: {voice.gender if hasattr(voice, 'gender') else 'N/A'}")
    print(f"   Age: {voice.age if hasattr(voice, 'age') else 'N/A'}")

print("\n" + "=" * 60)
print(f"Total voices found: {len(voices)}")

# Test each voice
print("\n🔊 Testing each voice...")
for i, voice in enumerate(voices):
    print(f"\nTesting voice {i}: {voice.name}")
    engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 300)  # Fast like a kid
    engine.say(f"Hello, this is voice number {i}")
    engine.runAndWait()
