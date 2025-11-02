"""
📱 AI-Powered Chat Monitor & Auto-Reply System
Read incoming messages (Email, SMS) and generate AI-powered replies with user approval
"""

import os
import json
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from typing import List, Dict, Optional
from gemini_controller import get_client
from google.genai import types


class ChatMonitor:
    """Monitor incoming messages and generate AI-powered replies"""
    
    def __init__(self):
        """Initialize chat monitor"""
        self.gmail_user = os.environ.get("GMAIL_USER") or os.environ.get("GMAIL_EMAIL")
        self.gmail_password = os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("GMAIL_PASSWORD")
        self.twilio_available = False
        self.gmail_available = bool(self.gmail_user and self.gmail_password)
        
        if os.environ.get("TWILIO_ACCOUNT_SID") and os.environ.get("TWILIO_AUTH_TOKEN"):
            self.twilio_available = True
        
        self.pending_replies = []
        self.chat_history_file = "chat_monitor_history.json"
        self.load_history()
        
        print("📱 Chat Monitor initialized")
        if self.gmail_available:
            print("   ✅ Gmail reading enabled")
        else:
            print("   ⚠️  Gmail credentials not configured")
        
        if self.twilio_available:
            print("   ✅ SMS reading enabled (via Twilio)")
        else:
            print("   ⚠️  Twilio credentials not configured")
    
    def load_history(self):
        """Load chat monitoring history"""
        if os.path.exists(self.chat_history_file):
            try:
                with open(self.chat_history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = {"emails": [], "sms": [], "whatsapp": []}
        else:
            self.history = {"emails": [], "sms": [], "whatsapp": []}
    
    def save_history(self):
        """Save chat monitoring history"""
        try:
            with open(self.chat_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def read_unread_emails(self, max_emails: int = 10) -> List[Dict]:
        """
        Read unread emails from Gmail inbox
        
        Args:
            max_emails: Maximum number of emails to fetch
        
        Returns:
            List of email dicts with sender, subject, body, timestamp
        """
        if not self.gmail_available:
            return {
                "success": False,
                "message": "Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD.",
                "emails": []
            }
        
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.gmail_user, self.gmail_password)
            mail.select("inbox")
            
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != "OK":
                return {
                    "success": False,
                    "message": "Failed to search inbox",
                    "emails": []
                }
            
            email_ids = messages[0].split()
            
            if not email_ids:
                return {
                    "success": True,
                    "message": "No unread emails found",
                    "emails": []
                }
            
            unread_emails = []
            
            for email_id in email_ids[-max_emails:]:
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                
                if status != "OK":
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        subject = self._decode_email_header(msg["Subject"])
                        from_email = self._decode_email_header(msg["From"])
                        date = msg["Date"]
                        
                        body = self._get_email_body(msg)
                        
                        email_data = {
                            "id": email_id.decode(),
                            "from": from_email,
                            "subject": subject,
                            "body": body[:500],
                            "full_body": body,
                            "date": date,
                            "timestamp": datetime.now().isoformat(),
                            "platform": "email"
                        }
                        
                        unread_emails.append(email_data)
            
            mail.close()
            mail.logout()
            
            for em in unread_emails:
                self.history["emails"].append({
                    "from": em["from"],
                    "subject": em["subject"],
                    "body": em["body"],
                    "timestamp": em["timestamp"]
                })
            
            self.save_history()
            
            return {
                "success": True,
                "message": f"Found {len(unread_emails)} unread email(s)",
                "emails": unread_emails
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading emails: {str(e)}",
                "emails": []
            }
    
    def _decode_email_header(self, header: str) -> str:
        """Decode email header"""
        if not header:
            return ""
        
        decoded_parts = decode_header(header)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(encoding or 'utf-8')
                except:
                    decoded_string += part.decode('utf-8', errors='ignore')
            else:
                decoded_string += str(part)
        
        return decoded_string
    
    def _get_email_body(self, msg) -> str:
        """Extract email body content"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                body = str(msg.get_payload())
        
        return body.strip()
    
    def read_sms_messages(self, max_messages: int = 10) -> Dict:
        """
        Read recent SMS messages from Twilio
        
        Args:
            max_messages: Maximum number of messages to fetch
        
        Returns:
            Dict with success status and list of SMS messages
        """
        if not self.twilio_available:
            return {
                "success": False,
                "message": "Twilio credentials not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER.",
                "messages": []
            }
        
        try:
            from twilio.rest import Client
            
            client = Client(
                os.environ.get("TWILIO_ACCOUNT_SID"),
                os.environ.get("TWILIO_AUTH_TOKEN")
            )
            
            twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER")
            
            messages = client.messages.list(
                to=twilio_phone,
                limit=max_messages
            )
            
            sms_list = []
            
            for msg in messages:
                sms_data = {
                    "id": msg.sid,
                    "from": msg.from_,
                    "to": msg.to,
                    "body": msg.body,
                    "timestamp": msg.date_created.isoformat() if msg.date_created else None,
                    "status": msg.status,
                    "platform": "sms"
                }
                sms_list.append(sms_data)
                
                self.history["sms"].append({
                    "from": msg.from_,
                    "body": msg.body,
                    "timestamp": sms_data["timestamp"]
                })
            
            self.save_history()
            
            return {
                "success": True,
                "message": f"Found {len(sms_list)} recent SMS message(s)",
                "messages": sms_list
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading SMS: {str(e)}",
                "messages": []
            }
    
    def generate_ai_reply(self, message_data: Dict, context: str = "professional") -> Dict:
        """
        Generate AI-powered reply for a message
        
        Args:
            message_data: Dict with 'from', 'subject' (optional), 'body', 'platform'
            context: Reply context - 'professional', 'casual', 'friendly'
        
        Returns:
            Dict with suggested reply
        """
        try:
            client = get_client()
            
            platform = message_data.get("platform", "email")
            sender = message_data.get("from", "Unknown")
            subject = message_data.get("subject", "")
            body = message_data.get("body", "")
            
            if platform == "email":
                prompt = f"""You are an AI assistant helping to write a reply to an email.

**Email Details:**
From: {sender}
Subject: {subject}

**Email Content:**
{body}

**Instructions:**
- Write a {context} reply to this email
- Keep it concise and appropriate
- Match the tone of the original email
- Address the main points raised
- Sign off appropriately

Generate ONLY the reply text, no additional commentary."""
            
            elif platform == "sms":
                prompt = f"""You are an AI assistant helping to write a reply to an SMS text message.

**Message From:** {sender}
**Message Content:** {body}

**Instructions:**
- Write a brief, {context} reply (SMS style - concise)
- Keep it under 160 characters if possible
- Be friendly and clear
- Address the message content directly

Generate ONLY the reply text, no additional commentary."""
            
            else:
                prompt = f"""Reply to this message in a {context} tone:

From: {sender}
Message: {body}

Generate a concise, appropriate reply."""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=500
                )
            )
            
            suggested_reply = response.text.strip()
            
            if suggested_reply:
                reply_data = {
                    "success": True,
                    "suggested_reply": suggested_reply,
                    "platform": platform,
                    "recipient": sender,
                    "original_message": body[:200],
                    "context": context
                }
                
                self.pending_replies.append(reply_data)
                
                return reply_data
            else:
                return {
                    "success": False,
                    "message": "Failed to generate reply"
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating AI reply: {str(e)}"
            }
    
    def monitor_and_suggest_replies(self, platforms: List[str] = None, context: str = "professional") -> Dict:
        """
        Monitor all platforms and generate AI reply suggestions
        
        Args:
            platforms: List of platforms to monitor ['email', 'sms'] or None for all
            context: Reply context - 'professional', 'casual', 'friendly'
        
        Returns:
            Dict with all unread messages and suggested replies
        """
        if platforms is None:
            platforms = ['email', 'sms']
        
        results = {
            "emails": [],
            "sms": [],
            "suggested_replies": []
        }
        
        if 'email' in platforms and self.gmail_available:
            email_result = self.read_unread_emails(max_emails=5)
            if email_result["success"] and email_result["emails"]:
                results["emails"] = email_result["emails"]
                
                for email_data in email_result["emails"]:
                    reply = self.generate_ai_reply(email_data, context)
                    if reply.get("success"):
                        results["suggested_replies"].append(reply)
        
        if 'sms' in platforms and self.twilio_available:
            sms_result = self.read_sms_messages(max_messages=5)
            if sms_result["success"] and sms_result["messages"]:
                results["sms"] = sms_result["messages"]
                
                for sms_data in sms_result["messages"]:
                    reply = self.generate_ai_reply(sms_data, context)
                    if reply.get("success"):
                        results["suggested_replies"].append(reply)
        
        return results
    
    def approve_and_send_reply(self, reply_index: int, send_now: bool = True) -> Dict:
        """
        Approve a suggested reply and optionally send it
        
        Args:
            reply_index: Index of the reply in pending_replies
            send_now: Whether to send immediately or just approve
        
        Returns:
            Dict with approval/send status
        """
        if reply_index < 0 or reply_index >= len(self.pending_replies):
            return {
                "success": False,
                "message": f"Invalid reply index. Must be between 0 and {len(self.pending_replies)-1}"
            }
        
        reply_data = self.pending_replies[reply_index]
        
        if not send_now:
            return {
                "success": True,
                "message": "Reply approved but not sent",
                "reply_data": reply_data
            }
        
        platform = reply_data["platform"]
        recipient = reply_data["recipient"]
        reply_text = reply_data["suggested_reply"]
        
        if platform == "email":
            from email_sender import EmailSender
            email_sender = EmailSender()
            
            result = email_sender.send_simple_email(
                to=recipient,
                subject="Re: " + reply_data.get("subject", "Your message"),
                message=reply_text
            )
            
            if result["success"]:
                self.pending_replies.pop(reply_index)
            
            return result
        
        elif platform == "sms":
            from messaging_service import MessagingService
            from contact_manager import ContactManager
            
            contact_mgr = ContactManager()
            msg_service = MessagingService(contact_mgr)
            
            result = msg_service.send_sms(
                phone=recipient,
                message=reply_text
            )
            
            if result["success"]:
                self.pending_replies.pop(reply_index)
            
            return result
        
        else:
            return {
                "success": False,
                "message": f"Unsupported platform: {platform}"
            }
    
    def get_pending_replies(self) -> List[Dict]:
        """Get all pending replies waiting for approval"""
        return self.pending_replies
    
    def clear_pending_replies(self):
        """Clear all pending replies"""
        self.pending_replies = []
        return {"success": True, "message": "All pending replies cleared"}
    
    def get_chat_summary(self) -> Dict:
        """Get summary of monitored chats"""
        return {
            "total_emails_monitored": len(self.history["emails"]),
            "total_sms_monitored": len(self.history["sms"]),
            "pending_replies": len(self.pending_replies),
            "gmail_enabled": self.gmail_available,
            "sms_enabled": self.twilio_available
        }
