#!/usr/bin/env python3
"""
🆕 Test Script: Screenshot Analysis (Cloud-Compatible!)

This works in Replit! Upload your screenshot and analyze it with AI.

How to use:
1. Upload your screenshot to this Replit workspace (drag & drop into file manager)
2. Update the SCREENSHOT_PATH below to match your filename
3. Run this script: python test_screenshot_analysis.py
"""

import os
from smart_screen_monitor import SmartScreenMonitor

# ========================================
# CONFIGURATION
# ========================================
SCREENSHOT_PATH = "my_screenshot.png"  # 👈 Change this to your screenshot filename

# Analysis focus options:
# - "general" : Overall description of what's on screen
# - "errors"  : Look for error messages and issues
# - "productivity" : Analyze productivity and focus level
# - "code"    : Analyze code quality and bugs
# - "design"  : Analyze UI/UX and design elements
ANALYSIS_FOCUS = "general"

# ========================================
# MAIN PROGRAM
# ========================================

def main():
    """Test the new screenshot upload analysis feature"""
    
    print("=" * 60)
    print("🆕 Screenshot Analysis Demo (Cloud-Compatible!)")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n❌ GEMINI_API_KEY not found!")
        print("\n📝 To fix this:")
        print("   1. Go to Replit Secrets (🔒 icon in sidebar)")
        print("   2. Add: GEMINI_API_KEY = your_api_key")
        print("   3. Get key from: https://aistudio.google.com/app/apikey")
        return
    
    print(f"\n✅ API key found! (length: {len(api_key)} chars)")
    
    # Check if screenshot file exists
    if not os.path.exists(SCREENSHOT_PATH):
        print(f"\n❌ Screenshot not found: {SCREENSHOT_PATH}")
        print("\n📝 How to upload your screenshot:")
        print("   1. Take a screenshot on your computer")
        print("   2. Drag & drop it into the Replit file manager")
        print("   3. Update SCREENSHOT_PATH in this script")
        print("   4. Run again: python test_screenshot_analysis.py")
        print("\n💡 Example screenshots you could analyze:")
        print("   • Screenshot of your code editor")
        print("   • Screenshot of a website you're building")
        print("   • Screenshot of an error message")
        print("   • Screenshot of a design mockup")
        return
    
    print(f"\n✅ Screenshot found: {SCREENSHOT_PATH}")
    print(f"📊 File size: {os.path.getsize(SCREENSHOT_PATH):,} bytes")
    
    # Initialize the screen monitor
    print("\n🔧 Initializing Smart Screen Monitor...")
    monitor = SmartScreenMonitor()
    
    # Analyze the screenshot
    print(f"\n🚀 Starting analysis (focus: {ANALYSIS_FOCUS})...")
    result = monitor.analyze_uploaded_screenshot(SCREENSHOT_PATH, focus=ANALYSIS_FOCUS)
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 ANALYSIS RESULTS")
    print("=" * 60)
    
    if result["success"]:
        print(f"\n✅ {result['message']}")
        print(f"\n📸 Screenshot: {result['screenshot']}")
        print(f"⏰ Analyzed at: {result['timestamp']}")
        print(f"\n🤖 AI Analysis:\n")
        print(result['analysis'])
    else:
        print(f"\n❌ Analysis failed:")
        print(result['message'])
    
    print("\n" + "=" * 60)
    print("✨ Analysis complete!")
    print("=" * 60)
    
    # Show next steps
    print("\n💡 Try different analysis modes:")
    print('   • Set ANALYSIS_FOCUS = "errors" to find bugs')
    print('   • Set ANALYSIS_FOCUS = "code" for code review')
    print('   • Set ANALYSIS_FOCUS = "design" for UI feedback')
    print('   • Set ANALYSIS_FOCUS = "productivity" to check focus')


if __name__ == "__main__":
    main()
