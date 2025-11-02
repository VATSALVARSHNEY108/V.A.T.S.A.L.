#!/usr/bin/env python3
"""
Create WAV sound effect files for voice commanding
"""

import numpy as np
import wave
import os

def create_beep(filename, frequency, duration, fade_duration=0.01):
    """Create a beep sound with fade in/out"""
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate sine wave
    wave_data = np.sin(2 * np.pi * frequency * t)
    
    # Apply fade in/out to avoid clicks
    fade_len = int(sample_rate * fade_duration)
    if fade_len > 0 and fade_len < len(wave_data):
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        wave_data[:fade_len] *= fade_in
        wave_data[-fade_len:] *= fade_out
    
    # Convert to 16-bit PCM
    wave_data = (wave_data * 32767 * 0.8).astype(np.int16)  # 80% volume
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"✅ Created: {filename} ({frequency}Hz, {duration}s)")

def create_two_tone(filename, freq1, freq2, duration):
    """Create a two-tone beep (rising or falling)"""
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate frequency sweep
    freq_sweep = np.linspace(freq1, freq2, len(t))
    phase = 2 * np.pi * np.cumsum(freq_sweep) / sample_rate
    wave_data = np.sin(phase)
    
    # Apply fade in/out
    fade_len = int(sample_rate * 0.01)
    if fade_len > 0 and fade_len < len(wave_data):
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        wave_data[:fade_len] *= fade_in
        wave_data[-fade_len:] *= fade_out
    
    # Convert to 16-bit PCM
    wave_data = (wave_data * 32767 * 0.8).astype(np.int16)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"✅ Created: {filename} ({freq1}Hz-{freq2}Hz, {duration}s)")

def create_chord(filename, frequencies, duration):
    """Create a chord with multiple frequencies"""
    sample_rate = 22050
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate multiple sine waves and combine
    wave_data = np.zeros(len(t))
    for freq in frequencies:
        wave_data += np.sin(2 * np.pi * freq * t) / len(frequencies)
    
    # Apply fade in/out
    fade_len = int(sample_rate * 0.01)
    if fade_len > 0 and fade_len < len(wave_data):
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        wave_data[:fade_len] *= fade_in
        wave_data[-fade_len:] *= fade_out
    
    # Convert to 16-bit PCM
    wave_data = (wave_data * 32767 * 0.8).astype(np.int16)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"✅ Created: {filename} (chord: {frequencies}Hz, {duration}s)")

def main():
    # Create directory if it doesn't exist
    sounds_dir = "voice_sounds"
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("=" * 60)
    print("🔊 Creating Voice Sound Effect WAV Files")
    print("=" * 60)
    print()
    
    # Wake word - High attention-grabbing beep
    create_two_tone(
        os.path.join(sounds_dir, "wake_word.wav"),
        600, 900,  # Rising tone
        0.12
    )
    
    # Listening - Gentle prompt
    create_beep(
        os.path.join(sounds_dir, "listening.wav"),
        700,
        0.15
    )
    
    # Processing - Quick acknowledgment
    create_beep(
        os.path.join(sounds_dir, "processing.wav"),
        800,
        0.08
    )
    
    # Success - Pleasant confirmation chord
    create_chord(
        os.path.join(sounds_dir, "success.wav"),
        [800, 1000, 1200],  # Major chord
        0.15
    )
    
    # Error - Descending tone
    create_two_tone(
        os.path.join(sounds_dir, "error.wav"),
        600, 400,  # Falling tone
        0.2
    )
    
    # Thinking - Pulsing tone
    create_beep(
        os.path.join(sounds_dir, "thinking.wav"),
        750,
        0.1
    )
    
    print()
    print("=" * 60)
    print("✅ All WAV files created successfully!")
    print("=" * 60)
    print()
    print(f"📁 Location: {sounds_dir}/")
    print()
    print("Files created:")
    for filename in os.listdir(sounds_dir):
        if filename.endswith('.wav'):
            filepath = os.path.join(sounds_dir, filename)
            size = os.path.getsize(filepath)
            print(f"  • {filename:20s} ({size:,} bytes)")
    print()
    print("🎉 Ready to use! Run: python test_voice_sounds.py")

if __name__ == "__main__":
    main()
