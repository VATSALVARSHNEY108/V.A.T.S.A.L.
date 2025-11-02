"""
🤝 Human-Like Interaction
Context recall, adaptive tone, emotional intelligence, and gamified productivity
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class HumanInteraction:
    """Human-like interaction features with emotional intelligence"""
    
    def __init__(self):
        self.conversation_file = "conversation_context.json"
        self.goals_file = "user_goals.json"
        self.achievements_file = "achievements.json"
        self.tone_settings_file = "tone_settings.json"
        self.conversation_context = self.load_conversation_context()
        self.goals = self.load_goals()
        self.achievements = self.load_achievements()
        self.tone_settings = self.load_tone_settings()
        
    def load_conversation_context(self):
        """Load conversation context and memory"""
        if os.path.exists(self.conversation_file):
            try:
                with open(self.conversation_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "previous_sessions": [],
            "topics_discussed": [],
            "user_preferences": {},
            "last_interaction": None
        }
    
    def save_conversation_context(self):
        """Save conversation context"""
        try:
            with open(self.conversation_file, 'w') as f:
                json.dump(self.conversation_context, f, indent=2)
        except Exception as e:
            print(f"Error saving conversation context: {e}")
    
    def load_goals(self):
        """Load user goals"""
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_goals(self):
        """Save goals"""
        try:
            with open(self.goals_file, 'w') as f:
                json.dump(self.goals, f, indent=2)
        except Exception as e:
            print(f"Error saving goals: {e}")
    
    def load_achievements(self):
        """Load achievements"""
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "total_xp": 0,
            "level": 1,
            "unlocked_achievements": [],
            "tasks_completed": 0
        }
    
    def save_achievements(self):
        """Save achievements"""
        try:
            with open(self.achievements_file, 'w') as f:
                json.dump(self.achievements, f, indent=2)
        except Exception as e:
            print(f"Error saving achievements: {e}")
    
    def load_tone_settings(self):
        """Load tone settings"""
        if os.path.exists(self.tone_settings_file):
            try:
                with open(self.tone_settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "current_tone": "casual",
            "formality_level": 5,
            "emoji_usage": True
        }
    
    def save_tone_settings(self):
        """Save tone settings"""
        try:
            with open(self.tone_settings_file, 'w') as f:
                json.dump(self.tone_settings, f, indent=2)
        except Exception as e:
            print(f"Error saving tone settings: {e}")
    
    def remember_conversation(self, topic: str, details: str):
        """Remember previous sessions and suggest follow-ups"""
        session = {
            "topic": topic,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "follow_up_suggested": False
        }
        
        self.conversation_context["previous_sessions"].append(session)
        if topic not in self.conversation_context["topics_discussed"]:
            self.conversation_context["topics_discussed"].append(topic)
        
        self.conversation_context["last_interaction"] = datetime.now().isoformat()
        
        if len(self.conversation_context["previous_sessions"]) > 100:
            self.conversation_context["previous_sessions"] = self.conversation_context["previous_sessions"][-100:]
        
        self.save_conversation_context()
        
        return {"success": True, "message": f"Remembered conversation about: {topic}"}
    
    def get_conversation_summary(self):
        """Get summary of conversation history"""
        output = "\n" + "="*60 + "\n"
        output += "💭 CONVERSATION MEMORY\n"
        output += "="*60 + "\n\n"
        
        output += f"Last Interaction: {self.conversation_context.get('last_interaction', 'Never')}\n"
        output += f"Topics Discussed: {len(self.conversation_context['topics_discussed'])}\n\n"
        
        output += "Recent Sessions:\n"
        for session in self.conversation_context["previous_sessions"][-5:]:
            output += f"  • {session['topic']}\n"
            output += f"    {session.get('details', '')[:60]}...\n"
        
        output += "\n" + "="*60 + "\n"
        return output
    
    def set_tone(self, tone: str):
        """Adjust response tone (professional, casual, developer-friendly, etc.)"""
        valid_tones = ["professional", "casual", "developer-friendly", "friendly", "formal"]
        
        if tone.lower() not in valid_tones:
            return {"success": False, "message": f"Invalid tone. Choose from: {', '.join(valid_tones)}"}
        
        self.tone_settings["current_tone"] = tone.lower()
        
        tone_descriptions = {
            "professional": "Formal and business-like responses",
            "casual": "Relaxed and friendly communication",
            "developer-friendly": "Technical with code examples",
            "friendly": "Warm and supportive interaction",
            "formal": "Strictly professional tone"
        }
        
        self.save_tone_settings()
        
        return {
            "success": True,
            "message": f"Tone set to: {tone}",
            "description": tone_descriptions[tone.lower()]
        }
    
    def get_tone_settings(self):
        """Get current tone settings"""
        output = "\n" + "="*60 + "\n"
        output += "🎭 TONE SETTINGS\n"
        output += "="*60 + "\n\n"
        
        output += f"Current Tone: {self.tone_settings['current_tone'].title()}\n"
        output += f"Formality Level: {self.tone_settings.get('formality_level', 5)}/10\n"
        output += f"Emoji Usage: {'✅ Enabled' if self.tone_settings.get('emoji_usage', True) else '❌ Disabled'}\n"
        
        output += "\n" + "="*60 + "\n"
        return output
    
    def detect_stress(self, typing_speed: float = None, message_tone: str = None):
        """Offer supportive prompts when stress or burnout is detected"""
        stress_detected = False
        stress_level = 0
        
        if typing_speed and typing_speed < 20:
            stress_level += 2
        
        if message_tone and any(word in message_tone.lower() for word in ["tired", "stressed", "overwhelmed", "exhausted"]):
            stress_level += 3
            stress_detected = True
        
        if stress_level >= 3:
            return {
                "success": True,
                "stress_detected": True,
                "level": "High",
                "suggestions": [
                    "☕ Take a 5-minute break",
                    "🧘 Try a quick breathing exercise",
                    "🚶 Go for a short walk",
                    "💧 Stay hydrated",
                    "📋 Break down tasks into smaller steps"
                ],
                "supportive_message": "I notice you might be feeling stressed. Remember to take care of yourself!"
            }
        
        return {"success": True, "stress_detected": False, "message": "You're doing great!"}
    
    def track_goal(self, goal_name: str, target: str, deadline: str = None):
        """Track personal or professional goals across apps"""
        goal = {
            "name": goal_name,
            "target": target,
            "deadline": deadline,
            "created_at": datetime.now().isoformat(),
            "progress": 0,
            "status": "in_progress"
        }
        
        self.goals.append(goal)
        self.save_goals()
        
        return {"success": True, "message": f"Goal tracked: {goal_name}"}
    
    def update_goal_progress(self, goal_name: str, progress: int):
        """Update progress on a goal"""
        for goal in self.goals:
            if goal["name"].lower() == goal_name.lower():
                goal["progress"] = progress
                if progress >= 100:
                    goal["status"] = "completed"
                    self.award_xp(50, f"Completed goal: {goal_name}")
                self.save_goals()
                return {"success": True, "message": f"Goal '{goal_name}' progress: {progress}%"}
        
        return {"success": False, "message": "Goal not found"}
    
    def get_goals_summary(self):
        """Get summary of goals and progress"""
        if not self.goals:
            return "No goals tracked yet."
        
        output = "\n" + "="*60 + "\n"
        output += "🎯 GOAL TRACKER\n"
        output += "="*60 + "\n\n"
        
        for i, goal in enumerate(self.goals, 1):
            status_emoji = "✅" if goal['status'] == "completed" else "🔄"
            output += f"{i}. {status_emoji} {goal['name']}\n"
            output += f"   Target: {goal.get('target', 'N/A')}\n"
            output += f"   Progress: {goal.get('progress', 0)}%\n"
            if goal.get('deadline'):
                output += f"   Deadline: {goal['deadline']}\n"
            output += "\n"
        
        output += "="*60 + "\n"
        return output
    
    def award_xp(self, xp_amount: int, reason: str):
        """Award XP for completing tasks (gamified productivity)"""
        self.achievements["total_xp"] += xp_amount
        self.achievements["tasks_completed"] += 1
        
        new_level = (self.achievements["total_xp"] // 100) + 1
        level_up = new_level > self.achievements["level"]
        
        if level_up:
            self.achievements["level"] = new_level
        
        self.save_achievements()
        
        output = f"\n🎮 +{xp_amount} XP Earned!\n"
        output += f"Reason: {reason}\n"
        output += f"Total XP: {self.achievements['total_xp']}\n"
        output += f"Level: {self.achievements['level']}\n"
        
        if level_up:
            output += f"\n🎉 LEVEL UP! You reached Level {new_level}!\n"
        
        return {"success": True, "message": output, "level_up": level_up}
    
    def get_achievements_summary(self):
        """Get gamification summary"""
        output = "\n" + "="*60 + "\n"
        output += "🏆 ACHIEVEMENTS & PROGRESS\n"
        output += "="*60 + "\n\n"
        
        output += f"Level: {self.achievements['level']}\n"
        output += f"Total XP: {self.achievements['total_xp']}\n"
        output += f"Tasks Completed: {self.achievements['tasks_completed']}\n"
        xp_to_next_level = (self.achievements['level'] * 100) - self.achievements['total_xp']
        output += f"XP to Next Level: {xp_to_next_level}\n\n"
        
        output += "Unlocked Achievements:\n"
        if self.achievements.get("unlocked_achievements"):
            for achievement in self.achievements["unlocked_achievements"]:
                output += f"  🏅 {achievement}\n"
        else:
            output += "  Keep working to unlock achievements!\n"
        
        output += "\n" + "="*60 + "\n"
        return output


def create_human_interaction():
    """Factory function to create a HumanInteraction instance"""
    return HumanInteraction()
