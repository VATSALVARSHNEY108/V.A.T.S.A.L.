"""
Notepad Writer Module
Handles opening Notepad in full screen and writing content
"""

import subprocess
import time
import pyperclip
import pyautogui
import os


def write_to_notepad(content: str, fullscreen: bool = True, title: str = None) -> dict:
    """
    Write content to Notepad with optional full screen mode

    Args:
        content: Text content to write
        fullscreen: Whether to open Notepad in full screen (default: True)
        title: Optional title for the content

    Returns:
        dict with success status and details
    """
    try:
        # Step 1: Open Notepad
        print("📝 Opening Notepad...")
        process = subprocess.Popen(['notepad.exe'] if os.name == 'nt' else ['gedit'])
        time.sleep(2)  # Wait for Notepad to fully open

        # Step 2: Put Notepad in TRUE FULLSCREEN if requested
        if fullscreen:
            print("🖥️  Opening in FULL SCREEN mode...")
            time.sleep(0.5)  # Brief pause to ensure window is ready

            # First maximize the window
            if os.name == 'nt':
                pyautogui.hotkey('win', 'up')
                time.sleep(0.3)
                # Then enter true fullscreen with F11
                pyautogui.press('f11')
            else:
                # For Linux, use F11 for full screen
                pyautogui.press('f11')

            time.sleep(1)  # Wait for fullscreen animation to complete
            print("✅ Notepad is now in FULL SCREEN mode")

        # Step 3: Add title if provided
        if title:
            content_with_title = f"{title}\n{'='*len(title)}\n\n{content}"
        else:
            content_with_title = content

        # Step 4: Copy content to clipboard
        print("📋 Copying content to clipboard...")
        pyperclip.copy(content_with_title)
        time.sleep(0.3)

        # Step 5: Paste content into Notepad
        print("⌨️  Writing to Notepad...")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        print("✅ Content written to Notepad successfully!")

        return {
            "success": True,
            "fullscreen": fullscreen,
            "chars_written": len(content_with_title),
            "message": "Content written to Notepad in full screen" if fullscreen else "Content written to Notepad"
        }

    except Exception as e:
        print(f"❌ Error writing to Notepad: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to write to Notepad: {str(e)}"
        }


def write_code_to_notepad(code: str, language: str = "python", fullscreen: bool = True) -> dict:
    """
    Write code to Notepad with language title

    Args:
        code: Code content to write
        language: Programming language (for title)
        fullscreen: Whether to open in full screen

    Returns:
        dict with success status
    """
    title = f"Generated {language.upper()} Code"
    return write_to_notepad(code, fullscreen=fullscreen, title=title)


def write_letter_to_notepad(letter: str, letter_type: str = "Letter", fullscreen: bool = True) -> dict:
    """
    Write letter to Notepad with letter type title

    Args:
        letter: Letter content to write
        letter_type: Type of letter (for title)
        fullscreen: Whether to open in full screen

    Returns:
        dict with success status
    """
    title = f"{letter_type}"
    return write_to_notepad(letter, fullscreen=fullscreen, title=title)


if __name__ == "__main__":
    # Test the notepad writer
    test_content = """This is a test of the Notepad writer.

The window should open in full screen,
and this content should be written automatically.

Features:
- Full screen mode
- Auto-maximize window
- Clean content writing
- Cross-platform support
"""

    print("Testing Notepad Writer with Full Screen")
    print("=" * 60)
    result = write_to_notepad(test_content, fullscreen=True, title="Test Document")

    if result["success"]:
        print(f"\n✅ Success! {result['chars_written']} characters written")
    else:
        print(f"\n❌ Error: {result['error']}")
