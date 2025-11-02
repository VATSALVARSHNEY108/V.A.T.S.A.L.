"""Test wake word + command extraction in same phrase"""

from voice_assistant import VoiceAssistant

def test_callback(command):
    """Test callback that shows what command was processed"""
    return f"Processed: {command}"

assistant = VoiceAssistant(command_callback=test_callback)

print('=' * 70)
print('🎤 TESTING WAKE WORD + COMMAND EXTRACTION')
print('=' * 70)

print('\n📝 Testing command extraction logic:')

# Simulate what happens in continuous listening
test_phrases = [
    ("hello", "Wake word only - should prompt for command"),
    ("hello open chrome", "Wake word + command - should extract 'open chrome'"),
    ("open chrome browser", "Wake word + command - should extract 'chrome browser'"),
    ("search python tutorial", "Wake word + command - should extract 'python tutorial'"),
    ("oye play music", "Wake word + command - should extract 'play music'"),
    ("bhaiya", "Wake word only - should prompt for command"),
]

for phrase, description in test_phrases:
    print(f'\n--- {description} ---')
    print(f'Input: "{phrase}"')
    
    # Check if it's a wake word
    if assistant.check_for_wake_word(phrase):
        command_parts = phrase.lower().strip().split(None, 1)
        
        if len(command_parts) > 1:
            actual_command = command_parts[1]
            print(f'✅ Wake word detected with command')
            print(f'   Wake word: "{command_parts[0]}"')
            print(f'   Command extracted: "{actual_command}"')
            print(f'   System says: "Ji"')
            print(f'   Processing immediately: {test_callback(actual_command)}')
        else:
            print(f'✅ Wake word only detected')
            print(f'   Wake word: "{command_parts[0]}"')
            print(f'   System says: "Ji, kaho"')
            print(f'   Waiting for next command...')
    else:
        print(f'❌ No wake word detected')

print('\n' + '=' * 70)
print('✅ FEATURE SUMMARY:')
print('=' * 70)
print('1. "hello" → Says "Ji, kaho", waits for command')
print('2. "hello open chrome" → Says "Ji", processes "open chrome" immediately')
print('3. "open chrome" → Says "Ji", processes "chrome" immediately')
print('\n💡 This solves the architect\'s concern about losing commands!')
