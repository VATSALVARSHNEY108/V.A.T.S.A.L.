import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'modules', 'ai_features'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'modules', 'utilities'))

from code_generator import generate_code
from notepad_writer import write_code_to_notepad, write_letter_to_notepad

def generate_and_write(description, fullscreen=True):
    print(f"🤖 Generating content: {description}...")

    result = generate_code(description)

    if result.get("success"):
        code = result["code"]
        source = result.get("source", "unknown")

        print(f"✅ Generated {result.get('language', 'text')} content ({len(code)} chars)")

        # Check if it's a letter or code
        if source == "letter_template":
            letter_type = result.get("letter_name", "Letter")
            print(f"📝 Writing {letter_type} to Notepad in full screen...")
            write_result = write_letter_to_notepad(code, letter_type, fullscreen=fullscreen)
        else:
            language = result.get("language", "text")
            print(f"📝 Writing {language} code to Notepad in full screen...")
            write_result = write_code_to_notepad(code, language, fullscreen=fullscreen)

        if write_result["success"]:
            print(f"✅ {write_result['message']}")
            print("\n" + "="*60)
            print(code[:500] + ("..." if len(code) > 500 else ""))
            print("="*60)
        else:
            print(f"❌ Error writing to Notepad: {write_result.get('error')}")
    else:
        print(f"❌ Error: {result.get('error')}")

if __name__ == "__main__":
    description = input("What code do you want to generate? ")
    generate_and_write(description)

