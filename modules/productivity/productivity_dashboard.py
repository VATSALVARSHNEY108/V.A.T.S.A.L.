"""
Productivity Analytics Dashboard - Comprehensive tracking and insights
Tracks time, efficiency, and patterns over weeks with beautiful visualizations
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class ProductivityDashboard:
    """Comprehensive productivity analytics and visualization"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.data_dir = self.script_dir / "productivity_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Load data from all modules
        self.activity_log_file = self.data_dir / "activity_log.json"
        self.pomodoro_history_file = self.data_dir / "pomodoro_history.json"
        self.distraction_log_file = self.data_dir / "distraction_log.json"
        self.energy_log_file = self.data_dir / "energy_levels.json"
        self.task_history_file = self.data_dir / "task_time_history.json"
    
    def get_comprehensive_dashboard(self, days=7):
        """Get complete productivity dashboard"""
        dashboard = {
            "period": f"Last {days} days",
            "generated_at": datetime.now().isoformat(),
            "overview": self._get_overview(days),
            "time_analysis": self._get_time_analysis(days),
            "productivity_metrics": self._get_productivity_metrics(days),
            "energy_patterns": self._get_energy_patterns(days),
            "distraction_analysis": self._get_distraction_analysis(days),
            "task_performance": self._get_task_performance(days),
            "recommendations": self._get_recommendations()
        }
        
        return dashboard
    
    def _get_overview(self, days):
        """Get high-level overview"""
        pomodoros = self._load_pomodoros(days)
        distractions = self._load_distractions(days)
        tasks = self._load_tasks(days)
        
        return {
            "total_work_sessions": len(pomodoros),
            "total_distractions": len(distractions),
            "total_tasks_completed": len([t for t in tasks if t.get("completed")]),
            "productivity_score": self._calculate_productivity_score(pomodoros, distractions)
        }
    
    def _get_time_analysis(self, days):
        """Analyze time usage patterns"""
        pomodoros = self._load_pomodoros(days)
        
        if not pomodoros:
            return {"no_data": True}
        
        # Daily breakdown
        daily_work = defaultdict(int)
        for pom in pomodoros:
            if pom.get("completed"):
                date = pom["timestamp"][:10]
                daily_work[date] += 25  # 25 min per pomodoro
        
        # Hour of day analysis
        hourly_productivity = defaultdict(int)
        for pom in pomodoros:
            if pom.get("completed"):
                hour = datetime.fromisoformat(pom["timestamp"]).hour
                hourly_productivity[hour] += 1
        
        best_hour = max(hourly_productivity.items(), key=lambda x: x[1])[0] if hourly_productivity else None
        
        return {
            "total_work_minutes": sum(daily_work.values()),
            "avg_work_minutes_per_day": sum(daily_work.values()) / days,
            "most_productive_hour": best_hour,
            "daily_breakdown": dict(daily_work)
        }
    
    def _get_productivity_metrics(self, days):
        """Calculate productivity metrics"""
        pomodoros = self._load_pomodoros(days)
        distractions = self._load_distractions(days)
        
        if not pomodoros:
            return {"no_data": True}
        
        completed = sum(1 for p in pomodoros if p.get("completed"))
        total = len(pomodoros)
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        # Calculate focus time vs distraction time
        focus_time = completed * 25  # minutes
        distraction_time = sum(d.get("duration", 0) / 60 for d in distractions)  # convert to minutes
        
        focus_ratio = (focus_time / (focus_time + distraction_time) * 100) if (focus_time + distraction_time) > 0 else 0
        
        return {
            "pomodoro_completion_rate": round(completion_rate, 1),
            "total_focus_minutes": focus_time,
            "total_distraction_minutes": round(distraction_time, 1),
            "focus_ratio": round(focus_ratio, 1),
            "efficiency_score": self._calculate_efficiency_score(pomodoros, distractions)
        }
    
    def _get_energy_patterns(self, days):
        """Analyze energy level patterns"""
        energy_data = self._load_energy_data(days)
        
        if not energy_data:
            return {"no_data": True}
        
        # Average energy by hour
        hourly_energy = defaultdict(list)
        for entry in energy_data:
            hour = datetime.fromisoformat(entry["timestamp"]).hour
            hourly_energy[hour].append(entry["energy_level"])
        
        hourly_avg = {
            hour: sum(levels) / len(levels)
            for hour, levels in hourly_energy.items()
        }
        
        peak_hour = max(hourly_avg.items(), key=lambda x: x[1])[0] if hourly_avg else None
        low_hour = min(hourly_avg.items(), key=lambda x: x[1])[0] if hourly_avg else None
        
        return {
            "avg_energy_level": sum(e["energy_level"] for e in energy_data) / len(energy_data),
            "peak_energy_hour": peak_hour,
            "low_energy_hour": low_hour,
            "energy_trend": self._analyze_energy_trend(energy_data)
        }
    
    def _get_distraction_analysis(self, days):
        """Analyze distraction patterns"""
        distractions = self._load_distractions(days)
        
        if not distractions:
            return {"no_data": True}
        
        # Category breakdown
        category_counts = defaultdict(int)
        category_time = defaultdict(float)
        
        for dist in distractions:
            cat = dist.get("category", "unknown")
            category_counts[cat] += 1
            category_time[cat] += dist.get("duration", 0) / 60  # minutes
        
        top_distraction = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None
        
        return {
            "total_distractions": len(distractions),
            "avg_distractions_per_day": len(distractions) / days,
            "top_distraction_category": top_distraction,
            "category_breakdown": dict(category_counts),
            "time_lost_minutes": sum(category_time.values())
        }
    
    def _get_task_performance(self, days):
        """Analyze task completion performance"""
        tasks = self._load_tasks(days)
        
        if not tasks:
            return {"no_data": True}
        
        completed = [t for t in tasks if t.get("completed")]
        
        if not completed:
            return {"no_data": True}
        
        # Calculate estimation accuracy
        accuracies = []
        for task in completed:
            estimated = task.get("estimated_minutes", 0)
            actual = task.get("actual_minutes", 0)
            if estimated > 0:
                accuracy = (1 - abs(actual - estimated) / estimated) * 100
                accuracies.append(accuracy)
        
        avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
        
        return {
            "total_tasks_completed": len(completed),
            "avg_completion_time_minutes": sum(t.get("actual_minutes", 0) for t in completed) / len(completed),
            "estimation_accuracy": round(avg_accuracy, 1),
            "fastest_task": min(t.get("actual_minutes", 0) for t in completed),
            "longest_task": max(t.get("actual_minutes", 0) for t in completed)
        }
    
    def _get_recommendations(self):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Based on dashboard data, generate actionable insights
        overview = self._get_overview(7)
        productivity = self._get_productivity_metrics(7)
        distractions = self._get_distraction_analysis(7)
        energy = self._get_energy_patterns(7)
        
        # Productivity score recommendations
        score = overview.get("productivity_score", 0)
        if score < 60:
            recommendations.append({
                "category": "productivity",
                "priority": "high",
                "message": "⚠️ Productivity score is low. Try using Focus Mode more often.",
                "action": "Enable Focus Mode for deep work sessions"
            })
        elif score < 80:
            recommendations.append({
                "category": "productivity",
                "priority": "medium",
                "message": "📈 Good productivity! Aim for 80%+ by reducing distractions.",
                "action": "Review top distractions and block during work hours"
            })
        
        # Distraction recommendations
        if not distractions.get("no_data"):
            avg_dist = distractions.get("avg_distractions_per_day", 0)
            if avg_dist > 5:
                recommendations.append({
                    "category": "distractions",
                    "priority": "high",
                    "message": f"🚨 {avg_dist:.1f} distractions/day is high. Use Focus Mode.",
                    "action": "Block top distraction category during work"
                })
        
        # Energy pattern recommendations
        if not energy.get("no_data"):
            peak_hour = energy.get("peak_energy_hour")
            if peak_hour:
                recommendations.append({
                    "category": "scheduling",
                    "priority": "medium",
                    "message": f"⚡ Your peak energy is around {peak_hour}:00. Schedule important tasks then.",
                    "action": f"Block {peak_hour}:00-{peak_hour+2}:00 for deep work"
                })
        
        return recommendations
    
    def _calculate_productivity_score(self, pomodoros, distractions):
        """Calculate overall productivity score (0-100)"""
        if not pomodoros:
            return 0
        
        completed_pomodoros = sum(1 for p in pomodoros if p.get("completed"))
        total_pomodoros = len(pomodoros)
        
        completion_rate = (completed_pomodoros / total_pomodoros) if total_pomodoros > 0 else 0
        
        # Factor in distractions
        distraction_penalty = min(len(distractions) * 2, 30)  # Max 30 point penalty
        
        score = (completion_rate * 100) - distraction_penalty
        return max(0, min(100, round(score)))
    
    def _calculate_efficiency_score(self, pomodoros, distractions):
        """Calculate efficiency score"""
        if not pomodoros:
            return 0
        
        work_time = sum(1 for p in pomodoros if p.get("completed")) * 25
        distraction_time = sum(d.get("duration", 0) / 60 for d in distractions)
        
        total_time = work_time + distraction_time
        
        if total_time == 0:
            return 0
        
        efficiency = (work_time / total_time) * 100
        return round(efficiency, 1)
    
    def _analyze_energy_trend(self, energy_data):
        """Analyze if energy is improving or declining"""
        if len(energy_data) < 10:
            return "insufficient_data"
        
        # Compare first half vs second half
        mid = len(energy_data) // 2
        first_half = [e["energy_level"] for e in energy_data[:mid]]
        second_half = [e["energy_level"] for e in energy_data[mid:]]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        if avg_second > avg_first * 1.1:
            return "improving"
        elif avg_second < avg_first * 0.9:
            return "declining"
        return "stable"
    
    def _load_pomodoros(self, days):
        """Load Pomodoro history"""
        try:
            if not self.pomodoro_history_file.exists():
                return []
            
            with open(self.pomodoro_history_file, 'r') as f:
                data = json.load(f)
            
            cutoff = datetime.now() - timedelta(days=days)
            return [p for p in data if datetime.fromisoformat(p["timestamp"]) > cutoff]
        except:
            return []
    
    def _load_distractions(self, days):
        """Load distraction log"""
        try:
            if not self.distraction_log_file.exists():
                return []
            
            with open(self.distraction_log_file, 'r') as f:
                data = json.load(f)
            
            cutoff = datetime.now() - timedelta(days=days)
            return [d for d in data if datetime.fromisoformat(d["timestamp"]) > cutoff]
        except:
            return []
    
    def _load_energy_data(self, days):
        """Load energy level data"""
        try:
            if not self.energy_log_file.exists():
                return []
            
            with open(self.energy_log_file, 'r') as f:
                data = json.load(f)
            
            cutoff = datetime.now() - timedelta(days=days)
            return [e for e in data if datetime.fromisoformat(e["timestamp"]) > cutoff]
        except:
            return []
    
    def _load_tasks(self, days):
        """Load task history"""
        try:
            if not self.task_history_file.exists():
                return []
            
            with open(self.task_history_file, 'r') as f:
                data = json.load(f)
            
            cutoff = datetime.now() - timedelta(days=days)
            return [t for t in data if datetime.fromisoformat(t["start_time"]) > cutoff]
        except:
            return []
    
    def generate_text_dashboard(self, days=7):
        """Generate a text-based dashboard for GUI display"""
        dashboard = self.get_comprehensive_dashboard(days)
        
        output = []
        output.append(f"╔{'='*58}╗")
        output.append(f"║{'PRODUCTIVITY DASHBOARD':^58}║")
        output.append(f"║{f'Last {days} Days':^58}║")
        output.append(f"╚{'='*58}╝")
        output.append("")
        
        # Overview
        overview = dashboard["overview"]
        output.append("📊 OVERVIEW")
        output.append("─" * 60)
        output.append(f"  Productivity Score: {overview['productivity_score']}%")
        output.append(f"  Work Sessions: {overview['total_work_sessions']}")
        output.append(f"  Tasks Completed: {overview['total_tasks_completed']}")
        output.append(f"  Distractions: {overview['total_distractions']}")
        output.append("")
        
        # Time Analysis
        time_analysis = dashboard["time_analysis"]
        if not time_analysis.get("no_data"):
            output.append("⏰ TIME ANALYSIS")
            output.append("─" * 60)
            output.append(f"  Total Work Time: {time_analysis['total_work_minutes']} minutes")
            output.append(f"  Daily Average: {time_analysis['avg_work_minutes_per_day']:.1f} minutes")
            if time_analysis.get("most_productive_hour"):
                output.append(f"  Most Productive Hour: {time_analysis['most_productive_hour']}:00")
            output.append("")
        
        # Productivity Metrics
        metrics = dashboard["productivity_metrics"]
        if not metrics.get("no_data"):
            output.append("📈 PRODUCTIVITY METRICS")
            output.append("─" * 60)
            output.append(f"  Completion Rate: {metrics['pomodoro_completion_rate']}%")
            output.append(f"  Focus Time: {metrics['total_focus_minutes']} min")
            output.append(f"  Distraction Time: {metrics['total_distraction_minutes']} min")
            output.append(f"  Focus Ratio: {metrics['focus_ratio']}%")
            output.append(f"  Efficiency Score: {metrics['efficiency_score']}%")
            output.append("")
        
        # Recommendations
        output.append("💡 RECOMMENDATIONS")
        output.append("─" * 60)
        for rec in dashboard["recommendations"][:3]:
            priority_icon = "🔴" if rec["priority"] == "high" else "🟡"
            output.append(f"  {priority_icon} {rec['message']}")
            output.append(f"     → {rec['action']}")
        
        return "\n".join(output)


# Singleton instance
_productivity_dashboard = None

def get_productivity_dashboard():
    """Get or create productivity dashboard instance"""
    global _productivity_dashboard
    if _productivity_dashboard is None:
        _productivity_dashboard = ProductivityDashboard()
    return _productivity_dashboard


if __name__ == "__main__":
    # Test the dashboard
    dashboard = get_productivity_dashboard()
    
    print("Testing Productivity Dashboard...")
    print("\n" + dashboard.generate_text_dashboard(7))
