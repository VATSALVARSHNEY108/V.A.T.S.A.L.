"""
Clipboard & Text Handling Module
Comprehensive clipboard management and text formatting utilities
"""

import pyperclip
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
import os


class ClipboardTextHandler:
    """Handles clipboard operations and text formatting"""
    
    def __init__(self):
        self.clipboard_history: List[Dict[str, Any]] = []
        self.max_history = 50
        self.history_file = "clipboard_history.json"
    
    def copy_text(self, text: str) -> Dict[str, Any]:
        """Copy text to clipboard"""
        try:
            pyperclip.copy(text)
            self._add_to_history("text", text)
            return {
                "success": True,
                "message": f"Copied {len(text)} characters to clipboard",
                "type": "text",
                "length": len(text)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def paste_text(self) -> Dict[str, Any]:
        """Get text from clipboard"""
        try:
            text = pyperclip.paste()
            return {
                "success": True,
                "content": text,
                "type": "text",
                "length": len(text)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def copy_image_path(self, image_path: str) -> Dict[str, Any]:
        """Copy image file path to clipboard"""
        try:
            if not os.path.exists(image_path):
                return {"success": False, "error": f"Image file not found: {image_path}"}
            
            pyperclip.copy(image_path)
            self._add_to_history("image_path", image_path)
            
            return {
                "success": True,
                "message": f"Image path copied to clipboard: {image_path}",
                "type": "image_path",
                "path": image_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def copy_file_paths(self, file_paths: List[str]) -> Dict[str, Any]:
        """Copy file paths to clipboard"""
        try:
            paths_text = "\n".join(file_paths)
            pyperclip.copy(paths_text)
            self._add_to_history("files", paths_text)
            
            return {
                "success": True,
                "message": f"Copied {len(file_paths)} file paths to clipboard",
                "type": "files",
                "count": len(file_paths)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clear_clipboard(self) -> Dict[str, Any]:
        """Clear clipboard content"""
        try:
            pyperclip.copy("")
            return {
                "success": True,
                "message": "Clipboard cleared"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_clipboard_info(self) -> Dict[str, Any]:
        """Get information about current clipboard content"""
        try:
            content = pyperclip.paste()
            
            content_type = "text"
            if "\n" in content and all(os.path.exists(p.strip()) for p in content.split("\n") if p.strip()):
                content_type = "file_paths"
            
            return {
                "success": True,
                "type": content_type,
                "length": len(content),
                "preview": content[:100],
                "lines": len(content.split("\n")) if "\n" in content else 1
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _add_to_history(self, content_type: str, content: str):
        """Add clipboard entry to history"""
        entry = {
            "type": content_type,
            "content": content[:200] if len(content) > 200 else content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.clipboard_history.insert(0, entry)
        if len(self.clipboard_history) > self.max_history:
            self.clipboard_history.pop()
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get clipboard history"""
        return self.clipboard_history[:limit]
    
    def clear_history(self) -> Dict[str, Any]:
        """Clear clipboard history"""
        self.clipboard_history.clear()
        return {"success": True, "message": "Clipboard history cleared"}
    
    def to_uppercase(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Convert text to uppercase"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text.upper()
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Converted to uppercase and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def to_lowercase(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Convert text to lowercase"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text.lower()
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Converted to lowercase and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def to_title_case(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Convert text to title case"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text.title()
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Converted to title case and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def to_sentence_case(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Convert text to sentence case"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            sentences = re.split(r'([.!?]\s+)', text)
            result = ""
            for i, part in enumerate(sentences):
                if i % 2 == 0 and part:
                    result += part[0].upper() + part[1:].lower()
                else:
                    result += part
            
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Converted to sentence case and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def toggle_case(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Toggle case of each character"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text.swapcase()
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Toggled case and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def capitalize_first(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Capitalize first letter only"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text[0].upper() + text[1:].lower() if text else ""
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Capitalized first letter and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def trim_whitespace(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Remove leading and trailing whitespace"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text.strip()
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Trimmed whitespace and copied to clipboard",
                "removed_chars": len(text) - len(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remove_extra_spaces(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Remove extra spaces (multiple spaces to single space)"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = re.sub(r'\s+', ' ', text).strip()
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Removed extra spaces and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remove_line_breaks(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Remove all line breaks"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text.replace('\n', ' ').replace('\r', '')
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Removed line breaks and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_line_breaks(self, text: Optional[str] = None, interval: int = 80) -> Dict[str, Any]:
        """Add line breaks at specified character intervals"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 <= interval:
                    current_line += (" " if current_line else "") + word
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            result = "\n".join(lines)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": f"Added line breaks every {interval} characters and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remove_special_characters(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Remove special characters (keep only letters, numbers, spaces)"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Removed special characters and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remove_numbers(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Remove all numbers from text"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = re.sub(r'\d', '', text)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Removed numbers and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remove_punctuation(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Remove all punctuation from text"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = re.sub(r'[^\w\s]', '', text)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Removed punctuation and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def word_count(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Count words in text"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            words = len(text.split())
            chars = len(text)
            chars_no_spaces = len(text.replace(' ', ''))
            lines = len(text.split('\n'))
            
            return {
                "success": True,
                "text": text,
                "words": words,
                "characters": chars,
                "characters_no_spaces": chars_no_spaces,
                "lines": lines
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def reverse_text(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Reverse the text"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            result = text[::-1]
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": "Reversed text and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sort_lines(self, text: Optional[str] = None, reverse: bool = False) -> Dict[str, Any]:
        """Sort lines alphabetically"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            lines = text.split('\n')
            sorted_lines = sorted(lines, reverse=reverse)
            result = '\n'.join(sorted_lines)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": f"Sorted lines {'(reverse)' if reverse else ''} and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def remove_duplicate_lines(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Remove duplicate lines while preserving order"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            lines = text.split('\n')
            seen = set()
            unique_lines = []
            
            for line in lines:
                if line not in seen:
                    seen.add(line)
                    unique_lines.append(line)
            
            result = '\n'.join(unique_lines)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "message": f"Removed {len(lines) - len(unique_lines)} duplicate lines and copied to clipboard",
                "removed": len(lines) - len(unique_lines)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_urls(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Extract all URLs from text"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            urls = re.findall(url_pattern, text)
            
            result = '\n'.join(urls)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "urls": urls,
                "count": len(urls),
                "message": f"Extracted {len(urls)} URLs and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_emails(self, text: Optional[str] = None) -> Dict[str, Any]:
        """Extract all email addresses from text"""
        try:
            if text is None:
                text = pyperclip.paste()
            
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            
            result = '\n'.join(emails)
            pyperclip.copy(result)
            
            return {
                "success": True,
                "original": text,
                "result": result,
                "emails": emails,
                "count": len(emails),
                "message": f"Extracted {len(emails)} email addresses and copied to clipboard"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    handler = ClipboardTextHandler()
    
    print("🎨 Clipboard & Text Handler initialized")
    print("✨ Multi-format clipboard support")
    print("🔤 Advanced text formatting")
    print("📋 Clipboard history tracking")
    
    test_text = "Hello World! This is a TEST."
    print(f"\nTest: {test_text}")
    print(f"Uppercase: {handler.to_uppercase(test_text)['result']}")
    print(f"Lowercase: {handler.to_lowercase(test_text)['result']}")
    print(f"Title Case: {handler.to_title_case(test_text)['result']}")
