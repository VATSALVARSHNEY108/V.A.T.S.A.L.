#!/usr/bin/env python3

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class UserProfileManager:
    """
    Comprehensive User Profile Manager
    Remembers user name, preferences, and custom settings
    """

    def __init__(self, profile_path: str = "config/vatsal_user_profile.json"):
        self.profile_path = Path(profile_path)
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        self.profile = self._load_profile()

    def _load_profile(self) -> Dict[str, Any]:
        """Load user profile from JSON file"""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading profile: {e}")
                return self._get_default_profile()
        else:
            return self._get_default_profile()

    def _get_default_profile(self) -> Dict[str, Any]:
        """Get default profile structure"""
        return {
            "user_info": {
                "name": "User",
                "nickname": "",
                "first_name": "",
                "last_name": "",
                "email": "",
                "timezone": "UTC"
            },
            "preferences": {
                "theme": "dark",
                "notification_style": "polite",
                "voice_enabled": True,
                "voice_speed": 150,
                "voice_volume": 1.0,
                "wake_time": "09:00",
                "sleep_time": "23:00",
                "language": "en",
                "auto_save": True,
                "confirm_actions": True
            },
            "custom_settings": {
                # User-defined custom settings
                # e.g., "favorite_color": "blue"
            },
            "things_to_change": [
                # List of things user wants to change/remember
                # Each entry: {"item": "description", "timestamp": "...", "status": "pending/done"}
            ],
            "habits": {
                # Learned user habits
                # e.g., "usually_works_at": "afternoon"
            },
            "interaction_stats": {
                "total_interactions": 0,
                "last_interaction": None,
                "first_interaction": None,
                "favorite_commands": {},
                "command_history": []
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": "2.0"
            }
        }

    def _save_profile(self):
        """Save profile to JSON file"""
        try:
            self.profile["metadata"]["updated_at"] = datetime.now().isoformat()
            with open(self.profile_path, 'w') as f:
                json.dump(self.profile, f, indent=2)
        except Exception as e:
            print(f"Error saving profile: {e}")

    # ============= User Info Methods =============

    def get_user_name(self) -> str:
        """Get user's name"""
        return self.profile["user_info"].get("name", "User")

    def set_user_name(self, name: str):
        """Set user's name"""
        self.profile["user_info"]["name"] = name
        self._save_profile()
        print(f"✅ User name set to: {name}")

    def get_user_info(self) -> Dict[str, str]:
        """Get all user info"""
        return self.profile["user_info"]

    def update_user_info(self, **kwargs):
        """Update user info fields"""
        for key, value in kwargs.items():
            if key in self.profile["user_info"]:
                self.profile["user_info"][key] = value
        self._save_profile()
        print(f"✅ User info updated")

    # ============= Preferences Methods =============

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a specific preference"""
        return self.profile["preferences"].get(key, default)

    def set_preference(self, key: str, value: Any):
        """Set a specific preference"""
        self.profile["preferences"][key] = value
        self._save_profile()
        print(f"✅ Preference '{key}' set to: {value}")

    def get_all_preferences(self) -> Dict[str, Any]:
        """Get all preferences"""
        return self.profile["preferences"]

    def update_preferences(self, **kwargs):
        """Update multiple preferences at once"""
        for key, value in kwargs.items():
            self.profile["preferences"][key] = value
        self._save_profile()
        print(f"✅ Updated {len(kwargs)} preferences")

    # ============= Custom Settings Methods =============

    def get_custom_setting(self, key: str, default: Any = None) -> Any:
        """Get a custom user-defined setting"""
        return self.profile["custom_settings"].get(key, default)

    def set_custom_setting(self, key: str, value: Any):
        """Set a custom user-defined setting"""
        self.profile["custom_settings"][key] = value
        self._save_profile()
        print(f"✅ Custom setting '{key}' set to: {value}")

    def get_all_custom_settings(self) -> Dict[str, Any]:
        """Get all custom settings"""
        return self.profile["custom_settings"]

    def remove_custom_setting(self, key: str):
        """Remove a custom setting"""
        if key in self.profile["custom_settings"]:
            del self.profile["custom_settings"][key]
            self._save_profile()
            print(f"✅ Custom setting '{key}' removed")

    # ============= Things to Change Methods =============

    def add_thing_to_change(self, item: str, category: str = "general", priority: str = "medium"):
        """Add something user wants to change/remember"""
        change_item = {
            "item": item,
            "category": category,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        self.profile["things_to_change"].append(change_item)
        self._save_profile()
        print(f"✅ Added to things to change: {item}")
        return change_item

    def get_things_to_change(self, status: Optional[str] = None) -> List[Dict]:
        """Get list of things to change, optionally filtered by status"""
        if status:
            return [item for item in self.profile["things_to_change"]
                    if item.get("status") == status]
        return self.profile["things_to_change"]

    def mark_thing_done(self, index: int):
        """Mark a thing to change as done"""
        if 0 <= index < len(self.profile["things_to_change"]):
            self.profile["things_to_change"][index]["status"] = "done"
            self.profile["things_to_change"][index]["completed_at"] = datetime.now().isoformat()
            self._save_profile()
            print(f"✅ Marked item {index} as done")

    def remove_thing_to_change(self, index: int):
        """Remove a thing to change"""
        if 0 <= index < len(self.profile["things_to_change"]):
            removed = self.profile["things_to_change"].pop(index)
            self._save_profile()
            print(f"✅ Removed: {removed['item']}")

    # ============= Habits Methods =============

    def learn_habit(self, habit_key: str, habit_value: Any):
        """Learn and remember a user habit"""
        self.profile["habits"][habit_key] = habit_value
        self._save_profile()
        print(f"✅ Learned habit: {habit_key}")

    def get_habit(self, habit_key: str, default: Any = None) -> Any:
        """Get a learned habit"""
        return self.profile["habits"].get(habit_key, default)

    def get_all_habits(self) -> Dict[str, Any]:
        """Get all learned habits"""
        return self.profile["habits"]

    # ============= Interaction Stats Methods =============

    def record_interaction(self, command: Optional[str] = None):
        """Record an interaction"""
        stats = self.profile["interaction_stats"]
        stats["total_interactions"] += 1
        stats["last_interaction"] = datetime.now().isoformat()

        if stats["first_interaction"] is None:
            stats["first_interaction"] = datetime.now().isoformat()

        if command:
            # Track favorite commands
            if command not in stats["favorite_commands"]:
                stats["favorite_commands"][command] = 0
            stats["favorite_commands"][command] += 1

            # Add to history (keep last 100)
            stats["command_history"].append({
                "command": command,
                "timestamp": datetime.now().isoformat()
            })
            if len(stats["command_history"]) > 100:
                stats["command_history"] = stats["command_history"][-100:]

        self._save_profile()

    def get_stats(self) -> Dict[str, Any]:
        """Get interaction statistics"""
        return self.profile["interaction_stats"]

    def get_favorite_commands(self, top_n: int = 10) -> List[tuple]:
        """Get top N favorite commands"""
        fav_commands = self.profile["interaction_stats"]["favorite_commands"]
        sorted_commands = sorted(fav_commands.items(), key=lambda x: x[1], reverse=True)
        return sorted_commands[:top_n]

    # ============= Utility Methods =============

    def get_greeting(self) -> str:
        """Get personalized greeting"""
        name = self.get_user_name()
        current_hour = datetime.now().hour

        if 5 <= current_hour < 12:
            greeting = f"Good morning, {name}!"
        elif 12 <= current_hour < 17:
            greeting = f"Good afternoon, {name}!"
        elif 17 <= current_hour < 21:
            greeting = f"Good evening, {name}!"
        else:
            greeting = f"Hello, {name}!"

        return greeting

    def export_profile(self, export_path: str):
        """Export profile to a file"""
        try:
            with open(export_path, 'w') as f:
                json.dump(self.profile, f, indent=2)
            print(f"✅ Profile exported to: {export_path}")
        except Exception as e:
            print(f"❌ Error exporting profile: {e}")

    def import_profile(self, import_path: str):
        """Import profile from a file"""
        try:
            with open(import_path, 'r') as f:
                imported_profile = json.load(f)
            self.profile = imported_profile
            self._save_profile()
            print(f"✅ Profile imported from: {import_path}")
        except Exception as e:
            print(f"❌ Error importing profile: {e}")

    def reset_profile(self):
        """Reset profile to default"""
        self.profile = self._get_default_profile()
        self._save_profile()
        print("✅ Profile reset to default")

    def get_profile_summary(self) -> str:
        """Get a summary of the profile"""
        name = self.get_user_name()
        stats = self.get_stats()
        things_pending = len(self.get_things_to_change(status="pending"))
        things_done = len(self.get_things_to_change(status="done"))

        summary = f"""
╔════════════════════════════════════════════╗
║         USER PROFILE SUMMARY               ║
╠════════════════════════════════════════════╣
║ Name: {name:<37}║
║ Total Interactions: {stats['total_interactions']:<24}║
║ Things to Change (Pending): {things_pending:<14}║
║ Things to Change (Done): {things_done:<17}║
║ Custom Settings: {len(self.profile['custom_settings']):<24}║
║ Learned Habits: {len(self.profile['habits']):<25}║
╚════════════════════════════════════════════╝
"""
        return summary


# Global instance
_user_profile_manager = None


def get_user_profile_manager() -> UserProfileManager:
    """Get or create the global UserProfileManager instance"""
    global _user_profile_manager
    if _user_profile_manager is None:
        _user_profile_manager = UserProfileManager()
    return _user_profile_manager


# Example usage
if __name__ == "__main__":
    profile = UserProfileManager()

    # Set user name
    profile.set_user_name("Vatsal")

    # Add things to change
    profile.add_thing_to_change("Improve wake word detection", category="features", priority="high")
    profile.add_thing_to_change("Add dark mode to settings", category="ui", priority="medium")

    # Set custom settings
    profile.set_custom_setting("favorite_color", "blue")
    profile.set_custom_setting("preferred_browser", "Chrome")

    # Record interaction
    profile.record_interaction("open calculator")

    # Print summary
    print(profile.get_profile_summary())
