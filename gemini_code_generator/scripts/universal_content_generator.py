"""
🌟 UNIVERSAL CONTENT GENERATOR
Generates ANY type of content: Stories, Code, Letters, Poems, etc.
Automatically writes to Notepad in full screen!
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from google import genai
import pyautogui
import pyperclip
import subprocess
import time

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def detect_content_type(description):
    """Detect what type of content user wants"""
    desc_lower = description.lower()

    # Check for POEM first (before code) because "poem" is more specific
    if any(word in desc_lower for word in ['poem', 'poetry', 'verse', 'haiku', 'sonnet', 'rhyme']):
        return 'poem'
    # Check for STORY
    elif any(word in desc_lower for word in ['story', 'tale', 'narrative', 'once upon']):
        return 'story'
    # Check for LETTER
    elif any(word in desc_lower for word in ['letter', 'email', 'application', 'resignation', 'complaint']):
        return 'letter'
    # Check for CODE (only if they specifically ask for code/program/function)
    elif any(word in desc_lower for word in ['code', 'program', 'function', 'script', 'algorithm', 'write python', 'write java', 'write javascript']):
        return 'code'
    # Check for ESSAY
    elif any(word in desc_lower for word in ['essay', 'article', 'blog']):
        return 'essay'
    else:
        return 'general'

def get_system_prompt(content_type):
    """Get the right prompt for each content type"""

    prompts = {
        'story': """You are a STORY WRITER. Write simple, fun stories.

RULES:
- Use simple, easy words
- Short sentences (10-15 words max)
- 3-5 paragraphs
- Make it fun and interesting!
- NO code blocks, just plain text story

FORMAT:
**[Title]**

[Story in paragraphs]""",

        'letter': """You are a LETTER WRITER. Write professional letters.

RULES:
- Use proper letter format
- Be polite and professional
- Include: date, greeting, body, closing, signature
- Clear and respectful tone

FORMAT:
[Date]

Dear [Name],

[Letter body in paragraphs]

Sincerely,
[Name]""",

        'poem': """You are a POET. Write beautiful poems. NEVER write code!

CRITICAL RULES:
- ONLY write the poem text - NO code!
- NO Python functions or programming code
- NO code blocks (```)
- Use poetic language with rhythm and imagery
- Can use rhyme or free verse
- Make it emotional and beautiful

FORMAT (plain text only):
**[Title]**

[Verse 1]

[Verse 2]

[Verse 3]

EXAMPLE:
**The Mighty Tree**

Standing tall with branches wide,
A home for birds to rest and hide.
Its leaves dance gently in the breeze,
A peaceful giant among the trees.""",

        'code': """You are a CODE WRITER. Write clean, working code.

RULES:
- Include helpful comments
- Make it simple and clear
- Show example usage
- Follow best practices

FORMAT:
```language
# Code with comments
```""",

        'essay': """You are an ESSAY WRITER. Write clear, informative essays.

RULES:
- Clear introduction
- Body paragraphs with details
- Strong conclusion
- Formal but readable tone

FORMAT:
**[Title]**

[Introduction]

[Body paragraphs]

[Conclusion]""",

        'general': """You are a HELPFUL WRITER. Write clear, useful content.

RULES:
- Match the request exactly
- Be clear and concise
- Use appropriate format
- Helpful and friendly"""
    }

    return prompts.get(content_type, prompts['general'])

def generate_content(description):
    """Generate ANY type of content based on description"""

    print(f"\n🤖 Analyzing your request: '{description}'")

    content_type = detect_content_type(description)

    icons = {
        'story': '📖',
        'letter': '✉️',
        'poem': '🎭',
        'code': '💻',
        'essay': '📝',
        'general': '📄'
    }

    print(f"{icons.get(content_type, '📄')} Detected type: {content_type.upper()}")
    print(f"🔮 Generating {content_type}...")

    try:
        system_prompt = get_system_prompt(content_type)

        response = client.models.generate_content(
            model='models/gemini-2.0-flash-exp',
            contents=description,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.8 if content_type in ['story', 'poem'] else 0.5
            )
        )

        content = response.text

        print(f"✅ Generated {len(content)} characters!")

        return {
            'success': True,
            'content': content,
            'type': content_type
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def write_to_notepad(content, fullscreen=True):
    """Write content to Notepad in full screen"""

    print("\n📝 Opening Notepad...")

    try:
        subprocess.Popen(['notepad.exe'])
        time.sleep(2.5)

        if fullscreen:
            print("🖥️ Making full screen...")
            pyautogui.hotkey('win', 'up')
            time.sleep(0.5)

        print("📋 Copying content to clipboard...")
        pyperclip.copy(content)
        time.sleep(0.3)

        print("⌨️ Pasting into Notepad...")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        print("✅ Content written to Notepad!")
        return True

    except Exception as e:
        print(f"❌ Error writing to Notepad: {e}")
        return False

def main():
    """Main function"""
    print("\n" + "="*70)
    print(" "*15 + "🌟 UNIVERSAL CONTENT GENERATOR 🌟")
    print("="*70)
    print("\n✨ I can generate:")
    print("   📖 Stories (simple and fun)")
    print("   💻 Code (any programming language)")
    print("   ✉️ Letters (professional and formal)")
    print("   🎭 Poems (beautiful and creative)")
    print("   📝 Essays (informative articles)")
    print("   📄 And anything else you need!")
    print("\n" + "="*70)

    while True:
        print("\n" + "-"*70)
        description = input("\n📝 What do you want me to create? (or 'quit' to exit): ").strip()

        if description.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break

        if not description:
            print("❌ Please enter a description!")
            continue

        result = generate_content(description)

        if result['success']:
            content = result['content']
            content_type = result['type']

            print("\n" + "="*70)
            print("📄 PREVIEW:")
            print("-"*70)
            preview = content[:300] + "..." if len(content) > 300 else content
            print(preview)
            print("-"*70)

            write_choice = input("\n📝 Write to Notepad? (y/n): ").strip().lower()

            if write_choice == 'y':
                write_to_notepad(content, fullscreen=True)
            else:
                print("\n✅ Content ready! Here it is:\n")
                print(content)

        else:
            print(f"\n❌ Failed to generate content: {result.get('error')}")

        continue_choice = input("\n🔄 Generate more content? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n👋 Thanks for using Universal Content Generator!\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
