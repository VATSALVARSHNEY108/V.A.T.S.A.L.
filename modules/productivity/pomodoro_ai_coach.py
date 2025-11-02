"""
Pomodoro with AI Coach - Personalized productivity coaching
Combines traditional Pomodoro with AI-powered insights and coaching
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path


class PomodoroAICoach:
    """Pomodoro timer with AI-powered productivity coaching"""
    
    def __init__(self, gemini_model=None):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.pomodoro_history_file = self.data_dir / "pomodoro_history.json"
        self.gemini = gemini_model
        
        # Pomodoro settings
        self.work_duration = 25 * 60  # 25 minutes
        self.short_break = 5 * 60  # 5 minutes
        self.long_break = 15 * 60  # 15 minutes
        self.pomodoros_until_long_break = 4
        
        # Current session
        self.is_running = False
        self.is_paused = False
        self.session_type = None  # 'work', 'short_break', 'long_break'
        self.time_remaining = 0
        self.pomodoros_completed_today = 0
        self.current_task = ""
        
        # Statistics
        self.total_pomodoros = 0
        self.total_work_time = 0
        self.completion_rate = 0.0
    
    def start_pomodoro(self, task_name="Focused Work"):
        """Start a new Pomodoro session"""
        if self.is_running:
            return {"success": False, "message": "Pomodoro already running"}
        
        self.is_running = True
        self.is_paused = False
        self.session_type = "work"
        self.time_remaining = self.work_duration
        self.current_task = task_name
        
        # Start timer thread
        timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        timer_thread.start()
        
        # Get AI coaching message
        ai_message = self._get_ai_start_message()
        
        return {
            "success": True,
            "message": f"🍅 Pomodoro started for '{task_name}'",
            "duration": self.work_duration / 60,
            "ai_coach": ai_message,
            "session_type": "work"
        }
    
    def start_break(self, is_long=False):
        """Start a break session"""
        if self.is_running:
            return {"success": False, "message": "Session already running"}
        
        self.is_running = True
        self.is_paused = False
        self.session_type = "long_break" if is_long else "short_break"
        self.time_remaining = self.long_break if is_long else self.short_break
        
        # Start timer thread
        timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        timer_thread.start()
        
        break_type = "long" if is_long else "short"
        ai_message = self._get_ai_break_message(break_type)
        
        return {
            "success": True,
            "message": f"☕ {break_type.title()} break started",
            "duration": self.time_remaining / 60,
            "ai_coach": ai_message,
            "session_type": self.session_type
        }
    
    def pause_session(self):
        """Pause current session"""
        if not self.is_running:
            return {"success": False, "message": "No active session"}
        
        self.is_paused = not self.is_paused
        status = "paused" if self.is_paused else "resumed"
        
        return {
            "success": True,
            "message": f"Session {status}",
            "time_remaining": self.time_remaining
        }
    
    def stop_session(self, completed=True):
        """Stop current session"""
        if not self.is_running:
            return {"success": False, "message": "No active session"}
        
        self.is_running = False
        self.is_paused = False
        
        # Log the session
        self._log_session(completed)
        
        if completed and self.session_type == "work":
            self.pomodoros_completed_today += 1
            self.total_pomodoros += 1
            
            # Get AI feedback
            ai_feedback = self._get_ai_completion_message()
            
            return {
                "success": True,
                "message": "🎉 Pomodoro completed!",
                "pomodoros_today": self.pomodoros_completed_today,
                "ai_coach": ai_feedback,
                "next_action": self._get_next_action()
            }
        
        return {
            "success": True,
            "message": "Session stopped",
            "completed": completed
        }
    
    def _timer_loop(self):
        """Main timer loop"""
        while self.is_running and self.time_remaining > 0:
            if not self.is_paused:
                time.sleep(1)
                self.time_remaining -= 1
                
                # Send periodic AI encouragement
                if self.session_type == "work":
                    if self.time_remaining in [600, 300]:  # 10 min, 5 min marks
                        # Could trigger an encouragement notification here
                        pass
        
        if self.is_running and self.time_remaining <= 0:
            # Session completed
            self.stop_session(completed=True)
    
    def get_status(self):
        """Get current Pomodoro status"""
        minutes_remaining = self.time_remaining // 60
        seconds_remaining = self.time_remaining % 60
        
        return {
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "session_type": self.session_type,
            "time_remaining_seconds": self.time_remaining,
            "time_remaining_formatted": f"{minutes_remaining:02d}:{seconds_remaining:02d}",
            "current_task": self.current_task,
            "pomodoros_today": self.pomodoros_completed_today,
            "next_break_type": self._get_next_action()
        }
    
    def _get_next_action(self):
        """Determine next recommended action"""
        if self.pomodoros_completed_today % self.pomodoros_until_long_break == 0:
            return "long_break"
        return "short_break"
    
    def _get_ai_start_message(self):
        """Get AI coaching message for starting work"""
        if not self.gemini:
            return "🚀 Let's crush this Pomodoro! Stay focused for 25 minutes."
        
        try:
            prompt = f"""
            User is starting a Pomodoro work session for task: "{self.current_task}".
            They've completed {self.pomodoros_completed_today} Pomodoros today.
            
            Give them a SHORT (1-2 sentences), motivating message to start strong.
            Be energetic and encouraging.
            """
            
            response = self.gemini.generate_content(prompt)
            return response.text.strip()
        except:
            return "🚀 Let's crush this Pomodoro! Stay focused for 25 minutes."
    
    def _get_ai_break_message(self, break_type):
        """Get AI coaching message for break"""
        if not self.gemini:
            messages = {
                "short": "☕ Take 5 minutes to recharge. Stretch, hydrate, relax!",
                "long": "🌟 Great work! Take 15 minutes for a proper break. You've earned it!"
            }
            return messages.get(break_type, "Take a break!")
        
        try:
            prompt = f"""
            User is taking a {break_type} break after completing a Pomodoro.
            Suggest a SHORT (1-2 sentences) activity for their break.
            Be specific and helpful.
            """
            
            response = self.gemini.generate_content(prompt)
            return response.text.strip()
        except:
            return "☕ Perfect time to stretch and recharge!"
    
    def _get_ai_completion_message(self):
        """Get AI feedback after completing Pomodoro"""
        if not self.gemini:
            return "🎉 Excellent work! You completed the Pomodoro!"
        
        try:
            prompt = f"""
            User just completed a 25-minute Pomodoro session.
            This is their {self.pomodoros_completed_today}th Pomodoro today.
            
            Give them SHORT (1-2 sentences) positive reinforcement.
            Be celebratory but brief.
            """
            
            response = self.gemini.generate_content(prompt)
            return response.text.strip()
        except:
            return "🎉 Excellent work! You're on a roll!"
    
    def get_ai_productivity_insight(self):
        """Get AI insight about productivity patterns"""
        if not self.gemini:
            return "Complete more Pomodoros to get AI insights!"
        
        history = self.get_pomodoro_history(days=7)
        if not history["success"]:
            return "Not enough data for insights yet."
        
        try:
            stats = history
            prompt = f"""
            User's Pomodoro statistics for the last 7 days:
            - Total Pomodoros: {stats.get('total_pomodoros', 0)}
            - Completion rate: {stats.get('completion_rate', 0):.1f}%
            - Best day: {stats.get('best_day', 'Unknown')}
            - Average per day: {stats.get('avg_per_day', 0):.1f}
            
            Provide 2-3 SHORT, actionable tips to improve their productivity.
            Be specific and encouraging.
            """
            
            response = self.gemini.generate_content(prompt)
            return response.text.strip()
        except:
            return "Keep up the great work with Pomodoros!"
    
    def _log_session(self, completed):
        """Log completed Pomodoro session"""
        try:
            # Load existing history
            history = []
            if self.pomodoro_history_file.exists():
                with open(self.pomodoro_history_file, 'r') as f:
                    history = json.load(f)
            
            # Add new session
            session = {
                "timestamp": datetime.now().isoformat(),
                "type": self.session_type,
                "task": self.current_task,
                "completed": completed,
                "duration_minutes": (self.work_duration - self.time_remaining) / 60 if self.session_type == "work" else 0
            }
            
            history.append(session)
            
            # Keep last 1000 sessions
            history = history[-1000:]
            
            with open(self.pomodoro_history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
        except Exception as e:
            print(f"Error logging session: {e}")
    
    def get_pomodoro_history(self, days=7):
        """Get Pomodoro history and statistics"""
        try:
            if not self.pomodoro_history_file.exists():
                return {"success": False, "message": "No history yet"}
            
            with open(self.pomodoro_history_file, 'r') as f:
                history = json.load(f)
            
            # Filter recent sessions
            cutoff = datetime.now() - timedelta(days=days)
            recent = [
                s for s in history
                if datetime.fromisoformat(s["timestamp"]) > cutoff and s["type"] == "work"
            ]
            
            total = len(recent)
            completed = sum(1 for s in recent if s["completed"])
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            # Daily breakdown
            daily = {}
            for session in recent:
                date = session["timestamp"][:10]
                if date not in daily:
                    daily[date] = 0
                if session["completed"]:
                    daily[date] += 1
            
            best_day = max(daily.items(), key=lambda x: x[1])[0] if daily else "N/A"
            
            return {
                "success": True,
                "days": days,
                "total_pomodoros": total,
                "completed_pomodoros": completed,
                "completion_rate": completion_rate,
                "avg_per_day": total / days,
                "daily_breakdown": daily,
                "best_day": best_day
            }
            
        except Exception as e:
            return {"success": False, "message": str(e)}


# Singleton instance
_pomodoro_coach = None

def get_pomodoro_coach(gemini_model=None):
    """Get or create Pomodoro coach instance"""
    global _pomodoro_coach
    if _pomodoro_coach is None:
        _pomodoro_coach = PomodoroAICoach(gemini_model)
    return _pomodoro_coach


if __name__ == "__main__":
    # Test the Pomodoro coach
    coach = get_pomodoro_coach()
    
    print("Testing Pomodoro AI Coach...")
    result = coach.start_pomodoro("Write code")
    print(f"\nStart: {json.dumps(result, indent=2)}")
    
    time.sleep(3)
    
    status = coach.get_status()
    print(f"\nStatus: {json.dumps(status, indent=2)}")
    
    stop_result = coach.stop_session(completed=False)
    print(f"\nStop: {json.dumps(stop_result, indent=2)}")
