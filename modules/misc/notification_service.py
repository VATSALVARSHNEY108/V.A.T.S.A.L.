#!/usr/bin/env python3
"""
Push Notification Service for VATSAL Mobile Companion
Supports SMS (Twilio), Email, and Webhook notifications
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


class NotificationService:
    def __init__(self):
        self.twilio_configured = False
        self.email_configured = False
        self.webhook_url = os.getenv('NOTIFICATION_WEBHOOK_URL')
        self.notification_history = []
        self.max_history = 100
        
        self._check_configurations()
    
    def _check_configurations(self):
        """Check which notification methods are configured"""
        twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_configured = bool(twilio_sid and twilio_token)
        
        email = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_PASSWORD')
        self.email_configured = bool(email and email_password)
    
    def send_sms(self, phone_number, message):
        """Send SMS notification via Twilio"""
        if not self.twilio_configured:
            return {
                'success': False,
                'error': 'Twilio not configured. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN'
            }
        
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_PHONE_NUMBER')
            
            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                body=message,
                from_=from_number,
                to=phone_number
            )
            
            self._log_notification('sms', phone_number, message.body, True)
            
            return {
                'success': True,
                'message_sid': message.sid,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self._log_notification('sms', phone_number, str(e), False)
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_email(self, to_email, subject, message):
        """Send email notification"""
        if not self.email_configured:
            return {
                'success': False,
                'error': 'Email not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD'
            }
        
        try:
            from_email = os.getenv('EMAIL_ADDRESS')
            password = os.getenv('EMAIL_PASSWORD')
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = f'[VATSAL] {subject}'
            
            body = f"""
VATSAL Desktop Automation Alert

{message}

---
Sent from VATSAL Mobile Companion
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            
            self._log_notification('email', to_email, subject, True)
            
            return {
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self._log_notification('email', to_email, str(e), False)
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_webhook(self, data):
        """Send webhook notification"""
        if not self.webhook_url:
            return {
                'success': False,
                'error': 'Webhook URL not configured. Set NOTIFICATION_WEBHOOK_URL'
            }
        
        try:
            payload = {
                'timestamp': datetime.now().isoformat(),
                'source': 'VATSAL Desktop Automation',
                'data': data
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            self._log_notification('webhook', self.webhook_url, str(data), response.ok)
            
            return {
                'success': response.ok,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self._log_notification('webhook', self.webhook_url, str(e), False)
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_push_notification(self, title, message, priority='normal', recipients=None):
        """Send push notification to configured channels"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'title': title,
            'message': message,
            'priority': priority,
            'channels': {}
        }
        
        if recipients is None:
            recipients = {}
        
        phone = recipients.get('phone') or os.getenv('NOTIFICATION_PHONE')
        if phone and self.twilio_configured:
            sms_text = f"[{priority.upper()}] {title}\n{message}"
            results['channels']['sms'] = self.send_sms(phone, sms_text)
        
        email = recipients.get('email') or os.getenv('NOTIFICATION_EMAIL')
        if email and self.email_configured:
            results['channels']['email'] = self.send_email(email, title, message)
        
        if self.webhook_url:
            webhook_data = {
                'title': title,
                'message': message,
                'priority': priority
            }
            results['channels']['webhook'] = self.send_webhook(webhook_data)
        
        if not results['channels']:
            results['warning'] = 'No notification channels configured'
        
        return results
    
    def notify_event(self, event_type, details, priority='normal'):
        """Send notification for specific event type"""
        event_messages = {
            'command_completed': lambda d: (
                'Command Completed',
                f"✅ Successfully executed: {d.get('command', 'Unknown')}"
            ),
            'command_failed': lambda d: (
                'Command Failed',
                f"❌ Failed to execute: {d.get('command', 'Unknown')}\nError: {d.get('error', 'Unknown error')}"
            ),
            'system_alert': lambda d: (
                'System Alert',
                f"⚠️ {d.get('alert', 'System alert detected')}"
            ),
            'security_alert': lambda d: (
                'Security Alert',
                f"🔒 {d.get('alert', 'Security event detected')}"
            ),
            'error': lambda d: (
                'System Error',
                f"❌ {d.get('message', 'An error occurred')}"
            ),
            'reminder': lambda d: (
                'Reminder',
                f"⏰ {d.get('message', 'You have a reminder')}"
            ),
            'task_complete': lambda d: (
                'Task Complete',
                f"✅ {d.get('task', 'Task completed successfully')}"
            )
        }
        
        if event_type not in event_messages:
            title = 'VATSAL Notification'
            message = str(details)
        else:
            title, message = event_messages[event_type](details)
        
        return self.send_push_notification(title, message, priority)
    
    def _log_notification(self, method, recipient, content, success):
        """Log notification attempt"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'recipient': recipient,
            'content': content[:100],
            'success': success
        }
        
        self.notification_history.append(log_entry)
        
        if len(self.notification_history) > self.max_history:
            self.notification_history.pop(0)
    
    def get_notification_history(self, limit=20):
        """Get recent notification history"""
        return {
            'success': True,
            'history': self.notification_history[-limit:],
            'total': len(self.notification_history)
        }
    
    def get_status(self):
        """Get notification service status"""
        return {
            'success': True,
            'configured_channels': {
                'sms': self.twilio_configured,
                'email': self.email_configured,
                'webhook': bool(self.webhook_url)
            },
            'total_notifications': len(self.notification_history)
        }


notification_service = NotificationService()


if __name__ == '__main__':
    service = NotificationService()
    print('📱 VATSAL Notification Service')
    print('=' * 50)
    status = service.get_status()
    print(f"SMS (Twilio): {'✅ Configured' if status['configured_channels']['sms'] else '❌ Not configured'}")
    print(f"Email: {'✅ Configured' if status['configured_channels']['email'] else '❌ Not configured'}")
    print(f"Webhook: {'✅ Configured' if status['configured_channels']['webhook'] else '❌ Not configured'}")
