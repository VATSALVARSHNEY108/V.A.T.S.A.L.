"""
Password Vault Module
Secure password storage and management with encryption
"""

import json
import os
import secrets
import string
from cryptography.fernet import Fernet
from datetime import datetime
import hashlib

class PasswordVault:
    def __init__(self, master_password=None):
        self.vault_file = "password_vault.json"
        self.key_file = ".vault_key"
        self.master_password = master_password
        self.cipher = self._load_or_create_key()
        self.load_vault()
        self.is_locked = True
    
    def _load_or_create_key(self):
        """Load or create encryption key - WARNING: Basic protection only"""
        try:
            import os
            
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    key = f.read()
            else:
                key = Fernet.generate_key()
                
                os.chmod('.', 0o755)
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                os.chmod(self.key_file, 0o600)
            
            return Fernet(key)
        except Exception:
            key = Fernet.generate_key()
            return Fernet(key)
    
    def load_vault(self):
        """Load password vault"""
        try:
            if os.path.exists(self.vault_file):
                with open(self.vault_file, 'r') as f:
                    encrypted_data = json.load(f)
                    self.vault = {}
                    
                    for name, encrypted_pass in encrypted_data.items():
                        try:
                            decrypted = self.cipher.decrypt(encrypted_pass.encode()).decode()
                            self.vault[name] = json.loads(decrypted)
                        except:
                            pass
            else:
                self.vault = {}
        except Exception:
            self.vault = {}
    
    def save_vault(self):
        """Save password vault with encryption"""
        try:
            encrypted_data = {}
            
            for name, data in self.vault.items():
                json_data = json.dumps(data)
                encrypted = self.cipher.encrypt(json_data.encode()).decode()
                encrypted_data[name] = encrypted
            
            with open(self.vault_file, 'w') as f:
                json.dump(encrypted_data, f, indent=2)
            
            return True
        except Exception as e:
            return False
    
    def add_password(self, name, username, password, url="", notes=""):
        """Add a new password to vault"""
        if name.lower() in [n.lower() for n in self.vault.keys()]:
            return f"⚠️ Entry '{name}' already exists! Use update to modify it."
        
        self.vault[name] = {
            'username': username,
            'password': password,
            'url': url,
            'notes': notes,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.save_vault()
        
        output = f"\n{'='*50}\n"
        output += f"🔐 PASSWORD SAVED\n"
        output += f"{'='*50}\n\n"
        output += f"✅ {name} has been added to your vault!\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_password(self, name):
        """Retrieve a password from vault - SECURITY: Consider implementing access confirmation"""
        for vault_name, data in self.vault.items():
            if vault_name.lower() == name.lower():
                output = f"\n{'='*50}\n"
                output += f"🔐 PASSWORD DETAILS\n"
                output += f"{'='*50}\n\n"
                output += f"⚠️ WARNING: Password will be shown in plaintext\n\n"
                output += f"Name: {vault_name}\n"
                output += f"Username: {data['username']}\n"
                output += f"Password: {data['password']}\n"
                
                if data.get('url'):
                    output += f"URL: {data['url']}\n"
                if data.get('notes'):
                    output += f"Notes: {data['notes']}\n"
                
                output += f"\nCreated: {data['created']}\n"
                output += f"{'='*50}\n"
                output += f"⚠️ Remember: Keep this information secure!\n"
                output += f"{'='*50}\n"
                
                return output
        
        return f"⚠️ No password found for '{name}'"
    
    def update_password(self, name, username=None, password=None, url=None, notes=None):
        """Update an existing password"""
        for vault_name in self.vault.keys():
            if vault_name.lower() == name.lower():
                if username:
                    self.vault[vault_name]['username'] = username
                if password:
                    self.vault[vault_name]['password'] = password
                if url:
                    self.vault[vault_name]['url'] = url
                if notes:
                    self.vault[vault_name]['notes'] = notes
                
                self.vault[vault_name]['modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_vault()
                
                return f"✅ Password for '{vault_name}' has been updated!"
        
        return f"⚠️ No password found for '{name}'"
    
    def delete_password(self, name):
        """Delete a password from vault"""
        for vault_name in list(self.vault.keys()):
            if vault_name.lower() == name.lower():
                del self.vault[vault_name]
                self.save_vault()
                
                return f"🗑️ Password for '{vault_name}' has been deleted!"
        
        return f"⚠️ No password found for '{name}'"
    
    def list_passwords(self):
        """List all saved passwords - passwords hidden for security"""
        if not self.vault:
            return "📭 Your password vault is empty."
        
        output = f"\n{'='*50}\n"
        output += f"🔐 PASSWORD VAULT\n"
        output += f"{'='*50}\n\n"
        
        for i, (name, data) in enumerate(self.vault.items(), 1):
            output += f"{i}. {name}\n"
            output += f"   👤 Username: {data['username']}\n"
            output += f"   🔒 Password: ••••••••\n"
            
            if data.get('url'):
                output += f"   🌐 URL: {data['url']}\n"
            
            output += f"\n"
        
        output += f"{'='*50}\n"
        output += f"Total Entries: {len(self.vault)}\n"
        output += f"💡 Use 'get password for [name]' to view passwords\n"
        output += f"{'='*50}\n"
        
        return output
    
    def generate_strong_password(self, length=16, include_symbols=True, include_numbers=True):
        """Generate a strong random password"""
        characters = string.ascii_letters
        
        if include_numbers:
            characters += string.digits
        
        if include_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        strength = self._check_password_strength(password)
        
        output = f"\n{'='*50}\n"
        output += f"🔑 GENERATED PASSWORD\n"
        output += f"{'='*50}\n\n"
        output += f"Password: {password}\n"
        output += f"Length: {length} characters\n"
        output += f"Strength: {strength}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def check_password_strength(self, password):
        """Check password strength"""
        strength = self._check_password_strength(password)
        
        output = f"\n{'='*50}\n"
        output += f"🔒 PASSWORD STRENGTH ANALYSIS\n"
        output += f"{'='*50}\n\n"
        output += f"Password Length: {len(password)} characters\n"
        output += f"Strength: {strength}\n"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        output += f"\n✓ Uppercase: {'Yes' if has_upper else 'No'}\n"
        output += f"✓ Lowercase: {'Yes' if has_lower else 'No'}\n"
        output += f"✓ Numbers: {'Yes' if has_digit else 'No'}\n"
        output += f"✓ Symbols: {'Yes' if has_symbol else 'No'}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def _check_password_strength(self, password):
        """Internal password strength checker"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        
        if score >= 6:
            return "💪 Very Strong"
        elif score >= 4:
            return "🔒 Strong"
        elif score >= 3:
            return "⚠️ Medium"
        else:
            return "❌ Weak"
    
    def search_passwords(self, query):
        """Search passwords by name or username"""
        results = []
        
        for name, data in self.vault.items():
            if query.lower() in name.lower() or query.lower() in data['username'].lower():
                results.append((name, data))
        
        if not results:
            return f"No passwords found matching '{query}'"
        
        output = f"\n{'='*50}\n"
        output += f"🔍 SEARCH RESULTS FOR '{query}'\n"
        output += f"{'='*50}\n\n"
        
        for name, data in results:
            output += f"• {name}\n"
            output += f"  Username: {data['username']}\n\n"
        
        output += f"{'='*50}\n"
        
        return output

if __name__ == "__main__":
    vault = PasswordVault()
    
    print("Testing Password Vault...")
    print(vault.generate_strong_password(16))
    print(vault.check_password_strength("MyP@ssw0rd123!"))
