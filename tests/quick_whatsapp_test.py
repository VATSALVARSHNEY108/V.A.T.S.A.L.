"""
Quick WhatsApp Desktop Test
Opens a specific contact in WhatsApp
"""

from whatsapp_automation import create_whatsapp_automation
import sys

def main():
    print("=" * 60)
    print("📱 WhatsApp Desktop - Quick Contact Opener")
    print("=" * 60)
    
    # Get phone number
    if len(sys.argv) > 1:
        phone = sys.argv[1]
    else:
        phone = input("\n📞 Enter phone number with country code (e.g., +1234567890): ").strip()
    
    # Get message (optional)
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
    else:
        message = input("💬 Enter message (or press Enter to skip): ").strip()
    
    # Create WhatsApp automation
    wa = create_whatsapp_automation()
    
    print("\n🚀 Opening WhatsApp...\n")
    
    # Open chat
    if message:
        result = wa.open_chat_in_desktop(phone, message)
    else:
        result = wa.open_chat_in_desktop(phone)
    
    print(result["message"])
    
    print("\n" + "=" * 60)
    print("📝 Note: A browser tab will open and redirect to WhatsApp Desktop")
    print("   Click 'Open WhatsApp Desktop' when prompted by your browser")
    print("=" * 60)


if __name__ == "__main__":
    main()
