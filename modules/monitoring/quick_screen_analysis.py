"""
Quick Screen Analysis - One Command, Instant Feedback!
Run this for instant AI suggestions on what's on your screen
"""

from screen_suggester import ScreenSuggester

def main():
    print("\n" + "="*70)
    print("🤖 QUICK SCREEN ANALYSIS - AI is watching your screen!")
    print("="*70)
    
    suggester = ScreenSuggester()
    
    # Automatically get suggestions
    result = suggester.analyze_and_suggest()
    print(result)
    
    print("\n" + "="*70)
    print("✅ Analysis complete!")
    print("📸 Screenshot saved in: screenshots/")
    print("="*70)


if __name__ == "__main__":
    main()
