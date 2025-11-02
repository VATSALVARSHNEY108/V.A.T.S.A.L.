"""
Debug script to see what Gemini returns for 'lock the screen'
"""

import os
from dotenv import load_dotenv
load_dotenv()

from gemini_controller import parse_command

# Test what Gemini returns for "lock the screen"
command = "lock the screen"
print(f"Testing command: '{command}'")
print("=" * 60)

result = parse_command(command)

print("\nGemini Response:")
print(f"  Action: {result.get('action')}")
print(f"  Parameters: {result.get('parameters')}")
print(f"  Description: {result.get('description')}")
print(f"  Steps: {result.get('steps', [])}")

# Now test if this would work with command executor
from command_executor import CommandExecutor

executor = CommandExecutor()
exec_result = executor.execute(result)

print("\nExecution Result:")
print(f"  Success: {exec_result['success']}")
print(f"  Message: {exec_result['message']}")
