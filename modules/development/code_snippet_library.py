"""
Code Snippet Library - Auto-saves useful code for reuse
Intelligent code storage with tagging, search, and AI categorization
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
import re


class CodeSnippetLibrary:
    """Manages code snippets with intelligent categorization and search"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.snippets_file = self.data_dir / "code_snippets.json"
        self.load_snippets()
        
        # Language detection patterns
        self.language_patterns = {
            "python": [r"def\s+\w+", r"import\s+\w+", r"class\s+\w+", r"print\("],
            "javascript": [r"function\s+\w+", r"const\s+\w+", r"let\s+\w+", r"console\.log"],
            "java": [r"public\s+class", r"private\s+\w+", r"System\.out"],
            "cpp": [r"#include", r"std::", r"cout\s*<<"],
            "html": [r"<html", r"<div", r"<p>", r"<span"],
            "css": [r"\{[^}]*:", r"\.[\w-]+\s*\{"],
            "sql": [r"SELECT\s+", r"FROM\s+", r"WHERE\s+", r"INSERT\s+INTO"],
            "bash": [r"#!/bin/bash", r"echo\s+", r"\$\w+"]
        }
    
    def load_snippets(self):
        """Load snippets from file"""
        if self.snippets_file.exists():
            with open(self.snippets_file, 'r', encoding='utf-8') as f:
                self.snippets = json.load(f)
        else:
            self.snippets = []
    
    def save_snippets(self):
        """Save snippets to file"""
        with open(self.snippets_file, 'w', encoding='utf-8') as f:
            json.dump(self.snippets, f, indent=2, ensure_ascii=False)
    
    def save_snippet(self, code, title="", description="", language=None, tags=None):
        """Save a code snippet"""
        # Auto-detect language if not provided
        if not language:
            language = self.detect_language(code)
        
        # Generate unique ID
        snippet_id = hashlib.md5(code.encode()).hexdigest()[:12]
        
        # Check if snippet already exists
        existing = next((s for s in self.snippets if s["id"] == snippet_id), None)
        if existing:
            return {
                "success": False,
                "message": "Snippet already exists",
                "id": snippet_id,
                "existing_title": existing["title"]
            }
        
        # Create snippet object
        snippet = {
            "id": snippet_id,
            "title": title or f"Snippet_{snippet_id}",
            "description": description,
            "code": code,
            "language": language,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "used_count": 0,
            "last_used": None,
            "favorited": False
        }
        
        self.snippets.append(snippet)
        self.save_snippets()
        
        return {
            "success": True,
            "message": "Snippet saved successfully",
            "id": snippet_id,
            "language": language
        }
    
    def detect_language(self, code):
        """Auto-detect programming language from code"""
        code_lower = code.lower()
        
        scores = {}
        for lang, patterns in self.language_patterns.items():
            score = sum(1 for pattern in patterns if re.search(pattern, code, re.IGNORECASE))
            if score > 0:
                scores[lang] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return "unknown"
    
    def search_snippets(self, query="", language=None, tags=None):
        """Search for snippets"""
        results = self.snippets.copy()
        
        # Filter by language
        if language:
            results = [s for s in results if s["language"].lower() == language.lower()]
        
        # Filter by tags
        if tags:
            tag_list = tags if isinstance(tags, list) else [tags]
            results = [s for s in results if any(tag in s["tags"] for tag in tag_list)]
        
        # Filter by query (search in title, description, code)
        if query:
            query_lower = query.lower()
            results = [
                s for s in results
                if query_lower in s["title"].lower()
                or query_lower in s["description"].lower()
                or query_lower in s["code"].lower()
            ]
        
        # Sort by last used, then favorites
        results.sort(key=lambda x: (x["favorited"], x["used_count"]), reverse=True)
        
        return {
            "success": True,
            "count": len(results),
            "snippets": results
        }
    
    def get_snippet(self, snippet_id):
        """Get a specific snippet by ID"""
        snippet = next((s for s in self.snippets if s["id"] == snippet_id), None)
        
        if not snippet:
            return {"success": False, "message": "Snippet not found"}
        
        # Update usage stats
        snippet["used_count"] += 1
        snippet["last_used"] = datetime.now().isoformat()
        self.save_snippets()
        
        return {
            "success": True,
            "snippet": snippet
        }
    
    def delete_snippet(self, snippet_id):
        """Delete a snippet"""
        original_count = len(self.snippets)
        self.snippets = [s for s in self.snippets if s["id"] != snippet_id]
        
        if len(self.snippets) == original_count:
            return {"success": False, "message": "Snippet not found"}
        
        self.save_snippets()
        return {"success": True, "message": "Snippet deleted"}
    
    def update_snippet(self, snippet_id, **updates):
        """Update snippet metadata"""
        snippet = next((s for s in self.snippets if s["id"] == snippet_id), None)
        
        if not snippet:
            return {"success": False, "message": "Snippet not found"}
        
        # Update allowed fields
        allowed_fields = ["title", "description", "tags", "favorited"]
        for field, value in updates.items():
            if field in allowed_fields:
                snippet[field] = value
        
        self.save_snippets()
        return {"success": True, "message": "Snippet updated"}
    
    def toggle_favorite(self, snippet_id):
        """Toggle favorite status"""
        snippet = next((s for s in self.snippets if s["id"] == snippet_id), None)
        
        if not snippet:
            return {"success": False, "message": "Snippet not found"}
        
        snippet["favorited"] = not snippet["favorited"]
        self.save_snippets()
        
        status = "favorited" if snippet["favorited"] else "unfavorited"
        return {"success": True, "message": f"Snippet {status}"}
    
    def get_statistics(self):
        """Get library statistics"""
        if not self.snippets:
            return {"success": False, "message": "No snippets in library"}
        
        # Count by language
        lang_counts = {}
        for snippet in self.snippets:
            lang = snippet["language"]
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        # Most used snippets
        most_used = sorted(self.snippets, key=lambda x: x["used_count"], reverse=True)[:5]
        
        # Favorites
        favorites = [s for s in self.snippets if s["favorited"]]
        
        return {
            "success": True,
            "total_snippets": len(self.snippets),
            "languages": lang_counts,
            "total_favorites": len(favorites),
            "most_used": [
                {"id": s["id"], "title": s["title"], "used_count": s["used_count"]}
                for s in most_used
            ],
            "languages_count": len(lang_counts)
        }
    
    def export_snippets(self, export_path=None):
        """Export all snippets to a file"""
        if not export_path:
            export_path = self.data_dir / f"snippets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.snippets, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "message": "Snippets exported",
                "file": str(export_path),
                "count": len(self.snippets)
            }
        except Exception as e:
            return {"success": False, "message": f"Export failed: {e}"}
    
    def import_snippets(self, import_path):
        """Import snippets from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            # Add imported snippets (avoid duplicates)
            new_count = 0
            for snippet in imported:
                snippet_id = snippet.get("id")
                if not any(s["id"] == snippet_id for s in self.snippets):
                    self.snippets.append(snippet)
                    new_count += 1
            
            self.save_snippets()
            
            return {
                "success": True,
                "message": f"Imported {new_count} new snippets",
                "total": len(self.snippets)
            }
        except Exception as e:
            return {"success": False, "message": f"Import failed: {e}"}


# Singleton instance
_snippet_library = None

def get_snippet_library():
    """Get or create snippet library instance"""
    global _snippet_library
    if _snippet_library is None:
        _snippet_library = CodeSnippetLibrary()
    return _snippet_library


if __name__ == "__main__":
    # Test the library
    library = get_snippet_library()
    
    print("Testing Code Snippet Library...")
    
    # Save a snippet
    code = """def hello_world():
    print("Hello, World!")
    return True"""
    
    result = library.save_snippet(
        code=code,
        title="Hello World Function",
        description="Simple hello world function in Python",
        tags=["python", "tutorial", "basic"]
    )
    print(f"\nSave result: {json.dumps(result, indent=2)}")
    
    # Search snippets
    search_result = library.search_snippets(query="hello")
    print(f"\nSearch result: Found {search_result['count']} snippets")
    
    # Get stats
    stats = library.get_statistics()
    print(f"\nLibrary stats: {json.dumps(stats, indent=2)}")
