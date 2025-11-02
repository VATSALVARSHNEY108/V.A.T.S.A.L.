"""Quick test of voice command recognition"""
from voice_assistant import VoiceAssistant

print("✅ Testing voice commands...")
a = VoiceAssistant()

tests = [
    ('change voice to male', 'change_voice|male'),
    ('change voice to chipmunk', 'change_voice|chipmunk'),
    ('change voice to funny', 'change_voice|funny'),
    ('change voice to robot', 'change_voice|robot'),
    ('speak faster', 'voice_speed|fast'),
    ('speak slower', 'voice_speed|slow'),
    ('list voices', 'list_voices'),
    ('current voice', 'current_voice')
]

passed = 0
for cmd, expected in tests:
    result = a.process_voice_command(cmd)
    status = '✅' if result == expected else '❌'
    print(f'{status} "{cmd}" → {result}')
    passed += 1 if result == expected else 0

print(f'\n✅ {passed}/{len(tests)} voice commands working!')
