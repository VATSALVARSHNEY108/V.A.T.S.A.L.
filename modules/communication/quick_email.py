"""
Quick Email Tool - Send emails in seconds!
Super simple interface for fast email sending
"""

from email_sender import EmailSender
from datetime import datetime
import sys


def main():
    print("\n" + "=" * 70)
    print("📧 QUICK EMAIL SENDER")
    print("=" * 70)
    
    sender = EmailSender()
    
    # Get email details
    print("\n📝 Enter email details:")
    to = input("To (email address): ").strip()
    
    if not to:
        print("❌ Email address is required!")
        return
    
    subject = input("Subject: ").strip() or "No Subject"
    
    print("\nMessage (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and (not lines or lines[-1] == ""):
            break
        lines.append(line)
    
    message = "\n".join(lines).strip()
    
    if not message:
        message = "No message content"
    
    # Ask about attachment
    attachment = input("\nAttachment (file path, or press Enter to skip): ").strip()
    
    # Send email
    print("\n📤 Sending email...")
    
    if attachment:
        result = sender.send_email(
            to=[to],
            subject=subject,
            body=message,
            attachments=[attachment]
        )
    else:
        result = sender.send_simple_email(to, subject, message)
    
    print(f"\n{result['message']}")
    
    if result['success']:
        print("✅ Done!")
    else:
        print("❌ Failed!")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
