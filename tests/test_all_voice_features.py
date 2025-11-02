"""
Test All 50+ Voice Command Features
Comprehensive demo of MEGA voice commands
"""

from voice_assistant import VoiceAssistant, create_voice_commands_list

print("=" * 70)
print("🎤 MEGA VOICE COMMANDS - 50+ FEATURES TEST")
print("=" * 70)
print()

# Show all available commands
print(create_voice_commands_list())
print()
print("=" * 70)
print()

# Test command processing (without actual execution)
assistant = VoiceAssistant()

print("🧪 TESTING COMMAND RECOGNITION:\n")

test_commands = [
    # Time & Date
    ("what time is it", "get_time"),
    ("what's the date", "get_date"),
    ("what day is today", "get_day"),
    
    # Weather
    ("weather", "weather"),
    ("weather in new york", "weather|new york"),
    ("weather forecast", "weather_forecast"),
    
    # Calculator
    ("calculate 25 plus 37", "calculate|25 plus 37"),
    ("50 times 3", "calculate|50 times 3"),
    
    # Notes
    ("create note buy groceries", "create_note|buy groceries"),
    ("list notes", "list_notes"),
    ("remind me to call mom", "create_reminder|to call mom"),
    
    # Clipboard
    ("copy to clipboard hello world", "copy_to_clipboard|hello world"),
    ("paste from clipboard", "paste_from_clipboard"),
    
    # Search & Web
    ("search for python tutorials", "web_search|python tutorials"),
    ("google best laptops", "web_search|best laptops"),
    ("open youtube", "open_url|https://youtube.com"),
    
    # Apps
    ("open chrome", "open_app|chrome"),
    ("open notepad", "open_app|notepad"),
    ("open vs code", "open_app|code"),
    ("open spotify", "open_app|spotify"),
    
    # Window Management
    ("close window", "close_window"),
    ("minimize all", "minimize_all"),
    ("show desktop", "show_desktop"),
    
    # Music
    ("play lofi beats", "play_music|lofi beats"),
    ("play shape of you on spotify", "play_spotify|shape of you"),
    ("pause music", "pause_music"),
    ("next song", "next_song"),
    
    # System Control
    ("screenshot", "screenshot"),
    ("max brightness", "brightness|100"),
    ("increase brightness", "brightness|80"),
    ("volume up", "volume_up"),
    ("mute volume", "mute"),
    ("shutdown", "shutdown"),
    ("restart", "restart"),
    ("lock screen", "lock_screen"),
    
    # File Operations
    ("organize downloads", "organize_downloads"),
    ("clear temp files", "clear_temp"),
    ("empty trash", "empty_trash"),
    ("check disk space", "check_disk_space"),
    
    # Productivity
    ("start timer", "start_timer"),
    ("enable focus mode", "focus_mode_on"),
    
    # Information
    ("system report", "system_report"),
    ("battery status", "battery_status"),
    ("ip address", "get_ip"),
    
    # Fun
    ("tell a joke", "tell_joke"),
    ("flip a coin", "flip_coin"),
    ("roll dice", "roll_dice"),
    
    # News
    ("tech news", "news|technology"),
    ("latest news", "news|general"),
]

passed = 0
failed = 0

for command, expected in test_commands:
    result = assistant.process_voice_command(command)
    status = "✅" if result == expected else "❌"
    
    if result == expected:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} '{command}' → {result}")
    if result != expected:
        print(f"   Expected: {expected}")

print()
print("=" * 70)
print(f"📊 TEST RESULTS: {passed} passed, {failed} failed")
print("=" * 70)
print()

# Show wake word detection test
print("🎯 WAKE WORD DETECTION TEST:\n")

wake_word_tests = [
    ("bhai open chrome", True),
    ("bhaiya what time is it", True),
    ("hello search python", True),
    ("oye play music", True),
    ("bye weather", True),  # Phonetic match!
    ("by calculator", True),  # Short form!
    ("bha screenshot", True),  # Just a hint!
    ("random command", False),
    ("open notepad", True),  # "open" is wake word
]

print("Testing wake word variations:")
for command, should_detect in wake_word_tests:
    detected = assistant.check_for_wake_word(command)
    status = "✅" if detected == should_detect else "❌"
    print(f"{status} '{command}' → {'Detected' if detected else 'Not detected'}")

print()
print("=" * 70)
print()
print("💡 TIP: Run 'python test_ultra_fast_bhai.py' for live voice testing!")
print()
print("🚀 Your voice assistant is ready with 50+ commands!")
print("   Say 'Bhai' (or even 'Bha') to activate instantly! ⚡")
print()
