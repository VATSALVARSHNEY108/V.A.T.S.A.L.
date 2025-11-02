"""
Dynamic WAV Sound Effects for Voice Commanding
Plays sound effects during voice command interactions
"""

import pygame
import threading
import os
from typing import Optional

class VoiceSoundEffects:
    """Manages sound effects for voice commanding"""
    
    def __init__(self, sounds_dir: str = "voice_sounds"):
        self.sounds_dir = sounds_dir
        self.enabled = True
        self.volume = 0.8  # Default volume (0.0 to 1.0)
        self._initialized = False
        self._lock = threading.Lock()
        
        # Create sounds directory if it doesn't exist
        os.makedirs(self.sounds_dir, exist_ok=True)
        
        # Sound file paths
        self.sound_files = {
            'wake_word': os.path.join(self.sounds_dir, 'wake_word.wav'),
            'listening': os.path.join(self.sounds_dir, 'listening.wav'),
            'processing': os.path.join(self.sounds_dir, 'processing.wav'),
            'success': os.path.join(self.sounds_dir, 'success.wav'),
            'error': os.path.join(self.sounds_dir, 'error.wav'),
            'thinking': os.path.join(self.sounds_dir, 'thinking.wav')
        }
        
        # Initialize pygame mixer
        self._init_pygame()
        
        # Create default beep sounds if WAV files don't exist
        self._create_default_sounds()
    
    def _init_pygame(self):
        """Initialize pygame mixer for audio playback"""
        try:
            with self._lock:
                if not self._initialized:
                    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                    self._initialized = True
                    print("✅ Voice sound effects initialized")
        except Exception as e:
            print(f"⚠️ Could not initialize sound effects: {e}")
            self.enabled = False
    
    def _create_default_sounds(self):
        """Create default beep sounds if custom WAV files don't exist"""
        try:
            import numpy as np
            import wave
            
            def create_beep(filename: str, frequency: int, duration: float):
                """Create a simple beep WAV file"""
                if os.path.exists(filename):
                    return  # Don't overwrite existing files
                
                sample_rate = 22050
                t = np.linspace(0, duration, int(sample_rate * duration))
                
                # Generate sine wave
                wave_data = np.sin(2 * np.pi * frequency * t)
                
                # Apply fade in/out to avoid clicks
                fade_len = int(sample_rate * 0.01)  # 10ms fade
                fade_in = np.linspace(0, 1, fade_len)
                fade_out = np.linspace(1, 0, fade_len)
                wave_data[:fade_len] *= fade_in
                wave_data[-fade_len:] *= fade_out
                
                # Convert to 16-bit PCM
                wave_data = (wave_data * 32767).astype(np.int16)
                
                # Write WAV file
                with wave.open(filename, 'w') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(wave_data.tobytes())
            
            # Create default sounds with different frequencies
            create_beep(self.sound_files['wake_word'], 800, 0.1)  # High beep
            create_beep(self.sound_files['listening'], 600, 0.15)  # Mid beep
            create_beep(self.sound_files['processing'], 700, 0.08)  # Quick beep
            create_beep(self.sound_files['success'], 1000, 0.12)  # Success tone
            create_beep(self.sound_files['error'], 400, 0.2)  # Low error tone
            create_beep(self.sound_files['thinking'], 650, 0.1)  # Thinking tone
            
            print(f"✅ Created default sound effects in {self.sounds_dir}/")
            
        except ImportError:
            print("⚠️ numpy not available for creating default sounds. You can add your own WAV files to the voice_sounds/ directory.")
        except Exception as e:
            print(f"⚠️ Could not create default sounds: {e}")
    
    def play_sound(self, sound_name: str, async_play: bool = True):
        """
        Play a sound effect
        
        Args:
            sound_name: Name of the sound ('wake_word', 'listening', 'processing', 'success', 'error', 'thinking')
            async_play: Play sound asynchronously (non-blocking)
        """
        if not self.enabled or not self._initialized:
            return
        
        if sound_name not in self.sound_files:
            print(f"⚠️ Unknown sound: {sound_name}")
            return
        
        sound_file = self.sound_files[sound_name]
        
        if not os.path.exists(sound_file):
            # print(f"⚠️ Sound file not found: {sound_file}")
            return
        
        try:
            if async_play:
                # Play in background thread
                thread = threading.Thread(target=self._play_sound_sync, args=(sound_file,), daemon=True)
                thread.start()
            else:
                self._play_sound_sync(sound_file)
        except Exception as e:
            print(f"⚠️ Error playing sound {sound_name}: {e}")
    
    def _play_sound_sync(self, sound_file: str):
        """Play sound synchronously (blocking)"""
        try:
            with self._lock:
                sound = pygame.mixer.Sound(sound_file)
                sound.set_volume(self.volume)  # Apply current volume to this sound
                channel = sound.play()
                # Wait for sound to finish
                while channel.get_busy():
                    pygame.time.wait(10)
        except Exception as e:
            print(f"⚠️ Sound playback error: {e}")
    
    def set_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        try:
            # Clamp volume to valid range
            self.volume = max(0.0, min(1.0, volume))
            # Note: Volume is applied per-sound in _play_sound_sync via Sound.set_volume()
        except Exception as e:
            print(f"⚠️ Could not set volume: {e}")
    
    def enable(self):
        """Enable sound effects"""
        self.enabled = True
        return "✅ Voice sound effects enabled"
    
    def disable(self):
        """Disable sound effects"""
        self.enabled = False
        return "✅ Voice sound effects disabled"
    
    def toggle(self):
        """Toggle sound effects on/off"""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        return f"✅ Voice sound effects {status}"
    
    def cleanup(self):
        """Clean up pygame mixer"""
        try:
            if self._initialized:
                pygame.mixer.quit()
                self._initialized = False
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")
    
    def add_custom_sound(self, sound_name: str, wav_file_path: str) -> str:
        """
        Add a custom sound effect
        
        Args:
            sound_name: Name for the sound
            wav_file_path: Path to the WAV file
        """
        if not os.path.exists(wav_file_path):
            return f"❌ File not found: {wav_file_path}"
        
        if not wav_file_path.lower().endswith('.wav'):
            return "❌ Only WAV files are supported"
        
        # Copy to sounds directory
        import shutil
        dest_path = os.path.join(self.sounds_dir, f"{sound_name}.wav")
        shutil.copy(wav_file_path, dest_path)
        self.sound_files[sound_name] = dest_path
        
        return f"✅ Added custom sound '{sound_name}' from {wav_file_path}"
    
    def list_sounds(self) -> dict:
        """List all available sounds and their status"""
        sounds_status = {}
        for name, path in self.sound_files.items():
            sounds_status[name] = {
                'path': path,
                'exists': os.path.exists(path),
                'size': os.path.getsize(path) if os.path.exists(path) else 0
            }
        return sounds_status


def create_voice_sound_effects(sounds_dir: str = "voice_sounds") -> VoiceSoundEffects:
    """Factory function to create VoiceSoundEffects instance"""
    return VoiceSoundEffects(sounds_dir)
