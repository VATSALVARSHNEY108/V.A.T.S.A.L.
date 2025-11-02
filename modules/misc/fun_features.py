"""
Fun Features Module
Mood themes, compliments system, mini chatbot companion
"""

import json
import os
import random
from datetime import datetime
import subprocess
import platform

class FunFeatures:
    def __init__(self):
        self.compliments_file = "compliments.json"
        self.mood_config_file = "mood_config.json"
        self.chatbot_context_file = "chatbot_context.json"
        
        self.load_compliments()
        self.load_mood_config()
        self.load_chatbot_context()
        
        self.wallpapers = {
            "happy": ["beach.jpg", "sunset.jpg", "flowers.jpg"],
            "calm": ["forest.jpg", "lake.jpg", "mountains.jpg"],
            "energetic": ["city.jpg", "abstract.jpg", "neon.jpg"],
            "focused": ["minimal.jpg", "dark.jpg", "workspace.jpg"]
        }
    
    def load_compliments(self):
        """Load compliments database"""
        if os.path.exists(self.compliments_file):
            with open(self.compliments_file, 'r') as f:
                data = json.load(f)
                self.compliments = data.get("compliments", [])
                self.encouragements = data.get("encouragements", [])
        else:
            self.compliments = [
                "You're doing amazing! 🌟",
                "Your code is looking great today! 💻",
                "You're making excellent progress! 🚀",
                "That was a smart move! 🧠",
                "You're absolutely crushing it! 💪",
                "Your productivity is inspiring! ⭐",
                "Great job on that task! 🎯",
                "You're on fire today! 🔥",
                "Your dedication is admirable! 🏆",
                "Keep up the fantastic work! 🎉"
            ]
            
            self.encouragements = [
                "Don't give up! You've got this! 💪",
                "Every expert was once a beginner. Keep learning! 📚",
                "Progress, not perfection! 🌱",
                "You're stronger than you think! 💎",
                "Mistakes are proof you're trying! 🎯",
                "Believe in yourself! ⭐",
                "Small steps lead to big achievements! 🚶‍♂️",
                "You're capable of amazing things! 🌟",
                "Keep pushing forward! 🚀",
                "Your hard work will pay off! 🏆"
            ]
            
            self.save_compliments()
    
    def save_compliments(self):
        """Save compliments database"""
        with open(self.compliments_file, 'w') as f:
            json.dump({
                "compliments": self.compliments,
                "encouragements": self.encouragements
            }, f, indent=2)
    
    def load_mood_config(self):
        """Load mood theme configuration"""
        if os.path.exists(self.mood_config_file):
            with open(self.mood_config_file, 'r') as f:
                self.mood_config = json.load(f)
        else:
            self.mood_config = {
                "current_mood": "neutral",
                "spotify_integration": False,
                "auto_theme": False
            }
            self.save_mood_config()
    
    def save_mood_config(self):
        """Save mood configuration"""
        with open(self.mood_config_file, 'w') as f:
            json.dump(self.mood_config, f, indent=2)
    
    def load_chatbot_context(self):
        """Load chatbot conversation context"""
        if os.path.exists(self.chatbot_context_file):
            with open(self.chatbot_context_file, 'r') as f:
                self.chatbot_context = json.load(f)
        else:
            self.chatbot_context = {
                "user_name": "Friend",
                "conversation_history": [],
                "personality": "friendly"
            }
            self.save_chatbot_context()
    
    def save_chatbot_context(self):
        """Save chatbot context"""
        with open(self.chatbot_context_file, 'w') as f:
            json.dump(self.chatbot_context, f, indent=2)
    
    def get_random_compliment(self):
        """Get a random compliment"""
        compliment = random.choice(self.compliments)
        return f"✨ {compliment}"
    
    def get_random_encouragement(self):
        """Get a random encouragement"""
        encouragement = random.choice(self.encouragements)
        return f"💝 {encouragement}"
    
    def celebrate_task_completion(self):
        """Celebrate completing a task"""
        celebrations = [
            "🎉 Woohoo! Task completed! You're unstoppable!",
            "🏆 Another win! You're on a roll!",
            "⭐ Excellent work! That's how it's done!",
            "🚀 Mission accomplished! Ready for the next challenge?",
            "💪 Crushed it! You're making great progress!",
            "🎯 Bulls-eye! Perfect execution!",
            "🌟 Brilliant! Your skills are showing!",
            "✅ Done and dusted! Time to celebrate!",
            "👏 Standing ovation! That was impressive!",
            "🔥 On fire! Nothing can stop you now!"
        ]
        
        return random.choice(celebrations)
    
    def set_mood_theme(self, mood):
        """Set desktop theme based on mood"""
        try:
            valid_moods = ["happy", "calm", "energetic", "focused", "neutral"]
            
            if mood not in valid_moods:
                return f"❌ Invalid mood. Choose from: {', '.join(valid_moods)}"
            
            self.mood_config["current_mood"] = mood
            self.save_mood_config()
            
            if mood == "neutral":
                return "✅ Mood set to neutral (default theme)"
            
            result = f"✅ Mood set to {mood}! 🎨\n"
            result += f"Theme suggestions: {', '.join(self.wallpapers.get(mood, []))}\n"
            
            return result
        except Exception as e:
            return f"❌ Failed to set mood: {str(e)}"
    
    def change_wallpaper_by_mood(self, mood):
        """Change desktop wallpaper based on mood"""
        try:
            wallpaper_suggestions = self.wallpapers.get(mood, ["default.jpg"])
            wallpaper = random.choice(wallpaper_suggestions)
            
            result = f"🖼️ Mood: {mood} - Wallpaper suggestion: {wallpaper}\n"
            result += "ℹ️ Note: Automatic wallpaper changing requires desktop environment.\n"
            result += "For manual change, check your Downloads/Wallpapers folder."
            
            return result
        except Exception as e:
            return f"❌ Failed to change wallpaper: {str(e)}"
    
    def chatbot_respond(self, user_input):
        """Mini chatbot companion response"""
        user_input = user_input.lower().strip()
        
        self.chatbot_context["conversation_history"].append({
            "user": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.chatbot_context["conversation_history"]) > 50:
            self.chatbot_context["conversation_history"] = self.chatbot_context["conversation_history"][-50:]
        
        self.save_chatbot_context()
        
        if any(word in user_input for word in ["hello", "hi", "hey"]):
            responses = [
                f"Hey {self.chatbot_context['user_name']}! How can I help? 😊",
                f"Hi there! Ready to get things done? 🚀",
                f"Hello! What can I do for you today? ✨"
            ]
            return random.choice(responses)
        
        elif any(word in user_input for word in ["how are you", "what's up", "wassup"]):
            responses = [
                "I'm doing great! Ready to help you automate anything! 🤖",
                "All systems operational! How can I assist? ⚡",
                "Feeling productive! What about you? 💪"
            ]
            return random.choice(responses)
        
        elif any(word in user_input for word in ["thanks", "thank you"]):
            responses = [
                "You're welcome! Happy to help! 😊",
                "Anytime! That's what I'm here for! 🌟",
                "My pleasure! Let me know if you need anything else! ✨"
            ]
            return random.choice(responses)
        
        elif any(word in user_input for word in ["good job", "well done", "nice"]):
            return "Aww, thank you! You're the real star here! ⭐"
        
        elif "motivate" in user_input or "encourage" in user_input:
            return self.get_random_encouragement()
        
        elif "compliment" in user_input:
            return self.get_random_compliment()
        
        elif any(word in user_input for word in ["tired", "exhausted", "break"]):
            return "Sounds like you need a break! ☕ Take 5 minutes to rest. You deserve it! 💙"
        
        elif any(word in user_input for word in ["help", "what can you do"]):
            return """I'm your automation buddy! I can:
🎉 Celebrate your wins
💝 Give you compliments
🎨 Suggest mood themes
💬 Chat when you're taking breaks
🚀 Keep you motivated!

Just say 'compliment me' or 'motivate me'!"""
        
        elif "bye" in user_input or "goodbye" in user_input:
            return "See you later! Keep being awesome! 👋✨"
        
        else:
            responses = [
                "Interesting! Tell me more! 🤔",
                "I'm listening! Go on... 👂",
                "Hmm, that's cool! 😊",
                "Got it! Anything else? 💭"
            ]
            return random.choice(responses)
    
    def set_chatbot_name(self, user_name):
        """Set user's name for personalized chatbot"""
        self.chatbot_context["user_name"] = user_name
        self.save_chatbot_context()
        return f"✅ Great to meet you, {user_name}! 👋"
    
    def set_chatbot_personality(self, personality):
        """Set chatbot personality (friendly, professional, funny)"""
        valid_personalities = ["friendly", "professional", "funny", "supportive"]
        
        if personality in valid_personalities:
            self.chatbot_context["personality"] = personality
            self.save_chatbot_context()
            return f"✅ Personality set to: {personality}"
        else:
            return f"❌ Choose from: {', '.join(valid_personalities)}"
    
    def get_conversation_stats(self):
        """Get chatbot conversation statistics"""
        total_messages = len(self.chatbot_context["conversation_history"])
        
        if total_messages == 0:
            return "ℹ️ No conversations yet! Say hi! 👋"
        
        recent = self.chatbot_context["conversation_history"][-5:]
        
        result = f"💬 Chatbot Stats:\n\n"
        result += f"Total messages: {total_messages}\n"
        result += f"Personality: {self.chatbot_context['personality']}\n\n"
        result += "Recent messages:\n"
        
        for msg in recent:
            time = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M")
            result += f"  [{time}] You: {msg['user']}\n"
        
        return result
    
    def add_custom_compliment(self, compliment):
        """Add a custom compliment"""
        self.compliments.append(compliment)
        self.save_compliments()
        return f"✅ Added custom compliment: {compliment}"
    
    def mood_playlist_suggestions(self, mood):
        """Suggest playlists based on mood"""
        playlists = {
            "happy": ["Happy Hits", "Feel Good Pop", "Upbeat Playlist"],
            "calm": ["Peaceful Piano", "Ambient Chill", "Relaxing Vibes"],
            "energetic": ["Workout Beats", "Electronic Energy", "Pump Up Mix"],
            "focused": ["Deep Focus", "Lofi Beats", "Concentration Mix"],
            "sad": ["Sad Songs", "Melancholy Mix", "Emotional Playlist"]
        }
        
        suggestions = playlists.get(mood, ["Mixed Playlist"])
        
        result = f"🎵 Playlist suggestions for {mood} mood:\n"
        for playlist in suggestions:
            result += f"  • {playlist}\n"
        
        return result

if __name__ == "__main__":
    fun = FunFeatures()
    print("Fun Features Module - Testing")
    print(fun.get_random_compliment())
    print(fun.chatbot_respond("Hello!"))
    print(fun.celebrate_task_completion())
