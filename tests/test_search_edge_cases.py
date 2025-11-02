"""Test search command edge cases (queries containing 'for')"""

from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

print('=' * 70)
print('🔍 TESTING SEARCH EDGE CASES')
print('=' * 70)

test_cases = [
    ('search python tutorial', 'web_search|python tutorial', 'Basic search'),
    ('search for best laptop', 'web_search|best laptop', 'Search with "for"'),
    ('search ford dealership', 'web_search|ford dealership', 'Query containing "for"'),
    ('search forensics updates', 'web_search|forensics updates', 'Query starting with "for"'),
    ('search formula 1 news', 'web_search|formula 1 news', 'Query with "for" substring'),
    ('search for ford trucks', 'web_search|ford trucks', '"for" in prefix and query'),
    ('search javascript', 'web_search|javascript', 'Simple query'),
]

print('\n📝 Testing search command edge cases:')
all_passed = True

for cmd, expected, description in test_cases:
    result = assistant.process_voice_command(cmd)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    if result != expected:
        all_passed = False
    
    print(f'\n{status} {description}')
    print(f'  Input:    "{cmd}"')
    print(f'  Expected: {expected}')
    print(f'  Got:      {result if result else "None"}')

if all_passed:
    print('\n✅ All edge cases handled correctly!')
    print('\n💡 Key improvements:')
    print('  • "search ford" → "web_search|ford" (not corrupted)')
    print('  • "search forensics" → "web_search|forensics" (not corrupted)')
    print('  • "search for best" → "web_search|best" (optional "for" removed)')
else:
    print('\n❌ Some tests failed')
