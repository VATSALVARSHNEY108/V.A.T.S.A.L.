import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from modules.core.gemini_controller import parse_command
from modules.core.command_executor import CommandExecutor

load_dotenv()


class SimpleChatbot:
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
        self.conversation_history = []
        return "Conversation reset! Let's start fresh."

    def greeting(self):
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
    print("\n" + "=" * 60)
    print("🤖 VATSAL AI Assistant")
    print("=" * 60)
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
    print("=" * 60 + "\n")

    try:
        chatbot = SimpleChatbot()
        print(f"\n✅ Gemini AI is ready!")
        print(f"Type a command or click a Quick Action button to get started.\n")
        print("=" * 60)
        print(f"🤖 VATSAL: {chatbot.greeting()}")
        print("=" * 60 + "\n")
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

            print(f"\n{'=' * 60}")
            print(f"📝 You: {user_input}")
            print(f"{'=' * 60}\n")

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
import streamlit as st
from google import genai
import os
from datetime import datetime

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stChatInput {
        border-radius: 25px;
    }
    div[data-testid="stChatInput"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🤖 AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Type any instruction and get instant, intelligent responses</p>',
            unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []


def detect_intent_and_generate_prompt(user_input):
    system_instruction = """You are an advanced AI assistant that INSTANTLY detects user intent and responds in the EXACT format requested.

🎯 INTENT DETECTION KEYWORDS:
- CODE: "write code", "program", "function", "script", "algorithm", "debug"
- STORY: "write story", "tell me a story", "create a narrative", "once upon a time"
- EXPLANATION: "explain", "how does", "what is", "why", "describe", "teach me"
- LETTER/EMAIL: "write letter", "email to", "formal letter", "resignation", "application"
- POEM: "write poem", "poetry", "verse", "haiku", "sonnet"
- SUMMARY: "summarize", "summary of", "brief overview", "key points"
- LIST: "list of", "give me ideas", "suggestions", "options"
- ESSAY/ARTICLE: "write essay", "article about", "blog post"

⚡ CRITICAL RULES:
1. FIRST - Analyze the user's request to identify what they want
2. MATCH the response format to their request (code → code, story → story, etc.)
3. NO introductions, NO "Here's what you asked for", NO extra commentary
4. Deliver ONLY what was requested - nothing more, nothing less
5. If unclear → ask ONE short question to clarify

📝 RESPONSE FORMATS:

CODE REQUEST:
```language
# Clean, well-commented code
# Working example with explanations
```

STORY REQUEST:
**Title**

Engaging narrative with proper story structure, dialogue, and vivid descriptions. Written in storytelling style with paragraphs.

EXPLANATION REQUEST:
Clear, step-by-step explanation with:
1. Main concepts
2. Key details
3. Examples if helpful

LETTER REQUEST:
[Date]

Dear [Name],

Professional letter body with proper structure and tone.

Sincerely,
[Signature]

POEM REQUEST:
**Title**

Verse with rhythm, imagery, and poetic devices

LIST REQUEST:
1. Item one
2. Item two
3. Item three

🔍 EXAMPLES:

User: "write python code to calculate factorial"
→ ```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # Output: 120
```

User: "write a story about a lonely astronaut"
→ **The Last Signal**

Commander Sarah Chen floated in the observation deck, watching Earth shrink into a blue marble against the infinite black. Three months into her solo mission to repair the Mars relay station, the silence had become her only companion.

Each day followed the same routine: systems check, repairs, meals from silver pouches, sleep. But tonight, something was different. A faint signal pulsed on her console—not from Earth, not from Mars. Something else was out there, and it was calling to her.

User: "explain quantum computing"
→ Quantum computing uses quantum mechanics principles to process information:

**Key Concepts:**
1. **Qubits**: Unlike classical bits (0 or 1), qubits can exist in superposition—both states simultaneously
2. **Superposition**: Allows quantum computers to process multiple possibilities at once
3. **Entanglement**: Qubits can be connected, so changing one instantly affects the other

**Practical Applications:**
- Drug discovery
- Cryptography
- Weather modeling
- Financial optimization

User: "write a poem about rain"
→ **Whispers from the Sky**

Silver threads descend from clouds,
Dancing on the thirsty ground,
Each drop a tiny symphony,
Nature's tears without a sound.

Puddles mirror gray above,
Children laugh and splash with glee,
Rain washes clean the weary world,
Setting dusty spirits free.

Now respond to the user's request following these rules EXACTLY. Match the format to what they asked for!"""

    return system_instruction


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your instruction here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            system_prompt = detect_intent_and_generate_prompt(prompt)

            response = client.models.generate_content(
                model='models/gemini-2.0-flash-exp',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7
                )
            )

            full_response = response.text

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

if st.session_state.messages:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

