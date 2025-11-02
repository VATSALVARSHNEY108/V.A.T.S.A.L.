#!/usr/bin/env python3
"""
Test script to demonstrate creator information retrieval
"""

from simple_chatbot import SimpleChatbot

def test_creator_questions():
    """Test various creator-related questions"""
    print("=" * 70)
    print("🤖 VATSAL CREATOR INFORMATION TEST")
    print("=" * 70)
    
    chatbot = SimpleChatbot()
    
    # Test questions about the creator
    test_questions = [
        "Who created you?",
        "Who is your creator?",
        "Who made this project?",
        "Tell me about your developer",
        "Who built you?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 70}")
        print(f"Test {i}: {question}")
        print("=" * 70)
        
        response = chatbot.chat(question)
        print(f"\n🤖 VATSAL: {response}\n")
    
    print("=" * 70)
    print("✅ Creator information test complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_creator_questions()
