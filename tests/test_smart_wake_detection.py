"""Test smart wake word detection (only at phrase start)"""

from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

print('=' * 70)
print('🎤 TESTING SMART WAKE WORD DETECTION')
print('=' * 70)

print('\n📝 Current Wake Words:')
wake_words = assistant.get_wake_words()
for i, word in enumerate(wake_words, 1):
    print(f'   {i}. {word.capitalize()}')

print('\n🧪 Testing Wake Word Detection (should only trigger at phrase START):')
test_cases = [
    # Should DETECT (wake word at start)
    ("hello", True, "Wake word only"),
    ("hello open chrome", True, "Wake word at start"),
    ("open the browser", True, "Wake word at start"),
    ("search for python", True, "Wake word at start"),
    ("oye play music", True, "Wake word at start"),
    ("bhaiya show time", True, "Wake word at start"),
    
    # Should NOT DETECT (wake word in middle or not at start)
    ("please open chrome", False, "Wake word in middle"),
    ("can you search google", False, "Wake word in middle"),
    ("I want to open chrome", False, "Wake word in middle"),
    ("let's search for help", False, "Wake word in middle"),
    ("just a random command", False, "No wake word"),
    ("chrome browser", False, "No wake word"),
]

print('\n✅ Expected to DETECT (wake word at START):')
for phrase, should_detect, description in test_cases:
    if should_detect:
        detected = assistant.check_for_wake_word(phrase)
        status = "✅ PASS" if detected else "❌ FAIL"
        print(f'   {status} "{phrase}" → {description}')

print('\n❌ Expected to NOT DETECT (wake word not at start):')
for phrase, should_detect, description in test_cases:
    if not should_detect:
        detected = assistant.check_for_wake_word(phrase)
        status = "✅ PASS" if not detected else "❌ FAIL"
        print(f'   {status} "{phrase}" → {description}')

# Check all test cases
all_passed = True
for phrase, should_detect, description in test_cases:
    detected = assistant.check_for_wake_word(phrase)
    if detected != should_detect:
        all_passed = False
        print(f'\n❌ FAILED: "{phrase}" - Expected {should_detect}, got {detected}')

if all_passed:
    print('\n✅ All tests PASSED! Wake word detection is working correctly!')
    print('\n💡 Key improvements:')
    print('   • Only detects wake words at the START of a phrase')
    print('   • "open chrome" triggers wake word (starts with "open")')
    print('   • "please open chrome" does NOT trigger (not at start)')
else:
    print('\n❌ Some tests failed!')
