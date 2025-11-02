"""
Smart Typing Assistant Module
Automate repetitive typing, form filling, and text expansion
"""

import pyperclip
import json
import os
from datetime import datetime
import re

class SmartTyping:
    def __init__(self):
        self.snippets_file = "typing_snippets.json"
        self.templates_file = "form_templates.json"
        self.load_snippets()
        self.load_templates()
    
    def load_snippets(self):
        """Load text snippets/shortcuts"""
        if os.path.exists(self.snippets_file):
            with open(self.snippets_file, 'r') as f:
                self.snippets = json.load(f)
        else:
            self.snippets = {
                "//email": "your.email@example.com",
                "//phone": "+1234567890",
                "//addr": "123 Main St, City, State",
                "//sig": "Best regards,\nYour Name",
                "//meet": "Let's schedule a meeting to discuss this further.",
                "//thanks": "Thank you for your time and consideration.",
                "//brb": "Be right back",
                "//omw": "On my way"
            }
            self.save_snippets()
    
    def save_snippets(self):
        """Save text snippets"""
        with open(self.snippets_file, 'w') as f:
            json.dump(self.snippets, f, indent=2)
    
    def load_templates(self):
        """Load form templates"""
        if os.path.exists(self.templates_file):
            with open(self.templates_file, 'r') as f:
                self.templates = json.load(f)
        else:
            self.templates = {
                "job_application": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "address": "123 Main St",
                    "linkedin": "linkedin.com/in/johndoe"
                },
                "contact_form": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "subject": "General Inquiry",
                    "message": "Hello, I would like to..."
                }
            }
            self.save_templates()
    
    def save_templates(self):
        """Save form templates"""
        with open(self.templates_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
    
    def add_snippet(self, shortcut, text):
        """Add a new text snippet"""
        self.snippets[shortcut] = text
        self.save_snippets()
        return f"✅ Snippet added: {shortcut} → {text[:50]}..."
    
    def expand_snippet(self, text):
        """Expand shortcuts in text"""
        expanded = text
        for shortcut, replacement in self.snippets.items():
            expanded = expanded.replace(shortcut, replacement)
        return expanded
    
    def get_snippet(self, shortcut):
        """Get text for a specific shortcut"""
        if shortcut in self.snippets:
            return self.snippets[shortcut]
        return None
    
    def list_snippets(self):
        """List all available snippets"""
        result = "📝 Text Snippets:\n"
        for shortcut, text in self.snippets.items():
            preview = text[:40] + "..." if len(text) > 40 else text
            result += f"  {shortcut} → {preview}\n"
        return result
    
    def add_template(self, name, fields):
        """Add a form template"""
        self.templates[name] = fields
        self.save_templates()
        return f"✅ Template '{name}' added with {len(fields)} fields"
    
    def get_template(self, name):
        """Get a form template"""
        return self.templates.get(name, {})
    
    def fill_form(self, template_name):
        """Get form data ready to paste"""
        template = self.get_template(template_name)
        if not template:
            return f"❌ Template '{template_name}' not found"
        
        result = ""
        for field, value in template.items():
            result += f"{field}: {value}\n"
        
        pyperclip.copy(result)
        return f"✅ Form data copied to clipboard:\n{result}"
    
    def list_templates(self):
        """List all form templates"""
        result = "📋 Form Templates:\n"
        for name, fields in self.templates.items():
            result += f"  • {name} ({len(fields)} fields)\n"
        return result
    
    def smart_date(self, format_type="today"):
        """Generate smart date strings"""
        now = datetime.now()
        
        formats = {
            "today": now.strftime("%Y-%m-%d"),
            "date": now.strftime("%B %d, %Y"),
            "time": now.strftime("%H:%M"),
            "datetime": now.strftime("%Y-%m-%d %H:%M"),
            "timestamp": now.strftime("%Y%m%d_%H%M%S"),
            "full": now.strftime("%A, %B %d, %Y at %I:%M %p")
        }
        
        return formats.get(format_type, formats["today"])
    
    def generate_email_template(self, email_type="professional"):
        """Generate email templates"""
        templates = {
            "professional": f"""Dear [Recipient Name],

I hope this email finds you well.

[Your message here]

Best regards,
[Your Name]
{self.smart_date('date')}""",
            
            "casual": f"""Hi [Name],

[Your message]

Thanks!
[Your Name]""",
            
            "followup": f"""Hi [Name],

I wanted to follow up on [previous topic]. 

[Follow-up message]

Looking forward to hearing from you.

Best,
[Your Name]""",
            
            "thank_you": f"""Dear [Name],

Thank you for [what they did]. I really appreciate [specific detail].

[Additional message]

Warm regards,
[Your Name]"""
        }
        
        template = templates.get(email_type, templates["professional"])
        pyperclip.copy(template)
        return f"✅ Email template copied:\n{template}"
    
    def auto_correct_common_typos(self, text):
        """Auto-correct common typing mistakes"""
        corrections = {
            r'\bteh\b': 'the',
            r'\badn\b': 'and',
            r'\byoru\b': 'your',
            r'\btaht\b': 'that',
            r'\bwoudl\b': 'would',
            r'\bcoudl\b': 'could',
            r'\bshoudl\b': 'should',
            r'\brecieve\b': 'receive',
            r'\boccured\b': 'occurred',
            r'\bseperate\b': 'separate'
        }
        
        corrected = text
        for wrong, right in corrections.items():
            corrected = re.sub(wrong, right, corrected, flags=re.IGNORECASE)
        
        return corrected
    
    def generate_password(self, length=16):
        """Generate a strong password"""
        import random
        import string
        
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        pyperclip.copy(password)
        return f"✅ Strong password generated and copied to clipboard"
    
    def generate_lorem(self, paragraphs=1):
        """Generate lorem ipsum text"""
        lorem = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        ]
        
        text = "\n\n".join(lorem[:paragraphs])
        pyperclip.copy(text)
        return f"✅ Lorem ipsum ({paragraphs} paragraph{'s' if paragraphs > 1 else ''}) copied to clipboard"

if __name__ == "__main__":
    assistant = SmartTyping()
    print("Smart Typing Assistant - Testing")
    print(assistant.list_snippets())
    print("\n")
    print(assistant.list_templates())
