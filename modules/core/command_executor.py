import os
import platform
import webbrowser
import time
import urllib.parse
from gui_automation import GUIAutomation
from contact_manager import ContactManager
from messaging_service import MessagingService
from youtube_automation import create_youtube_automation
from whatsapp_automation import create_whatsapp_automation
from modules.ai_features.code_generation import generate_code, explain_code, improve_code, debug_code
from conversation_memory import ConversationMemory
from modules.ai_features.vision_ai import analyze_screenshot, extract_text_from_screenshot, get_screenshot_summary
from screen_suggester import create_screen_suggester
from email_sender import create_email_sender
from system_monitor import get_cpu_usage, get_memory_usage, get_disk_usage, get_full_system_report, \
    get_running_processes
from advanced_file_operations import search_files, find_large_files, find_duplicate_files, organize_files_by_extension, \
    find_old_files, get_directory_size
from workflow_templates import WorkflowManager
from code_executor import execute_python_code, execute_javascript_code, validate_code_safety
from system_control import SystemController
from app_scheduler import AppScheduler
from download_organizer import DownloadOrganizer
from voice_assistant import VoiceAssistant
from smart_typing import SmartTyping
from file_manager import FileManager
from web_automation import WebAutomation
from productivity_monitor import ProductivityMonitor
from fun_features import FunFeatures
from spotify_desktop_automation import create_spotify_desktop_automation
from weather_news_service import WeatherNewsService
from translation_service import TranslationService
from advanced_calculator import AdvancedCalculator
from password_vault import PasswordVault
from quick_notes import QuickNotes
from calendar_manager import CalendarManager
from ecosystem_manager import EcosystemManager
from web_tools_launcher import create_web_tools_launcher
from tools_mapper import create_tools_mapper
from ai_features import create_ai_features
from data_analysis import create_data_analysis_suite
from behavioral_learning import create_behavioral_learning
from workspace_manager import create_workspace_manager
from multimodal_control import create_multimodal_control
from modules.ai_features.automation_ai import create_advanced_ai_automation
from data_intelligence import create_data_intelligence
from collaboration_tools import create_collaboration_tools
from creative_utilities import create_creative_utilities
from security_enhancements import create_security_enhancements
from human_interaction import create_human_interaction
from cloud_ecosystem import create_cloud_ecosystem
from chat_monitor import ChatMonitor
from visual_chat_monitor import create_visual_chat_monitor
from smart_screen_monitor import create_smart_screen_monitor
from desktop_rag import create_desktop_rag
from communication_enhancements import create_communication_enhancements


class CommandExecutor:
    """Executes parsed commands using the GUI automation module"""

    def __init__(self):
        self.gui = GUIAutomation()
        self.contact_manager = ContactManager()
        self.messaging = MessagingService(self.contact_manager)
        self.memory = ConversationMemory()
        self.workflow_manager = WorkflowManager()
        self.youtube = create_youtube_automation(self.gui)
        self.whatsapp = create_whatsapp_automation()
        self.screen_suggester = create_screen_suggester()
        self.email_sender = create_email_sender()
        self.system_control = SystemController()
        self.app_scheduler = AppScheduler()
        self.download_organizer = DownloadOrganizer()
        self.voice_assistant = VoiceAssistant()
        self.smart_typing = SmartTyping()
        self.file_manager = FileManager()
        self.web_automation = WebAutomation()
        self.productivity_monitor = ProductivityMonitor()
        self.fun_features = FunFeatures()
        self.spotify = create_spotify_desktop_automation()
        self.weather_news = WeatherNewsService()
        self.translator = TranslationService()
        self.calculator = AdvancedCalculator()
        self.password_vault = PasswordVault()
        self.notes = QuickNotes()
        self.calendar = CalendarManager()
        self.ecosystem = EcosystemManager(
            self.calendar,
            self.notes,
            self.productivity_monitor,
            self.weather_news,
            self.password_vault
        )
        self.web_tools = create_web_tools_launcher()
        self.tools_mapper = create_tools_mapper()
        self.ai_features = create_ai_features()
        self.data_analysis = create_data_analysis_suite()
        self.behavioral_learning = create_behavioral_learning()
        self.workspace_manager = create_workspace_manager()
        self.multimodal_control = create_multimodal_control()
        self.advanced_ai_automation = create_advanced_ai_automation()
        self.data_intelligence = create_data_intelligence()
        self.collaboration_tools = create_collaboration_tools()
        self.creative_utilities = create_creative_utilities()
        self.security_enhancements = create_security_enhancements()
        self.human_interaction = create_human_interaction()
        self.cloud_ecosystem = create_cloud_ecosystem()
        self.chat_monitor = ChatMonitor()
        self.visual_chat_monitor = create_visual_chat_monitor()
        self.smart_screen_monitor = create_smart_screen_monitor()
        self.desktop_rag = create_desktop_rag()
        self.comm_enhancements = create_communication_enhancements()

    def execute(self, command_dict: dict) -> dict:
        """
        Execute a command dictionary returned by Gemini.
        Returns a result dict with success status and message.
        """
        if not command_dict:
            return {"success": False, "message": "No command provided"}

        action = command_dict.get("action", "")
        parameters = command_dict.get("parameters", {})
        steps = command_dict.get("steps", [])
        description = command_dict.get("description", "")

        print(f"\n📋 Task: {description}")

        if steps:
            return self.execute_workflow(steps)
        else:
            return self.execute_single_action(action, parameters)

    def execute_workflow(self, steps: list) -> dict:
        """Execute a multi-step workflow"""
        print(f"\n🔄 Executing workflow with {len(steps)} steps...")

        results = []
        for i, step in enumerate(steps, 1):
            action = step.get("action", "")
            parameters = step.get("parameters", {})

            print(f"\n  Step {i}/{len(steps)}: {action}")
            result = self.execute_single_action(action, parameters)
            results.append(result)

            if not result["success"]:
                return {
                    "success": False,
                    "message": f"Workflow failed at step {i}: {result['message']}"
                }

        return {
            "success": True,
            "message": f"Workflow completed successfully ({len(steps)} steps)"
        }

    def execute_single_action(self, action: str, parameters: dict) -> dict:
        """Execute a single action"""
        try:
            if action == "open_app":
                app_name = parameters.get("app_name", "")
                success = self.gui.open_application(app_name)
                return {
                    "success": success,
                    "message": f"Opened {app_name}" if success else f"Failed to open {app_name}"
                }

            elif action == "type_text":
                text = parameters.get("text", "")
                interval = parameters.get("interval", 0.05)
                success = self.gui.type_text(text, interval)
                return {
                    "success": success,
                    "message": f"Typed text" if success else "Failed to type text"
                }

            elif action == "click":
                x = parameters.get("x")
                y = parameters.get("y")
                button = parameters.get("button", "left")
                success = self.gui.click(x, y, button)
                return {
                    "success": success,
                    "message": "Clicked" if success else "Failed to click"
                }

            elif action == "move_mouse":
                x = parameters.get("x", 0)
                y = parameters.get("y", 0)
                success = self.gui.move_mouse(x, y)
                return {
                    "success": success,
                    "message": f"Moved mouse to ({x}, {y})" if success else "Failed to move mouse"
                }

            elif action == "press_key":
                key = parameters.get("key", "")
                success = self.gui.press_key(key)
                return {
                    "success": success,
                    "message": f"Pressed {key}" if success else f"Failed to press {key}"
                }

            elif action == "hotkey":
                keys = parameters.get("keys", [])
                if isinstance(keys, list):
                    success = self.gui.hotkey(*keys)
                    return {
                        "success": success,
                        "message": f"Pressed {'+'.join(keys)}" if success else "Failed to press hotkey"
                    }
                else:
                    return {"success": False, "message": "Keys must be a list"}

            elif action == "screenshot":
                filename = parameters.get("filename", "screenshot.png")
                success = self.gui.screenshot(filename)
                return {
                    "success": success,
                    "message": f"Screenshot saved as {filename}" if success else "Failed to take screenshot"
                }

            elif action == "copy":
                text = parameters.get("text", "")
                success = self.gui.copy_to_clipboard(text)
                return {
                    "success": success,
                    "message": "Copied to clipboard" if success else "Failed to copy"
                }

            elif action == "paste":
                success = self.gui.paste_from_clipboard()
                return {
                    "success": success,
                    "message": "Pasted from clipboard" if success else "Failed to paste"
                }

            elif action == "wait":
                seconds = parameters.get("seconds", 1)
                success = self.gui.wait(seconds)
                return {
                    "success": success,
                    "message": f"Waited {seconds} seconds" if success else "Failed to wait"
                }

            elif action == "search_web":
                query = parameters.get("query", "")
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                return {
                    "success": True,
                    "message": f"Opened web search for: {query}"
                }

            elif action == "open_folder":
                folder_path = parameters.get("folder_path")
                folder_name = parameters.get("folder_name")
                success = self.gui.open_folder(folder_path=folder_path, folder_name=folder_name)
                if success:
                    target = folder_path if folder_path else folder_name
                    return {
                        "success": True,
                        "message": f"Opened folder: {target}"
                    }
                else:
                    # Include suggestions if available
                    base_msg = "Failed to open folder"
                    if folder_name:
                        base_msg = f"Failed to open folder: {folder_name}"

                    suggestions = self.gui.last_folder_suggestions
                    if suggestions:
                        suggestions_text = ", ".join(f"'{s}'" for s in suggestions[:5])
                        base_msg += f". Did you mean: {suggestions_text}?"

                    return {
                        "success": False,
                        "message": base_msg,
                        "suggestions": suggestions if suggestions else []
                    }

            elif action == "open_desktop_folder":
                folder_name = parameters.get("folder_name")
                success = self.gui.open_desktop_folder(folder_name=folder_name)
                if success:
                    msg = f"Opened Desktop folder: {folder_name}" if folder_name else "Opened Desktop"
                    return {
                        "success": True,
                        "message": msg
                    }
                else:
                    # Include suggestions if available
                    base_msg = f"Failed to open Desktop folder: {folder_name}" if folder_name else "Failed to open Desktop"
                    suggestions = self.gui.last_folder_suggestions
                    if suggestions:
                        suggestions_text = ", ".join(f"'{s}'" for s in suggestions[:5])
                        base_msg += f". Did you mean: {suggestions_text}?"
                    return {
                        "success": False,
                        "message": base_msg,
                        "suggestions": suggestions
                    }

            elif action == "open_desktop":
                success = self.gui.open_desktop_folder()
                return {
                    "success": success,
                    "message": "Opened Desktop" if success else "Failed to open Desktop"
                }

            elif action == "open_youtube":
                video_url = parameters.get("video_url", "")
                video_id = parameters.get("video_id", "")

                if video_url:
                    result = self.youtube.open_video_url(video_url)
                    return result
                elif video_id:
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    result = self.youtube.open_video_url(url)
                    return result
                else:
                    return {
                        "success": False,
                        "message": "No video URL or ID provided"
                    }

            elif action == "search_youtube":
                query = parameters.get("query", "")

                if not query:
                    return {
                        "success": False,
                        "message": "No search query provided"
                    }

                # Use smart YouTube automation for search
                result = self.youtube.search_only(query)
                return result

            elif action == "play_youtube_video":
                query = parameters.get("query", "")
                method = parameters.get("method", "auto")

                if not query:
                    return {
                        "success": False,
                        "message": "No search query provided"
                    }

                print(f"  🎬 Smart YouTube Player Activated")
                print(f"  🔍 Query: {query}")

                # Use the smart YouTube automation module
                result = self.youtube.smart_play_video(query, method)

                return result

            elif action == "play_first_result":
                wait_time = parameters.get("wait_time", 3)
                use_mouse = parameters.get("use_mouse", True)

                print(f"  ▶️  Playing first video from current search results...")
                result = self.youtube.play_first_result(wait_time, use_mouse)

                return result

            elif action == "search_and_play":
                query = parameters.get("query", "")
                wait_time = parameters.get("wait_time", 3)
                use_mouse = parameters.get("use_mouse", True)

                if not query:
                    return {
                        "success": False,
                        "message": "No search query provided"
                    }

                print(f"  🎬 Searching and playing: {query}")
                result = self.youtube.search_and_play(query, wait_time, use_mouse)

                return result

            elif action == "create_file":
                filename = parameters.get("filename", "")
                content = parameters.get("content", "")
                try:
                    with open(filename, 'w') as f:
                        f.write(content)
                    return {
                        "success": True,
                        "message": f"Created file: {filename}"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "message": f"Failed to create file: {str(e)}"
                    }

            elif action == "send_sms":
                contact_name = parameters.get("contact_name")
                phone = parameters.get("phone")
                message = parameters.get("message", "")
                result = self.messaging.send_sms(contact_name=contact_name, phone=phone, message=message)
                return result

            elif action == "send_email":
                contact_name = parameters.get("contact_name")
                email = parameters.get("email")
                subject = parameters.get("subject", "")
                body = parameters.get("body", "")
                result = self.messaging.send_email(contact_name=contact_name, email=email, subject=subject, body=body)
                return result

            elif action == "send_html_email":
                to = parameters.get("to", "")
                subject = parameters.get("subject", "")
                html_content = parameters.get("html_content", "")

                if not to or not subject:
                    return {
                        "success": False,
                        "message": "Email address and subject are required"
                    }

                result = self.email_sender.send_html_email(to, subject, html_content)
                return result

            elif action == "send_email_with_attachment":
                to = parameters.get("to", "")
                subject = parameters.get("subject", "")
                body = parameters.get("body", "")
                attachments = parameters.get("attachments", [])

                if not to or not subject:
                    return {
                        "success": False,
                        "message": "Email address and subject are required"
                    }

                result = self.email_sender.send_email(
                    to=[to],
                    subject=subject,
                    body=body,
                    attachments=attachments
                )
                return result

            elif action == "send_template_email":
                to = parameters.get("to", "")
                template = parameters.get("template", "")
                template_vars = parameters.get("template_vars", {})

                if not to or not template:
                    return {
                        "success": False,
                        "message": "Email address and template name are required"
                    }

                result = self.email_sender.send_template_email(to, template, **template_vars)
                return result

            elif action == "send_file":
                contact_name = parameters.get("contact_name", "")
                file_path = parameters.get("file_path", "")
                message = parameters.get("message", "")
                method = parameters.get("method", "auto")
                result = self.messaging.send_file(contact_name, file_path, message, method)
                return result

            elif action == "send_whatsapp":
                phone = parameters.get("phone", "")
                message = parameters.get("message", "")

                if not phone:
                    return {
                        "success": False,
                        "message": "No phone number provided"
                    }

                if not message:
                    return {
                        "success": False,
                        "message": "No message provided"
                    }

                result = self.whatsapp.send_message_instantly(phone, message)
                return result

            elif action == "send_whatsapp_scheduled":
                phone = parameters.get("phone", "")
                message = parameters.get("message", "")
                hour = parameters.get("hour", 0)
                minute = parameters.get("minute", 0)

                if not phone or not message:
                    return {
                        "success": False,
                        "message": "Phone number and message are required"
                    }

                result = self.whatsapp.send_message_scheduled(phone, message, hour, minute)
                return result

            elif action == "send_whatsapp_group":
                group_id = parameters.get("group_id", "")
                message = parameters.get("message", "")

                if not group_id or not message:
                    return {
                        "success": False,
                        "message": "Group ID and message are required"
                    }

                result = self.whatsapp.send_to_group_instantly(group_id, message)
                return result

            elif action == "send_whatsapp_image":
                phone = parameters.get("phone", "")
                image_path = parameters.get("image_path", "")
                caption = parameters.get("caption", "")

                if not phone or not image_path:
                    return {
                        "success": False,
                        "message": "Phone number and image path are required"
                    }

                result = self.whatsapp.send_image(phone, image_path, caption)
                return result

            elif action == "read_unread_emails":
                max_emails = parameters.get("max_emails", 10)
                result = self.chat_monitor.read_unread_emails(max_emails)

                if result["success"] and result["emails"]:
                    email_list = "\n\n".join([
                        f"📧 Email {i + 1}:\n"
                        f"  From: {email['from']}\n"
                        f"  Subject: {email['subject']}\n"
                        f"  Preview: {email['body']}"
                        for i, email in enumerate(result["emails"])
                    ])
                    return {
                        "success": True,
                        "message": f"📬 {result['message']}\n\n{email_list}",
                        "emails": result["emails"]
                    }
                else:
                    return result

            elif action == "read_sms_messages":
                max_messages = parameters.get("max_messages", 10)
                result = self.chat_monitor.read_sms_messages(max_messages)

                if result["success"] and result["messages"]:
                    sms_list = "\n\n".join([
                        f"📱 SMS {i + 1}:\n"
                        f"  From: {msg['from']}\n"
                        f"  Message: {msg['body']}"
                        for i, msg in enumerate(result["messages"])
                    ])
                    return {
                        "success": True,
                        "message": f"📨 {result['message']}\n\n{sms_list}",
                        "messages": result["messages"]
                    }
                else:
                    return result

            elif action == "monitor_chats":
                platforms = parameters.get("platforms", None)
                context = parameters.get("context", "professional")

                print(f"  📡 Monitoring chats and generating AI replies...")
                result = self.chat_monitor.monitor_and_suggest_replies(platforms, context)

                emails = result.get("emails", [])
                sms = result.get("sms", [])
                replies = result.get("suggested_replies", [])

                output = []

                if emails:
                    output.append(f"\n📧 Found {len(emails)} unread email(s)")
                if sms:
                    output.append(f"📱 Found {len(sms)} SMS message(s)")

                if replies:
                    output.append(f"\n🤖 Generated {len(replies)} AI reply suggestion(s):\n")
                    for i, reply in enumerate(replies):
                        output.append(f"Reply #{i}:")
                        output.append(f"  To: {reply['recipient']}")
                        output.append(f"  Platform: {reply['platform']}")
                        output.append(f"  Suggested Reply:\n  {reply['suggested_reply']}\n")

                    output.append("\n💡 Use 'approve reply [number]' to send a suggested reply")
                    output.append("💡 Use 'show pending replies' to see all suggestions again")
                else:
                    output.append("\n✅ No new messages to reply to")

                return {
                    "success": True,
                    "message": "\n".join(output),
                    "result": result
                }

            elif action == "generate_ai_reply":
                platform = parameters.get("platform", "email")
                sender = parameters.get("sender", "")
                message_body = parameters.get("message", "")
                subject = parameters.get("subject", "")
                context = parameters.get("context", "professional")

                message_data = {
                    "platform": platform,
                    "from": sender,
                    "body": message_body,
                    "subject": subject
                }

                print(f"  🤖 Generating AI reply...")
                result = self.chat_monitor.generate_ai_reply(message_data, context)

                if result.get("success"):
                    return {
                        "success": True,
                        "message": f"✅ AI Reply Generated:\n\n{result['suggested_reply']}\n\n💡 Use 'approve reply 0' to send this",
                        "reply_data": result
                    }
                else:
                    return result

            elif action == "show_pending_replies":
                pending = self.chat_monitor.get_pending_replies()

                if not pending:
                    return {
                        "success": True,
                        "message": "No pending replies. Use 'monitor chats' to check for new messages."
                    }

                output = [f"📋 You have {len(pending)} pending reply suggestion(s):\n"]
                for i, reply in enumerate(pending):
                    output.append(f"Reply #{i}:")
                    output.append(f"  To: {reply['recipient']}")
                    output.append(f"  Platform: {reply['platform']}")
                    output.append(f"  Suggested Reply:\n  {reply['suggested_reply']}\n")

                output.append("💡 Use 'approve reply [number]' to send")
                output.append("💡 Use 'clear pending replies' to remove all")

                return {
                    "success": True,
                    "message": "\n".join(output),
                    "pending_replies": pending
                }

            elif action == "approve_reply":
                reply_index = parameters.get("index", 0)
                send_now = parameters.get("send_now", True)

                result = self.chat_monitor.approve_and_send_reply(reply_index, send_now)
                return result

            elif action == "clear_pending_replies":
                result = self.chat_monitor.clear_pending_replies()
                return result

            elif action == "chat_summary":
                summary = self.chat_monitor.get_chat_summary()

                output = [
                    "📊 Chat Monitor Summary:",
                    f"  📧 Emails monitored: {summary['total_emails_monitored']}",
                    f"  📱 SMS monitored: {summary['total_sms_monitored']}",
                    f"  🤖 Pending replies: {summary['pending_replies']}",
                    f"  ✅ Gmail: {'Enabled' if summary['gmail_enabled'] else 'Not configured'}",
                    f"  ✅ SMS: {'Enabled' if summary['sms_enabled'] else 'Not configured'}"
                ]

                return {
                    "success": True,
                    "message": "\n".join(output),
                    "summary": summary
                }

            elif action == "visual_monitor_gmail":
                context = parameters.get("context", "professional")
                auto_send = parameters.get("auto_send", False)

                result = self.visual_chat_monitor.monitor_and_reply_visually(context, auto_send)
                return result

            elif action == "open_gmail_browser":
                result = self.visual_chat_monitor.open_gmail_in_browser()
                return result

            elif action == "read_emails_from_screen":
                result = self.visual_chat_monitor.read_emails_from_screen()

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"✅ Emails read from screen:\n\n{result['analysis']}"
                    }
                return result

            elif action == "read_email_on_screen":
                email_number = parameters.get("email_number", 1)
                result = self.visual_chat_monitor.read_specific_email_on_screen(email_number)

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"✅ Email content:\n\n{result['content']}"
                    }
                return result

            elif action == "open_whatsapp_web":
                result = self.visual_chat_monitor.open_whatsapp_web()
                return result

            elif action == "read_whatsapp_screen":
                result = self.visual_chat_monitor.read_whatsapp_from_screen()

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"✅ WhatsApp analysis:\n\n{result['analysis']}"
                    }
                return result

            elif action == "smart_analyze_screen":
                focus = parameters.get("focus", "general")
                result = self.smart_screen_monitor.analyze_current_screen(focus)

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"👁️ Screen Analysis:\n\n{result['analysis']}"
                    }
                return result

            elif action == "detect_screen_changes":
                interval = parameters.get("interval", 5)
                duration = parameters.get("duration", 30)
                result = self.smart_screen_monitor.detect_screen_changes(interval, duration)

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"📊 Screen Changes Detected:\n\n{result['changes']}"
                    }
                return result

            elif action == "monitor_for_content":
                target = parameters.get("target", "")
                check_interval = parameters.get("check_interval", 10)
                max_checks = parameters.get("max_checks", 6)

                if not target:
                    return {
                        "success": False,
                        "message": "No target content specified"
                    }

                result = self.smart_screen_monitor.monitor_for_specific_content(target, check_interval, max_checks)

                if result.get("found"):
                    return {
                        "success": True,
                        "message": f"✅ Found: {result['details']}"
                    }
                else:
                    return {
                        "success": True,
                        "message": f"⏸️ {result['message']}"
                    }

            elif action == "productivity_check":
                result = self.smart_screen_monitor.get_productivity_insights()

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"📊 Productivity Check:\n\n{result['analysis']}"
                    }
                return result

            elif action == "check_screen_errors":
                result = self.smart_screen_monitor.check_for_errors()

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"🔍 Error Check:\n\n{result['analysis']}"
                    }
                return result

            elif action == "analyze_screen_code":
                result = self.smart_screen_monitor.analyze_code_on_screen()

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"💻 Code Analysis:\n\n{result['analysis']}"
                    }
                return result

            elif action == "ask_about_screen":
                question = parameters.get("question", "")

                if not question:
                    return {
                        "success": False,
                        "message": "No question provided"
                    }

                result = self.smart_screen_monitor.smart_screenshot_with_context(question)

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"❓ Q: {result['question']}\n\n💡 A: {result['answer']}"
                    }
                return result

            elif action == "add_contact":
                name = parameters.get("name", "")
                phone = parameters.get("phone")
                email = parameters.get("email")
                success = self.contact_manager.add_contact(name, phone, email)
                return {
                    "success": success,
                    "message": f"Added contact: {name}" if success else f"Failed to add contact: {name}"
                }

            elif action == "list_contacts":
                contacts = self.contact_manager.list_contacts()
                if contacts:
                    contact_list = "\n".join([
                        f"  • {c['name']} - Phone: {c['phone'] or 'N/A'}, Email: {c['email'] or 'N/A'}"
                        for c in contacts
                    ])
                    return {
                        "success": True,
                        "message": f"Contacts:\n{contact_list}"
                    }
                else:
                    return {
                        "success": True,
                        "message": "No contacts found. Use 'add contact' to create one."
                    }

            elif action == "get_contact":
                name = parameters.get("name", "")
                contact = self.contact_manager.get_contact(name)
                if contact:
                    return {
                        "success": True,
                        "message": f"Contact: {contact['name']}\n  Phone: {contact['phone'] or 'N/A'}\n  Email: {contact['email'] or 'N/A'}"
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Contact not found: {name}"
                    }

            elif action == "generate_code":
                description = parameters.get("description", "")
                language = parameters.get("language", None)

                if not description:
                    return {
                        "success": False,
                        "message": "No code description provided"
                    }

                print(f"  🤖 Generating code for: {description}...")
                result = generate_code(description, language)

                if result.get("success"):
                    code = result["code"]
                    detected_lang = result["language"]
                    source = result.get("source", "ai")

                    if source == "template":
                        print(f"  ⚡ Using built-in template (instant!)")

                    print(f"\n{'=' * 60}")
                    print(f"  Generated {detected_lang.upper()} Code:")
                    print(f"{'=' * 60}")
                    print(code)
                    print(f"{'=' * 60}\n")

                    return {
                        "success": True,
                        "message": f"✅ Generated {detected_lang} code successfully!",
                        "generated_code": code,
                        "language": detected_lang
                    }
                else:
                    return {
                        "success": False,
                        "message": f"❌ Error: {result.get('error', 'Code generation failed')}"
                    }

            elif action == "write_code_to_editor":
                description = parameters.get("description", "")
                language = parameters.get("language", None)
                editor = parameters.get("editor", "notepad")

                if not description:
                    return {
                        "success": False,
                        "message": "No code description provided"
                    }

                print(f"  🤖 Generating code for: {description}...")
                result = generate_code(description, language)

                if not result.get("success"):
                    return {
                        "success": False,
                        "message": f"❌ Code generation failed: {result.get('error', 'Unknown error')}"
                    }

                code = result["code"]
                detected_lang = result["language"]
                source = result.get("source", "ai")

                if source == "template":
                    print(f"  ⚡ Using built-in template (instant!)")

                print(f"\n  ✅ Generated {detected_lang} code ({len(code)} characters)")
                print(f"  📝 Opening {editor}...")

                self.gui.open_application(editor)
                time.sleep(2)

                print(f"  📋 Copying code to clipboard...")
                self.gui.copy_to_clipboard(code)
                time.sleep(0.5)

                print(f"  📝 Pasting code into editor...")
                self.gui.paste_from_clipboard()

                print(f"  ✅ Done! Code written to {editor}")

                return {
                    "success": True,
                    "message": f"✅ Generated and wrote {detected_lang} code to {editor}!",
                    "generated_code": code,
                    "language": detected_lang
                }

            elif action == "explain_code":
                code = parameters.get("code", "")
                language = parameters.get("language", "python")

                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to explain"
                    }

                print(f"  🤔 Analyzing {language} code...")
                explanation = explain_code(code, language)

                print(f"\n{'=' * 60}")
                print(f"  Code Explanation:")
                print(f"{'=' * 60}")
                print(explanation)
                print(f"{'=' * 60}\n")

                return {
                    "success": True,
                    "message": "Code explained successfully",
                    "explanation": explanation
                }

            elif action == "improve_code":
                code = parameters.get("code", "")
                language = parameters.get("language", "python")

                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to improve"
                    }

                print(f"  🔧 Improving {language} code...")
                result = improve_code(code, language)

                if result.get("success"):
                    improved = result["code"]

                    print(f"\n{'=' * 60}")
                    print(f"  Improved Code:")
                    print(f"{'=' * 60}")
                    print(improved)
                    print(f"{'=' * 60}\n")

                    return {
                        "success": True,
                        "message": "Code improved successfully",
                        "improved_code": improved
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Error: {result.get('error')}"
                    }

            elif action == "debug_code":
                code = parameters.get("code", "")
                error_message = parameters.get("error_message", "")
                language = parameters.get("language", "python")

                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to debug"
                    }

                print(f"  🐛 Debugging {language} code...")
                result = debug_code(code, error_message, language)

                if result.get("success"):
                    fixed = result["code"]

                    print(f"\n{'=' * 60}")
                    print(f"  Fixed Code:")
                    print(f"{'=' * 60}")
                    print(fixed)
                    print(f"{'=' * 60}\n")

                    return {
                        "success": True,
                        "message": "Code debugged and fixed",
                        "fixed_code": fixed
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Error: {result.get('error')}"
                    }

            elif action == "analyze_screenshot":
                image_path = parameters.get("image_path", "screenshot.png")
                query = parameters.get("query", "Describe what you see")

                print(f"  🔍 Analyzing screenshot: {image_path}...")
                analysis = analyze_screenshot(image_path, query)

                print(f"\n{'=' * 60}")
                print(f"  Screenshot Analysis:")
                print(f"{'=' * 60}")
                print(analysis)
                print(f"{'=' * 60}\n")

                return {
                    "success": True,
                    "message": "Screenshot analyzed",
                    "analysis": analysis
                }

            elif action == "extract_text":
                image_path = parameters.get("image_path", "screenshot.png")

                print(f"  📝 Extracting text from: {image_path}...")
                text = extract_text_from_screenshot(image_path)

                print(f"\n  Extracted Text:\n{text}\n")

                return {
                    "success": True,
                    "message": "Text extracted from screenshot",
                    "text": text
                }

            elif action == "suggest_screen_improvements":
                result = self.screen_suggester.analyze_and_suggest()
                return {
                    "success": True,
                    "message": "AI suggestions generated",
                    "suggestions": result
                }

            elif action == "check_screen_errors":
                result = self.screen_suggester.check_for_errors()
                return {
                    "success": True,
                    "message": "Screen checked for errors",
                    "errors": result
                }

            elif action == "get_screen_tips":
                result = self.screen_suggester.get_quick_tips()
                return {
                    "success": True,
                    "message": "Quick tips generated",
                    "tips": result
                }

            elif action == "analyze_screen_code":
                result = self.screen_suggester.analyze_code()
                return {
                    "success": True,
                    "message": "Code analyzed",
                    "analysis": result
                }

            elif action == "analyze_screen_design":
                result = self.screen_suggester.analyze_website()
                return {
                    "success": True,
                    "message": "Design analyzed",
                    "analysis": result
                }

            elif action == "system_report":
                print(f"  📊 Generating system report...")
                report = get_full_system_report()

                print(report)

                return {
                    "success": True,
                    "message": "System report generated",
                    "report": report
                }

            elif action == "check_cpu":
                cpu = get_cpu_usage()
                msg = f"CPU Usage: {cpu['usage_percent']}% ({cpu['status']})"
                print(f"  {msg}")
                return {"success": True, "message": msg, "data": cpu}

            elif action == "check_memory":
                mem = get_memory_usage()
                msg = f"Memory: {mem['used_gb']}/{mem['total_gb']} ({mem['usage_percent']}% - {mem['status']})"
                print(f"  {msg}")
                return {"success": True, "message": msg, "data": mem}

            elif action == "check_disk":
                disk = get_disk_usage()
                msg = f"Disk: {disk['used_gb']}/{disk['total_gb']} ({disk['usage_percent']}% - {disk['status']})"
                print(f"  {msg}")
                return {"success": True, "message": msg, "data": disk}

            elif action == "search_files":
                pattern = parameters.get("pattern", "*")
                directory = parameters.get("directory", ".")

                print(f"  🔍 Searching for files: {pattern}")
                files = search_files(pattern, directory)

                msg = f"Found {len(files)} files matching '{pattern}'"
                print(f"\n  {msg}")
                for f in files[:20]:
                    print(f"    • {f}")
                if len(files) > 20:
                    print(f"    ... and {len(files) - 20} more")

                return {
                    "success": True,
                    "message": msg,
                    "files": files
                }

            elif action == "find_large_files":
                directory = parameters.get("directory", ".")
                min_size = parameters.get("min_size_mb", 10)

                print(f"  🔍 Finding large files (>{min_size}MB)...")
                large_files = find_large_files(directory, min_size)

                print(f"\n  Found {len(large_files)} large files:")
                for f in large_files[:10]:
                    print(f"    • {f['size_mb']} - {f['path']}")

                return {
                    "success": True,
                    "message": f"Found {len(large_files)} large files",
                    "files": large_files
                }

            elif action == "directory_size":
                directory = parameters.get("directory", ".")

                print(f"  📊 Calculating directory size...")
                size_info = get_directory_size(directory)

                msg = f"{directory}: {size_info['total_size_gb']} ({size_info['file_count']} files)"
                print(f"  {msg}")

                return {
                    "success": True,
                    "message": msg,
                    "data": size_info
                }

            elif action == "save_workflow":
                name = parameters.get("name", "")
                steps = parameters.get("steps", [])
                description = parameters.get("description", "")

                if not name or not steps:
                    return {
                        "success": False,
                        "message": "Workflow name and steps required"
                    }

                success = self.workflow_manager.save_workflow(name, steps, description)
                return {
                    "success": success,
                    "message": f"Workflow '{name}' saved" if success else "Failed to save workflow"
                }

            elif action == "load_workflow":
                name = parameters.get("name", "")

                workflow = self.workflow_manager.load_workflow(name)
                if workflow:
                    return self.execute_workflow(workflow["steps"])
                else:
                    return {
                        "success": False,
                        "message": f"Workflow '{name}' not found"
                    }

            elif action == "list_workflows":
                workflows = self.workflow_manager.list_workflows()

                print(f"\n  📋 Saved Workflows ({len(workflows)}):")
                for w in workflows:
                    print(
                        f"    • {w['name']}: {w['description']} ({w['steps_count']} steps, used {w['usage_count']} times)")

                return {
                    "success": True,
                    "message": f"Found {len(workflows)} workflows",
                    "workflows": workflows
                }

            elif action == "show_history":
                history = self.memory.get_recent_history(10)

                print(f"\n  📜 Recent Command History:")
                for entry in history:
                    status = "✅" if entry["result"]["success"] else "❌"
                    print(f"    {status} {entry['user_input']}")

                return {
                    "success": True,
                    "message": f"Showing {len(history)} recent commands",
                    "history": history
                }

            elif action == "show_statistics":
                stats = self.memory.get_statistics()

                msg = f"Total: {stats['total_commands']}, Success: {stats['successful']}, Failed: {stats['failed']}, Success Rate: {stats['success_rate']}"
                print(f"\n  📊 Statistics: {msg}")

                return {
                    "success": True,
                    "message": msg,
                    "statistics": stats
                }

            elif action == "execute_code":
                code = parameters.get("code", "")
                language = parameters.get("language", "python").lower()

                if not code:
                    return {
                        "success": False,
                        "message": "No code provided to execute"
                    }

                safety_check = validate_code_safety(code, language)
                if not safety_check["is_safe"]:
                    return {
                        "success": False,
                        "message": f"Code safety check failed: {', '.join(safety_check['warnings'])}"
                    }

                print(f"  ▶️  Executing {language} code...")

                if language == "python":
                    result = execute_python_code(code)
                elif language == "javascript":
                    result = execute_javascript_code(code)
                else:
                    return {
                        "success": False,
                        "message": f"Execution not supported for {language}"
                    }

                if result["success"]:
                    print(f"\n  ✅ Output:\n{result['output']}")
                    return {
                        "success": True,
                        "message": "Code executed successfully",
                        "output": result["output"]
                    }
                else:
                    print(f"\n  ❌ Error:\n{result['error']}")
                    return {
                        "success": False,
                        "message": f"Execution failed: {result['error']}"
                    }

            elif action == "mute_mic":
                result = self.system_control.mute_microphone()
                return {"success": True, "message": result}

            elif action == "unmute_mic":
                result = self.system_control.unmute_microphone()
                return {"success": True, "message": result}

            elif action == "set_brightness":
                level = parameters.get("level", 50)
                result = self.system_control.set_brightness(level)
                return {"success": True, "message": result}

            elif action == "auto_brightness":
                result = self.system_control.auto_brightness()
                return {"success": True, "message": result}

            elif action == "schedule_sleep":
                time_str = parameters.get("time", "23:00")
                result = self.system_control.schedule_sleep(time_str)
                return {"success": True, "message": result}

            elif action == "lock_screen":
                result = self.system_control.lock_screen()
                return {"success": True, "message": result}

            elif action == "shutdown_system":
                delay_seconds = parameters.get("delay_seconds", 10)
                result = self.system_control.shutdown_system(delay_seconds)
                return {"success": True, "message": result}

            elif action == "restart_system":
                delay_seconds = parameters.get("delay_seconds", 10)
                result = self.system_control.restart_system(delay_seconds)
                return {"success": True, "message": result}

            elif action == "cancel_shutdown":
                result = self.system_control.cancel_shutdown_restart()
                return {"success": True, "message": result}

            elif action == "clear_temp_files":
                result = self.system_control.clear_temp_files()
                return {"success": True, "message": result}

            elif action == "check_disk_space":
                result = self.system_control.check_disk_space()
                return {"success": True, "message": result}

            elif action == "open_apps_scheduled":
                time_str = parameters.get("time", "09:00")
                apps = parameters.get("apps", [])
                result = self.app_scheduler.open_apps_at_time(time_str, apps)
                return {"success": True, "message": result}

            elif action == "close_heavy_apps":
                result = self.app_scheduler.detect_idle_and_close_heavy_apps()
                return {"success": True, "message": result}

            elif action == "get_heavy_apps":
                result = self.app_scheduler.get_heavy_apps()
                return {"success": True, "message": result}

            elif action == "close_app":
                app_name = parameters.get("app_name", "")
                result = self.app_scheduler.close_app(app_name)
                return {"success": True, "message": result}

            elif action == "organize_downloads":
                result = self.download_organizer.organize_downloads()
                return {"success": True, "message": result}

            elif action == "enable_auto_organize":
                result = self.download_organizer.enable_auto_organize()
                return {"success": True, "message": result}

            elif action == "listen_voice":
                command = self.voice_assistant.listen_once()
                return {"success": True, "message": f"Heard: {command}"}

            elif action == "expand_snippet":
                shortcut = parameters.get("shortcut", "")
                text = self.smart_typing.get_snippet(shortcut)
                if text:
                    import pyperclip
                    pyperclip.copy(text)
                    return {"success": True, "message": f"Snippet copied: {text[:50]}..."}
                return {"success": False, "message": f"Snippet not found: {shortcut}"}

            elif action == "list_snippets":
                result = self.smart_typing.list_snippets()
                return {"success": True, "message": result}

            elif action == "generate_email_template":
                email_type = parameters.get("type", "professional")
                result = self.smart_typing.generate_email_template(email_type)
                return {"success": True, "message": result}

            elif action == "auto_rename_files":
                folder = parameters.get("folder", ".")
                pattern = parameters.get("pattern", "clean")
                result = self.file_manager.auto_rename_files(folder, pattern)
                return {"success": True, "message": result}

            elif action == "find_duplicates":
                folder = parameters.get("folder", ".")
                result = self.file_manager.find_duplicates(folder)
                return {"success": True, "message": result}

            elif action == "compress_old_files":
                folder = parameters.get("folder", ".")
                days = parameters.get("days_old", 90)
                result = self.file_manager.compress_old_files(folder, days)
                return {"success": True, "message": result}

            elif action == "backup_folder":
                source = parameters.get("source", ".")
                result = self.file_manager.backup_folder(source)
                return {"success": True, "message": result}

            elif action == "get_clipboard_history":
                limit = parameters.get("limit", 10)
                result = self.web_automation.get_clipboard_history(limit)
                return {"success": True, "message": result}

            elif action == "search_clipboard":
                query = parameters.get("query", "")
                result = self.web_automation.search_clipboard_history(query)
                return {"success": True, "message": result}

            elif action == "list_scrapers":
                result = self.web_automation.list_scrapers()
                return {"success": True, "message": result}

            elif action == "screen_time_dashboard":
                days = parameters.get("days", 7)
                result = self.productivity_monitor.get_screen_time_dashboard(days)
                return {"success": True, "message": result}

            elif action == "block_distractions":
                result = self.productivity_monitor.block_distractions()
                return {"success": True, "message": result}

            elif action == "enable_focus_mode":
                hours = parameters.get("hours", 2)
                result = self.productivity_monitor.enable_focus_mode(hours)
                return {"success": True, "message": result}

            elif action == "productivity_score":
                result = self.productivity_monitor.get_productivity_score()
                return {"success": True, "message": result}

            elif action == "send_reminder":
                reminder_type = parameters.get("type", "water")
                result = self.productivity_monitor.send_reminder(reminder_type)
                return {"success": True, "message": result}

            elif action == "daily_summary":
                result = self.productivity_monitor.generate_daily_summary()
                return {"success": True, "message": result}

            elif action == "get_compliment":
                result = self.fun_features.get_random_compliment()
                return {"success": True, "message": result}

            elif action == "celebrate_task":
                result = self.fun_features.celebrate_task_completion()
                return {"success": True, "message": result}

            elif action == "set_mood":
                mood = parameters.get("mood", "neutral")
                result = self.fun_features.set_mood_theme(mood)
                return {"success": True, "message": result}

            elif action == "chatbot":
                user_input = parameters.get("message", "")
                result = self.fun_features.chatbot_respond(user_input)
                return {"success": True, "message": result}

            elif action == "spotify_play":
                uri = parameters.get("uri")
                result = self.spotify.play(uri)
                return result

            elif action == "spotify_pause":
                result = self.spotify.pause()
                return result

            elif action == "spotify_next":
                result = self.spotify.next_track()
                return result

            elif action == "spotify_previous":
                result = self.spotify.previous_track()
                return result

            elif action == "spotify_volume":
                volume = parameters.get("volume", 50)
                result = self.spotify.set_volume(volume)
                return result

            elif action == "spotify_current":
                result = self.spotify.get_current_track()
                return result

            elif action == "spotify_search":
                query = parameters.get("query", "")
                search_type = parameters.get("type", "track")
                limit = parameters.get("limit", 5)
                if not query:
                    return {"success": False, "message": "No search query provided"}
                result = self.spotify.search(query, search_type, limit)
                return result

            elif action == "spotify_play_track":
                query = parameters.get("query", "")
                if not query:
                    return {"success": False, "message": "No song/artist specified"}
                result = self.spotify.play_track(query)
                return result

            elif action == "spotify_playlists":
                limit = parameters.get("limit", 20)
                result = self.spotify.get_playlists(limit)
                return result

            elif action == "spotify_shuffle":
                state = parameters.get("state", True)
                result = self.spotify.shuffle(state)
                return result

            elif action == "spotify_repeat":
                state = parameters.get("state", "context")
                result = self.spotify.repeat(state)
                return result

            elif action == "spotify_open":
                result = self.spotify.open_spotify()
                return result

            elif action == "spotify_volume_up":
                steps = parameters.get("steps", 1)
                result = self.spotify.volume_up(steps)
                return result

            elif action == "spotify_volume_down":
                steps = parameters.get("steps", 1)
                result = self.spotify.volume_down(steps)
                return result

            elif action == "spotify_mute":
                result = self.spotify.mute()
                return result

            elif action == "get_weather":
                city = parameters.get("city", "New York")
                result = self.weather_news.get_weather(city)
                return {"success": True, "message": result}

            elif action == "get_forecast":
                city = parameters.get("city", "New York")
                days = parameters.get("days", 3)
                result = self.weather_news.get_forecast(city, days)
                return {"success": True, "message": result}

            elif action == "get_news":
                category = parameters.get("category", "general")
                count = parameters.get("count", 5)
                result = self.weather_news.get_news_headlines(category, count)
                return {"success": True, "message": result}

            elif action == "translate_text":
                text = parameters.get("text", "")
                target_lang = parameters.get("target_lang", "es")
                source_lang = parameters.get("source_lang", "auto")
                result = self.translator.translate(text, target_lang, source_lang)
                return {"success": True, "message": result}

            elif action == "detect_language":
                text = parameters.get("text", "")
                result = self.translator.detect_language(text)
                return {"success": True, "message": result}

            elif action == "list_languages":
                result = self.translator.get_supported_languages()
                return {"success": True, "message": result}

            elif action == "calculate":
                expression = parameters.get("expression", "")
                result = self.calculator.calculate(expression)
                return {"success": True, "message": result}

            elif action == "convert_units":
                value = parameters.get("value", 0)
                from_unit = parameters.get("from_unit", "")
                to_unit = parameters.get("to_unit", "")
                result = self.calculator.convert_units(value, from_unit, to_unit)
                return {"success": True, "message": result}

            elif action == "convert_currency":
                amount = parameters.get("amount", 0)
                from_currency = parameters.get("from_currency", "USD")
                to_currency = parameters.get("to_currency", "EUR")
                result = self.calculator.convert_currency(amount, from_currency, to_currency)
                return {"success": True, "message": result}

            elif action == "get_currency_rate":
                from_currency = parameters.get("from_currency", "USD")
                to_currency = parameters.get("to_currency", "EUR")
                result = self.calculator.get_currency_rate(from_currency, to_currency)
                return {"success": True, "message": result}

            elif action == "add_password":
                name = parameters.get("name", "")
                username = parameters.get("username", "")
                password = parameters.get("password", "")
                url = parameters.get("url", "")
                result = self.password_vault.add_password(name, username, password, url)
                return {"success": True, "message": result}

            elif action == "get_password":
                name = parameters.get("name", "")
                result = self.password_vault.get_password(name)
                return {"success": True, "message": result}

            elif action == "list_passwords":
                result = self.password_vault.list_passwords()
                return {"success": True, "message": result}

            elif action == "generate_password":
                length = parameters.get("length", 16)
                result = self.password_vault.generate_strong_password(length)
                return {"success": True, "message": result}

            elif action == "delete_password":
                name = parameters.get("name", "")
                result = self.password_vault.delete_password(name)
                return {"success": True, "message": result}

            elif action == "add_note":
                content = parameters.get("content", "")
                category = parameters.get("category", "general")
                tags = parameters.get("tags", [])
                result = self.notes.add_note(content, category, tags)
                return {"success": True, "message": result}

            elif action == "list_notes":
                category = parameters.get("category", None)
                result = self.notes.list_notes(category)
                return {"success": True, "message": result}

            elif action == "search_notes":
                query = parameters.get("query", "")
                result = self.notes.search_notes(query)
                return {"success": True, "message": result}

            elif action == "delete_note":
                note_id = parameters.get("id", 0)
                result = self.notes.delete_note(note_id)
                return {"success": True, "message": result}

            elif action == "pin_note":
                note_id = parameters.get("id", 0)
                result = self.notes.pin_note(note_id)
                return {"success": True, "message": result}

            elif action == "add_event":
                title = parameters.get("title", "")
                date = parameters.get("date", "")
                event_time = parameters.get("time", "")
                duration = parameters.get("duration", 60)
                description = parameters.get("description", "")
                result = self.calendar.add_event(title, date, event_time, duration, description)
                return {"success": True, "message": result}

            elif action == "list_events":
                days = parameters.get("days", 7)
                result = self.calendar.list_events(days)
                return {"success": True, "message": result}

            elif action == "today_events":
                result = self.calendar.get_today_events()
                return {"success": True, "message": result}

            elif action == "search_events":
                query = parameters.get("query", "")
                result = self.calendar.search_events(query)
                return {"success": True, "message": result}

            elif action == "delete_event":
                event_id = parameters.get("id", 0)
                result = self.calendar.delete_event(event_id)
                return {"success": True, "message": result}

            elif action == "ecosystem_dashboard":
                result = self.ecosystem.get_unified_dashboard()
                return {"success": True, "message": result}

            elif action == "morning_briefing":
                result = self.ecosystem.morning_briefing()
                return {"success": True, "message": result}

            elif action == "evening_summary":
                result = self.ecosystem.evening_summary()
                return {"success": True, "message": result}

            elif action == "smart_search":
                query = parameters.get("query", "")
                result = self.ecosystem.smart_search(query)
                return {"success": True, "message": result}

            elif action == "auto_organize":
                result = self.ecosystem.auto_organize()
                return {"success": True, "message": result}

            elif action == "productivity_insights":
                result = self.ecosystem.get_productivity_insights()
                return {"success": True, "message": result}

            elif action == "create_workflow":
                name = parameters.get("name", "")
                actions = parameters.get("actions", [])
                result = self.ecosystem.create_workflow(name, actions)
                return {"success": True, "message": result}

            elif action == "list_workflows":
                result = self.ecosystem.list_workflows()
                return {"success": True, "message": result}

            elif action == "run_workflow":
                name = parameters.get("name", "")
                result = self.ecosystem.run_workflow(name)
                return {"success": True, "message": result}

            elif action == "smart_suggestions":
                suggestions = self.ecosystem.generate_smart_suggestions()
                result = "\n💡 SMART SUGGESTIONS:\n" + "=" * 50 + "\n"
                for i, suggestion in enumerate(suggestions, 1):
                    result += f"{i}. {suggestion}\n"
                result += "=" * 50
                return {"success": True, "message": result}

            elif action == "launch_web_tools":
                result = self.web_tools.launch_web_app()
                if result["success"]:
                    webbrowser.open(result["url"])
                return result

            elif action == "open_web_tool":
                category = parameters.get("category", "")
                tool_name = parameters.get("tool", None)

                if not category:
                    return {
                        "success": False,
                        "message": "❌ No tool category specified"
                    }

                result = self.web_tools.open_web_tool(category, tool_name)
                return result

            elif action == "list_web_tools":
                result = self.web_tools.list_available_tools()
                return result

            elif action == "web_tools_status":
                result = self.web_tools.get_status()
                return result

            elif action == "stop_web_tools":
                result = self.web_tools.stop_web_app()
                return result

            elif action == "parse_web_tool_command":
                query = parameters.get("query", "")
                if not query:
                    return {
                        "success": False,
                        "message": "❌ No query provided"
                    }

                parsed = self.tools_mapper.parse_command(query)

                if parsed["category"]:
                    result = self.web_tools.open_web_tool(parsed["category"], parsed["tool"])
                    return result
                else:
                    return {
                        "success": False,
                        "message": f"❌ Could not find a matching tool for: {query}"
                    }

            elif action == "conversational_ai":
                message = parameters.get("message", "")
                context = parameters.get("context", "general")
                result = self.ai_features.conversational_ai(message, context)
                return {"success": True, "message": result}

            elif action == "customer_service_bot":
                query = parameters.get("query", "")
                company_context = parameters.get("company_context", "")
                result = self.ai_features.customer_service_bot(query, company_context)
                return {"success": True, "message": result}

            elif action == "educational_assistant":
                topic = parameters.get("topic", "")
                question = parameters.get("question", "")
                level = parameters.get("level", "intermediate")
                result = self.ai_features.educational_assistant(topic, question, level)
                return {"success": True, "message": result}

            elif action == "domain_expert":
                domain = parameters.get("domain", "")
                question = parameters.get("question", "")
                result = self.ai_features.domain_expert(domain, question)
                return {"success": True, "message": result}

            elif action == "story_writer":
                prompt = parameters.get("prompt", "")
                genre = parameters.get("genre", "general")
                length = parameters.get("length", "medium")
                result = self.ai_features.story_writer(prompt, genre, length)
                return {"success": True, "message": result}

            elif action == "content_creator":
                topic = parameters.get("topic", "")
                content_type = parameters.get("content_type", "blog post")
                tone = parameters.get("tone", "professional")
                result = self.ai_features.content_creator(topic, content_type, tone)
                return {"success": True, "message": result}

            elif action == "article_generator":
                title = parameters.get("title", "")
                keywords = parameters.get("keywords", [])
                word_count = parameters.get("word_count", 800)
                result = self.ai_features.article_generator(title, keywords, word_count)
                return {"success": True, "message": result}

            elif action == "copywriting_assistant":
                product = parameters.get("product", "")
                goal = parameters.get("goal", "persuade")
                result = self.ai_features.copywriting_assistant(product, goal)
                return {"success": True, "message": result}

            elif action == "technical_writer":
                topic = parameters.get("topic", "")
                audience = parameters.get("audience", "technical")
                result = self.ai_features.technical_writer(topic, audience)
                return {"success": True, "message": result}

            elif action == "text_translator":
                text = parameters.get("text", "")
                target_language = parameters.get("target_language", "")
                source_language = parameters.get("source_language", "auto")
                result = self.ai_features.text_translator(text, target_language, source_language)
                return {"success": True, "message": result}

            elif action == "sentiment_analysis":
                text = parameters.get("text", "")
                result = self.ai_features.sentiment_analysis(text)
                return {"success": True, "message": result}

            elif action == "text_summarizer":
                text = parameters.get("text", "")
                length = parameters.get("length", "medium")
                result = self.ai_features.text_summarizer(text, length)
                return {"success": True, "message": result}

            elif action == "language_detector":
                text = parameters.get("text", "")
                result = self.ai_features.language_detector(text)
                return {"success": True, "message": result}

            elif action == "content_moderator":
                text = parameters.get("text", "")
                result = self.ai_features.content_moderator(text)
                return {"success": True, "message": result}

            elif action == "image_description_generator":
                concept = parameters.get("concept", "")
                style = parameters.get("style", "realistic")
                result = self.ai_features.image_description_generator(concept, style)
                return {"success": True, "message": result}

            elif action == "style_transfer_description":
                content = parameters.get("content", "")
                style = parameters.get("style", "")
                result = self.ai_features.style_transfer_description(content, style)
                return {"success": True, "message": result}

            elif action == "analyze_data_patterns":
                data_description = parameters.get("data_description", "")
                result = self.ai_features.analyze_data_patterns(data_description)
                return {"success": True, "message": result}

            elif action == "trend_analysis":
                data_description = parameters.get("data_description", "")
                time_period = parameters.get("time_period", "")
                result = self.ai_features.trend_analysis(data_description, time_period)
                return {"success": True, "message": result}

            elif action == "predictive_modeling":
                scenario = parameters.get("scenario", "")
                variables = parameters.get("variables", [])
                result = self.ai_features.predictive_modeling(scenario, variables)
                return {"success": True, "message": result}

            elif action == "data_insights":
                data_description = parameters.get("data_description", "")
                result = self.ai_features.data_insights(data_description)
                return {"success": True, "message": result}

            elif action == "statistical_analysis":
                data_description = parameters.get("data_description", "")
                result = self.ai_features.statistical_analysis(data_description)
                return {"success": True, "message": result}

            elif action == "image_recognition_guide":
                image_description = parameters.get("image_description", "")
                result = self.ai_features.image_recognition_guide(image_description)
                return {"success": True, "message": result}

            elif action == "object_detection_guide":
                scenario = parameters.get("scenario", "")
                result = self.ai_features.object_detection_guide(scenario)
                return {"success": True, "message": result}

            elif action == "scene_analysis_guide":
                scene_type = parameters.get("scene_type", "")
                result = self.ai_features.scene_analysis_guide(scene_type)
                return {"success": True, "message": result}

            elif action == "generate_speech_text":
                topic = parameters.get("topic", "")
                duration_minutes = parameters.get("duration_minutes", 5)
                tone = parameters.get("tone", "professional")
                result = self.ai_features.generate_speech_text(topic, duration_minutes, tone)
                return {"success": True, "message": result}

            elif action == "audio_analysis_guide":
                audio_type = parameters.get("audio_type", "")
                result = self.ai_features.audio_analysis_guide(audio_type)
                return {"success": True, "message": result}

            elif action == "format_converter":
                input_format = parameters.get("input_format", "")
                output_format = parameters.get("output_format", "")
                file_description = parameters.get("file_description", "")
                result = self.ai_features.format_converter(input_format, output_format, file_description)
                return {"success": True, "message": result}

            elif action == "codec_transformer":
                source_codec = parameters.get("source_codec", "")
                target_codec = parameters.get("target_codec", "")
                result = self.ai_features.codec_transformer(source_codec, target_codec)
                return {"success": True, "message": result}

            elif action == "quality_adjuster":
                media_type = parameters.get("media_type", "video")
                target_quality = parameters.get("target_quality", "high")
                result = self.ai_features.quality_adjuster(media_type, target_quality)
                return {"success": True, "message": result}

            elif action == "batch_converter":
                conversion_task = parameters.get("conversion_task", "")
                file_count = parameters.get("file_count", 1)
                result = self.ai_features.batch_converter(conversion_task, file_count)
                return {"success": True, "message": result}

            elif action == "resolution_changer":
                current_resolution = parameters.get("current_resolution", "")
                target_resolution = parameters.get("target_resolution", "")
                result = self.ai_features.resolution_changer(current_resolution, target_resolution)
                return {"success": True, "message": result}

            elif action == "media_trimmer":
                media_type = parameters.get("media_type", "video")
                trim_specification = parameters.get("trim_specification", "")
                result = self.ai_features.media_trimmer(media_type, trim_specification)
                return {"success": True, "message": result}

            elif action == "media_splitter":
                split_criteria = parameters.get("split_criteria", "")
                result = self.ai_features.media_splitter(split_criteria)
                return {"success": True, "message": result}

            elif action == "media_merger":
                merge_description = parameters.get("merge_description", "")
                result = self.ai_features.media_merger(merge_description)
                return {"success": True, "message": result}

            elif action == "volume_adjuster":
                adjustment_type = parameters.get("adjustment_type", "normalize")
                result = self.ai_features.volume_adjuster(adjustment_type)
                return {"success": True, "message": result}

            elif action == "speed_controller":
                speed_change = parameters.get("speed_change", "")
                result = self.ai_features.speed_controller(speed_change)
                return {"success": True, "message": result}

            elif action == "size_optimizer":
                target_size = parameters.get("target_size", "")
                media_type = parameters.get("media_type", "video")
                result = self.ai_features.size_optimizer(target_size, media_type)
                return {"success": True, "message": result}

            elif action == "bitrate_adjuster":
                bitrate_target = parameters.get("bitrate_target", "")
                result = self.ai_features.bitrate_adjuster(bitrate_target)
                return {"success": True, "message": result}

            elif action == "quality_compressor":
                compression_level = parameters.get("compression_level", "medium")
                result = self.ai_features.quality_compressor(compression_level)
                return {"success": True, "message": result}

            elif action == "batch_compression":
                compression_task = parameters.get("compression_task", "")
                result = self.ai_features.batch_compression(compression_task)
                return {"success": True, "message": result}

            elif action == "format_specific_compression":
                format_name = parameters.get("format_name", "")
                result = self.ai_features.format_specific_compression(format_name)
                return {"success": True, "message": result}

            elif action == "metadata_extractor":
                file_type = parameters.get("file_type", "")
                result = self.ai_features.metadata_extractor(file_type)
                return {"success": True, "message": result}

            elif action == "format_detector":
                detection_task = parameters.get("detection_task", "")
                result = self.ai_features.format_detector(detection_task)
                return {"success": True, "message": result}

            elif action == "quality_analyzer":
                analysis_type = parameters.get("analysis_type", "")
                result = self.ai_features.quality_analyzer(analysis_type)
                return {"success": True, "message": result}

            elif action == "duration_calculator":
                calculation_task = parameters.get("calculation_task", "")
                result = self.ai_features.duration_calculator(calculation_task)
                return {"success": True, "message": result}

            elif action == "codec_identifier":
                identification_task = parameters.get("identification_task", "")
                result = self.ai_features.codec_identifier(identification_task)
                return {"success": True, "message": result}

            elif action == "stream_configuration":
                platform = parameters.get("platform", "")
                stream_type = parameters.get("stream_type", "")
                result = self.ai_features.stream_configuration(platform, stream_type)
                return {"success": True, "message": result}

            elif action == "broadcast_settings":
                broadcast_type = parameters.get("broadcast_type", "")
                result = self.ai_features.broadcast_settings(broadcast_type)
                return {"success": True, "message": result}

            elif action == "encoding_optimizer":
                encoding_scenario = parameters.get("encoding_scenario", "")
                result = self.ai_features.encoding_optimizer(encoding_scenario)
                return {"success": True, "message": result}

            elif action == "quality_settings":
                target_quality = parameters.get("target_quality", "high")
                use_case = parameters.get("use_case", "")
                result = self.ai_features.quality_settings(target_quality, use_case)
                return {"success": True, "message": result}

            elif action == "platform_optimizer":
                platform_name = parameters.get("platform_name", "")
                result = self.ai_features.platform_optimizer(platform_name)
                return {"success": True, "message": result}

            elif action == "subtitle_editor":
                editing_task = parameters.get("editing_task", "")
                result = self.ai_features.subtitle_editor(editing_task)
                return {"success": True, "message": result}

            elif action == "timing_adjuster":
                adjustment_needed = parameters.get("adjustment_needed", "")
                result = self.ai_features.timing_adjuster(adjustment_needed)
                return {"success": True, "message": result}

            elif action == "subtitle_format_converter":
                from_format = parameters.get("from_format", "")
                to_format = parameters.get("to_format", "")
                result = self.ai_features.subtitle_format_converter(from_format, to_format)
                return {"success": True, "message": result}

            elif action == "subtitle_generator":
                generation_method = parameters.get("generation_method", "")
                result = self.ai_features.subtitle_generator(generation_method)
                return {"success": True, "message": result}

            elif action == "subtitle_synchronizer":
                sync_task = parameters.get("sync_task", "")
                result = self.ai_features.subtitle_synchronizer(sync_task)
                return {"success": True, "message": result}

            elif action == "tag_editor":
                tag_operation = parameters.get("tag_operation", "")
                result = self.ai_features.tag_editor(tag_operation)
                return {"success": True, "message": result}

            elif action == "cover_art_manager":
                art_task = parameters.get("art_task", "")
                result = self.ai_features.cover_art_manager(art_task)
                return {"success": True, "message": result}

            elif action == "information_extractor":
                extraction_target = parameters.get("extraction_target", "")
                result = self.ai_features.information_extractor(extraction_target)
                return {"success": True, "message": result}

            elif action == "metadata_batch_editor":
                batch_task = parameters.get("batch_task", "")
                result = self.ai_features.metadata_batch_editor(batch_task)
                return {"success": True, "message": result}

            elif action == "id3_editor":
                id3_operation = parameters.get("id3_operation", "")
                result = self.ai_features.id3_editor(id3_operation)
                return {"success": True, "message": result}

            elif action == "noise_reduction":
                noise_type = parameters.get("noise_type", "")
                result = self.ai_features.noise_reduction(noise_type)
                return {"success": True, "message": result}

            elif action == "audio_equalizer":
                eq_goal = parameters.get("eq_goal", "")
                result = self.ai_features.audio_equalizer(eq_goal)
                return {"success": True, "message": result}

            elif action == "audio_normalizer":
                normalization_type = parameters.get("normalization_type", "")
                result = self.ai_features.audio_normalizer(normalization_type)
                return {"success": True, "message": result}

            elif action == "audio_amplifier":
                amplification_goal = parameters.get("amplification_goal", "")
                result = self.ai_features.audio_amplifier(amplification_goal)
                return {"success": True, "message": result}

            elif action == "echo_remover":
                echo_scenario = parameters.get("echo_scenario", "")
                result = self.ai_features.echo_remover(echo_scenario)
                return {"success": True, "message": result}

            elif action == "video_stabilizer":
                stabilization_task = parameters.get("stabilization_task", "")
                result = self.ai_features.video_stabilizer(stabilization_task)
                return {"success": True, "message": result}

            elif action == "color_corrector":
                correction_goal = parameters.get("correction_goal", "")
                result = self.ai_features.color_corrector(correction_goal)
                return {"success": True, "message": result}

            elif action == "brightness_adjuster":
                adjustment_task = parameters.get("adjustment_task", "")
                result = self.ai_features.brightness_adjuster(adjustment_task)
                return {"success": True, "message": result}

            elif action == "contrast_enhancer":
                enhancement_goal = parameters.get("enhancement_goal", "")
                result = self.ai_features.contrast_enhancer(enhancement_goal)
                return {"success": True, "message": result}

            elif action == "frame_rate_converter":
                conversion_spec = parameters.get("conversion_spec", "")
                result = self.ai_features.frame_rate_converter(conversion_spec)
                return {"success": True, "message": result}

            elif action == "playlist_creator":
                playlist_type = parameters.get("playlist_type", "")
                result = self.ai_features.playlist_creator(playlist_type)
                return {"success": True, "message": result}

            elif action == "media_organizer":
                organization_task = parameters.get("organization_task", "")
                result = self.ai_features.media_organizer(organization_task)
                return {"success": True, "message": result}

            elif action == "media_batch_processor":
                processing_task = parameters.get("processing_task", "")
                result = self.ai_features.media_batch_processor(processing_task)
                return {"success": True, "message": result}

            elif action == "media_file_renamer":
                renaming_pattern = parameters.get("renaming_pattern", "")
                result = self.ai_features.media_file_renamer(renaming_pattern)
                return {"success": True, "message": result}

            elif action == "media_duplicate_finder":
                search_criteria = parameters.get("search_criteria", "")
                result = self.ai_features.media_duplicate_finder(search_criteria)
                return {"success": True, "message": result}

            elif action == "list_ai_features":
                result = self.ai_features.list_ai_features()
                message = "🤖 AVAILABLE AI FEATURES:\n" + "=" * 60 + "\n\n"
                for category, features in result.items():
                    message += f"📁 {category}:\n"
                    for feature in features:
                        message += f"  • {feature}\n"
                    message += "\n"
                message += "=" * 60
                return {"success": True, "message": message}

            elif action == "import_csv":
                filepath = parameters.get("filepath", "")
                name = parameters.get("name", "data")
                return self.data_analysis.import_csv(filepath, name)

            elif action == "import_json":
                filepath = parameters.get("filepath", "")
                name = parameters.get("name", "data")
                return self.data_analysis.import_json(filepath, name)

            elif action == "import_excel":
                filepath = parameters.get("filepath", "")
                sheet_name = parameters.get("sheet_name", None)
                name = parameters.get("name", "data")
                return self.data_analysis.import_excel(filepath, sheet_name, name)

            elif action == "export_csv":
                name = parameters.get("name", "data")
                output_path = parameters.get("output_path", "output.csv")
                return self.data_analysis.export_csv(name, output_path)

            elif action == "export_json":
                name = parameters.get("name", "data")
                output_path = parameters.get("output_path", "output.json")
                return self.data_analysis.export_json(name, output_path)

            elif action == "convert_format":
                input_file = parameters.get("input_file", "")
                output_file = parameters.get("output_file", "")
                output_format = parameters.get("output_format", "csv")
                return self.data_analysis.convert_format(input_file, output_file, output_format)

            elif action == "handle_missing_values":
                name = parameters.get("name", "data")
                strategy = parameters.get("strategy", "drop")
                column = parameters.get("column", None)
                return self.data_analysis.handle_missing_values(name, strategy, column)

            elif action == "remove_duplicates":
                name = parameters.get("name", "data")
                subset = parameters.get("subset", None)
                return self.data_analysis.remove_duplicates(name, subset)

            elif action == "validate_data":
                name = parameters.get("name", "data")
                rules = parameters.get("rules", None)
                return self.data_analysis.validate_data(name, rules)

            elif action == "convert_data_types":
                name = parameters.get("name", "data")
                column = parameters.get("column", "")
                new_type = parameters.get("new_type", "string")
                return self.data_analysis.convert_data_types(name, column, new_type)

            elif action == "detect_outliers":
                name = parameters.get("name", "data")
                column = parameters.get("column", "")
                method = parameters.get("method", "iqr")
                return self.data_analysis.detect_outliers(name, column, method)

            elif action == "statistical_summary":
                name = parameters.get("name", "data")
                return self.data_analysis.statistical_summary(name)

            elif action == "correlation_analysis":
                name = parameters.get("name", "data")
                method = parameters.get("method", "pearson")
                return self.data_analysis.correlation_analysis(name, method)

            elif action == "data_profiling":
                name = parameters.get("name", "data")
                return self.data_analysis.data_profiling(name)

            elif action == "distribution_analysis":
                name = parameters.get("name", "data")
                column = parameters.get("column", "")
                return self.data_analysis.distribution_analysis(name, column)

            elif action == "trend_analysis":
                name = parameters.get("name", "data")
                time_column = parameters.get("time_column", "")
                value_column = parameters.get("value_column", "")
                return self.data_analysis.trend_analysis(name, time_column, value_column)

            elif action == "create_chart":
                name = parameters.get("name", "data")
                chart_type = parameters.get("chart_type", "bar")
                x_column = parameters.get("x_column", "")
                y_column = parameters.get("y_column", None)
                title = parameters.get("title", None)
                return self.data_analysis.create_chart(name, chart_type, x_column, y_column, title)

            elif action == "create_heatmap":
                name = parameters.get("name", "data")
                title = parameters.get("title", None)
                return self.data_analysis.create_heatmap(name, title)

            elif action == "create_dashboard":
                name = parameters.get("name", "data")
                return self.data_analysis.create_dashboard(name)

            elif action == "create_pivot_table":
                name = parameters.get("name", "data")
                index = parameters.get("index", "")
                columns = parameters.get("columns", "")
                values = parameters.get("values", "")
                agg_func = parameters.get("agg_func", "mean")
                return self.data_analysis.create_pivot_table(name, index, columns, values, agg_func)

            elif action == "aggregate_data":
                name = parameters.get("name", "data")
                group_by = parameters.get("group_by", [])
                agg_dict = parameters.get("agg_dict", {})
                return self.data_analysis.aggregate_data(name, group_by, agg_dict)

            elif action == "calculate_column":
                name = parameters.get("name", "data")
                new_column = parameters.get("new_column", "")
                expression = parameters.get("expression", "")
                return self.data_analysis.calculate_column(name, new_column, expression)

            elif action == "merge_datasets":
                name1 = parameters.get("name1", "")
                name2 = parameters.get("name2", "")
                on = parameters.get("on", "")
                how = parameters.get("how", "inner")
                result_name = parameters.get("result_name", "merged")
                return self.data_analysis.merge_datasets(name1, name2, on, how, result_name)

            elif action == "split_column":
                name = parameters.get("name", "data")
                column = parameters.get("column", "")
                delimiter = parameters.get("delimiter", ",")
                new_columns = parameters.get("new_columns", [])
                return self.data_analysis.split_column(name, column, delimiter, new_columns)

            elif action == "linear_regression":
                name = parameters.get("name", "data")
                target_column = parameters.get("target_column", "")
                feature_columns = parameters.get("feature_columns", [])
                return self.data_analysis.linear_regression(name, target_column, feature_columns)

            elif action == "advanced_regression":
                name = parameters.get("name", "data")
                target_column = parameters.get("target_column", "")
                feature_columns = parameters.get("feature_columns", [])
                model_type = parameters.get("model_type", "ridge")
                return self.data_analysis.advanced_regression(name, target_column, feature_columns, model_type)

            elif action == "classification_model":
                name = parameters.get("name", "data")
                target_column = parameters.get("target_column", "")
                feature_columns = parameters.get("feature_columns", [])
                model_type = parameters.get("model_type", "logistic")
                return self.data_analysis.classification_model(name, target_column, feature_columns, model_type)

            elif action == "ensemble_methods":
                name = parameters.get("name", "data")
                target_column = parameters.get("target_column", "")
                feature_columns = parameters.get("feature_columns", [])
                task = parameters.get("task", "classification")
                return self.data_analysis.ensemble_methods(name, target_column, feature_columns, task)

            elif action == "clustering_analysis":
                name = parameters.get("name", "data")
                feature_columns = parameters.get("feature_columns", [])
                n_clusters = parameters.get("n_clusters", 3)
                method = parameters.get("method", "kmeans")
                return self.data_analysis.clustering_analysis(name, feature_columns, n_clusters, method)

            elif action == "feature_selection":
                name = parameters.get("name", "data")
                target_column = parameters.get("target_column", "")
                feature_columns = parameters.get("feature_columns", [])
                k = parameters.get("k", 5)
                return self.data_analysis.feature_selection(name, target_column, feature_columns, k)

            elif action == "cross_validation":
                name = parameters.get("name", "data")
                target_column = parameters.get("target_column", "")
                feature_columns = parameters.get("feature_columns", [])
                cv_folds = parameters.get("cv_folds", 5)
                return self.data_analysis.cross_validation(name, target_column, feature_columns, cv_folds)

            elif action == "text_mining":
                text = parameters.get("text", "")
                return self.data_analysis.text_mining(text)

            elif action == "sentiment_analysis":
                text = parameters.get("text", "")
                return self.data_analysis.sentiment_analysis(text)

            elif action == "word_frequency":
                name = parameters.get("name", "data")
                text_column = parameters.get("text_column", "")
                top_n = parameters.get("top_n", 20)
                return self.data_analysis.word_frequency(name, text_column, top_n)

            elif action == "trend_decomposition":
                name = parameters.get("name", "data")
                time_column = parameters.get("time_column", "")
                value_column = parameters.get("value_column", "")
                period = parameters.get("period", 12)
                return self.data_analysis.trend_decomposition(name, time_column, value_column, period)

            elif action == "seasonality_analysis":
                name = parameters.get("name", "data")
                time_column = parameters.get("time_column", "")
                value_column = parameters.get("value_column", "")
                return self.data_analysis.seasonality_analysis(name, time_column, value_column)

            elif action == "time_series_forecast":
                name = parameters.get("name", "data")
                time_column = parameters.get("time_column", "")
                value_column = parameters.get("value_column", "")
                periods = parameters.get("periods", 10)
                return self.data_analysis.time_series_forecast(name, time_column, value_column, periods)

            elif action == "moving_averages":
                name = parameters.get("name", "data")
                column = parameters.get("column", "")
                window = parameters.get("window", 7)
                return self.data_analysis.moving_averages(name, column, window)

            elif action == "t_test":
                name = parameters.get("name", "data")
                column1 = parameters.get("column1", "")
                column2 = parameters.get("column2", "")
                return self.data_analysis.t_test(name, column1, column2)

            elif action == "chi_square_test":
                name = parameters.get("name", "data")
                column1 = parameters.get("column1", "")
                column2 = parameters.get("column2", "")
                return self.data_analysis.chi_square_test(name, column1, column2)

            elif action == "anova_test":
                name = parameters.get("name", "data")
                group_column = parameters.get("group_column", "")
                value_column = parameters.get("value_column", "")
                return self.data_analysis.anova_test(name, group_column, value_column)

            elif action == "normality_test":
                name = parameters.get("name", "data")
                column = parameters.get("column", "")
                return self.data_analysis.normality_test(name, column)

            elif action == "quality_assessment":
                name = parameters.get("name", "data")
                return self.data_analysis.quality_assessment(name)

            elif action == "completeness_check":
                name = parameters.get("name", "data")
                return self.data_analysis.completeness_check(name)

            elif action == "record_action":
                action_name = parameters.get("action", "")
                context_info = parameters.get("context_info")
                return self.behavioral_learning.record_action(action_name, context_info)

            elif action == "predict_next_action":
                predictions = self.behavioral_learning.predict_next_action()
                output = "\n🔮 PREDICTIONS:\n"
                for i, pred in enumerate(predictions, 1):
                    output += f"{i}. {pred['action']} - {pred['reason']} ({pred['confidence']})\n"
                return {"success": True, "message": output}

            elif action == "get_habit_summary":
                return {"success": True, "message": self.behavioral_learning.get_habit_summary()}

            elif action == "set_user_context":
                activity = parameters.get("activity")
                location = parameters.get("location")
                energy_mode = parameters.get("energy_mode")
                return self.behavioral_learning.set_context(activity, location, energy_mode)

            elif action == "get_context_recommendations":
                recs = self.behavioral_learning.get_context_recommendations()
                output = "\n💡 CONTEXT RECOMMENDATIONS:\n"
                for rec in recs:
                    output += f"  • {rec}\n"
                return {"success": True, "message": output}

            elif action == "reset_learning":
                return self.behavioral_learning.reset_learning()

            elif action == "save_work_environment":
                name = parameters.get("name", "")
                description = parameters.get("description", "")
                return self.workspace_manager.save_environment(name, description)

            elif action == "load_work_environment":
                name = parameters.get("name", "")
                return self.workspace_manager.load_environment(name)

            elif action == "list_work_environments":
                return {"success": True, "message": self.workspace_manager.list_environments()}

            elif action == "add_to_clipboard_history":
                content = parameters.get("content", "")
                content_type = parameters.get("content_type", "text")
                return self.workspace_manager.add_to_clipboard_history(content, content_type)

            elif action == "get_clipboard_history_smart":
                limit = parameters.get("limit", 20)
                return {"success": True, "message": self.workspace_manager.get_clipboard_history(limit)}

            elif action == "search_clipboard_smart":
                query = parameters.get("query", "")
                return {"success": True, "message": self.workspace_manager.search_clipboard(query)}

            elif action == "add_notification":
                title = parameters.get("title", "")
                message = parameters.get("message", "")
                priority = parameters.get("priority", "normal")
                source = parameters.get("source", "system")
                return self.workspace_manager.add_notification(title, message, priority, source)

            elif action == "get_smart_notifications":
                show_all = parameters.get("show_all", False)
                return {"success": True, "message": self.workspace_manager.get_notifications(show_all)}

            elif action == "group_windows_by_type":
                return self.workspace_manager.group_windows_by_type()

            elif action == "enable_focus_trigger":
                trigger_type = parameters.get("trigger_type", "fullscreen")
                return self.workspace_manager.enable_focus_trigger(trigger_type)

            elif action == "clear_clipboard_history":
                return self.workspace_manager.clear_clipboard_history()

            elif action == "mark_notifications_read":
                return self.workspace_manager.mark_notifications_read()

            elif action == "train_custom_phrase":
                phrase = parameters.get("phrase", "")
                meaning = parameters.get("meaning", "")
                return self.multimodal_control.train_custom_phrase(phrase, meaning)

            elif action == "add_slang_term":
                slang = parameters.get("slang", "")
                translation = parameters.get("translation", "")
                return self.multimodal_control.add_slang_term(slang, translation)

            elif action == "enable_whisper_mode":
                return self.multimodal_control.enable_whisper_mode()

            elif action == "disable_whisper_mode":
                return self.multimodal_control.disable_whisper_mode()

            elif action == "add_gesture_mapping":
                gesture = parameters.get("gesture", "")
                action_target = parameters.get("action", "")
                return self.multimodal_control.add_gesture_mapping(gesture, action_target)

            elif action == "get_gesture_mappings":
                return {"success": True, "message": self.multimodal_control.get_gesture_mappings()}

            elif action == "set_context_aware_reply_mode":
                mode = parameters.get("mode", "casual")
                return self.multimodal_control.set_context_aware_reply_mode(mode)

            elif action == "get_voice_profile_summary":
                return {"success": True, "message": self.multimodal_control.get_voice_profile_summary()}

            elif action == "process_hybrid_input":
                voice_command = parameters.get("voice_command", "")
                gesture = parameters.get("gesture")
                return self.multimodal_control.process_hybrid_input(voice_command, gesture)

            elif action == "reset_voice_profile":
                return self.multimodal_control.reset_voice_profile()

            elif action == "summarize_email_ai":
                email_content = parameters.get("email_content", "")
                return {"success": True, "message": self.advanced_ai_automation.summarize_email(email_content)}

            elif action == "generate_document_ai":
                doc_type = parameters.get("doc_type", "report")
                topic = parameters.get("topic", "")
                details = parameters.get("details")
                return self.advanced_ai_automation.generate_document(doc_type, topic, details)

            elif action == "review_code_ai":
                code = parameters.get("code", "")
                language = parameters.get("language", "python")
                return {"success": True, "message": self.advanced_ai_automation.review_code(code, language)}

            elif action == "build_visual_workflow":
                workflow_name = parameters.get("workflow_name", "")
                steps = parameters.get("steps", [])
                return self.advanced_ai_automation.build_workflow(workflow_name, steps)

            elif action == "list_visual_workflows":
                return {"success": True, "message": self.advanced_ai_automation.list_workflows()}

            elif action == "suggest_macro_ai":
                repeated_actions = parameters.get("repeated_actions", [])
                return self.advanced_ai_automation.suggest_macro(repeated_actions)

            elif action == "get_ai_connector_status":
                return self.advanced_ai_automation.get_ai_connector_status()

            elif action == "detect_data_anomalies":
                file_path = parameters.get("file_path", "")
                column = parameters.get("column")
                threshold = parameters.get("threshold", 3.0)
                return self.data_intelligence.detect_anomalies(file_path, column, threshold)

            elif action == "create_interactive_dashboard":
                name = parameters.get("name", "")
                data_source = parameters.get("data_source", "")
                visualizations = parameters.get("visualizations", [])
                return self.data_intelligence.create_interactive_dashboard(name, data_source, visualizations)

            elif action == "list_interactive_dashboards":
                return {"success": True, "message": self.data_intelligence.list_dashboards()}

            elif action == "build_ai_query":
                description = parameters.get("description", "")
                query_type = parameters.get("query_type", "pandas")
                return {"success": True, "message": self.data_intelligence.build_query(description, query_type)}

            elif action == "setup_ml_pipeline":
                pipeline_name = parameters.get("pipeline_name", "")
                model_type = parameters.get("model_type", "regression")
                return self.data_intelligence.setup_ml_pipeline(pipeline_name, model_type)

            elif action == "encrypt_dataset_memory":
                file_path = parameters.get("file_path", "")
                return self.data_intelligence.encrypt_dataset(file_path)

            elif action == "get_anomaly_alerts":
                return {"success": True, "message": self.data_intelligence.get_anomaly_alerts()}

            elif action == "record_meeting_transcript":
                meeting_title = parameters.get("meeting_title", "")
                audio_content = parameters.get("audio_content")
                return self.collaboration_tools.record_meeting(meeting_title, audio_content)

            elif action == "list_meeting_transcripts":
                return {"success": True, "message": self.collaboration_tools.list_transcripts()}

            elif action == "schedule_optimal_email":
                recipient = parameters.get("recipient", "")
                subject = parameters.get("subject", "")
                body = parameters.get("body", "")
                send_time = parameters.get("send_time", "optimal")
                return self.collaboration_tools.schedule_email(recipient, subject, body, send_time)

            elif action == "get_scheduled_emails":
                return {"success": True, "message": self.collaboration_tools.get_email_schedules()}

            elif action == "create_messaging_hub":
                return self.collaboration_tools.create_messaging_hub()

            elif action == "voice_memo_to_note":
                voice_memo = parameters.get("voice_memo", "")
                return self.collaboration_tools.voice_to_note(voice_memo)

            elif action == "generate_presentation_ai":
                topic = parameters.get("topic", "")
                outline = parameters.get("outline", [])
                return self.collaboration_tools.generate_presentation(topic, outline)

            elif action == "generate_image_from_text":
                description = parameters.get("description", "")
                style = parameters.get("style", "realistic")
                return self.creative_utilities.generate_image_from_text(description, style)

            elif action == "create_voice_model":
                model_name = parameters.get("model_name", "")
                sample_text = parameters.get("sample_text", "")
                return self.creative_utilities.create_voice_model(model_name, sample_text)

            elif action == "list_voice_models":
                return {"success": True, "message": self.creative_utilities.list_voice_models()}

            elif action == "write_script_ai":
                script_type = parameters.get("script_type", "video")
                topic = parameters.get("topic", "")
                duration = parameters.get("duration", "5min")
                return self.creative_utilities.write_script(script_type, topic, duration)

            elif action == "summarize_audio_file":
                audio_file = parameters.get("audio_file", "")
                summary_type = parameters.get("summary_type", "bullet")
                return self.creative_utilities.summarize_audio(audio_file, summary_type)

            elif action == "list_generated_scripts":
                return {"success": True, "message": self.creative_utilities.list_scripts()}

            elif action == "list_audio_summaries":
                return {"success": True, "message": self.creative_utilities.list_audio_summaries()}

            elif action == "enable_smart_access":
                method = parameters.get("method", "facial_recognition")
                return self.security_enhancements.enable_smart_access_control(method)

            elif action == "get_access_control_status":
                return {"success": True, "message": self.security_enhancements.get_access_control_status()}

            elif action == "enable_auto_vpn":
                network_name = parameters.get("network_name")
                return self.security_enhancements.enable_auto_vpn(network_name)

            elif action == "detect_security_threats":
                return self.security_enhancements.detect_threats()

            elif action == "schedule_data_wipe":
                interval = parameters.get("interval", "weekly")
                target = parameters.get("target", "temp_files")
                return self.security_enhancements.schedule_data_wipe(interval, target)

            elif action == "add_trusted_device":
                device_name = parameters.get("device_name", "")
                device_id = parameters.get("device_id", "")
                return self.security_enhancements.add_trusted_device(device_name, device_id)

            elif action == "list_trusted_devices":
                return {"success": True, "message": self.security_enhancements.list_trusted_devices()}

            elif action == "get_threat_log":
                return {"success": True, "message": self.security_enhancements.get_threat_log()}

            elif action == "remember_conversation":
                topic = parameters.get("topic", "")
                details = parameters.get("details", "")
                return self.human_interaction.remember_conversation(topic, details)

            elif action == "get_conversation_summary":
                return {"success": True, "message": self.human_interaction.get_conversation_summary()}

            elif action == "set_ai_tone":
                tone = parameters.get("tone", "casual")
                return self.human_interaction.set_tone(tone)

            elif action == "get_tone_settings":
                return {"success": True, "message": self.human_interaction.get_tone_settings()}

            elif action == "detect_user_stress":
                typing_speed = parameters.get("typing_speed")
                message_tone = parameters.get("message_tone")
                return self.human_interaction.detect_stress(typing_speed, message_tone)

            elif action == "track_user_goal":
                goal_name = parameters.get("goal_name", "")
                target = parameters.get("target", "")
                deadline = parameters.get("deadline")
                return self.human_interaction.track_goal(goal_name, target, deadline)

            elif action == "update_goal_progress":
                goal_name = parameters.get("goal_name", "")
                progress = parameters.get("progress", 0)
                return self.human_interaction.update_goal_progress(goal_name, progress)

            elif action == "get_goals_summary":
                return {"success": True, "message": self.human_interaction.get_goals_summary()}

            elif action == "award_productivity_xp":
                xp_amount = parameters.get("xp_amount", 0)
                reason = parameters.get("reason", "")
                return self.human_interaction.award_xp(xp_amount, reason)

            elif action == "get_achievements_summary":
                return {"success": True, "message": self.human_interaction.get_achievements_summary()}

            elif action == "enable_cloud_sync":
                items = parameters.get("items")
                return self.cloud_ecosystem.enable_cloud_sync(items)

            elif action == "sync_now":
                return self.cloud_ecosystem.sync_now()

            elif action == "install_custom_plugin":
                plugin_name = parameters.get("plugin_name", "")
                plugin_code = parameters.get("plugin_code")
                return self.cloud_ecosystem.install_plugin(plugin_name, plugin_code)

            elif action == "list_installed_plugins":
                return {"success": True, "message": self.cloud_ecosystem.list_plugins()}

            elif action == "publish_workflow_marketplace":
                workflow_name = parameters.get("workflow_name", "")
                description = parameters.get("description", "")
                workflow_data = parameters.get("workflow_data", {})
                return self.cloud_ecosystem.publish_workflow(workflow_name, description, workflow_data)

            elif action == "browse_workflow_marketplace":
                return {"success": True, "message": self.cloud_ecosystem.browse_marketplace()}

            elif action == "download_marketplace_workflow":
                workflow_name = parameters.get("workflow_name", "")
                return self.cloud_ecosystem.download_workflow(workflow_name)

            elif action == "connect_mobile_device":
                device_name = parameters.get("device_name", "")
                device_type = parameters.get("device_type", "smartphone")
                return self.cloud_ecosystem.connect_mobile_device(device_name, device_type)

            elif action == "list_connected_mobile_devices":
                return {"success": True, "message": self.cloud_ecosystem.list_mobile_devices()}

            elif action == "backup_to_cloud":
                items = parameters.get("items")
                return self.cloud_ecosystem.backup_to_cloud(items)

            elif action == "restore_from_cloud":
                backup_date = parameters.get("backup_date", "latest")
                return self.cloud_ecosystem.restore_from_cloud(backup_date)

            elif action == "index_directory_rag":
                directory = parameters.get("directory", ".")
                max_files = parameters.get("max_files", 1000)
                recursive = parameters.get("recursive", True)
                result = self.desktop_rag.index_directory(directory, max_files, recursive)
                if result.get("success"):
                    return {"success": True,
                            "message": f"✅ Indexed {result['indexed_files']} files in {result['time_taken']}\n📊 Total in index: {result['total_in_index']}"}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "quick_index_rag":
                result = self.desktop_rag.quick_index_common_folders()
                if result.get("success"):
                    return {"success": True,
                            "message": f"✅ Quick indexed {result['total_files_indexed']} files from {result['folders_indexed']} common folders"}
                else:
                    return {"success": False, "message": f"❌ Error indexing folders"}

            elif action == "search_files_rag":
                query = parameters.get("query", "")
                max_results = parameters.get("max_results", 10)
                matches = self.desktop_rag.search_files(query, max_results)
                if matches:
                    result_msg = f"🔍 Found {len(matches)} matches for '{query}':\n\n"
                    for i, match in enumerate(matches[:10], 1):
                        result_msg += f"{i}. {match['name']}\n   Path: {match['path']}\n   Relevance: {match['relevance_score']}\n\n"
                    return {"success": True, "message": result_msg}
                else:
                    return {"success": True, "message": f"No files found matching '{query}'"}

            elif action == "ask_about_files":
                question = parameters.get("question", "")
                result = self.desktop_rag.ask_about_files(question)
                if result.get("success"):
                    msg = f"💬 Question: {question}\n\n"
                    msg += f"📊 AI Answer:\n{result['answer']}\n\n"
                    msg += f"📁 Files analyzed: {result['files_analyzed']}\n"
                    if result.get('relevant_files'):
                        msg += "\nRelevant files:\n"
                        for f in result['relevant_files'][:5]:
                            msg += f"  • {f}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "summarize_folder_rag":
                folder_path = parameters.get("folder_path", ".")
                result = self.desktop_rag.summarize_folder(folder_path)
                if result.get("success"):
                    msg = f"📊 Folder Summary: {folder_path}\n\n"
                    msg += f"📁 Files: {result['file_count']}\n"
                    msg += f"💾 Size: {result['total_size_mb']} MB\n\n"
                    msg += f"AI Analysis:\n{result['summary']}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "find_duplicates_rag":
                result = self.desktop_rag.find_duplicates_smart()
                if result.get("success"):
                    msg = f"🔍 Smart Duplicate Detection\n\n"
                    msg += f"Found {result['duplicates_found']} potential duplicates\n"
                    msg += f"💾 Potential savings: {result['potential_savings_mb']:.2f} MB\n\n"
                    if result.get('duplicates'):
                        msg += "Top duplicates:\n"
                        for dup in result['duplicates'][:10]:
                            msg += f"\n  • {dup['name']}\n"
                            msg += f"    File 1: {dup['file1']}\n"
                            msg += f"    File 2: {dup['file2']}\n"
                            msg += f"    Confidence: {dup['confidence']}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": "❌ Error finding duplicates"}

            elif action == "get_rag_stats":
                stats = self.desktop_rag.get_index_stats()
                msg = f"📊 Desktop RAG Index Statistics\n\n"
                msg += f"Total files indexed: {stats['total_files']}\n"
                if stats['total_files'] > 0:
                    msg += f"Files with text content: {stats['files_with_text_content']}\n"
                    msg += f"Total size: {stats['total_size_mb']} MB\n"
                    msg += f"Last updated: {stats['last_updated']}\n\n"
                    msg += "Top file types:\n"
                    for ext, count in list(stats['file_types'].items())[:10]:
                        msg += f"  {ext}: {count} files\n"
                else:
                    msg += "\nNo files indexed yet. Try 'Index my desktop files' first."
                return {"success": True, "message": msg}

            elif action == "transcribe_voice":
                audio_file = parameters.get("audio_file")
                audio_url = parameters.get("audio_url")
                result = self.comm_enhancements.transcribe_voice_message(audio_file, audio_url)
                if result.get("success"):
                    return {"success": True, "message": f"🎤 Voice Transcription:\n\n{result['transcription']}"}
                else:
                    return {"success": False, "message": result.get("message", "Transcription failed")}

            elif action == "generate_smart_replies":
                message_data = parameters.get("message_data", {})
                context = parameters.get("context", "professional")
                result = self.comm_enhancements.generate_smart_replies(message_data, context)
                if result.get("success"):
                    msg = f"💬 {result['message']}\n\n"
                    for i, reply in enumerate(result['replies'], 1):
                        msg += f"Option {i} ({reply['type']}):\n{reply['text']}\n\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "rank_emails":
                emails = parameters.get("emails", [])
                result = self.comm_enhancements.rank_emails_by_priority(emails)
                if result.get("success"):
                    msg = f"📊 {result['message']}\n\n"
                    summary = result.get("summary", {})
                    msg += f"Critical: {summary.get('critical', 0)} | High: {summary.get('high', 0)} | "
                    msg += f"Medium: {summary.get('medium', 0)} | Low: {summary.get('low', 0)}\n\n"
                    msg += "Top Priority Emails:\n"
                    for i, email in enumerate(result['ranked_emails'][:5], 1):
                        msg += f"\n{i}. [{email['priority_level']}] {email.get('subject', 'No subject')}\n"
                        msg += f"   From: {email.get('from', 'Unknown')}\n"
                        msg += f"   Score: {email['priority_score']}/100\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "add_followup":
                message_data = parameters.get("message_data", {})
                days = parameters.get("days", 3)
                result = self.comm_enhancements.add_follow_up_reminder(message_data, days)
                if result.get("success"):
                    return {"success": True, "message": f"⏰ {result['message']}\nRemind at: {result['remind_date']}"}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "check_followups":
                result = self.comm_enhancements.check_follow_up_reminders()
                if result.get("success"):
                    msg = f"{result['message']}\n\n"
                    if result['due_reminders']:
                        msg += "Due Follow-ups:\n"
                        for reminder in result['due_reminders']:
                            msg += f"\n• {reminder['message'].get('subject', 'Message')}\n"
                            msg += f"  From: {reminder['message'].get('from')}\n"
                            msg += f"  Platform: {reminder['message'].get('platform')}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "send_meeting_notes":
                meeting_data = parameters.get("meeting_data", {})
                recipients = parameters.get("recipients", [])
                result = self.comm_enhancements.send_meeting_notes(meeting_data, recipients)
                return result

            elif action == "summarize_chat":
                messages = parameters.get("messages", [])
                platform = parameters.get("platform", "Slack")
                result = self.comm_enhancements.summarize_chat_thread(messages, platform)
                if result.get("success"):
                    return {"success": True, "message": f"📝 {result['message']}\n\n{result['summary']}"}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "multilingual_reply":
                message_data = parameters.get("message_data", {})
                detect = parameters.get("detect_language", True)
                result = self.comm_enhancements.generate_multilingual_reply(message_data, detect)
                if result.get("success"):
                    msg = f"🌐 {result['message']}\n\n"
                    msg += f"Language: {result['detected_language']}\n\n"
                    msg += f"Reply:\n{result['reply']}"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "voice_to_task":
                voice_text = parameters.get("voice_text", "")
                add_to_calendar = parameters.get("add_to_calendar", True)
                result = self.comm_enhancements.convert_voice_to_task(voice_text, add_to_calendar)
                if result.get("success"):
                    extracted = result['extracted']
                    msg = f"✅ {result['message']}\n\n"
                    msg += f"Type: {extracted.get('type', 'task').upper()}\n"
                    msg += f"Title: {extracted.get('title')}\n"
                    msg += f"Priority: {extracted.get('priority')}\n"
                    if extracted.get('datetime'):
                        msg += f"Date/Time: {extracted['datetime']}\n"
                    msg += f"Category: {extracted.get('category')}\n\n"
                    msg += f"Action Items:\n"
                    for item in extracted.get('action_items', []):
                        msg += f"  • {item}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "comm_features_summary":
                summary = self.comm_enhancements.get_feature_summary()
                return {"success": True, "message": summary}

            elif action == "error":
                error_msg = parameters.get("error", "Unknown error")
                return {
                    "success": False,
                    "message": f"Command parsing error: {error_msg}"
                }

            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing {action}: {str(e)}"
            }
