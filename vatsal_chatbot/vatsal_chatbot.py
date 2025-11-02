#!/usr/bin/env python3
"""
VATSAL AI Chatbot - Simple CLI Interface
An intelligent chatbot that can answer any type of question using Google Gemini AI
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from vatsal_ai import create_vatsal_ai
except ImportError:
    print("Error: Cannot import VatsalAI. Make sure vatsal_ai.py is in the same directory.")
    sys.exit(1)


def print_header():
    """Display chatbot header"""
    print("\n" + "=" * 70)
    print("🤖 VATSAL AI - Intelligent Chatbot")
    print("=" * 70)
    print("💡 Ask me anything! I can help with:")
    print("   • General knowledge questions")
    print("   • Coding and programming help")
    print("   • Math and science problems")
    print("   • Creative writing and ideas")
    print("   • Explanations and tutorials")
    print("   • And much more!")
    print("\n📝 Type 'quit', 'exit', or 'bye' to end the conversation")
    print("📊 Type 'stats' to see chatbot statistics")
    print("🔄 Type 'reset' to start a new conversation")
    print("=" * 70 + "\n")


async def run_chatbot():
    """Main chatbot conversation loop"""
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found!")
        print("Please set your Gemini API key in the .env file or environment variables.")
        sys.exit(1)

    # Create chatbot instance
    print("🔧 Initializing VATSAL AI chatbot...")
    try:
        vatsal = create_vatsal_ai()
        print("✅ Chatbot ready!\n")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        sys.exit(1)

    # Display header
    print_header()

    # Initial greeting
    greeting = vatsal.initiate_conversation()
    print(f"🤖 VATSAL: {greeting}\n")

    # Conversation loop
    conversation_active = True

    while conversation_active:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 VATSAL: Goodbye! It was nice talking with you. Your conversation has been saved!")
                vatsal.end_conversation()
                conversation_active = False
                break

            elif user_input.lower() == 'stats':
                stats = vatsal.get_stats()
                print("\n📊 Chatbot Statistics:")
                print("=" * 50)
                print(f"  👤 User Name: {stats.get('user_name', 'Unknown')}")
                print(f"  💬 Messages this session: {stats.get('current_messages', 0)}")
                print(f"  📝 Total conversations: {stats.get('total_conversations', 0)}")
                print(f"  📨 Total messages: {stats.get('total_messages', 0)}")
                print(f"  🎯 Learned preferences: {stats.get('learned_preferences', 0)}")
                print(f"  🔥 Top topics: {', '.join(stats.get('top_topics', []))}")
                print(f"  🤖 AI available: {stats.get('ai_available', False)}")
                print(f"  📅 First interaction: {stats.get('first_interaction', 'Never')}")
                print(f"  🕐 Last interaction: {stats.get('last_interaction', 'Never')}")
                print("=" * 50 + "\n")
                continue

            elif user_input.lower() == 'reset':
                print("\n🔄 Starting a new conversation...")
                vatsal.reset_conversation()
                greeting = vatsal.initiate_conversation()
                print(f"🤖 VATSAL: {greeting}\n")
                continue

            # Process the message with AI
            print("🤖 VATSAL: ", end="", flush=True)
            response = await vatsal.process_message(user_input)
            print(f"{response}\n")

        except KeyboardInterrupt:
            print("\n\n🤖 VATSAL: Conversation interrupted. Saving your chat...")
            vatsal.end_conversation()
            conversation_active = False
            break

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.\n")

    print("\n" + "=" * 70)
    print("Thank you for using VATSAL AI! 👋")
    print("=" * 70 + "\n")


def main():
    """Entry point for the chatbot"""
    try:
        asyncio.run(run_chatbot())
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
