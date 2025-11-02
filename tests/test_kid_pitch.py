"""
Test different pitch/voice settings for kid voice using espeak
"""
import subprocess
import pyttsx3

print("🎤 Testing Kid Voice with Different Pitch Settings")
print("=" * 60)

# Test espeak directly with pitch control
print("\n1. Testing espeak with HIGH pitch (kid voice) directly...")
subprocess.run(['espeak', '-p', '99', '-s', '200', 'Hello! I am a kid voice!'])

print("\n2. Testing espeak with VERY HIGH pitch...")
subprocess.run(['espeak', '-p', '80', '-s', '220', 'This is my voice as a child!'])

print("\n3. Testing espeak with child voice variant...")
subprocess.run(['espeak', '-v', 'en+f3', '-s', '200', 'I sound like a little kid!'])

print("\n" + "=" * 60)
print("Which one sounded most like a kid? Let me know!")
