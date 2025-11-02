"""
Predictive Actions Engine
Suggests what you'll need next based on context, patterns, and learning
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter

class PredictedAction:
    """Represents a predicted action"""
    
    def __init__(self, action: str, confidence: float, reasoning: str,
                 category: str = "general", metadata: Optional[Dict] = None):
        self.action = action
        self.confidence = confidence
        self.reasoning = reasoning
        self.category = category
        self.metadata = metadata or {}
        self.predicted_at = datetime.now().isoformat()
        self.was_correct = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "action": self.action,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "category": self.category,
            "metadata": self.metadata,
            "predicted_at": self.predicted_at,
            "was_correct": self.was_correct
        }


class PredictiveActionsEngine:
    """
    Predictive Actions Engine
    
    Features:
    - Context-aware predictions
    - Pattern-based suggestions
    - Time-based proactive actions
    - Sequence prediction
    - Confidence scoring
    - Learning from outcomes
    """
    
    def __init__(self):
        self.predictions_file = "predictions_history.json"
        self.patterns_file = "action_patterns.json"
        self.sequences_file = "action_sequences.json"
        
        self.prediction_history: List[Dict] = []
        self.action_patterns: Dict = {}
        self.action_sequences: List[List[str]] = []
        
        self._load_all()
        
        print("🔮 Predictive Actions Engine initialized")
    
    def _load_all(self):
        """Load all prediction data"""
        if os.path.exists(self.predictions_file):
            try:
                with open(self.predictions_file, 'r') as f:
                    self.prediction_history = json.load(f)
            except:
                self.prediction_history = []
        
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r') as f:
                    self.action_patterns = json.load(f)
            except:
                self.action_patterns = self._default_patterns()
        else:
            self.action_patterns = self._default_patterns()
        
        if os.path.exists(self.sequences_file):
            try:
                with open(self.sequences_file, 'r') as f:
                    self.action_sequences = json.load(f)
            except:
                self.action_sequences = []
    
    def _default_patterns(self) -> Dict:
        """Default action patterns"""
        return {
            "time_based": {},
            "context_based": {},
            "sequence_based": {},
            "frequency": {}
        }
    
    def _save_all(self):
        """Save all prediction data"""
        try:
            with open(self.predictions_file, 'w') as f:
                json.dump(self.prediction_history[-500:], f, indent=2)
        except Exception as e:
            print(f"Error saving predictions: {e}")
        
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.action_patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving patterns: {e}")
        
        try:
            with open(self.sequences_file, 'w') as f:
                json.dump(self.action_sequences[-200:], f, indent=2)
        except Exception as e:
            print(f"Error saving sequences: {e}")
    
    def record_action(self, action: str, context: Optional[Dict] = None):
        """
        Record an action that was taken
        
        Args:
            action: Action that was performed
            context: Contextual information
        """
        now = datetime.now()
        hour = now.hour
        day_of_week = now.strftime("%A")
        
        time_key = f"{day_of_week}_{hour}"
        if time_key not in self.action_patterns["time_based"]:
            self.action_patterns["time_based"][time_key] = []
        self.action_patterns["time_based"][time_key].append(action)
        
        if action not in self.action_patterns["frequency"]:
            self.action_patterns["frequency"][action] = 0
        self.action_patterns["frequency"][action] += 1
        
        if context:
            context_key = context.get("activity", "general")
            if context_key not in self.action_patterns["context_based"]:
                self.action_patterns["context_based"][context_key] = []
            self.action_patterns["context_based"][context_key].append(action)
        
        if len(self.action_sequences) == 0 or len(self.action_sequences[-1]) >= 10:
            self.action_sequences.append([action])
        else:
            self.action_sequences[-1].append(action)
        
        self._save_all()
    
    def predict_next_actions(self, current_context: Optional[Dict] = None,
                            recent_actions: Optional[List[str]] = None,
                            max_predictions: int = 5) -> List[PredictedAction]:
        """
        Predict next likely actions
        
        Args:
            current_context: Current situation/context
            recent_actions: Actions taken recently
            max_predictions: Maximum number of predictions
        
        Returns:
            List of predicted actions with confidence scores
        """
        predictions = []
        
        time_based = self._predict_from_time()
        predictions.extend(time_based)
        
        if current_context:
            context_based = self._predict_from_context(current_context)
            predictions.extend(context_based)
        
        if recent_actions:
            sequence_based = self._predict_from_sequence(recent_actions)
            predictions.extend(sequence_based)
        
        frequency_based = self._predict_from_frequency()
        predictions.extend(frequency_based)
        
        predictions = self._merge_and_rank_predictions(predictions)
        
        return predictions[:max_predictions]
    
    def _predict_from_time(self) -> List[PredictedAction]:
        """Predict based on current time"""
        now = datetime.now()
        hour = now.hour
        day_of_week = now.strftime("%A")
        time_key = f"{day_of_week}_{hour}"
        
        predictions = []
        
        if time_key in self.action_patterns["time_based"]:
            actions = self.action_patterns["time_based"][time_key]
            action_counts = Counter(actions)
            
            for action, count in action_counts.most_common(3):
                confidence = count / len(actions)
                predictions.append(PredictedAction(
                    action=action,
                    confidence=confidence,
                    reasoning=f"You often do this on {day_of_week} at {hour}:00",
                    category="time_based",
                    metadata={"time_key": time_key, "frequency": count}
                ))
        
        return predictions
    
    def _predict_from_context(self, context: Dict) -> List[PredictedAction]:
        """Predict based on current context"""
        predictions = []
        
        activity = context.get("activity", "general")
        
        if activity in self.action_patterns["context_based"]:
            actions = self.action_patterns["context_based"][activity]
            action_counts = Counter(actions)
            
            for action, count in action_counts.most_common(3):
                confidence = count / len(actions)
                predictions.append(PredictedAction(
                    action=action,
                    confidence=confidence,
                    reasoning=f"Common action during {activity}",
                    category="context_based",
                    metadata={"activity": activity, "frequency": count}
                ))
        
        return predictions
    
    def _predict_from_sequence(self, recent_actions: List[str]) -> List[PredictedAction]:
        """Predict based on action sequence"""
        predictions = []
        
        if len(recent_actions) < 2:
            return predictions
        
        last_two = recent_actions[-2:]
        
        matching_sequences = []
        for sequence in self.action_sequences:
            for i in range(len(sequence) - 2):
                if sequence[i:i+2] == last_two and i+2 < len(sequence):
                    matching_sequences.append(sequence[i+2])
        
        if matching_sequences:
            sequence_counts = Counter(matching_sequences)
            
            for action, count in sequence_counts.most_common(3):
                confidence = count / len(matching_sequences)
                predictions.append(PredictedAction(
                    action=action,
                    confidence=confidence,
                    reasoning=f"Often follows your recent actions",
                    category="sequence_based",
                    metadata={"sequence": last_two, "frequency": count}
                ))
        
        return predictions
    
    def _predict_from_frequency(self) -> List[PredictedAction]:
        """Predict based on overall frequency"""
        predictions = []
        
        if not self.action_patterns["frequency"]:
            return predictions
        
        sorted_actions = sorted(
            self.action_patterns["frequency"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        total_actions = sum(count for _, count in sorted_actions)
        
        for action, count in sorted_actions[:3]:
            confidence = count / total_actions
            predictions.append(PredictedAction(
                action=action,
                confidence=confidence * 0.3,
                reasoning=f"One of your frequent actions",
                category="frequency_based",
                metadata={"total_count": count}
            ))
        
        return predictions
    
    def _merge_and_rank_predictions(self, predictions: List[PredictedAction]) -> List[PredictedAction]:
        """Merge duplicate predictions and rank by confidence"""
        action_map = {}
        
        for pred in predictions:
            if pred.action in action_map:
                existing = action_map[pred.action]
                existing.confidence = max(existing.confidence, pred.confidence)
                
                if pred.confidence > existing.confidence * 0.8:
                    existing.reasoning += f" & {pred.reasoning}"
            else:
                action_map[pred.action] = pred
        
        merged = list(action_map.values())
        merged.sort(key=lambda x: x.confidence, reverse=True)
        
        return merged
    
    def get_proactive_suggestions(self, current_context: Optional[Dict] = None) -> List[Dict]:
        """
        Get proactive suggestions for user
        
        Args:
            current_context: Current situation
        
        Returns:
            List of actionable suggestions
        """
        predictions = self.predict_next_actions(current_context=current_context, max_predictions=3)
        
        suggestions = []
        
        for pred in predictions:
            if pred.confidence >= 0.3:
                suggestion = {
                    "action": pred.action,
                    "reason": pred.reasoning,
                    "confidence": round(pred.confidence * 100),
                    "category": pred.category,
                    "emoji": self._get_suggestion_emoji(pred.category)
                }
                suggestions.append(suggestion)
        
        time_suggestions = self._get_time_based_suggestions()
        suggestions.extend(time_suggestions)
        
        return suggestions[:5]
    
    def _get_suggestion_emoji(self, category: str) -> str:
        """Get emoji for suggestion category"""
        emojis = {
            "time_based": "⏰",
            "context_based": "🎯",
            "sequence_based": "🔄",
            "frequency_based": "⭐",
            "proactive": "💡"
        }
        return emojis.get(category, "💡")
    
    def _get_time_based_suggestions(self) -> List[Dict]:
        """Get suggestions based on current time"""
        now = datetime.now()
        hour = now.hour
        
        suggestions = []
        
        if 6 <= hour < 9:
            suggestions.append({
                "action": "Start your morning routine",
                "reason": "Good morning! Time to plan your day",
                "confidence": 80,
                "category": "proactive",
                "emoji": "🌅"
            })
        elif 9 <= hour < 12:
            suggestions.append({
                "action": "Focus on important tasks",
                "reason": "Peak productivity hours",
                "confidence": 75,
                "category": "proactive",
                "emoji": "💪"
            })
        elif 12 <= hour < 14:
            suggestions.append({
                "action": "Take a break",
                "reason": "Lunch time - recharge your energy",
                "confidence": 70,
                "category": "proactive",
                "emoji": "🍽️"
            })
        elif 14 <= hour < 17:
            suggestions.append({
                "action": "Complete pending tasks",
                "reason": "Afternoon productivity window",
                "confidence": 65,
                "category": "proactive",
                "emoji": "✅"
            })
        elif 17 <= hour < 20:
            suggestions.append({
                "action": "Review your day",
                "reason": "End of workday - wrap up and plan tomorrow",
                "confidence": 75,
                "category": "proactive",
                "emoji": "📝"
            })
        elif 20 <= hour < 22:
            suggestions.append({
                "action": "Relax and unwind",
                "reason": "Evening relaxation time",
                "confidence": 70,
                "category": "proactive",
                "emoji": "🌙"
            })
        
        return suggestions
    
    def validate_prediction(self, predicted_action: str, actual_action: str):
        """
        Validate whether prediction was correct
        
        Args:
            predicted_action: What was predicted
            actual_action: What actually happened
        """
        was_correct = predicted_action.lower() == actual_action.lower()
        
        validation_entry = {
            "predicted": predicted_action,
            "actual": actual_action,
            "correct": was_correct,
            "timestamp": datetime.now().isoformat()
        }
        
        self.prediction_history.append(validation_entry)
        
        self._save_all()
        
        return was_correct
    
    def get_accuracy_metrics(self) -> Dict:
        """Get prediction accuracy metrics"""
        if not self.prediction_history:
            return {
                "total_predictions": 0,
                "accuracy": 0.0,
                "by_category": {}
            }
        
        recent = self.prediction_history[-100:]
        
        total = len(recent)
        correct = sum(1 for entry in recent if entry.get("correct", False))
        
        accuracy = correct / total if total > 0 else 0.0
        
        return {
            "total_predictions": total,
            "correct_predictions": correct,
            "accuracy": round(accuracy * 100, 1),
            "recent_sample_size": total
        }
    
    def get_statistics(self) -> Dict:
        """Get engine statistics"""
        return {
            "total_actions_recorded": sum(self.action_patterns.get("frequency", {}).values()),
            "unique_actions": len(self.action_patterns.get("frequency", {})),
            "sequences_learned": len(self.action_sequences),
            "time_patterns": len(self.action_patterns.get("time_based", {})),
            "context_patterns": len(self.action_patterns.get("context_based", {})),
            "prediction_accuracy": self.get_accuracy_metrics().get("accuracy", 0)
        }


def create_predictive_actions_engine():
    """Factory function"""
    return PredictiveActionsEngine()


if __name__ == "__main__":
    print("🔮 Predictive Actions Engine - Test Mode\n")
    
    engine = create_predictive_actions_engine()
    
    engine.record_action("open_chrome", {"activity": "browsing"})
    engine.record_action("search_google", {"activity": "browsing"})
    engine.record_action("check_email", {"activity": "communication"})
    
    predictions = engine.predict_next_actions(
        current_context={"activity": "browsing"},
        recent_actions=["open_chrome"],
        max_predictions=5
    )
    
    print(f"Predictions: {len(predictions)}")
    for pred in predictions:
        print(f"  - {pred.action} ({pred.confidence*100:.0f}%): {pred.reasoning}")
    
    suggestions = engine.get_proactive_suggestions()
    print(f"\nProactive Suggestions: {len(suggestions)}")
    for sug in suggestions:
        print(f"  {sug['emoji']} {sug['action']} ({sug['confidence']}%)")
    
    stats = engine.get_statistics()
    print(f"\nStatistics: {json.dumps(stats, indent=2)}")
