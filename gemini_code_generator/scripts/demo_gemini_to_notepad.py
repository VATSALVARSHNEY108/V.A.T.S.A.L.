"""
🚀 GEMINI → NOTEPAD AUTO-CODE WRITER DEMO
Complete demonstration of AI code generation with automatic Notepad writing
"""

import os
from code_generator import generate_code
import subprocess
import time
import pyperclip
import pyautogui


def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print demo header"""
    print("\n" + "=" * 80)
    print(" " * 20 + "🤖 GEMINI AI → NOTEPAD CODE WRITER 🤖")
    print("=" * 80)
    print("\n✨ This demo shows how Gemini AI generates code and writes it to Notepad\n")


def demo_code_generation(description, language=None):
    """
    Complete demo: Generate code with Gemini and write to Notepad
    """
    print("=" * 80)
    print(f"📝 REQUEST: {description}")
    if language:
        print(f"🎯 LANGUAGE: {language}")
    print("=" * 80)

    # Step 1: Generate code
    print("\n[STEP 1/4] 🤖 Calling Gemini AI to generate code...")
    start_time = time.time()

    result = generate_code(description, language)

    generation_time = time.time() - start_time

    if not result.get("success"):
        print(f"\n❌ ERROR: {result.get('error', 'Unknown error')}")
        return False

    code = result["code"]
    detected_lang = result["language"]
    source = result.get("source", "ai")

    print(f"✅ Code generated in {generation_time:.2f} seconds!")
    print(f"   📊 Language: {detected_lang.upper()}")
    print(f"   📦 Source: {source.upper()} {'(Instant Template!)' if source == 'template' else '(AI Generated)'}")
    print(f"   📏 Size: {len(code)} characters, {len(code.splitlines())} lines")

    # Step 2: Preview code
    print("\n[STEP 2/4] 👀 Code Preview:")
    print("-" * 80)
    lines = code.split('\n')
    preview_lines = min(20, len(lines))
    for i, line in enumerate(lines[:preview_lines], 1):
        print(f"  {i:3d} | {line}")
    if len(lines) > preview_lines:
        print(f"  ... | ({len(lines) - preview_lines} more lines)")
    print("-" * 80)

    # Step 3: Open Notepad
    print("\n[STEP 3/4] 📝 Opening Notepad...")
    try:
        subprocess.Popen(['notepad.exe'])
        print("✅ Notepad opened successfully!")
        time.sleep(2.5)  # Wait for Notepad to fully load
    except Exception as e:
        print(f"❌ Error opening Notepad: {e}")
        return False

    # Step 4: Copy and paste code
    print("\n[STEP 4/4] ⌨️  Writing code to Notepad...")
    try:
        print("   📋 Copying code to clipboard...")
        pyperclip.copy(code)
        time.sleep(0.3)

        print("   ⌨️  Auto-pasting into Notepad...")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        print("\n✅ SUCCESS! Code has been written to Notepad!")
    except Exception as e:
        print(f"❌ Error writing to Notepad: {e}")
        return False

    print("\n" + "=" * 80)
    print(f"✨ COMPLETE! Generated {detected_lang.upper()} code is now in Notepad!")
    print("=" * 80)

    return True


def run_demo():
    """Run the complete demonstration"""
    clear_screen()
    print_header()

    # Demo examples
    examples = [
        ("bubble sort algorithm", "python"),
        ("palindrome checker", None),
        ("fibonacci sequence", "python"),
        ("binary search", "cpp"),
        ("simple calculator", "javascript"),
    ]

    print("📚 AVAILABLE DEMO EXAMPLES:\n")
    for i, (desc, lang) in enumerate(examples, 1):
        lang_display = lang.upper() if lang else "Auto-detect"
        print(f"   {i}. {desc.title()} ({lang_display})")

    print("\n   6. Custom request")
    print("   0. Exit")

    print("\n" + "=" * 80)

    while True:
        choice = input("\n👉 Select an option (0-6): ").strip()

        if choice == "0":
            print("\n👋 Thanks for watching the demo! Goodbye!\n")
            break

        elif choice.isdigit() and 1 <= int(choice) <= 5:
            desc, lang = examples[int(choice) - 1]
            print(f"\n🚀 Starting demo for: {desc}")
            input("\nPress ENTER to start generation...")
            demo_code_generation(desc, lang)

            cont = input("\n❓ Try another example? (y/n): ").strip().lower()
            if cont != 'y':
                print("\n👋 Demo complete! Goodbye!\n")
                break

        elif choice == "6":
            print("\n📝 CUSTOM REQUEST")
            print("-" * 80)
            custom_desc = input("What code do you want? ")
            custom_lang = input("Language (or press Enter for auto-detect): ").strip() or None

            print(f"\n🚀 Generating: {custom_desc}")
            demo_code_generation(custom_desc, custom_lang)

            cont = input("\n❓ Generate more code? (y/n): ").strip().lower()
            if cont != 'y':
                print("\n👋 Demo complete! Goodbye!\n")
                break
        else:
            print("❌ Invalid choice. Please select 0-6.")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
