"""
Tools Mapper
Maps natural language commands to specific In-One-Box tools
Provides intelligent tool selection and routing
"""

import re
from typing import Dict, List, Tuple, Optional

class ToolsMapper:
    def __init__(self):
        # Map keywords to tool categories and specific tools
        self.category_keywords = {
            "AI Tools": ["ai", "artificial intelligence", "chatbot", "gpt", "language model", "generate text"],
            "Audio/Video Tools": ["audio", "video", "music", "sound", "mp3", "mp4", "wav", "convert audio", "convert video"],
            "Coding Tools": ["code", "programming", "syntax", "formatter", "minifier", "beautify", "regex", "json", "api"],
            "Color Tools": ["color", "palette", "gradient", "hex", "rgb", "picker"],
            "CSS Tools": ["css", "stylesheet", "box shadow", "border", "flexbox", "grid"],
            "Data Tools": ["data", "csv", "xml", "database", "sql", "dataset"],
            "File Tools": ["file", "compress", "zip", "archive", "rename", "duplicate"],
            "Image Tools": ["image", "photo", "picture", "png", "jpg", "resize", "compress image", "watermark"],
            "Science/Math Tools": ["math", "calculate", "equation", "statistics", "graph", "plot"],
            "Security/Privacy Tools": ["security", "password", "encrypt", "hash", "vpn", "privacy"],
            "Social Media Tools": ["social media", "facebook", "twitter", "instagram", "post", "hashtag"],
            "SEO/Marketing Tools": ["seo", "marketing", "keyword", "backlink", "domain", "meta tag"],
            "Text Tools": ["text", "word count", "case", "base64", "qr code", "lorem ipsum", "hash"],
            "Web Developer Tools": ["web dev", "html", "javascript", "minify", "performance"],
            "News & Events Tools": ["news", "events", "rss", "weather", "calendar"]
        }
        
        # Map specific tool names to categories
        self.tool_mappings = {
            # Text Tools
            "qr code": ("Text Tools", "QR Code Generator"),
            "qr": ("Text Tools", "QR Code Generator"),
            "base64": ("Text Tools", "Base64 Encoder/Decoder"),
            "hash": ("Text Tools", "Hash Generator"),
            "word count": ("Text Tools", "Word Counter"),
            "case convert": ("Text Tools", "Case Converter"),
            "lorem ipsum": ("Text Tools", "Lorem Ipsum Generator"),
            "password": ("Text Tools", "Password Generator"),
            "uuid": ("Text Tools", "UUID Generator"),
            
            # Image Tools
            "image convert": ("Image Tools", "Image Format Converter"),
            "resize image": ("Image Tools", "Image Resizer"),
            "compress image": ("Image Tools", "Image Compressor"),
            "watermark": ("Image Tools", "Image Watermark"),
            "crop": ("Image Tools", "Image Cropper"),
            
            # File Tools
            "zip": ("File Tools", "ZIP Creator"),
            "compress file": ("File Tools", "File Compressor"),
            "rename": ("File Tools", "Bulk Renamer"),
            "duplicate finder": ("File Tools", "Duplicate Finder"),
            "file encrypt": ("File Tools", "File Encryption"),
            
            # Coding Tools
            "json": ("Coding Tools", "JSON Validator"),
            "regex": ("Coding Tools", "Regex Tester"),
            "code format": ("Coding Tools", "Code Formatter"),
            "minify": ("Coding Tools", "Code Minifier"),
            
            # Color Tools
            "color pick": ("Color Tools", "Color Picker"),
            "gradient": ("Color Tools", "Gradient Generator"),
            "palette": ("Color Tools", "Color Palette"),
            
            # Security Tools
            "encrypt": ("Security/Privacy Tools", "File Encryption"),
            "generate password": ("Security/Privacy Tools", "Password Generator"),
            
            # Math Tools
            "calculate": ("Science/Math Tools", "Calculator"),
            "convert unit": ("Science/Math Tools", "Unit Converter"),
            
            # Data Tools
            "csv": ("Data Tools", "CSV Converter"),
            "xml": ("Data Tools", "XML Parser"),
            "sql": ("Data Tools", "SQL Formatter"),
        }
    
    def find_category(self, query: str) -> Optional[str]:
        """Find the most relevant category for a query"""
        query_lower = query.lower()
        
        # Check for exact matches first
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return category
        
        return None
    
    def find_tool(self, query: str) -> Optional[Tuple[str, str]]:
        """Find the most relevant tool for a query"""
        query_lower = query.lower()
        
        # Check direct tool mappings
        for keyword, (category, tool) in self.tool_mappings.items():
            if keyword in query_lower:
                return (category, tool)
        
        # If no specific tool found, return just the category
        category = self.find_category(query)
        if category:
            return (category, None)
        
        return None
    
    def parse_command(self, command: str) -> Dict:
        """
        Parse a natural language command and extract tool information
        
        Returns:
            Dict with 'action', 'category', 'tool', and 'parameters'
        """
        command_lower = command.lower()
        
        # Detect action intent
        action = "open_web_tool"
        if any(word in command_lower for word in ["launch", "start", "run"]):
            action = "launch_web_tool"
        elif any(word in command_lower for word in ["list", "show all", "what tools"]):
            action = "list_web_tools"
        elif any(word in command_lower for word in ["status", "running", "check"]):
            action = "web_tools_status"
        elif any(word in command_lower for word in ["stop", "close", "quit"]):
            action = "stop_web_tools"
        
        # Find relevant tool
        tool_info = self.find_tool(command)
        
        result = {
            "action": action,
            "category": tool_info[0] if tool_info else None,
            "tool": tool_info[1] if tool_info else None,
            "parameters": {}
        }
        
        return result
    
    def get_suggestions(self, partial_query: str) -> List[str]:
        """Get tool suggestions based on partial query"""
        suggestions = []
        query_lower = partial_query.lower()
        
        # Search in tool names
        for keyword, (category, tool) in self.tool_mappings.items():
            if query_lower in keyword:
                suggestions.append(f"{tool} ({category})")
        
        # Search in categories
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if query_lower in keyword:
                    suggestions.append(category)
                    break
        
        return list(set(suggestions))[:10]  # Return top 10 unique suggestions
    
    def get_tool_description(self, category: str, tool: Optional[str] = None) -> str:
        """Get a description of what a tool does"""
        descriptions = {
            "Text Tools": {
                "QR Code Generator": "Generate QR codes from text, URLs, or data",
                "Base64 Encoder/Decoder": "Encode or decode Base64 text",
                "Hash Generator": "Generate MD5, SHA1, SHA256, SHA512 hashes",
                "Word Counter": "Count words, characters, sentences in text",
                "Case Converter": "Convert text case (uppercase, lowercase, title case)",
                "Password Generator": "Generate secure random passwords",
                "_category": "Process, format, and analyze text data"
            },
            "Image Tools": {
                "Image Format Converter": "Convert images between different formats (PNG, JPG, WebP, etc.)",
                "Image Resizer": "Resize images to specific dimensions",
                "Image Compressor": "Reduce image file size while maintaining quality",
                "_category": "Edit, convert, and optimize images"
            },
            "File Tools": {
                "ZIP Creator": "Create ZIP archives from files",
                "File Compressor": "Compress files to reduce size",
                "Bulk Renamer": "Rename multiple files at once",
                "_category": "Manage, organize, and convert files"
            },
            "Coding Tools": {
                "JSON Validator": "Validate and format JSON data",
                "Regex Tester": "Test and debug regular expressions",
                "Code Formatter": "Format and beautify code",
                "_category": "Development utilities and code tools"
            }
        }
        
        if category in descriptions:
            if tool and tool in descriptions[category]:
                return descriptions[category][tool]
            elif "_category" in descriptions[category]:
                return descriptions[category]["_category"]
        
        return f"Access tools in the {category} category"

def create_tools_mapper():
    """Factory function to create ToolsMapper instance"""
    return ToolsMapper()
