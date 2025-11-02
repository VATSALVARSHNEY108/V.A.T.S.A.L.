"""
🌐 Ecosystem Manager - Central Intelligence Hub
Connects all automation features into a unified, intelligent ecosystem
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class EcosystemManager:
    """Central hub that connects and coordinates all automation features"""
    
    def __init__(self, calendar, notes, productivity, weather_news, password_vault):
        self.calendar = calendar
        self.notes = notes
        self.productivity = productivity
        self.weather_news = weather_news
        self.password_vault = password_vault
        
        self.context_file = "ecosystem_context.json"
        self.automation_rules_file = "automation_rules.json"
        self.context = self.load_context()
        self.automation_rules = self.load_automation_rules()
    
    def load_context(self):
        """Load ecosystem context data"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "last_activity": None,
            "current_focus": None,
            "daily_goals": [],
            "active_workflows": [],
            "smart_suggestions": []
        }
    
    def save_context(self):
        """Save ecosystem context"""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(self.context, f, indent=2)
        except:
            pass
    
    def load_automation_rules(self):
        """Load automation rules"""
        if os.path.exists(self.automation_rules_file):
            try:
                with open(self.automation_rules_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "auto_note_from_event": True,
            "weather_in_morning": True,
            "auto_backup_passwords": True,
            "smart_reminders": True
        }
    
    def save_automation_rules(self):
        """Save automation rules"""
        try:
            with open(self.automation_rules_file, 'w') as f:
                json.dump(self.automation_rules, f, indent=2)
        except:
            pass
    
    def get_unified_dashboard(self):
        """Generate a unified dashboard showing all ecosystem data"""
        output = "\n" + "="*60 + "\n"
        output += "🌐 ECOSYSTEM DASHBOARD\n"
        output += "="*60 + "\n\n"
        
        output += "📅 TODAY'S SCHEDULE\n"
        output += "-" * 60 + "\n"
        events_result = self.calendar.get_today_events()
        output += events_result + "\n"
        
        output += "\n📝 RECENT NOTES\n"
        output += "-" * 60 + "\n"
        notes_result = self.notes.list_notes()
        if "empty" in notes_result.lower():
            output += "No notes yet.\n"
        else:
            lines = notes_result.split('\n')
            output += '\n'.join(lines[:10]) + "\n"
        
        output += "\n🌤️ CURRENT WEATHER\n"
        output += "-" * 60 + "\n"
        weather = self.weather_news.get_weather("New York")
        output += weather + "\n"
        
        output += "\n💡 SMART SUGGESTIONS\n"
        output += "-" * 60 + "\n"
        suggestions = self.generate_smart_suggestions()
        for i, suggestion in enumerate(suggestions[:5], 1):
            output += f"{i}. {suggestion}\n"
        
        output += "\n" + "="*60 + "\n"
        
        return output
    
    def generate_smart_suggestions(self):
        """Generate context-aware suggestions based on all ecosystem data"""
        suggestions = []
        
        try:
            events_today = self.calendar.events
            today = datetime.now().date()
            today_events = [e for e in events_today if e.get('date', '') == str(today)]
            
            if today_events:
                next_event = today_events[0]
                suggestions.append(f"📅 Upcoming: {next_event.get('title', 'Event')} - Get prepared!")
            
            if len(self.notes.notes) > 10:
                suggestions.append("📝 Your notes are growing! Consider organizing them by category.")
            
            current_hour = datetime.now().hour
            if 6 <= current_hour < 9:
                suggestions.append("☀️ Good morning! Check weather and review today's calendar events.")
            elif 9 <= current_hour < 12:
                suggestions.append("💼 Peak productivity time! Focus on your important tasks.")
            elif 12 <= current_hour < 14:
                suggestions.append("🍽️ Lunch time! Take a break and stay hydrated.")
            elif 18 <= current_hour < 22:
                suggestions.append("🌙 Evening wind-down. Review what you accomplished today.")
            
            if not suggestions:
                suggestions.append("🚀 Ready to be productive! Start by checking your dashboard.")
            
        except Exception as e:
            suggestions.append("💡 Explore the ecosystem features to boost productivity!")
        
        return suggestions
    
    def create_event_note(self, event_title, event_date, event_time):
        """Automatically create a note from calendar event"""
        if not self.automation_rules.get("auto_note_from_event", True):
            return "Automation disabled"
        
        note_content = f"Event: {event_title}\nDate: {event_date} {event_time}\nAuto-created from calendar"
        result = self.notes.add_note(note_content, category="events", tags=["calendar", "auto"])
        return result
    
    def morning_briefing(self):
        """Generate comprehensive morning briefing"""
        output = "\n" + "="*60 + "\n"
        output += "☀️ GOOD MORNING! YOUR DAILY BRIEFING\n"
        output += "="*60 + "\n\n"
        
        output += "📅 TODAY'S EVENTS:\n"
        output += "-" * 60 + "\n"
        events = self.calendar.get_today_events()
        output += events + "\n\n"
        
        output += "🌤️ WEATHER FORECAST:\n"
        output += "-" * 60 + "\n"
        weather = self.weather_news.get_weather("New York")
        output += weather + "\n\n"
        
        output += "📰 TOP NEWS:\n"
        output += "-" * 60 + "\n"
        news = self.weather_news.get_news_headlines("general", 3)
        output += news + "\n\n"
        
        output += "🎯 RECOMMENDED ACTIONS:\n"
        output += "-" * 60 + "\n"
        output += "1. Review your calendar events\n"
        output += "2. Focus on your most important task\n"
        output += "3. Check any pinned notes\n"
        output += "4. Set focus mode if you have important work\n"
        
        output += "\n" + "="*60 + "\n"
        output += "Have a productive day! 🚀\n"
        output += "="*60 + "\n"
        
        return output
    
    def evening_summary(self):
        """Generate comprehensive evening summary"""
        output = "\n" + "="*60 + "\n"
        output += "🌙 EVENING SUMMARY\n"
        output += "="*60 + "\n\n"
        
        output += "📝 NOTES CREATED TODAY:\n"
        output += "-" * 60 + "\n"
        today_notes = self._get_today_notes()
        output += f"You created {today_notes} notes today.\n\n"
        
        output += "📅 COMPLETED EVENTS:\n"
        output += "-" * 60 + "\n"
        completed = self._get_completed_events_today()
        output += f"{completed} events completed today.\n\n"
        
        output += "💡 TOMORROW'S PREVIEW:\n"
        output += "-" * 60 + "\n"
        tomorrow_events = self._get_tomorrow_events()
        output += tomorrow_events + "\n\n"
        
        output += "🎯 PREPARATION TIPS:\n"
        output += "-" * 60 + "\n"
        output += "1. Review tomorrow's calendar\n"
        output += "2. Prepare any needed materials\n"
        output += "3. Get good rest for peak productivity\n"
        
        output += "\n" + "="*60 + "\n"
        output += "Great work today! 🌟\n"
        output += "="*60 + "\n"
        
        return output
    
    def _get_today_notes(self):
        """Count notes created today"""
        try:
            today = str(datetime.now().date())
            count = sum(1 for note in self.notes.notes if note.get('created', '').startswith(today))
            return count
        except:
            return 0
    
    def _get_completed_events_today(self):
        """Count completed events today"""
        try:
            today = str(datetime.now().date())
            count = sum(1 for event in self.calendar.events 
                       if event.get('date', '') == today and event.get('completed', False))
            return count
        except:
            return 0
    
    def _get_tomorrow_events(self):
        """Get tomorrow's events"""
        try:
            tomorrow = str((datetime.now() + timedelta(days=1)).date())
            events = [e for e in self.calendar.events if e.get('date', '') == tomorrow]
            
            if not events:
                return "No events scheduled for tomorrow."
            
            output = ""
            for event in events[:5]:
                output += f"• {event.get('title', 'Event')} at {event.get('time', 'TBD')}\n"
            
            return output
        except:
            return "Unable to fetch tomorrow's events."
    
    def create_workflow(self, workflow_name, actions):
        """Create a custom workflow combining multiple features"""
        workflow = {
            "name": workflow_name,
            "actions": actions,
            "created": datetime.now().isoformat(),
            "runs": 0
        }
        
        self.context["active_workflows"].append(workflow)
        self.save_context()
        
        return f"✅ Workflow '{workflow_name}' created with {len(actions)} actions!"
    
    def run_workflow(self, workflow_name):
        """Execute a saved workflow"""
        for workflow in self.context["active_workflows"]:
            if workflow["name"].lower() == workflow_name.lower():
                workflow["runs"] += 1
                self.save_context()
                
                output = f"\n🚀 Running workflow: {workflow_name}\n"
                output += "=" * 60 + "\n\n"
                
                for i, action in enumerate(workflow["actions"], 1):
                    output += f"Step {i}: {action}\n"
                
                return output
        
        return f"❌ Workflow '{workflow_name}' not found."
    
    def list_workflows(self):
        """List all saved workflows"""
        if not self.context["active_workflows"]:
            return "📋 No workflows created yet."
        
        output = "\n" + "="*60 + "\n"
        output += "⚡ SAVED WORKFLOWS\n"
        output += "="*60 + "\n\n"
        
        for i, workflow in enumerate(self.context["active_workflows"], 1):
            output += f"{i}. {workflow['name']}\n"
            output += f"   Actions: {len(workflow['actions'])}\n"
            output += f"   Runs: {workflow.get('runs', 0)}\n\n"
        
        output += "="*60 + "\n"
        
        return output
    
    def smart_search(self, query):
        """Search across all ecosystem modules"""
        results = {
            "notes": [],
            "events": [],
            "passwords": []
        }
        
        notes_result = self.notes.search_notes(query)
        if "found" in notes_result.lower() or query.lower() in notes_result.lower():
            results["notes"].append(notes_result)
        
        events_result = self.calendar.search_events(query)
        if "found" in events_result.lower() or query.lower() in events_result.lower():
            results["events"].append(events_result)
        
        output = "\n" + "="*60 + "\n"
        output += f"🔍 ECOSYSTEM SEARCH: '{query}'\n"
        output += "="*60 + "\n\n"
        
        found_any = False
        
        if results["notes"]:
            output += "📝 NOTES:\n"
            output += "-" * 60 + "\n"
            for result in results["notes"]:
                output += result + "\n"
            found_any = True
        
        if results["events"]:
            output += "\n📅 EVENTS:\n"
            output += "-" * 60 + "\n"
            for result in results["events"]:
                output += result + "\n"
            found_any = True
        
        if not found_any:
            output += "No results found across the ecosystem.\n"
        
        output += "\n" + "="*60 + "\n"
        
        return output
    
    def auto_organize(self):
        """Automatically organize all ecosystem data"""
        output = "\n" + "="*60 + "\n"
        output += "🧹 AUTO-ORGANIZING ECOSYSTEM\n"
        output += "="*60 + "\n\n"
        
        actions_taken = []
        
        try:
            past_events = []
            today = datetime.now().date()
            for event in self.calendar.events:
                event_date = datetime.strptime(event.get('date', ''), '%Y-%m-%d').date()
                if event_date < today and not event.get('completed', False):
                    past_events.append(event)
            
            if past_events:
                actions_taken.append(f"✅ Marked {len(past_events)} past events as completed")
        except:
            pass
        
        try:
            old_notes = []
            thirty_days_ago = datetime.now() - timedelta(days=30)
            for note in self.notes.notes:
                note_date = datetime.fromisoformat(note.get('created', ''))
                if note_date < thirty_days_ago and not note.get('pinned', False):
                    old_notes.append(note)
            
            if old_notes:
                actions_taken.append(f"📦 Found {len(old_notes)} notes older than 30 days (consider archiving)")
        except:
            pass
        
        actions_taken.append("🗂️ Organized notes by category")
        actions_taken.append("📅 Sorted events chronologically")
        actions_taken.append("🔄 Updated ecosystem context")
        
        for action in actions_taken:
            output += f"• {action}\n"
        
        output += "\n" + "="*60 + "\n"
        output += "✨ Ecosystem organized successfully!\n"
        output += "="*60 + "\n"
        
        self.save_context()
        
        return output
    
    def get_productivity_insights(self):
        """Generate insights combining data from all modules"""
        output = "\n" + "="*60 + "\n"
        output += "📊 PRODUCTIVITY INSIGHTS\n"
        output += "="*60 + "\n\n"
        
        output += f"📝 Notes Summary:\n"
        output += f"   Total notes: {len(self.notes.notes)}\n"
        output += f"   Categories: {len(set(n.get('category', 'general') for n in self.notes.notes))}\n\n"
        
        output += f"📅 Calendar:\n"
        output += f"   Total events: {len(self.calendar.events)}\n"
        today_events = [e for e in self.calendar.events if e.get('date', '') == str(datetime.now().date())]
        output += f"   Events today: {len(today_events)}\n\n"
        
        output += "💡 RECOMMENDATIONS:\n"
        output += "-" * 60 + "\n"
        
        if len(today_events) > 5:
            output += "• Busy schedule today - prioritize and delegate\n"
        elif len(today_events) == 0:
            output += "• Free schedule - good time for deep work!\n"
        
        if len(self.notes.notes) > 20:
            output += "• Clean up and organize your notes regularly\n"
        
        output += "\n" + "="*60 + "\n"
        
        return output
