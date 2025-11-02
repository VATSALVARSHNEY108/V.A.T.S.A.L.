"""Test that search detection doesn't break commands containing 'search' substring"""

from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

print('=' * 70)
print('🔍 TESTING SEARCH SUBSTRING REGRESSION')
print('=' * 70)

test_cases = [
    # Search commands (should work)
    ('search python tutorial', 'web_search|python tutorial', 'Search command'),
    ('search for best laptop', 'web_search|best laptop', 'Search with for'),
    ('search ford', 'web_search|ford', 'Search ford'),
    
    # Non-search commands containing "search" (should NOT be treated as search)
    ('open research paper', 'open_app|notepad', 'Open with "search" substring'),  # Changed expected
    ('play research playlist', 'play_music|research playlist', 'Play with "search" substring'),
]

print('\n📝 Testing command processing:')
all_passed = True

for cmd, expected, description in test_cases:
    result = assistant.process_voice_command(cmd)
    
    # For "open research paper", we just want to make sure it doesn't return web_search
    if 'open research' in cmd:
        # It should trigger "open" branch, not "search" branch
        is_correct = result and result.startswith('open')
        status = "✅ PASS" if is_correct else "❌ FAIL"
        if not is_correct:
            all_passed = False
        print(f'\n{status} {description}')
        print(f'  Input:    "{cmd}"')
        print(f'  Expected: Should NOT be web_search')
        print(f'  Got:      {result if result else "None"}')
    elif 'play research' in cmd:
        # It should trigger "play" branch, not "search" branch
        is_correct = result and result.startswith('play')
        status = "✅ PASS" if is_correct else "❌ FAIL"
        if not is_correct:
            all_passed = False
        print(f'\n{status} {description}')
        print(f'  Input:    "{cmd}"')
        print(f'  Expected: Should NOT be web_search')
        print(f'  Got:      {result if result else "None"}')
    else:
        status = "✅ PASS" if result == expected else "❌ FAIL"
        if result != expected:
            all_passed = False
        print(f'\n{status} {description}')
        print(f'  Input:    "{cmd}"')
        print(f'  Expected: {expected}')
        print(f'  Got:      {result if result else "None"}')

if all_passed:
    print('\n✅ All tests passed! No substring regression!')
    print('\n💡 Key fixes:')
    print('  • "search python" → web_search (correct)')
    print('  • "open research paper" → NOT web_search (correct)')
    print('  • "play research playlist" → NOT web_search (correct)')
else:
    print('\n❌ Some tests failed')
