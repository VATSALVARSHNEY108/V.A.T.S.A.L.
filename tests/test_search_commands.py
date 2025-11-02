"""Test search command processing"""

from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

print('=' * 70)
print('🔍 TESTING SEARCH COMMAND SUPPORT')
print('=' * 70)

test_commands = [
    ('search python tutorial', 'web_search|python tutorial'),
    ('search for best laptop', 'web_search|best laptop'),
    ('search javascript', 'web_search|javascript'),
    ('open chrome', 'open_app|chrome'),
    ('open notepad', 'open_app|notepad'),
]

print('\n📝 Testing command processor:')
all_passed = True

for cmd, expected in test_commands:
    result = assistant.process_voice_command(cmd)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    if result != expected:
        all_passed = False
    print(f'{status} "{cmd}"')
    print(f'     Expected: {expected}')
    print(f'     Got:      {result if result else "None"}')
    print()

if all_passed:
    print('✅ All search commands working correctly!')
else:
    print('❌ Some tests failed')
