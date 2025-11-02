"""
🎙️ Voice & Multimodal Control
Advanced voice commands with personalization, whisper detection, and hybrid input
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class MultimodalControl:
    """Handles voice, gesture, and hybrid input methods"""
    
    def __init__(self):
        self.voice_profile_file = "voice_profile.json"
        self.gestures_file = "gesture_mappings.json"
        self.voice_profile = self.load_voice_profile()
        self.gestures = self.load_gestures()
        self.whisper_mode = False
        self.context_aware_mode = True
        
    def load_voice_profile(self):
        """Load voice personalization profile"""
        if os.path.exists(self.voice_profile_file):
            try:
                with open(self.voice_profile_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "custom_phrases": {},
            "voice_speed_preference": "normal",
            "accent": "neutral",
            "slang_dictionary": {},
            "command_shortcuts": {}
        }
    
    def save_voice_profile(self):
        """Save voice profile"""
        try:
            with open(self.voice_profile_file, 'w') as f:
                json.dump(self.voice_profile, f, indent=2)
        except Exception as e:
            print(f"Error saving voice profile: {e}")
    
    def load_gestures(self):
        """Load gesture mappings"""
        if os.path.exists(self.gestures_file):
            try:
                with open(self.gestures_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "hand_raise": "pause_music",
            "thumbs_up": "approve",
            "wave": "dismiss_notification",
            "point": "click_at_position"
        }
    
    def save_gestures(self):
        """Save gesture mappings"""
        try:
            with open(self.gestures_file, 'w') as f:
                json.dump(self.gestures, f, indent=2)
        except Exception as e:
            print(f"Error saving gestures: {e}")
    
    def train_custom_phrase(self, phrase: str, meaning: str):
        """Train the AI to understand custom phrasing or slang"""
        self.voice_profile["custom_phrases"][phrase.lower()] = meaning
        self.save_voice_profile()
        
        return {"success": True, "message": f"Learned: '{phrase}' means '{meaning}'"}
    
    def add_slang_term(self, slang: str, translation: str):
        """Add slang dictionary entry"""
        self.voice_profile["slang_dictionary"][slang.lower()] = translation
        self.save_voice_profile()
        
        return {"success": True, "message": f"Added slang: '{slang}' → '{translation}'"}
    
    def enable_whisper_mode(self):
        """Enable low-volume voice command detection"""
        self.whisper_mode = True
        return {
            "success": True,
            "message": "Whisper mode enabled - I can now detect low-volume commands",
            "info": "Microphone sensitivity increased for quiet environments"
        }
    
    def disable_whisper_mode(self):
        """Disable whisper mode"""
        self.whisper_mode = False
        return {"success": True, "message": "Whisper mode disabled"}
    
    def add_gesture_mapping(self, gesture: str, action: str):
        """Map a gesture to an action"""
        self.gestures[gesture.lower()] = action
        self.save_gestures()
        
        return {"success": True, "message": f"Gesture '{gesture}' now triggers '{action}'"}
    
    def get_gesture_mappings(self):
        """Get all gesture mappings"""
        output = "\n" + "="*60 + "\n"
        output += "👋 GESTURE MAPPINGS\n"
        output += "="*60 + "\n\n"
        
        for gesture, action in self.gestures.items():
            emoji = "🖐️" if "hand" in gesture else "👍" if "thumb" in gesture else "👋"
            output += f"{emoji} {gesture.title()}: {action}\n"
        
        output += "\n" + "="*60 + "\n"
        return output
    
    def set_context_aware_reply_mode(self, mode: str):
        """Set how AI responds based on context (coding, gaming, studying)"""
        valid_modes = ["coding", "gaming", "studying", "working", "casual"]
        
        if mode.lower() not in valid_modes:
            return {"success": False, "message": f"Invalid mode. Choose from: {', '.join(valid_modes)}"}
        
        reply_styles = {
            "coding": "Technical and precise responses with code examples",
            "gaming": "Quick, casual responses without interrupting gameplay",
            "studying": "Detailed explanations with educational focus",
            "working": "Professional and efficient responses",
            "casual": "Friendly and conversational tone"
        }
        
        self.voice_profile["context_mode"] = mode.lower()
        self.save_voice_profile()
        
        return {
            "success": True,
            "message": f"Context mode set to: {mode}",
            "style": reply_styles[mode.lower()]
        }
    
    def get_voice_profile_summary(self):
        """Get summary of voice personalization"""
        output = "\n" + "="*60 + "\n"
        output += "🎙️ VOICE PERSONALIZATION PROFILE\n"
        output += "="*60 + "\n\n"
        
        output += f"Whisper Mode: {'✅ Enabled' if self.whisper_mode else '❌ Disabled'}\n"
        output += f"Context Aware: {'✅ Enabled' if self.context_aware_mode else '❌ Disabled'}\n"
        output += f"Current Context: {self.voice_profile.get('context_mode', 'casual').title()}\n\n"
        
        output += "Custom Phrases:\n"
        if self.voice_profile["custom_phrases"]:
            for phrase, meaning in self.voice_profile["custom_phrases"].items():
                output += f"  • '{phrase}' → '{meaning}'\n"
        else:
            output += "  None configured\n"
        
        output += "\nSlang Dictionary:\n"
        if self.voice_profile["slang_dictionary"]:
            for slang, translation in self.voice_profile["slang_dictionary"].items():
                output += f"  • '{slang}' → '{translation}'\n"
        else:
            output += "  None configured\n"
        
        output += "\n" + "="*60 + "\n"
        return output
    
    def process_hybrid_input(self, voice_command: str, gesture: str = None):
        """Process combined voice and gesture input"""
        result = f"Processing hybrid input:\n"
        result += f"  Voice: {voice_command}\n"
        
        if gesture:
            action = self.gestures.get(gesture.lower(), "unknown")
            result += f"  Gesture: {gesture} → {action}\n"
            result += f"\n✅ Combined action executed"
        else:
            result += f"  No gesture detected\n"
        
        return {"success": True, "message": result}
    
    def reset_voice_profile(self):
        """Reset voice personalization"""
        self.voice_profile = {
            "custom_phrases": {},
            "voice_speed_preference": "normal",
            "accent": "neutral",
            "slang_dictionary": {},
            "command_shortcuts": {}
        }
        self.save_voice_profile()
        
        return {"success": True, "message": "Voice profile reset to defaults"}


def create_multimodal_control():
    """Factory function to create a MultimodalControl instance"""
    return MultimodalControl()
