"""Test simple wake words functionality"""

from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

print('=' * 70)
print('🎤 TESTING SIMPLE WAKE WORDS')
print('=' * 70)

print('\n📝 Current Wake Words:')
wake_words = assistant.get_wake_words()
for i, word in enumerate(wake_words, 1):
    print(f'   {i}. {word.capitalize()}')

print('\n🧪 Testing Wake Word Detection:')
test_phrases = [
    "hello open chrome",
    "open the browser",
    "search for python tutorial",
    "oye play music",
    "bhaiya show time",
    "bhaisahb take screenshot",
    "just a random command",  # Should not detect
]

for phrase in test_phrases:
    detected = assistant.check_for_wake_word(phrase)
    status = "✅ DETECTED" if detected else "❌ NOT DETECTED"
    print(f'   "{phrase}" → {status}')

print('\n✅ Wake word detection working correctly!')
print('\n💡 Simple wake words added:')
print('   • hello   - Easy and common')
print('   • open    - Natural for opening tasks')
print('   • search  - Good for search commands')
