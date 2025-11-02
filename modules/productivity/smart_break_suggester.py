"""
Smart Break Suggestions - AI recommends optimal activity type for breaks
Personalized based on time of day, energy level, and work intensity
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import random


class SmartBreakSuggester:
    """Suggests optimal break activities based on context"""
    
    def __init__(self, gemini_model=None):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.break_history_file = self.data_dir / "break_history.json"
        self.gemini = gemini_model
        
        # Break activity categories
        self.break_activities = {
            "physical": [
                {"name": "Walk", "duration": 5, "energy_gain": 15, "description": "Take a 5-minute walk around your space"},
                {"name": "Stretch", "duration": 3, "energy_gain": 10, "description": "Full body stretching routine"},
                {"name": "Exercise", "duration": 10, "energy_gain": 25, "description": "Quick exercise (jumping jacks, push-ups)"},
                {"name": "Yoga", "duration": 10, "energy_gain": 20, "description": "Simple yoga poses for desk workers"}
            ],
            "mental": [
                {"name": "Meditate", "duration": 5, "energy_gain": 15, "description": "5-minute mindfulness meditation"},
                {"name": "Deep Breathing", "duration": 2, "energy_gain": 8, "description": "Box breathing or 4-7-8 technique"},
                {"name": "Music", "duration": 5, "energy_gain": 10, "description": "Listen to calming music"},
                {"name": "Nature Sounds", "duration": 3, "energy_gain": 8, "description": "Close eyes and listen to nature"}
            ],
            "social": [
                {"name": "Chat", "duration": 5, "energy_gain": 12, "description": "Quick chat with a colleague or friend"},
                {"name": "Video Call", "duration": 10, "energy_gain": 15, "description": "Short video call with loved ones"},
                {"name": "Team Check-in", "duration": 5, "energy_gain": 10, "description": "Quick team bonding moment"}
            ],
            "refreshment": [
                {"name": "Water", "duration": 1, "energy_gain": 5, "description": "Drink a glass of water"},
                {"name": "Snack", "duration": 3, "energy_gain": 8, "description": "Healthy snack (fruit, nuts)"},
                {"name": "Coffee/Tea", "duration": 5, "energy_gain": 10, "description": "Make fresh coffee or tea"},
                {"name": "Meal", "duration": 15, "energy_gain": 20, "description": "Proper meal break"}
            ],
            "creative": [
                {"name": "Doodle", "duration": 5, "energy_gain": 10, "description": "Free drawing or doodling"},
                {"name": "Read", "duration": 10, "energy_gain": 12, "description": "Read something non-work related"},
                {"name": "Journal", "duration": 5, "energy_gain": 10, "description": "Quick journaling or reflection"},
                {"name": "Puzzle", "duration": 5, "energy_gain": 8, "description": "Quick puzzle or brain teaser"}
            ],
            "sensory": [
                {"name": "Fresh Air", "duration": 3, "energy_gain": 10, "description": "Step outside for fresh air"},
                {"name": "Sunlight", "duration": 5, "energy_gain": 12, "description": "Get natural sunlight exposure"},
                {"name": "Eye Rest", "duration": 2, "energy_gain": 8, "description": "20-20-20 rule: look 20ft away for 20 seconds"},
                {"name": "Cold Water Face Wash", "duration": 2, "energy_gain": 10, "description": "Splash cold water on face"}
            ]
        }
        
        self.last_break_time = None
        self.breaks_today = 0
    
    def suggest_break(self, energy_level=50, work_intensity="medium", time_since_last_break=60):
        """Suggest optimal break activity based on context"""
        hour = datetime.now().hour
        
        # Determine break category based on context
        if energy_level < 30:
            # Very low energy - physical or refreshment
            preferred_categories = ["physical", "refreshment", "sensory"]
        elif energy_level < 50:
            # Moderate energy - mental or light physical
            preferred_categories = ["mental", "physical", "sensory"]
        elif work_intensity == "high":
            # High intensity work - mental relaxation
            preferred_categories = ["mental", "creative", "sensory"]
        else:
            # Normal - any category
            preferred_categories = list(self.break_activities.keys())
        
        # Time-based adjustments
        if hour < 10:
            # Morning - energizing activities
            preferred_categories = ["physical", "refreshment"]
        elif 12 <= hour < 14:
            # Lunch time - meal/refreshment
            preferred_categories = ["refreshment", "social"]
        elif hour >= 18:
            # Evening - wind down
            preferred_categories = ["mental", "creative"]
        
        # Select random category from preferred
        category = random.choice(preferred_categories)
        activities = self.break_activities[category]
        
        # Select activity based on available time
        if time_since_last_break > 120:
            # Long work session - longer break
            suitable = [a for a in activities if a["duration"] >= 5]
        else:
            # Recent break - quick activity
            suitable = [a for a in activities if a["duration"] <= 5]
        
        activity = random.choice(suitable if suitable else activities)
        
        # Get AI-enhanced suggestion if available
        ai_insight = self._get_ai_break_suggestion(energy_level, category, activity["name"])
        
        return {
            "category": category,
            "activity": activity["name"],
            "duration_minutes": activity["duration"],
            "description": activity["description"],
            "expected_energy_gain": activity["energy_gain"],
            "ai_tip": ai_insight,
            "urgency": "high" if energy_level < 30 else "medium" if energy_level < 50 else "low"
        }
    
    def _get_ai_break_suggestion(self, energy_level, category, activity_name):
        """Get AI-enhanced break suggestion"""
        if not self.gemini:
            return f"Try {activity_name} to recharge!"
        
        try:
            prompt = f"""
            User has energy level of {energy_level}/100.
            Suggesting a {category} break: {activity_name}.
            
            Give ONE SENTENCE of encouraging, specific advice for this break.
            Be motivating and practical.
            """
            
            response = self.gemini.generate_content(prompt)
            return response.text.strip()
        except:
            return f"Perfect time for {activity_name}!"
    
    def log_break(self, activity, duration_minutes, energy_before, energy_after):
        """Log break activity and effectiveness"""
        try:
            history = []
            if self.break_history_file.exists():
                with open(self.break_history_file, 'r') as f:
                    history = json.load(f)
            
            entry = {
                "timestamp": datetime.now().isoformat(),
                "activity": activity,
                "duration_minutes": duration_minutes,
                "energy_before": energy_before,
                "energy_after": energy_after,
                "energy_gain": energy_after - energy_before,
                "hour_of_day": datetime.now().hour
            }
            
            history.append(entry)
            history = history[-500:]  # Keep last 500
            
            with open(self.break_history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            self.last_break_time = datetime.now()
            self.breaks_today += 1
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_break_analytics(self, days=7):
        """Analyze break effectiveness"""
        try:
            if not self.break_history_file.exists():
                return {"success": False, "message": "No break history"}
            
            with open(self.break_history_file, 'r') as f:
                history = json.load(f)
            
            cutoff = datetime.now() - timedelta(days=days)
            recent = [
                b for b in history
                if datetime.fromisoformat(b["timestamp"]) > cutoff
            ]
            
            if not recent:
                return {"success": False, "message": "No recent breaks"}
            
            # Calculate effectiveness by activity
            activity_stats = {}
            for entry in recent:
                activity = entry["activity"]
                if activity not in activity_stats:
                    activity_stats[activity] = {"count": 0, "total_gain": 0}
                activity_stats[activity]["count"] += 1
                activity_stats[activity]["total_gain"] += entry["energy_gain"]
            
            # Calculate average gain per activity
            for activity in activity_stats:
                avg_gain = activity_stats[activity]["total_gain"] / activity_stats[activity]["count"]
                activity_stats[activity]["avg_energy_gain"] = round(avg_gain, 1)
            
            # Best activity
            best_activity = max(activity_stats.items(), key=lambda x: x[1]["avg_energy_gain"])[0] if activity_stats else None
            
            return {
                "success": True,
                "days": days,
                "total_breaks": len(recent),
                "avg_breaks_per_day": len(recent) / days,
                "activity_stats": activity_stats,
                "most_effective": best_activity
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
_break_suggester = None

def get_break_suggester(gemini_model=None):
    """Get or create break suggester instance"""
    global _break_suggester
    if _break_suggester is None:
        _break_suggester = SmartBreakSuggester(gemini_model)
    return _break_suggester
