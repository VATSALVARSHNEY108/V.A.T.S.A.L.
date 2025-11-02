"""
🧠 Behavioral Learning Engine
Learns user habits over time and predicts next actions for intelligent automation
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict, Counter

class BehavioralLearningEngine:
    """Learns user patterns and provides intelligent predictions"""
    
    def __init__(self):
        self.patterns_file = "behavioral_patterns.json"
        self.context_file = "behavioral_context.json"
        self.patterns = self.load_patterns()
        self.context = self.load_context()
        
    def load_patterns(self):
        """Load learned behavior patterns"""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "time_based": {},
            "sequence_based": {},
            "context_based": {},
            "app_usage": {},
            "command_frequency": {}
        }
    
    def save_patterns(self):
        """Save learned patterns"""
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving patterns: {e}")
    
    def load_context(self):
        """Load current context"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "current_activity": "idle",
            "location": "unknown",
            "last_command": None,
            "command_history": [],
            "energy_mode": "balanced"
        }
    
    def save_context(self):
        """Save current context"""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(self.context, f, indent=2)
        except Exception as e:
            print(f"Error saving context: {e}")
    
    def record_action(self, action: str, context_info: Dict = None):
        """Record a user action to learn patterns"""
        now = datetime.now()
        hour = now.hour
        day_of_week = now.strftime("%A")
        time_key = f"{day_of_week}_{hour}"
        
        if time_key not in self.patterns["time_based"]:
            self.patterns["time_based"][time_key] = []
        
        self.patterns["time_based"][time_key].append(action)
        
        if action not in self.patterns["command_frequency"]:
            self.patterns["command_frequency"][action] = 0
        self.patterns["command_frequency"][action] += 1
        
        if len(self.context["command_history"]) > 0:
            last_action = self.context["command_history"][-1]
            sequence_key = f"{last_action}_>{action}"
            
            if sequence_key not in self.patterns["sequence_based"]:
                self.patterns["sequence_based"][sequence_key] = 0
            self.patterns["sequence_based"][sequence_key] += 1
        
        self.context["command_history"].append(action)
        if len(self.context["command_history"]) > 50:
            self.context["command_history"] = self.context["command_history"][-50:]
        
        self.context["last_command"] = action
        
        self.save_patterns()
        self.save_context()
        
        return {"success": True, "message": f"Recorded action: {action}"}
    
    def predict_next_action(self):
        """Predict what the user might want to do next"""
        predictions = []
        
        now = datetime.now()
        hour = now.hour
        day_of_week = now.strftime("%A")
        time_key = f"{day_of_week}_{hour}"
        
        if time_key in self.patterns["time_based"]:
            time_actions = self.patterns["time_based"][time_key]
            action_counts = Counter(time_actions)
            most_common = action_counts.most_common(3)
            
            for action, count in most_common:
                confidence = (count / len(time_actions)) * 100
                predictions.append({
                    "action": action,
                    "reason": f"You often do this on {day_of_week} at {hour}:00",
                    "confidence": f"{confidence:.1f}%"
                })
        
        if len(self.context["command_history"]) > 0:
            last_action = self.context["command_history"][-1]
            
            for seq_key, count in self.patterns["sequence_based"].items():
                if seq_key.startswith(last_action + "_>"):
                    next_action = seq_key.split("_>")[1]
                    predictions.append({
                        "action": next_action,
                        "reason": f"You usually do this after '{last_action}'",
                        "confidence": "High"
                    })
        
        if not predictions:
            top_commands = sorted(
                self.patterns["command_frequency"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            for action, count in top_commands:
                predictions.append({
                    "action": action,
                    "reason": f"This is one of your frequent actions ({count} times)",
                    "confidence": "Medium"
                })
        
        return predictions[:5]
    
    def get_habit_summary(self):
        """Get a summary of learned habits"""
        output = "\n" + "="*60 + "\n"
        output += "🧠 BEHAVIORAL LEARNING SUMMARY\n"
        output += "="*60 + "\n\n"
        
        output += "📊 Most Frequent Actions:\n"
        top_actions = sorted(
            self.patterns["command_frequency"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        for i, (action, count) in enumerate(top_actions, 1):
            output += f"  {i}. {action} - {count} times\n"
        
        output += "\n⏰ Time-Based Patterns:\n"
        time_patterns = {}
        for time_key, actions in self.patterns["time_based"].items():
            if len(actions) >= 3:
                most_common_action = Counter(actions).most_common(1)[0][0]
                time_patterns[time_key] = most_common_action
        
        for time_key, action in sorted(time_patterns.items())[:10]:
            day, hour = time_key.split("_")
            output += f"  {day} at {hour}:00 → {action}\n"
        
        output += "\n🔗 Common Sequences:\n"
        top_sequences = sorted(
            self.patterns["sequence_based"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        for seq, count in top_sequences:
            actions = seq.split("_>")
            output += f"  {actions[0]} → {actions[1]} ({count} times)\n"
        
        output += "\n💡 Predictions for Now:\n"
        predictions = self.predict_next_action()
        for i, pred in enumerate(predictions, 1):
            output += f"  {i}. {pred['action']}\n"
            output += f"     {pred['reason']} (Confidence: {pred['confidence']})\n"
        
        output += "\n" + "="*60 + "\n"
        
        return output
    
    def set_context(self, activity: str = None, location: str = None, energy_mode: str = None):
        """Set the current context for context-aware automation"""
        if activity:
            self.context["current_activity"] = activity
        if location:
            self.context["location"] = location
        if energy_mode and energy_mode in ["power_save", "balanced", "performance"]:
            self.context["energy_mode"] = energy_mode
        
        self.save_context()
        
        return {
            "success": True,
            "message": f"Context updated: activity={self.context['current_activity']}, location={self.context['location']}, energy={self.context['energy_mode']}"
        }
    
    def get_context_recommendations(self):
        """Get recommendations based on current context"""
        recommendations = []
        
        activity = self.context["current_activity"]
        energy_mode = self.context["energy_mode"]
        
        if activity == "coding":
            recommendations.append("💻 Focus mode enabled - Minimize distractions")
            recommendations.append("🎵 Play concentration music")
            recommendations.append("📝 Open coding tools and documentation")
        
        elif activity == "meeting":
            recommendations.append("🔇 Enable do not disturb")
            recommendations.append("📹 Check camera and microphone")
            recommendations.append("📋 Open calendar and notes")
        
        elif activity == "break":
            recommendations.append("☕ Take a walk or stretch")
            recommendations.append("🎵 Play relaxing music")
            recommendations.append("📊 Review productivity stats")
        
        if energy_mode == "power_save":
            recommendations.append("🔋 Reducing screen brightness")
            recommendations.append("⚡ Closing unnecessary applications")
            recommendations.append("🌙 Enabling dark mode for all apps")
        
        return recommendations
    
    def reset_learning(self):
        """Reset all learned patterns"""
        self.patterns = {
            "time_based": {},
            "sequence_based": {},
            "context_based": {},
            "app_usage": {},
            "command_frequency": {}
        }
        self.save_patterns()
        
        return {"success": True, "message": "All learned patterns have been reset"}


def create_behavioral_learning():
    """Factory function to create a BehavioralLearningEngine instance"""
    return BehavioralLearningEngine()
