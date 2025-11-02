"""
Enhanced Email Sender
Easy-to-use email tool with HTML support, templates, and multiple recipients
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional


class EmailSender:
    """Enhanced email sending with HTML support and templates"""
    
    def __init__(self):
        """Initialize email sender"""
        self.gmail_user = os.environ.get("GMAIL_USER") or os.environ.get("GMAIL_EMAIL")
        self.gmail_password = os.environ.get("GMAIL_APP_PASSWORD") or os.environ.get("GMAIL_PASSWORD")
        self.demo_mode = not (self.gmail_user and self.gmail_password)
        
        if self.demo_mode:
            print("📧 Email Sender (DEMO MODE - credentials not configured)")
        else:
            print(f"📧 Email Sender ready (sending from: {self.gmail_user})")
    
    def send_simple_email(self, to: str, subject: str, message: str) -> dict:
        """
        Send a simple text email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            message: Email body (plain text)
        
        Returns:
            Result dict with success status
        """
        return self.send_email(
            to=[to],
            subject=subject,
            body=message,
            html=False
        )
    
    def send_html_email(self, to: str, subject: str, html_content: str) -> dict:
        """
        Send an HTML formatted email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            html_content: HTML email body
        
        Returns:
            Result dict with success status
        """
        return self.send_email(
            to=[to],
            subject=subject,
            body=html_content,
            html=True
        )
    
    def send_email(self, 
                   to: List[str],
                   subject: str,
                   body: str,
                   html: bool = False,
                   cc: Optional[List[str]] = None,
                   bcc: Optional[List[str]] = None,
                   attachments: Optional[List[str]] = None) -> dict:
        """
        Send email with full features: HTML, CC, BCC, attachments.
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Email body (plain text or HTML)
            html: If True, body is treated as HTML
            cc: List of CC email addresses
            bcc: List of BCC email addresses
            attachments: List of file paths to attach
        
        Returns:
            Result dict with success status and message
        """
        if not to:
            return {
                "success": False,
                "message": "No recipient email provided"
            }
        
        # Convert single email to list
        if isinstance(to, str):
            to = [to]
        
        if self.demo_mode:
            print(f"\n  [DEMO] Would send email:")
            print(f"  To: {', '.join(to)}")
            if cc:
                print(f"  CC: {', '.join(cc)}")
            if bcc:
                print(f"  BCC: {', '.join(bcc)}")
            print(f"  Subject: {subject}")
            print(f"  Body Type: {'HTML' if html else 'Plain Text'}")
            print(f"  Body Preview: {body[:100]}...")
            if attachments:
                print(f"  Attachments: {', '.join(attachments)}")
            print()
            return {
                "success": True,
                "message": f"[DEMO] Email would be sent to {len(to)} recipient(s)",
                "demo": True
            }
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.gmail_user
            msg['To'] = ', '.join(to)
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Add body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition',
                                          f'attachment; filename={os.path.basename(file_path)}')
                            msg.attach(part)
                    else:
                        print(f"  ⚠️  Attachment not found: {file_path}")
            
            # Send email
            print(f"  📤 Sending email to {len(to)} recipient(s)...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            
            # Combine all recipients for actual sending
            all_recipients = to.copy()
            if cc:
                all_recipients.extend(cc)
            if bcc:
                all_recipients.extend(bcc)
            
            server.send_message(msg, to_addrs=all_recipients)
            server.quit()
            
            print(f"  ✅ Email sent successfully!")
            
            return {
                "success": True,
                "message": f"Email sent to {len(to)} recipient(s)"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }
    
    def send_template_email(self, to: str, template: str, **kwargs) -> dict:
        """
        Send email using a pre-defined template.
        
        Args:
            to: Recipient email address
            template: Template name ('welcome', 'notification', 'report', 'invitation')
            **kwargs: Template variables (name, message, etc.)
        
        Returns:
            Result dict with success status
        """
        templates = {
            'welcome': {
                'subject': 'Welcome!',
                'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #4CAF50;">Welcome, {name}!</h2>
                    <p>{message}</p>
                    <p>We're excited to have you on board.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">This is an automated message.</p>
                </body>
                </html>
                '''
            },
            'notification': {
                'subject': 'Notification: {title}',
                'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #2196F3;">🔔 {title}</h2>
                    <p>{message}</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">Sent at {time}</p>
                </body>
                </html>
                '''
            },
            'report': {
                'subject': 'Report: {title}',
                'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #FF9800;">📊 {title}</h2>
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                        <p><strong>Summary:</strong></p>
                        <p>{summary}</p>
                    </div>
                    <p>{details}</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">Generated automatically</p>
                </body>
                </html>
                '''
            },
            'invitation': {
                'subject': 'You\'re Invited: {event}',
                'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #E91E63;">🎉 You're Invited!</h2>
                    <p>Hi {name},</p>
                    <p>You're invited to: <strong>{event}</strong></p>
                    <p><strong>Date:</strong> {date}</p>
                    <p><strong>Time:</strong> {time}</p>
                    <p><strong>Location:</strong> {location}</p>
                    <p>{message}</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">Please RSVP by {rsvp_date}</p>
                </body>
                </html>
                '''
            }
        }
        
        if template not in templates:
            return {
                "success": False,
                "message": f"Unknown template: {template}. Available: {', '.join(templates.keys())}"
            }
        
        template_data = templates[template]
        subject = template_data['subject'].format(**kwargs)
        html_body = template_data['html'].format(**kwargs)
        
        return self.send_html_email(to, subject, html_body)


def create_email_sender():
    """Factory function to create EmailSender instance"""
    return EmailSender()


if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    print("=" * 70)
    print("📧 EMAIL SENDER")
    print("=" * 70)
    
    sender = EmailSender()
    
    if sender.demo_mode:
        print("\n⚠️  DEMO MODE: Gmail credentials not configured")
        print("To send real emails, set these environment variables:")
        print("  - GMAIL_USER (your Gmail address)")
        print("  - GMAIL_APP_PASSWORD (Gmail app-specific password)")
        print("\nRunning demo with example data...\n")
        
        # Demo examples
        sender.send_simple_email(
            to="example@example.com",
            subject="Test Email",
            message="This is a test message!"
        )
        
        sender.send_template_email(
            to="example@example.com",
            template="notification",
            title="System Alert",
            message="Your report is ready!",
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    else:
        print("\nChoose an option:")
        print("1. Send simple email")
        print("2. Send HTML email")
        print("3. Send with template")
        print("4. Send with attachment")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            to = input("To: ").strip()
            subject = input("Subject: ").strip()
            message = input("Message: ").strip()
            
            result = sender.send_simple_email(to, subject, message)
            print(f"\n{result['message']}")
        
        elif choice == "2":
            to = input("To: ").strip()
            subject = input("Subject: ").strip()
            print("Enter HTML content (or press Enter for default):")
            html = input().strip()
            
            if not html:
                html = f"<h1>Hello!</h1><p>This is a test HTML email sent at {datetime.now()}</p>"
            
            result = sender.send_html_email(to, subject, html)
            print(f"\n{result['message']}")
        
        elif choice == "3":
            to = input("To: ").strip()
            print("Templates: welcome, notification, report, invitation")
            template = input("Template: ").strip()
            
            if template == "welcome":
                name = input("Name: ").strip()
                message = input("Message: ").strip()
                result = sender.send_template_email(to, template, name=name, message=message)
            
            elif template == "notification":
                title = input("Title: ").strip()
                message = input("Message: ").strip()
                result = sender.send_template_email(
                    to, template,
                    title=title,
                    message=message,
                    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            
            print(f"\n{result['message']}")
        
        elif choice == "4":
            to = input("To: ").strip()
            subject = input("Subject: ").strip()
            message = input("Message: ").strip()
            attachment = input("Attachment path: ").strip()
            
            result = sender.send_email(
                to=[to],
                subject=subject,
                body=message,
                attachments=[attachment] if attachment else None
            )
            print(f"\n{result['message']}")
    
    print("\n" + "=" * 70)
