"""
Test script to debug the lock screen command flow
Run this on your Windows machine to see where the issue is
"""

import os
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 60)
print("TESTING LOCK SCREEN COMMAND FLOW")
print("=" * 60)

# Step 1: Check API key
print("\n1️⃣ Checking GEMINI_API_KEY...")
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print(f"   ✅ API key found: {api_key[:10]}...")
else:
    print("   ❌ API key NOT found!")
    print("   Please set GEMINI_API_KEY in your .env file")
    exit(1)

# Step 2: Test Gemini parsing
print("\n2️⃣ Testing Gemini command parsing...")
try:
    from gemini_controller import parse_command
    
    result = parse_command("lock the screen")
    print(f"   Gemini returned:")
    print(f"   Action: {result.get('action')}")
    print(f"   Parameters: {result.get('parameters')}")
    print(f"   Description: {result.get('description')}")
    
    if result.get('action') == 'lock_screen':
        print("   ✅ Gemini correctly identified 'lock_screen' action")
    else:
        print(f"   ❌ Gemini returned unexpected action: {result.get('action')}")
        print("   Full response:", json.dumps(result, indent=2))
except Exception as e:
    print(f"   ❌ Gemini parsing failed: {e}")
    exit(1)

# Step 3: Test command executor
print("\n3️⃣ Testing CommandExecutor...")
try:
    from command_executor import CommandExecutor
    
    executor = CommandExecutor()
    
    # Test with the result from Gemini
    exec_result = executor.execute(result)
    
    print(f"   Execution result:")
    print(f"   Success: {exec_result.get('success')}")
    print(f"   Message: {exec_result.get('message')}")
    
    if exec_result.get('success'):
        print("   ✅ Command executed successfully!")
    else:
        print(f"   ❌ Execution failed!")
        
except Exception as e:
    print(f"   ❌ Command execution failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 4: Test direct system_control
print("\n4️⃣ Testing SystemController directly...")
try:
    from system_control import SystemController
    
    system_ctrl = SystemController()
    result = system_ctrl.lock_screen()
    
    print(f"   Direct call result: {result}")
    
    if "locked" in result.lower():
        print("   ✅ SystemController.lock_screen() works!")
    else:
        print("   ⚠️ Unexpected result from lock_screen()")
        
except Exception as e:
    print(f"   ❌ SystemController test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ TEST COMPLETE")
print("=" * 60)
print("\n💡 If all tests pass but GUI still fails:")
print("   1. Close the GUI app completely")
print("   2. Delete all __pycache__ folders")
print("   3. Restart the GUI app")
