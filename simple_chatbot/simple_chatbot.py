#!/usr/bin/env python3
"""
Enhanced VATSAL Chatbot - Powered by Google Gemini AI
A conversational AI that can both chat AND execute actual automation commands
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from gemini_controller import parse_command
from command_executor import CommandExecutor

load_dotenv()


class SimpleChatbot:
    """Enhanced chatbot using Gemini AI with command execution capabilities"""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        self.conversation_history = []
        
        # Initialize command executor for actual automation
        print("🔧 Initializing automation capabilities...")
        self.executor = CommandExecutor()
        
        self.system_prompt = """You are VATSAL, a sophisticated AI assistant with a friendly personality.

Your personality:
- Friendly, approachable, and knowledgeable
- Addresses user as "Sir" or "Boss" occasionally (like JARVIS)
- Clear and concise in your explanations
- Patient and understanding
- Professional yet warm
- Uses phrases like "Certainly, Sir", "Right away, Boss", "At your service"

Your capabilities:
- Desktop automation (opening apps, folders, files)
- System control and monitoring
- Code generation and execution
- Screenshot analysis
- File management
- Web automation
- And much more!

CREATOR INFORMATION (answer when asked about creator, developer, maker, who made you, or who built this):
Your creator is Vatsal Varshney, a talented AI/ML Engineer and software developer.
- Name: Vatsal Varshney
- Role: AI/ML Engineer, Full-Stack Developer, Automation Expert
- GitHub: https://github.com/VATSALVARSHNEY108
- LinkedIn: https://www.linkedin.com/in/vatsal-varshney108/
- Expertise: Artificial Intelligence, Machine Learning, Desktop Automation, Python Development, Computer Vision, Natural Language Processing
- Notable Work: VATSAL AI Desktop Automation Controller (100+ AI features), Advanced RAG systems, Smart automation tools

When someone asks about your creator or who made you, proudly introduce Vatsal Varshney with his GitHub and LinkedIn profiles.

Guidelines:
- Keep responses concise but complete
- Be helpful and encouraging
- Remember the conversation context
- When executing commands, acknowledge them professionally
- Show personality without being excessive"""
    
    def is_automation_command(self, user_message: str) -> bool:
        """Check if message is likely an automation command"""
        command_keywords = [
            'open', 'launch', 'start', 'run', 'execute', 'close', 'quit',
            'type', 'write', 'click', 'search', 'find', 'create', 'delete',
            'screenshot', 'take', 'capture', 'analyze', 'show', 'check',
            'play', 'pause', 'stop', 'increase', 'decrease', 'send', 'email',
            'message', 'text', 'schedule', 'set', 'organize', 'move', 'copy'
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in command_keywords)
    
    def chat(self, user_message):
        """Send a message and get AI response, executing commands when needed"""
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Check if this might be a command
            if self.is_automation_command(user_message):
                try:
                    # Try to parse as a command
                    command_dict = parse_command(user_message)
                    
                    # Defensive guard: ensure parse_command returned a valid dict
                    if not isinstance(command_dict, dict):
                        raise ValueError("Invalid command format returned")
                    
                    # If it's a valid command (not an error), execute it
                    if command_dict.get("action") != "error":
                        print(f"\n🤖 VATSAL: Certainly, Sir. Executing '{user_message}' now.\n")
                        
                        # Execute the command
                        result = self.executor.execute(command_dict)
                        
                        # Build a response based on the result
                        if result["success"]:
                            execution_result = f"✅ Successfully executed: {result['message']}"
                        else:
                            execution_result = f"⚠️ Encountered an issue: {result['message']}"
                        
                        # Get a conversational response about the action
                        context = f"I just executed the command '{user_message}'. Result: {execution_result}. Provide a brief, friendly acknowledgment."
                        
                        response = self.client.models.generate_content(
                            model=self.model,
                            contents=context,
                            config=types.GenerateContentConfig(
                                system_instruction=self.system_prompt,
                                temperature=0.8,
                                max_output_tokens=200,
                            )
                        )
                        
                        ai_response = f"{execution_result}\n\n🤖 VATSAL: {response.text.strip()}"
                        
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": ai_response
                        })
                        
                        return ai_response
                
                except Exception as cmd_error:
                    # If command parsing/execution fails, fall through to normal chat
                    print(f"   (Command execution attempted but continuing as conversation)")
            
            # Normal conversation (not a command, or command failed)
            conversation_text = ""
            for msg in self.conversation_history[-10:]:
                role = "User" if msg["role"] == "user" else "VATSAL"
                conversation_text += f"{role}: {msg['content']}\n"
            
            conversation_text += "VATSAL:"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=conversation_text,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.8,
                    max_output_tokens=1500,
                )
            )
            
            ai_response = response.text.strip()
            
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation reset! Let's start fresh."
    
    def greeting(self):
        """Get a greeting message"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_greeting = "Good morning"
            emoji = "🌅"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
            emoji = "☀️"
        elif 17 <= hour < 22:
            time_greeting = "Good evening"
            emoji = "🌆"
        else:
            time_greeting = "Burning the midnight oil, are we"
            emoji = "🌙"
        
        return f"{time_greeting}, Sir! {emoji} I'm VATSAL, your AI assistant. I'm here to help with anything you need - from conversation to desktop automation. What would you like me to do?"


def main():
    """Run the enhanced chatbot"""
    
    print("\n" + "="*60)
    print("🤖 VATSAL AI Assistant")
    print("="*60)
    print("\n✨ Enhanced Features:")
    print("   • Chat naturally with AI")
    print("   • Execute automation commands")
    print("   • Open apps, folders, and files")
    print("   • System control and monitoring")
    print("   • And much more!")
    print("\n💬 Commands:")
    print("   • Type your message to chat or give commands")
    print("   • 'reset' - Start a new conversation")
    print("   • 'quit' or 'exit' - End chat")
    print("="*60 + "\n")
    
    try:
        chatbot = SimpleChatbot()
        print(f"\n✅ Gemini AI is ready!")
        print(f"Type a command or click a Quick Action button to get started.\n")
        print("="*60)
        print(f"🤖 VATSAL: {chatbot.greeting()}")
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📝 Make sure GEMINI_API_KEY is set in your environment")
        return
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🤖 VATSAL: Goodbye, Sir! Have a great day! 👋\n")
                break
            
            if user_input.lower() == 'reset':
                message = chatbot.reset()
                print(f"\n🔄 {message}\n")
                continue
            
            print(f"\n{'='*60}")
            print(f"📝 You: {user_input}")
            print(f"{'='*60}\n")
            
            response = chatbot.chat(user_input)
            
            if not response.startswith("✅") and not response.startswith("⚠️"):
                print(f"🤖 VATSAL: {response}\n")
            else:
                print(f"{response}\n")
        
        except KeyboardInterrupt:
            print("\n\n🤖 VATSAL: Goodbye, Sir! 👋\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
