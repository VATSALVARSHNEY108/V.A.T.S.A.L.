import os
import base64
from typing import Optional, Dict
from contact_manager import ContactManager

class MessagingService:
    """Handles SMS and Email sending capabilities"""
    
    def __init__(self, contact_manager: ContactManager):
        self.contact_manager = contact_manager
        self.twilio_available = False
        self.gmail_available = False
        self.demo_mode = True
        
        self._check_integrations()
    
    def _check_integrations(self):
        """Check which messaging integrations are available"""
        if os.environ.get("TWILIO_ACCOUNT_SID") and os.environ.get("TWILIO_AUTH_TOKEN"):
            self.twilio_available = True
            self.demo_mode = False
        
        gmail_user = os.environ.get("GMAIL_USER") or os.environ.get("GMAIL_EMAIL")
        gmail_password = os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("GMAIL_PASSWORD")
        if gmail_user and gmail_password:
            self.gmail_available = True
            self.demo_mode = False
    
    def send_sms(self, contact_name: Optional[str] = None, phone: Optional[str] = None, message: str = "") -> Dict:
        """Send SMS to a contact"""
        if contact_name:
            phone = self.contact_manager.get_phone(contact_name)
            if not phone:
                return {
                    "success": False,
                    "message": f"No phone number found for contact: {contact_name}"
                }
        
        if not phone:
            return {
                "success": False,
                "message": "No phone number provided"
            }
        
        if self.demo_mode or not self.twilio_available:
            print(f"  [DEMO] Would send SMS to {phone}: '{message[:50]}...'")
            return {
                "success": True,
                "message": f"[DEMO] SMS would be sent to {phone}",
                "demo": True
            }
        
        try:
            from twilio.rest import Client
            client = Client(
                os.environ.get("TWILIO_ACCOUNT_SID"),
                os.environ.get("TWILIO_AUTH_TOKEN")
            )
            
            twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER")
            if not twilio_phone:
                return {
                    "success": False,
                    "message": "Twilio phone number not configured"
                }
            
            message_obj = client.messages.create(
                body=message,
                from_=twilio_phone,
                to=phone
            )
            
            return {
                "success": True,
                "message": f"SMS sent to {phone}",
                "sid": message_obj.sid
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending SMS: {str(e)}"
            }
    
    def send_email(self, contact_name: Optional[str] = None, email: Optional[str] = None, 
                   subject: str = "", body: str = "", 
                   attachment_path: Optional[str] = None) -> Dict:
        """Send email to a contact"""
        if contact_name:
            email = self.contact_manager.get_email(contact_name)
            if not email:
                return {
                    "success": False,
                    "message": f"No email address found for contact: {contact_name}"
                }
        
        if not email:
            return {
                "success": False,
                "message": "No email address provided"
            }
        
        if self.demo_mode or not self.gmail_available:
            attachment_msg = f" with attachment: {attachment_path}" if attachment_path else ""
            print(f"  [DEMO] Would send email to {email}")
            print(f"  [DEMO] Subject: {subject}")
            print(f"  [DEMO] Body: {body[:100]}...{attachment_msg}")
            return {
                "success": True,
                "message": f"[DEMO] Email would be sent to {email}",
                "demo": True
            }
        
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            
            gmail_user = os.environ.get("GMAIL_USER") or os.environ.get("GMAIL_EMAIL")
            gmail_password = os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("GMAIL_PASSWORD")
            
            if not gmail_user or not gmail_password:
                return {
                    "success": False,
                    "message": "Gmail credentials not configured. Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables."
                }
            
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 
                                  f'attachment; filename={os.path.basename(attachment_path)}')
                    msg.attach(part)
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()
            
            return {
                "success": True,
                "message": f"Email sent to {email}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }
    
    def send_file(self, contact_name: str, file_path: str, 
                  message: str = "", method: str = "auto") -> Dict:
        """Send a file to a contact via email or messaging app"""
        contact = self.contact_manager.get_contact(contact_name)
        
        if not contact:
            return {
                "success": False,
                "message": f"Contact not found: {contact_name}"
            }
        
        if not os.path.exists(file_path):
            return {
                "success": False,
                "message": f"File not found: {file_path}"
            }
        
        if method == "auto":
            if contact.get("email"):
                method = "email"
            elif contact.get("phone"):
                method = "sms"
            else:
                return {
                    "success": False,
                    "message": f"No contact method available for {contact_name}"
                }
        
        if method == "email":
            subject = f"File: {os.path.basename(file_path)}"
            body = message if message else f"Attached file: {os.path.basename(file_path)}"
            return self.send_email(
                contact_name=contact_name,
                subject=subject,
                body=body,
                attachment_path=file_path
            )
        elif method == "sms":
            msg = message if message else f"File: {file_path}"
            msg += f" (Note: File sharing via SMS requires MMS support)"
            return self.send_sms(contact_name=contact_name, message=msg)
        else:
            return {
                "success": False,
                "message": f"Unknown send method: {method}"
            }
