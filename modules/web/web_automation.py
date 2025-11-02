"""
Web Automation Module
Auto-login, web scraping shortcuts, clipboard history with AI search
"""

import json
import os
from datetime import datetime
import pyperclip
import time
import webbrowser
from cryptography.fernet import Fernet
import base64

class WebAutomation:
    def __init__(self):
        self.credentials_file = "credentials.enc"
        self.clipboard_history_file = "clipboard_history.json"
        self.scrapers_file = "web_scrapers.json"
        self.clipboard_history = []
        self.max_clipboard_items = 100
        
        self.encryption_key = self.get_or_create_key()
        self.load_clipboard_history()
        self.load_scrapers()
    
    def get_or_create_key(self):
        """Get or create encryption key for credentials"""
        key_file = ".encryption_key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def load_clipboard_history(self):
        """Load clipboard history"""
        if os.path.exists(self.clipboard_history_file):
            with open(self.clipboard_history_file, 'r') as f:
                self.clipboard_history = json.load(f)
        else:
            self.clipboard_history = []
    
    def save_clipboard_history(self):
        """Save clipboard history"""
        with open(self.clipboard_history_file, 'w') as f:
            json.dump(self.clipboard_history, f, indent=2)
    
    def load_scrapers(self):
        """Load web scraper configurations"""
        if os.path.exists(self.scrapers_file):
            with open(self.scrapers_file, 'r') as f:
                self.scrapers = json.load(f)
        else:
            self.scrapers = {
                "weather": {
                    "url": "https://wttr.in/?format=3",
                    "description": "Get current weather"
                },
                "crypto": {
                    "url": "https://api.coindesk.com/v1/bpi/currentprice.json",
                    "description": "Get Bitcoin price"
                }
            }
            self.save_scrapers()
    
    def save_scrapers(self):
        """Save web scraper configurations"""
        with open(self.scrapers_file, 'w') as f:
            json.dump(self.scrapers, f, indent=2)
    
    def save_credentials(self, site_name, username, password):
        """Safely save login credentials (encrypted)"""
        try:
            fernet = Fernet(self.encryption_key)
            
            credentials = {}
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'rb') as f:
                    encrypted_data = f.read()
                    if encrypted_data:
                        decrypted_data = fernet.decrypt(encrypted_data)
                        credentials = json.loads(decrypted_data)
            
            credentials[site_name] = {
                "username": username,
                "password": password,
                "saved_at": datetime.now().isoformat()
            }
            
            encrypted_data = fernet.encrypt(json.dumps(credentials).encode())
            
            with open(self.credentials_file, 'wb') as f:
                f.write(encrypted_data)
            
            return f"✅ Credentials saved for {site_name}"
        except Exception as e:
            return f"❌ Failed to save credentials: {str(e)}"
    
    def get_credentials(self, site_name):
        """Retrieve saved credentials"""
        try:
            if not os.path.exists(self.credentials_file):
                return None
            
            fernet = Fernet(self.encryption_key)
            
            with open(self.credentials_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                credentials = json.loads(decrypted_data)
            
            return credentials.get(site_name)
        except Exception as e:
            return None
    
    def list_saved_sites(self):
        """List all sites with saved credentials"""
        try:
            if not os.path.exists(self.credentials_file):
                return "ℹ️ No saved credentials"
            
            fernet = Fernet(self.encryption_key)
            
            with open(self.credentials_file, 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                credentials = json.loads(decrypted_data)
            
            result = "🔐 Saved Login Sites:\n"
            for site, data in credentials.items():
                saved_date = datetime.fromisoformat(data['saved_at']).strftime("%Y-%m-%d")
                result += f"  • {site} (saved {saved_date})\n"
            
            return result
        except Exception as e:
            return f"❌ Failed to list sites: {str(e)}"
    
    def add_to_clipboard_history(self, text):
        """Add text to clipboard history"""
        if text and text.strip():
            item = {
                "text": text[:500],
                "timestamp": datetime.now().isoformat(),
                "length": len(text)
            }
            
            self.clipboard_history.insert(0, item)
            
            self.clipboard_history = self.clipboard_history[:self.max_clipboard_items]
            
            self.save_clipboard_history()
    
    def get_clipboard_history(self, limit=10):
        """Get recent clipboard history"""
        if not self.clipboard_history:
            return "ℹ️ Clipboard history is empty"
        
        result = f"📋 Clipboard History (last {min(limit, len(self.clipboard_history))} items):\n\n"
        
        for i, item in enumerate(self.clipboard_history[:limit], 1):
            timestamp = datetime.fromisoformat(item['timestamp']).strftime("%H:%M:%S")
            preview = item['text'][:60] + "..." if len(item['text']) > 60 else item['text']
            result += f"{i}. [{timestamp}] {preview}\n"
        
        return result
    
    def search_clipboard_history(self, query):
        """Search clipboard history"""
        results = []
        
        for item in self.clipboard_history:
            if query.lower() in item['text'].lower():
                results.append(item)
        
        if not results:
            return f"ℹ️ No results found for '{query}'"
        
        result = f"🔍 Found {len(results)} results for '{query}':\n\n"
        
        for i, item in enumerate(results[:10], 1):
            timestamp = datetime.fromisoformat(item['timestamp']).strftime("%Y-%m-%d %H:%M")
            preview = item['text'][:80] + "..." if len(item['text']) > 80 else item['text']
            result += f"{i}. [{timestamp}] {preview}\n"
        
        return result
    
    def restore_from_clipboard_history(self, index):
        """Restore item from clipboard history"""
        try:
            if 0 <= index < len(self.clipboard_history):
                text = self.clipboard_history[index]['text']
                pyperclip.copy(text)
                return f"✅ Restored to clipboard: {text[:50]}..."
            else:
                return f"❌ Invalid index: {index}"
        except Exception as e:
            return f"❌ Failed to restore: {str(e)}"
    
    def add_scraper(self, name, url, description=""):
        """Add a web scraper shortcut"""
        self.scrapers[name] = {
            "url": url,
            "description": description
        }
        self.save_scrapers()
        return f"✅ Scraper '{name}' added"
    
    def run_scraper(self, name):
        """Run a saved web scraper"""
        if name not in self.scrapers:
            return f"❌ Scraper '{name}' not found"
        
        scraper = self.scrapers[name]
        webbrowser.open(scraper['url'])
        return f"✅ Opened: {scraper['description'] or name}"
    
    def list_scrapers(self):
        """List all saved scrapers"""
        if not self.scrapers:
            return "ℹ️ No scrapers configured"
        
        result = "🕷️ Web Scrapers:\n"
        for name, data in self.scrapers.items():
            result += f"  • {name}: {data['description']}\n"
        
        return result
    
    def quick_search(self, query, engine="google"):
        """Quick web search"""
        engines = {
            "google": f"https://www.google.com/search?q={query}",
            "bing": f"https://www.bing.com/search?q={query}",
            "duckduckgo": f"https://duckduckgo.com/?q={query}",
            "youtube": f"https://www.youtube.com/results?search_query={query}",
            "github": f"https://github.com/search?q={query}"
        }
        
        url = engines.get(engine, engines["google"])
        webbrowser.open(url)
        return f"✅ Searching {engine} for: {query}"
    
    def monitor_clipboard(self, duration_seconds=60):
        """Monitor clipboard for changes and save to history"""
        print(f"📋 Monitoring clipboard for {duration_seconds} seconds...")
        
        last_text = ""
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            try:
                current_text = pyperclip.paste()
                
                if current_text != last_text and current_text.strip():
                    self.add_to_clipboard_history(current_text)
                    print(f"✅ Saved: {current_text[:50]}...")
                    last_text = current_text
                
                time.sleep(1)
            except:
                continue
        
        return f"✅ Clipboard monitoring complete. Saved {len(self.clipboard_history)} items."

if __name__ == "__main__":
    automation = WebAutomation()
    print("Web Automation Module - Testing")
    print(automation.get_clipboard_history())
