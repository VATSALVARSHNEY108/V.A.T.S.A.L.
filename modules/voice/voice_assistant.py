"""
Voice Assistant Module
Voice commands for hands-free automation control
"""

import speech_recognition as sr
import pyttsx3
import threading
import re
from datetime import datetime, timedelta
from difflib import SequenceMatcher

class VoiceAssistant:
    def __init__(self, command_callback=None):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.command_callback = command_callback
        self.listening = False
        self.wake_word_enabled = True
        # Simple and easy wake words for quick activation
        self.wake_words = ["hello", "open", "search", "oye", "bhai", "bhaiya", "bhaisahb"]
        # Action verbs that should be kept in the command
        self.action_wake_words = ["open", "search"]
        
        # Phonetic variations and hints for ultra-fast "bhai" detection
        self.bhai_variations = [
            "bhai", "bhaiya", "bhaisahb", "by", "bye", "buy", 
            "bha", "bhay", "bae", "bi", "b", "vai", "why"
        ]
        
        # ULTRA sensitivity settings for instant "bhai" detection
        self.recognizer.energy_threshold = 100  # ULTRA LOW = maximum sensitivity
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust to ambient noise
        self.recognizer.dynamic_energy_adjustment_damping = 0.08  # VERY fast adaptation
        self.recognizer.dynamic_energy_ratio = 1.05  # Detect even slightest sound
        self.recognizer.pause_threshold = 0.3  # VERY short pause for instant response
        self.recognizer.operation_timeout = None  # No timeout for constant listening
        
        # Get all available voices
        self.available_voices = self.engine.getProperty('voices')
        self.current_voice_type = "male"  # Default (male voice)
        
        # Set male voice (index 0 is usually male)
        if len(self.available_voices) > 0:
            self.engine.setProperty('voice', self.available_voices[0].id)
        
        # Voice settings
        self.engine.setProperty('rate', 150)  # Normal speaking rate
        self.engine.setProperty('volume', 0.9)
        
        # Voice presets for easy switching
        self.voice_presets = {
            "male": {"index": 0, "rate": 150, "pitch": 1.0},
            "female": {"index": 1, "rate": 150, "pitch": 1.0},
            "modi": {"index": 0, "rate": 140, "pitch": 0.7},  # Deep, authoritative voice
            "kid": {"index": 1, "rate": 220, "pitch": 1.8},
            "fast": {"index": 1, "rate": 250, "pitch": 1.2},
            "slow": {"index": 0, "rate": 100, "pitch": 0.8},
            "robot": {"index": 0, "rate": 180, "pitch": 0.5},
            "chipmunk": {"index": 1, "rate": 300, "pitch": 2.0},
            "deep": {"index": 0, "rate": 120, "pitch": 0.6},
            "funny": {"index": 1, "rate": 200, "pitch": 1.5}
        }
        
        # ==================== INTELLIGENT FEATURES ====================
        # Conversation context and memory
        self.conversation_history = []
        self.last_command = None
        self.last_command_time = None
        self.context = {}
        
        # Intent synonyms for natural language understanding
        self.intent_synonyms = {
            "open": ["open", "launch", "start", "run", "execute", "fire up", "bring up", "load"],
            "close": ["close", "quit", "exit", "shut", "kill", "terminate", "end"],
            "search": ["search", "find", "look for", "google", "lookup", "query", "seek"],
            "play": ["play", "start playing", "put on", "listen to", "stream"],
            "stop": ["stop", "pause", "halt", "freeze", "cancel"],
            "increase": ["increase", "raise", "boost", "turn up", "make louder", "enhance"],
            "decrease": ["decrease", "lower", "reduce", "turn down", "make quieter", "diminish"],
            "create": ["create", "make", "generate", "build", "new", "add"],
            "delete": ["delete", "remove", "erase", "clear", "destroy", "trash"],
            "tell": ["tell me", "what is", "what's", "give me", "show me", "display"],
        }
        
        # Entity extraction patterns
        self.number_words = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
            "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000
        }
        
        # Common command patterns
        self.learned_patterns = {}
        self.command_count = {}
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Speech failed: {str(e)}")
    
    def listen_once(self):
        """Listen for a single voice command"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                # Quick ambient noise adjustment for faster response
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                # Increased timeout and phrase limit for better detection
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
                
                print("🔄 Processing...")
                command = self.recognizer.recognize_google(audio)
                print(f"✅ Heard: {command}")
                
                return command
        except sr.WaitTimeoutError:
            return "❌ No speech detected"
        except sr.UnknownValueError:
            return "❌ Could not understand audio"
        except sr.RequestError as e:
            return f"❌ Recognition service error: {str(e)}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def check_for_wake_word(self, text):
        """Check if the text starts with any wake word - ULTRA FAST for 'bhai' detection"""
        text_lower = text.lower().strip()
        words = text_lower.split()
        
        # INSTANT ACTIVATION: Check for ANY "bhai" variation (even hints!)
        # This catches "bhai", "bha", "bye", "by", etc.
        for variation in self.bhai_variations:
            if variation in text_lower:
                return True
        
        # Check if the first word matches any wake word
        if words and words[0] in self.wake_words:
            return True
        
        # Also check for wake word at the very beginning (for short phrases)
        for wake_word in self.wake_words:
            # Check if text starts with wake word followed by space or is exactly the wake word
            if text_lower == wake_word or text_lower.startswith(wake_word + " "):
                return True
        
        # Fuzzy matching for partial sounds
        if words:
            first_word = words[0]
            # Check if first word is similar to any wake word (partial match)
            for wake_word in self.wake_words:
                if len(first_word) >= 2 and (
                    wake_word.startswith(first_word) or 
                    first_word in wake_word or
                    self._sounds_similar(first_word, wake_word)
                ):
                    return True
        
        return False
    
    def _sounds_similar(self, word1, word2):
        """Check if two words sound similar (simple phonetic matching)"""
        # Quick phonetic similarity check
        if len(word1) < 2 or len(word2) < 2:
            return False
        
        # Check if they share at least 2 characters in sequence
        for i in range(len(word1) - 1):
            if word1[i:i+2] in word2:
                return True
        return False
    
    def listen_continuous(self):
        """Listen continuously for voice commands with wake word detection"""
        self.listening = True
        
        def listen_thread():
            with sr.Microphone() as source:
                if self.wake_word_enabled:
                    wake_words_str = ", ".join(self.wake_words)
                    print(f"🎤 Voice assistant started! Say wake word ({wake_words_str}) followed by your command")
                    print("   Or say 'stop listening' to quit")
                else:
                    print("🎤 Voice assistant started (say 'stop listening' to quit)")
                
                # ULTRA QUICK calibration for instant startup
                print("📊 Calibrating microphone (ULTRA FAST mode)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print("✅ Ready! Listening... (Say 'bhai' or any hint of it to activate!)")
                waiting_for_wake_word = self.wake_word_enabled
                
                while self.listening:
                    try:
                        # ULTRA FAST: Very short timeout and phrase limit for instant "bhai" detection
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        command = self.recognizer.recognize_google(audio)
                        command_lower = command.lower()
                        
                        if "stop listening" in command_lower:
                            self.listening = False
                            self.speak("Stopping voice assistant")
                            print("👋 Voice assistant stopped")
                            break
                        
                        if self.wake_word_enabled:
                            if waiting_for_wake_word:
                                if self.check_for_wake_word(command):
                                    # Extract command from the same phrase if present
                                    command_parts = command.lower().strip().split(None, 1)
                                    wake_word_used = command_parts[0] if command_parts else ""
                                    
                                    # Check if there's a command after the wake word
                                    if len(command_parts) > 1:
                                        # Wake word + command in same phrase
                                        # If wake word is an action verb, keep it in the command
                                        if wake_word_used in self.action_wake_words:
                                            # Keep the full phrase (e.g., "open chrome" stays as "open chrome")
                                            actual_command = command.lower().strip()
                                        else:
                                            # Remove non-action wake word (e.g., "hello open chrome" → "open chrome")
                                            actual_command = command_parts[1]
                                        
                                        print(f"👂 Wake word detected with command: {actual_command}")
                                        self.speak("Ji")
                                        
                                        # Process the command immediately
                                        if self.command_callback:
                                            response = self.command_callback(actual_command)
                                            if response:
                                                self.speak(response)
                                            else:
                                                self.speak("Samajh nahi aaya")
                                        waiting_for_wake_word = True  # Reset for next command
                                    else:
                                        # Wake word only, wait for command
                                        print(f"👂 Wake word detected! Listening for command...")
                                        self.speak("Ji, kaho")
                                        waiting_for_wake_word = False
                                else:
                                    continue
                            else:
                                # Already activated, process command
                                print(f"✅ Command: {command}")
                                waiting_for_wake_word = True
                                
                                if self.command_callback:
                                    response = self.command_callback(command)
                                    if response:
                                        self.speak(response)
                                    else:
                                        self.speak("Samajh nahi aaya. Phir se kaho")
                        else:
                            print(f"✅ Command: {command}")
                            if self.command_callback:
                                response = self.command_callback(command)
                                if response:
                                    self.speak(response)
                                    
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        if not waiting_for_wake_word:
                            waiting_for_wake_word = True
                        continue
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")
                        if not waiting_for_wake_word:
                            waiting_for_wake_word = True
                        continue
        
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
        return "✅ Voice assistant started"
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.listening = False
        return "✅ Voice assistant stopped"
    
    def add_wake_word(self, wake_word):
        """Add a custom wake word"""
        if wake_word.lower() not in self.wake_words:
            self.wake_words.append(wake_word.lower())
            return f"✅ Wake word '{wake_word}' added"
        return f"⚠️ Wake word '{wake_word}' already exists"
    
    def remove_wake_word(self, wake_word):
        """Remove a wake word"""
        if wake_word.lower() in self.wake_words:
            self.wake_words.remove(wake_word.lower())
            return f"✅ Wake word '{wake_word}' removed"
        return f"⚠️ Wake word '{wake_word}' not found"
    
    def enable_wake_word(self):
        """Enable wake word detection"""
        self.wake_word_enabled = True
        return "✅ Wake word detection enabled"
    
    def disable_wake_word(self):
        """Disable wake word detection"""
        self.wake_word_enabled = False
        return "✅ Wake word detection disabled"
    
    def get_wake_words(self):
        """Get list of current wake words"""
        return self.wake_words
    
    def set_sensitivity(self, level="high"):
        """
        Set microphone sensitivity level
        
        Args:
            level: "low", "medium", "high", or "ultra"
        """
        if level == "low":
            self.recognizer.energy_threshold = 2000
            self.recognizer.pause_threshold = 1.0
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 2.0  # Higher ratio = less sensitive
            self.recognizer.dynamic_energy_adjustment_damping = 0.25
            return "✅ Sensitivity set to LOW (fewer false triggers)"
        elif level == "medium":
            self.recognizer.energy_threshold = 1000
            self.recognizer.pause_threshold = 0.8
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 1.5
            self.recognizer.dynamic_energy_adjustment_damping = 0.20
            return "✅ Sensitivity set to MEDIUM (balanced)"
        elif level == "high":
            self.recognizer.energy_threshold = 300
            self.recognizer.pause_threshold = 0.5
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 1.2
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            return "✅ Sensitivity set to HIGH (very responsive)"
        elif level == "ultra":
            self.recognizer.energy_threshold = 100
            self.recognizer.pause_threshold = 0.3
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_ratio = 1.1
            self.recognizer.dynamic_energy_adjustment_damping = 0.10
            return "✅ Sensitivity set to ULTRA HIGH (maximum sensitivity)"
        else:
            return "❌ Invalid level. Use: low, medium, high, or ultra"
    
    def get_sensitivity_info(self):
        """Get current sensitivity settings"""
        return f"""
🎚️ Current Sensitivity Settings:
  • Energy Threshold: {self.recognizer.energy_threshold}
  • Pause Threshold: {self.recognizer.pause_threshold}
  • Dynamic Adjustment: {self.recognizer.dynamic_energy_threshold}
  • Dynamic Damping: {self.recognizer.dynamic_energy_adjustment_damping}
  • Dynamic Ratio: {self.recognizer.dynamic_energy_ratio}
"""
    
    def list_voices(self):
        """List all available voices"""
        voice_info = "🎤 Available Voices:\n\n"
        for i, voice in enumerate(self.available_voices):
            voice_info += f"{i}. {voice.name}\n"
            voice_info += f"   ID: {voice.id}\n"
            voice_info += f"   Languages: {voice.languages}\n\n"
        return voice_info
    
    def change_voice(self, voice_type="female"):
        """Change voice to different styles"""
        voice_type = voice_type.lower()
        
        if voice_type in self.voice_presets:
            preset = self.voice_presets[voice_type]
            
            # Set voice by index (with bounds checking)
            voice_index = min(preset["index"], len(self.available_voices) - 1)
            self.engine.setProperty('voice', self.available_voices[voice_index].id)
            
            # Set speaking rate
            self.engine.setProperty('rate', preset["rate"])
            
            # Note: Pitch control is not directly supported in pyttsx3
            # But we can simulate it with rate changes
            
            self.current_voice_type = voice_type
            
            return f"✅ Voice changed to {voice_type.upper()} mode!"
        
        # Try to find voice by name/type in available voices
        for i, voice in enumerate(self.available_voices):
            if voice_type in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                self.current_voice_type = voice_type
                return f"✅ Voice changed to: {voice.name}"
        
        return f"❌ Voice type '{voice_type}' not found. Available: {', '.join(self.voice_presets.keys())}"
    
    def get_current_voice(self):
        """Get information about current voice"""
        current = self.engine.getProperty('voice')
        rate = self.engine.getProperty('rate')
        volume = self.engine.getProperty('volume')
        
        for voice in self.available_voices:
            if voice.id == current:
                return f"""
🎤 Current Voice Settings:
  • Type: {self.current_voice_type.upper()}
  • Name: {voice.name}
  • Rate: {rate} words/min
  • Volume: {int(volume * 100)}%
"""
        return "Current voice information not available"
    
    def set_voice_speed(self, speed="normal"):
        """Change voice speaking speed"""
        speed_map = {
            "very slow": 80,
            "slow": 120,
            "normal": 150,
            "fast": 200,
            "very fast": 250,
            "super fast": 300
        }
        
        if speed in speed_map:
            self.engine.setProperty('rate', speed_map[speed])
            return f"✅ Voice speed set to {speed.upper()} ({speed_map[speed]} wpm)"
        
        return f"❌ Invalid speed. Options: {', '.join(speed_map.keys())}"
    
    def set_voice_volume(self, volume_percent=90):
        """Set voice volume (0-100)"""
        try:
            volume = max(0, min(100, int(volume_percent))) / 100
            self.engine.setProperty('volume', volume)
            return f"✅ Voice volume set to {int(volume * 100)}%"
        except:
            return "❌ Invalid volume value"
    
    # ==================== INTELLIGENT NLP METHODS ====================
    
    def extract_numbers(self, text):
        """Extract numbers from text (both digits and words)"""
        numbers = []
        
        # Extract digit numbers
        digit_matches = re.findall(r'\d+', text)
        numbers.extend([int(n) for n in digit_matches])
        
        # Extract word numbers
        words = text.lower().split()
        for word in words:
            if word in self.number_words:
                numbers.append(self.number_words[word])
        
        return numbers
    
    def extract_time(self, text):
        """Extract time from natural language"""
        # Match patterns like "at 3pm", "3:30", "fifteen minutes"
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(am|pm)?',
            r'(\d{1,2})\s*(am|pm)',
            r'in\s+(\d+)\s+(minute|hour|second)',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(0)
        
        return None
    
    def normalize_intent(self, command):
        """Normalize command to standard intent using synonyms"""
        command_lower = command.lower()
        
        for intent, synonyms in self.intent_synonyms.items():
            for synonym in synonyms:
                if synonym in command_lower:
                    # Replace synonym with standard intent
                    command_lower = command_lower.replace(synonym, intent)
                    break
        
        return command_lower
    
    def similarity_score(self, a, b):
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def find_best_match(self, command, possible_commands, threshold=0.6):
        """Find best matching command from possibilities using fuzzy matching"""
        best_match = None
        best_score = 0
        
        for possible in possible_commands:
            score = self.similarity_score(command, possible)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = possible
        
        return best_match, best_score
    
    def extract_app_name(self, command):
        """Intelligently extract application name from command"""
        # Common app keywords
        apps = [
            "chrome", "firefox", "edge", "browser",
            "notepad", "word", "excel", "powerpoint",
            "calculator", "calc", "calendar",
            "spotify", "music", "player",
            "explorer", "files", "folder",
            "terminal", "cmd", "powershell",
            "settings", "control panel",
            "paint", "photos", "camera"
        ]
        
        command_lower = command.lower()
        
        # Try exact match
        for app in apps:
            if app in command_lower:
                return app
        
        # Try fuzzy match
        words = command_lower.split()
        for word in words:
            for app in apps:
                if self.similarity_score(word, app) > 0.8:
                    return app
        
        # Extract quoted app names
        quoted = re.findall(r'"([^"]*)"', command)
        if quoted:
            return quoted[0]
        
        return None
    
    def understand_context(self, command):
        """Add context awareness to commands"""
        # Skip if this is an explicit repeat command (handled separately)
        if "repeat" in command.lower() and ("last" in command.lower() or "that" in command.lower()):
            return None  # Let regular command processing handle it
        
        # Check if command refers to previous action
        context_words = ["that", "it", "this", "again", "same", "more"]
        
        if any(word in command.lower() for word in context_words):
            if self.last_command:
                # Command is referring to previous action
                return f"context_repeat|{self.last_command}"
        
        return None
    
    def learn_from_command(self, command, intent):
        """Learn user's command patterns"""
        # Track command frequency
        if intent not in self.command_count:
            self.command_count[intent] = 0
        self.command_count[intent] += 1
        
        # Store command pattern
        if intent not in self.learned_patterns:
            self.learned_patterns[intent] = []
        
        if command not in self.learned_patterns[intent]:
            self.learned_patterns[intent].append(command)
        
        # Update context
        self.last_command = intent
        self.last_command_time = datetime.now()
        self.conversation_history.append({
            "command": command,
            "intent": intent,
            "timestamp": datetime.now()
        })
        
        # Keep only last 20 commands in history
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_smart_suggestions(self):
        """Get suggestions based on learned patterns"""
        if not self.command_count:
            return "No usage history yet"
        
        # Get top 5 most used commands
        sorted_commands = sorted(self.command_count.items(), key=lambda x: x[1], reverse=True)
        top_commands = sorted_commands[:5]
        
        suggestions = "🧠 Your most used commands:\n"
        for cmd, count in top_commands:
            suggestions += f"  • {cmd} ({count} times)\n"
        
        return suggestions
    
    def intelligent_parse(self, command):
        """Enhanced intelligent command parsing with NLP"""
        original_command = command
        command = command.lower().strip()
        
        # Check context first
        context_result = self.understand_context(command)
        if context_result:
            return context_result
        
        # Normalize synonyms
        normalized = self.normalize_intent(command)
        
        # Extract entities
        numbers = self.extract_numbers(command)
        time_info = self.extract_time(command)
        app_name = self.extract_app_name(command)
        
        # Store extracted info in context
        self.context = {
            "numbers": numbers,
            "time": time_info,
            "app": app_name,
            "original": original_command,
            "normalized": normalized
        }
        
        # Natural language patterns for common intents
        
        # Volume/brightness control with natural language
        if any(word in command for word in ["louder", "quieter", "brighter", "dimmer", "volume", "sound"]):
            if "louder" in command or ("turn up" in command and "sound" in command):
                return "volume_up"
            elif "quieter" in command or ("turn down" in command and "sound" in command):
                return "volume_down"
            elif "brighter" in command or ("turn up" in command and "bright" in command):
                return "brightness_up"
            elif "dimmer" in command or ("turn down" in command and "bright" in command):
                return "brightness_down"
            elif "volume" in command or "sound" in command:
                if "up" in command or "increase" in command or "raise" in command or "louder" in command:
                    return "volume_up"
                elif "down" in command or "decrease" in command or "lower" in command or "quieter" in command:
                    return "volume_down"
        
        # Smart app opening with various phrasings
        if app_name and any(word in normalized for word in ["open", "launch", "start", "run"]):
            return f"open_app|{app_name}"
        
        # Timer/reminder with natural language
        if "remind me" in command or "reminder" in command:
            if time_info:
                return f"set_reminder|{time_info}|{command}"
            if numbers:
                return f"set_reminder|{numbers[0]} minutes|{command}"
        
        if "timer" in command or "alarm" in command:
            if numbers:
                return f"set_timer|{numbers[0]}"
        
        # Math with natural language
        math_patterns = [
            (r"what is (\d+) (\+|\-|\*|\/|plus|minus|times|divided by) (\d+)", "calculate"),
            (r"calculate (\d+) (\+|\-|\*|\/|plus|minus|times|divided by) (\d+)", "calculate"),
        ]
        
        for pattern, intent in math_patterns:
            if re.search(pattern, command):
                return f"{intent}|{command}"
        
        # Continue with regular command processing
        return None
    
    def process_voice_command(self, command):
        """Process and execute voice commands - ULTRA INTELLIGENT with NLP!"""
        original_command = command
        command = command.lower().strip()
        
        # ==================== INTELLIGENT PRE-PROCESSING ====================
        # Try intelligent parsing first
        intelligent_result = self.intelligent_parse(command)
        if intelligent_result:
            # Learn from this command
            self.learn_from_command(original_command, intelligent_result.split('|')[0])
            return intelligent_result
        
        # ==================== PRODUCTIVITY (check first to avoid conflicts) ====================
        if "timer" in command:
            if "start" in command or "set" in command:
                return "start_timer"
            elif "stop" in command or "cancel" in command:
                return "stop_timer"
        
        elif "stopwatch" in command:
            if "start" in command:
                return "start_stopwatch"
            elif "stop" in command:
                return "stop_stopwatch"
        
        elif "focus mode" in command or "do not disturb" in command:
            if "enable" in command or "on" in command or "start" in command:
                return "focus_mode_on"
            else:
                return "focus_mode_off"
        
        # ==================== TIME & DATE ====================
        elif any(word in command for word in ["time", "clock"]) and "timer" not in command:
            return "get_time"
        
        elif any(word in command for word in ["date", "today"]):
            return "get_date"
        
        elif "day" in command and "is" in command:
            return "get_day"
        
        # ==================== WEATHER ====================
        elif "weather" in command:
            if "forecast" in command or "tomorrow" in command:
                return "weather_forecast"
            else:
                city = command.replace("weather", "").replace("in", "").strip()
                return f"weather|{city}" if city else "weather"
        
        # ==================== CALCULATOR ====================
        elif "calculate" in command or "compute" in command:
            expr = command.replace("calculate", "").replace("compute", "").strip()
            return f"calculate|{expr}"
        
        elif "plus" in command or "minus" in command or "times" in command or "divided by" in command:
            return f"calculate|{command}"
        
        # ==================== NOTES & REMINDERS ====================
        elif "note" in command or "write this" in command:
            if "create" in command or "add" in command or "make" in command:
                note_text = command.replace("create", "").replace("add", "").replace("make", "").replace("note", "").strip()
                return f"create_note|{note_text}"
            elif "show" in command or "list" in command or "read" in command:
                return "list_notes"
            elif "delete" in command or "remove" in command:
                return "delete_note"
        
        elif "remind me" in command or "reminder" in command or "set alarm" in command:
            reminder_text = command.replace("remind me", "").replace("reminder", "").replace("set alarm", "").strip()
            return f"create_reminder|{reminder_text}"
        
        # ==================== CLIPBOARD ====================
        elif "copy" in command and "clipboard" in command:
            text = command.replace("copy", "").replace("clipboard", "").strip()
            return f"copy_to_clipboard|{text}"
        
        elif "paste" in command or "clipboard" in command:
            return "paste_from_clipboard"
        
        # ==================== INTELLIGENT FEATURES (PRIORITY - check before clipboard) ====================
        # Check clear history first (before clipboard clear)
        elif "clear history" in command or ("forget" in command and "history" in command):
            # Clear the history
            self.conversation_history = []
            self.command_count = {}
            self.learned_patterns = {}
            self.last_command = None
            return "clear_history"
        
        elif "clear clipboard" in command:
            return "clear_clipboard"
        
        # ==================== SEARCH ====================
        elif any(keyword in command for keyword in ["search", "google", "find information", "look for", "lookup"]) and not "open" in command:
            query = command.strip()
            # Remove search keywords intelligently
            for keyword in ["search for", "search", "google", "find information about", "find", "look for", "lookup", "for "]:
                query = query.replace(keyword, "")
            
            query = query.strip()
            return f"web_search|{query}" if query else "web_search"
        
        # ==================== APPS & PROGRAMS ====================
        elif "open" in command:
            if "project folder" in command or "folder" in command:
                return "open_folder|."
            elif "chrome" in command or "browser" in command:
                return "open_app|chrome"
            elif "notepad" in command:
                return "open_app|notepad"
            elif "calculator" in command:
                return "open_app|calc"
            elif "paint" in command:
                return "open_app|mspaint"
            elif "word" in command:
                return "open_app|winword"
            elif "excel" in command:
                return "open_app|excel"
            elif "powerpoint" in command:
                return "open_app|powerpnt"
            elif "vscode" in command or "vs code" in command or "code" in command:
                return "open_app|code"
            elif "spotify" in command:
                return "open_app|spotify"
            elif "whatsapp" in command:
                return "open_app|whatsapp"
            elif "telegram" in command:
                return "open_app|telegram"
            elif "discord" in command:
                return "open_app|discord"
            elif "youtube" in command:
                return "open_url|https://youtube.com"
            elif "gmail" in command or "email" in command:
                return "open_url|https://gmail.com"
            elif "twitter" in command:
                return "open_url|https://twitter.com"
            elif "facebook" in command:
                return "open_url|https://facebook.com"
            elif "instagram" in command:
                return "open_url|https://instagram.com"
        
        elif "close" in command:
            if "window" in command or "app" in command or "this" in command:
                return "close_window"
        
        # ==================== MUSIC & MEDIA ====================
        elif "play" in command:
            if "spotify" in command:
                song = command.replace("play", "").replace("spotify", "").replace("on", "").strip()
                return f"play_spotify|{song}"
            elif "youtube" in command:
                song = command.replace("play", "").replace("youtube", "").replace("on", "").strip()
                return f"play_youtube|{song}"
            elif "lofi" in command or "beats" in command:
                return "play_music|lofi beats"
            else:
                song = command.replace("play", "").strip()
                return f"play_music|{song}"
        
        elif "pause" in command or "stop music" in command:
            return "pause_music"
        
        elif "next song" in command or "skip" in command:
            return "next_song"
        
        elif "previous song" in command:
            return "previous_song"
        
        # ==================== COMMUNICATION ====================
        elif "send email" in command or "email" in command:
            return "send_email|" + command
        
        elif "whatsapp" in command or "message" in command:
            if "send" in command:
                return "send_whatsapp|" + command
        
        # ==================== SYSTEM CONTROL ====================
        elif "screenshot" in command or "take a picture" in command or "capture screen" in command:
            return "screenshot"
        
        elif "brightness" in command:
            if "increase" in command or "up" in command or "higher" in command:
                return "brightness|80"
            elif "decrease" in command or "down" in command or "lower" in command:
                return "brightness|30"
            elif "max" in command or "full" in command:
                return "brightness|100"
            elif "min" in command:
                return "brightness|10"
        
        elif "volume" in command:
            if "mute" in command:
                return "mute"
            elif "unmute" in command:
                return "unmute"
            elif "up" in command or "increase" in command:
                return "volume_up"
            elif "down" in command or "decrease" in command:
                return "volume_down"
            elif "max" in command or "full" in command:
                return "volume_max"
        
        elif "shutdown" in command or "shut down" in command:
            return "shutdown"
        
        elif "restart" in command or "reboot" in command:
            return "restart"
        
        elif "sleep" in command or "hibernate" in command:
            if "cancel" in command:
                return "cancel_sleep"
            else:
                return "sleep"
        
        elif "lock" in command and ("screen" in command or "computer" in command):
            return "lock_screen"
        
        elif "log out" in command or "logout" in command or "sign out" in command:
            return "logout"
        
        # ==================== WINDOW MANAGEMENT ====================
        elif "minimize" in command:
            if "all" in command:
                return "minimize_all"
            else:
                return "minimize_window"
        
        elif "maximize" in command:
            return "maximize_window"
        
        elif "switch window" in command or "switch app" in command:
            return "switch_window"
        
        elif "show desktop" in command:
            return "show_desktop"
        
        # ==================== FILE OPERATIONS ====================
        elif "organize" in command and "downloads" in command:
            return "organize_downloads"
        
        elif "clean" in command or "clear" in command:
            if "temp" in command or "temporary" in command:
                return "clear_temp"
            elif "trash" in command or "recycle" in command:
                return "empty_trash"
            elif "cache" in command:
                return "clear_cache"
        
        elif "empty" in command and ("trash" in command or "recycle" in command):
            return "empty_trash"
        
        elif "disk space" in command or "storage" in command:
            return "check_disk_space"
        
        
        # ==================== INFORMATION ====================
        elif "system" in command:
            if "report" in command or "info" in command or "information" in command:
                return "system_report"
            elif "usage" in command or "performance" in command:
                return "system_usage"
        
        elif "battery" in command:
            return "battery_status"
        
        elif "wifi" in command or "network" in command:
            if "password" in command or "pass" in command:
                return "wifi_password"
            else:
                return "network_status"
        
        # ==================== FUN FEATURES (check before IP to avoid conflicts) ====================
        elif ("flip" in command and "coin" in command) or "coin flip" in command:
            return "flip_coin"
        
        elif "joke" in command or ("funny" in command and "voice" not in command and "change" not in command):
            return "tell_joke"
        
        elif "quote" in command or "motivation" in command or "inspire" in command:
            return "motivational_quote"
        
        elif "ip address" in command or (command.endswith("ip") or command.startswith("ip ") or " ip" in command):
            return "get_ip"
        
        elif ("roll" in command and "dice" in command) or "dice" in command:
            return "roll_dice"
        
        elif "random number" in command:
            return "random_number"
        
        # ==================== TRANSLATION ====================
        elif "translate" in command:
            return "translate|" + command
        
        # ==================== NEWS ====================
        elif "news" in command:
            if "tech" in command or "technology" in command:
                return "news|technology"
            elif "sports" in command:
                return "news|sports"
            elif "business" in command:
                return "news|business"
            else:
                return "news|general"
        
        # ==================== VOICE CONTROL ====================
        elif "change voice" in command or "switch voice" in command:
            if "male" in command:
                return "change_voice|male"
            elif "female" in command:
                return "change_voice|female"
            elif "robot" in command:
                return "change_voice|robot"
            elif "chipmunk" in command:
                return "change_voice|chipmunk"
            elif "deep" in command:
                return "change_voice|deep"
            elif "funny" in command or "fun" in command:
                return "change_voice|funny"
            elif "fast" in command:
                return "change_voice|fast"
            elif "slow" in command:
                return "change_voice|slow"
            else:
                return "change_voice|female"
        
        elif "speak" in command and ("faster" in command or "slower" in command or "speed" in command):
            if "faster" in command or "fast" in command:
                return "voice_speed|fast"
            elif "slower" in command or "slow" in command:
                return "voice_speed|slow"
            elif "very fast" in command or "super fast" in command:
                return "voice_speed|very fast"
            elif "very slow" in command:
                return "voice_speed|very slow"
            else:
                return "voice_speed|normal"
        
        elif "list voices" in command or "show voices" in command or "available voices" in command:
            return "list_voices"
        
        elif "current voice" in command or "voice info" in command:
            return "current_voice"
        
        # ==================== INTELLIGENT FEATURES ====================
        # Check repeat commands before history (to avoid conflict)
        elif ("repeat" in command or "do it again" in command) and not "context_repeat" in command:
            if "last" in command or "that" in command or "again" in command:
                return "repeat_last"
        
        elif "suggestions" in command or "what do i use" in command or "my habits" in command:
            return "show_suggestions"
        
        elif "history" in command or "conversation history" in command or "what did i say" in command:
            return "show_history"
        
        # ==================== HELP ====================
        elif "help" in command or "commands" in command or "what can you do" in command:
            return "show_help"
        
        # Learn from every command for future improvements
        self.learn_from_command(original_command, "unknown")
        
        return None

def create_voice_commands_list():
    """Return list of supported voice commands"""
    return """
🎤 MEGA VOICE COMMAND LIST - 50+ Commands! (ULTRA FAST SENSITIVITY)

Wake Words (say one of these first):
  Simple & Quick:
  • "Hello"
  • "Open"
  • "Search"
  
  Hindi (ULTRA FAST - even hints activate!):
  • "Bhai" ⚡ (Detects: bhai, bha, bye, by, etc.)
  • "Bhaiya"
  • "Bhaisahb"
  • "Oye"

Usage: Say wake word → Wait for "Ji, kaho" → Give your command

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ TIME & DATE:
  • "What time is it?"
  • "What's the date?"
  • "What day is today?"

🌤️ WEATHER:
  • "Weather" / "Weather in [city]"
  • "Weather forecast"
  • "Weather tomorrow"

🔢 CALCULATOR:
  • "Calculate 25 plus 37"
  • "Compute 100 divided by 4"
  • "50 times 3"

📝 NOTES & REMINDERS:
  • "Create note [text]"
  • "Make note [text]"
  • "List notes" / "Show notes"
  • "Remind me to [task]"
  • "Set alarm for [time]"

📋 CLIPBOARD:
  • "Copy to clipboard [text]"
  • "Paste from clipboard"
  • "Clear clipboard"

🔍 SEARCH & WEB:
  • "Search for [query]"
  • "Google [query]"
  • "Open YouTube"
  • "Open Gmail"
  • "Open Twitter/Facebook/Instagram"

💻 OPEN APPS:
  • "Open Chrome/Browser"
  • "Open Notepad"
  • "Open Calculator"
  • "Open Paint"
  • "Open Word/Excel/PowerPoint"
  • "Open VS Code"
  • "Open Spotify"
  • "Open WhatsApp/Telegram/Discord"

🪟 WINDOW MANAGEMENT:
  • "Close window"
  • "Minimize window"
  • "Maximize window"
  • "Minimize all"
  • "Switch window"
  • "Show desktop"

🎵 MUSIC & MEDIA:
  • "Play [song name]"
  • "Play lofi beats"
  • "Play [song] on Spotify"
  • "Play [song] on YouTube"
  • "Pause music" / "Stop music"
  • "Next song" / "Skip"
  • "Previous song"

💬 COMMUNICATION:
  • "Send email to [name]"
  • "Send WhatsApp message"

⚙️ SYSTEM CONTROL:
  • "Screenshot" / "Capture screen"
  • "Increase/Decrease brightness"
  • "Max brightness" / "Min brightness"
  • "Mute/Unmute volume"
  • "Volume up/down"
  • "Max volume"
  • "Shutdown"
  • "Restart/Reboot"
  • "Sleep/Hibernate"
  • "Cancel sleep"
  • "Lock screen"
  • "Log out/Sign out"

📁 FILE OPERATIONS:
  • "Organize downloads"
  • "Clear temp files"
  • "Empty trash/recycle bin"
  • "Clear cache"
  • "Check disk space"

⏱️ PRODUCTIVITY:
  • "Start timer"
  • "Stop timer"
  • "Start stopwatch"
  • "Stop stopwatch"
  • "Enable focus mode"
  • "Disable focus mode"

ℹ️ INFORMATION:
  • "System report"
  • "System usage/performance"
  • "Battery status"
  • "Network status"
  • "WiFi password"
  • "IP address"

🎲 FUN FEATURES:
  • "Tell a joke"
  • "Motivational quote"
  • "Flip a coin"
  • "Roll dice"
  • "Random number"

📰 NEWS:
  • "News" / "Latest news"
  • "Tech news"
  • "Sports news"
  • "Business news"

🌐 TRANSLATION:
  • "Translate [text]"

🎤 VOICE CONTROL:
  • "Change voice to male"
  • "Change voice to female"
  • "Change voice to robot"
  • "Change voice to chipmunk" 🐿️
  • "Change voice to deep"
  • "Change voice to funny"
  • "Speak faster"
  • "Speak slower"
  • "Speak very fast" / "Super fast"
  • "Speak very slow"
  • "List voices"
  • "Current voice"

🧠 INTELLIGENT FEATURES (NEW!):
  • "Show suggestions" - See your most used commands
  • "Show history" - View conversation history
  • "Repeat that" / "Do it again" - Repeat last command
  • "Clear history" - Clear conversation memory
  
  Natural Language Understanding:
  • "Make it louder" → Volume up
  • "Turn down the sound" → Volume down
  • "Launch calculator" → Open calculator
  • "Fire up Chrome" → Open Chrome
  • "Set timer for 5 minutes" → Timer with auto-detection
  • "Remind me in 10 minutes" → Smart reminder
  • "What is 25 plus 30?" → Calculator

❓ HELP:
  • "Help" / "Show commands"
  • "What can you do?"

🛑 STOP:
  • "Stop listening"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎚️ Sensitivity Levels:
  • LOW    - Fewer false triggers
  • MEDIUM - Balanced detection
  • HIGH   - Very responsive
  • ULTRA  - Maximum sensitivity (DEFAULT) ⭐

Example Usage:
  1. Say "Bhai" (or even "Bha") ⚡
  2. Wait for "Ji, kaho"
  3. Say "Open Chrome"
  4. Done! ✅

⚡ ULTRA FAST MODE: 50+ commands ready instantly!
  
Change sensitivity: assistant.set_sensitivity('ultra')
"""

if __name__ == "__main__":
    assistant = VoiceAssistant()
    print("Voice Assistant Module - Testing")
    print(create_voice_commands_list())
    
    print("\nSay something:")
    command = assistant.listen_once()
    print(f"Result: {command}")
