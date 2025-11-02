"""
Calendar Manager Module
Manage events, reminders, and appointments
"""

import json
import os
from datetime import datetime, timedelta

class CalendarManager:
    def __init__(self):
        self.events_file = "calendar_events.json"
        self.load_events()
    
    def load_events(self):
        """Load events from file"""
        try:
            if os.path.exists(self.events_file):
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    self.events = json.load(f)
            else:
                self.events = []
        except Exception:
            self.events = []
    
    def save_events(self):
        """Save events to file"""
        try:
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def add_event(self, title, date, time="", duration=60, description="", reminder=False):
        """Add a new event"""
        try:
            event_datetime = self._parse_datetime(date, time)
            
            event = {
                'id': len(self.events) + 1,
                'title': title,
                'date': event_datetime.strftime("%Y-%m-%d"),
                'time': event_datetime.strftime("%H:%M") if time else "",
                'duration': duration,
                'description': description,
                'reminder': reminder,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'completed': False
            }
            
            self.events.append(event)
            self.save_events()
            
            output = f"\n{'='*50}\n"
            output += f"📅 EVENT CREATED\n"
            output += f"{'='*50}\n\n"
            output += f"✅ {title}\n"
            output += f"📆 {event['date']}"
            
            if event['time']:
                output += f" at {event['time']}\n"
            else:
                output += "\n"
            
            output += f"⏱️  Duration: {duration} minutes\n"
            output += f"{'='*50}\n"
            
            return output
            
        except Exception as e:
            return f"Error creating event: {str(e)}"
    
    def get_event(self, event_id):
        """Get a specific event by ID"""
        for event in self.events:
            if event['id'] == event_id:
                return self._format_event(event)
        
        return f"⚠️ Event #{event_id} not found."
    
    def update_event(self, event_id, title=None, date=None, time=None, description=None):
        """Update an existing event"""
        for event in self.events:
            if event['id'] == event_id:
                if title:
                    event['title'] = title
                if date:
                    event_datetime = self._parse_datetime(date, time or event['time'])
                    event['date'] = event_datetime.strftime("%Y-%m-%d")
                if time is not None:
                    if time:
                        event['time'] = time
                    else:
                        event['time'] = ""
                if description:
                    event['description'] = description
                
                self.save_events()
                
                return f"✅ Event #{event_id} has been updated!"
        
        return f"⚠️ Event #{event_id} not found."
    
    def delete_event(self, event_id):
        """Delete an event"""
        for i, event in enumerate(self.events):
            if event['id'] == event_id:
                del self.events[i]
                self.save_events()
                
                return f"🗑️ Event #{event_id} has been deleted!"
        
        return f"⚠️ Event #{event_id} not found."
    
    def list_events(self, days=7):
        """List upcoming events for the next N days"""
        if not self.events:
            return "📭 No events found. Create your first event!"
        
        today = datetime.now().date()
        future_date = today + timedelta(days=days)
        
        upcoming = []
        
        for event in self.events:
            if not event.get('completed', False):
                event_date = datetime.strptime(event['date'], "%Y-%m-%d").date()
                
                if today <= event_date <= future_date:
                    upcoming.append(event)
        
        if not upcoming:
            return f"📭 No upcoming events in the next {days} days."
        
        upcoming.sort(key=lambda x: (x['date'], x['time']))
        
        output = f"\n{'='*50}\n"
        output += f"📅 UPCOMING EVENTS ({days} DAYS)\n"
        output += f"{'='*50}\n\n"
        
        for event in upcoming:
            event_date = datetime.strptime(event['date'], "%Y-%m-%d").date()
            days_until = (event_date - today).days
            
            if days_until == 0:
                date_text = "Today"
            elif days_until == 1:
                date_text = "Tomorrow"
            else:
                date_text = f"In {days_until} days"
            
            output += f"#{event['id']} - {event['title']}\n"
            output += f"   📆 {event['date']} ({date_text})"
            
            if event['time']:
                output += f" at {event['time']}\n"
            else:
                output += "\n"
            
            if event.get('description'):
                desc_preview = event['description'][:50] + "..." if len(event['description']) > 50 else event['description']
                output += f"   📝 {desc_preview}\n"
            
            output += "\n"
        
        output += f"{'='*50}\n"
        output += f"Total Events: {len(upcoming)}\n"
        output += f"{'='*50}\n"
        
        return output
    
    def get_today_events(self):
        """Get events for today"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        today_events = [e for e in self.events if e['date'] == today and not e.get('completed', False)]
        
        if not today_events:
            return "📭 No events scheduled for today."
        
        today_events.sort(key=lambda x: x['time'])
        
        output = f"\n{'='*50}\n"
        output += f"📅 TODAY'S EVENTS\n"
        output += f"{'='*50}\n\n"
        
        for event in today_events:
            output += f"• {event['title']}\n"
            
            if event['time']:
                output += f"  ⏰ {event['time']}\n"
            
            if event.get('description'):
                output += f"  📝 {event['description']}\n"
            
            output += "\n"
        
        output += f"{'='*50}\n"
        
        return output
    
    def search_events(self, query):
        """Search events by title or description"""
        results = []
        
        for event in self.events:
            if not event.get('completed', False):
                if (query.lower() in event['title'].lower() or
                    query.lower() in event.get('description', '').lower()):
                    results.append(event)
        
        if not results:
            return f"No events found matching '{query}'"
        
        output = f"\n{'='*50}\n"
        output += f"🔍 SEARCH RESULTS FOR '{query}'\n"
        output += f"{'='*50}\n\n"
        
        for event in results:
            output += f"#{event['id']} - {event['title']}\n"
            output += f"   📆 {event['date']}"
            
            if event['time']:
                output += f" at {event['time']}\n"
            else:
                output += "\n"
            
            output += "\n"
        
        output += f"{'='*50}\n"
        output += f"Found {len(results)} event(s)\n"
        output += f"{'='*50}\n"
        
        return output
    
    def mark_completed(self, event_id):
        """Mark an event as completed"""
        for event in self.events:
            if event['id'] == event_id:
                event['completed'] = True
                self.save_events()
                
                return f"✅ Event #{event_id} marked as completed!"
        
        return f"⚠️ Event #{event_id} not found."
    
    def get_overdue_events(self):
        """Get overdue events"""
        today = datetime.now().date()
        
        overdue = []
        
        for event in self.events:
            if not event.get('completed', False):
                event_date = datetime.strptime(event['date'], "%Y-%m-%d").date()
                
                if event_date < today:
                    overdue.append(event)
        
        if not overdue:
            return "✅ No overdue events!"
        
        output = f"\n{'='*50}\n"
        output += f"⚠️ OVERDUE EVENTS\n"
        output += f"{'='*50}\n\n"
        
        for event in overdue:
            output += f"#{event['id']} - {event['title']}\n"
            output += f"   📆 {event['date']}\n\n"
        
        output += f"{'='*50}\n"
        
        return output
    
    def _parse_datetime(self, date, time=""):
        """Parse date and time strings"""
        date = date.lower()
        
        if date == "today":
            event_date = datetime.now().date()
        elif date == "tomorrow":
            event_date = datetime.now().date() + timedelta(days=1)
        else:
            try:
                event_date = datetime.strptime(date, "%Y-%m-%d").date()
            except:
                try:
                    event_date = datetime.strptime(date, "%m/%d/%Y").date()
                except:
                    event_date = datetime.strptime(date, "%d-%m-%Y").date()
        
        if time:
            try:
                event_time = datetime.strptime(time, "%H:%M").time()
                return datetime.combine(event_date, event_time)
            except:
                return datetime.combine(event_date, datetime.min.time())
        else:
            return datetime.combine(event_date, datetime.min.time())
    
    def _format_event(self, event):
        """Format a single event for display"""
        output = f"\n{'='*50}\n"
        output += f"📅 EVENT #{event['id']}\n"
        output += f"{'='*50}\n\n"
        output += f"Title: {event['title']}\n"
        output += f"Date: {event['date']}\n"
        
        if event['time']:
            output += f"Time: {event['time']}\n"
        
        output += f"Duration: {event['duration']} minutes\n"
        
        if event.get('description'):
            output += f"\nDescription:\n{event['description']}\n"
        
        output += f"\nStatus: {'✅ Completed' if event.get('completed') else '⏳ Pending'}\n"
        output += f"Created: {event['created']}\n"
        output += f"{'='*50}\n"
        
        return output

if __name__ == "__main__":
    calendar = CalendarManager()
    
    print("Testing Calendar Manager...")
    print(calendar.add_event("Team Meeting", "today", "14:00", 60, "Discuss project updates"))
    print(calendar.add_event("Doctor Appointment", "tomorrow", "10:30", 30))
    print(calendar.list_events())
