"""
Energy Level Tracker - Tracks energy based on typing/mouse patterns
Suggests breaks or task changes based on detected energy levels
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque


class EnergyLevelTracker:
    """Tracks user energy levels through activity patterns"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.energy_log_file = self.data_dir / "energy_levels.json"
        
        # Activity buffers (last 5 minutes of activity)
        self.keyboard_buffer = deque(maxlen=300)  # 5 min at 1 sec intervals
        self.mouse_buffer = deque(maxlen=300)
        self.activity_timestamps = deque(maxlen=300)
        
        # Energy metrics
        self.current_energy_level = 50  # 0-100 scale
        self.energy_trend = "stable"  # rising, falling, stable
        self.last_break_suggestion = None
        
        # Activity thresholds
        self.high_energy_threshold = 70
        self.low_energy_threshold = 30
        self.burnout_threshold = 15
        
        # Patterns
        self.typing_speed_history = []
        self.mouse_movement_history = []
    
    def record_keyboard_event(self):
        """Record a keyboard activity event"""
        self.keyboard_buffer.append(1)
        self.activity_timestamps.append(datetime.now())
        self._update_energy_level()
    
    def record_mouse_event(self, movement_distance=1):
        """Record a mouse movement event"""
        self.mouse_buffer.append(movement_distance)
        self.activity_timestamps.append(datetime.now())
        self._update_energy_level()
    
    def _update_energy_level(self):
        """Calculate current energy level based on activity patterns"""
        if len(self.activity_timestamps) < 10:
            return  # Not enough data
        
        # Get activity in last minute
        one_min_ago = datetime.now() - timedelta(minutes=1)
        recent_activity = sum(
            1 for ts in self.activity_timestamps
            if ts > one_min_ago
        )
        
        # Calculate typing rate
        typing_rate = sum(self.keyboard_buffer) / len(self.keyboard_buffer) if self.keyboard_buffer else 0
        
        # Calculate mouse activity
        mouse_activity = sum(self.mouse_buffer) / len(self.mouse_buffer) if self.mouse_buffer else 0
        
        # Combined activity score (0-100)
        activity_score = min(100, (typing_rate * 50 + mouse_activity * 30 + recent_activity * 2))
        
        # Update energy level (weighted average)
        self.current_energy_level = (self.current_energy_level * 0.7) + (activity_score * 0.3)
        
        # Detect trend
        if len(self.typing_speed_history) > 5:
            recent_avg = sum(self.typing_speed_history[-5:]) / 5
            older_avg = sum(self.typing_speed_history[-10:-5]) / 5 if len(self.typing_speed_history) >= 10 else recent_avg
            
            if recent_avg > older_avg * 1.1:
                self.energy_trend = "rising"
            elif recent_avg < older_avg * 0.9:
                self.energy_trend = "falling"
            else:
                self.energy_trend = "stable"
        
        # Store for trend analysis
        self.typing_speed_history.append(typing_rate)
        self.mouse_movement_history.append(mouse_activity)
        
        # Keep only last 100 measurements
        if len(self.typing_speed_history) > 100:
            self.typing_speed_history.pop(0)
        if len(self.mouse_movement_history) > 100:
            self.mouse_movement_history.pop(0)
    
    def get_current_energy(self):
        """Get current energy level and status"""
        # Determine energy category
        if self.current_energy_level >= self.high_energy_threshold:
            category = "high"
            emoji = "🔋"
            status = "Peak Performance"
        elif self.current_energy_level >= 50:
            category = "medium"
            emoji = "⚡"
            status = "Steady Energy"
        elif self.current_energy_level >= self.low_energy_threshold:
            category = "low"
            emoji = "🪫"
            status = "Declining Energy"
        else:
            category = "very_low"
            emoji = "❌"
            status = "Burnout Risk"
        
        return {
            "level": int(self.current_energy_level),
            "category": category,
            "emoji": emoji,
            "status": status,
            "trend": self.energy_trend,
            "suggestion": self._get_energy_suggestion(category)
        }
    
    def _get_energy_suggestion(self, category):
        """Get suggestion based on energy level"""
        suggestions = {
            "high": [
                "✨ Your energy is great! Tackle your most challenging tasks now.",
                "🚀 Perfect time for deep, creative work!",
                "💪 Use this energy for important decisions or complex problems."
            ],
            "medium": [
                "⚡ Steady energy. Good for moderate tasks and meetings.",
                "📋 Maintain momentum with organized, structured work.",
                "🎯 Perfect for completing ongoing tasks."
            ],
            "low": [
                "☕ Energy dipping. Consider a 5-minute break.",
                "🌿 Time for a quick walk or stretch to recharge.",
                "💧 Hydrate and take a brief mental reset."
            ],
            "very_low": [
                "⚠️ BREAK NEEDED! Step away for 10-15 minutes.",
                "🛑 You're approaching burnout. Take a proper break now!",
                "🌳 Go outside, breathe fresh air, or take a power nap."
            ]
        }
        
        import random
        return random.choice(suggestions.get(category, ["Monitor your energy levels"]))
    
    def suggest_break_or_task_change(self):
        """Suggest if user should take break or change tasks"""
        energy = self.get_current_energy()
        
        # Check if enough time since last suggestion
        if self.last_break_suggestion:
            time_since = (datetime.now() - self.last_break_suggestion).total_seconds()
            if time_since < 600:  # Don't suggest more than once per 10 minutes
                return {"should_act": False, "message": "Recent suggestion still applies"}
        
        if energy["category"] == "very_low":
            self.last_break_suggestion = datetime.now()
            return {
                "should_act": True,
                "action": "take_break",
                "duration": 15,
                "reason": "Energy critically low - burnout risk",
                "message": "🛑 MANDATORY BREAK: You need 15 minutes to recover. Step away now!",
                "urgency": "critical"
            }
        
        elif energy["category"] == "low" and energy["trend"] == "falling":
            self.last_break_suggestion = datetime.now()
            return {
                "should_act": True,
                "action": "take_break",
                "duration": 5,
                "reason": "Energy declining steadily",
                "message": "☕ Quick 5-minute break recommended to recharge.",
                "urgency": "medium"
            }
        
        elif energy["category"] == "medium" and energy["trend"] == "falling":
            return {
                "should_act": True,
                "action": "change_task",
                "reason": "Energy moderating - switch to lighter tasks",
                "message": "📝 Consider switching to easier, routine tasks for a while.",
                "urgency": "low"
            }
        
        return {
            "should_act": False,
            "message": "Energy levels good - keep going!",
            "current_level": energy["level"]
        }
    
    def log_energy_data(self):
        """Log current energy snapshot"""
        try:
            log = []
            if self.energy_log_file.exists():
                with open(self.energy_log_file, 'r') as f:
                    log = json.load(f)
            
            energy = self.get_current_energy()
            entry = {
                "timestamp": datetime.now().isoformat(),
                "energy_level": energy["level"],
                "category": energy["category"],
                "trend": energy["trend"],
                "typing_rate": sum(self.typing_speed_history[-10:]) / 10 if self.typing_speed_history else 0,
                "mouse_activity": sum(self.mouse_movement_history[-10:]) / 10 if self.mouse_movement_history else 0
            }
            
            log.append(entry)
            log = log[-1000:]  # Keep last 1000 entries
            
            with open(self.energy_log_file, 'w') as f:
                json.dump(log, f, indent=2)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_energy_patterns(self, hours=8):
        """Analyze energy patterns over time"""
        try:
            if not self.energy_log_file.exists():
                return {"success": False, "message": "No energy data logged yet"}
            
            with open(self.energy_log_file, 'r') as f:
                log = json.load(f)
            
            cutoff = datetime.now() - timedelta(hours=hours)
            recent = [
                e for e in log
                if datetime.fromisoformat(e["timestamp"]) > cutoff
            ]
            
            if not recent:
                return {"success": False, "message": "No recent data"}
            
            # Calculate average energy by hour
            hourly_avg = {}
            for entry in recent:
                hour = datetime.fromisoformat(entry["timestamp"]).hour
                if hour not in hourly_avg:
                    hourly_avg[hour] = []
                hourly_avg[hour].append(entry["energy_level"])
            
            hourly_avg = {
                hour: sum(levels) / len(levels)
                for hour, levels in hourly_avg.items()
            }
            
            # Find peak and low energy hours
            peak_hour = max(hourly_avg.items(), key=lambda x: x[1])[0] if hourly_avg else None
            low_hour = min(hourly_avg.items(), key=lambda x: x[1])[0] if hourly_avg else None
            
            return {
                "success": True,
                "hourly_average": hourly_avg,
                "peak_hour": peak_hour,
                "low_hour": low_hour,
                "total_entries": len(recent),
                "avg_energy": sum(e["energy_level"] for e in recent) / len(recent)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
_energy_tracker = None

def get_energy_tracker():
    """Get or create energy tracker instance"""
    global _energy_tracker
    if _energy_tracker is None:
        _energy_tracker = EnergyLevelTracker()
    return _energy_tracker


if __name__ == "__main__":
    # Test the energy tracker
    tracker = get_energy_tracker()
    
    print("Testing Energy Level Tracker...")
    
    # Simulate some activity
    for i in range(20):
        tracker.record_keyboard_event()
        tracker.record_mouse_event(2)
        time.sleep(0.1)
    
    energy = tracker.get_current_energy()
    print(f"\nCurrent Energy: {json.dumps(energy, indent=2)}")
    
    suggestion = tracker.suggest_break_or_task_change()
    print(f"\nSuggestion: {json.dumps(suggestion, indent=2)}")
    
    tracker.log_energy_data()
    print("\n✅ Energy data logged")
