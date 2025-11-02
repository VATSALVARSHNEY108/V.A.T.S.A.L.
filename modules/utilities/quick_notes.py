"""
Quick Notes Module
Fast note-taking with categories, tags, and search
"""

import json
import os
from datetime import datetime

class QuickNotes:
    def __init__(self):
        self.notes_file = "quick_notes.json"
        self.load_notes()
    
    def load_notes(self):
        """Load notes from file"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            else:
                self.notes = []
        except Exception:
            self.notes = []
    
    def save_notes(self):
        """Save notes to file"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def add_note(self, content, category="general", tags=None):
        """Add a new note"""
        note = {
            'id': len(self.notes) + 1,
            'content': content,
            'category': category.lower(),
            'tags': tags or [],
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'pinned': False
        }
        
        self.notes.append(note)
        self.save_notes()
        
        output = f"\n{'='*50}\n"
        output += f"📝 NOTE SAVED\n"
        output += f"{'='*50}\n\n"
        output += f"✅ Note #{note['id']} has been saved!\n"
        output += f"Category: {category}\n"
        
        if tags:
            output += f"Tags: {', '.join(tags)}\n"
        
        output += f"{'='*50}\n"
        
        return output
    
    def get_note(self, note_id):
        """Get a specific note by ID"""
        for note in self.notes:
            if note['id'] == note_id:
                return self._format_note(note)
        
        return f"⚠️ Note #{note_id} not found."
    
    def update_note(self, note_id, content=None, category=None, tags=None):
        """Update an existing note"""
        for note in self.notes:
            if note['id'] == note_id:
                if content:
                    note['content'] = content
                if category:
                    note['category'] = category.lower()
                if tags:
                    note['tags'] = tags
                
                note['modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                
                return f"✅ Note #{note_id} has been updated!"
        
        return f"⚠️ Note #{note_id} not found."
    
    def delete_note(self, note_id):
        """Delete a note"""
        for i, note in enumerate(self.notes):
            if note['id'] == note_id:
                del self.notes[i]
                self.save_notes()
                
                return f"🗑️ Note #{note_id} has been deleted!"
        
        return f"⚠️ Note #{note_id} not found."
    
    def list_notes(self, category=None, limit=20):
        """List all notes or notes in a specific category"""
        if not self.notes:
            return "📭 No notes found. Create your first note!"
        
        filtered_notes = self.notes
        
        if category:
            filtered_notes = [n for n in self.notes if n['category'] == category.lower()]
            
            if not filtered_notes:
                return f"📭 No notes found in category '{category}'."
        
        filtered_notes.sort(key=lambda x: (not x.get('pinned', False), x['modified']), reverse=True)
        
        output = f"\n{'='*50}\n"
        
        if category:
            output += f"📝 NOTES - {category.upper()}\n"
        else:
            output += f"📝 ALL NOTES\n"
        
        output += f"{'='*50}\n\n"
        
        for note in filtered_notes[:limit]:
            pin_icon = "📌 " if note.get('pinned') else ""
            content_preview = note['content'][:60] + "..." if len(note['content']) > 60 else note['content']
            
            output += f"{pin_icon}#{note['id']} - {note['category']}\n"
            output += f"   {content_preview}\n"
            output += f"   🕐 {note['modified']}\n\n"
        
        output += f"{'='*50}\n"
        output += f"Total Notes: {len(filtered_notes)}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def search_notes(self, query):
        """Search notes by content, category, or tags"""
        results = []
        
        for note in self.notes:
            if (query.lower() in note['content'].lower() or
                query.lower() in note['category'].lower() or
                any(query.lower() in tag.lower() for tag in note.get('tags', []))):
                results.append(note)
        
        if not results:
            return f"No notes found matching '{query}'"
        
        output = f"\n{'='*50}\n"
        output += f"🔍 SEARCH RESULTS FOR '{query}'\n"
        output += f"{'='*50}\n\n"
        
        for note in results:
            content_preview = note['content'][:60] + "..." if len(note['content']) > 60 else note['content']
            
            output += f"#{note['id']} - {note['category']}\n"
            output += f"   {content_preview}\n"
            output += f"   🕐 {note['modified']}\n\n"
        
        output += f"{'='*50}\n"
        output += f"Found {len(results)} note(s)\n"
        output += f"{'='*50}\n"
        
        return output
    
    def pin_note(self, note_id):
        """Pin/unpin a note"""
        for note in self.notes:
            if note['id'] == note_id:
                note['pinned'] = not note.get('pinned', False)
                self.save_notes()
                
                status = "pinned" if note['pinned'] else "unpinned"
                return f"📌 Note #{note_id} has been {status}!"
        
        return f"⚠️ Note #{note_id} not found."
    
    def get_categories(self):
        """Get list of all categories"""
        categories = {}
        
        for note in self.notes:
            cat = note['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        if not categories:
            return "No categories found."
        
        output = f"\n{'='*50}\n"
        output += f"📂 NOTE CATEGORIES\n"
        output += f"{'='*50}\n\n"
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            output += f"  • {cat}: {count} note(s)\n"
        
        output += f"\n{'='*50}\n"
        
        return output
    
    def _format_note(self, note):
        """Format a single note for display"""
        output = f"\n{'='*50}\n"
        output += f"📝 NOTE #{note['id']}\n"
        output += f"{'='*50}\n\n"
        output += f"{note['content']}\n\n"
        output += f"📂 Category: {note['category']}\n"
        
        if note.get('tags'):
            output += f"🏷️  Tags: {', '.join(note['tags'])}\n"
        
        output += f"📌 Pinned: {'Yes' if note.get('pinned') else 'No'}\n"
        output += f"🕐 Created: {note['created']}\n"
        output += f"🕐 Modified: {note['modified']}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def export_notes(self, category=None):
        """Export notes to text file"""
        try:
            filename = f"notes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            filtered_notes = self.notes
            if category:
                filtered_notes = [n for n in self.notes if n['category'] == category.lower()]
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"NOTES EXPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                for note in filtered_notes:
                    f.write(f"Note #{note['id']} - {note['category']}\n")
                    f.write(f"Created: {note['created']}\n")
                    f.write("-"*50 + "\n")
                    f.write(f"{note['content']}\n")
                    f.write("="*50 + "\n\n")
            
            return f"✅ Notes exported to {filename}"
            
        except Exception as e:
            return f"Export error: {str(e)}"

if __name__ == "__main__":
    notes = QuickNotes()
    
    print("Testing Quick Notes...")
    print(notes.add_note("Remember to buy groceries", "personal", ["shopping", "urgent"]))
    print(notes.add_note("Meeting at 3 PM tomorrow", "work", ["meetings"]))
    print(notes.list_notes())
