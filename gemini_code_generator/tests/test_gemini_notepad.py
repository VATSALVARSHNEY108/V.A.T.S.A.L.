"""
Test Gemini Code Generation with Auto Notepad Writing
This script demonstrates how to generate code with Gemini and automatically write it to Notepad
"""

from code_generator import generate_code
import subprocess
import time
import pyperclip

def test_code_generation_to_notepad(description, language=None):
    """
    Generate code using Gemini and automatically write it to Notepad
    
    Args:
        description: What code you want to generate
        language: Programming language (auto-detected if not provided)
    """
    print("="*70)
    print("🚀 GEMINI CODE GENERATOR → NOTEPAD AUTOMATION TEST")
    print("="*70)
    
    print(f"\n📝 Request: {description}")
    print(f"🎯 Language: {language or 'Auto-detect'}")
    
    print("\n⏳ Step 1: Generating code with Gemini AI...")
    result = generate_code(description, language)
    
    if not result.get("success"):
        print(f"\n❌ Error: {result.get('error', 'Code generation failed')}")
        return False
    
    code = result["code"]
    detected_lang = result["language"]
    source = result.get("source", "ai")
    
    print(f"✅ Code generated successfully!")
    print(f"   Language: {detected_lang}")
    print(f"   Source: {source.upper()}")
    print(f"   Length: {len(code)} characters")
    
    print("\n" + "="*70)
    print("Generated Code Preview:")
    print("="*70)
    
    lines = code.split('\n')
    preview_lines = lines[:15]
    for line in preview_lines:
        print(line)
    if len(lines) > 15:
        print(f"... ({len(lines) - 15} more lines)")
    
    print("\n" + "="*70)
    
    print("\n⏳ Step 2: Opening Notepad...")
    subprocess.Popen(['notepad.exe'])
    time.sleep(2)
    
    print("⏳ Step 3: Copying code to clipboard...")
    pyperclip.copy(code)
    time.sleep(0.5)
    
    print("⏳ Step 4: Auto-pasting to Notepad...")
    import pyautogui
    pyautogui.hotkey('ctrl', 'v')
    
    print("\n✅ COMPLETE! Code has been written to Notepad!")
    print("="*70)
    
    return True

if __name__ == "__main__":
    print("\n🎉 Testing Gemini → Notepad Integration\n")
    
    test_cases = [
        {
            "description": "bubble sort algorithm",
            "language": "python"
        },
        {
            "description": "fibonacci sequence calculator",
            "language": None
        },
        {
            "description": "binary search in C++",
            "language": "cpp"
        }
    ]
    
    print("Available test cases:")
    for i, test in enumerate(test_cases, 1):
        print(f"  {i}. {test['description']} ({test['language'] or 'auto-detect'})")
    
    print("\n" + "="*70)
    choice = input("\nEnter test case number (1-3) or press Enter for custom: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(test_cases):
        test = test_cases[int(choice) - 1]
        test_code_generation_to_notepad(test["description"], test["language"])
    else:
        custom_desc = input("Enter your code description: ")
        custom_lang = input("Enter language (or press Enter for auto-detect): ").strip() or None
        test_code_generation_to_notepad(custom_desc, custom_lang)
