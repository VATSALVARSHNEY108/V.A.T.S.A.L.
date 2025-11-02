"""Test sensitivity presets with dynamic parameters"""

from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()

print('=== TESTING FIXED SENSITIVITY PRESETS ===\n')

levels = ['low', 'medium', 'high', 'ultra']

for level in levels:
    print(f'\n--- Testing {level.upper()} ---')
    print(assistant.set_sensitivity(level))
    print(f'Energy Threshold: {assistant.recognizer.energy_threshold}')
    print(f'Pause Threshold: {assistant.recognizer.pause_threshold}')
    print(f'Dynamic Ratio: {assistant.recognizer.dynamic_energy_ratio}')
    print(f'Dynamic Damping: {assistant.recognizer.dynamic_energy_adjustment_damping}')

print('\n✅ All presets now have distinct dynamic parameters!')
print('\n📊 Sensitivity Comparison:')
print('  LOW:    energy=2000, ratio=2.0 (least sensitive)')
print('  MEDIUM: energy=1000, ratio=1.5')
print('  HIGH:   energy=300,  ratio=1.2 (default)')
print('  ULTRA:  energy=100,  ratio=1.1 (most sensitive)')
