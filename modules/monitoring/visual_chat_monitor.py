"""
📱 Visual AI Chat Monitor & Reply System
Controls real Gmail/WhatsApp on screen with AI Vision + GUI Automation
Everything happens visually - you can watch the AI work!
"""

import time
import webbrowser
from modules.automation.gui_automation import GUIAutomation
from modules.ai_features.vision_ai import extract_text_from_screenshot
from modules.ai_features.screenshot_analysis import analyze_screenshot
from modules.core.gemini_controller import get_client
from google.genai import types
import os


class VisualChatMonitor:
    """Monitor and reply to chats by controlling the actual screen/browser"""

    def __init__(self):
        """Initialize visual chat monitor"""
        self.gui = GUIAutomation()
        print("📱 Visual Chat Monitor initialized")
        print("   ✅ Will control real Gmail/WhatsApp on your screen")

    def open_gmail_in_browser(self):
        """Open Gmail in default browser"""
        print("\n🌐 Opening Gmail in browser...")
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        print("   ⏳ Waiting 7 seconds for Gmail to load...")
        time.sleep(7)

        print("   🪟 Maximizing browser window...")
        time.sleep(1)
        self.gui.hotkey('win', 'up')
        time.sleep(1)

        return {"success": True, "message": "Gmail opened and maximized"}

    def read_emails_from_screen(self) -> dict:
        """
        Take screenshot of Gmail and use AI Vision to read emails

        Returns:
            Dict with emails found on screen
        """
        print("\n📸 Taking screenshot of Gmail inbox...")
        screenshot_path = self.gui.screenshot("gmail_inbox")

        if not screenshot_path:
            return {
                "success": False,
                "message": "❌ Screenshot feature not available in cloud environment. This feature requires running VATSAL locally on your desktop."
            }

        print("   🤖 Analyzing screenshot with AI Vision...")

        prompt = """Analyze this Gmail inbox screenshot and extract email information.

For each visible email in the inbox, provide:
1. Sender name/email
2. Subject line
3. Preview text (if visible)

Format your response as a numbered list of emails."""

        analysis_result = analyze_screenshot(screenshot_path, prompt)

        if analysis_result:
            return {
                "success": True,
                "message": "Emails read from screen",
                "analysis": analysis_result,
                "screenshot": screenshot_path
            }
        else:
            return {
                "success": False,
                "message": "Could not analyze Gmail screenshot"
            }

    def read_specific_email_on_screen(self, email_number: int = 1) -> dict:
        """
        Use keyboard shortcuts to open an email and read its content

        Args:
            email_number: Which email to open (1 = first/top email)

        Returns:
            Dict with full email content
        """
        print(f"\n⌨️  Opening email #{email_number} using keyboard...")

        print("   🏠 Going to inbox (g then i) - ensures proper focus...")
        self.gui.press_key('g')
        time.sleep(0.2)
        self.gui.press_key('i')
        time.sleep(2)

        print("   📧 Focusing on message list (Escape to clear, then Ctrl+Home)...")
        self.gui.press_key('escape')
        time.sleep(0.3)
        self.gui.hotkey('ctrl', 'home')
        time.sleep(0.5)

        if email_number > 1:
            for i in range(email_number - 1):
                print(f"   ⬇️  Moving down to email {i+2} (j key)...")
                self.gui.press_key('j')
                time.sleep(0.4)

        print("   📬 Opening email (Enter key)...")
        self.gui.press_key('enter')

        print("   ⏳ Waiting for email to open...")
        time.sleep(3)

        print("   📸 Taking screenshot of opened email...")
        screenshot_path = self.gui.screenshot("gmail_email_open")

        print("   🤖 Reading email content with AI Vision...")

        prompt = """Analyze this opened Gmail email and extract:
1. From: (sender email/name)
2. Subject: (email subject line)
3. Full email body/content

Provide the complete text so I can reply to it."""

        analysis_result = analyze_screenshot(screenshot_path, prompt)

        if analysis_result:
            return {
                "success": True,
                "message": "Email content read from screen",
                "content": analysis_result,
                "screenshot": screenshot_path
            }
        else:
            return {
                "success": False,
                "message": "Could not read email content"
            }

    def generate_ai_reply_for_email(self, email_content: str, context: str = "professional") -> dict:
        """
        Generate AI reply based on email content

        Args:
            email_content: The email content extracted from screen
            context: Reply style - 'professional', 'casual', 'friendly'

        Returns:
            Dict with suggested reply
        """
        try:
            client = get_client()

            prompt = f"""You are helping write a reply to this email:

{email_content}

**Instructions:**
- Write a {context} reply
- Keep it concise and appropriate
- Address the main points
- Sign off professionally

Generate ONLY the reply text that should be typed, no additional commentary."""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=500
                )
            )

            suggested_reply = response.text.strip()

            return {
                "success": True,
                "suggested_reply": suggested_reply
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating reply: {str(e)}"
            }

    def type_reply_in_gmail(self, reply_text: str, send: bool = False) -> dict:
        """
        Type the reply into Gmail compose window using keyboard shortcuts

        Args:
            reply_text: The reply text to type
            send: Whether to send after typing

        Returns:
            Dict with success status
        """
        print("\n✉️  Opening Reply (keyboard shortcut 'r')...")
        self.gui.press_key('r')
        print("   ⏳ Waiting for compose window to open and auto-focus...")
        time.sleep(4)

        print("   ✏️  Gmail should have auto-focused the compose area")
        print("   📝 Typing AI-generated reply...")
        self.gui.type_text(reply_text, interval=0.02)

        if send:
            print("   📤 Sending email (Ctrl+Enter)...")
            time.sleep(1)
            self.gui.hotkey('ctrl', 'enter')
            time.sleep(2)
            print("   ✅ Email sent!")
            return {
                "success": True,
                "message": "✅ Reply typed and sent!"
            }
        else:
            print("   ⏸️  Reply typed - NOT sent (review it on screen)")
            return {
                "success": True,
                "message": "✅ Reply typed (NOT sent - review it first!)\n   💡 Press Tab+Enter in Gmail to send when ready"
            }

    def monitor_and_reply_visually(self, context: str = "professional", auto_send: bool = False) -> dict:
        """
        Complete visual workflow:
        1. Open Gmail
        2. Read first email from screen
        3. Generate AI reply
        4. Type reply (with your approval)

        Args:
            context: Reply style
            auto_send: If True, send automatically. If False, just type for your review

        Returns:
            Dict with workflow results
        """
        print("\n🤖 Starting Visual Chat Monitor Workflow...")
        print("=" * 60)

        self.open_gmail_in_browser()

        inbox_result = self.read_emails_from_screen()

        if not inbox_result["success"]:
            return inbox_result

        print("\n📧 Emails visible on screen:")
        print(inbox_result["analysis"])

        input("\n⏸️  Press ENTER to read the first email...")

        email_result = self.read_specific_email_on_screen(email_number=1)

        if not email_result["success"]:
            return email_result

        print("\n📖 Email Content:")
        print("=" * 60)
        print(email_result["content"])
        print("=" * 60)

        print("\n🤖 Generating AI reply...")
        reply_result = self.generate_ai_reply_for_email(
            email_result["content"],
            context
        )

        if not reply_result["success"]:
            return reply_result

        print("\n💬 AI Suggested Reply:")
        print("=" * 60)
        print(reply_result["suggested_reply"])
        print("=" * 60)

        approval = input("\n❓ Type 'yes' to type this reply in Gmail: ").strip().lower()

        if approval == 'yes':
            send_now = False
            if auto_send:
                send_confirm = input("   ❓ Also send it immediately? (yes/no): ").strip().lower()
                send_now = (send_confirm == 'yes')

            type_result = self.type_reply_in_gmail(
                reply_result["suggested_reply"],
                send=send_now
            )

            return {
                "success": True,
                "message": type_result["message"],
                "workflow_complete": True
            }
        else:
            return {
                "success": True,
                "message": "Reply canceled by user",
                "workflow_complete": False
            }

    def open_whatsapp_web(self):
        """Open WhatsApp Web in browser"""
        print("\n🌐 Opening WhatsApp Web...")
        webbrowser.open("https://web.whatsapp.com/")
        print("   ⏳ Waiting 10 seconds for WhatsApp to load...")
        print("   📱 Make sure you're logged in on your phone!")
        time.sleep(10)

        print("   🪟 Maximizing browser window...")
        self.gui.hotkey('win', 'up')
        time.sleep(1)

        return {"success": True, "message": "WhatsApp Web opened and maximized"}

    def read_whatsapp_from_screen(self) -> dict:
        """
        Take screenshot of WhatsApp and read messages with AI Vision

        Returns:
            Dict with messages found on screen
        """
        print("\n📸 Taking screenshot of WhatsApp...")
        screenshot_path = self.gui.screenshot("whatsapp_screen")

        if not screenshot_path:
            return {
                "success": False,
                "message": "❌ Screenshot feature not available in cloud environment. This feature requires running VATSAL locally on your desktop."
            }

        print("   🤖 Analyzing WhatsApp with AI Vision...")

        prompt = """Analyze this WhatsApp Web screenshot and extract:
1. Chat names/contacts visible
2. Recent message previews
3. Unread message indicators

Describe what you see in the WhatsApp interface."""

        analysis_result = analyze_screenshot(screenshot_path, prompt)

        if analysis_result:
            return {
                "success": True,
                "message": "WhatsApp analyzed",
                "analysis": analysis_result,
                "screenshot": screenshot_path
            }
        else:
            return {
                "success": False,
                "message": "Could not analyze WhatsApp"
            }


def create_visual_chat_monitor():
    """Factory function to create visual chat monitor"""
    return VisualChatMonitor()
