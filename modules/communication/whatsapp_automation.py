"""
WhatsApp Automation Module
Send messages via WhatsApp Web and Desktop
"""

import time
import webbrowser
import subprocess
import platform
import os
from urllib.parse import quote

try:
    import pywhatkit as pwk
    PYWHATKIT_AVAILABLE = True
except Exception as e:
    print(f"⚠️  PyWhatKit not available: {e}")
    print("WhatsApp automation will use web-based method")
    pwk = None
    PYWHATKIT_AVAILABLE = False


class WhatsAppAutomation:
    """Handles WhatsApp messaging automation"""
    
    def __init__(self):
        """Initialize WhatsApp automation"""
        print("📱 WhatsApp automation ready")
    
    def send_message_instantly(self, phone_number, message):
        """
        Send WhatsApp message instantly to a phone number.
        
        Args:
            phone_number: Phone number with country code (e.g., "+1234567890")
            message: Message text to send
        
        Returns:
            Success status and message
        """
        if not PYWHATKIT_AVAILABLE:
            print(f"  📱 Using WhatsApp Web (desktop automation not available)")
            print(f"  💬 Message: {message}")
            return self._send_via_web(phone_number, message)
        
        try:
            print(f"  📱 Sending WhatsApp message to {phone_number}")
            print(f"  💬 Message: {message}")
            
            pwk.sendwhatmsg_instantly(
                phone_no=phone_number,
                message=message,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp message sent to {phone_number}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error sending WhatsApp message: {str(e)}"
            }
    
    def _send_via_web(self, phone_number, message):
        """Send message via WhatsApp Web URL"""
        try:
            if not phone_number or not isinstance(phone_number, str):
                return {
                    "success": False,
                    "message": "❌ Invalid phone number provided"
                }
            
            if message is None:
                message = ""
            
            clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "")
            
            if not clean_number or not clean_number.isdigit():
                return {
                    "success": False,
                    "message": f"❌ Invalid phone number format: {phone_number}. Use format: +1234567890"
                }
            
            encoded_message = quote(str(message))
            url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_message}"
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"✅ Opened WhatsApp Web for {phone_number}. Please press Enter in the browser to send."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error opening WhatsApp Web: {str(e)}"
            }
    
    def send_message_scheduled(self, phone_number, message, hour, minute):
        """
        Schedule a WhatsApp message for a specific time.
        
        Args:
            phone_number: Phone number with country code
            message: Message text to send
            hour: Hour in 24h format (0-23)
            minute: Minute (0-59)
        
        Returns:
            Success status and message
        """
        if not PYWHATKIT_AVAILABLE:
            print(f"  ⚠️  Scheduled messages not available in web mode")
            print(f"  📱 Opening WhatsApp Web instead (you can send manually)")
            return self._send_via_web(phone_number, message)
        
        try:
            print(f"  📱 Scheduling WhatsApp message to {phone_number}")
            print(f"  ⏰ Scheduled for: {hour}:{minute:02d}")
            print(f"  💬 Message: {message}")
            
            pwk.sendwhatmsg(
                phone_no=phone_number,
                message=message,
                time_hour=hour,
                time_min=minute,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp message scheduled for {hour}:{minute:02d}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error scheduling WhatsApp message: {str(e)}"
            }
    
    def send_to_group_instantly(self, group_id, message):
        """
        Send WhatsApp message to a group instantly.
        
        Args:
            group_id: WhatsApp group ID (from invite link)
            message: Message text to send
        
        Returns:
            Success status and message
        """
        if not PYWHATKIT_AVAILABLE:
            return {
                "success": False,
                "message": "❌ Group messaging requires desktop automation. Please use WhatsApp Web/Desktop manually for group messages."
            }
        
        try:
            print(f"  📱 Sending WhatsApp message to group")
            print(f"  💬 Message: {message}")
            
            pwk.sendwhatmsg_to_group_instantly(
                group_id=group_id,
                message=message,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp message sent to group"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error sending WhatsApp group message: {str(e)}"
            }
    
    def send_image(self, phone_number, image_path, caption=""):
        """
        Send an image via WhatsApp.
        
        Args:
            phone_number: Phone number with country code
            image_path: Path to the image file (JPG only, PNG not supported)
            caption: Optional image caption
        
        Returns:
            Success status and message
        """
        if not PYWHATKIT_AVAILABLE:
            return {
                "success": False,
                "message": "❌ Image sending requires desktop automation. Please use WhatsApp Web/Desktop manually to send images."
            }
        
        try:
            print(f"  📱 Sending WhatsApp image to {phone_number}")
            print(f"  🖼️  Image: {image_path}")
            if caption:
                print(f"  💬 Caption: {caption}")
            
            pwk.sendwhats_image(
                receiver=phone_number,
                img_path=image_path,
                caption=caption,
                wait_time=15,
                tab_close=True
            )
            
            return {
                "success": True,
                "message": f"✅ WhatsApp image sent to {phone_number}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error sending WhatsApp image: {str(e)}"
            }


    def open_whatsapp_desktop(self):
        """
        Open WhatsApp Desktop application directly.
        
        Returns:
            Success status and message
        """
        try:
            system = platform.system()
            
            if system == "Windows":
                print("  💻 Opening WhatsApp Desktop on Windows...")
                subprocess.Popen(["start", "whatsapp://"], shell=True)
            
            elif system == "Darwin":
                print("  💻 Opening WhatsApp Desktop on Mac...")
                subprocess.Popen(["open", "whatsapp://"])
            
            elif system == "Linux":
                print("  💻 Opening WhatsApp Desktop on Linux...")
                subprocess.Popen(["xdg-open", "whatsapp://"])
            
            else:
                return {
                    "success": False,
                    "message": f"❌ Unsupported operating system: {system}"
                }
            
            return {
                "success": True,
                "message": "✅ WhatsApp Desktop opened successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error opening WhatsApp Desktop: {str(e)}"
            }
    
    def open_chat_in_desktop(self, phone_number, message=None):
        """
        Open WhatsApp Desktop and navigate to a specific chat.
        Optionally pre-fill a message.
        
        Args:
            phone_number: Phone number with country code (e.g., "+1234567890")
            message: Optional message to pre-fill
        
        Returns:
            Success status and message
        """
        try:
            phone_clean = phone_number.replace("+", "").replace(" ", "").replace("-", "")
            
            if message:
                encoded_message = quote(message)
                url = f"https://wa.me/{phone_clean}?text={encoded_message}"
                print(f"  💻 Opening WhatsApp chat with {phone_number}")
                print(f"  💬 Pre-filled message: {message}")
            else:
                url = f"https://wa.me/{phone_clean}"
                print(f"  💻 Opening WhatsApp chat with {phone_number}")
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"✅ WhatsApp chat opened with {phone_number}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error opening WhatsApp chat: {str(e)}"
            }
    
    def launch_desktop_app(self):
        """
        Launch WhatsApp Desktop application using executable path.
        Alternative method if URL scheme doesn't work.
        
        Returns:
            Success status and message
        """
        try:
            system = platform.system()
            
            if system == "Windows":
                app_paths = [
                    os.path.join(os.environ.get("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe"),
                    os.path.join(os.environ.get("PROGRAMFILES", ""), "WhatsApp", "WhatsApp.exe"),
                    os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "WhatsApp", "WhatsApp.exe"),
                ]
                
                for path in app_paths:
                    if os.path.exists(path):
                        print(f"  💻 Launching WhatsApp from: {path}")
                        subprocess.Popen([path])
                        return {
                            "success": True,
                            "message": "✅ WhatsApp Desktop launched successfully"
                        }
                
                return {
                    "success": False,
                    "message": "❌ WhatsApp Desktop not found. Please install it from whatsapp.com/download"
                }
            
            elif system == "Darwin":
                app_path = "/Applications/WhatsApp.app"
                if os.path.exists(app_path):
                    print(f"  💻 Launching WhatsApp from: {app_path}")
                    subprocess.Popen(["open", "-a", "WhatsApp"])
                    return {
                        "success": True,
                        "message": "✅ WhatsApp Desktop launched successfully"
                    }
                else:
                    return {
                        "success": False,
                        "message": "❌ WhatsApp Desktop not found. Please install it from whatsapp.com/download"
                    }
            
            elif system == "Linux":
                try:
                    subprocess.Popen(["whatsapp"])
                    return {
                        "success": True,
                        "message": "✅ WhatsApp Desktop launched successfully"
                    }
                except FileNotFoundError:
                    return {
                        "success": False,
                        "message": "❌ WhatsApp Desktop not found. Please install it"
                    }
            
            else:
                return {
                    "success": False,
                    "message": f"❌ Unsupported operating system: {system}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error launching WhatsApp Desktop: {str(e)}"
            }


def create_whatsapp_automation():
    """
    Factory function to create WhatsAppAutomation instance.
    
    Returns:
        WhatsAppAutomation instance
    """
    return WhatsAppAutomation()
