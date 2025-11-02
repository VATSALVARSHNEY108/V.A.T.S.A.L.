"""
Test lock screen functionality directly
"""

from system_control import SystemController
from command_executor import CommandExecutor

# Test 1: Direct system control
print("=" * 60)
print("Test 1: Direct System Control")
print("=" * 60)
controller = SystemController()
result = controller.lock_screen()
print(f"Result: {result}")

# Test 2: Command executor with action
print("\n" + "=" * 60)
print("Test 2: Command Executor")
print("=" * 60)
executor = CommandExecutor()
command_dict = {
    "action": "lock_screen",
    "parameters": {},
    "description": "Lock the computer screen"
}
result = executor.execute(command_dict)
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")

# Test 3: Try different action names that Gemini might return
print("\n" + "=" * 60)
print("Test 3: Testing various action names")
print("=" * 60)
test_actions = ["lock_screen", "lock", "screen_lock", "lockscreen"]
for action in test_actions:
    command_dict = {
        "action": action,
        "parameters": {},
        "description": "Lock the screen"
    }
    result = executor.execute(command_dict)
    print(f"Action '{action}': {result['success']} - {result['message']}")
