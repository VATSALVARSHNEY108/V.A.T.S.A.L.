"""
Smart Automation & AI Module
Advanced intelligent automation features for VATSAL

Features:
1. Auto-Bug Fixer - AI analyzes error logs and suggests/applies fixes
2. Meeting Scheduler AI - Finds optimal meeting times by analyzing calendars
3. Smart File Recommendations - Suggests relevant files based on current activity
4. Auto-Documentation Generator - Generates code/docs in real-time
5. Intelligent Command Shortcuts - Learns frequently-used command chains
6. Project Context Switcher - Switch between project environments with one click
7. Task Auto-Prioritizer - AI ranks tasks based on urgency, deadlines, and past behavior
8. Workflow Auto-Optimizer - Observes repeated actions and suggests smarter automations
9. Smart Template Generator - Creates boilerplate templates for code, emails, and documents
"""

import os
import json
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import defaultdict, Counter
import threading

from gemini_controller import get_client
from google.genai import types


def get_gemini_response(prompt: str) -> str:
    """Helper function to get response from Gemini AI"""
    try:
        client = get_client()
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error getting AI response: {str(e)}"


def safe_json_parse(response: str, default: Dict = None) -> Dict:
    """Safely parse JSON response from AI with fallback"""
    if default is None:
        default = {}
    
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        return default


class AutoBugFixer:
    """AI-powered automatic bug detection and fixing system"""
    
    def __init__(self):
        self.error_log_path = "error_logs.json"
        self.fix_history_path = "bug_fix_history.json"
        self.load_history()
    
    def load_history(self):
        """Load bug fix history"""
        try:
            if os.path.exists(self.fix_history_path):
                with open(self.fix_history_path, 'r') as f:
                    self.fix_history = json.load(f)
            else:
                self.fix_history = []
        except:
            self.fix_history = []
    
    def save_history(self):
        """Save bug fix history"""
        try:
            with open(self.fix_history_path, 'w') as f:
                json.dump(self.fix_history, f, indent=2)
        except Exception as e:
            print(f"Error saving fix history: {e}")
    
    def analyze_error_log(self, error_text: str) -> Dict:
        """Analyze error log and suggest fixes using AI"""
        prompt = f"""Analyze this error log and provide:
1. Error type and severity (Critical/High/Medium/Low)
2. Root cause analysis
3. Specific fix suggestions (step-by-step)
4. Code snippets to fix the issue (if applicable)
5. Prevention tips

Error Log:
{error_text}

Respond in JSON format with keys: error_type, severity, root_cause, fix_steps, code_fix, prevention_tips"""
        
        try:
            response = get_gemini_response(prompt)
            
            analysis = safe_json_parse(response, {
                "error_type": "Unknown",
                "severity": "Medium",
                "root_cause": response[:200] if response else "No response",
                "fix_steps": ["Review the error manually"],
                "code_fix": None,
                "prevention_tips": []
            })
            
            analysis.setdefault('error_type', 'Unknown')
            analysis.setdefault('severity', 'Medium')
            analysis.setdefault('fix_steps', [])
            analysis.setdefault('prevention_tips', [])
            
            analysis['timestamp'] = datetime.now().isoformat()
            analysis['original_error'] = error_text
            
            return analysis
        except Exception as e:
            return {
                "error": str(e),
                "error_type": "Analysis Failed",
                "severity": "Unknown",
                "fix_steps": [],
                "prevention_tips": []
            }
    
    def auto_fix_error(self, file_path: str, error_analysis: Dict, auto_apply: bool = False) -> Dict:
        """Suggest fixes for the error - does NOT automatically modify files for safety"""
        result = {
            "success": False,
            "message": "",
            "suggested_fix": None
        }
        
        if not error_analysis.get('code_fix'):
            result['message'] = "No code fix available for this error"
            return result
        
        if not os.path.exists(file_path):
            result['message'] = f"File not found: {file_path}"
            return result
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            result['success'] = True
            result['suggested_fix'] = error_analysis['code_fix']
            result['original_content'] = original_content
            result['backup_recommended'] = True
            result['message'] = "Fix suggestion generated. IMPORTANT: Review the suggested fix carefully before applying manually. Auto-apply is disabled for safety."
            
            if auto_apply:
                result['message'] += "\n\nWARNING: Auto-apply was requested but is disabled for safety. Please review and apply the fix manually."
            
            self.fix_history.append({
                'timestamp': datetime.now().isoformat(),
                'file': file_path,
                'error_type': error_analysis.get('error_type', 'Unknown'),
                'fix_applied': False,
                'fix_suggested': True
            })
            self.save_history()
        
        except Exception as e:
            result['message'] = f"Error generating fix suggestion: {str(e)}"
        
        return result
    
    def monitor_logs(self, log_file: str, callback=None):
        """Monitor a log file for errors in real-time"""
        if not os.path.exists(log_file):
            return {"error": f"Log file not found: {log_file}"}
        
        try:
            with open(log_file, 'r') as f:
                f.seek(0, 2)
                
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    
                    if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed', 'critical']):
                        analysis = self.analyze_error_log(line)
                        if callback:
                            callback(analysis)
        except Exception as e:
            return {"error": f"Monitoring failed: {str(e)}"}


class MeetingSchedulerAI:
    """AI-powered meeting scheduler that finds optimal times"""
    
    def __init__(self):
        self.calendar_path = "calendar_data.json"
        self.preferences_path = "meeting_preferences.json"
        self.load_data()
    
    def load_data(self):
        """Load calendar and preference data"""
        if os.path.exists(self.calendar_path):
            with open(self.calendar_path, 'r') as f:
                self.calendar_data = json.load(f)
        else:
            self.calendar_data = {}
        
        if os.path.exists(self.preferences_path):
            with open(self.preferences_path, 'r') as f:
                self.preferences = json.load(f)
        else:
            self.preferences = {
                "preferred_hours": {"start": 9, "end": 17},
                "avoid_days": [],
                "min_break_between_meetings": 15,
                "max_meetings_per_day": 8
            }
    
    def save_data(self):
        """Save calendar and preference data"""
        with open(self.calendar_path, 'w') as f:
            json.dump(self.calendar_data, f, indent=2)
        
        with open(self.preferences_path, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def add_event(self, title: str, start_time: datetime, duration_minutes: int, attendees: Optional[List[str]] = None):
        """Add event to calendar"""
        event_id = f"event_{int(time.time())}_{len(self.calendar_data)}"
        
        self.calendar_data[event_id] = {
            "title": title,
            "start": start_time.isoformat(),
            "duration": duration_minutes,
            "attendees": attendees or [],
            "created": datetime.now().isoformat()
        }
        
        self.save_data()
        return event_id
    
    def find_optimal_time(self, duration_minutes: int, attendees: List[str], 
                          days_ahead: int = 7, preferred_times: Optional[List[str]] = None) -> List[Dict]:
        """Find optimal meeting times using AI analysis"""
        
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days_ahead)
        
        busy_slots = []
        for event_id, event in self.calendar_data.items():
            event_start = datetime.fromisoformat(event['start'])
            if start_date <= event_start <= end_date:
                busy_slots.append({
                    'start': event_start,
                    'end': event_start + timedelta(minutes=event['duration'])
                })
        
        available_slots = []
        current_day = start_date.replace(hour=self.preferences['preferred_hours']['start'], minute=0)
        
        while current_day <= end_date:
            if current_day.weekday() not in self.preferences.get('avoid_days', []):
                day_end = current_day.replace(hour=self.preferences['preferred_hours']['end'])
                current_slot = current_day
                
                while current_slot + timedelta(minutes=duration_minutes) <= day_end:
                    slot_end = current_slot + timedelta(minutes=duration_minutes)
                    
                    is_available = True
                    for busy in busy_slots:
                        if not (slot_end <= busy['start'] or current_slot >= busy['end']):
                            is_available = False
                            break
                    
                    if is_available:
                        available_slots.append({
                            'start': current_slot.isoformat(),
                            'end': slot_end.isoformat(),
                            'score': 0
                        })
                    
                    current_slot += timedelta(minutes=30)
            
            current_day += timedelta(days=1)
            current_day = current_day.replace(hour=self.preferences['preferred_hours']['start'], minute=0)
        
        prompt = f"""Analyze these available time slots and rank them for a {duration_minutes}-minute meeting.
Consider: time of day preferences, attendee availability patterns, meeting fatigue, and productivity hours.

Available slots: {json.dumps(available_slots[:20], indent=2)}
Attendees: {attendees}
Preferred times: {preferred_times or 'No specific preference'}

Return top 5 recommended slots with scores (0-100) and reasoning in JSON format:
{{"recommendations": [{{"start": "...", "end": "...", "score": 95, "reason": "..."}}]}}"""
        
        try:
            response = get_gemini_response(prompt)
            result = safe_json_parse(response, {'recommendations': available_slots[:5]})
            return result.get('recommendations', available_slots[:5])
        except Exception as e:
            print(f"Meeting scheduler AI error: {e}")
            return available_slots[:5]
    
    def schedule_meeting(self, title: str, duration_minutes: int, attendees: List[str]) -> Dict:
        """Automatically schedule a meeting at the optimal time"""
        optimal_times = self.find_optimal_time(duration_minutes, attendees)
        
        if not optimal_times:
            return {"success": False, "message": "No available time slots found"}
        
        best_time = optimal_times[0]
        event_id = self.add_event(
            title, 
            datetime.fromisoformat(best_time['start']), 
            duration_minutes, 
            attendees
        )
        
        return {
            "success": True,
            "event_id": event_id,
            "scheduled_time": best_time,
            "alternatives": optimal_times[1:3]
        }


class SmartFileRecommender:
    """AI-powered file recommendation system based on current activity"""
    
    def __init__(self):
        self.activity_log_path = "file_activity_log.json"
        self.recommendations_cache = {}
        self.load_activity_log()
    
    def load_activity_log(self):
        """Load file activity history"""
        if os.path.exists(self.activity_log_path):
            with open(self.activity_log_path, 'r') as f:
                self.activity_log = json.load(f)
        else:
            self.activity_log = []
    
    def save_activity_log(self):
        """Save file activity history"""
        with open(self.activity_log_path, 'w') as f:
            json.dump(self.activity_log[-1000:], f, indent=2)
    
    def log_activity(self, file_path: str, activity_type: str, context: str = ""):
        """Log file activity"""
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'file': file_path,
            'activity': activity_type,
            'context': context
        })
        self.save_activity_log()
    
    def get_file_patterns(self) -> Dict:
        """Analyze file access patterns"""
        patterns = {
            'frequently_accessed': Counter(),
            'recent_files': [],
            'file_associations': defaultdict(list),
            'time_patterns': defaultdict(list)
        }
        
        for entry in self.activity_log[-500:]:
            file_path = entry.get('file', '')
            patterns['frequently_accessed'][file_path] += 1
            
            if entry not in patterns['recent_files'][-20:]:
                patterns['recent_files'].append(entry)
        
        for i, entry in enumerate(self.activity_log[-200:]):
            if i > 0:
                prev_file = self.activity_log[i-1].get('file')
                curr_file = entry.get('file')
                if prev_file and curr_file and prev_file != curr_file:
                    patterns['file_associations'][prev_file].append(curr_file)
        
        return patterns
    
    def recommend_files(self, current_file: Optional[str] = None, current_task: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Recommend relevant files based on current activity"""
        patterns = self.get_file_patterns()
        
        recommendations = []
        
        if current_file:
            associated_files = patterns['file_associations'].get(current_file, [])
            for file in associated_files[:5]:
                recommendations.append({
                    'file': file,
                    'reason': f'Frequently accessed after {os.path.basename(current_file)}',
                    'score': 90,
                    'type': 'association'
                })
        
        for file, count in patterns['frequently_accessed'].most_common(10):
            if file not in [r['file'] for r in recommendations]:
                recommendations.append({
                    'file': file,
                    'reason': f'Frequently accessed ({count} times)',
                    'score': min(80, 50 + count),
                    'type': 'frequency'
                })
        
        if current_task:
            prompt = f"""Based on this task description, recommend relevant file types and names:
Task: {current_task}
Recent files: {[f['file'] for f in patterns['recent_files'][:10]]}

Suggest 5 relevant files that might be needed. Return JSON: {{"suggestions": [{{"file": "...", "reason": "..."}}]}}"""
            
            try:
                response = get_gemini_response(prompt)
                result = safe_json_parse(response, {'suggestions': []})
                for suggestion in result.get('suggestions', []):
                    if isinstance(suggestion, dict) and 'file' in suggestion:
                        recommendations.append({
                            'file': suggestion.get('file', 'unknown'),
                            'reason': suggestion.get('reason', 'AI suggestion'),
                            'score': 85,
                            'type': 'ai_suggestion'
                        })
            except Exception as e:
                print(f"File recommender AI error: {e}")
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def smart_search(self, query: str, search_path: str = ".") -> List[Dict]:
        """Intelligent file search using AI and pattern matching"""
        matching_files = []
        
        for root, dirs, files in os.walk(search_path):
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules', '.venv']):
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                if query.lower() in file.lower():
                    matching_files.append({
                        'path': file_path,
                        'name': file,
                        'score': 100 if query.lower() == file.lower() else 70
                    })
        
        prompt = f"""Rank these files by relevance to the query: "{query}"
Files: {json.dumps([f['name'] for f in matching_files[:30]], indent=2)}

Return JSON with ranked files and scores: {{"ranked": [{{"file": "...", "score": 95, "reason": "..."}}]}}"""
        
        try:
            response = get_gemini_response(prompt)
            result = safe_json_parse(response, {'ranked': []})
            
            ranked_files = []
            for item in result.get('ranked', []):
                if isinstance(item, dict) and 'file' in item:
                    for mf in matching_files:
                        if item['file'] in mf['name']:
                            ranked_files.append({
                                'path': mf['path'],
                                'name': mf['name'],
                                'score': item.get('score', 50),
                                'reason': item.get('reason', '')
                            })
                            break
            
            return ranked_files if ranked_files else sorted(matching_files, key=lambda x: x['score'], reverse=True)
        except Exception as e:
            print(f"Smart search AI error: {e}")
            return sorted(matching_files, key=lambda x: x['score'], reverse=True)


class AutoDocGenerator:
    """Automatic documentation generator for code and projects"""
    
    def __init__(self):
        self.docs_output_dir = "auto_generated_docs"
        os.makedirs(self.docs_output_dir, exist_ok=True)
    
    def generate_function_docs(self, code: str, language: str = "python") -> str:
        """Generate documentation for functions in code"""
        prompt = f"""Analyze this {language} code and generate comprehensive documentation:

Code:
```{language}
{code}
```

Generate:
1. Function/method descriptions
2. Parameter explanations
3. Return value descriptions
4. Usage examples
5. Edge cases and notes

Format as proper {language} docstrings/comments."""
        
        try:
            docs = get_gemini_response(prompt)
            return docs
        except Exception as e:
            return f"Error generating documentation: {str(e)}"
    
    def generate_readme(self, project_path: str = ".") -> str:
        """Generate README.md for a project"""
        project_files = []
        code_files = []
        
        for root, dirs, files in os.walk(project_path):
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules']):
                continue
            
            for file in files:
                if file.endswith(('.py', '.js', '.java', '.cpp', '.go')):
                    code_files.append(os.path.join(root, file))
                project_files.append(file)
        
        code_samples = {}
        for code_file in code_files[:5]:
            try:
                with open(code_file, 'r', encoding='utf-8') as f:
                    code_samples[code_file] = f.read()[:500]
            except:
                pass
        
        prompt = f"""Generate a comprehensive README.md for this project:

Project files: {project_files[:30]}
Code samples: {json.dumps(code_samples, indent=2)}

Include:
1. Project title and description
2. Features list
3. Installation instructions
4. Usage examples
5. Dependencies
6. File structure
7. Contributing guidelines

Format as proper Markdown."""
        
        try:
            readme = get_gemini_response(prompt)
            
            output_path = os.path.join(self.docs_output_dir, "README_generated.md")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(readme)
            
            return readme
        except Exception as e:
            return f"Error generating README: {str(e)}"
    
    def generate_api_docs(self, code: str, language: str = "python") -> str:
        """Generate API documentation"""
        prompt = f"""Generate API documentation for this {language} code:

{code}

Create documentation with:
1. Endpoint/Function descriptions
2. Request/Response formats
3. Authentication requirements
4. Error codes
5. Example requests
6. Rate limits (if applicable)

Format as Markdown."""
        
        try:
            docs = get_gemini_response(prompt)
            return docs
        except Exception as e:
            return f"Error generating API docs: {str(e)}"
    
    def document_file(self, file_path: str) -> Dict:
        """Automatically document a code file"""
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            ext = os.path.splitext(file_path)[1]
            language = {'.py': 'python', '.js': 'javascript', '.java': 'java', 
                       '.cpp': 'cpp', '.go': 'go'}.get(ext, 'python')
            
            docs = self.generate_function_docs(code, language)
            
            docs_filename = os.path.basename(file_path) + ".docs.md"
            docs_path = os.path.join(self.docs_output_dir, docs_filename)
            
            with open(docs_path, 'w', encoding='utf-8') as f:
                f.write(f"# Documentation for {file_path}\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(docs)
            
            return {
                "success": True,
                "docs_path": docs_path,
                "documentation": docs
            }
        except Exception as e:
            return {"error": str(e)}


class IntelligentCommandShortcuts:
    """Learn and suggest command shortcuts based on usage patterns"""
    
    def __init__(self):
        self.command_history_path = "command_history.json"
        self.shortcuts_path = "intelligent_shortcuts.json"
        self.load_data()
    
    def load_data(self):
        """Load command history and shortcuts"""
        if os.path.exists(self.command_history_path):
            with open(self.command_history_path, 'r') as f:
                self.command_history = json.load(f)
        else:
            self.command_history = []
        
        if os.path.exists(self.shortcuts_path):
            with open(self.shortcuts_path, 'r') as f:
                self.shortcuts = json.load(f)
        else:
            self.shortcuts = {}
    
    def save_data(self):
        """Save command history and shortcuts"""
        with open(self.command_history_path, 'w') as f:
            json.dump(self.command_history[-1000:], f, indent=2)
        
        with open(self.shortcuts_path, 'w') as f:
            json.dump(self.shortcuts, f, indent=2)
    
    def log_command(self, command: str, context: str = ""):
        """Log executed command"""
        self.command_history.append({
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'context': context
        })
        self.save_data()
    
    def find_command_chains(self, min_frequency: int = 3) -> List[Dict]:
        """Find frequently used command chains"""
        chains = defaultdict(int)
        
        for i in range(len(self.command_history) - 1):
            cmd1 = self.command_history[i]['command']
            cmd2 = self.command_history[i + 1]['command']
            
            time1 = datetime.fromisoformat(self.command_history[i]['timestamp'])
            time2 = datetime.fromisoformat(self.command_history[i + 1]['timestamp'])
            
            if (time2 - time1).total_seconds() < 300:
                chain = f"{cmd1} → {cmd2}"
                chains[chain] += 1
        
        frequent_chains = []
        for chain, count in chains.items():
            if count >= min_frequency:
                frequent_chains.append({
                    'chain': chain,
                    'frequency': count,
                    'commands': chain.split(' → ')
                })
        
        return sorted(frequent_chains, key=lambda x: x['frequency'], reverse=True)
    
    def suggest_shortcuts(self) -> List[Dict]:
        """Suggest intelligent shortcuts based on patterns"""
        chains = self.find_command_chains()
        
        prompt = f"""Analyze these frequently used command chains and suggest intelligent shortcuts:

Command chains: {json.dumps(chains[:10], indent=2)}

For each chain, suggest:
1. A short, memorable shortcut name
2. Description of what it does
3. Parameters (if any)

Return JSON: {{"suggestions": [{{"shortcut": "...", "description": "...", "commands": [...], "parameters": [...]}}]}}"""
        
        try:
            response = get_gemini_response(prompt)
            result = safe_json_parse(response, {'suggestions': []})
            suggestions = result.get('suggestions', [])
            
            if not suggestions:
                for i, chain in enumerate(chains[:5]):
                    suggestions.append({
                        'shortcut': f"chain{i+1}",
                        'description': f"Execute: {chain['chain']}",
                        'commands': chain['commands'],
                        'frequency': chain['frequency']
                    })
            
            return suggestions
        except Exception as e:
            print(f"Command shortcuts AI error: {e}")
            suggestions = []
            for i, chain in enumerate(chains[:5]):
                suggestions.append({
                    'shortcut': f"chain{i+1}",
                    'description': f"Execute: {chain['chain']}",
                    'commands': chain['commands'],
                    'frequency': chain['frequency']
                })
            return suggestions
    
    def create_shortcut(self, shortcut_name: str, commands: List[str], description: str = "") -> Dict:
        """Create a new shortcut"""
        self.shortcuts[shortcut_name] = {
            'commands': commands,
            'description': description,
            'created': datetime.now().isoformat(),
            'usage_count': 0
        }
        self.save_data()
        
        return {
            "success": True,
            "shortcut": shortcut_name,
            "commands": commands
        }
    
    def execute_shortcut(self, shortcut_name: str) -> Dict:
        """Execute a shortcut"""
        if shortcut_name not in self.shortcuts:
            return {"error": f"Shortcut '{shortcut_name}' not found"}
        
        shortcut = self.shortcuts[shortcut_name]
        shortcut['usage_count'] = shortcut.get('usage_count', 0) + 1
        shortcut['last_used'] = datetime.now().isoformat()
        self.save_data()
        
        return {
            "success": True,
            "shortcut": shortcut_name,
            "commands": shortcut['commands'],
            "description": shortcut.get('description', '')
        }
    
    def get_most_used_shortcuts(self, limit: int = 10) -> List[Dict]:
        """Get most frequently used shortcuts"""
        shortcuts_list = []
        for name, data in self.shortcuts.items():
            shortcuts_list.append({
                'name': name,
                'usage_count': data.get('usage_count', 0),
                'description': data.get('description', ''),
                'commands': data['commands']
            })
        
        return sorted(shortcuts_list, key=lambda x: x['usage_count'], reverse=True)[:limit]


class ProjectContextSwitcher:
    """Switch between project environments with one click"""
    
    def __init__(self):
        self.contexts_path = "project_contexts.json"
        self.current_context_path = "current_context.json"
        self.load_contexts()
    
    def load_contexts(self):
        """Load saved project contexts"""
        if os.path.exists(self.contexts_path):
            with open(self.contexts_path, 'r') as f:
                self.contexts = json.load(f)
        else:
            self.contexts = {}
        
        if os.path.exists(self.current_context_path):
            with open(self.current_context_path, 'r') as f:
                self.current_context = json.load(f)
        else:
            self.current_context = None
    
    def save_contexts(self):
        """Save project contexts"""
        with open(self.contexts_path, 'w') as f:
            json.dump(self.contexts, f, indent=2)
        
        with open(self.current_context_path, 'w') as f:
            json.dump(self.current_context, f, indent=2)
    
    def save_context(self, context_name: str, project_path: str, 
                    open_files: Optional[List[str]] = None, notes: str = "") -> Dict:
        """Save current project context"""
        context = {
            'name': context_name,
            'project_path': project_path,
            'open_files': open_files or [],
            'notes': notes,
            'created': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'environment_vars': {},
            'recent_commands': []
        }
        
        self.contexts[context_name] = context
        self.save_contexts()
        
        return {"success": True, "context": context_name}
    
    def switch_context(self, context_name: str) -> Dict:
        """Switch to a different project context"""
        if context_name not in self.contexts:
            return {"error": f"Context '{context_name}' not found"}
        
        context = self.contexts[context_name]
        context['last_accessed'] = datetime.now().isoformat()
        
        self.current_context = context
        self.save_contexts()
        
        return {
            "success": True,
            "context": context_name,
            "project_path": context['project_path'],
            "open_files": context['open_files'],
            "notes": context.get('notes', '')
        }
    
    def list_contexts(self) -> List[Dict]:
        """List all saved contexts"""
        contexts_list = []
        for name, data in self.contexts.items():
            contexts_list.append({
                'name': name,
                'project_path': data['project_path'],
                'last_accessed': data.get('last_accessed', data.get('created', '')),
                'file_count': len(data.get('open_files', []))
            })
        
        return sorted(contexts_list, key=lambda x: x.get('last_accessed', ''), reverse=True)
    
    def delete_context(self, context_name: str) -> Dict:
        """Delete a saved context"""
        if context_name in self.contexts:
            del self.contexts[context_name]
            self.save_contexts()
            return {"success": True, "message": f"Context '{context_name}' deleted"}
        return {"error": f"Context '{context_name}' not found"}
    
    def get_current_context(self) -> Optional[Dict]:
        """Get currently active context"""
        return self.current_context


class TaskAutoPrioritizer:
    """AI-powered task prioritization based on urgency, deadlines, and behavior"""
    
    def __init__(self):
        self.tasks_path = "tasks_data.json"
        self.behavior_path = "task_behavior_data.json"
        self.load_data()
    
    def load_data(self):
        """Load tasks and behavior data"""
        if os.path.exists(self.tasks_path):
            with open(self.tasks_path, 'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []
        
        if os.path.exists(self.behavior_path):
            with open(self.behavior_path, 'r') as f:
                self.behavior_data = json.load(f)
        else:
            self.behavior_data = {
                'completion_patterns': [],
                'average_completion_time': {},
                'preferred_work_hours': []
            }
    
    def save_data(self):
        """Save tasks and behavior data"""
        with open(self.tasks_path, 'w') as f:
            json.dump(self.tasks, f, indent=2)
        
        with open(self.behavior_path, 'w') as f:
            json.dump(self.behavior_data, f, indent=2)
    
    def add_task(self, title: str, description: str = "", deadline: Optional[str] = None, 
                estimated_time: Optional[int] = None, category: str = "general") -> Dict:
        """Add a new task"""
        task = {
            'id': f"task_{int(time.time())}_{len(self.tasks)}",
            'title': title,
            'description': description,
            'deadline': deadline,
            'estimated_time': estimated_time,
            'category': category,
            'created': datetime.now().isoformat(),
            'status': 'pending',
            'priority_score': 0
        }
        
        self.tasks.append(task)
        self.save_data()
        
        return {"success": True, "task_id": task['id']}
    
    def calculate_priority_score(self, task: Dict) -> float:
        """Calculate AI-powered priority score for a task"""
        score = 50.0
        
        if task.get('deadline'):
            try:
                deadline = datetime.fromisoformat(task['deadline'])
                days_until = (deadline - datetime.now()).total_seconds() / 86400
                
                if days_until < 1:
                    score += 40
                elif days_until < 3:
                    score += 30
                elif days_until < 7:
                    score += 20
                elif days_until < 14:
                    score += 10
            except:
                pass
        
        if task.get('estimated_time'):
            if task['estimated_time'] < 30:
                score += 10
        
        category_weights = {
            'urgent': 25,
            'important': 20,
            'work': 15,
            'personal': 10,
            'general': 5
        }
        score += category_weights.get(task.get('category', 'general'), 5)
        
        return min(100, score)
    
    def prioritize_tasks(self) -> List[Dict]:
        """Prioritize all tasks using AI"""
        for task in self.tasks:
            if task['status'] == 'pending':
                task['priority_score'] = self.calculate_priority_score(task)
        
        pending_tasks = [t for t in self.tasks if t['status'] == 'pending']
        
        if len(pending_tasks) > 1:
            prompt = f"""Analyze and rank these tasks by priority considering:
1. Deadlines and urgency
2. Estimated time to complete
3. Task dependencies
4. Categories and importance

Tasks: {json.dumps(pending_tasks, indent=2)}

Return ranked task IDs with adjusted scores: {{"ranked": [{{"id": "...", "score": 95, "reason": "..."}}]}}"""
            
            try:
                response = get_gemini_response(prompt)
                result = safe_json_parse(response, {'ranked': []})
                
                for ranked in result.get('ranked', []):
                    if isinstance(ranked, dict) and 'id' in ranked:
                        for task in self.tasks:
                            if task['id'] == ranked['id']:
                                task['priority_score'] = ranked.get('score', task.get('priority_score', 50))
                                task['priority_reason'] = ranked.get('reason', '')
            except Exception as e:
                print(f"Task prioritizer AI error: {e}")
        
        self.save_data()
        
        prioritized = sorted(
            [t for t in self.tasks if t['status'] == 'pending'],
            key=lambda x: x.get('priority_score', 0),
            reverse=True
        )
        
        return prioritized
    
    def complete_task(self, task_id: str) -> Dict:
        """Mark task as complete and update behavior data"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                
                if task.get('created'):
                    created = datetime.fromisoformat(task['created'])
                    completed = datetime.fromisoformat(task['completed_at'])
                    completion_time = (completed - created).total_seconds() / 60
                    
                    self.behavior_data['completion_patterns'].append({
                        'category': task.get('category', 'general'),
                        'time_taken': completion_time,
                        'hour': completed.hour
                    })
                
                self.save_data()
                return {"success": True, "task": task['title']}
        
        return {"error": "Task not found"}
    
    def get_task_suggestions(self) -> List[str]:
        """Get AI suggestions for task management"""
        prioritized = self.prioritize_tasks()
        
        suggestions = []
        
        if prioritized:
            top_task = prioritized[0]
            suggestions.append(f"Focus on: {top_task['title']} (Priority: {top_task.get('priority_score', 0):.0f})")
        
        urgent_tasks = [t for t in prioritized if t.get('priority_score', 0) > 80]
        if len(urgent_tasks) > 3:
            suggestions.append(f"You have {len(urgent_tasks)} urgent tasks - consider delegating or rescheduling some")
        
        if self.behavior_data['completion_patterns']:
            avg_hour = sum(p['hour'] for p in self.behavior_data['completion_patterns']) / len(self.behavior_data['completion_patterns'])
            suggestions.append(f"You're most productive around {int(avg_hour)}:00 - schedule important tasks then")
        
        return suggestions


class WorkflowAutoOptimizer:
    """Observes repeated actions and suggests optimized workflows"""
    
    def __init__(self):
        self.actions_log_path = "workflow_actions_log.json"
        self.optimizations_path = "workflow_optimizations.json"
        self.load_data()
    
    def load_data(self):
        """Load action logs and optimizations"""
        if os.path.exists(self.actions_log_path):
            with open(self.actions_log_path, 'r') as f:
                self.actions_log = json.load(f)
        else:
            self.actions_log = []
        
        if os.path.exists(self.optimizations_path):
            with open(self.optimizations_path, 'r') as f:
                self.optimizations = json.load(f)
        else:
            self.optimizations = []
    
    def save_data(self):
        """Save action logs and optimizations"""
        with open(self.actions_log_path, 'w') as f:
            json.dump(self.actions_log[-2000:], f, indent=2)
        
        with open(self.optimizations_path, 'w') as f:
            json.dump(self.optimizations, f, indent=2)
    
    def log_action(self, action_type: str, details: Dict):
        """Log a workflow action"""
        self.actions_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action_type,
            'details': details
        })
        self.save_data()
    
    def detect_patterns(self, min_occurrences: int = 3) -> List[Dict]:
        """Detect repeated action patterns"""
        patterns = defaultdict(list)
        
        for i in range(len(self.actions_log) - 2):
            sequence = []
            for j in range(min(5, len(self.actions_log) - i)):
                sequence.append(self.actions_log[i + j]['action'])
            
            pattern_key = ' → '.join(sequence[:3])
            patterns[pattern_key].append({
                'start_index': i,
                'timestamp': self.actions_log[i]['timestamp']
            })
        
        repeated_patterns = []
        for pattern, occurrences in patterns.items():
            if len(occurrences) >= min_occurrences:
                repeated_patterns.append({
                    'pattern': pattern,
                    'occurrences': len(occurrences),
                    'actions': pattern.split(' → ')
                })
        
        return sorted(repeated_patterns, key=lambda x: x['occurrences'], reverse=True)
    
    def suggest_optimizations(self) -> List[Dict]:
        """Suggest workflow optimizations using AI"""
        patterns = self.detect_patterns()
        
        if not patterns:
            return []
        
        prompt = f"""Analyze these repeated workflow patterns and suggest optimizations:

Patterns: {json.dumps(patterns[:10], indent=2)}

For each pattern, suggest:
1. How to combine steps
2. What can be automated
3. Estimated time savings
4. Implementation difficulty (Easy/Medium/Hard)

Return JSON: {{"optimizations": [{{"pattern": "...", "suggestion": "...", "time_saved": "...", "difficulty": "..."}}]}}"""
        
        try:
            response = get_gemini_response(prompt)
            result = safe_json_parse(response, {'optimizations': []})
            
            suggestions = result.get('optimizations', [])
            
            for suggestion in suggestions:
                if isinstance(suggestion, dict):
                    suggestion['created'] = datetime.now().isoformat()
                    suggestion['status'] = 'suggested'
            
            if suggestions:
                self.optimizations.extend(suggestions)
                self.save_data()
            
            return suggestions
        except Exception as e:
            print(f"Workflow optimizer AI error: {e}")
            return []
    
    def create_automated_workflow(self, pattern: str, workflow_name: str) -> Dict:
        """Create an automated workflow from a pattern"""
        patterns = self.detect_patterns()
        
        matching_pattern = None
        for p in patterns:
            if p['pattern'] == pattern:
                matching_pattern = p
                break
        
        if not matching_pattern:
            return {"error": "Pattern not found"}
        
        workflow = {
            'name': workflow_name,
            'pattern': pattern,
            'actions': matching_pattern['actions'],
            'created': datetime.now().isoformat(),
            'usage_count': 0
        }
        
        return {
            "success": True,
            "workflow": workflow
        }
    
    def get_efficiency_report(self) -> Dict:
        """Generate efficiency report"""
        total_actions = len(self.actions_log)
        patterns = self.detect_patterns()
        
        optimizable_actions = sum(p['occurrences'] for p in patterns if p['occurrences'] >= 3)
        
        efficiency_score = 100 - (optimizable_actions / max(total_actions, 1) * 100)
        
        report = {
            'total_actions': total_actions,
            'detected_patterns': len(patterns),
            'optimizable_actions': optimizable_actions,
            'efficiency_score': round(efficiency_score, 1),
            'top_patterns': patterns[:5],
            'recommendations': []
        }
        
        if efficiency_score < 70:
            report['recommendations'].append("Many repeated patterns detected - consider creating automated workflows")
        if len(patterns) > 10:
            report['recommendations'].append(f"Found {len(patterns)} patterns - prioritize automating the most frequent ones")
        
        return report


class SmartTemplateGenerator:
    """AI-powered template generator for code, emails, and documents"""
    
    def __init__(self):
        self.templates_dir = "smart_templates"
        os.makedirs(self.templates_dir, exist_ok=True)
        self.templates_index_path = os.path.join(self.templates_dir, "templates_index.json")
        self.load_templates_index()
    
    def load_templates_index(self):
        """Load templates index"""
        if os.path.exists(self.templates_index_path):
            with open(self.templates_index_path, 'r') as f:
                self.templates_index = json.load(f)
        else:
            self.templates_index = {}
    
    def save_templates_index(self):
        """Save templates index"""
        with open(self.templates_index_path, 'w') as f:
            json.dump(self.templates_index, f, indent=2)
    
    def generate_code_template(self, language: str, template_type: str, 
                              description: str = "") -> str:
        """Generate code template using AI"""
        prompt = f"""Generate a {language} {template_type} template.

Description: {description or 'Standard implementation'}

Include:
1. Proper structure and boilerplate
2. Common imports/dependencies
3. Placeholder comments for customization
4. Best practices and patterns
5. Error handling
6. Example usage in comments

Generate production-ready, well-commented code."""
        
        try:
            template = get_gemini_response(prompt)
            
            template_name = f"{language}_{template_type}_{int(time.time())}"
            template_path = os.path.join(self.templates_dir, f"{template_name}.txt")
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template)
            
            self.templates_index[template_name] = {
                'type': 'code',
                'language': language,
                'template_type': template_type,
                'path': template_path,
                'created': datetime.now().isoformat()
            }
            self.save_templates_index()
            
            return template
        except Exception as e:
            return f"Error generating template: {str(e)}"
    
    def generate_email_template(self, purpose: str, tone: str = "professional") -> str:
        """Generate email template using AI"""
        prompt = f"""Generate an email template for: {purpose}

Tone: {tone}
Include:
1. Subject line
2. Greeting
3. Body with placeholders for customization
4. Call-to-action
5. Professional closing
6. Signature block

Make it professional and effective."""
        
        try:
            template = get_gemini_response(prompt)
            
            template_name = f"email_{purpose.replace(' ', '_')}_{int(time.time())}"
            template_path = os.path.join(self.templates_dir, f"{template_name}.txt")
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template)
            
            self.templates_index[template_name] = {
                'type': 'email',
                'purpose': purpose,
                'tone': tone,
                'path': template_path,
                'created': datetime.now().isoformat()
            }
            self.save_templates_index()
            
            return template
        except Exception as e:
            return f"Error generating email template: {str(e)}"
    
    def generate_document_template(self, document_type: str, sections: Optional[List[str]] = None) -> str:
        """Generate document template using AI"""
        sections_text = ', '.join(sections) if sections else 'standard sections'
        
        prompt = f"""Generate a {document_type} template.

Sections to include: {sections_text}

Create a comprehensive template with:
1. Title and header
2. All requested sections with descriptions
3. Placeholders for content
4. Formatting guidelines
5. Footer

Format as Markdown."""
        
        try:
            template = get_gemini_response(prompt)
            
            template_name = f"document_{document_type.replace(' ', '_')}_{int(time.time())}"
            template_path = os.path.join(self.templates_dir, f"{template_name}.md")
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template)
            
            self.templates_index[template_name] = {
                'type': 'document',
                'document_type': document_type,
                'sections': sections or [],
                'path': template_path,
                'created': datetime.now().isoformat()
            }
            self.save_templates_index()
            
            return template
        except Exception as e:
            return f"Error generating document template: {str(e)}"
    
    def list_templates(self, template_type: Optional[str] = None) -> List[Dict]:
        """List all saved templates"""
        templates = []
        for name, data in self.templates_index.items():
            if template_type is None or data.get('type') == template_type:
                templates.append({
                    'name': name,
                    'type': data.get('type', 'unknown'),
                    'path': data.get('path', ''),
                    'created': data.get('created', '')
                })
        
        return sorted(templates, key=lambda x: x.get('created', ''), reverse=True)
    
    def use_template(self, template_name: str, customizations: Optional[Dict] = None) -> str:
        """Use a template with customizations"""
        if template_name not in self.templates_index:
            return "Template not found"
        
        template_data = self.templates_index[template_name]
        template_path = template_data['path']
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            if customizations:
                for key, value in customizations.items():
                    placeholder = f"{{{{{key}}}}}"
                    template_content = template_content.replace(placeholder, str(value))
            
            return template_content
        except Exception as e:
            return f"Error using template: {str(e)}"


class SmartAutomationManager:
    """Main manager for all smart automation features"""
    
    def __init__(self):
        self.bug_fixer = AutoBugFixer()
        self.meeting_scheduler = MeetingSchedulerAI()
        self.file_recommender = SmartFileRecommender()
        self.doc_generator = AutoDocGenerator()
        self.command_shortcuts = IntelligentCommandShortcuts()
        self.context_switcher = ProjectContextSwitcher()
        self.task_prioritizer = TaskAutoPrioritizer()
        self.workflow_optimizer = WorkflowAutoOptimizer()
        self.template_generator = SmartTemplateGenerator()
    
    def get_dashboard_summary(self) -> Dict:
        """Get summary of all smart automation features"""
        return {
            'auto_bug_fixer': {
                'fixes_applied': len(self.bug_fixer.fix_history),
                'recent_fixes': self.bug_fixer.fix_history[-5:]
            },
            'meeting_scheduler': {
                'upcoming_meetings': len([e for e in self.meeting_scheduler.calendar_data.values()])
            },
            'file_recommender': {
                'tracked_files': len(set(e['file'] for e in self.file_recommender.activity_log))
            },
            'command_shortcuts': {
                'shortcuts_created': len(self.command_shortcuts.shortcuts),
                'most_used': self.command_shortcuts.get_most_used_shortcuts(3)
            },
            'project_contexts': {
                'saved_contexts': len(self.context_switcher.contexts),
                'current': self.context_switcher.get_current_context()
            },
            'task_prioritizer': {
                'pending_tasks': len([t for t in self.task_prioritizer.tasks if t['status'] == 'pending']),
                'top_priority': self.task_prioritizer.prioritize_tasks()[:3] if self.task_prioritizer.tasks else []
            },
            'workflow_optimizer': {
                'patterns_detected': len(self.workflow_optimizer.detect_patterns()),
                'efficiency_score': self.workflow_optimizer.get_efficiency_report().get('efficiency_score', 0)
            },
            'template_generator': {
                'templates_created': len(self.template_generator.templates_index)
            }
        }


if __name__ == "__main__":
    manager = SmartAutomationManager()
    
    print("🎯 Smart Automation & AI - Feature Test")
    print("=" * 50)
    
    print("\n1. Auto-Bug Fixer Test")
    test_error = "TypeError: Cannot read property 'length' of undefined at line 42"
    analysis = manager.bug_fixer.analyze_error_log(test_error)
    print(f"Error Analysis: {analysis.get('error_type', 'N/A')}")
    print(f"Severity: {analysis.get('severity', 'N/A')}")
    
    print("\n2. Meeting Scheduler Test")
    meeting = manager.meeting_scheduler.schedule_meeting(
        "Team Standup",
        30,
        ["alice@example.com", "bob@example.com"]
    )
    print(f"Meeting scheduled: {meeting.get('success', False)}")
    
    print("\n3. Smart File Recommendations Test")
    recs = manager.file_recommender.recommend_files(current_task="Fix authentication bug", limit=3)
    print(f"Recommended files: {len(recs)}")
    
    print("\n4. Auto-Documentation Test")
    print("Documentation generator initialized ✓")
    
    print("\n5. Command Shortcuts Test")
    suggestions = manager.command_shortcuts.suggest_shortcuts()
    print(f"Shortcut suggestions: {len(suggestions)}")
    
    print("\n6. Project Context Switcher Test")
    contexts = manager.context_switcher.list_contexts()
    print(f"Saved contexts: {len(contexts)}")
    
    print("\n7. Task Auto-Prioritizer Test")
    manager.task_prioritizer.add_task("Complete documentation", deadline=(datetime.now() + timedelta(days=2)).isoformat())
    prioritized = manager.task_prioritizer.prioritize_tasks()
    print(f"Prioritized tasks: {len(prioritized)}")
    
    print("\n8. Workflow Auto-Optimizer Test")
    efficiency = manager.workflow_optimizer.get_efficiency_report()
    print(f"Efficiency score: {efficiency.get('efficiency_score', 0)}")
    
    print("\n9. Smart Template Generator Test")
    templates = manager.template_generator.list_templates()
    print(f"Available templates: {len(templates)}")
    
    print("\n" + "=" * 50)
    print("Dashboard Summary:")
    summary = manager.get_dashboard_summary()
    print(json.dumps(summary, indent=2))
