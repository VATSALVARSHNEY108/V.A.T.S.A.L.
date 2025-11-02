#!/usr/bin/env python3
"""
Enhanced Intelligent Chatbot powered by Google Gemini AI
Fully compatible with GUI app with advanced features
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class EnhancedGeminiChatbot:
    """Enhanced intelligent chatbot using Gemini AI with full GUI compatibility"""
    
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"
        self.conversation_history = []
        self.session_start = datetime.now()
        self.total_messages = 0
        self.user_name = "User"
        self.personality = "friendly"
        self.ai_available = True
        
        self.system_prompt = """You are VATSAL, an intelligent and helpful AI assistant.

Your personality:
- Friendly, approachable, and knowledgeable
- Enthusiastic about helping users
- Clear and concise in your explanations
- Patient and understanding
- Professional yet warm

Your capabilities:
- Answer questions on any topic
- Help with coding and technical problems
- Provide explanations and tutorials
- Assist with writing and creativity
- Offer advice and suggestions
- Engage in meaningful conversations

Guidelines:
- Keep responses concise but complete (2-5 sentences unless more detail is needed)
- Use examples when helpful
- Break down complex topics into simple terms
- Ask clarifying questions if needed
- Be encouraging and positive
- Remember context from the conversation"""

    def chat(self, user_message: str) -> str:
        """Send a message and get AI response with enhanced context"""
        
        try:
            self.total_messages += 1
            
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Build conversation context (last 15 messages for better context)
            recent_history = self.conversation_history[-15:]
            
            # Format conversation for the prompt
            conversation_text = ""
            for msg in recent_history:
                role = "User" if msg["role"] == "user" else "VATSAL"
                conversation_text += f"{role}: {msg['content']}\n"
            
            # Create the full prompt with context
            full_prompt = f"{conversation_text}VATSAL:"
            
            # Get response from Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.8,
                    max_output_tokens=1500,
                    top_p=0.95,
                )
            )
            
            ai_response = response.text.strip()
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            })
            
            return ai_response
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}"
            return error_msg
    
    async def process_message(self, user_message: str) -> str:
        """Process message asynchronously (GUI compatibility)"""
        return self.chat(user_message)
    
    def initiate_conversation(self) -> str:
        """Start a new conversation with a greeting (GUI compatibility)"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greeting = "Good morning! 🌅"
        elif 12 <= hour < 17:
            greeting = "Good afternoon! ☀️"
        elif 17 <= hour < 22:
            greeting = "Good evening! 🌆"
        else:
            greeting = "Hello there! 🌙"
        
        return f"{greeting} I'm VATSAL, your AI assistant. I'm here to help with anything you need - from answering questions to having a friendly chat. What would you like to talk about?"
    
    def reset(self):
        """Clear conversation history and start fresh"""
        self.conversation_history = []
        self.session_start = datetime.now()
        return "✨ Conversation reset! Let's start fresh. How can I help you?"
    
    def reset_conversation(self):
        """Reset conversation (GUI compatibility - same as reset)"""
        return self.reset()
    
    def set_user_name(self, name: str):
        """Set user's name for personalization"""
        self.user_name = name
        return f"Nice to meet you, {name}! 👋"
    
    def get_stats(self) -> dict:
        """Get chatbot statistics (enhanced for GUI compatibility)"""
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        # Calculate conversation length
        conversation_length = len([msg for msg in self.conversation_history if msg["role"] == "user"])
        
        return {
            "total_messages": self.total_messages,
            "current_messages": conversation_length,
            "conversation_length": len(self.conversation_history),
            "total_conversations": 1 if self.conversation_history else 0,
            "session_duration_minutes": round(session_duration / 60, 1),
            "session_start": self.session_start.strftime("%Y-%m-%d %H:%M:%S"),
            "user_name": self.user_name,
            "ai_available": self.ai_available,
            "learned_preferences": 0,
            "top_topics": [],
            "first_interaction": self.session_start.isoformat() if self.conversation_history else "Never"
        }
    
    def save_conversation(self, filepath: str = "conversation_history.json"):
        """Save conversation history to a file"""
        try:
            data = {
                "session_start": self.session_start.isoformat(),
                "user_name": self.user_name,
                "total_messages": self.total_messages,
                "conversation": self.conversation_history
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return f"✅ Conversation saved to {filepath}"
        except Exception as e:
            return f"❌ Error saving conversation: {str(e)}"
    
    def load_conversation(self, filepath: str = "conversation_history.json"):
        """Load conversation history from a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.conversation_history = data.get("conversation", [])
            self.total_messages = data.get("total_messages", 0)
            self.user_name = data.get("user_name", "User")
            
            return f"✅ Conversation loaded from {filepath}"
        except FileNotFoundError:
            return "❌ No saved conversation found"
        except Exception as e:
            return f"❌ Error loading conversation: {str(e)}"
    
    def get_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation to summarize yet."
        
        try:
            # Get conversation text
            conversation_text = ""
            for msg in self.conversation_history:
                role = "User" if msg["role"] == "user" else "AI"
                conversation_text += f"{role}: {msg['content']}\n"
            
            # Ask AI to summarize
            summary_prompt = f"Please provide a brief summary of this conversation:\n\n{conversation_text}\n\nSummary:"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=summary_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=300,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"


def create_vatsal_ai(api_key=None):
    """Create chatbot instance (for compatibility with GUI app)"""
    try:
        return EnhancedGeminiChatbot(api_key)
    except Exception as e:
        # Return a fallback object if API key is not available
        class FallbackChatbot:
            def __init__(self):
                self.user_name = "User"
                self.ai_available = False
                
            def chat(self, message):
                return "API key not configured. Please add GEMINI_API_KEY to your secrets."
            
            async def process_message(self, message):
                return self.chat(message)
            
            def initiate_conversation(self):
                return "⚠️ GEMINI_API_KEY not found. Please configure it in Replit Secrets."
            
            def reset(self):
                return "Chatbot not available without API key."
            
            def reset_conversation(self):
                return self.reset()
            
            def get_stats(self):
                return {
                    "total_messages": 0,
                    "current_messages": 0,
                    "conversation_length": 0,
                    "total_conversations": 0,
                    "session_duration_minutes": 0,
                    "session_start": "N/A",
                    "user_name": "User",
                    "ai_available": False,
                    "learned_preferences": 0,
                    "top_topics": [],
                    "first_interaction": "Never"
                }
        
        return FallbackChatbot()


def print_header():
    """Display chatbot header"""
    print("\n" + "="*75)
    print("🤖 VATSAL - Enhanced AI Chatbot (Powered by Google Gemini)")
    print("="*75)
    print("✨ Features:")
    print("   • 💬 Natural conversation with context awareness")
    print("   • 🧠 Enhanced memory (remembers last 15 messages)")
    print("   • 📊 Session statistics and analytics")
    print("   • 💾 Save and load conversations")
    print("   • 🎯 Personalized responses")
    print("\n💡 Ask me anything! I can help with:")
    print("   • General knowledge & facts")
    print("   • Programming & coding help")
    print("   • Math, science & technology")
    print("   • Writing & creative tasks")
    print("   • Explanations & tutorials")
    print("   • And much more!")
    print("\n💬 Commands:")
    print("   • Just type your question or message")
    print("   • 'reset' - Start a new conversation")
    print("   • 'stats' - View session statistics")
    print("   • 'summary' - Get conversation summary")
    print("   • 'save' - Save conversation to file")
    print("   • 'load' - Load previous conversation")
    print("   • 'quit' or 'exit' - End chat")
    print("="*75 + "\n")


def main():
    """Run the enhanced chatbot"""
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found!")
        print("\n📝 To fix this:")
        print("   1. Go to Replit Secrets (🔒 icon)")
        print("   2. Add: GEMINI_API_KEY = your_api_key")
        print("   3. Get API key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)
    
    # Initialize chatbot
    print("🔧 Initializing Enhanced AI Chatbot...")
    try:
        chatbot = EnhancedGeminiChatbot()
        print("✅ Chatbot ready!\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Display header
    print_header()
    
    # Get user's name (optional)
    try:
        name_input = input("👤 What's your name? (or press Enter to skip): ").strip()
        if name_input:
            print(chatbot.set_user_name(name_input))
        print()
    except:
        print()
    
    # Initial greeting
    print(f"🤖 VATSAL: {chatbot.initiate_conversation()}\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input(f"👤 {chatbot.user_name}: ").strip()
            
            # Skip empty input
            if not user_input:
                continue
            
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 VATSAL: It was great chatting with you! Goodbye! 👋✨\n")
                break
            
            # Handle reset command
            if user_input.lower() == 'reset':
                message = chatbot.reset()
                print(f"\n🔄 {message}\n")
                continue
            
            # Handle stats command
            if user_input.lower() == 'stats':
                stats = chatbot.get_stats()
                print(f"\n📊 Session Statistics:")
                print(f"   • Messages: {stats['total_messages']}")
                print(f"   • Conversation length: {stats['conversation_length']} exchanges")
                print(f"   • Session duration: {stats['session_duration_minutes']} minutes")
                print(f"   • Started: {stats['session_start']}")
                print(f"   • User: {stats['user_name']}\n")
                continue
            
            # Handle summary command
            if user_input.lower() == 'summary':
                print("\n📝 Generating conversation summary...\n")
                summary = chatbot.get_summary()
                print(f"📋 Summary: {summary}\n")
                continue
            
            # Handle save command
            if user_input.lower() == 'save':
                message = chatbot.save_conversation()
                print(f"\n{message}\n")
                continue
            
            # Handle load command
            if user_input.lower() == 'load':
                message = chatbot.load_conversation()
                print(f"\n{message}\n")
                continue
            
            # Get AI response
            print("\n🤖 VATSAL: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(f"{response}\n")
        
        except KeyboardInterrupt:
            print("\n\n🤖 VATSAL: Goodbye! Take care! 👋\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
