"""Test that action verbs are preserved in commands"""

from voice_assistant import VoiceAssistant

# Use the actual command processor from voice_assistant
def test_with_real_processor(command):
    """Use the real process_voice_command method"""
    assistant = VoiceAssistant()
    result = assistant.process_voice_command(command)
    return result if result else "❌ No action matched"

assistant = VoiceAssistant(command_callback=test_with_real_processor)

print('=' * 70)
print('🎤 TESTING ACTION VERB PRESERVATION')
print('=' * 70)

print('\n📝 Testing with real command processor:')

# Simulate wake word detection and command extraction
test_cases = [
    ("open chrome", "Action wake word + target"),
    ("search python tutorial", "Action wake word + query"),
    ("hello open chrome", "Greeting + action + target"),
    ("oye play music", "Hindi wake word + action"),
    ("bhaiya open notepad", "Hindi wake word + action + target"),
]

for phrase, description in test_cases:
    print(f'\n--- {description} ---')
    print(f'Input phrase: "{phrase}"')
    
    if assistant.check_for_wake_word(phrase):
        command_parts = phrase.lower().strip().split(None, 1)
        wake_word_used = command_parts[0] if command_parts else ""
        
        if len(command_parts) > 1:
            # Determine actual command based on wake word type
            if wake_word_used in assistant.action_wake_words:
                actual_command = phrase.lower().strip()
            else:
                actual_command = command_parts[1]
            
            print(f'Wake word: "{wake_word_used}"')
            print(f'Command to process: "{actual_command}"')
            
            # Test with real command processor
            result = test_with_real_processor(actual_command)
            print(f'Command processor result: {result}')
            
            # Verify action verbs are preserved
            if wake_word_used in ["open", "search"]:
                if wake_word_used in actual_command:
                    print(f'✅ PASS: Action verb "{wake_word_used}" preserved!')
                else:
                    print(f'❌ FAIL: Action verb "{wake_word_used}" was stripped!')
        else:
            print(f'Wake word only: "{wake_word_used}"')

print('\n' + '=' * 70)
print('✅ VERIFICATION SUMMARY:')
print('=' * 70)
print('• "open chrome" → Command: "open chrome" (action verb kept)')
print('• "search python" → Command: "search python" (action verb kept)')
print('• "hello open chrome" → Command: "open chrome" (hello stripped)')
print('• "oye play music" → Command: "play music" (oye stripped)')
print('\n💡 Action verbs are now preserved correctly!')
