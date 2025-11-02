import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from google import genai
import pyautogui
import pyperclip
import subprocess
import time

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def quick_generate(description):
    desc_lower = description.lower()

    # Check for POEM first
    if 'poem' in desc_lower or 'poetry' in desc_lower or 'verse' in desc_lower:
        content_type = 'POEM'
        system_prompt = """Write a beautiful poem. NEVER write code!
ONLY write the poem text - NO Python functions.
NO code blocks. Just the poem verses.
Use poetic language with rhythm and imagery."""

    elif 'story' in desc_lower or 'tale' in desc_lower:
        content_type = 'STORY'
        system_prompt = """Write a simple, fun story with easy words. 
Short sentences. 3-5 paragraphs. Make it interesting!
NO code blocks, just plain text."""

    elif 'letter' in desc_lower or 'email' in desc_lower:
        content_type = 'LETTER'
        system_prompt = """Write a professional letter with proper format.
Include date, greeting, body, closing.
Be polite and clear."""

    elif 'code' in desc_lower or 'program' in desc_lower or 'function' in desc_lower:
        content_type = 'CODE'
        system_prompt = """Write clean, working code with comments.
Include example usage. Make it simple and clear."""

    else:
        content_type = 'TEXT'
        system_prompt = """Write clear, helpful content that matches the request exactly."""

    print(f"🔮 Generating {content_type}...")

    try:
        response = client.models.generate_content(
            model='models/gemini-2.0-flash-exp',
            contents=description,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7
            )
        )

        content = response.text
        print(f"✅ Generated {len(content)} characters!")

        print("📝 Writing to Notepad...")
        subprocess.Popen(['notepad.exe'])
        time.sleep(2.5)

        pyautogui.hotkey('win', 'up')
        time.sleep(0.5)

        pyperclip.copy(content)
        time.sleep(0.3)

        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        print("✅ Done! Check Notepad!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        description = ' '.join(sys.argv[1:])
        quick_generate(description)
    else:
        description = input("What do you want to create? ")
        quick_generate(description)

