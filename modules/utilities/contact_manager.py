import json
import os
from typing import Dict, List, Optional

class ContactManager:
    """Manages contacts for messaging automation"""
    
    def __init__(self, contacts_file: str = "contacts.json"):
        self.contacts_file = contacts_file
        self.contacts = self._load_contacts()
    
    def _load_contacts(self) -> Dict[str, Dict]:
        """Load contacts from JSON file"""
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading contacts: {e}")
                return {}
        return {}
    
    def _save_contacts(self) -> bool:
        """Save contacts to JSON file"""
        try:
            with open(self.contacts_file, 'w') as f:
                json.dump(self.contacts, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving contacts: {e}")
            return False
    
    def add_contact(self, name: str, phone: Optional[str] = None, email: Optional[str] = None) -> bool:
        """Add a new contact"""
        if not name:
            return False
        
        name_lower = name.lower()
        self.contacts[name_lower] = {
            "name": name,
            "phone": phone,
            "email": email
        }
        return self._save_contacts()
    
    def get_contact(self, name: str) -> Optional[Dict]:
        """Get a contact by name (case-insensitive)"""
        return self.contacts.get(name.lower())
    
    def update_contact(self, name: str, phone: Optional[str] = None, email: Optional[str] = None) -> bool:
        """Update an existing contact"""
        name_lower = name.lower()
        if name_lower not in self.contacts:
            return False
        
        if phone is not None:
            self.contacts[name_lower]["phone"] = phone
        if email is not None:
            self.contacts[name_lower]["email"] = email
        
        return self._save_contacts()
    
    def delete_contact(self, name: str) -> bool:
        """Delete a contact"""
        name_lower = name.lower()
        if name_lower in self.contacts:
            del self.contacts[name_lower]
            return self._save_contacts()
        return False
    
    def list_contacts(self) -> List[Dict]:
        """Get all contacts"""
        return list(self.contacts.values())
    
    def search_contacts(self, query: str) -> List[Dict]:
        """Search contacts by name"""
        query_lower = query.lower()
        return [
            contact for contact in self.contacts.values()
            if query_lower in contact["name"].lower()
        ]
    
    def get_phone(self, name: str) -> Optional[str]:
        """Get phone number for a contact"""
        contact = self.get_contact(name)
        return contact.get("phone") if contact else None
    
    def get_email(self, name: str) -> Optional[str]:
        """Get email address for a contact"""
        contact = self.get_contact(name)
        return contact.get("email") if contact else None
