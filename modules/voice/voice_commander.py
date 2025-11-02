"""
Enhanced Voice Commander for VATSAL
Provides voice input and speech output for all VATSAL commands with human-like personality
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import random
from typing import Callable, Optional
from datetime import datetime
from voice_sounds import create_voice_sound_effects

class VoiceCommander:
    """Enhanced voice commanding with speech recognition and text-to-speech"""
    
    def __init__(self, command_callback: Optional[Callable] = None):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.command_callback = command_callback
        
        # Speech settings
        self.tts_engine.setProperty('rate', 165)
        self.tts_engine.setProperty('volume', 0.95)
        
        # Set male voice (index 0 is typically male)
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 0:
            self.tts_engine.setProperty('voice', voices[0].id)
        
        # Initialize sound effects for voice commanding
        try:
            self.sound_effects = create_voice_sound_effects()
            print("🔊 Voice sound effects ready!")
        except Exception as e:
            print(f"⚠️ Sound effects initialization failed: {e}")
            self.sound_effects = None
        
        # Recognition settings - HIGH SENSITIVITY for better wake word detection
        self.recognizer.energy_threshold = 300  # Lower = more sensitive (default is 4000)
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15  # Faster adaptation to noise
        self.recognizer.dynamic_energy_ratio = 1.2  # Lower threshold for speech detection
        self.recognizer.pause_threshold = 0.5  # Shorter pause (faster response)
        
        # State management
        self.continuous_listening = False
        self.listen_thread = None
        self.tts_queue = queue.Queue()
        self.tts_thread = None
        self.is_speaking = False
        
        # Wake word detection - support multiple wake phrases
        self.wake_words = ["vatsal", "hey vatsal", "ok vatsal", "bhai", "computer", "hey computer", "bhiaya", "bhaisahb"]
        self.wake_word_enabled = True  # Enabled by default
        self.wake_word = "vatsal"  # Primary wake word for display
        
        # Human-like response variations
        self._init_response_variations()
        
        # Advanced features
        self.command_history = []  # Track all commands
        self.max_history = 50  # Keep last 50 commands
        self.conversation_mode = False  # Multi-turn conversation without wake word
        self.conversation_timeout = 10  # Seconds before exiting conversation mode
        self.last_command_time = None
        self.voice_shortcuts = {}  # Custom voice macros
        self.context = {}  # Store context between commands
        
        # Start TTS worker thread
        self._start_tts_worker()
    
    def _init_response_variations(self):
        """Initialize human-like response variations for natural conversation"""
        self.responses = {
            'wake_acknowledgment': [
                "Ji, I am listening",
                "Yes, how can I help?",
                "I'm here, what do you need?",
                "At your service",
                "Ready, what's on your mind?",
                "Ji, kaho",
                "Yes sir, listening",
                "I'm all ears"
            ],
            'wake_with_command': [
                "Ji",
                "On it",
                "Right away",
                "Got it",
                "Sure thing",
                "Okay"
            ],
            'activation': [
                "Voice commanding activated. Ready to assist you",
                "Hello! Voice assistant is online",
                "I'm ready to help. Just say my name",
                "Voice system active. How may I assist?",
                "All systems online. At your service"
            ],
            'deactivation': [
                "Voice commanding deactivated. See you soon",
                "Going offline. Call me when you need me",
                "Signing off. Have a great day",
                "Voice assistant disabled. Until next time",
                "Standby mode activated"
            ],
            'error': [
                "Sorry, I didn't catch that",
                "Could you repeat that please?",
                "I didn't quite understand",
                "Pardon me, say that again?",
                "My apologies, I missed that"
            ],
            'greeting_morning': [
                "Good morning sir. Ready to make today productive",
                "Morning! Let's get things done today",
                "Good morning. What shall we accomplish?"
            ],
            'greeting_afternoon': [
                "Good afternoon. How can I assist you?",
                "Afternoon! Ready when you are",
                "Good afternoon sir. At your service"
            ],
            'greeting_evening': [
                "Good evening. Hope you had a productive day",
                "Evening! Still working hard I see",
                "Good evening sir. What can I do for you?"
            ],
            'greeting_night': [
                "Burning the midnight oil? I'm here to help",
                "Late night session. Let's get it done",
                "Good evening. Even at this hour, I'm ready"
            ]
        }
    
    def _get_random_response(self, category: str) -> str:
        """Get a random response from the specified category"""
        if category in self.responses:
            return random.choice(self.responses[category])
        return "Ready"
    
    def _get_time_based_greeting(self) -> str:
        """Get greeting based on current time of day"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return self._get_random_response('greeting_morning')
        elif 12 <= hour < 17:
            return self._get_random_response('greeting_afternoon')
        elif 17 <= hour < 22:
            return self._get_random_response('greeting_evening')
        else:
            return self._get_random_response('greeting_night')
    
    def _start_tts_worker(self):
        """Start background thread for text-to-speech"""
        def tts_worker():
            while True:
                try:
                    text = self.tts_queue.get()
                    if text is None:
                        break
                    
                    self.is_speaking = True
                    try:
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                        # Add delay after speaking to prevent microphone from hearing echo
                        time.sleep(0.8)
                    except Exception as e:
                        print(f"❌ TTS Error: {str(e)}")
                    finally:
                        self.is_speaking = False
                        # Additional safety delay after flag is cleared
                        time.sleep(0.2)
                        
                except Exception as e:
                    print(f"❌ TTS Worker Error: {str(e)}")
        
        self.tts_thread = threading.Thread(target=tts_worker, daemon=True)
        self.tts_thread.start()
    
    def speak(self, text: str, interrupt: bool = False):
        """Queue text for speech output"""
        if interrupt:
            # Clear the queue and speak immediately
            while not self.tts_queue.empty():
                try:
                    self.tts_queue.get_nowait()
                except queue.Empty:
                    break
        
        self.tts_queue.put(text)
    
    def listen_once(self, timeout: int = 5) -> dict:
        """
        Listen for a single voice command
        Returns: dict with 'success', 'command', and 'message'
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                print("🔄 Processing speech...")
                command = self.recognizer.recognize_google(audio)
                
                print(f"✅ Heard: {command}")
                return {
                    "success": True,
                    "command": command,
                    "message": f"Heard: {command}"
                }
                
        except sr.WaitTimeoutError:
            return {
                "success": False,
                "command": None,
                "message": "No speech detected (timeout)"
            }
        except sr.UnknownValueError:
            return {
                "success": False,
                "command": None,
                "message": "Could not understand audio"
            }
        except sr.RequestError as e:
            return {
                "success": False,
                "command": None,
                "message": f"Recognition service error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "command": None,
                "message": f"Error: {str(e)}"
            }
    
    def start_continuous_listening(self, callback: Optional[Callable] = None):
        """Start continuous voice command listening"""
        if self.continuous_listening:
            return {"success": False, "message": "Already listening"}
        
        if callback:
            self.command_callback = callback
        
        if not self.command_callback:
            return {"success": False, "message": "No command callback provided"}
        
        self.continuous_listening = True
        
        def listen_loop():
            """Continuous listening loop"""
            waiting_for_wake_word = True
            
            try:
                with sr.Microphone() as source:
                    print("🎤 Continuous listening started")
                    greeting = self._get_random_response('activation')
                    self.speak(greeting, interrupt=True)
                    
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                    while self.continuous_listening:
                        try:
                            # Don't listen while speaking
                            if self.is_speaking:
                                time.sleep(0.1)
                                continue
                            
                            # Small delay to ensure system's voice has finished playing
                            time.sleep(0.1)
                            
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                            
                            try:
                                command = self.recognizer.recognize_google(audio)
                                print(f"🎤 Heard: {command}")
                                
                                # Check for stop command
                                if any(phrase in command.lower() for phrase in ["stop listening", "stop voice", "disable voice"]):
                                    self.stop_continuous_listening()
                                    break
                                
                                # Check for wake word if enabled
                                if self.wake_word_enabled:
                                    if waiting_for_wake_word:
                                        # We're waiting for a wake word
                                        command_lower = command.lower().strip()
                                        wake_word_found = False
                                        wake_word_used = None
                                        remaining = ""
                                        
                                        # Check if any wake word is at the start
                                        for wake_word in self.wake_words:
                                            if command_lower.startswith(wake_word):
                                                wake_word_found = True
                                                wake_word_used = wake_word
                                                # Extract everything after the wake word
                                                remaining = command_lower[len(wake_word):].strip()
                                                break
                                        
                                        if wake_word_found:
                                            # Wake word detected! Play sound
                                            if self.sound_effects:
                                                self.sound_effects.play_sound('wake_word')
                                            
                                            if remaining:
                                                # There's a command right after the wake word
                                                print(f"✅ Wake word detected! Executing: {remaining}")
                                                acknowledgment = self._get_random_response('wake_with_command')
                                                self.speak(acknowledgment, interrupt=False)
                                                
                                                # Play processing sound
                                                if self.sound_effects:
                                                    self.sound_effects.play_sound('processing')
                                                
                                                # Execute command via callback with advanced features
                                                self._execute_advanced_command(remaining)
                                                
                                                # Play success sound
                                                if self.sound_effects:
                                                    self.sound_effects.play_sound('success')
                                                
                                                # Reset - wait for wake word again
                                                waiting_for_wake_word = True
                                            else:
                                                # Just the wake word, no command yet - enable conversation mode
                                                print(f"✅ Wake word detected! Entering conversation mode...")
                                                
                                                # Play listening sound
                                                if self.sound_effects:
                                                    self.sound_effects.play_sound('listening')
                                                
                                                listening_response = self._get_random_response('wake_acknowledgment')
                                                self.speak(listening_response, interrupt=False)
                                                waiting_for_wake_word = False
                                                # Enable conversation mode for easy follow-ups
                                                self.enable_conversation_mode(timeout=15)
                                        else:
                                            # No wake word found
                                            print(f"⏭️  Skipped (no wake word): {command}")
                                            continue
                                    else:
                                        # Already activated by wake word, this is the command
                                        print(f"✅ Executing command: {command}")
                                        
                                        # Play processing sound
                                        if self.sound_effects:
                                            self.sound_effects.play_sound('processing')
                                        
                                        # Execute command with advanced features
                                        self._execute_advanced_command(command.lower().strip())
                                        
                                        # Play success sound
                                        if self.sound_effects:
                                            self.sound_effects.play_sound('success')
                                        
                                        # Check conversation timeout
                                        if self.check_conversation_timeout():
                                            print("💬 Conversation mode timed out")
                                            waiting_for_wake_word = True
                                        else:
                                            # Stay in conversation mode if still active
                                            waiting_for_wake_word = not self.conversation_mode
                                else:
                                    # Wake word disabled, process all commands
                                    print(f"✅ Executing command: {command}")
                                    if command and command.strip():
                                        try:
                                            self.command_callback(command)
                                            print(f"✅ Command sent to callback successfully")
                                        except Exception as e:
                                            print(f"❌ Callback error: {str(e)}")
                                
                            except sr.UnknownValueError:
                                # Couldn't understand - play error sound
                                if self.sound_effects and not waiting_for_wake_word:
                                    self.sound_effects.play_sound('error')
                                # Reset if we were waiting for a command
                                if not waiting_for_wake_word:
                                    waiting_for_wake_word = True
                                continue
                            except sr.RequestError as e:
                                print(f"❌ Recognition error: {str(e)}")
                                # Play error sound
                                if self.sound_effects:
                                    self.sound_effects.play_sound('error')
                                time.sleep(1)
                                continue
                                
                        except sr.WaitTimeoutError:
                            continue
                        except Exception as e:
                            print(f"❌ Listen error: {str(e)}")
                            # Reset state on error
                            if not waiting_for_wake_word:
                                waiting_for_wake_word = True
                            continue
                            
            except Exception as e:
                print(f"❌ Microphone error: {str(e)}")
                self.continuous_listening = False
        
        self.listen_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listen_thread.start()
        
        return {"success": True, "message": "Continuous listening started"}
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        if not self.continuous_listening:
            return {"success": False, "message": "Not currently listening"}
        
        self.continuous_listening = False
        farewell = self._get_random_response('deactivation')
        self.speak(farewell, interrupt=True)
        
        return {"success": True, "message": "Continuous listening stopped"}
    
    def toggle_wake_word(self, enabled: bool = None) -> dict:
        """Toggle wake word detection"""
        if enabled is None:
            self.wake_word_enabled = not self.wake_word_enabled
        else:
            self.wake_word_enabled = enabled
        
        status = "enabled" if self.wake_word_enabled else "disabled"
        return {
            "success": True,
            "message": f"Wake word '{self.wake_word}' {status}",
            "enabled": self.wake_word_enabled
        }
    
    def set_wake_word(self, wake_word: str) -> dict:
        """Set custom wake word"""
        self.wake_word = wake_word.lower().strip()
        # Also add to wake words list if not present
        if self.wake_word not in self.wake_words:
            self.wake_words.append(self.wake_word)
        return {
            "success": True,
            "message": f"Wake word set to '{self.wake_word}'"
        }
    
    def add_wake_word(self, wake_word: str) -> dict:
        """Add an additional wake word"""
        wake_word = wake_word.lower().strip()
        if wake_word not in self.wake_words:
            self.wake_words.append(wake_word)
            return {
                "success": True,
                "message": f"Added wake word '{wake_word}'"
            }
        return {
            "success": False,
            "message": f"Wake word '{wake_word}' already exists"
        }
    
    def get_wake_words(self) -> list:
        """Get list of all wake words"""
        return self.wake_words.copy()
    
    def get_status(self) -> dict:
        """Get current voice commander status"""
        return {
            "listening": self.continuous_listening,
            "speaking": self.is_speaking,
            "wake_word_enabled": self.wake_word_enabled,
            "wake_word": self.wake_word,
            "wake_words": self.wake_words,
            "conversation_mode": self.conversation_mode,
            "command_history_count": len(self.command_history),
            "shortcuts_count": len(self.voice_shortcuts)
        }
    
    def add_to_history(self, command: str):
        """Add command to history"""
        import datetime
        self.command_history.append({
            'command': command,
            'timestamp': datetime.datetime.now().isoformat()
        })
        # Keep only last max_history commands
        if len(self.command_history) > self.max_history:
            self.command_history.pop(0)
        self.last_command_time = time.time()
    
    def get_command_history(self, limit: int = 10) -> list:
        """Get recent command history"""
        return self.command_history[-limit:]
    
    def clear_history(self):
        """Clear command history"""
        self.command_history = []
        return {"success": True, "message": "Command history cleared"}
    
    def add_voice_shortcut(self, trigger: str, commands: list) -> dict:
        """
        Add a voice shortcut/macro
        trigger: The phrase to trigger the shortcut
        commands: List of commands to execute
        """
        trigger = trigger.lower().strip()
        self.voice_shortcuts[trigger] = commands
        return {
            "success": True,
            "message": f"Voice shortcut '{trigger}' created with {len(commands)} commands"
        }
    
    def remove_voice_shortcut(self, trigger: str) -> dict:
        """Remove a voice shortcut"""
        trigger = trigger.lower().strip()
        if trigger in self.voice_shortcuts:
            del self.voice_shortcuts[trigger]
            return {"success": True, "message": f"Shortcut '{trigger}' removed"}
        return {"success": False, "message": f"Shortcut '{trigger}' not found"}
    
    def get_voice_shortcuts(self) -> dict:
        """Get all voice shortcuts"""
        return self.voice_shortcuts
    
    def enable_conversation_mode(self, timeout: int = 10):
        """
        Enable conversation mode - no wake word needed for follow-up commands
        timeout: Seconds before automatically exiting conversation mode
        """
        self.conversation_mode = True
        self.conversation_timeout = timeout
        self.last_command_time = time.time()
        return {
            "success": True,
            "message": f"Conversation mode enabled for {timeout} seconds"
        }
    
    def disable_conversation_mode(self):
        """Disable conversation mode"""
        self.conversation_mode = False
        return {"success": True, "message": "Conversation mode disabled"}
    
    def check_conversation_timeout(self):
        """Check if conversation mode should timeout"""
        if self.conversation_mode and self.last_command_time:
            if time.time() - self.last_command_time > self.conversation_timeout:
                self.conversation_mode = False
                return True
        return False
    
    def set_context(self, key: str, value):
        """Store context information"""
        self.context[key] = value
    
    def get_context(self, key: str, default=None):
        """Retrieve context information"""
        return self.context.get(key, default)
    
    def clear_context(self):
        """Clear all context"""
        self.context = {}
        return {"success": True, "message": "Context cleared"}
    
    def process_command_chain(self, command: str) -> list:
        """
        Process chained commands (separated by 'and then' or 'and')
        Returns list of individual commands
        """
        # Split by common chain separators
        separators = [' and then ', ' then ', ' and also ', ' after that ']
        commands = [command]
        
        for separator in separators:
            new_commands = []
            for cmd in commands:
                if separator in cmd.lower():
                    new_commands.extend(cmd.lower().split(separator))
                else:
                    new_commands.append(cmd)
            commands = new_commands
        
        # Clean up commands
        return [cmd.strip() for cmd in commands if cmd.strip()]
    
    def _execute_advanced_command(self, command: str):
        """
        Execute command with advanced features:
        - Check for voice shortcuts
        - Process command chains
        - Add to history
        - Execute via callback
        """
        command = command.strip()
        
        # Add to history
        self.add_to_history(command)
        
        # Check if this is a voice shortcut
        if command in self.voice_shortcuts:
            print(f"🔗 Voice shortcut detected: '{command}'")
            commands_to_execute = self.voice_shortcuts[command]
            self.speak(f"Executing shortcut with {len(commands_to_execute)} commands")
            
            for cmd in commands_to_execute:
                print(f"  ▶️ Shortcut command: {cmd}")
                try:
                    if self.command_callback:
                        self.command_callback(cmd)
                        time.sleep(0.5)  # Brief pause between chained commands
                except Exception as e:
                    print(f"❌ Callback error: {str(e)}")
            return
        
        # Check for command chaining
        chained_commands = self.process_command_chain(command)
        
        if len(chained_commands) > 1:
            print(f"🔗 Command chain detected: {len(chained_commands)} commands")
            self.speak(f"Executing {len(chained_commands)} commands")
            
            for i, cmd in enumerate(chained_commands, 1):
                print(f"  {i}. {cmd}")
                try:
                    if self.command_callback:
                        self.command_callback(cmd)
                        if i < len(chained_commands):
                            time.sleep(1)  # Pause between chained commands
                except Exception as e:
                    print(f"❌ Callback error on command {i}: {str(e)}")
        else:
            # Single command execution
            try:
                if self.command_callback:
                    self.command_callback(command)
                    print(f"✅ Command sent to callback successfully")
            except Exception as e:
                print(f"❌ Callback error: {str(e)}")
    
    def toggle_sound_effects(self) -> dict:
        """Toggle voice sound effects on/off"""
        if not self.sound_effects:
            return {"success": False, "message": "Sound effects not available"}
        
        result = self.sound_effects.toggle()
        return {"success": True, "message": result}
    
    def enable_sound_effects(self) -> dict:
        """Enable voice sound effects"""
        if not self.sound_effects:
            return {"success": False, "message": "Sound effects not available"}
        
        result = self.sound_effects.enable()
        return {"success": True, "message": result}
    
    def disable_sound_effects(self) -> dict:
        """Disable voice sound effects"""
        if not self.sound_effects:
            return {"success": False, "message": "Sound effects not available"}
        
        result = self.sound_effects.disable()
        return {"success": True, "message": result}
    
    def set_sound_volume(self, volume: float) -> dict:
        """Set sound effects volume (0.0 to 1.0)"""
        if not self.sound_effects:
            return {"success": False, "message": "Sound effects not available"}
        
        try:
            self.sound_effects.set_volume(volume)
            return {"success": True, "message": f"Sound volume set to {int(volume * 100)}%"}
        except Exception as e:
            return {"success": False, "message": f"Error setting volume: {str(e)}"}
    
    def add_custom_sound(self, sound_name: str, wav_file_path: str) -> dict:
        """Add a custom sound effect"""
        if not self.sound_effects:
            return {"success": False, "message": "Sound effects not available"}
        
        result = self.sound_effects.add_custom_sound(sound_name, wav_file_path)
        return {"success": True, "message": result}
    
    def list_sound_effects(self) -> dict:
        """List all available sound effects"""
        if not self.sound_effects:
            return {"success": False, "message": "Sound effects not available"}
        
        sounds = self.sound_effects.list_sounds()
        return {"success": True, "sounds": sounds}
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_continuous_listening()
        self.tts_queue.put(None)
        if self.tts_thread:
            self.tts_thread.join(timeout=2)
        if self.sound_effects:
            self.sound_effects.cleanup()


def create_voice_commander(command_callback: Optional[Callable] = None) -> VoiceCommander:
    """Factory function to create a VoiceCommander instance"""
    return VoiceCommander(command_callback)


if __name__ == "__main__":
    # Test the voice commander
    print("Testing Voice Commander")
    
    def test_callback(command):
        print(f"Executing command: {command}")
    
    commander = create_voice_commander(test_callback)
    
    print("\n1. Testing single listen:")
    result = commander.listen_once()
    print(f"Result: {result}")
    
    if result['success']:
        commander.speak(f"You said: {result['command']}")
    
    print("\n2. Testing text-to-speech:")
    commander.speak("Hello, I am VATSAL, your AI desktop automation assistant")
    
    time.sleep(3)
    
    print("\nVoice Commander test complete")
