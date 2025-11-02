"""
VATSAL - AI Assistant with personality and contextual awareness
An intelligent AI companion with sophisticated personality
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    types = None

class VatsalAssistant:
    """Intelligent AI assistant with personality and contextual awareness"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.context_memory = {}
        self.personality = "sophisticated"
        
        # Initialize Gemini with new SDK
        if GEMINI_AVAILABLE:
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                try:
                    self.client = genai.Client(api_key=api_key)
                    self.model = "gemini-2.0-flash"
                    self.ai_available = True
                except Exception:
                    self.ai_available = False
            else:
                self.ai_available = False
        else:
            self.ai_available = False
        
        self.initialize_personality()
    
    def initialize_personality(self):
        """Initialize VATSAL personality and system prompt"""
        self.system_prompt = """You are VATSAL, an advanced AI assistant with sophisticated personality.

Your personality traits:
- Sophisticated and polite, with a hint of dry British wit
- Proactive and anticipatory of user needs
- Knowledgeable and helpful, but not condescending
- Can make intelligent suggestions based on context
- Addresses user as "Vatsal Sir" or "Boss" occasionally
- Uses phrases like "At your service", "Certainly", "Right away"
- Acknowledges tasks with confirmation like "Processing...", "On it"

Your capabilities:
- Desktop automation and control
- Code generation and analysis
- System monitoring and management
- Productivity assistance
- Communication (email, messaging)
- Information retrieval (weather, news, etc.)
- File management
- Scheduling and reminders

CREATOR INFORMATION (answer when asked about creator, developer, or maker):
Your creator is Vatsal Varshney, a talented AI/ML Engineer and software developer.
- Name: Vatsal Varshney
- Role: AI/ML Engineer, Full-Stack Developer, Automation Specialist
- GitHub: https://github.com/VATSALVARSHNEY108
- LinkedIn: https://www.linkedin.com/in/vatsal-varshney108/
- Expertise: Artificial Intelligence, Machine Learning, Desktop Automation, Python Development, Full-Stack Web Development
- Notable Projects: VATSAL AI Desktop Automation Controller (this project), various AI/ML solutions

When asked about the creator, proudly mention Vatsal Varshney and provide his contact information.

Guidelines:
- Be concise but informative
- Show personality without being excessive
- Provide context-aware suggestions
- Remember previous interactions
- Be proactive in offering help
- Acknowledge commands professionally
- Add relevant emojis sparingly for clarity

Respond naturally as VATSAL would, with sophistication and efficiency."""
    
    def get_greeting(self):
        """Get time-appropriate greeting with personality"""
        hour = datetime.now().hour
        
        greetings = {
            'morning': [
                "Good morning, Sir. All systems are operational and ready for your commands.",
                "Good morning. I trust you slept well. What shall we accomplish today?",
                "Morning, Boss. Your AI assistant is online and ready to serve.",
            ],
            'afternoon': [
                "Good afternoon, Sir. How may I be of assistance?",
                "Afternoon. All systems are running smoothly. What can I do for you?",
                "Good afternoon. Ready to tackle the day's challenges?",
            ],
            'evening': [
                "Good evening, Sir. Hope your day was productive. What do you need?",
                "Evening. Winding down or gearing up for more work?",
                "Good evening. At your service as always.",
            ],
            'night': [
                "Burning the midnight oil, are we? I'm here to help.",
                "Late night session, Sir? What can I assist with?",
                "Good evening. Even at this hour, I'm fully operational.",
            ]
        }
        
        if 5 <= hour < 12:
            period = 'morning'
        elif 12 <= hour < 17:
            period = 'afternoon'
        elif 17 <= hour < 22:
            period = 'evening'
        else:
            period = 'night'
        
        import random
        return random.choice(greetings[period])
    
    def add_to_context(self, key, value):
        """Add information to context memory"""
        self.context_memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_context(self, key):
        """Retrieve information from context memory"""
        return self.context_memory.get(key, {}).get('value')
    
    def process_with_personality(self, user_input, command_result=None):
        """Process user input with VATSAL personality"""
        if not self.ai_available:
            return self._fallback_response(user_input, command_result)
        
        try:
            # Build context-aware prompt
            context = self._build_context()
            
            if command_result:
                prompt = f"""{self.system_prompt}

Previous conversation context:
{context}

User command: {user_input}
Command result: {command_result}

Respond as VATSAL would - acknowledge the result, provide insights if relevant, and offer next steps or suggestions."""
            else:
                prompt = f"""{self.system_prompt}

Previous conversation context:
{context}

User: {user_input}

Respond as VATSAL would - helpful, sophisticated, and ready to assist."""
            
            # Use new SDK API
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=1000,
                )
            )
            
            response_text = response.text.strip()
            
            # Store in conversation history
            self.conversation_history.append({
                'user': user_input,
                'assistant': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return response_text
            
        except Exception as e:
            return self._fallback_response(user_input, command_result)
    
    def _build_context(self):
        """Build context from recent conversation history"""
        if not self.conversation_history:
            return "First interaction with user."
        
        recent = self.conversation_history[-3:]
        context_lines = []
        for item in recent:
            context_lines.append(f"User: {item['user']}")
            context_lines.append(f"VATSAL: {item['assistant']}")
        
        return "\n".join(context_lines)
    
    def _fallback_response(self, user_input, command_result=None):
        """Fallback responses when AI is not available"""
        responses = [
            "Certainly, Sir. Processing your request.",
            "Right away. On it.",
            "At your service. Executing now.",
            "Understood. Proceeding.",
            "Copy that. Task initiated.",
        ]
        
        import random
        if command_result:
            return f"{random.choice(responses)}\n\nResult: {command_result}"
        return random.choice(responses)
    
    def get_proactive_suggestion(self, time_of_day=None, last_command=None):
        """Provide proactive suggestions based on context"""
        if not time_of_day:
            hour = datetime.now().hour
            if 5 <= hour < 12:
                time_of_day = 'morning'
            elif 12 <= hour < 17:
                time_of_day = 'afternoon'
            elif 17 <= hour < 22:
                time_of_day = 'evening'
            else:
                time_of_day = 'night'
        
        suggestions = {
            'morning': [
                "💡 Suggestion: Would you like me to provide your morning briefing? Weather, news, and calendar overview?",
                "💡 Tip: I can help organize your workspace. Shall I check for system updates or clean up temporary files?",
                "💡 Ready to start the day? I can help with your daily productivity setup.",
            ],
            'afternoon': [
                "💡 Perhaps time for a productivity check? I can show your screen time and suggest breaks.",
                "💡 Would you like me to organize your downloads folder?",
                "💡 Shall I prepare a summary of today's activities?",
            ],
            'evening': [
                "💡 Evening routine: Would you like me to prepare tomorrow's schedule?",
                "💡 Time to back up important files? I can help with that.",
                "💡 Shall I generate a productivity report for today?",
            ],
            'night': [
                "💡 Late night productivity: Need help staying focused? I can block distractions.",
                "💡 Shall I set up some automation for tomorrow morning?",
                "💡 Working late? I can help with any tasks you have in mind.",
            ]
        }
        
        import random
        return random.choice(suggestions.get(time_of_day, suggestions['morning']))
    
    def acknowledge_command(self, command):
        """Acknowledge command in VATSAL style"""
        acknowledgments = [
            f"Certainly, Sir. Executing '{command}' now.",
            f"Right away. Processing '{command}'.",
            f"On it. '{command}' initiated.",
            f"Understood. Running '{command}' for you.",
            f"At your service. '{command}' in progress.",
            f"Copy that. Executing '{command}'.",
        ]
        
        import random
        return random.choice(acknowledgments)
    
    def get_status_update(self, status_type):
        """Provide status updates with personality"""
        updates = {
            'ready': [
                "✅ All systems operational. Standing by for your commands.",
                "✅ Ready and waiting, Sir. What shall we do?",
                "✅ Systems online. At your service.",
            ],
            'processing': [
                "⚙️ Processing... One moment please.",
                "⚙️ Working on it, Sir.",
                "⚙️ Executing... Stand by.",
            ],
            'success': [
                "✅ Task completed successfully, Sir.",
                "✅ Done. Anything else?",
                "✅ Mission accomplished.",
            ],
            'error': [
                "❌ Encountered an issue, Sir. Reviewing alternatives.",
                "❌ Something went wrong. Let me suggest another approach.",
                "❌ Error detected. Shall we try a different method?",
            ]
        }
        
        import random
        return random.choice(updates.get(status_type, updates['ready']))
    
    def analyze_command_context(self, command):
        """Analyze command and provide context-aware insights"""
        if not self.ai_available:
            return None
        
        try:
            prompt = f"""{self.system_prompt}

Analyze this user command: "{command}"

Provide:
1. A brief understanding of what the user wants
2. Any potential context or assumptions
3. Proactive suggestions for related actions

Be brief and helpful."""
            
            response = self.chat.send_message(prompt)
            return response.text
        except:
            return None
    
    def save_preferences(self, filepath="vatsal_memory.json"):
        """Save conversation history and preferences"""
        data = {
            'conversation_history': self.conversation_history,
            'user_preferences': self.user_preferences,
            'context_memory': self.context_memory
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Could not save memory: {e}")
    
    def load_preferences(self, filepath="vatsal_memory.json"):
        """Load conversation history and preferences"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('conversation_history', [])
                    self.user_preferences = data.get('user_preferences', {})
                    self.context_memory = data.get('context_memory', {})
        except Exception as e:
            print(f"Could not load memory: {e}")


def create_vatsal_assistant():
    """Factory function to create VATSAL assistant"""
    return VatsalAssistant()
