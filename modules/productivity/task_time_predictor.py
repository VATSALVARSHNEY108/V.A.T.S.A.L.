"""
Task Time Predictor - Predicts task durations based on history
Uses machine learning-like patterns to improve estimates over time
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class TaskTimePredictor:
    """Predicts task completion time based on historical data"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.task_history_file = self.data_dir / "task_time_history.json"
        self.load_history()
        
        # Task categories with default estimates (minutes)
        self.default_estimates = {
            "coding": 60,
            "meeting": 30,
            "email": 15,
            "documentation": 45,
            "research": 90,
            "debugging": 75,
            "design": 120,
            "testing": 45,
            "learning": 60,
            "planning": 30
        }
    
    def load_history(self):
        """Load task history from file"""
        if self.task_history_file.exists():
            with open(self.task_history_file, 'r') as f:
                self.task_history = json.load(f)
        else:
            self.task_history = []
    
    def save_history(self):
        """Save task history to file"""
        with open(self.task_history_file, 'w') as f:
            json.dump(self.task_history, f, indent=2)
    
    def start_task(self, task_name, task_category="general", estimated_minutes=None):
        """Start tracking a new task"""
        task = {
            "id": len(self.task_history) + 1,
            "name": task_name,
            "category": task_category.lower(),
            "estimated_minutes": estimated_minutes or self.default_estimates.get(task_category.lower(), 60),
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "actual_minutes": None,
            "completed": False,
            "interruptions": 0
        }
        
        self.task_history.append(task)
        self.save_history()
        
        # Get prediction based on similar tasks
        prediction = self.predict_task_duration(task_name, task_category)
        
        return {
            "success": True,
            "task_id": task["id"],
            "task_name": task_name,
            "estimated_minutes": task["estimated_minutes"],
            "predicted_minutes": prediction["predicted_minutes"],
            "confidence": prediction["confidence"],
            "similar_tasks": prediction["similar_tasks_count"]
        }
    
    def complete_task(self, task_id):
        """Mark task as complete and record actual time"""
        task = next((t for t in self.task_history if t["id"] == task_id and not t["completed"]), None)
        
        if not task:
            return {"success": False, "message": "Task not found or already completed"}
        
        task["end_time"] = datetime.now().isoformat()
        task["completed"] = True
        
        # Calculate actual duration
        start = datetime.fromisoformat(task["start_time"])
        end = datetime.fromisoformat(task["end_time"])
        actual_minutes = (end - start).total_seconds() / 60
        task["actual_minutes"] = actual_minutes
        
        self.save_history()
        
        # Calculate accuracy
        estimated = task["estimated_minutes"]
        accuracy = (1 - abs(actual_minutes - estimated) / estimated) * 100 if estimated > 0 else 0
        
        return {
            "success": True,
            "task_name": task["name"],
            "estimated_minutes": estimated,
            "actual_minutes": actual_minutes,
            "difference_minutes": actual_minutes - estimated,
            "accuracy_percentage": accuracy,
            "feedback": self._get_accuracy_feedback(accuracy)
        }
    
    def predict_task_duration(self, task_name, task_category="general"):
        """Predict how long a task will take based on history"""
        # Find similar completed tasks
        similar_tasks = self._find_similar_tasks(task_name, task_category)
        
        if not similar_tasks:
            # No history, use default estimate
            default = self.default_estimates.get(task_category.lower(), 60)
            return {
                "predicted_minutes": default,
                "confidence": "low",
                "similar_tasks_count": 0,
                "method": "default_estimate"
            }
        
        # Calculate average duration of similar tasks
        avg_duration = sum(t["actual_minutes"] for t in similar_tasks) / len(similar_tasks)
        
        # Calculate standard deviation for confidence
        variance = sum((t["actual_minutes"] - avg_duration) ** 2 for t in similar_tasks) / len(similar_tasks)
        std_dev = variance ** 0.5
        
        # Determine confidence level
        if len(similar_tasks) >= 5 and std_dev < avg_duration * 0.3:
            confidence = "high"
        elif len(similar_tasks) >= 2:
            confidence = "medium"
        else:
            confidence = "low"
        
        return {
            "predicted_minutes": round(avg_duration, 1),
            "confidence": confidence,
            "similar_tasks_count": len(similar_tasks),
            "std_deviation": round(std_dev, 1),
            "range_min": round(avg_duration - std_dev, 1),
            "range_max": round(avg_duration + std_dev, 1),
            "method": "historical_average"
        }
    
    def _find_similar_tasks(self, task_name, task_category):
        """Find similar completed tasks"""
        completed_tasks = [t for t in self.task_history if t["completed"]]
        
        similar = []
        task_name_lower = task_name.lower()
        
        for task in completed_tasks:
            # Check category match
            if task["category"] == task_category.lower():
                # Check name similarity
                task_lower = task["name"].lower()
                
                # Simple similarity check (contains common words)
                task_words = set(task_lower.split())
                name_words = set(task_name_lower.split())
                common_words = task_words & name_words
                
                if common_words or task["category"] == task_category.lower():
                    similar.append(task)
        
        return similar[-10:]  # Use last 10 similar tasks
    
    def _get_accuracy_feedback(self, accuracy):
        """Get feedback message based on estimation accuracy"""
        if accuracy >= 90:
            return "🎯 Excellent estimate! Nearly perfect."
        elif accuracy >= 75:
            return "👍 Good estimate! Minor variance."
        elif accuracy >= 50:
            return "📊 Moderate accuracy. Review complexity next time."
        else:
            return "⚠️ Significant difference. Consider task breakdown."
    
    def get_category_stats(self, category):
        """Get statistics for a task category"""
        category_tasks = [
            t for t in self.task_history
            if t["completed"] and t["category"] == category.lower()
        ]
        
        if not category_tasks:
            return {"success": False, "message": f"No completed tasks in category '{category}'"}
        
        actual_times = [t["actual_minutes"] for t in category_tasks]
        estimated_times = [t["estimated_minutes"] for t in category_tasks]
        
        avg_actual = sum(actual_times) / len(actual_times)
        avg_estimated = sum(estimated_times) / len(estimated_times)
        
        # Calculate overall estimation bias
        bias = avg_actual - avg_estimated
        
        return {
            "success": True,
            "category": category,
            "total_tasks": len(category_tasks),
            "avg_actual_minutes": round(avg_actual, 1),
            "avg_estimated_minutes": round(avg_estimated, 1),
            "estimation_bias": round(bias, 1),
            "bias_type": "underestimate" if bias > 0 else "overestimate",
            "fastest_task": round(min(actual_times), 1),
            "slowest_task": round(max(actual_times), 1)
        }
    
    def get_personal_productivity_insights(self):
        """Get insights about personal task completion patterns"""
        completed = [t for t in self.task_history if t["completed"]]
        
        if len(completed) < 5:
            return {"success": False, "message": "Need at least 5 completed tasks for insights"}
        
        # Calculate overall accuracy
        accuracies = []
        for task in completed:
            if task["estimated_minutes"] > 0:
                accuracy = (1 - abs(task["actual_minutes"] - task["estimated_minutes"]) / task["estimated_minutes"]) * 100
                accuracies.append(accuracy)
        
        avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
        
        # Find best and worst categories
        category_performance = defaultdict(list)
        for task in completed:
            if task["estimated_minutes"] > 0:
                accuracy = (1 - abs(task["actual_minutes"] - task["estimated_minutes"]) / task["estimated_minutes"]) * 100
                category_performance[task["category"]].append(accuracy)
        
        category_avg = {
            cat: sum(accs) / len(accs)
            for cat, accs in category_performance.items()
            if accs
        }
        
        best_category = max(category_avg.items(), key=lambda x: x[1])[0] if category_avg else "N/A"
        worst_category = min(category_avg.items(), key=lambda x: x[1])[0] if category_avg else "N/A"
        
        return {
            "success": True,
            "total_completed_tasks": len(completed),
            "overall_accuracy": round(avg_accuracy, 1),
            "estimation_skill": "excellent" if avg_accuracy >= 80 else "good" if avg_accuracy >= 60 else "needs improvement",
            "best_category": best_category,
            "worst_category": worst_category,
            "category_stats": category_avg,
            "recommendation": self._get_improvement_recommendation(avg_accuracy, category_avg)
        }
    
    def _get_improvement_recommendation(self, avg_accuracy, category_avg):
        """Get personalized recommendation for improving estimates"""
        if avg_accuracy >= 80:
            return "🏆 Excellent estimation skills! Keep tracking to maintain accuracy."
        elif avg_accuracy >= 60:
            worst = min(category_avg.items(), key=lambda x: x[1])[0] if category_avg else None
            if worst:
                return f"💡 Focus on improving estimates for '{worst}' tasks. Break them into smaller subtasks."
            return "📊 Good accuracy overall. Review underestimated tasks to identify patterns."
        else:
            return "⚠️ Consider: 1) Breaking tasks into smaller pieces, 2) Adding buffer time, 3) Tracking interruptions"


# Singleton instance
_task_predictor = None

def get_task_predictor():
    """Get or create task predictor instance"""
    global _task_predictor
    if _task_predictor is None:
        _task_predictor = TaskTimePredictor()
    return _task_predictor


if __name__ == "__main__":
    # Test the predictor
    predictor = get_task_predictor()
    
    print("Testing Task Time Predictor...")
    
    # Start a task
    result = predictor.start_task("Write Python function", "coding", 30)
    print(f"\nTask started: {json.dumps(result, indent=2)}")
    
    # Simulate completion
    import time
    time.sleep(2)
    
    complete_result = predictor.complete_task(result["task_id"])
    print(f"\nTask completed: {json.dumps(complete_result, indent=2)}")
    
    # Get insights
    insights = predictor.get_personal_productivity_insights()
    print(f"\nInsights: {json.dumps(insights, indent=2)}")
