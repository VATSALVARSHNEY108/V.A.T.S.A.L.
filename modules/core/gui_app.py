#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import threading
import os
from dotenv import load_dotenv
from gemini_controller import parse_command, get_ai_suggestion
from command_executor import CommandExecutor
from vatsal_assistant import create_vatsal_assistant
from advanced_smart_screen_monitor import create_advanced_smart_screen_monitor
from ai_screen_monitoring_system import create_ai_screen_monitoring_system
from modules.ai_features.chatbots import SimpleChatbot
from file_automation import create_file_automation
from clipboard_text_handler import ClipboardTextHandler
from smart_automation import SmartAutomationManager
from datetime import datetime
from pathlib import Path
from desktop_controller_integration import DesktopFileController
from desktop_sync_manager import auto_initialize_on_gui_start, DesktopSyncManager
from comprehensive_desktop_controller import ComprehensiveDesktopController
from modules.ai_features.vision_ai import VirtualLanguageModel
from gui_automation import GUIAutomation

from productivity_dashboard import ProductivityDashboard
from pomodoro_ai_coach import PomodoroAICoach
from task_time_predictor import TaskTimePredictor
from energy_level_tracker import EnergyLevelTracker
from distraction_detector import DistractionDetector
from productivity_monitor import ProductivityMonitor
from password_vault import PasswordVault
from calendar_manager import CalendarManager
from quick_notes import QuickNotes
from weather_news_service import WeatherNewsService
from translation_service import TranslationService
from smart_break_suggester import SmartBreakSuggester
from selenium_web_automator import SeleniumWebAutomator
from vatsal_desktop_automator import VATSALAutomator
from self_operating_computer import SelfOperatingComputer
from self_operating_integrations import SelfOperatingIntegrationHub, SmartTaskRouter
from command_executor_integration import EnhancedCommandExecutor, CommandInterceptor
from voice_commander import create_voice_commander
from system_control import SystemController
from websocket_client import get_websocket_client
from macro_recorder import MacroRecorder, MacroTemplates
from nl_workflow_builder import create_nl_workflow_builder
from workflow_templates import WorkflowManager
from security_dashboard import SecurityDashboard
from user_profile_manager import get_user_profile_manager
from user_settings_dialog import open_user_settings

load_dotenv()


# VNC Display Optimization
def setup_vnc_display():
    """Configure optimal settings for VNC display"""
    display = os.environ.get('DISPLAY', ':0')
    vnc_mode = display == ':0'

    if vnc_mode:
        print("🖥️  Running in VNC mode - Virtual Desktop enabled")
        print(f"📺 Display: {display}")

        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.expanduser("~/screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        print(f"📸 Screenshots will be saved to: {screenshots_dir}")

    return vnc_mode


# Initialize VNC settings
VNC_MODE = setup_vnc_display()


class AutomationControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ VATSAL - AI Desktop Automation Controller")
        self.root.geometry("1400x900")
        self.root.configure(bg="#000000")  # Pure black background

        # Initialize User Profile Manager
        self.user_profile = get_user_profile_manager()
        print(f"✅ User Profile Manager initialized - Welcome, {self.user_profile.get_user_name()}!")

        # Initialize system controller for direct access
        self.system_controller = SystemController()

        # Initialize base executor
        self.base_executor = CommandExecutor()

        # Wrap with enhanced executor for self-operating integration
        try:
            self.executor = EnhancedCommandExecutor(self.base_executor)
            self.command_interceptor = CommandInterceptor(self.executor)
            print("✅ Enhanced Command Executor with self-operating integration initialized")
        except Exception as e:
            self.executor = self.base_executor  # Fallback to base
            self.command_interceptor = None
            print(f"⚠️ Using base executor (enhanced integration unavailable): {e}")

        self.vatsal = create_vatsal_assistant()
        self.advanced_monitor = create_advanced_smart_screen_monitor()
        self.ai_monitor = create_ai_screen_monitoring_system()
        self.file_automation = create_file_automation()
        self.clipboard_handler = ClipboardTextHandler()
        self.smart_automation = SmartAutomationManager()
        self.desktop_controller = DesktopFileController()

        try:
            self.comprehensive_controller = ComprehensiveDesktopController()
        except Exception as e:
            self.comprehensive_controller = None
            print(f"Comprehensive controller initialization failed: {e}")

        try:
            self.simple_chatbot = SimpleChatbot()
        except Exception as e:
            self.simple_chatbot = None
            print(f"Simple chatbot initialization failed: {e}")

        self.productivity_dashboard = ProductivityDashboard()
        self.pomodoro_coach = PomodoroAICoach()
        self.task_predictor = TaskTimePredictor()
        self.energy_tracker = EnergyLevelTracker()
        self.distraction_detector = DistractionDetector()
        self.productivity_monitor = ProductivityMonitor()
        self.password_vault = PasswordVault()
        self.calendar = CalendarManager()
        self.notes = QuickNotes()
        self.weather_news = WeatherNewsService()
        self.translator = TranslationService()
        self.break_suggester = SmartBreakSuggester()

        try:
            self.web_automator = SeleniumWebAutomator()
        except Exception as e:
            self.web_automator = None
            print(f"Web automator initialization failed: {e}")

        # Initialize Virtual Language Model
        try:
            gui_automation = GUIAutomation()
            self.vlm = VirtualLanguageModel(gui_automation)
            self.vlm_last_decision = None
        except Exception as e:
            self.vlm = None
            self.vlm_last_decision = None
            print(f"Virtual Language Model initialization failed: {e}")

        try:
            self.vatsal_automator = VATSALAutomator()
        except Exception as e:
            self.vatsal_automator = None
            print(f"VATSAL Automator initialization failed: {e}")

        try:
            self.self_operating_computer = SelfOperatingComputer(verbose=True)
            self.soc_running = False
            self.soc_thread = None
        except Exception as e:
            self.self_operating_computer = None
            self.soc_running = False
            self.soc_thread = None
            print(f"Self-Operating Computer initialization failed: {e}")

        # Initialize Self-Operating Integration Hub
        try:
            self.integration_hub = SelfOperatingIntegrationHub()
            self.task_router = SmartTaskRouter(self.integration_hub)
            print("✅ Self-Operating Integration Hub initialized")
        except Exception as e:
            self.integration_hub = None
            self.task_router = None
            print(f"Integration Hub initialization failed: {e}")

        self.vatsal_mode = True
        self.self_operating_mode = True
        self.processing = False
        self.hover_colors = {}
        self.vatsal_conversation_active = False
        self.active_chatbot = "simple"

        # Initialize WebSocket client for real-time updates
        try:
            self.ws_client = get_websocket_client()
            self.ws_client.connect()
            print("✅ WebSocket client initialized for real-time updates")
        except Exception as e:
            self.ws_client = None
            print(f"⚠️ WebSocket client initialization failed: {e}")

        # Initialize Voice Commander with callback
        try:
            self.voice_commander = create_voice_commander(command_callback=self.handle_voice_command)
            self.voice_listening = False
            self.voice_enabled = True
            print("✅ Voice Commander initialized with callback")
        except Exception as e:
            self.voice_commander = None
            self.voice_listening = False
            self.voice_enabled = False
            print(f"⚠️ Voice Commander initialization failed: {e}")

        # Initialize Macro Recorder
        try:
            self.macro_recorder = MacroRecorder()
            self.macro_templates = MacroTemplates()
            self.recording_active = False
            self.current_macro_name = None
            print("✅ Macro Recorder initialized")
        except Exception as e:
            self.macro_recorder = None
            self.macro_templates = None
            print(f"⚠️ Macro Recorder initialization failed: {e}")

        # Initialize Natural Language Workflow Builder
        try:
            self.workflow_manager = WorkflowManager()
            self.nl_workflow_builder = create_nl_workflow_builder(
                workflow_manager=self.workflow_manager,
                log_callback=self.workflow_log
            )
            print("✅ Natural Language Workflow Builder initialized")
        except Exception as e:
            self.workflow_manager = None
            self.nl_workflow_builder = None
            print(f"⚠️ Workflow Builder initialization failed: {e}")

        # Initialize Security Dashboard with Gemini AI
        try:
            self.security_dashboard = SecurityDashboard()
            print("✅ Security Dashboard with Gemini AI initialized")
        except Exception as e:
            self.security_dashboard = None
            print(f"⚠️ Security Dashboard initialization failed: {e}")

        self.setup_ui()
        self.check_api_key()
        self.start_time_update()

        # Auto-initialize desktop sync on startup
        threading.Thread(target=self.auto_desktop_sync, daemon=True).start()

        self.show_vatsal_greeting()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Fancy fonts and black/white theme
        style.configure("Header.TLabel",
                        background="#000000",
                        foreground="#ffffff",
                        font=("Copperplate Gothic Bold", 26, "bold"))
        style.configure("Info.TLabel",
                        background="#000000",
                        foreground="#cccccc",
                        font=("Consolas", 11))
        style.configure("Category.TLabel",
                        background="#0a0a0a",
                        foreground="#00ff88",
                        font=("Impact", 12, "bold"))
        style.configure("TNotebook", background="#0a0a0a", borderwidth=2, relief="solid")
        style.configure("TNotebook.Tab",
                        background="#1a1a1a",
                        foreground="#ffffff",
                        padding=[15, 10],
                        font=("Arial Black", 10, "bold"),
                        borderwidth=2)
        style.map("TNotebook.Tab",
                  background=[("selected", "#00d4ff")],
                  foreground=[("selected", "#000000")])

        header_frame = tk.Frame(
            self.root,
            bg="#000000",
            pady=20,
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        header_frame.pack(fill="x", padx=3, pady=3)

        header_container = tk.Frame(
            header_frame,
            bg="#0a0a0a",
            relief="solid",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        header_container.pack(fill="x", padx=5)

        self.add_gradient_effect(header_container)

        title_frame = tk.Frame(header_container, bg="#0a0a0a")
        title_frame.pack(pady=15)

        title = tk.Label(title_frame,
                         text="✨ V.A.T.S.A.L. ✨",
                         bg="#0a0a0a",
                         fg="#ffffff",
                         font=("Copperplate Gothic Bold", 32, "bold"))
        title.pack()

        subtitle = tk.Label(title_frame,
                            text="⚡ Vastly Advanced Technological System Above Limitations ⚡",
                            bg="#0a0a0a",
                            fg="#00d4ff",
                            font=("Georgia", 12, "italic"))
        subtitle.pack(pady=(5, 0))

        stats_frame = tk.Frame(header_container, bg="#0a0a0a")
        stats_frame.pack(pady=(10, 15))

        self.time_label = tk.Label(stats_frame,
                                   text="",
                                   bg="#0a0a0a",
                                   fg="#00ff88",
                                   font=("Consolas", 11, "bold"))
        self.time_label.pack(side="left", padx=15)

        separator1 = tk.Label(stats_frame, text="●", bg="#0a0a0a", fg="#ffffff", font=("Arial", 10))
        separator1.pack(side="left", padx=5)

        features_label = tk.Label(stats_frame,
                                  text="100+ AI Features Available",
                                  bg="#0a0a0a",
                                  fg="#00d4ff",
                                  font=("Arial Black", 10, "bold"))
        features_label.pack(side="left", padx=15)

        separator2 = tk.Label(stats_frame, text="●", bg="#0a0a0a", fg="#ffffff", font=("Arial", 10))
        separator2.pack(side="left", padx=5)

        self.vatsal_toggle_btn = tk.Button(stats_frame,
                                           text="🤖 VATSAL Mode: ON",
                                           bg="#00d4ff",
                                           fg="#000000",
                                           font=("Arial Black", 10, "bold"),
                                           relief="solid",
                                           borderwidth=2,
                                           cursor="hand2",
                                           command=self.toggle_vatsal_mode,
                                           padx=15,
                                           pady=5,
                                           highlightbackground="#ffffff",
                                           highlightthickness=1)
        self.vatsal_toggle_btn.pack(side="left", padx=15)
        self.add_hover_effect(self.vatsal_toggle_btn, "#00d4ff", "#00ff88")

        separator3 = tk.Label(stats_frame, text="●", bg="#0a0a0a", fg="#ffffff", font=("Arial", 10))
        separator3.pack(side="left", padx=5)

        self.self_operating_toggle_btn = tk.Button(stats_frame,
                                                   text="🎮 Self-Operating: ON",
                                                   bg="#b19cd9",
                                                   fg="#000000",
                                                   font=("Arial Black", 10, "bold"),
                                                   relief="solid",
                                                   borderwidth=2,
                                                   cursor="hand2",
                                                   command=self.toggle_self_operating_mode,
                                                   padx=15,
                                                   pady=5,
                                                   highlightbackground="#ffffff",
                                                   highlightthickness=1)
        self.self_operating_toggle_btn.pack(side="left", padx=15)
        self.add_hover_effect(self.self_operating_toggle_btn, "#b19cd9", "#ff0080")

        separator4 = tk.Label(stats_frame, text="●", bg="#0a0a0a", fg="#ffffff", font=("Arial", 10))
        separator4.pack(side="left", padx=5)

        self.user_settings_btn = tk.Button(stats_frame,
                                           text="⚙️ User Settings",
                                           bg="#00ff88",
                                           fg="#000000",
                                           font=("Arial Black", 10, "bold"),
                                           relief="solid",
                                           borderwidth=2,
                                           cursor="hand2",
                                           command=self.open_user_settings,
                                           padx=15,
                                           pady=5,
                                           highlightbackground="#ffffff",
                                           highlightthickness=1)
        self.user_settings_btn.pack(side="left", padx=15)
        self.add_hover_effect(self.user_settings_btn, "#00ff88", "#00d4ff")

        main_container = tk.Frame(
            self.root,
            bg="#000000",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        left_panel = tk.Frame(
            main_container,
            bg="#0a0a0a",
            width=450,
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        left_panel.pack(side="left", fill="both", expand=False, padx=5)
        left_panel.pack_propagate(False)

        left_header = tk.Frame(
            left_panel,
            bg="#1a1a1a",
            relief="solid",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        left_header.pack(fill="x", pady=5, padx=5)

        categories_label = tk.Label(left_header,
                                    text="⚡ Quick Actions Center ⚡",
                                    bg="#1a1a1a",
                                    fg="#00d4ff",
                                    font=("Impact", 16, "bold"),
                                    pady=12)
        categories_label.pack()

        # Quick actions navigation container
        self.quick_actions_container = tk.Frame(
            left_panel,
            bg="#0a0a0a",
            relief="solid",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        self.quick_actions_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Create sidebar and main content container
        self.sidebar_main_container = tk.Frame(self.quick_actions_container, bg="#0a0a0a")
        self.sidebar_main_container.pack(fill="both", expand=True)

        # Create collapsible sidebar
        self.sidebar_expanded = True
        self.sidebar = tk.Frame(
            self.sidebar_main_container,
            bg="#1a1a1a",
            width=120,
            highlightbackground="#ffffff",
            highlightthickness=1
        )
        self.sidebar.pack(side="left", fill="y", padx=2)
        self.sidebar.pack_propagate(False)

        # Sidebar toggle button
        self.sidebar_toggle_btn = tk.Button(self.sidebar,
                                            text="◀",
                                            bg="#00d4ff",
                                            fg="#000000",
                                            font=("Arial Black", 12, "bold"),
                                            relief="solid",
                                            borderwidth=2,
                                            cursor="hand2",
                                            command=self.toggle_sidebar,
                                            padx=10,
                                            pady=5,
                                            highlightbackground="#ffffff")
        self.sidebar_toggle_btn.pack(fill="x", padx=3, pady=3)
        self.add_hover_effect(self.sidebar_toggle_btn, "#00d4ff", "#00ff88")

        # Sidebar title
        self.sidebar_title = tk.Label(self.sidebar,
                                      text="MENU",
                                      bg="#1a1a1a",
                                      fg="#ffffff",
                                      font=("Impact", 10, "bold"))
        self.sidebar_title.pack(pady=(5, 10))

        # Category navigation data
        self.sidebar_categories = [
            ("🖥️", "SYSTEM", "#00d4ff"),
            ("🌐", "WEB", "#00ff88"),
            ("📁", "WORK", "#b19cd9"),
            ("🎵", "MEDIA", "#ff0080"),
        ]

        self.sidebar_buttons = []
        self.active_sidebar_category = None

        # Create category buttons in sidebar
        for icon, name, color in self.sidebar_categories:
            btn_frame = tk.Frame(self.sidebar, bg="#1a1a1a")
            btn_frame.pack(fill="x", pady=3, padx=3)

            btn = tk.Button(btn_frame,
                            text=f"{icon}\n{name}",
                            bg="#0a0a0a",
                            fg=color,
                            font=("Arial Black", 9, "bold"),
                            relief="solid",
                            borderwidth=2,
                            cursor="hand2",
                            command=lambda cat=name: self.scroll_to_category(cat),
                            padx=8,
                            pady=10,
                            width=10,
                            wraplength=80,
                            highlightbackground="#ffffff",
                            highlightthickness=1)
            btn.pack(fill="both", expand=True)

            self.sidebar_buttons.append((btn, name, color))
            self.add_hover_effect(btn, "#0a0a0a", color)

        # Create main menu view
        self.quick_menu_view = tk.Frame(self.sidebar_main_container, bg="#0a0a0a")

        # Subtitle
        menu_subtitle = tk.Label(self.quick_menu_view,
                                 text="⚡ Choose an action below ⚡",
                                 bg="#0a0a0a",
                                 fg="#00ff88",
                                 font=("Consolas", 10, "bold"))
        menu_subtitle.pack(anchor="w", padx=8, pady=(5, 8))

        # Scrollable menu
        self.menu_canvas = tk.Canvas(
            self.quick_menu_view,
            bg="#0a0a0a",
            highlightbackground="#ffffff",
            highlightthickness=1
        )
        menu_scrollbar = ttk.Scrollbar(self.quick_menu_view, orient="vertical", command=self.menu_canvas.yview)
        menu_scrollable = tk.Frame(self.menu_canvas, bg="#0a0a0a")

        menu_scrollable.bind(
            "<Configure>",
            lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))
        )

        self.menu_canvas.create_window((0, 0), window=menu_scrollable, anchor="nw")
        self.menu_canvas.configure(yscrollcommand=menu_scrollbar.set)

        # Store header widgets for scrolling
        self.category_headers = {}

        # Define quick actions with features
        self.quick_actions_data = [
            ("🖥️ SYSTEM", None, "#89b4fa", True, None),
            ("💻 Screenshot", "Take a screenshot", "#89b4fa", False, "screenshot"),
            ("🔒 Lock PC", "Lock the computer", "#f38ba8", False, "lock"),
            ("📊 Task Manager", "Open Task Manager", "#cba6f7", False, "taskmanager"),
            ("🔋 Battery Info", "View battery status", "#a6e3a1", False, "battery"),
            ("⚙️ System Settings", "Open system settings", "#89dceb", False, "settings"),

            ("🌐 WEB & APPS", None, "#89dceb", True, None),
            ("🌍 Chrome", "Open Chrome and go to Google", "#89dceb", False, "chrome"),
            ("🔍 Google Search", "Search Google for Python tutorials", "#a6e3a1", False, "google"),
            ("📧 Gmail", "Open Gmail in browser", "#f38ba8", False, "gmail"),
            ("💬 WhatsApp", "Open WhatsApp Web", "#a6e3a1", False, "whatsapp"),
            ("📺 YouTube", "Open YouTube", "#f38ba8", False, "youtube"),

            ("📁 PRODUCTIVITY", None, "#a6e3a1", True, None),
            ("📝 VS Code", "Launch VS Code", "#89b4fa", False, "vscode"),
            ("📂 File Explorer", "Open File Explorer", "#f9e2af", False, "explorer"),
            ("🗒️ Notepad", "Open Notepad", "#cba6f7", False, "notepad"),
            ("📊 Excel", "Launch Microsoft Excel", "#a6e3a1", False, "excel"),
            ("📄 Word", "Launch Microsoft Word", "#89dceb", False, "word"),

            ("🎵 MEDIA", None, "#f5c2e7", True, None),
            ("🎵 Spotify", "Launch Spotify", "#a6e3a1", False, "spotify"),
            ("🎬 VLC Player", "Open VLC Media Player", "#f9e2af", False, "vlc"),
            ("🔊 Volume Control", "Control system volume", "#89dceb", False, "volume"),
            ("🎧 Sound Settings", "Open sound settings", "#cba6f7", False, "sound"),

            ("🎬 AUTOMATION", None, "#f5c2e7", True, None),
            ("💬 Workflow Builder", "Build workflows in plain English", "#a6e3a1", False, "workflow_builder"),
            ("🎬 Macro Recorder", "Record and playback macros", "#f5c2e7", False, "macro_recorder"),
            ("📱 Mobile Control", "Remote control via mobile", "#89dceb", False, "mobile_control"),
        ]

        # Create menu buttons
        for item in self.quick_actions_data:
            text, description, color, is_header, feature_id = item

            if is_header:
                header_container = tk.Frame(menu_scrollable, bg="#1a1a2e", height=35)
                header_container.pack(fill="x", padx=5, pady=(12, 3))
                header_container.pack_propagate(False)

                # Store header for scrolling
                self.category_headers[text] = header_container

                accent = tk.Frame(header_container, bg=color, width=4)
                accent.pack(side="left", fill="y", padx=(0, 10))

                header_label = tk.Label(header_container,
                                        text=text,
                                        bg="#1a1a2e",
                                        fg=color,
                                        font=("Segoe UI", 10, "bold"))
                header_label.pack(side="left", pady=8)
            else:
                btn = tk.Button(menu_scrollable,
                                text=text,
                                bg="#313244",
                                fg="#cdd6f4",
                                font=("Segoe UI", 10),
                                relief="flat",
                                cursor="hand2",
                                command=lambda t=text, d=description, c=color,
                                               f=feature_id: self.show_quick_action_feature(t, d, c, f),
                                padx=20,
                                pady=12,
                                anchor="w",
                                bd=0)
                btn.pack(fill="x", padx=8, pady=3)

                def make_hover(button, accent_color):
                    def on_enter(e):
                        button.config(bg="#45475a", fg=accent_color)

                    def on_leave(e):
                        button.config(bg="#313244", fg="#cdd6f4")

                    button.bind("<Enter>", on_enter)
                    button.bind("<Leave>", on_leave)

                make_hover(btn, color)

        self.menu_canvas.pack(side="left", fill="both", expand=True)
        menu_scrollbar.pack(side="right", fill="y")

        # Create feature view (initially hidden)
        self.quick_feature_view = tk.Frame(self.quick_actions_container, bg="#1a1a2e")

        # Feature view header
        feature_header_frame = tk.Frame(self.quick_feature_view, bg="#1a1a2e", height=60)
        feature_header_frame.pack(fill="x", pady=(0, 10))
        feature_header_frame.pack_propagate(False)

        # Back button
        self.back_button = tk.Button(feature_header_frame,
                                     text="← Back",
                                     bg="#313244",
                                     fg="#89b4fa",
                                     font=("Segoe UI", 11, "bold"),
                                     relief="flat",
                                     cursor="hand2",
                                     command=self.show_quick_actions_menu,
                                     padx=20,
                                     pady=10)
        self.back_button.pack(side="left", padx=10, pady=10)
        self.add_hover_effect(self.back_button, "#313244", "#45475a")

        # Feature title
        self.feature_title = tk.Label(feature_header_frame,
                                      text="",
                                      bg="#1a1a2e",
                                      fg="#f9e2af",
                                      font=("Segoe UI", 13, "bold"))
        self.feature_title.pack(side="left", padx=15, pady=10)

        # Feature content area
        self.feature_content = tk.Frame(self.quick_feature_view, bg="#181825", relief="flat")
        self.feature_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Show menu view by default
        self.quick_menu_view.pack(fill="both", expand=True)

        right_panel = tk.Frame(
            main_container,
            bg="#0a0a0a",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=5)

        command_card = tk.Frame(
            right_panel,
            bg="#1a1a1a",
            relief="solid",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        command_card.pack(fill="x", pady=5, padx=5)

        input_frame = tk.Frame(command_card, bg="#1a1a1a")
        input_frame.pack(fill="x", padx=15, pady=15)

        input_label = tk.Label(input_frame,
                               text="💬 Command Input 💬",
                               bg="#1a1a1a",
                               fg="#00d4ff",
                               font=("Impact", 14, "bold"))
        input_label.pack(anchor="w", pady=(0, 10))

        input_container = tk.Frame(input_frame, bg="#1a1a1a")
        input_container.pack(fill="x")

        self.command_input = tk.Entry(input_container,
                                      bg="#0a0a0a",
                                      fg="#ffffff",
                                      font=("Consolas", 13),
                                      insertbackground="#00ff88",
                                      relief="solid",
                                      borderwidth=2,
                                      highlightbackground="#ffffff",
                                      highlightcolor="#00d4ff",
                                      highlightthickness=1)
        self.command_input.pack(side="left", fill="both", expand=True, ipady=12, padx=(0, 10))
        self.command_input.bind("<Return>", lambda e: self.execute_command())

        # Voice command buttons
        voice_frame = tk.Frame(input_container, bg="#1a1a1a")
        voice_frame.pack(side="right", padx=(0, 10))

        self.voice_listen_btn = tk.Button(voice_frame,
                                          text="🎤",
                                          bg="#00ff88",
                                          fg="#000000",
                                          font=("Arial Black", 14, "bold"),
                                          relief="solid",
                                          borderwidth=2,
                                          cursor="hand2",
                                          command=self.start_voice_listen,
                                          padx=12,
                                          pady=10,
                                          highlightbackground="#ffffff",
                                          activebackground="#00d4ff")
        self.voice_listen_btn.pack(side="left", padx=2)
        self.add_hover_effect(self.voice_listen_btn, "#00ff88", "#00d4ff")

        self.voice_continuous_btn = tk.Button(voice_frame,
                                              text="🔊",
                                              bg="#b19cd9",
                                              fg="#000000",
                                              font=("Arial Black", 12, "bold"),
                                              relief="solid",
                                              borderwidth=2,
                                              cursor="hand2",
                                              command=self.toggle_continuous_listening,
                                              padx=12,
                                              pady=10,
                                              highlightbackground="#ffffff",
                                              activebackground="#ff0080")
        self.voice_continuous_btn.pack(side="left", padx=2)
        self.add_hover_effect(self.voice_continuous_btn, "#b19cd9", "#ff0080")

        # Wake word toggle button
        self.wake_word_btn = tk.Button(voice_frame,
                                       text="💬",
                                       bg="#00d4ff",
                                       fg="#000000",
                                       font=("Arial Black", 11, "bold"),
                                       relief="solid",
                                       borderwidth=2,
                                       cursor="hand2",
                                       command=self.toggle_wake_word,
                                       padx=10,
                                       pady=10,
                                       highlightbackground="#ffffff",
                                       activebackground="#00ff88")
        self.wake_word_btn.pack(side="left", padx=2)
        self.add_hover_effect(self.wake_word_btn, "#00d4ff", "#00ff88")

        # Sound effects toggle button
        self.sound_fx_btn = tk.Button(voice_frame,
                                      text="🔊",
                                      bg="#a6e3a1",
                                      fg="#0f0f1e",
                                      font=("Segoe UI", 11, "bold"),
                                      relief="flat",
                                      cursor="hand2",
                                      command=self.toggle_sound_effects,
                                      padx=10,
                                      pady=10,
                                      activebackground="#94e2d5")
        self.sound_fx_btn.pack(side="left", padx=2)
        self.add_hover_effect(self.sound_fx_btn, "#a6e3a1", "#94e2d5")

        # Right-click to open sound settings
        self.sound_fx_btn.bind("<Button-3>", lambda e: self.show_sound_settings())

        self.execute_btn = tk.Button(input_container,
                                     text="⚡ Execute ⚡",
                                     bg="#00ff88",
                                     fg="#000000",
                                     font=("Arial Black", 13, "bold"),
                                     relief="solid",
                                     borderwidth=2,
                                     cursor="hand2",
                                     command=self.execute_command,
                                     padx=25,
                                     pady=12,
                                     highlightbackground="#ffffff",
                                     activebackground="#00d4ff")
        self.execute_btn.pack(side="right")
        self.add_hover_effect(self.execute_btn, "#00ff88", "#00d4ff")

        output_card = tk.Frame(
            right_panel,
            bg="#1a1a1a",
            relief="solid",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        output_card.pack(fill="both", expand=True, pady=5, padx=5)

        output_header = tk.Frame(output_card, bg="#1a1a1a")
        output_header.pack(fill="x", padx=15, pady=(15, 10))

        output_label = tk.Label(output_header,
                                text="📋 Output Console 📋",
                                bg="#1a1a1a",
                                fg="#00d4ff",
                                font=("Impact", 14, "bold"))
        output_label.pack(side="left")

        clear_console_btn = tk.Button(output_header,
                                      text="🗑️ Clear",
                                      bg="#ff0080",
                                      fg="#ffffff",
                                      font=("Arial Black", 10, "bold"),
                                      relief="solid",
                                      borderwidth=2,
                                      cursor="hand2",
                                      command=self.clear_output,
                                      padx=15,
                                      pady=5,
                                      highlightbackground="#ffffff",
                                      activebackground="#b19cd9")
        clear_console_btn.pack(side="right")
        self.add_hover_effect(clear_console_btn, "#ff0080", "#b19cd9")

        self.output_area = scrolledtext.ScrolledText(output_card,
                                                     bg="#0a0a0a",
                                                     fg="#ffffff",
                                                     font=("Consolas", 11),
                                                     relief="solid",
                                                     borderwidth=2,
                                                     padx=15,
                                                     pady=15,
                                                     wrap="word",
                                                     insertbackground="#00ff88",
                                                     highlightbackground="#ffffff",
                                                     highlightthickness=1)
        self.output_area.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.output_area.config(state="disabled")

        bottom_frame = tk.Frame(
            self.root,
            bg="#1a1a1a",
            pady=12,
            padx=20,
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        bottom_frame.pack(fill="x", side="bottom", padx=5, pady=5)

        button_config = {
            "bg": "#0a0a0a",
            "fg": "#ffffff",
            "font": ("Arial Black", 10, "bold"),
            "relief": "solid",
            "borderwidth": 2,
            "cursor": "hand2",
            "padx": 18,
            "pady": 8,
            "highlightbackground": "#ffffff",
            "activebackground": "#00d4ff"
        }

        help_btn = tk.Button(bottom_frame, text="❓ Full Help", command=self.show_help, **button_config)
        help_btn.pack(side="left", padx=5)
        self.add_hover_effect(help_btn, "#0a0a0a", "#00d4ff")

        contacts_btn = tk.Button(bottom_frame, text="👥 Contacts", command=self.show_contacts, **button_config)
        contacts_btn.pack(side="left", padx=5)
        self.add_hover_effect(contacts_btn, "#0a0a0a", "#00ff88")

        about_btn = tk.Button(bottom_frame, text="ℹ️ About", command=self.show_about, **button_config)
        about_btn.pack(side="left", padx=5)
        self.add_hover_effect(about_btn, "#0a0a0a", "#b19cd9")

        suggest_btn = tk.Button(bottom_frame, text="💡 Suggestion", command=self.show_suggestion, **button_config)
        suggest_btn.pack(side="left", padx=5)
        self.add_hover_effect(suggest_btn, "#0a0a0a", "#ff0080")

        security_btn = tk.Button(bottom_frame, text="🛡️ Security", command=self.show_security_dashboard,
                                 **button_config)
        security_btn.pack(side="left", padx=5)
        self.add_hover_effect(security_btn, "#0a0a0a", "#00d4ff")

        status_container = tk.Frame(
            bottom_frame,
            bg="#0a0a0a",
            relief="solid",
            highlightbackground="#ffffff",
            highlightthickness=2
        )
        status_container.pack(side="right", padx=10, pady=0)

        self.status_label = tk.Label(status_container,
                                     text="✅ Ready",
                                     bg="#0a0a0a",
                                     fg="#00ff88",
                                     font=("Consolas", 11, "bold"),
                                     padx=20,
                                     pady=10)
        self.status_label.pack()

    def add_gradient_effect(self, widget):
        widget.configure(highlightbackground="#45475a", highlightthickness=1)

    def add_hover_effect(self, button, normal_color, hover_color):
        def on_enter(e):
            button['background'] = hover_color

        def on_leave(e):
            button['background'] = normal_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def start_time_update(self):
        def update_time():
            current_time = datetime.now().strftime("%A, %B %d, %Y • %I:%M:%S %p")
            self.time_label.config(text=current_time)
            self.root.after(1000, update_time)

        update_time()

    def create_vatsal_ai_tab(self, notebook):
        """Simple VATSAL Chatbot"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="💬 VATSAL Chat")

        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="💬 VATSAL - Simple AI Chatbot",
                          bg="#1a1a2e",
                          fg="#89b4fa",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="For direct and Quick Questions and Answers , giveing bot",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        self.vatsal_conversation_display = scrolledtext.ScrolledText(
            tab,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 10),
            wrap=tk.WORD,
            height=12,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.vatsal_conversation_display.pack(fill="both", expand=False, padx=10, pady=(10, 5))

        self.vatsal_conversation_display.tag_config("vatsal", foreground="#89b4fa", font=("Consolas", 10, "bold"))
        self.vatsal_conversation_display.tag_config("user", foreground="#a6e3a1", font=("Consolas", 10, "bold"))
        self.vatsal_conversation_display.tag_config("timestamp", foreground="#6c7086", font=("Consolas", 8))

        input_frame = tk.Frame(tab, bg="#1e1e2e")
        input_frame.pack(fill="x", padx=10, pady=5)

        input_label = tk.Label(input_frame,
                               text="💬 Type your message:",
                               bg="#1e1e2e",
                               fg="#a6adc8",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(5, 2))

        input_box_frame = tk.Frame(input_frame, bg="#1e1e2e")
        input_box_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.vatsal_input = tk.Entry(input_box_frame,
                                     bg="#313244",
                                     fg="#ffffff",
                                     font=("Segoe UI", 12),
                                     relief="solid",
                                     bd=2,
                                     insertbackground="#89b4fa")
        self.vatsal_input.pack(side="left", fill="x", expand=True, ipady=10)
        self.vatsal_input.bind("<Return>", lambda e: self.send_to_vatsal_ai())

        send_btn = tk.Button(input_box_frame,
                             text="➤ Send",
                             bg="#89b4fa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 11, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.send_to_vatsal_ai,
                             padx=25,
                             pady=10)
        send_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(send_btn, "#89b4fa", "#74c7ec")

        button_frame = tk.Frame(tab, bg="#1e1e2e")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        start_btn = tk.Button(button_frame,
                              text="▶️ Start Conversation",
                              bg="#313244",
                              fg="#ffffff",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.start_vatsal_ai_conversation,
                              padx=15,
                              pady=8)
        start_btn.pack(side="left", padx=5)
        self.add_hover_effect(start_btn, "#313244", "#45475a")

        suggest_btn = tk.Button(button_frame,
                                text="💡 Help Me Start",
                                bg="#313244",
                                fg="#ffffff",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.vatsal_ai_get_suggestion,
                                padx=15,
                                pady=8)
        suggest_btn.pack(side="left", padx=5)
        self.add_hover_effect(suggest_btn, "#313244", "#45475a")

        clear_btn = tk.Button(button_frame,
                              text="🗑️ Clear Chat",
                              bg="#313244",
                              fg="#ffffff",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.clear_vatsal_ai_conversation,
                              padx=15,
                              pady=8)
        clear_btn.pack(side="left", padx=5)
        self.add_hover_effect(clear_btn, "#313244", "#45475a")

        stats_btn = tk.Button(button_frame,
                              text="📊 View Stats",
                              bg="#313244",
                              fg="#ffffff",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.show_vatsal_ai_stats,
                              padx=15,
                              pady=8)
        stats_btn.pack(side="left", padx=5)
        self.add_hover_effect(stats_btn, "#313244", "#45475a")

    def create_vatsal_automator_tab(self, notebook):
        """VATSAL Intelligent Desktop Automator - Local execution with AI understanding"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="⚡ VATSAL Auto")

        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="⚡ VATSAL Desktop Automator",
                          bg="#1a1a2e",
                          fg="#f9e2af",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🤖 AI Understanding • 💻 Local Execution • ⚠️ Safe Confirmations",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        description_frame = tk.Frame(tab, bg="#1e1e2e")
        description_frame.pack(fill="x", padx=10, pady=5)

        desc_text = tk.Label(description_frame,
                             text="Intelligent desktop automation that uses Gemini only for understanding commands.\nAll actions execute locally via Python modules. Destructive actions require confirmation.",
                             bg="#1e1e2e",
                             fg="#6c7086",
                             font=("Segoe UI", 9),
                             justify="left")
        desc_text.pack(anchor="w", padx=10, pady=5)

        self.vatsal_automator_output = scrolledtext.ScrolledText(
            tab,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 10),
            wrap=tk.WORD,
            height=10,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.vatsal_automator_output.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.vatsal_automator_output.tag_config("success", foreground="#a6e3a1")
        self.vatsal_automator_output.tag_config("error", foreground="#f38ba8")
        self.vatsal_automator_output.tag_config("warning", foreground="#f9e2af")
        self.vatsal_automator_output.tag_config("info", foreground="#89b4fa")

        input_frame = tk.Frame(tab, bg="#1e1e2e")
        input_frame.pack(fill="x", padx=10, pady=5)

        input_label = tk.Label(input_frame,
                               text="💬 Command (e.g., 'Open notepad and type Hello', 'Show system info'):",
                               bg="#1e1e2e",
                               fg="#a6adc8",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(5, 2))

        input_box_frame = tk.Frame(input_frame, bg="#1e1e2e")
        input_box_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.vatsal_automator_input = tk.Entry(input_box_frame,
                                               bg="#313244",
                                               fg="#ffffff",
                                               font=("Segoe UI", 12),
                                               relief="solid",
                                               bd=2,
                                               insertbackground="#89b4fa")
        self.vatsal_automator_input.pack(side="left", fill="x", expand=True, ipady=10)
        self.vatsal_automator_input.bind("<Return>", lambda e: self.execute_vatsal_automator_command())

        execute_btn = tk.Button(input_box_frame,
                                text="▶️ Execute",
                                bg="#a6e3a1",
                                fg="#0f0f1e",
                                font=("Segoe UI", 11, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.execute_vatsal_automator_command,
                                padx=25,
                                pady=10)
        execute_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(execute_btn, "#a6e3a1", "#94e2d5")

        quick_actions_frame = tk.Frame(tab, bg="#1e1e2e")
        quick_actions_frame.pack(fill="x", padx=10, pady=(0, 10))

        actions_label = tk.Label(quick_actions_frame,
                                 text="⚡ Quick Actions:",
                                 bg="#1e1e2e",
                                 fg="#a6adc8",
                                 font=("Segoe UI", 9, "bold"))
        actions_label.pack(anchor="w", padx=5, pady=(5, 2))

        button_container = tk.Frame(quick_actions_frame, bg="#1e1e2e")
        button_container.pack(fill="x", padx=5)

        quick_actions = [
            ("💻 System Info", "Show system info"),
            ("📸 Screenshot", "Take a screenshot"),
            ("📂 Open Desktop", "Open Desktop folder"),
            ("📝 Notepad", "Open notepad"),
            ("🧹 Clear Output", None)
        ]

        for text, command in quick_actions:
            btn = tk.Button(button_container,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=lambda cmd=command: self.vatsal_quick_action(cmd),
                            padx=12,
                            pady=8)
            btn.pack(side="left", padx=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_self_operating_tab(self, notebook):
        """Self-Operating Computer - Autonomous AI Control with Vision"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🎮 Self-Operating")

        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🎮 Self-Operating Computer",
                          bg="#1a1a2e",
                          fg="#cba6f7",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="👁️ AI Vision • 🖱️ Autonomous Control • 🎯 Goal-Driven Operation",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        desc_frame = tk.Frame(tab, bg="#1e1e2e")
        desc_frame.pack(fill="x", padx=10, pady=5)

        desc_text = tk.Label(desc_frame,
                             text="AI views your screen like a human and autonomously performs mouse/keyboard actions to accomplish objectives.\nInspired by OthersideAI's self-operating-computer, powered by Gemini Vision.",
                             bg="#1e1e2e",
                             fg="#6c7086",
                             font=("Segoe UI", 9),
                             justify="left")
        desc_text.pack(anchor="w", padx=10, pady=5)

        main_container = tk.Frame(tab, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        left_column = tk.Frame(main_container, bg="#1e1e2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        status_frame = tk.Frame(left_column, bg="#313244", relief="flat")
        status_frame.pack(fill="x", pady=(0, 10))

        status_label = tk.Label(status_frame,
                                text="Status: Ready",
                                bg="#313244",
                                fg="#a6e3a1",
                                font=("Segoe UI", 10, "bold"),
                                anchor="w",
                                padx=10,
                                pady=8)
        status_label.pack(fill="x")
        self.soc_status_label = status_label

        input_section = tk.Frame(left_column, bg="#1e1e2e")
        input_section.pack(fill="x", pady=(5, 10))

        input_label = tk.Label(input_section,
                               text="🎯 Enter your objective:",
                               bg="#1e1e2e",
                               fg="#a6adc8",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.soc_objective = tk.Text(input_section,
                                     bg="#313244",
                                     fg="#ffffff",
                                     font=("Segoe UI", 11),
                                     height=3,
                                     relief="solid",
                                     bd=2,
                                     insertbackground="#cba6f7",
                                     padx=8,
                                     pady=8,
                                     wrap=tk.WORD)
        self.soc_objective.pack(fill="x", padx=5)
        self.soc_objective.bind('<Control-Return>', lambda e: self.auto_start_if_enabled())

        hint_label = tk.Label(input_section,
                              text="💡 Tip: Press Ctrl+Enter to quick-start when Auto Mode is enabled",
                              bg="#1e1e2e",
                              fg="#6c7086",
                              font=("Segoe UI", 8, "italic"))
        hint_label.pack(anchor="w", padx=5, pady=(2, 0))

        controls_frame = tk.Frame(left_column, bg="#1e1e2e")
        controls_frame.pack(fill="x", pady=5)

        start_text_btn = tk.Button(controls_frame,
                                   text="▶️ Start (Text)",
                                   bg="#cba6f7",
                                   fg="#0f0f1e",
                                   font=("Segoe UI", 10, "bold"),
                                   relief="flat",
                                   cursor="hand2",
                                   command=self.start_self_operating_text,
                                   padx=20,
                                   pady=10)
        start_text_btn.pack(side="left", expand=True, fill="x", padx=(5, 2))
        self.add_hover_effect(start_text_btn, "#cba6f7", "#b4befe")

        start_voice_btn = tk.Button(controls_frame,
                                    text="🎤 Start (Voice)",
                                    bg="#89b4fa",
                                    fg="#0f0f1e",
                                    font=("Segoe UI", 10, "bold"),
                                    relief="flat",
                                    cursor="hand2",
                                    command=self.start_self_operating_voice,
                                    padx=20,
                                    pady=10)
        start_voice_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(start_voice_btn, "#89b4fa", "#74c7ec")

        stop_btn = tk.Button(controls_frame,
                             text="⏹️ Stop",
                             bg="#f38ba8",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.stop_self_operating,
                             padx=20,
                             pady=10)
        stop_btn.pack(side="left", expand=True, fill="x", padx=(2, 5))
        self.add_hover_effect(stop_btn, "#f38ba8", "#eba0ac")

        toggle_frame = tk.Frame(left_column, bg="#1e1e2e")
        toggle_frame.pack(fill="x", pady=10)

        toggle_label_text = tk.Label(toggle_frame,
                                     text="🔄 Auto Self-Control Mode:",
                                     bg="#1e1e2e",
                                     fg="#a6adc8",
                                     font=("Segoe UI", 9, "bold"))
        toggle_label_text.pack(side="left", padx=5)

        self.auto_control_enabled = False
        self.auto_control_btn = tk.Button(toggle_frame,
                                          text="❌ Disabled",
                                          bg="#313244",
                                          fg="#f38ba8",
                                          font=("Segoe UI", 9, "bold"),
                                          relief="flat",
                                          cursor="hand2",
                                          command=self.toggle_auto_control,
                                          padx=20,
                                          pady=8)
        self.auto_control_btn.pack(side="left", padx=5)
        self.add_hover_effect(self.auto_control_btn, "#313244", "#45475a")

        toggle_info = tk.Label(toggle_frame,
                               text="When enabled, AI will automatically start self-operating mode after commands",
                               bg="#1e1e2e",
                               fg="#6c7086",
                               font=("Segoe UI", 8, "italic"))
        toggle_info.pack(side="left", padx=10)

        examples_frame = tk.Frame(left_column, bg="#1e1e2e")
        examples_frame.pack(fill="x", pady=(10, 5))

        examples_label = tk.Label(examples_frame,
                                  text="💡 Example Objectives:",
                                  bg="#1e1e2e",
                                  fg="#a6adc8",
                                  font=("Segoe UI", 9, "bold"))
        examples_label.pack(anchor="w", padx=5)

        examples_text = tk.Text(examples_frame,
                                bg="#0f0f1e",
                                fg="#89dceb",
                                font=("Consolas", 8),
                                height=5,
                                relief="flat",
                                padx=8,
                                pady=8,
                                wrap=tk.WORD)
        examples_text.pack(fill="x", padx=5, pady=5)
        examples_text.insert("1.0",
                             "• Open Google Chrome and search for Python tutorials\n"
                             "• Open a new file in Notepad and write 'Hello World'\n"
                             "• Go to YouTube and play a video about AI\n"
                             "• Open Calculator and calculate 25 * 47\n"
                             "• Create a new folder on Desktop named 'AI Projects'")
        examples_text.config(state='disabled')

        right_column = tk.Frame(main_container, bg="#1e1e2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📊 Real-Time Output:",
                                bg="#1e1e2e",
                                fg="#a6adc8",
                                font=("Segoe UI", 9, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.soc_output = scrolledtext.ScrolledText(
            right_column,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 9),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.soc_output.pack(fill="both", expand=True, padx=5, pady=5)

        self.soc_output.tag_config("iteration", foreground="#cba6f7", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("thought", foreground="#89dceb")
        self.soc_output.tag_config("action", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("progress", foreground="#f9e2af")
        self.soc_output.tag_config("success", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("error", foreground="#f38ba8", font=("Consolas", 9, "bold"))
        self.soc_output.tag_config("warning", foreground="#f9e2af")

        bottom_frame = tk.Frame(tab, bg="#1e1e2e")
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

        buttons = [
            ("📖 View Guide", self.show_soc_guide, "#89b4fa"),
            ("🔄 Clear Output", self.clear_soc_output, "#313244"),
            ("📸 View Screenshots", self.view_soc_screenshots, "#89dceb")
        ]

        for text, command, color in buttons:
            btn = tk.Button(bottom_frame,
                            text=text,
                            bg=color,
                            fg="#0f0f1e" if color != "#313244" else "#ffffff",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            padx=15,
                            pady=8)
            btn.pack(side="left", expand=True, fill="x", padx=3)
            hover_color = "#b4befe" if color == "#89b4fa" else "#74c7ec" if color == "#89dceb" else "#45475a"
            self.add_hover_effect(btn, color, hover_color)

    def create_comprehensive_controller_tab(self, notebook):
        """
        Comprehensive Desktop Controller Tab for GUI
        This creates the UI tab for the 3-phase automation system
        3-Phase Desktop Automation Controller Tab
        - Phase 1: Understand the Prompt
        - Phase 2: Break into Steps
        - Phase 3: Monitor & Execute
        """
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🎯 Smart Control")

        # Header
        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🎯 Comprehensive Desktop Controller",
                          bg="#1a1a2e",
                          fg="#f9e2af",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🧠 Understands → 📋 Plans → 👁️ Monitors • AI-Powered 3-Phase Automation",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Phase indicator
        phase_frame = tk.Frame(tab, bg="#1e1e2e")
        phase_frame.pack(fill="x", padx=10, pady=5)

        self.phase_labels = {}
        phases = [
            ("🧠", "UNDERSTAND", "#89b4fa"),
            ("📋", "PLAN", "#f9e2af"),
            ("👁️", "MONITOR", "#a6e3a1")
        ]

        for icon, name, color in phases:
            phase_container = tk.Frame(phase_frame, bg="#313244", relief="flat")
            phase_container.pack(side="left", expand=True, fill="x", padx=5, pady=5)

            label = tk.Label(phase_container,
                             text=f"{icon} {name}",
                             bg="#313244",
                             fg=color,
                             font=("Segoe UI", 9, "bold"),
                             pady=8)
            label.pack()
            self.phase_labels[name] = label

        # Main container with two columns
        main_container = tk.Frame(tab, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Input and controls
        left_column = tk.Frame(main_container, bg="#1e1e2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Input section
        input_section = tk.Frame(left_column, bg="#1e1e2e")
        input_section.pack(fill="x", pady=(5, 10))

        input_label = tk.Label(input_section,
                               text="🎯 Enter your automation command:",
                               bg="#1e1e2e",
                               fg="#a6adc8",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(0, 5))

        # Input box with send button
        input_box_frame = tk.Frame(input_section, bg="#1e1e2e")
        input_box_frame.pack(fill="x", padx=5)

        self.comprehensive_input = tk.Entry(input_box_frame,
                                            bg="#313244",
                                            fg="#ffffff",
                                            font=("Segoe UI", 11),
                                            relief="solid",
                                            bd=2,
                                            insertbackground="#f9e2af")
        self.comprehensive_input.pack(side="left", fill="x", expand=True, ipady=8)
        self.comprehensive_input.bind("<Return>", lambda e: self.execute_comprehensive_command())

        execute_btn = tk.Button(input_box_frame,
                                text="▶️ Execute",
                                bg="#f9e2af",
                                fg="#0f0f1e",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.execute_comprehensive_command,
                                padx=20,
                                pady=8)
        execute_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(execute_btn, "#f9e2af", "#f5c2e7")

        # Quick actions section with navigation
        self.quick_actions_container = tk.Frame(left_column, bg="#1e1e2e")
        self.quick_actions_container.pack(fill="both", expand=True, pady=(5, 10))

        # Create main menu view
        self.quick_menu_view = tk.Frame(self.quick_actions_container, bg="#1e1e2e")

        # Header
        menu_header = tk.Label(self.quick_menu_view,
                               text="⚡ Quick Actions Centre",
                               bg="#1e1e2e",
                               fg="#f9e2af",
                               font=("Segoe UI", 11, "bold"))
        menu_header.pack(anchor="w", padx=8, pady=(5, 2))

        # Subtitle
        menu_subtitle = tk.Label(self.quick_menu_view,
                                 text="Choose an action below",
                                 bg="#1e1e2e",
                                 fg="#6c7086",
                                 font=("Segoe UI", 8))
        menu_subtitle.pack(anchor="w", padx=8, pady=(0, 8))

        # Scrollable menu
        menu_canvas = tk.Canvas(self.quick_menu_view, bg="#1e1e2e", highlightthickness=0, height=400)
        menu_scrollbar = ttk.Scrollbar(self.quick_menu_view, orient="vertical", command=menu_canvas.yview)
        menu_scrollable = tk.Frame(menu_canvas, bg="#1e1e2e")

        menu_scrollable.bind(
            "<Configure>",
            lambda e: menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))
        )

        menu_canvas.create_window((0, 0), window=menu_scrollable, anchor="nw", width=400)
        menu_canvas.configure(yscrollcommand=menu_scrollbar.set)

        # Define quick actions with features
        self.quick_actions_data = [
            ("🖥️ SYSTEM", None, "#89b4fa", True, None),
            ("💻 Screenshot", "Take a screenshot", "#89b4fa", False, "screenshot"),
            ("🔒 Lock PC", "Lock the computer", "#f38ba8", False, "lock"),
            ("📊 Task Manager", "Open Task Manager", "#cba6f7", False, "taskmanager"),

            ("🌐 WEB & APPS", None, "#89dceb", True, None),
            ("🌍 Chrome", "Open Chrome and go to Google", "#89dceb", False, "chrome"),
            ("🔍 Google Search", "Search Google for Python tutorials", "#a6e3a1", False, "google"),
            ("📧 Gmail", "Open Gmail in browser", "#f38ba8", False, "gmail"),
            ("💬 WhatsApp", "Open WhatsApp Web", "#a6e3a1", False, "whatsapp"),

            ("📁 PRODUCTIVITY", None, "#a6e3a1", True, None),
            ("📝 VS Code", "Launch VS Code", "#89b4fa", False, "vscode"),
            ("📂 File Explorer", "Open File Explorer", "#f9e2af", False, "explorer"),
            ("🗒️ Notepad", "Open Notepad", "#cba6f7", False, "notepad"),

            ("🎵 MEDIA", None, "#f5c2e7", True, None),
            ("🎵 Spotify", "Launch Spotify", "#a6e3a1", False, "spotify"),
            ("🎬 YouTube", "Open YouTube", "#f38ba8", False, "youtube"),
            ("🔊 Volume", "Control system volume", "#89dceb", False, "volume"),
        ]

        # Create menu buttons
        for item in self.quick_actions_data:
            text, description, color, is_header, feature_id = item

            if is_header:
                header_container = tk.Frame(menu_scrollable, bg="#1e1e2e", height=35)
                header_container.pack(fill="x", padx=5, pady=(8, 3))
                header_container.pack_propagate(False)

                accent = tk.Frame(header_container, bg=color, width=3)
                accent.pack(side="left", fill="y", padx=(0, 8))

                header_label = tk.Label(header_container,
                                        text=text,
                                        bg="#1e1e2e",
                                        fg=color,
                                        font=("Segoe UI", 9, "bold"))
                header_label.pack(side="left", pady=8)
            else:
                btn = tk.Button(menu_scrollable,
                                text=text,
                                bg="#313244",
                                fg="#cdd6f4",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=lambda t=text, d=description, c=color,
                                               f=feature_id: self.show_quick_action_feature(t, d, c, f),
                                padx=15,
                                pady=10,
                                anchor="w",
                                bd=0)
                btn.pack(fill="x", padx=8, pady=2)

                def make_hover(button, accent_color):
                    def on_enter(e):
                        button.config(bg="#45475a", fg=accent_color)

                    def on_leave(e):
                        button.config(bg="#313244", fg="#cdd6f4")

                    button.bind("<Enter>", on_enter)
                    button.bind("<Leave>", on_leave)

                make_hover(btn, color)

        self.menu_canvas.pack(side="left", fill="both", expand=True)
        menu_scrollbar.pack(side="right", fill="y")

        # Create feature view (initially hidden)
        self.quick_feature_view = tk.Frame(self.quick_actions_container, bg="#1e1e2e")

        # Feature view header
        feature_header_frame = tk.Frame(self.quick_feature_view, bg="#1e1e2e", height=50)
        feature_header_frame.pack(fill="x", pady=(0, 10))
        feature_header_frame.pack_propagate(False)

        # Back button
        self.back_button = tk.Button(feature_header_frame,
                                     text="← Back",
                                     bg="#313244",
                                     fg="#89b4fa",
                                     font=("Segoe UI", 10, "bold"),
                                     relief="flat",
                                     cursor="hand2",
                                     command=self.show_quick_actions_menu,
                                     padx=15,
                                     pady=8)
        self.back_button.pack(side="left", padx=8, pady=8)
        self.add_hover_effect(self.back_button, "#313244", "#45475a")

        # Feature title
        self.feature_title = tk.Label(feature_header_frame,
                                      text="",
                                      bg="#1e1e2e",
                                      fg="#f9e2af",
                                      font=("Segoe UI", 12, "bold"))
        self.feature_title.pack(side="left", padx=10, pady=8)

        # Feature content area
        self.feature_content = tk.Frame(self.quick_feature_view, bg="#181825", relief="flat")
        self.feature_content.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Show menu view by default
        self.quick_menu_view.pack(fill="both", expand=True)

        # Example prompts
        examples_frame = tk.Frame(left_column, bg="#1e1e2e")
        examples_frame.pack(fill="x", pady=(10, 5))

        examples_label = tk.Label(examples_frame,
                                  text="💡 Example Prompts:",
                                  bg="#1e1e2e",
                                  fg="#a6adc8",
                                  font=("Segoe UI", 9, "bold"))
        examples_label.pack(anchor="w", padx=5)

        examples_text = tk.Text(examples_frame,
                                bg="#0f0f1e",
                                fg="#89dceb",
                                font=("Consolas", 8),
                                height=4,
                                relief="flat",
                                padx=8,
                                pady=8,
                                wrap=tk.WORD)
        examples_text.pack(fill="x", padx=5, pady=5)
        examples_text.insert("1.0",
                             "• Open Chrome, navigate to GitHub, and screenshot\n"
                             "• Launch Spotify and play jazz music\n"
                             "• Search Google for Python tutorials, open first 3 results\n"
                             "• Create a new folder on Desktop named 'Projects'")
        examples_text.config(state='disabled')

        # Right column - Output
        right_column = tk.Frame(main_container, bg="#1e1e2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📊 Execution Output:",
                                bg="#1e1e2e",
                                fg="#a6adc8",
                                font=("Segoe UI", 9, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(0, 5))

        # Output display with scrollbar
        self.comprehensive_output = scrolledtext.ScrolledText(
            right_column,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 9),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.comprehensive_output.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure text tags for colored output
        self.comprehensive_output.tag_config("phase1", foreground="#89b4fa", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("phase2", foreground="#f9e2af", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("phase3", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("success", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("error", foreground="#f38ba8", font=("Consolas", 9, "bold"))
        self.comprehensive_output.tag_config("info", foreground="#89dceb")
        self.comprehensive_output.tag_config("highlight", foreground="#f9e2af", font=("Consolas", 9, "bold"))

        # Bottom buttons
        bottom_frame = tk.Frame(tab, bg="#1e1e2e")
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

        buttons = [
            ("📖 View Guide", self.show_comprehensive_guide, "#89b4fa"),
            ("🔄 Clear Output", self.clear_comprehensive_output, "#313244"),
            ("📸 View Screenshots", self.view_comprehensive_screenshots, "#89dceb"),
            ("📊 View Stats", self.show_comprehensive_stats, "#a6e3a1")
        ]

        for btn_text, command, color in buttons:
            btn = tk.Button(bottom_frame,
                            text=btn_text,
                            bg=color,
                            fg="#0f0f1e" if color != "#313244" else "#ffffff",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            padx=15,
                            pady=8)
            btn.pack(side="left", padx=5)
            hover_color = "#74c7ec" if color == "#89b4fa" else "#45475a" if color == "#313244" else color
            self.add_hover_effect(btn, color, hover_color)

        # Status indicator
        status_container = tk.Frame(bottom_frame, bg="#313244", relief="flat")
        status_container.pack(side="right", padx=5)

        self.comprehensive_status = tk.Label(status_container,
                                             text="✅ Ready",
                                             bg="#313244",
                                             fg="#a6e3a1",
                                             font=("Segoe UI", 9, "bold"),
                                             padx=15,
                                             pady=8)
        self.comprehensive_status.pack()

        # Initial welcome message
        self.append_comprehensive_output("=" * 60 + "\n", "info")
        self.append_comprehensive_output("🎯 COMPREHENSIVE DESKTOP CONTROLLER\n", "highlight")
        self.append_comprehensive_output("=" * 60 + "\n\n", "info")
        self.append_comprehensive_output("Welcome! This system:\n", "info")
        self.append_comprehensive_output("  🧠 Phase 1: ", "phase1")
        self.append_comprehensive_output("Understands your prompt deeply\n", "info")
        self.append_comprehensive_output("  📋 Phase 2: ", "phase2")
        self.append_comprehensive_output("Breaks it into executable steps\n", "info")
        self.append_comprehensive_output("  👁️  Phase 3: ", "phase3")
        self.append_comprehensive_output("Monitors screen in real-time\n\n", "info")
        self.append_comprehensive_output("💡 Try a command above or use Quick Actions!\n", "highlight")
        self.append_comprehensive_output("=" * 60 + "\n", "info")

    def create_vlm_tab(self, notebook):
        """
        Virtual Language Model GUI Tab
        Self-learning AI that observes, learns, and controls
        """
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🧠 Learning AI")

        # Header
        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🧠 Virtual Language Model",
                          bg="#1a1a2e",
                          fg="#cba6f7",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="👁️ Observes Screen → 📚 Learns Patterns → 🎯 Controls Desktop",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Main container with two columns
        main_container = tk.Frame(tab, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Controls
        left_column = tk.Frame(main_container, bg="#1e1e2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Learning stats
        stats_frame = tk.Frame(left_column, bg="#313244", relief="flat")
        stats_frame.pack(fill="x", pady=5, padx=5)

        stats_title = tk.Label(stats_frame,
                               text="📊 Learning Statistics",
                               bg="#313244",
                               fg="#cba6f7",
                               font=("Segoe UI", 10, "bold"))
        stats_title.pack(pady=8)

        self.vlm_stats_display = tk.Text(stats_frame,
                                         bg="#0f0f1e",
                                         fg="#cdd6f4",
                                         font=("Consolas", 9),
                                         height=6,
                                         relief="flat",
                                         padx=10,
                                         pady=10,
                                         state='disabled')
        self.vlm_stats_display.pack(fill="x", padx=5, pady=(0, 8))

        # Goal input section
        goal_frame = tk.Frame(left_column, bg="#1e1e2e")
        goal_frame.pack(fill="x", pady=(10, 5))

        goal_label = tk.Label(goal_frame,
                              text="🎯 Goal for AI:",
                              bg="#1e1e2e",
                              fg="#a6adc8",
                              font=("Segoe UI", 9, "bold"))
        goal_label.pack(anchor="w", padx=5, pady=(0, 5))

        goal_input_frame = tk.Frame(goal_frame, bg="#1e1e2e")
        goal_input_frame.pack(fill="x", padx=5)

        self.vlm_goal_input = tk.Entry(goal_input_frame,
                                       bg="#313244",
                                       fg="#ffffff",
                                       font=("Segoe UI", 11),
                                       relief="solid",
                                       bd=2,
                                       insertbackground="#cba6f7")
        self.vlm_goal_input.pack(side="left", fill="x", expand=True, ipady=8)

        # Action buttons
        actions_frame = tk.Frame(left_column, bg="#1e1e2e")
        actions_frame.pack(fill="x", pady=10, padx=5)

        actions_label = tk.Label(actions_frame,
                                 text="⚡ Actions:",
                                 bg="#1e1e2e",
                                 fg="#a6adc8",
                                 font=("Segoe UI", 9, "bold"))
        actions_label.pack(anchor="w", pady=(0, 5))

        # Row 1
        row1 = tk.Frame(actions_frame, bg="#1e1e2e")
        row1.pack(fill="x", pady=2)

        observe_btn = tk.Button(row1,
                                text="👁️ Observe Screen",
                                bg="#89b4fa",
                                fg="#0f0f1e",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.vlm_observe,
                                padx=15,
                                pady=8)
        observe_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(observe_btn, "#89b4fa", "#74c7ec")

        decide_btn = tk.Button(row1,
                               text="🤔 Decide Action",
                               bg="#f9e2af",
                               fg="#0f0f1e",
                               font=("Segoe UI", 9, "bold"),
                               relief="flat",
                               cursor="hand2",
                               command=self.vlm_decide,
                               padx=15,
                               pady=8)
        decide_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(decide_btn, "#f9e2af", "#f5c2e7")

        # Row 2
        row2 = tk.Frame(actions_frame, bg="#1e1e2e")
        row2.pack(fill="x", pady=2)

        execute_btn = tk.Button(row2,
                                text="▶️ Execute",
                                bg="#a6e3a1",
                                fg="#0f0f1e",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.vlm_execute,
                                padx=15,
                                pady=8)
        execute_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(execute_btn, "#a6e3a1", "#94e2d5")

        learn_btn = tk.Button(row2,
                              text="🧠 Learn Session",
                              bg="#cba6f7",
                              fg="#0f0f1e",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.vlm_learn_session,
                              padx=15,
                              pady=8)
        learn_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(learn_btn, "#cba6f7", "#b4befe")

        # Row 3
        row3 = tk.Frame(actions_frame, bg="#1e1e2e")
        row3.pack(fill="x", pady=2)

        query_btn = tk.Button(row3,
                              text="💬 Query Knowledge",
                              bg="#313244",
                              fg="#ffffff",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.vlm_query,
                              padx=15,
                              pady=8)
        query_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(query_btn, "#313244", "#45475a")

        refresh_btn = tk.Button(row3,
                                text="🔄 Refresh Stats",
                                bg="#313244",
                                fg="#ffffff",
                                font=("Segoe UI", 9, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.vlm_refresh_stats,
                                padx=15,
                                pady=8)
        refresh_btn.pack(side="left", expand=True, fill="x", padx=2)
        self.add_hover_effect(refresh_btn, "#313244", "#45475a")

        # Knowledge display
        knowledge_frame = tk.Frame(left_column, bg="#1e1e2e")
        knowledge_frame.pack(fill="both", expand=True, pady=(10, 5))

        knowledge_label = tk.Label(knowledge_frame,
                                   text="📚 Learned Knowledge:",
                                   bg="#1e1e2e",
                                   fg="#a6adc8",
                                   font=("Segoe UI", 9, "bold"))
        knowledge_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.vlm_knowledge_display = scrolledtext.ScrolledText(
            knowledge_frame,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 8),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.vlm_knowledge_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Right column - Output
        right_column = tk.Frame(main_container, bg="#1e1e2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📊 Activity Log:",
                                bg="#1e1e2e",
                                fg="#a6adc8",
                                font=("Segoe UI", 9, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.vlm_output = scrolledtext.ScrolledText(
            right_column,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 9),
            wrap=tk.WORD,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.vlm_output.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure text tags
        self.vlm_output.tag_config("success", foreground="#a6e3a1", font=("Consolas", 9, "bold"))
        self.vlm_output.tag_config("error", foreground="#f38ba8", font=("Consolas", 9, "bold"))
        self.vlm_output.tag_config("info", foreground="#89dceb")
        self.vlm_output.tag_config("highlight", foreground="#cba6f7", font=("Consolas", 9, "bold"))
        self.vlm_output.tag_config("decision", foreground="#f9e2af", font=("Consolas", 9, "bold"))

        # Bottom status
        bottom_frame = tk.Frame(tab, bg="#1e1e2e")
        bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

        help_btn = tk.Button(bottom_frame,
                             text="📖 How It Works",
                             bg="#89b4fa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 9, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.show_vlm_help,
                             padx=15,
                             pady=8)
        help_btn.pack(side="left", padx=5)
        self.add_hover_effect(help_btn, "#89b4fa", "#74c7ec")

        clear_btn = tk.Button(bottom_frame,
                              text="🗑️ Clear Output",
                              bg="#313244",
                              fg="#ffffff",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.vlm_clear_output,
                              padx=15,
                              pady=8)
        clear_btn.pack(side="left", padx=5)
        self.add_hover_effect(clear_btn, "#313244", "#45475a")

        # Status
        status_container = tk.Frame(bottom_frame, bg="#313244", relief="flat")
        status_container.pack(side="right", padx=5)

        self.vlm_status = tk.Label(status_container,
                                   text="✅ Ready to Learn",
                                   bg="#313244",
                                   fg="#a6e3a1",
                                   font=("Segoe UI", 9, "bold"),
                                   padx=15,
                                   pady=8)
        self.vlm_status.pack()

        # Initialize with welcome message
        self.vlm_append_output("=" * 60 + "\n", "info")
        self.vlm_append_output("🧠 VIRTUAL LANGUAGE MODEL\n", "highlight")
        self.vlm_append_output("=" * 60 + "\n\n", "info")
        self.vlm_append_output("Welcome to the self-learning AI system!\n\n", "info")
        self.vlm_append_output("This AI can:\n", "info")
        self.vlm_append_output("  👁️  Observe and analyze your screen\n", "info")
        self.vlm_append_output("  📚 Learn UI patterns and workflows\n", "info")
        self.vlm_append_output("  🤔 Make intelligent decisions\n", "info")
        self.vlm_append_output("  🎯 Execute actions based on learned knowledge\n", "info")
        self.vlm_append_output("  💬 Answer questions about what it learned\n\n", "info")
        self.vlm_append_output("💡 Try: Click 'Observe Screen' to let it see your desktop!\n", "highlight")
        self.vlm_append_output("=" * 60 + "\n", "info")

        # Load initial stats
        self.vlm_refresh_stats()

    def create_web_automation_tab(self, notebook):
        """Web Automation with Selenium"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🌐 Web Auto")

        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🌐 Intelligent Web Automation",
                          bg="#1a1a2e",
                          fg="#89dceb",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🤖 AI-Powered Browser Control • Works in Replit Cloud",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        input_section = tk.Frame(tab, bg="#1e1e2e")
        input_section.pack(fill="x", padx=10, pady=10)

        input_label = tk.Label(input_section,
                               text="💬 Natural Language Command:",
                               bg="#1e1e2e",
                               fg="#a6adc8",
                               font=("Segoe UI", 9, "bold"))
        input_label.pack(anchor="w", padx=5, pady=(5, 2))

        input_box_frame = tk.Frame(input_section, bg="#1e1e2e")
        input_box_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.web_auto_input = tk.Entry(input_box_frame,
                                       bg="#313244",
                                       fg="#ffffff",
                                       font=("Segoe UI", 11),
                                       relief="solid",
                                       bd=2,
                                       insertbackground="#89dceb")
        self.web_auto_input.pack(side="left", fill="x", expand=True, ipady=8)
        self.web_auto_input.bind("<Return>", lambda e: self.execute_web_automation())

        execute_btn = tk.Button(input_box_frame,
                                text="🚀 Execute",
                                bg="#89dceb",
                                fg="#0f0f1e",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=self.execute_web_automation,
                                padx=20,
                                pady=8)
        execute_btn.pack(side="right", padx=(5, 0))
        self.add_hover_effect(execute_btn, "#89dceb", "#74c7ec")

        quick_frame = tk.Frame(tab, bg="#1a1a2e")
        quick_frame.pack(fill="both", expand=True, padx=10, pady=10)

        quick_label = tk.Label(quick_frame,
                               text="⚡ Quick Actions",
                               bg="#1a1a2e",
                               fg="#f9e2af",
                               font=("Segoe UI", 11, "bold"))
        quick_label.pack(pady=10)

        canvas = tk.Canvas(quick_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(quick_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        quick_actions = [
            ("🎯 LeetCode Problem 34", "open leetcode problem 34"),
            ("🎯 LeetCode Problem 1", "open leetcode problem 1"),
            ("📚 LeetCode Problemset", "open https://leetcode.com/problemset/all/"),
            ("🔍 Search GitHub Python", "search github for python automation"),
            ("🌟 GitHub Trending Python", "open https://github.com/trending/python"),
            ("🌟 GitHub Trending", "open https://github.com/trending"),
            ("💡 Search Google ML", "search google for machine learning"),
            ("🔎 Search StackOverflow", "search stackoverflow for python async"),
            ("📺 YouTube Python Tutorial", "search youtube for python tutorial"),
            ("📺 YouTube Coding", "search youtube for coding tutorials"),
        ]

        for text, command in quick_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 9),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_web_automation(c),
                            anchor="w",
                            padx=15,
                            pady=8,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=2)
            self.add_hover_effect(btn, "#313244", "#45475a")

        control_frame = tk.Frame(tab, bg="#1e1e2e")
        control_frame.pack(fill="x", padx=10, pady=(0, 10))

        init_btn = tk.Button(control_frame,
                             text="▶️ Start Browser",
                             bg="#313244",
                             fg="#ffffff",
                             font=("Segoe UI", 9, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.initialize_web_browser,
                             padx=12,
                             pady=6)
        init_btn.pack(side="left", padx=5)
        self.add_hover_effect(init_btn, "#313244", "#45475a")

        close_btn = tk.Button(control_frame,
                              text="🔒 Close Browser",
                              bg="#313244",
                              fg="#ffffff",
                              font=("Segoe UI", 9, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=self.close_web_browser,
                              padx=12,
                              pady=6)
        close_btn.pack(side="left", padx=5)
        self.add_hover_effect(close_btn, "#313244", "#45475a")

        screenshot_btn = tk.Button(control_frame,
                                   text="📸 Screenshot",
                                   bg="#313244",
                                   fg="#ffffff",
                                   font=("Segoe UI", 9, "bold"),
                                   relief="flat",
                                   cursor="hand2",
                                   command=self.take_web_screenshot,
                                   padx=12,
                                   pady=6)
        screenshot_btn.pack(side="left", padx=5)
        self.add_hover_effect(screenshot_btn, "#313244", "#45475a")

    def create_code_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="💻 Code")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("🤖 Generate Palindrome Checker", "Write code for checking palindrome"),
            ("🔢 Generate Bubble Sort", "Generate Python code for bubble sort"),
            ("🧮 Generate Calculator", "Create JavaScript code for calculator"),
            ("📊 Generate Data Analysis", "Write Python code for data analysis"),
            ("🔐 Generate Password Generator", "Create code for password generator"),
            ("🌐 Generate Web Scraper", "Write Python code for web scraping"),
            ("📝 Generate Todo App", "Create JavaScript todo app"),
            ("🎮 Generate Game Logic", "Write Python code for tic-tac-toe game"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_desktop_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🖥️ Desktop")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame,
                 text="🗂️ Desktop File Controller",
                 bg="#1e1e2e",
                 fg="#f9e2af",
                 font=("Segoe UI", 12, "bold"),
                 pady=10).pack(fill="x", padx=8)

        file_controller_actions = [
            ("🗂️ Launch Batch Controller", lambda: self.launch_batch_controller()),
            ("📋 List Desktop Items", lambda: self.list_desktop_items()),
            ("➕ Create New Folder", lambda: self.create_desktop_folder()),
            ("📁 Organize Desktop", lambda: self.organize_desktop()),
            ("🔍 Search Desktop Files", lambda: self.search_desktop_files()),
        ]

        for text, command in file_controller_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#45475a",
                            fg="#ffffff",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#585b70")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#45475a", "#585b70")

        tk.Label(scrollable_frame,
                 text="🖥️ Desktop Quick Actions",
                 bg="#1e1e2e",
                 fg="#f9e2af",
                 font=("Segoe UI", 12, "bold"),
                 pady=10).pack(fill="x", padx=8, pady=(15, 0))

        actions = [
            ("📝 Open Notepad", "Open notepad"),
            ("📸 Take Screenshot", "Take a screenshot"),
            ("🔍 Search Google", "Search Google for Python tutorials"),
            ("🌐 Open Browser", "Open chrome"),
            ("📋 Copy Text", "Copy text Hello World to clipboard"),
            ("📁 Create File", "Create file test.txt with content Hello"),
            ("⌨️ Type Text", "Type Hello World"),
            ("🖱️ Analyze Screen", "Analyze current screen"),
            ("📊 Get System Info", "Show system information"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_file_automation_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📁 File Auto")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📅 Rename by Date", "Rename files in Downloads folder by date"),
            ("🔢 Rename Sequential", "Rename files sequentially with numbers"),
            ("📂 Rename by Type", "Rename files by their type"),
            ("📁 Rename by Project", "Rename files using folder name as prefix"),
            ("🔍 Start Folder Monitor", "Monitor Downloads folder for new files"),
            ("⏹️ Stop Folder Monitor", "Stop monitoring folder"),
            ("📊 View Active Monitors", "Show all active folder monitors"),
            ("🗜️ Compress Folder", "Compress Documents folder to ZIP"),
            ("📦 Extract ZIP", "Extract archive.zip to current folder"),
            ("🗂️ Compress Old Files", "Compress files older than 30 days"),
            ("📁 Batch Compress", "Compress multiple files into one archive"),
            ("🔄 Auto-Archive by Age", "Automatically archive old files"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_clipboard_text_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📋 Clipboard & Text")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📋 Paste from Clipboard", "Get text from clipboard"),
            ("📊 Clipboard Info", "Show clipboard information"),
            ("🗑️ Clear Clipboard", "Clear clipboard content"),
            ("📜 Clipboard History", "View clipboard history"),
            ("🔠 UPPERCASE", "Convert clipboard text to uppercase"),
            ("🔡 lowercase", "Convert clipboard text to lowercase"),
            ("🔤 Title Case", "Convert clipboard text to title case"),
            ("✏️ Sentence case", "Convert clipboard text to sentence case"),
            ("🔄 Toggle Case", "Toggle case of clipboard text"),
            ("✂️ Trim Whitespace", "Remove leading and trailing spaces"),
            ("🧹 Remove Extra Spaces", "Remove multiple spaces"),
            ("↔️ Remove Line Breaks", "Remove all line breaks"),
            ("↕️ Add Line Breaks", "Add line breaks at intervals"),
            ("🚫 Remove Special Chars", "Remove special characters"),
            ("🔢 Remove Numbers", "Remove all numbers from text"),
            ("📖 Word Count", "Count words and characters"),
            ("🔄 Reverse Text", "Reverse the text"),
            ("📊 Sort Lines", "Sort lines alphabetically"),
            ("🔗 Extract URLs", "Extract all URLs from text"),
            ("📧 Extract Emails", "Extract all email addresses"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_messaging_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📱 Messaging")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("👥 Add Contact", "Add contact John with phone 555-1234"),
            ("📋 List Contacts", "List all contacts"),
            ("📧 Send Email", "Send email to example@email.com"),
            ("💬 Send WhatsApp", "Send WhatsApp message"),
            ("📨 Email with Template", "Send template email"),
            ("📎 Email with Attachment", "Send email with attachment"),
            ("🎥 Open YouTube", "Search YouTube for music"),
            ("▶️ Play YouTube Video", "Play YouTube video"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_system_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="⚙️ System")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Direct action buttons (lock and shutdown)
        direct_actions = [
            ("🔒 Lock Computer", self.direct_lock_screen, "#f38ba8"),
            ("⚠️ Shutdown Computer", self.direct_shutdown_system, "#f38ba8"),
        ]

        for text, command_func, color in direct_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg=color,
                            fg="#ffffff",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=command_func,
                            anchor="w",
                            padx=15,
                            pady=12,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            hover_color = "#fab387" if color == "#f38ba8" else "#45475a"
            self.add_hover_effect(btn, color, hover_color)

        # Separator
        separator = tk.Frame(scrollable_frame, bg="#45475a", height=2)
        separator.pack(fill="x", padx=8, pady=8)

        # AI-powered actions (through command parsing)
        actions = [
            ("📊 System Report", "Get full system report"),
            ("💾 Check Disk Usage", "Show disk usage"),
            ("🧠 Check Memory", "Show memory usage"),
            ("⚡ CPU Usage", "Get CPU usage"),
            ("📂 Organize Downloads", "Organize downloads folder"),
            ("🔍 Find Large Files", "Find large files"),
            ("📁 Find Duplicates", "Find duplicate files"),
            ("🗜️ Compress Old Files", "Compress files older than 90 days"),
            ("💤 Sleep Computer", "Put computer to sleep"),
            ("🔊 Volume Control", "Set volume to 50"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_productivity_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📈 Productivity")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📊 Screen Time Dashboard", "Show screen time dashboard"),
            ("🎯 Enable Focus Mode", "Enable focus mode for 2 hours"),
            ("🚫 Block Distractions", "Block distracting websites"),
            ("📈 Productivity Score", "Get my productivity score"),
            ("💧 Water Reminder", "Send water reminder"),
            ("📋 Daily Summary", "Generate daily summary"),
            ("📝 Smart Reply", "Generate smart reply"),
            ("✉️ Email Template", "Generate professional email template"),
            ("📊 Workflow Dashboard", "Show workflow dashboard"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_utilities_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🔧 Utilities")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("🌤️ Get Weather", "Get weather for New York"),
            ("📰 Get News", "Get latest technology news"),
            ("🌍 Translate to Spanish", "Translate 'Hello, how are you?' to Spanish"),
            ("🧮 Calculate", "Calculate 2 + 2 * 5"),
            ("💱 Currency Conversion", "Convert 100 USD to EUR"),
            ("🔐 Generate Password", "Generate a strong password"),
            ("🗝️ List Passwords", "List all saved passwords"),
            ("📝 Add Note", "Add note: Meeting tomorrow at 3 PM"),
            ("📋 List Notes", "List all my notes"),
            ("📅 Add Event", "Add event: Team meeting tomorrow at 2 PM"),
            ("📆 Today's Events", "Show today's events"),
            ("🗓️ Upcoming Events", "Show upcoming events"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_ecosystem_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🌐 Ecosystem")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("📊 Unified Dashboard", "Show ecosystem dashboard"),
            ("☀️ Morning Briefing", "Give me morning briefing"),
            ("🌙 Evening Summary", "Show evening summary"),
            ("💡 Smart Suggestions", "Give me smart suggestions"),
            ("🔍 Smart Search", "Smart search for meeting"),
            ("📈 Productivity Insights", "Show productivity insights"),
            ("🧹 Auto Organize", "Auto organize ecosystem"),
            ("⚡ Create Workflow", "Create workflow: Morning Routine"),
            ("📋 List Workflows", "List all workflows"),
            ("🚀 Run Workflow", "Run workflow: Morning Routine"),
            ("🔗 Cross-Module Search", "Search everywhere for project"),
            ("📅 Today Overview", "What's my schedule today?"),
            ("🎯 Daily Goals", "Show my daily goals"),
            ("📊 Weekly Summary", "Generate weekly summary"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_ai_features_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🤖 AI Features")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        header = tk.Label(scrollable_frame,
                          text="🤖 ADVANCED AI CAPABILITIES",
                          bg="#1e1e2e",
                          fg="#89b4fa",
                          font=("Segoe UI", 12, "bold"))
        header.pack(pady=12)

        info = tk.Label(scrollable_frame,
                        text="80+ AI-powered features available",
                        bg="#1e1e2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9))
        info.pack(pady=(0, 15))

        screen_monitor_section = tk.Label(scrollable_frame,
                                          text="👁️ AI SCREEN MONITORING SYSTEM (Next-Gen)",
                                          bg="#1e1e2e",
                                          fg="#f9e2af",
                                          font=("Segoe UI", 11, "bold"))
        screen_monitor_section.pack(pady=(10, 8), anchor="w", padx=8)

        info_label = tk.Label(scrollable_frame,
                              text="Real-time AI monitoring with intelligent triggers, analytics, and automated actions",
                              bg="#1e1e2e",
                              fg="#a6adc8",
                              font=("Segoe UI", 9, "italic"))
        info_label.pack(pady=(0, 8), anchor="w", padx=8)

        screen_monitor_actions = [
            ("📊 Productivity Analysis (Instant)", self.ai_monitor_productivity),
            ("🔒 Security Scan (Instant)", self.ai_monitor_security),
            ("⚡ Performance Analysis (Instant)", self.ai_monitor_performance),
            ("🐛 Error Detection (Instant)", self.ai_monitor_errors),
            ("🎨 UX/Design Review (Instant)", self.ai_monitor_ux),
            ("♿ Accessibility Audit (Instant)", self.ai_monitor_accessibility),
            ("💻 Code Review (Instant)", self.ai_monitor_code),
            ("🤖 Automation Discovery (Instant)", self.ai_monitor_automation),
            ("", None),
            ("🔄 Start Continuous Monitoring", self.ai_monitor_start_continuous),
            ("⏸️ Pause/Resume Monitoring", self.ai_monitor_pause_resume),
            ("🛑 Stop Monitoring", self.ai_monitor_stop),
            ("", None),
            ("📈 View Analytics Dashboard", self.ai_monitor_view_analytics),
            ("📊 Productivity Trends", self.ai_monitor_productivity_trends),
            ("🚨 Recent Alerts", self.ai_monitor_view_alerts),
            ("⚙️ Configure Settings", self.ai_monitor_configure),
            ("🧹 Clear Analytics Data", self.ai_monitor_clear_analytics),
        ]

        for text, command in screen_monitor_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        rag_section = tk.Label(scrollable_frame,
                               text="🧠 DESKTOP RAG - SMART FILE INTELLIGENCE",
                               bg="#1e1e2e",
                               fg="#f9e2af",
                               font=("Segoe UI", 11, "bold"))
        rag_section.pack(pady=(15, 8), anchor="w", padx=8)

        rag_actions = [
            ("🚀 Quick Index My Files", "Index my desktop files"),
            ("📂 Index Specific Folder", "Index C:\\Users folder"),
            ("🔍 Search Files", "Search files for Python"),
            ("💬 Ask About My Files", "What Python projects do I have?"),
            ("📊 Summarize Folder", "Summarize my Documents folder"),
            ("🔎 Find Duplicate Files", "Find duplicate files in my computer"),
            ("📈 Show RAG Statistics", "Show desktop index statistics"),
        ]

        for text, command in rag_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        smart_automation_section = tk.Label(scrollable_frame,
                                            text="🎯 SMART AUTOMATION & AI",
                                            bg="#1e1e2e",
                                            fg="#f9e2af",
                                            font=("Segoe UI", 11, "bold"))
        smart_automation_section.pack(pady=(15, 8), anchor="w", padx=8)

        smart_info = tk.Label(scrollable_frame,
                              text="9 intelligent automation features powered by AI",
                              bg="#1e1e2e",
                              fg="#a6adc8",
                              font=("Segoe UI", 9, "italic"))
        smart_info.pack(pady=(0, 8), anchor="w", padx=8)

        smart_actions = [
            ("🐛 Auto-Bug Fixer", self.smart_auto_bug_fixer),
            ("📅 Meeting Scheduler AI", self.smart_meeting_scheduler),
            ("📁 Smart File Recommendations", self.smart_file_recommender),
            ("📝 Auto-Documentation Generator", self.smart_doc_generator),
            ("⚡ Intelligent Command Shortcuts", self.smart_command_shortcuts),
            ("🔀 Project Context Switcher", self.smart_context_switcher),
            ("🎯 Task Auto-Prioritizer", self.smart_task_prioritizer),
            ("🔧 Workflow Auto-Optimizer", self.smart_workflow_optimizer),
            ("📋 Smart Template Generator", self.smart_template_generator),
            ("", None),
            ("📊 Smart Automation Dashboard", self.smart_automation_dashboard),
        ]

        for text, command in smart_actions:
            if text:
                btn = tk.Button(scrollable_frame,
                                text=text,
                                bg="#313244",
                                fg="#ffffff",
                                font=("Segoe UI", 10),
                                relief="flat",
                                cursor="hand2",
                                command=command,
                                anchor="w",
                                padx=15,
                                pady=10,
                                activebackground="#45475a")
                btn.pack(fill="x", padx=8, pady=3)
                self.add_hover_effect(btn, "#313244", "#45475a")

        ai_section = tk.Label(scrollable_frame,
                              text="💬 AI ASSISTANTS & TEXT GENERATION",
                              bg="#1e1e2e",
                              fg="#f9e2af",
                              font=("Segoe UI", 11, "bold"))
        ai_section.pack(pady=(15, 8), anchor="w", padx=8)

        actions = [
            ("📋 List All AI Features", "List all AI features"),
            ("💬 Conversational AI", "Chat with AI about the weather"),
            ("🎓 Educational Assistant", "Explain quantum physics simply"),
            ("👔 Customer Service Bot", "Help with customer inquiry about returns"),
            ("🎯 Domain Expert", "Ask expert about machine learning"),
            ("📖 Story Writer", "Write a short sci-fi story about robots"),
            ("✍️ Content Creator", "Create a blog post about productivity"),
            ("📰 Article Generator", "Generate article about AI trends"),
            ("🔍 Text Summarizer", "Summarize this text"),
            ("🎨 Creative Writer", "Write a creative poem about nature"),
        ]

        for text, command in actions:
            if text:
                btn = tk.Button(scrollable_frame,
                                text=text,
                                bg="#313244",
                                fg="#ffffff",
                                font=("Segoe UI", 10),
                                relief="flat",
                                cursor="hand2",
                                command=lambda c=command: self.quick_command(c),
                                anchor="w",
                                padx=15,
                                pady=10,
                                activebackground="#45475a")
                btn.pack(fill="x", padx=8, pady=3)
                self.add_hover_effect(btn, "#313244", "#45475a")

    def create_fun_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🎉 Fun")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("💪 Get Motivation", "Give me motivation"),
            ("🎯 Daily Quote", "Send me a quote"),
            ("😄 Tell a Joke", "Tell me a joke"),
            ("🎲 Random Fact", "Tell me a random fact"),
            ("🎮 Play Trivia", "Ask me a trivia question"),
            ("🎨 Generate Art Prompt", "Generate art prompt"),
            ("📚 Book Recommendation", "Recommend a book"),
            ("🎬 Movie Suggestion", "Suggest a movie"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_advanced_ai_tab(self, notebook):
        """Advanced AI Enhancements - Multi-modal, Memory, Learning, Predictions"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🧠 Advanced AI")

        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🧠 Advanced AI Enhancements",
                          bg="#1a1a2e",
                          fg="#cba6f7",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="👁️ Multi-Modal • 🧠 Contextual Memory • 📚 Learning from Corrections • 🔮 Predictive Actions",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        main_container = tk.Frame(tab, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        left_column = tk.Frame(main_container, bg="#1e1e2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        multi_modal_section = tk.Label(left_column,
                                       text="👁️ MULTI-MODAL AI",
                                       bg="#1e1e2e",
                                       fg="#cba6f7",
                                       font=("Segoe UI", 11, "bold"))
        multi_modal_section.pack(pady=(10, 8), anchor="w", padx=8)

        mm_buttons = [
            ("🧠 Analyze Current Screen", lambda: self.advanced_ai_analyze_screen()),
            ("🎤 Voice + Vision Analysis", lambda: self.advanced_ai_voice_vision()),
            ("📊 Multi-Modal Statistics", lambda: self.advanced_ai_mm_stats())
        ]

        for text, command in mm_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        memory_section = tk.Label(left_column,
                                  text="🧠 CONTEXTUAL MEMORY",
                                  bg="#1e1e2e",
                                  fg="#89b4fa",
                                  font=("Segoe UI", 11, "bold"))
        memory_section.pack(pady=(15, 8), anchor="w", padx=8)

        memory_buttons = [
            ("📝 Remember Something", lambda: self.advanced_ai_remember()),
            ("🔍 Recall Memories", lambda: self.advanced_ai_recall()),
            ("⚙️ Update Preferences", lambda: self.advanced_ai_preferences()),
            ("📊 Memory Statistics", lambda: self.advanced_ai_memory_stats())
        ]

        for text, command in memory_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        learning_section = tk.Label(left_column,
                                    text="📚 CORRECTION LEARNING",
                                    bg="#1e1e2e",
                                    fg="#a6e3a1",
                                    font=("Segoe UI", 11, "bold"))
        learning_section.pack(pady=(15, 8), anchor="w", padx=8)

        learning_buttons = [
            ("✏️ Record Correction", lambda: self.advanced_ai_record_correction()),
            ("📈 Learning Report", lambda: self.advanced_ai_learning_report()),
            ("🎯 Apply Learning", lambda: self.advanced_ai_apply_learning())
        ]

        for text, command in learning_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        predictions_section = tk.Label(left_column,
                                       text="🔮 PREDICTIVE ACTIONS",
                                       bg="#1e1e2e",
                                       fg="#f9e2af",
                                       font=("Segoe UI", 11, "bold"))
        predictions_section.pack(pady=(15, 8), anchor="w", padx=8)

        pred_buttons = [
            ("🔮 Get Predictions", lambda: self.advanced_ai_predictions()),
            ("💡 Proactive Suggestions", lambda: self.advanced_ai_suggestions()),
            ("📊 Prediction Accuracy", lambda: self.advanced_ai_accuracy())
        ]

        for text, command in pred_buttons:
            btn = tk.Button(left_column,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        right_column = tk.Frame(main_container, bg="#1e1e2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        output_label = tk.Label(right_column,
                                text="📋 Output Console",
                                bg="#1e1e2e",
                                fg="#ffffff",
                                font=("Segoe UI", 11, "bold"))
        output_label.pack(pady=(10, 5), anchor="w", padx=8)

        self.advanced_ai_output = scrolledtext.ScrolledText(
            right_column,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 10),
            wrap=tk.WORD,
            height=25,
            state='disabled',
            relief="flat",
            padx=10,
            pady=10
        )
        self.advanced_ai_output.pack(fill="both", expand=True, padx=8, pady=(0, 10))

        self.advanced_ai_output.tag_config("success", foreground="#a6e3a1")
        self.advanced_ai_output.tag_config("error", foreground="#f38ba8")
        self.advanced_ai_output.tag_config("warning", foreground="#f9e2af")
        self.advanced_ai_output.tag_config("info", foreground="#89b4fa")
        self.advanced_ai_output.tag_config("prediction", foreground="#cba6f7")

        clear_btn = tk.Button(right_column,
                              text="🗑️ Clear Output",
                              bg="#45475a",
                              fg="#ffffff",
                              font=("Segoe UI", 9),
                              relief="flat",
                              cursor="hand2",
                              command=lambda: self.advanced_ai_clear_output(),
                              padx=15,
                              pady=8)
        clear_btn.pack(pady=(0, 10), padx=8)
        self.add_hover_effect(clear_btn, "#45475a", "#585b70")

    def create_web_tools_tab(self, notebook):
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🌐 Web")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = [
            ("🌐 Launch Web App", "Open In-One-Box web application"),
            ("🔗 Open GitHub", "Open GitHub repository"),
            ("📊 Dashboard View", "Show web dashboard"),
            ("⚙️ Settings Panel", "Open web settings"),
        ]

        for text, command in actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=lambda c=command: self.quick_command(c),
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_productivity_hub_tab(self, notebook):
        """Create comprehensive productivity hub tab with all productivity features"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📊 Productivity Hub")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Pomodoro Section
        pomodoro_section = tk.Label(scrollable_frame,
                                    text="🍅 POMODORO AI COACH",
                                    bg="#1e1e2e",
                                    fg="#f9e2af",
                                    font=("Segoe UI", 11, "bold"))
        pomodoro_section.pack(pady=(10, 8), anchor="w", padx=8)

        pomodoro_actions = [
            ("🍅 Start Pomodoro (25 min)", lambda: self.start_pomodoro_session()),
            ("☕ Take Short Break (5 min)", lambda: self.start_short_break()),
            ("🌳 Take Long Break (15 min)", lambda: self.start_long_break()),
            ("⏸️ Pause/Resume Session", lambda: self.toggle_pomodoro()),
            ("🛑 Stop Session", lambda: self.stop_pomodoro()),
            ("📊 View Pomodoro Stats", lambda: self.view_pomodoro_stats()),
        ]

        for text, command in pomodoro_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Task Time Predictor Section
        task_section = tk.Label(scrollable_frame,
                                text="⏱️ TASK TIME PREDICTOR",
                                bg="#1e1e2e",
                                fg="#f9e2af",
                                font=("Segoe UI", 11, "bold"))
        task_section.pack(pady=(15, 8), anchor="w", padx=8)

        task_actions = [
            ("▶️ Start Task Tracking", lambda: self.start_task_tracking()),
            ("✅ Complete Current Task", lambda: self.complete_task()),
            ("📈 View Task Predictions", lambda: self.view_task_predictions()),
            ("📊 Task Analytics", lambda: self.view_task_analytics()),
        ]

        for text, command in task_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Energy & Focus Section
        energy_section = tk.Label(scrollable_frame,
                                  text="🔋 ENERGY & FOCUS TRACKING",
                                  bg="#1e1e2e",
                                  fg="#f9e2af",
                                  font=("Segoe UI", 11, "bold"))
        energy_section.pack(pady=(15, 8), anchor="w", padx=8)

        energy_actions = [
            ("🔋 Check Energy Level", lambda: self.check_energy_level()),
            ("📈 Energy Trends", lambda: self.view_energy_trends()),
            ("🎯 Get Break Suggestion", lambda: self.get_break_suggestion()),
            ("⚠️ Distraction Check", lambda: self.check_distractions()),
            ("📊 Focus Report", lambda: self.view_focus_report()),
        ]

        for text, command in energy_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Productivity Dashboard Section
        dashboard_section = tk.Label(scrollable_frame,
                                     text="📊 PRODUCTIVITY DASHBOARD",
                                     bg="#1e1e2e",
                                     fg="#f9e2af",
                                     font=("Segoe UI", 11, "bold"))
        dashboard_section.pack(pady=(15, 8), anchor="w", padx=8)

        dashboard_actions = [
            ("📊 View Complete Dashboard", lambda: self.view_productivity_dashboard()),
            ("📅 Weekly Summary", lambda: self.view_weekly_summary()),
            ("📈 Productivity Trends", lambda: self.view_productivity_trends()),
            ("🎯 Get Recommendations", lambda: self.get_productivity_recommendations()),
        ]

        for text, command in dashboard_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def create_tools_utilities_tab(self, notebook):
        """Create tools & utilities tab with password vault, notes, calendar, etc."""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🛠️ Tools & Utilities")

        canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Password Vault Section
        password_section = tk.Label(scrollable_frame,
                                    text="🔐 PASSWORD VAULT",
                                    bg="#1e1e2e",
                                    fg="#f9e2af",
                                    font=("Segoe UI", 11, "bold"))
        password_section.pack(pady=(10, 8), anchor="w", padx=8)

        password_actions = [
            ("➕ Add Password", lambda: self.add_password_dialog()),
            ("🔍 View Password", lambda: self.view_password_dialog()),
            ("📋 List All Passwords", lambda: self.list_passwords()),
            ("🔑 Generate Secure Password", lambda: self.generate_password()),
        ]

        for text, command in password_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Quick Notes Section
        notes_section = tk.Label(scrollable_frame,
                                 text="📝 QUICK NOTES",
                                 bg="#1e1e2e",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 11, "bold"))
        notes_section.pack(pady=(15, 8), anchor="w", padx=8)

        notes_actions = [
            ("➕ New Note", lambda: self.add_note_dialog()),
            ("📋 View All Notes", lambda: self.list_notes()),
            ("🔍 Search Notes", lambda: self.search_notes_dialog()),
            ("📌 Pinned Notes", lambda: self.view_pinned_notes()),
        ]

        for text, command in notes_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Calendar Section
        calendar_section = tk.Label(scrollable_frame,
                                    text="📅 CALENDAR MANAGER",
                                    bg="#1e1e2e",
                                    fg="#f9e2af",
                                    font=("Segoe UI", 11, "bold"))
        calendar_section.pack(pady=(15, 8), anchor="w", padx=8)

        calendar_actions = [
            ("➕ Add Event", lambda: self.add_event_dialog()),
            ("📅 Today's Events", lambda: self.view_today_events()),
            ("📆 This Week", lambda: self.view_week_events()),
            ("🔔 Upcoming Reminders", lambda: self.view_reminders()),
        ]

        for text, command in calendar_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Weather & News Section
        weather_section = tk.Label(scrollable_frame,
                                   text="🌤️ WEATHER & NEWS",
                                   bg="#1e1e2e",
                                   fg="#f9e2af",
                                   font=("Segoe UI", 11, "bold"))
        weather_section.pack(pady=(15, 8), anchor="w", padx=8)

        weather_actions = [
            ("🌤️ Get Weather", lambda: self.get_weather_dialog()),
            ("📅 3-Day Forecast", lambda: self.get_forecast()),
            ("📰 Latest News Headlines", lambda: self.get_news()),
            ("💼 Tech News", lambda: self.get_tech_news()),
        ]

        for text, command in weather_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

        # Translation Section
        translation_section = tk.Label(scrollable_frame,
                                       text="🌐 TRANSLATION SERVICE",
                                       bg="#1e1e2e",
                                       fg="#f9e2af",
                                       font=("Segoe UI", 11, "bold"))
        translation_section.pack(pady=(15, 8), anchor="w", padx=8)

        translation_actions = [
            ("🌐 Translate Text", lambda: self.translate_text_dialog()),
            ("🔍 Detect Language", lambda: self.detect_language_dialog()),
            ("📚 Supported Languages", lambda: self.show_supported_languages()),
        ]

        for text, command in translation_actions:
            btn = tk.Button(scrollable_frame,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10,
                            activebackground="#45475a")
            btn.pack(fill="x", padx=8, pady=3)
            self.add_hover_effect(btn, "#313244", "#45475a")

    def toggle_vatsal_mode(self):
        """Toggle VATSAL personality mode"""
        self.vatsal_mode = not self.vatsal_mode
        if self.vatsal_mode:
            self.vatsal_toggle_btn.config(text="🤖 VATSAL Mode: ON", bg="#89b4fa")
            self.update_output("\n" + "=" * 60 + "\n", "info")
            self.update_output("🤖 VATSAL Mode Activated\n", "success")
            self.update_output(self.vatsal.get_status_update('ready') + "\n", "info")
            self.update_output("=" * 60 + "\n\n", "info")
        else:
            self.vatsal_toggle_btn.config(text="🤖 VATSAL Mode: OFF", bg="#45475a")
            self.update_output("\n" + "=" * 60 + "\n", "info")
            self.update_output("Standard Mode Activated\n", "warning")
            self.update_output("=" * 60 + "\n\n", "info")

    def toggle_self_operating_mode(self):
        """Toggle Self-Operating Computer feature on/off"""
        self.self_operating_mode = not self.self_operating_mode
        if self.self_operating_mode:
            self.self_operating_toggle_btn.config(text="🎮 Self-Operating: ON", bg="#cba6f7")
            self.update_output("\n" + "=" * 60 + "\n", "info")
            self.update_output("🎮 Self-Operating Computer Mode: ENABLED\n", "success")
            self.update_output("AI can now autonomously control your computer based on prompts.\n", "info")
            self.update_output("Use the 🎮 Self-Operating tab to give objectives.\n", "info")
            self.update_output("=" * 60 + "\n\n", "info")
        else:
            self.self_operating_toggle_btn.config(text="🎮 Self-Operating: OFF", bg="#45475a")
            self.update_output("\n" + "=" * 60 + "\n", "info")
            self.update_output("🎮 Self-Operating Computer Mode: DISABLED\n", "warning")
            self.update_output("Self-operating features are now turned off.\n", "info")
            self.update_output("=" * 60 + "\n\n", "info")

    def open_user_settings(self):
        """Open user profile settings dialog"""
        try:
            open_user_settings(self.root)
        except Exception as e:
            self.update_output(f"❌ Error opening user settings: {e}\n", "error")

    def show_vatsal_greeting(self):
        """Show VATSAL greeting message"""
        # Use personalized greeting from user profile
        personalized_greeting = self.user_profile.get_greeting()
        greeting = self.vatsal.get_greeting()

        self.update_output("\n" + "=" * 60 + "\n", "info")
        self.update_output("🤖 VATSAL AI Assistant\n", "success")
        self.update_output("=" * 60 + "\n", "info")
        self.update_output(f"{personalized_greeting}\n", "success")
        self.update_output(f"{greeting}\n\n", "info")

        # Show proactive suggestion
        suggestion = self.vatsal.get_proactive_suggestion()
        self.update_output(f"{suggestion}\n\n", "command")

        # Record interaction
        self.user_profile.record_interaction()

    def get_vatsal_response(self, user_input, command_result=None):
        """Get VATSAL personality response"""
        if self.vatsal_mode and self.vatsal.ai_available:
            return self.vatsal.process_with_personality(user_input, command_result)
        return command_result

    def start_vatsal_ai_conversation(self):
        """Start conversation with Simple Chat"""
        if self.simple_chatbot:
            greeting = self.simple_chatbot.greeting()
        else:
            greeting = "Hello! I'm VATSAL, your AI assistant. How can I help you today?"

        self._add_vatsal_ai_message("VATSAL", greeting)
        self.vatsal_conversation_active = True

    def send_to_vatsal_ai(self):
        """Send message to VATSAL"""
        user_message = self.vatsal_input.get().strip()
        if not user_message:
            return

        self.vatsal_input.delete(0, tk.END)
        self._add_vatsal_ai_message("YOU", user_message)

        thread = threading.Thread(target=self._process_vatsal_ai_message, args=(user_message,))
        thread.start()

    def _process_vatsal_ai_message(self, user_message):
        """Process message with Simple Chat in background"""
        try:
            if self.simple_chatbot:
                response = self.simple_chatbot.chat(user_message)
            else:
                response = "Chatbot not available. Please check your Gemini API key configuration."

            self._add_vatsal_ai_message("VATSAL", response)
        except Exception as e:
            self._add_vatsal_ai_message("VATSAL", f"Sorry, I encountered an error: {str(e)}")

    def _add_vatsal_ai_message(self, sender, message):
        """Add message to VATSAL conversation display"""
        self.vatsal_conversation_display.config(state='normal')

        timestamp = datetime.now().strftime("%I:%M:%S %p")

        if sender == "VATSAL":
            self.vatsal_conversation_display.insert(tk.END, f"\n🤖 VATSAL", "vatsal")
            self.vatsal_conversation_display.insert(tk.END, f" ({timestamp})\n", "timestamp")
            self.vatsal_conversation_display.insert(tk.END, f"{message}\n", "")
        else:
            self.vatsal_conversation_display.insert(tk.END, f"\n👤 {sender}", "user")
            self.vatsal_conversation_display.insert(tk.END, f" ({timestamp})\n", "timestamp")
            self.vatsal_conversation_display.insert(tk.END, f"{message}\n", "")

        self.vatsal_conversation_display.config(state='disabled')
        self.vatsal_conversation_display.see(tk.END)

    def vatsal_ai_get_suggestion(self):
        """Get a friendly prompt from VATSAL"""
        suggestions = [
            "💡 Try asking me: 'What's the weather like in programming?'",
            "💡 I can help with: General questions, coding, math, science, and more!",
            "💡 Ask me anything! From 'How do loops work?' to 'Tell me a joke'",
            "💡 Need help? Try: 'Explain Python functions' or 'What's 5+5?'",
            "💡 I'm here to chat! Ask me about any topic you're curious about."
        ]
        import random
        self._add_vatsal_ai_message("VATSAL", random.choice(suggestions))

    def clear_vatsal_ai_conversation(self):
        """Clear conversation history"""
        if self.simple_chatbot:
            self.simple_chatbot.reset()

        self.vatsal_conversation_display.config(state='normal')
        self.vatsal_conversation_display.delete(1.0, tk.END)
        self.vatsal_conversation_display.config(state='disabled')
        self.vatsal_conversation_active = False
        messagebox.showinfo("Cleared", "Chat cleared! Ready for a fresh conversation.")

    def show_vatsal_ai_stats(self):
        """Show chatbot statistics"""
        if self.simple_chatbot:
            conv_count = len(self.simple_chatbot.conversation_history)
            stats_message = f"""
📊 VATSAL Simple Chatbot Statistics

💬 Current Conversation: {conv_count // 2} exchanges
🤖 Model: Gemini 2.5 Flash (Latest)
🧠 Memory: Remembers last 10 exchanges
✅ Status: Active and ready to chat!
🎯 Purpose: Quick questions & friendly conversations
"""
            title = "VATSAL Stats"
        else:
            stats_message = "Chatbot not available. Please check configuration."
            title = "Stats"

        messagebox.showinfo(title, stats_message)

    def execute_vatsal_automator_command(self):
        """Execute command using VATSAL automator"""
        if not self.vatsal_automator:
            self._update_vatsal_automator_output("❌ VATSAL Automator not available. Check Gemini API key.\n", "error")
            return

        command = self.vatsal_automator_input.get().strip()
        if not command:
            return

        self.vatsal_automator_input.delete(0, tk.END)
        self._update_vatsal_automator_output(f"\n🎯 Command: {command}\n", "info")

        thread = threading.Thread(target=self._process_vatsal_automator_command, args=(command,))
        thread.start()

    def _vatsal_confirmation_callback(self, intent, risk_level):
        """Confirmation callback for destructive VATSAL actions"""
        result = messagebox.askyesno(
            "⚠️ Confirmation Required",
            f"Risk Level: {risk_level.upper()}\n\nAction: {intent}\n\nDo you want to proceed?",
            icon='warning'
        )
        return result

    def _process_vatsal_automator_command(self, command):
        """Process VATSAL automator command in background"""
        try:
            self._update_vatsal_automator_output("🤔 Understanding command...\n", "info")
            result = self.vatsal_automator.execute_command(command,
                                                           confirmation_callback=self._vatsal_confirmation_callback)

            if "✓" in result:
                self._update_vatsal_automator_output(f"\n{result}\n", "success")
            elif "✗" in result or "❌" in result:
                self._update_vatsal_automator_output(f"\n{result}\n", "error")
            elif "⚠️" in result:
                self._update_vatsal_automator_output(f"\n{result}\n", "warning")
            else:
                self._update_vatsal_automator_output(f"\n{result}\n", "info")

        except Exception as e:
            self._update_vatsal_automator_output(f"\n❌ Error: {str(e)}\n", "error")

    def _update_vatsal_automator_output(self, message, tag=""):
        """Update VATSAL automator output display"""
        self.vatsal_automator_output.config(state='normal')
        self.vatsal_automator_output.insert(tk.END, message, tag)
        self.vatsal_automator_output.config(state='disabled')
        self.vatsal_automator_output.see(tk.END)

    def vatsal_quick_action(self, command):
        """Execute quick action or clear output"""
        if command is None:
            self.vatsal_automator_output.config(state='normal')
            self.vatsal_automator_output.delete(1.0, tk.END)
            self.vatsal_automator_output.config(state='disabled')
            return

        self.vatsal_automator_input.delete(0, tk.END)
        self.vatsal_automator_input.insert(0, command)
        self.execute_vatsal_automator_command()

    def start_self_operating_text(self):
        """Start self-operating computer with text objective"""
        if not self.self_operating_mode:
            messagebox.showwarning(
                "Feature Disabled",
                "🎮 Self-Operating Computer mode is currently DISABLED.\n\n"
                "Please enable it using the '🎮 Self-Operating: OFF' toggle button in the header to use this feature."
            )
            self._update_soc_output("⚠️ Self-Operating mode is disabled. Enable it from the header toggle.\n",
                                    "warning")
            return

        if not self.self_operating_computer:
            self._update_soc_output("❌ Self-Operating Computer not available. Check Gemini API key.\n", "error")
            return

        if self.soc_running:
            messagebox.showwarning("Already Running", "Self-operating mode is already active!")
            return

        objective = self.soc_objective.get("1.0", tk.END).strip()
        if not objective:
            messagebox.showwarning("No Objective", "Please enter an objective first!")
            return

        self.soc_running = True
        self.soc_status_label.config(text=f"Status: Running...", fg="#f9e2af")
        self._update_soc_output(f"\n🎯 Starting self-operating mode...\n", "success")
        self._update_soc_output(f"📋 Objective: {objective}\n\n", "progress")

        self.soc_thread = threading.Thread(target=self._run_self_operating, args=(objective,), daemon=True)
        self.soc_thread.start()

        # Auto-minimize window so user can see AI working on desktop
        self.root.after(500, self.root.iconify)

    def start_self_operating_voice(self):
        """Start self-operating computer with voice objective"""
        if not self.self_operating_mode:
            messagebox.showwarning(
                "Feature Disabled",
                "🎮 Self-Operating Computer mode is currently DISABLED.\n\n"
                "Please enable it using the '🎮 Self-Operating: OFF' toggle button in the header to use this feature."
            )
            self._update_soc_output("⚠️ Self-Operating mode is disabled. Enable it from the header toggle.\n",
                                    "warning")
            return

        if not self.self_operating_computer:
            self._update_soc_output("❌ Self-Operating Computer not available. Check Gemini API key.\n", "error")
            return

        if self.soc_running:
            messagebox.showwarning("Already Running", "Self-operating mode is already active!")
            return

        self.soc_running = True
        self.soc_status_label.config(text="Status: Listening...", fg="#89b4fa")
        self._update_soc_output("\n🎤 Voice input mode activated...\n", "success")
        self._update_soc_output("Please state your objective clearly.\n\n", "progress")

        self.soc_thread = threading.Thread(target=self._run_self_operating_voice, daemon=True)
        self.soc_thread.start()

        # Auto-minimize window so user can see AI working on desktop
        self.root.after(500, self.root.iconify)

    def stop_self_operating(self):
        """Stop the self-operating computer"""
        if not self.soc_running:
            messagebox.showinfo("Not Running", "Self-operating mode is not currently active.")
            return

        self.soc_running = False
        self.soc_status_label.config(text="Status: Stopped", fg="#f38ba8")
        self._update_soc_output("\n🛑 Self-operating mode stopped by user.\n", "warning")

    def _run_self_operating(self, objective):
        """Run self-operating computer in background"""
        try:
            import sys
            from io import StringIO

            old_stdout = sys.stdout
            sys.stdout = StringIO()

            class GUILogger:
                def __init__(self, gui):
                    self.gui = gui

                def log(self, message, level="INFO"):
                    if "🔍" in message or "Analyzing" in message:
                        tag = "iteration"
                    elif "💭" in message or "Thought:" in message:
                        tag = "thought"
                    elif "⚡" in message or "Action:" in message:
                        tag = "action"
                    elif "📊" in message or "Progress:" in message:
                        tag = "progress"
                    elif "✅" in message or "COMPLETE" in message:
                        tag = "success"
                    elif "❌" in message or "ERROR" in level:
                        tag = "error"
                    elif "⚠️" in message or "WARN" in level:
                        tag = "warning"
                    else:
                        tag = ""

                    self.gui._update_soc_output(message + "\n", tag)

            logger = GUILogger(self)
            self.self_operating_computer._log = lambda msg, level="INFO": logger.log(msg, level)

            result = self.self_operating_computer.operate(objective)

            sys.stdout = old_stdout

            if result.get("completed"):
                self._update_soc_output(f"\n✅ Objective completed in {result['duration_seconds']}s!\n", "success")
                self._update_soc_output(f"📊 Total iterations: {result['iterations']}\n", "progress")
                self.soc_status_label.config(text="Status: Completed ✅", fg="#a6e3a1")
            else:
                self._update_soc_output(f"\n⏸️ Session ended (max iterations reached)\n", "warning")
                self._update_soc_output(f"📊 Total iterations: {result['iterations']}\n", "progress")
                self.soc_status_label.config(text="Status: Incomplete", fg="#f9e2af")

            self.soc_running = False

        except Exception as e:
            self._update_soc_output(f"\n❌ Error: {str(e)}\n", "error")
            self.soc_status_label.config(text="Status: Error", fg="#f38ba8")
            self.soc_running = False

    def _run_self_operating_voice(self):
        """Run self-operating computer with voice input"""
        try:
            result = self.self_operating_computer.operate_with_voice()

            if not result:
                self._update_soc_output("❌ Voice input failed. Please try again.\n", "error")
                self.soc_status_label.config(text="Status: Ready", fg="#a6e3a1")
                self.soc_running = False
                return

            if result.get("completed"):
                self._update_soc_output(f"\n✅ Objective completed!\n", "success")
                self.soc_status_label.config(text="Status: Completed ✅", fg="#a6e3a1")
            else:
                self._update_soc_output(f"\n⏸️ Session ended\n", "warning")
                self.soc_status_label.config(text="Status: Incomplete", fg="#f9e2af")

            self.soc_running = False

        except Exception as e:
            self._update_soc_output(f"\n❌ Error: {str(e)}\n", "error")
            self.soc_status_label.config(text="Status: Error", fg="#f38ba8")
            self.soc_running = False

    def _update_soc_output(self, message, tag=""):
        """Update self-operating computer output display"""
        self.soc_output.config(state='normal')
        self.soc_output.insert(tk.END, message, tag)
        self.soc_output.config(state='disabled')
        self.soc_output.see(tk.END)

    def clear_soc_output(self):
        """Clear self-operating computer output"""
        self.soc_output.config(state='normal')
        self.soc_output.delete(1.0, tk.END)
        self.soc_output.config(state='disabled')
        messagebox.showinfo("Cleared", "Output cleared!")

    def show_soc_guide(self):
        """Show self-operating computer guide"""
        guide = """
🎮 SELF-OPERATING COMPUTER GUIDE

Powered by Gemini Vision, this feature lets AI autonomously control
your computer to accomplish objectives.

HOW IT WORKS:
1. AI views your screen (takes screenshots)
2. Analyzes what it sees using Gemini Vision
3. Decides the next mouse/keyboard action
4. Executes the action
5. Repeats until objective is complete

INPUT MODES:
▶️ Text Mode: Type your objective and click Start
🎤 Voice Mode: Speak your objective when prompted

EXAMPLE OBJECTIVES:
• Open Google Chrome and search for Python tutorials
• Go to YouTube and play a video about AI
• Open Calculator and calculate 25 × 47
• Create a new folder on Desktop named 'AI Projects'
• Open Notepad and write 'Hello World'

TIPS:
✓ Be specific and clear with objectives
✓ Simple tasks work best (1-3 steps)
✓ AI can see and interact with visible UI elements
✓ Click Stop if you need to interrupt
✓ Check screenshots/ folder to see what AI saw

SAFETY:
⚠️ AI will not perform destructive actions without context
⚠️ Move mouse to corner to trigger failsafe (PyAutoGUI)
⚠️ Maximum 30 iterations per session

Based on OthersideAI's self-operating-computer framework
"""
        messagebox.showinfo("Self-Operating Computer Guide", guide)

    def view_soc_screenshots(self):
        """Open screenshots folder"""
        import subprocess
        import platform

        screenshots_dir = Path("screenshots")
        if not screenshots_dir.exists():
            messagebox.showinfo("No Screenshots", "No screenshots have been taken yet.")
            return

        try:
            if platform.system() == "Windows":
                os.startfile(screenshots_dir)
            elif platform.system() == "Darwin":
                subprocess.run(["open", screenshots_dir])
            else:
                subprocess.run(["xdg-open", screenshots_dir])

            self._update_soc_output("📸 Opened screenshots folder\n", "success")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")

    def auto_start_if_enabled(self):
        """Auto-start self-operating mode if enabled"""
        if self.auto_control_enabled:
            self._update_soc_output("\n🚀 Auto-starting self-operating mode...\n", "success")
            self.start_self_operating_text()
        else:
            messagebox.showinfo(
                "Auto Mode Disabled",
                "Auto Self-Control Mode is currently disabled.\n\n"
                "Enable it using the toggle button to use Ctrl+Enter quick-start."
            )

    def toggle_auto_control(self):
        """Toggle auto self-control mode on/off"""
        self.auto_control_enabled = not self.auto_control_enabled

        if self.auto_control_enabled:
            self.auto_control_btn.config(
                text="✅ Enabled",
                fg="#a6e3a1",
                bg="#45475a"
            )
            self._update_soc_output("\n🔄 Auto Self-Control Mode: ENABLED\n", "success")
            self._update_soc_output("AI will automatically start self-operating mode after commands.\n", "progress")
            messagebox.showinfo(
                "Auto Mode Enabled",
                "✅ Auto Self-Control Mode is now ENABLED!\n\n"
                "When you give a command, AI will automatically:\n"
                "1. Understand the command\n"
                "2. Enter self-operating mode\n"
                "3. View the screen and perform actions\n"
                "4. Complete the objective autonomously\n\n"
                "You can toggle this off anytime."
            )
        else:
            self.auto_control_btn.config(
                text="❌ Disabled",
                fg="#f38ba8",
                bg="#313244"
            )
            self._update_soc_output("\n🔄 Auto Self-Control Mode: DISABLED\n", "warning")
            self._update_soc_output("Manual control restored. Use Start buttons to begin.\n", "progress")
            messagebox.showinfo(
                "Auto Mode Disabled",
                "❌ Auto Self-Control Mode is now DISABLED.\n\n"
                "Use the Start buttons to manually begin self-operating mode."
            )

    def execute_web_automation(self):
        """Execute web automation from input"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        command = self.web_auto_input.get().strip()
        if not command:
            self.update_output("⚠️  Please enter a command\n", "warning")
            return

        self.update_output(f"\n🤖 EXECUTING WEB AUTOMATION\n", "info")
        self.update_output(f"📋 Command: {command}\n", "info")

        def run_automation():
            try:
                result = self.web_automator.execute_task(command, interactive=False)

                if result.get('success'):
                    self.update_output(f"\n✅ Task completed successfully!\n", "success")
                    self.update_output(f"📊 Success rate: {result['successful_steps']}/{result['total_steps']}\n",
                                       "info")
                else:
                    self.update_output(f"\n⚠️  Task completed with issues\n", "warning")

                for i, step_result in enumerate(result.get('results', []), 1):
                    if step_result.get('success'):
                        self.update_output(f"   Step {i}: ✅ {step_result.get('message', 'Done')}\n", "success")
                    else:
                        self.update_output(f"   Step {i}: ❌ {step_result.get('error', 'Failed')}\n", "error")

                self.web_auto_input.delete(0, tk.END)

            except Exception as e:
                self.update_output(f"❌ Error: {str(e)}\n", "error")

        thread = threading.Thread(target=run_automation, daemon=True)
        thread.start()

    def quick_web_automation(self, command):
        """Quick web automation action"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        self.web_auto_input.delete(0, tk.END)
        self.web_auto_input.insert(0, command)
        self.execute_web_automation()

    def initialize_web_browser(self):
        """Initialize the web browser"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        self.update_output("🌐 Initializing browser...\n", "info")

        def init():
            try:
                if self.web_automator.initialize_browser():
                    self.update_output("✅ Browser initialized successfully!\n", "success")
                    self.update_output(f"📍 Ready for automation commands\n", "info")
                else:
                    self.update_output("❌ Failed to initialize browser\n", "error")
            except Exception as e:
                self.update_output(f"❌ Error: {str(e)}\n", "error")

        thread = threading.Thread(target=init, daemon=True)
        thread.start()

    def close_web_browser(self):
        """Close the web browser"""
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        try:
            self.web_automator.close_browser()
            self.update_output("🔒 Browser closed\n", "info")
        except Exception as e:
            self.update_output(f"❌ Error closing browser: {str(e)}\n", "error")

    def take_web_screenshot(self):
        """Take a screenshot of the current page"""
        import time
        if not self.web_automator:
            self.update_output("❌ Web automation not available\n", "error")
            return

        try:
            filename = f"web_screenshot_{int(time.time())}.png"
            if self.web_automator.take_screenshot(filename):
                self.update_output(f"📸 Screenshot saved: {filename}\n", "success")
                self.update_output(f"📍 URL: {self.web_automator.get_current_url()}\n", "info")
            else:
                self.update_output("❌ Screenshot failed - browser not initialized\n", "error")
        except Exception as e:
            self.update_output(f"❌ Error: {str(e)}\n", "error")

    def select_command_text(self):
        """Select all text in command input for easy editing"""
        self.command_input.select_range(0, tk.END)
        self.command_input.icursor(tk.END)

    def check_api_key(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.update_output("⚠️ WARNING: GEMINI_API_KEY not found in environment variables.\n", "warning")
            self.update_output("Please set your Gemini API key to use AI features.\n\n", "info")
            self.update_status("⚠️ API Key Missing", "#f9e2af")
        else:
            self.update_output("✅ Gemini AI is ready!\n", "success")
            self.update_output("Type a command or click a Quick Action button to get started.\n\n", "info")

    def quick_command(self, command):
        self.command_input.delete(0, tk.END)
        self.command_input.insert(0, command)
        self.execute_command()

    def direct_lock_screen(self):
        """Directly lock the screen without going through AI parsing"""
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        self.processing = True
        self.update_status("🔒 Locking...", "#f9e2af")

        def lock_thread():
            try:
                self.update_output(f"\n{'=' * 60}\n", "info")
                self.update_output("🔒 Locking the computer...\n", "info")
                result = self.system_controller.lock_screen()
                self.update_output(f"{result}\n", "success")
                self.update_status("✅ Ready", "#a6e3a1")
            except Exception as e:
                self.update_output(f"❌ Error locking screen: {str(e)}\n", "error")
                self.update_status("❌ Error", "#f38ba8")
            finally:
                self.processing = False

        threading.Thread(target=lock_thread, daemon=True).start()

    def direct_shutdown_system(self):
        """Directly shutdown the system without going through AI parsing"""
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        # Confirm shutdown action
        confirm = messagebox.askyesno(
            "Confirm Shutdown",
            "Are you sure you want to shutdown the computer?\n\nThe system will shutdown in 10 seconds."
        )

        if not confirm:
            return

        self.processing = True
        self.update_status("⚠️ Shutting down...", "#f38ba8")

        def shutdown_thread():
            try:
                self.update_output(f"\n{'=' * 60}\n", "info")
                self.update_output("⚠️ Initiating shutdown...\n", "warning")
                result = self.system_controller.shutdown_system(delay_seconds=10)
                self.update_output(f"{result}\n", "warning")
                self.update_status("⚠️ Shutting down", "#f38ba8")
            except Exception as e:
                self.update_output(f"❌ Error during shutdown: {str(e)}\n", "error")
                self.update_status("❌ Error", "#f38ba8")
            finally:
                self.processing = False

        threading.Thread(target=shutdown_thread, daemon=True).start()

    def execute_command(self):
        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        command = self.command_input.get().strip()
        if not command:
            messagebox.showwarning("Empty Command", "Please enter a command.")
            return

        # Clear the input box immediately
        self.command_input.delete(0, tk.END)

        self.processing = True
        self.update_status("⚙️ Running...", "#f9e2af")
        self.execute_btn.config(state="disabled", text="⏳ Running...")

        thread = threading.Thread(target=self._execute_in_thread, args=(command,))
        thread.start()

    def _execute_in_thread(self, command):
        try:
            # Broadcast command started
            if self.ws_client and self.ws_client.connected:
                self.ws_client.emit('command_started', {
                    'command': command,
                    'timestamp': datetime.now().isoformat()
                })

            self.update_output(f"\n{'=' * 60}\n", "info")
            self.update_output(f"📝 You: {command}\n", "command")
            self.update_output(f"{'=' * 60}\n\n", "info")

            # VATSAL acknowledgment
            if self.vatsal_mode:
                ack = self.vatsal.acknowledge_command(command)
                self.update_output(f"🤖 VATSAL: {ack}\n\n", "info")

            command_dict = parse_command(command)

            if command_dict.get("action") == "error":
                error_msg = command_dict.get('description', 'Error processing command')

                if self.vatsal_mode:
                    vatsal_response = self.vatsal.process_with_personality(
                        command,
                        f"Error: {error_msg}"
                    )
                    self.update_output(f"🤖 VATSAL: {vatsal_response}\n", "error")

                    # Speak error response if voice is enabled
                    if self.voice_commander and self.voice_enabled:
                        self.voice_commander.speak(vatsal_response)
                else:
                    self.update_output(f"❌ {error_msg}\n", "error")
                    suggestion = get_ai_suggestion(f"User tried: {command}, but got error. Suggest alternatives.")
                    self.update_output(f"\n💡 Suggestion: {suggestion}\n", "info")

                self.update_status("❌ Error", "#f38ba8")
                return

            result = self.executor.execute(command_dict)

            if result["success"]:
                # Broadcast command completed
                if self.ws_client and self.ws_client.connected:
                    self.ws_client.emit('command_completed', {
                        'command': command,
                        'result': str(result['message']),
                        'timestamp': datetime.now().isoformat()
                    })

                # Get VATSAL response if mode is enabled
                if self.vatsal_mode:
                    vatsal_response = self.get_vatsal_response(command, result['message'])
                    self.update_output(f"🤖 VATSAL:\n{vatsal_response}\n\n", "success")

                    # Speak VATSAL's response if voice is enabled
                    if self.voice_commander and self.voice_enabled:
                        self.voice_commander.speak(vatsal_response)

                    # Show technical result in smaller text
                    self.update_output(f"📊 Technical Details:\n{result['message']}\n", "info")
                else:
                    self.update_output(f"✅ Result:\n{result['message']}\n", "success")

                self.update_status("✅ Ready", "#a6e3a1")

                # Occasionally show proactive suggestions
                import random
                if random.random() < 0.3 and self.vatsal_mode:  # 30% chance
                    suggestion = self.vatsal.get_proactive_suggestion()
                    self.update_output(f"\n{suggestion}\n", "command")

            else:
                # Broadcast command failed
                if self.ws_client and self.ws_client.connected:
                    self.ws_client.emit('command_failed', {
                        'command': command,
                        'error': str(result['message']),
                        'timestamp': datetime.now().isoformat()
                    })

                if self.vatsal_mode:
                    vatsal_response = self.vatsal.process_with_personality(
                        command,
                        f"Error: {result['message']}"
                    )
                    self.update_output(f"🤖 VATSAL: {vatsal_response}\n", "error")

                    # Speak error response if voice is enabled
                    if self.voice_commander and self.voice_enabled:
                        self.voice_commander.speak(vatsal_response)
                else:
                    self.update_output(f"❌ Error:\n{result['message']}\n", "error")

                self.update_status("❌ Error", "#f38ba8")

        except Exception as e:
            # Broadcast exception
            if self.ws_client and self.ws_client.connected:
                self.ws_client.emit('command_failed', {
                    'command': command,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })

            if self.vatsal_mode:
                self.update_output(f"🤖 VATSAL: Apologies, Sir. Encountered an unexpected error: {str(e)}\n", "error")
            else:
                self.update_output(f"❌ Error: {str(e)}\n", "error")
            self.update_status("❌ Error", "#f38ba8")

        finally:
            self.processing = False
            self.root.after(0, lambda: self.execute_btn.config(state="normal", text="▶ Execute"))

    def update_output(self, message, msg_type="info"):
        def _update():
            self.output_area.config(state="normal")

            colors = {
                "info": "#a6adc8",
                "success": "#a6e3a1",
                "error": "#f38ba8",
                "warning": "#f9e2af",
                "command": "#89b4fa"
            }

            tag_name = msg_type
            if tag_name not in self.output_area.tag_names():
                self.output_area.tag_configure(tag_name, foreground=colors.get(msg_type, "#ffffff"))

            self.output_area.insert(tk.END, message, tag_name)
            self.output_area.see(tk.END)
            self.output_area.config(state="disabled")

        self.root.after(0, _update)

    def update_status(self, text, color):
        def _update():
            self.status_label.config(text=text, fg=color)

        self.root.after(0, _update)

    def clear_output(self):
        self.output_area.config(state="normal")
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state="disabled")
        self.update_output("✨ Console cleared!\n\n", "success")

    def start_voice_listen(self):
        """Start push-to-talk voice command"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        if self.processing:
            messagebox.showwarning("Busy", "Please wait for the current command to finish.")
            return

        def voice_thread():
            self.update_output("\n🎤 Listening for voice command...\n", "info")
            self.update_status("🎤 Listening...", "#f9e2af")
            self.root.after(0, lambda: self.voice_listen_btn.config(bg="#f38ba8"))

            result = self.voice_commander.listen_once(timeout=10)

            self.root.after(0, lambda: self.voice_listen_btn.config(bg="#a6e3a1"))

            if result['success'] and result['command']:
                self.update_output(f"✅ Heard: {result['command']}\n\n", "success")

                # Execute the command
                self.command_input.delete(0, tk.END)
                self.command_input.insert(0, result['command'])
                self.execute_command()

            else:
                self.update_output(f"❌ {result['message']}\n", "error")
                self.update_status("✅ Ready", "#a6e3a1")

        thread = threading.Thread(target=voice_thread, daemon=True)
        thread.start()

    def toggle_continuous_listening(self):
        """Toggle continuous voice listening mode"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        if not self.voice_listening:
            # Start continuous listening (callback already set during init)
            result = self.voice_commander.start_continuous_listening()

            if result['success']:
                self.voice_listening = True
                self.voice_continuous_btn.config(bg="#a6e3a1", text="🔇")

                # Show wake word status
                wake_words = ", ".join(self.voice_commander.get_wake_words()[:3])
                wake_status = ""
                if self.voice_commander.wake_word_enabled:
                    wake_status = f"\n💬 Wake words: {wake_words}\n"

                self.update_output("\n🔊 Continuous voice listening ENABLED\n", "success")
                self.update_output(wake_status, "info")
                self.update_output("Say 'stop listening' to disable\n\n", "info")
                self.update_status("🎤 Voice Active", "#a6e3a1")
            else:
                messagebox.showerror("Voice Error", result['message'])
        else:
            # Stop continuous listening
            result = self.voice_commander.stop_continuous_listening()

            if result['success']:
                self.voice_listening = False
                self.voice_continuous_btn.config(bg="#45475a", text="🔊")
                self.update_output("\n🔇 Continuous voice listening DISABLED\n", "warning")
                self.update_status("✅ Ready", "#a6e3a1")

    def toggle_wake_word(self):
        """Toggle wake word detection on/off"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        result = self.voice_commander.toggle_wake_word()

        if result['success']:
            if result['enabled']:
                self.wake_word_btn.config(bg="#a6e3a1")
                wake_words = ", ".join(self.voice_commander.get_wake_words()[:3])
                self.update_output(f"\n💬 Wake word ENABLED\n", "success")
                self.update_output(f"Say: {wake_words}\n", "info")
                self.update_output(f"Then your command (e.g., 'Hey VATSAL, what time is it')\n\n", "info")
            else:
                self.wake_word_btn.config(bg="#f9e2af")
                self.update_output(f"\n💬 Wake word DISABLED\n", "warning")
                self.update_output(f"Continuous listening will respond to all speech\n\n", "info")

    def handle_voice_command(self, command):
        """Handle voice command from continuous listening"""
        print(f"📞 Callback received command: '{command}'")
        # Execute on main thread for thread safety
        self.root.after(0, lambda: self._execute_voice_command(command))

    def _execute_voice_command(self, command):
        """Internal method to execute voice command on main thread"""
        print(f"🎯 Executing voice command on main thread: '{command}'")
        self.update_output(f"\n🎤 Voice Command: {command}\n", "info")

        # Insert command and execute
        self.command_input.delete(0, tk.END)
        self.command_input.insert(0, command)

        # Execute the command
        print(f"⚙️  Calling execute_command()...")
        self.execute_command()
        print(f"✅ execute_command() completed")

    def toggle_sound_effects(self):
        """Toggle voice sound effects on/off"""
        if not self.voice_commander:
            messagebox.showerror("Voice Error", "Voice commander not available")
            return

        result = self.voice_commander.toggle_sound_effects()

        if result['success']:
            if result['enabled']:
                self.sound_fx_btn.config(bg="#a6e3a1", text="🔊")
                self.update_output(f"\n🔊 Voice sound effects ENABLED\n", "success")
                self.update_output(f"You'll hear beeps during voice interactions\n", "info")

                # Play success sound to demonstrate
                if self.voice_commander.sound_effects:
                    self.voice_commander.sound_effects.play_sound('success', async_play=True)
            else:
                self.sound_fx_btn.config(bg="#45475a", text="🔇")
                self.update_output(f"\n🔇 Voice sound effects DISABLED\n", "warning")
                self.update_output(f"Voice commands will work silently\n", "info")

    def show_sound_settings(self):
        """Show sound effects settings dialog"""
        if not self.voice_commander or not self.voice_commander.sound_effects:
            messagebox.showerror("Sound Error", "Sound effects not available")
            return

        settings_window = tk.Toplevel(self.root)
        settings_window.title("🔊 Sound Effects Settings")
        settings_window.geometry("500x450")
        settings_window.configure(bg="#1a1a2e")

        header = tk.Label(settings_window,
                          text="🔊 Voice Sound Effects Settings",
                          bg="#1a1a2e",
                          fg="#ffffff",
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        # Sound effects status
        status_frame = tk.Frame(settings_window, bg="#2a2a3e", relief="flat")
        status_frame.pack(fill="x", padx=20, pady=10)

        sounds_list = self.voice_commander.list_sound_effects()
        status_text = "🎵 Available Sound Effects:\n\n"

        if sounds_list['success']:
            for name, info in sounds_list['sounds'].items():
                status = "✅" if info['exists'] else "❌"
                status_text += f"{status} {name.replace('_', ' ').title()}\n"

        status_label = tk.Label(status_frame,
                                text=status_text,
                                bg="#2a2a3e",
                                fg="#ffffff",
                                font=("Segoe UI", 11),
                                justify="left",
                                pady=15,
                                padx=15)
        status_label.pack()

        # Volume control
        volume_frame = tk.Frame(settings_window, bg="#1a1a2e")
        volume_frame.pack(fill="x", padx=20, pady=15)

        volume_label = tk.Label(volume_frame,
                                text="🎚️ Volume:",
                                bg="#1a1a2e",
                                fg="#ffffff",
                                font=("Segoe UI", 12, "bold"))
        volume_label.pack(side="left", padx=10)

        current_volume = self.voice_commander.sound_effects.volume if self.voice_commander.sound_effects else 0.8

        def update_volume(val):
            volume = float(val)
            self.voice_commander.set_sound_volume(volume)
            volume_value.config(text=f"{int(volume * 100)}%")

        volume_slider = tk.Scale(volume_frame,
                                 from_=0.0,
                                 to=1.0,
                                 resolution=0.1,
                                 orient="horizontal",
                                 bg="#313244",
                                 fg="#ffffff",
                                 highlightthickness=0,
                                 command=update_volume,
                                 length=250)
        volume_slider.set(current_volume)
        volume_slider.pack(side="left", padx=10)

        volume_value = tk.Label(volume_frame,
                                text=f"{int(current_volume * 100)}%",
                                bg="#1a1a2e",
                                fg="#a6e3a1",
                                font=("Segoe UI", 11, "bold"))
        volume_value.pack(side="left", padx=10)

        # Test sounds section
        test_frame = tk.Frame(settings_window, bg="#2a2a3e", relief="flat")
        test_frame.pack(fill="x", padx=20, pady=15)

        test_header = tk.Label(test_frame,
                               text="🎵 Test Sounds:",
                               bg="#2a2a3e",
                               fg="#f9e2af",
                               font=("Segoe UI", 12, "bold"),
                               pady=10)
        test_header.pack()

        test_buttons_frame = tk.Frame(test_frame, bg="#2a2a3e")
        test_buttons_frame.pack(pady=10)

        sound_names = ['wake_word', 'listening', 'processing', 'success', 'error']

        def play_test_sound(sound_name):
            self.voice_commander.sound_effects.play_sound(sound_name, async_play=True)

        for sound_name in sound_names:
            btn_text = sound_name.replace('_', ' ').title()
            test_btn = tk.Button(test_buttons_frame,
                                 text=btn_text,
                                 bg="#313244",
                                 fg="#ffffff",
                                 font=("Segoe UI", 9),
                                 relief="flat",
                                 cursor="hand2",
                                 command=lambda s=sound_name: play_test_sound(s),
                                 padx=15,
                                 pady=8)
            test_btn.pack(side="left", padx=5)
            self.add_hover_effect(test_btn, "#313244", "#45475a")

        # Info section
        info_frame = tk.Frame(settings_window, bg="#1a1a2e")
        info_frame.pack(fill="x", padx=20, pady=15)

        info_text = """
💡 Tips:
• Click sound names above to test them
• Adjust volume slider to your preference
• Sound effects play during voice interactions
• Toggle 🔊 button to enable/disable sounds
        """

        info_label = tk.Label(info_frame,
                              text=info_text,
                              bg="#1a1a2e",
                              fg="#a6adc8",
                              font=("Segoe UI", 10),
                              justify="left")
        info_label.pack()

        # Close button
        close_btn = tk.Button(settings_window,
                              text="✅ Done",
                              bg="#89b4fa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=settings_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=15)
        self.add_hover_effect(close_btn, "#89b4fa", "#74c7ec")

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help Guide")
        help_window.geometry("900x700")
        help_window.configure(bg="#1a1a2e")

        header = tk.Label(help_window,
                          text="🤖 AI Desktop Automation Controller - Help Guide",
                          bg="#1a1a2e",
                          fg="#ffffff",
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        text_area = scrolledtext.ScrolledText(help_window,
                                              bg="#2a2a3e",
                                              fg="#ffffff",
                                              font=("Segoe UI", 11),
                                              wrap="word",
                                              padx=20,
                                              pady=20)
        text_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        help_text = """
🎯 QUICK START GUIDE

The AI Desktop Automation Controller is your personal AI-powered assistant for automating tasks on your computer.

📋 HOW TO USE:

1. Click any button in the Quick Actions panel
2. Or type a natural language command in the input field
3. Press Enter or click the Execute button
4. View the results in the Output Console

💡 EXAMPLE COMMANDS:

Desktop Control:
• "Take a screenshot"
• "Open notepad"
• "Search Google for Python tutorials"

Code Generation:
• "Write Python code for bubble sort"
• "Generate a calculator in JavaScript"

Messaging:
• "Send email to example@email.com"
• "Add contact John with phone 555-1234"

System Management:
• "Show system information"
• "Check disk usage"
• "Organize downloads folder"

AI Features:
• "Write a story about robots"
• "Explain quantum physics"
• "Generate a professional email template"

And much more! Explore all tabs for 80+ features.

🔑 REQUIREMENTS:

• Gemini API key (set GEMINI_API_KEY environment variable)
• Various system permissions for automation features

⚡ TIPS:

• Use natural language - the AI understands context
• Check the Output Console for detailed results
• Use Quick Actions for common tasks
• Explore all tabs to discover features

For more information, visit the documentation or contact support.
        """

        text_area.insert(1.0, help_text.strip())
        text_area.config(state="disabled")

        close_btn = tk.Button(help_window,
                              text="Close",
                              bg="#89b4fa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=help_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=(0, 20))

    def show_contacts(self):
        contacts_window = tk.Toplevel(self.root)
        contacts_window.title("👥 Contacts Manager")
        contacts_window.geometry("700x600")
        contacts_window.configure(bg="#1a1a2e")

        header = tk.Label(contacts_window,
                          text="👥 Contact Manager",
                          bg="#1a1a2e",
                          fg="#ffffff",
                          font=("Segoe UI", 16, "bold"),
                          pady=20)
        header.pack()

        info = tk.Label(contacts_window,
                        text="Manage your contacts for email and messaging automation",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 10))
        info.pack()

        text_area = scrolledtext.ScrolledText(contacts_window,
                                              bg="#2a2a3e",
                                              fg="#ffffff",
                                              font=("Segoe UI", 11),
                                              wrap="word",
                                              padx=20,
                                              pady=20)
        text_area.pack(fill="both", expand=True, padx=20, pady=20)

        try:
            command_dict = parse_command("List all contacts")
            result = self.executor.execute(command_dict)
            if result["success"]:
                text_area.insert(1.0, result["message"])
            else:
                text_area.insert(1.0, f"Error: {result['message']}")
        except Exception as e:
            text_area.insert(1.0,
                             f"No contacts found or error loading contacts.\n\nUse the command:\n'Add contact NAME with phone NUMBER and email EMAIL'\n\nError details: {str(e)}")

        text_area.config(state="disabled")

        close_btn = tk.Button(contacts_window,
                              text="Close",
                              bg="#89b4fa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=contacts_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=(0, 20))

    def show_suggestion(self):
        """Show VATSAL proactive suggestion"""
        suggestion = self.vatsal.get_proactive_suggestion()
        self.update_output(f"\n{suggestion}\n\n", "command")

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ About VATSAL")
        about_window.geometry("700x600")
        about_window.configure(bg="#1a1a2e")

        header = tk.Label(about_window,
                          text="🤖 VATSAL AI Assistant",
                          bg="#1a1a2e",
                          fg="#ffffff",
                          font=("Segoe UI", 18, "bold"),
                          pady=20)
        header.pack()

        version = tk.Label(about_window,
                           text="Version 2.0.0 - VATSAL Edition",
                           bg="#1a1a2e",
                           fg="#89b4fa",
                           font=("Segoe UI", 11))
        version.pack()

        description_frame = tk.Frame(about_window, bg="#2a2a3e")
        description_frame.pack(fill="both", expand=True, padx=30, pady=30)

        description = tk.Label(description_frame,
                               text="""
⚡ Virtual Assistant To Serve And Learn

Powered by Google Gemini AI

VATSAL is your intelligent AI assistant with sophisticated 
personality and advanced capabilities.

✓ 80+ AI-powered features
✓ Sophisticated personality & conversational AI
✓ Context-aware responses with memory
✓ Proactive suggestions & assistance
✓ Natural language command processing
✓ Desktop automation & control
✓ Code generation assistance
✓ Email & messaging automation
✓ System management tools
✓ Productivity tracking
✓ Smart scheduling & workflows

VATSAL Mode Features:
• Personalized responses with wit and charm
• Contextual understanding of your commands
• Proactive suggestions based on time and usage
• Conversational memory across sessions
• Professional yet friendly communication

Toggle VATSAL Mode ON/OFF anytime from the header.

© 2025 AI Automation Suite
                              """,
                               bg="#2a2a3e",
                               fg="#ffffff",
                               font=("Segoe UI", 10),
                               justify="center")
        description.pack(expand=True)

        close_btn = tk.Button(about_window,
                              text="Close",
                              bg="#89b4fa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=about_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=(0, 20))

    def show_security_dashboard(self):
        """Display AI-Powered Security Dashboard"""
        if not self.security_dashboard:
            messagebox.showerror("Error", "Security Dashboard not initialized")
            return

        sec_window = tk.Toplevel(self.root)
        sec_window.title("🛡️ AI-Powered Security Dashboard")
        sec_window.geometry("1000x700")
        sec_window.configure(bg="#1a1a2e")

        header_frame = tk.Frame(sec_window, bg="#0f0f1e")
        header_frame.pack(fill="x", pady=(0, 10))

        header = tk.Label(header_frame,
                          text="🛡️ Security Dashboard with Gemini AI",
                          bg="#0f0f1e",
                          fg="#f38ba8",
                          font=("Segoe UI", 18, "bold"),
                          pady=15)
        header.pack()

        subtitle = tk.Label(header_frame,
                            text="🤖 AI-Powered Threat Analysis • 🔐 Enhanced Security Features",
                            bg="#0f0f1e",
                            fg="#a6adc8",
                            font=("Segoe UI", 10, "italic"))
        subtitle.pack()

        # Main content area
        main_frame = tk.Frame(sec_window, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel - Actions
        left_panel = tk.Frame(main_frame, bg="#1e1e2e", width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        actions_label = tk.Label(left_panel,
                                 text="🎯 Security Actions",
                                 bg="#1e1e2e",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 12, "bold"),
                                 pady=10)
        actions_label.pack()

        # Security action buttons
        security_actions = [
            ("📊 Security Status", self.show_security_status),
            ("🤖 AI Threat Analysis", self.show_ai_threat_analysis),
            ("💡 AI Recommendations", self.show_ai_security_recommendations),
            ("🔍 Anomaly Detection", self.show_ai_anomaly_detection),
            ("📄 Full AI Report", self.show_ai_security_report),
            ("❓ Ask Security Question", self.ask_security_question)
        ]

        for text, command in security_actions:
            btn = tk.Button(left_panel,
                            text=text,
                            bg="#313244",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=12)
            btn.pack(fill="x", padx=10, pady=5)

        # Right panel - Display area
        right_panel = tk.Frame(main_frame, bg="#1e1e2e")
        right_panel.pack(side="right", fill="both", expand=True)

        display_label = tk.Label(right_panel,
                                 text="📋 Security Information",
                                 bg="#1e1e2e",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 12, "bold"),
                                 pady=10)
        display_label.pack()

        # Display area
        self.security_display = scrolledtext.ScrolledText(
            right_panel,
            bg="#0f0f1e",
            fg="#cdd6f4",
            font=("Consolas", 10),
            wrap=tk.WORD,
            relief="flat",
            padx=15,
            pady=15
        )
        self.security_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Show initial status
        status = self.security_dashboard.get_comprehensive_security_status()
        status_text = f"""
🛡️ SECURITY DASHBOARD STATUS
{'=' * 60}

Security Level: {status['dashboard_info']['security_level'].upper()}
Current User: {status['dashboard_info']['current_user'] or 'Not Authenticated'}
Authenticated: {status['dashboard_info']['authenticated']}

🔐 BIOMETRIC AUTHENTICATION
  • Enrolled Users: {status['biometric_authentication']['enrolled_users']}
  • Success Rate: {status['biometric_authentication']['success_rate']:.1f}%

🔑 TWO-FACTOR AUTHENTICATION
  • Enabled Users: {status['two_factor_authentication']['enabled_users']}
  • Success Rate: {status['two_factor_authentication']['success_rate']:.1f}%

🔒 ENCRYPTED STORAGE
  • Status: {'ENABLED' if status['encrypted_storage']['enabled'] else 'DISABLED'}
  • Encrypted Files: {status['encrypted_storage']['encrypted_files']}

🛡️ ACTIVITY MONITORING
  • Status: {'ACTIVE' if status['activity_monitoring']['active'] else 'INACTIVE'}
  • Total Activities: {status['activity_monitoring']['total_activities']}
  • Threats Detected: {status['activity_monitoring']['threats_detected']}

⚠️ THREATS (24H)
  • Total: {status['threat_summary_24h']['total_threats']}
  • Critical: {status['threat_summary_24h']['critical']}
  • High: {status['threat_summary_24h']['high']}

Click the buttons on the left to access AI-powered security features.
        """
        self.security_display.insert("1.0", status_text)

        close_btn = tk.Button(sec_window,
                              text="Close",
                              bg="#89b4fa",
                              fg="#0f0f1e",
                              font=("Segoe UI", 11, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=sec_window.destroy,
                              padx=30,
                              pady=10)
        close_btn.pack(pady=20)

    def show_security_status(self):
        """Show current security status"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "Loading security status...\n")
        self.security_display.update()

        status = self.security_dashboard.get_comprehensive_security_status()
        report = self.security_dashboard.generate_security_report()

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", report)

    def show_ai_threat_analysis(self):
        """Show AI-powered threat analysis"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "🤖 Analyzing threats with Gemini AI...\nThis may take a moment...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_analyze_threats()

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
🤖 AI-POWERED THREAT ANALYSIS
{'=' * 60}

Threat Count: {result.get('threat_count', 0)}
Analysis Time: {result.get('timestamp', 'N/A')}

{result['analysis']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def show_ai_security_recommendations(self):
        """Show AI-powered security recommendations"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "🤖 Generating security recommendations with Gemini AI...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_security_recommendations()

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
💡 AI-POWERED SECURITY RECOMMENDATIONS
{'=' * 60}

Current Security Level: {result.get('security_level', 'N/A').upper()}
Analysis Time: {result.get('timestamp', 'N/A')}

{result['recommendations']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def show_ai_anomaly_detection(self):
        """Show AI-powered anomaly detection"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", "🤖 Detecting anomalies with Gemini AI...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_detect_anomalies()

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
🔍 AI-POWERED ANOMALY DETECTION
{'=' * 60}

Activities Analyzed: {result.get('activities_analyzed', 0)}
Analysis Time: {result.get('timestamp', 'N/A')}

{result['anomalies']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def show_ai_security_report(self):
        """Show comprehensive AI-enhanced security report"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0",
                                     "🤖 Generating comprehensive AI security report...\nThis may take a moment...\n")
        self.security_display.update()

        report = self.security_dashboard.ai_generate_security_report()

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", report)

    def ask_security_question(self):
        """Ask a natural language security question"""
        if not hasattr(self, 'security_display'):
            messagebox.showinfo("Info", "Please open Security Dashboard first")
            return

        question = simpledialog.askstring(
            "Security Question",
            "Ask me anything about your security status:",
            parent=self.root
        )

        if not question:
            return

        self.security_display.delete("1.0", "end")
        self.security_display.insert("1.0", f"❓ Question: {question}\n\n🤖 Thinking...\n")
        self.security_display.update()

        result = self.security_dashboard.ai_natural_language_query(question)

        self.security_display.delete("1.0", "end")
        if result.get("success"):
            self.security_display.insert("1.0", f"""
❓ SECURITY QUESTION & ANSWER
{'=' * 60}

Question: {result.get('question', question)}
Answered: {result.get('timestamp', 'N/A')}

{result['answer']}
            """)
        else:
            self.security_display.insert("1.0", f"⚠️ Error: {result.get('message', 'Unknown error')}")

    def run_comprehensive_analysis(self):
        """Run comprehensive AI screen analysis"""

        def execute():
            self.update_output("\n🧠 Running Comprehensive AI Analysis...\n", "command")
            result = self.advanced_monitor.advanced_screen_analysis("comprehensive")
            if result["success"]:
                self.update_output(result["analysis"], "success")
                if result.get("structured_data"):
                    scores = result["structured_data"].get("scores", {})
                    if scores:
                        self.update_output(f"\n📊 Scores: {scores}", "info")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_security_scan(self):
        """Run security scan"""

        def execute():
            self.update_output("\n🛡️ Running Security Scan...\n", "command")
            result = self.advanced_monitor.security_scan()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_performance_audit(self):
        """Run performance audit"""

        def execute():
            self.update_output("\n⚡ Running Performance Audit...\n", "command")
            result = self.advanced_monitor.performance_audit()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_ux_review(self):
        """Run UX expert review"""

        def execute():
            self.update_output("\n🎨 Running UX Expert Review...\n", "command")
            result = self.advanced_monitor.ux_expert_review()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_accessibility_audit(self):
        """Run accessibility audit"""

        def execute():
            self.update_output("\n♿ Running Accessibility Audit...\n", "command")
            result = self.advanced_monitor.accessibility_audit()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_code_review(self):
        """Run code review"""

        def execute():
            self.update_output("\n💻 Running Code Review...\n", "command")
            result = self.advanced_monitor.code_review()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_design_critique(self):
        """Run design critique"""

        def execute():
            self.update_output("\n🎭 Running Design Critique...\n", "command")
            result = self.advanced_monitor.design_critique()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def run_automation_discovery(self):
        """Find automation opportunities"""

        def execute():
            self.update_output("\n🤖 Finding Automation Opportunities...\n", "command")
            result = self.advanced_monitor.find_automation_opportunities()
            if result["success"]:
                self.update_output(result["analysis"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def view_analytics_report(self):
        """View analytics report"""

        def execute():
            self.update_output("\n📊 Generating Analytics Report...\n", "command")
            result = self.advanced_monitor.get_analytics_report()
            if result["success"]:
                self.update_output(result["report"], "success")
            else:
                self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def start_continuous_monitoring(self):
        """Start continuous monitoring with dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 Continuous Monitoring Setup")
        dialog.geometry("500x400")
        dialog.configure(bg="#1a1a2e")

        tk.Label(dialog, text="⚙️ Configure Continuous Monitoring",
                 bg="#1a1a2e", fg="#ffffff",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        tk.Label(dialog, text="Duration (minutes):",
                 bg="#1a1a2e", fg="#a6adc8",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        duration_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        duration_entry.insert(0, "60")
        duration_entry.pack()

        tk.Label(dialog, text="Check Interval (seconds):",
                 bg="#1a1a2e", fg="#a6adc8",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, "30")
        interval_entry.pack()

        triggers_frame = tk.Frame(dialog, bg="#1a1a2e")
        triggers_frame.pack(pady=15)

        tk.Label(triggers_frame, text="Triggers:",
                 bg="#1a1a2e", fg="#a6adc8",
                 font=("Segoe UI", 10, "bold")).pack()

        error_var = tk.BooleanVar(value=True)
        security_var = tk.BooleanVar(value=True)
        perf_var = tk.BooleanVar(value=True)

        tk.Checkbutton(triggers_frame, text="Error Detection",
                       variable=error_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Checkbutton(triggers_frame, text="Security Monitoring",
                       variable=security_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
        tk.Checkbutton(triggers_frame, text="Performance Issues",
                       variable=perf_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")

        def start_monitoring():
            duration = int(duration_entry.get())
            interval = int(interval_entry.get())
            triggers = {
                "errors": error_var.get(),
                "security": security_var.get(),
                "performance_issues": perf_var.get()
            }
            dialog.destroy()

            def execute():
                self.update_output(f"\n🔄 Starting Continuous Monitoring for {duration} minutes...\n", "command")
                result = self.advanced_monitor.continuous_monitoring(
                    duration_minutes=duration,
                    check_interval=interval,
                    triggers=triggers
                )
                if result["success"]:
                    self.update_output(
                        f"✅ Monitoring completed! {result['total_checks']} checks performed, {result['alerts_triggered']} alerts triggered.",
                        "success")
                else:
                    self.update_output(f"Error: {result.get('error', 'Unknown error')}", "error")

            threading.Thread(target=execute, daemon=True).start()

        tk.Button(dialog, text="▶️ Start Monitoring",
                  bg="#89b4fa", fg="#0f0f1e",
                  font=("Segoe UI", 11, "bold"),
                  command=start_monitoring, padx=20, pady=8).pack(pady=15)

    def ai_monitor_productivity(self):
        """Run instant productivity analysis with new AI monitor"""

        def execute():
            self.update_output("\n📊 Analyzing Productivity...\n", "command")
            result = self.ai_monitor.analyze_now("productivity")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                score = data.get("productivity_score", 0)

                self.update_output(f"⭐ Productivity Score: {score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Analysis failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_security(self):
        """Run instant security scan"""

        def execute():
            self.update_output("\n🔒 Running Security Scan...\n", "command")
            result = self.ai_monitor.analyze_now("security")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                risk_level = data.get("risk_level", "UNKNOWN")

                self.update_output(f"🛡️ Risk Level: {risk_level}\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Scan failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_performance(self):
        """Run instant performance analysis"""

        def execute():
            self.update_output("\n⚡ Analyzing Performance...\n", "command")
            result = self.ai_monitor.analyze_now("performance")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                score = data.get("performance_score", 0)

                self.update_output(f"⚡ Performance Score: {score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Analysis failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_errors(self):
        """Run instant error detection"""

        def execute():
            self.update_output("\n🐛 Detecting Errors...\n", "command")
            result = self.ai_monitor.analyze_now("errors")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                errors_found = data.get("errors_found", False)
                error_count = data.get("error_count", 0)

                if errors_found:
                    self.update_output(f"⚠️ {error_count} Error(s) Detected!\n", "info")
                else:
                    self.update_output(f"✅ No Errors Detected\n", "info")

                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Detection failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_ux(self):
        """Run instant UX/Design review"""

        def execute():
            self.update_output("\n🎨 Reviewing UX/Design...\n", "command")
            result = self.ai_monitor.analyze_now("ux")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                ux_score = data.get("ux_score", 0)

                self.update_output(f"🎨 UX Score: {ux_score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Review failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_accessibility(self):
        """Run instant accessibility audit"""

        def execute():
            self.update_output("\n♿ Running Accessibility Audit...\n", "command")
            result = self.ai_monitor.analyze_now("accessibility")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                acc_score = data.get("accessibility_score", 0)

                self.update_output(f"♿ Accessibility Score: {acc_score}/10\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Audit failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_code(self):
        """Run instant code review"""

        def execute():
            self.update_output("\n💻 Reviewing Code...\n", "command")
            result = self.ai_monitor.analyze_now("code")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                code_detected = data.get("code_detected", False)

                if code_detected:
                    quality_score = data.get("code_quality_score", 0)
                    self.update_output(f"💻 Code Quality Score: {quality_score}/10\n", "info")
                else:
                    self.update_output(f"ℹ️ No Code Detected\n", "info")

                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Review failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_automation(self):
        """Run instant automation discovery"""

        def execute():
            self.update_output("\n🤖 Finding Automation Opportunities...\n", "command")
            result = self.ai_monitor.analyze_now("automation")
            if result.get("success"):
                data = result.get("data", {})
                analysis = result.get("analysis", "")
                opportunities = data.get("automation_opportunities", [])

                self.update_output(f"🤖 {len(opportunities)} Automation Opportunity(ies) Found\n", "info")
                self.update_output(f"{analysis}\n", "success")
            else:
                self.update_output(f"❌ {result.get('message', 'Discovery failed')}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_start_continuous(self):
        """Start continuous AI monitoring"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 Start Continuous Monitoring")
        dialog.geometry("550x500")
        dialog.configure(bg="#1a1a2e")

        tk.Label(dialog, text="🔄 Continuous AI Monitoring",
                 bg="#1a1a2e", fg="#ffffff",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        tk.Label(dialog, text="Select monitoring modes:",
                 bg="#1a1a2e", fg="#a6adc8",
                 font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))

        modes_frame = tk.Frame(dialog, bg="#1a1a2e")
        modes_frame.pack(pady=10)

        mode_vars = {}
        for mode_id, mode_info in self.ai_monitor.ANALYSIS_MODES.items():
            var = tk.BooleanVar(value=mode_id in ["productivity", "errors", "security"])
            tk.Checkbutton(modes_frame, text=f"{mode_info['icon']} {mode_info['name']}",
                           variable=var, bg="#1a1a2e", fg="#ffffff",
                           selectcolor="#313244", font=("Segoe UI", 9)).pack(anchor="w")
            mode_vars[mode_id] = var

        tk.Label(dialog, text="Check interval (seconds):",
                 bg="#1a1a2e", fg="#a6adc8",
                 font=("Segoe UI", 10)).pack(pady=(15, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, "30")
        interval_entry.pack()

        def start():
            selected_modes = [mode for mode, var in mode_vars.items() if var.get()]
            interval = int(interval_entry.get())
            dialog.destroy()

            def execute():
                self.update_output(f"\n🔄 Starting Continuous Monitoring...\n", "command")
                self.update_output(f"   📊 Modes: {', '.join(selected_modes)}\n", "info")
                self.update_output(f"   ⏱️  Interval: {interval}s\n", "info")

                result = self.ai_monitor.start_monitoring(modes=selected_modes, interval=interval)
                if result.get("success"):
                    self.update_output(f"✅ {result['message']}\n", "success")
                    self.update_output(f"   ℹ️ Monitoring is running in background. Use 'Stop Monitoring' to end.\n",
                                       "info")
                else:
                    self.update_output(f"❌ {result.get('message')}", "error")

            threading.Thread(target=execute, daemon=True).start()

        tk.Button(dialog, text="▶️ Start Monitoring",
                  bg="#89b4fa", fg="#0f0f1e",
                  font=("Segoe UI", 11, "bold"),
                  command=start, padx=20, pady=8).pack(pady=15)

    def ai_monitor_pause_resume(self):
        """Pause or resume monitoring"""
        if self.ai_monitor.paused:
            result = self.ai_monitor.resume_monitoring()
            self.update_output(f"▶️ {result['message']}\n", "success")
        else:
            result = self.ai_monitor.pause_monitoring()
            self.update_output(f"⏸️ {result['message']}\n", "success")

    def ai_monitor_stop(self):
        """Stop continuous monitoring"""
        result = self.ai_monitor.stop_monitoring()
        if result.get("success"):
            stats = result.get("stats", {})
            self.update_output(f"\n✅ {result['message']}\n", "success")
            self.update_output(f"   📊 Session Statistics:\n", "info")
            self.update_output(f"      • Screenshots: {stats.get('total_screenshots', 0)}\n", "info")
            self.update_output(f"      • AI Analyses: {stats.get('ai_analyses', 0)}\n", "info")
            self.update_output(f"      • Changes Detected: {stats.get('changes_detected', 0)}\n", "info")
            self.update_output(f"      • Alerts Triggered: {stats.get('alerts_triggered', 0)}\n", "info")
        else:
            self.update_output(f"❌ {result.get('message')}", "error")

    def ai_monitor_view_analytics(self):
        """View analytics dashboard"""

        def execute():
            self.update_output("\n📈 Analytics Dashboard\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            summary = self.ai_monitor.get_analytics_summary()

            prod = summary.get("productivity", {})
            sec = summary.get("security", {})
            err = summary.get("errors", {})
            perf = summary.get("performance", {})
            patterns = summary.get("patterns", {})
            session = summary.get("session", {})

            self.update_output(f"\n📊 Productivity Analytics:\n", "info")
            self.update_output(f"   • Average Score: {prod.get('average_score', 0)}/10\n", "success")
            self.update_output(f"   • Total Measurements: {prod.get('total_measurements', 0)}\n", "success")

            self.update_output(f"\n🔒 Security Analytics:\n", "info")
            self.update_output(f"   • Total Issues: {sec.get('total_issues', 0)}\n", "success")
            self.update_output(f"   • Critical Issues: {sec.get('critical_issues', 0)}\n", "success")

            self.update_output(f"\n🐛 Error Analytics:\n", "info")
            self.update_output(f"   • Total Errors: {err.get('total_errors', 0)}\n", "success")

            self.update_output(f"\n⚡ Performance Analytics:\n", "info")
            self.update_output(f"   • Measurements: {perf.get('measurements', 0)}\n", "success")

            self.update_output(f"\n🧠 Pattern Learning:\n", "info")
            self.update_output(f"   • Patterns Learned: {patterns.get('patterns_learned', 0)}\n", "success")

            self.update_output(f"\n📊 Current Session:\n", "info")
            self.update_output(f"   • Screenshots: {session.get('total_screenshots', 0)}\n", "success")
            self.update_output(f"   • AI Analyses: {session.get('ai_analyses', 0)}\n", "success")
            self.update_output(f"   • Changes Detected: {session.get('changes_detected', 0)}\n", "success")
            self.update_output(f"   • Alerts: {session.get('alerts_triggered', 0)}\n", "success")

            self.update_output("\n" + "=" * 60 + "\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_productivity_trends(self):
        """View productivity trends"""

        def execute():
            self.update_output("\n📊 Productivity Trends Analysis\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            trends = self.ai_monitor.get_productivity_trends()

            if "message" in trends:
                self.update_output(f"{trends['message']}\n", "info")
            else:
                hourly = trends.get("hourly_averages", {})
                peak_hour = trends.get("peak_productivity_hour", 0)
                peak_score = trends.get("peak_productivity_score", 0)
                low_hour = trends.get("lowest_productivity_hour", 0)
                low_score = trends.get("lowest_productivity_score", 0)

                self.update_output(f"📈 Hourly Productivity Averages:\n", "info")
                for hour in sorted(hourly.keys()):
                    score = hourly[hour]
                    bar = "█" * int(score)
                    self.update_output(f"   {hour:02d}:00 | {bar} {score:.1f}/10\n", "success")

                self.update_output(f"\n🌟 Peak Productivity:\n", "info")
                self.update_output(f"   • Hour: {peak_hour:02d}:00\n", "success")
                self.update_output(f"   • Score: {peak_score:.1f}/10\n", "success")

                self.update_output(f"\n📉 Lowest Productivity:\n", "info")
                self.update_output(f"   • Hour: {low_hour:02d}:00\n", "success")
                self.update_output(f"   • Score: {low_score:.1f}/10\n", "success")

            self.update_output("\n" + "=" * 60 + "\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_view_alerts(self):
        """View recent alerts"""

        def execute():
            self.update_output("\n🚨 Recent Alerts\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            alerts = self.ai_monitor.get_recent_alerts(limit=10)

            if not alerts:
                self.update_output("ℹ️ No alerts yet\n", "info")
            else:
                for i, alert in enumerate(alerts, 1):
                    severity = alert.get("severity", "UNKNOWN")
                    alert_type = alert.get("type", "UNKNOWN")
                    message = alert.get("message", "")
                    timestamp = alert.get("timestamp", "")

                    icon = "🔴" if severity == "CRITICAL" else "🟡" if severity == "HIGH" else "🟢"

                    self.update_output(f"\n{i}. {icon} [{severity}] {alert_type}\n", "info")
                    self.update_output(f"   {message}\n", "success")
                    self.update_output(f"   ⏰ {timestamp}\n", "success")

            self.update_output("\n" + "=" * 60 + "\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def ai_monitor_configure(self):
        """Configure monitoring settings"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚙️ Monitoring Configuration")
        dialog.geometry("500x550")
        dialog.configure(bg="#1a1a2e")

        tk.Label(dialog, text="⚙️ Monitoring Settings",
                 bg="#1a1a2e", fg="#ffffff",
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        config = self.ai_monitor.get_config()

        tk.Label(dialog, text="Default check interval (seconds):",
                 bg="#1a1a2e", fg="#a6adc8",
                 font=("Segoe UI", 10)).pack(pady=(10, 5))
        interval_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=20)
        interval_entry.insert(0, str(config.get("default_interval", 30)))
        interval_entry.pack()

        change_detection_var = tk.BooleanVar(value=config.get("change_detection", True))
        tk.Checkbutton(dialog, text="Enable change detection (skip identical screens)",
                       variable=change_detection_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)

        smart_scheduling_var = tk.BooleanVar(value=config.get("smart_scheduling", True))
        tk.Checkbutton(dialog, text="Enable smart scheduling",
                       variable=smart_scheduling_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)

        privacy_mode_var = tk.BooleanVar(value=config.get("privacy_mode", False))
        tk.Checkbutton(dialog, text="Privacy mode (no screenshots saved)",
                       variable=privacy_mode_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=5)

        tk.Label(dialog, text="Auto Actions:",
                 bg="#1a1a2e", fg="#a6adc8",
                 font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))

        auto_actions = config.get("auto_actions", {})

        screenshot_on_error_var = tk.BooleanVar(value=auto_actions.get("screenshot_on_error", True))
        tk.Checkbutton(dialog, text="Auto-screenshot on errors",
                       variable=screenshot_on_error_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)

        alert_on_security_var = tk.BooleanVar(value=auto_actions.get("alert_on_security", True))
        tk.Checkbutton(dialog, text="Alert on security issues",
                       variable=alert_on_security_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)

        log_productivity_var = tk.BooleanVar(value=auto_actions.get("log_productivity", True))
        tk.Checkbutton(dialog, text="Log productivity metrics",
                       variable=log_productivity_var, bg="#1a1a2e", fg="#ffffff",
                       selectcolor="#313244", font=("Segoe UI", 9)).pack(pady=2)

        def save_settings():
            updates = {
                "default_interval": int(interval_entry.get()),
                "change_detection": change_detection_var.get(),
                "smart_scheduling": smart_scheduling_var.get(),
                "privacy_mode": privacy_mode_var.get(),
                "auto_actions": {
                    "screenshot_on_error": screenshot_on_error_var.get(),
                    "alert_on_security": alert_on_security_var.get(),
                    "log_productivity": log_productivity_var.get()
                }
            }

            result = self.ai_monitor.update_config(updates)
            self.update_output(f"✅ {result['message']}\n", "success")
            dialog.destroy()

        tk.Button(dialog, text="💾 Save Settings",
                  bg="#89b4fa", fg="#0f0f1e",
                  font=("Segoe UI", 11, "bold"),
                  command=save_settings, padx=20, pady=8).pack(pady=20)

    def ai_monitor_clear_analytics(self):
        """Clear analytics data"""
        response = messagebox.askyesno(
            "Confirm Clear Analytics",
            "Are you sure you want to clear all analytics data?\n\nThis will delete:\n• Productivity history\n• Security issues log\n• Error history\n• Performance metrics\n• Learned patterns\n\nThis action cannot be undone."
        )

        if response:
            result = self.ai_monitor.clear_analytics()
            self.update_output(f"✅ {result['message']}\n", "success")

    def smart_auto_bug_fixer(self):
        """Auto-Bug Fixer interface"""

        def execute():
            self.update_output("\n🐛 Auto-Bug Fixer\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            error_text = self.show_input_dialog(
                "Auto-Bug Fixer",
                "Enter error log or error message to analyze:"
            )

            if error_text:
                self.update_output(f"Analyzing error...\n", "info")
                analysis = self.smart_automation.bug_fixer.analyze_error_log(error_text)

                self.update_output(f"\n📋 Error Analysis\n", "success")
                self.update_output(f"Type: {analysis.get('error_type', 'Unknown')}\n", "info")
                self.update_output(f"Severity: {analysis.get('severity', 'Unknown')}\n", "info")
                self.update_output(f"\n🔍 Root Cause:\n{analysis.get('root_cause', 'N/A')}\n", "info")

                if analysis.get('fix_steps'):
                    self.update_output(f"\n✅ Fix Steps:\n", "success")
                    for i, step in enumerate(analysis.get('fix_steps', []), 1):
                        self.update_output(f"{i}. {step}\n", "info")

                if analysis.get('prevention_tips'):
                    self.update_output(f"\n💡 Prevention Tips:\n", "success")
                    for tip in analysis.get('prevention_tips', []):
                        self.update_output(f"• {tip}\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_meeting_scheduler(self):
        """Meeting Scheduler AI interface"""

        def execute():
            self.update_output("\n📅 Meeting Scheduler AI\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            title = self.show_input_dialog("Meeting Title", "Enter meeting title:")
            if not title:
                return

            duration = self.show_input_dialog("Duration", "Duration in minutes (e.g., 30):")
            if not duration:
                return

            attendees = self.show_input_dialog("Attendees", "Enter attendee emails (comma-separated):")
            if not attendees:
                return

            attendee_list = [a.strip() for a in attendees.split(',') if a.strip()]

            self.update_output("Finding optimal meeting time...\n", "info")
            result = self.smart_automation.meeting_scheduler.schedule_meeting(
                title, int(duration), attendee_list
            )

            if result.get('success'):
                time_slot = result['scheduled_time']
                self.update_output(f"\n✅ Meeting Scheduled!\n", "success")
                self.update_output(f"Title: {title}\n", "info")
                self.update_output(f"Time: {time_slot.get('start', 'N/A')}\n", "info")
                self.update_output(f"Duration: {duration} minutes\n", "info")
                self.update_output(f"Event ID: {result.get('event_id', 'N/A')}\n", "info")

                if result.get('alternatives'):
                    self.update_output(f"\n📋 Alternative Times:\n", "success")
                    for alt in result['alternatives']:
                        self.update_output(f"• {alt.get('start', 'N/A')}\n", "info")
            else:
                self.update_output(f"❌ {result.get('message', 'Failed to schedule')}\n", "error")

        threading.Thread(target=execute, daemon=True).start()

    def smart_file_recommender(self):
        """Smart File Recommendations interface"""

        def execute():
            self.update_output("\n📁 Smart File Recommendations\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            task = self.show_input_dialog(
                "Current Task",
                "What are you working on? (optional, press Enter to skip):"
            )

            self.update_output("Analyzing file patterns...\n", "info")
            recommendations = self.smart_automation.file_recommender.recommend_files(
                current_task=task if task else None,
                limit=10
            )

            if recommendations:
                self.update_output(f"\n✅ Recommended Files ({len(recommendations)}):\n", "success")
                for i, rec in enumerate(recommendations, 1):
                    self.update_output(f"\n{i}. {rec.get('file', 'Unknown')}\n", "info")
                    self.update_output(f"   Reason: {rec.get('reason', 'N/A')}\n", "success")
                    self.update_output(f"   Score: {rec.get('score', 0)}/100\n", "info")
            else:
                self.update_output("ℹ️ No recommendations available yet. Start working with files to build patterns!\n",
                                   "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_doc_generator(self):
        """Auto-Documentation Generator interface"""

        def execute():
            self.update_output("\n📝 Auto-Documentation Generator\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            doc_type = self.show_input_dialog(
                "Documentation Type",
                "What to generate?\n1. README for project\n2. Function documentation\n3. API documentation\n\nEnter number (1-3):"
            )

            if doc_type == "1":
                self.update_output("Generating README.md...\n", "info")
                readme = self.smart_automation.doc_generator.generate_readme(".")
                self.update_output(f"\n✅ README Generated!\n", "success")
                self.update_output(f"{readme[:500]}...\n", "info")
                self.update_output(f"\nSaved to: auto_generated_docs/README_generated.md\n", "success")
            elif doc_type == "2":
                file_path = self.show_input_dialog("File Path", "Enter file path to document:")
                if file_path:
                    self.update_output(f"Generating documentation for {file_path}...\n", "info")
                    result = self.smart_automation.doc_generator.document_file(file_path)
                    if result.get('success'):
                        self.update_output(f"\n✅ Documentation Generated!\n", "success")
                        self.update_output(f"Saved to: {result.get('docs_path', 'N/A')}\n", "info")
                    else:
                        self.update_output(f"❌ {result.get('error', 'Failed')}\n", "error")
            elif doc_type == "3":
                self.update_output("API documentation feature requires code input.\n", "info")
                self.update_output("Use 'Function documentation' option instead.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_command_shortcuts(self):
        """Intelligent Command Shortcuts interface"""

        def execute():
            self.update_output("\n⚡ Intelligent Command Shortcuts\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            action = self.show_input_dialog(
                "Command Shortcuts",
                "What would you like to do?\n1. View suggestions\n2. Create shortcut\n3. View most used\n\nEnter number (1-3):"
            )

            if action == "1":
                self.update_output("Analyzing command patterns...\n", "info")
                suggestions = self.smart_automation.command_shortcuts.suggest_shortcuts()

                if suggestions:
                    self.update_output(f"\n✅ Shortcut Suggestions ({len(suggestions)}):\n", "success")
                    for i, sug in enumerate(suggestions, 1):
                        self.update_output(f"\n{i}. {sug.get('shortcut', 'N/A')}\n", "info")
                        self.update_output(f"   {sug.get('description', 'N/A')}\n", "success")
                        self.update_output(f"   Commands: {', '.join(sug.get('commands', []))}\n", "info")
                else:
                    self.update_output("ℹ️ No patterns detected yet. Keep using commands!\n", "info")

            elif action == "2":
                name = self.show_input_dialog("Shortcut Name", "Enter shortcut name:")
                if name:
                    self.update_output(f"Shortcut '{name}' created!\n", "success")

            elif action == "3":
                shortcuts = self.smart_automation.command_shortcuts.get_most_used_shortcuts(5)
                if shortcuts:
                    self.update_output(f"\n✅ Most Used Shortcuts:\n", "success")
                    for i, shortcut in enumerate(shortcuts, 1):
                        self.update_output(f"\n{i}. {shortcut.get('name', 'N/A')}\n", "info")
                        self.update_output(f"   Used: {shortcut.get('usage_count', 0)} times\n", "success")
                else:
                    self.update_output("ℹ️ No shortcuts created yet.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_context_switcher(self):
        """Project Context Switcher interface"""

        def execute():
            self.update_output("\n🔀 Project Context Switcher\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            contexts = self.smart_automation.context_switcher.list_contexts()

            if contexts:
                self.update_output(f"\n📋 Saved Contexts ({len(contexts)}):\n", "success")
                for i, ctx in enumerate(contexts, 1):
                    self.update_output(f"\n{i}. {ctx.get('name', 'N/A')}\n", "info")
                    self.update_output(f"   Path: {ctx.get('project_path', 'N/A')}\n", "success")
                    self.update_output(f"   Files: {ctx.get('file_count', 0)}\n", "info")
                    self.update_output(f"   Last accessed: {ctx.get('last_accessed', 'N/A')[:19]}\n", "info")
            else:
                self.update_output("ℹ️ No saved contexts yet.\n", "info")

            current = self.smart_automation.context_switcher.get_current_context()
            if current:
                self.update_output(f"\n✅ Current Context: {current.get('name', 'None')}\n", "success")

        threading.Thread(target=execute, daemon=True).start()

    def smart_task_prioritizer(self):
        """Task Auto-Prioritizer interface"""

        def execute():
            self.update_output("\n🎯 Task Auto-Prioritizer\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            self.update_output("Prioritizing tasks with AI...\n", "info")
            prioritized = self.smart_automation.task_prioritizer.prioritize_tasks()

            if prioritized:
                self.update_output(f"\n✅ Prioritized Tasks ({len(prioritized)}):\n", "success")
                for i, task in enumerate(prioritized[:10], 1):
                    score = task.get('priority_score', 0)
                    self.update_output(f"\n{i}. [{score:.0f}/100] {task.get('title', 'N/A')}\n", "info")
                    if task.get('deadline'):
                        self.update_output(f"   Deadline: {task['deadline'][:10]}\n", "success")
                    if task.get('priority_reason'):
                        self.update_output(f"   Why: {task['priority_reason']}\n", "info")

                suggestions = self.smart_automation.task_prioritizer.get_task_suggestions()
                if suggestions:
                    self.update_output(f"\n💡 Suggestions:\n", "success")
                    for suggestion in suggestions:
                        self.update_output(f"• {suggestion}\n", "info")
            else:
                self.update_output("ℹ️ No tasks to prioritize. Add tasks first!\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_workflow_optimizer(self):
        """Workflow Auto-Optimizer interface"""

        def execute():
            self.update_output("\n🔧 Workflow Auto-Optimizer\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            self.update_output("Analyzing workflow patterns...\n", "info")
            report = self.smart_automation.workflow_optimizer.get_efficiency_report()

            self.update_output(f"\n📊 Efficiency Report\n", "success")
            self.update_output(f"Total Actions: {report.get('total_actions', 0)}\n", "info")
            self.update_output(f"Detected Patterns: {report.get('detected_patterns', 0)}\n", "info")
            self.update_output(f"Optimizable Actions: {report.get('optimizable_actions', 0)}\n", "info")
            self.update_output(f"Efficiency Score: {report.get('efficiency_score', 0)}/100\n", "success")

            if report.get('top_patterns'):
                self.update_output(f"\n🔄 Top Repeated Patterns:\n", "success")
                for pattern in report['top_patterns'][:5]:
                    self.update_output(f"• {pattern.get('pattern', 'N/A')} ({pattern.get('occurrences', 0)}x)\n",
                                       "info")

            if report.get('recommendations'):
                self.update_output(f"\n💡 Recommendations:\n", "success")
                for rec in report['recommendations']:
                    self.update_output(f"• {rec}\n", "info")

            self.update_output("\nGenerating optimization suggestions...\n", "info")
            optimizations = self.smart_automation.workflow_optimizer.suggest_optimizations()

            if optimizations:
                self.update_output(f"\n✅ Optimization Suggestions:\n", "success")
                for i, opt in enumerate(optimizations[:5], 1):
                    self.update_output(f"\n{i}. Pattern: {opt.get('pattern', 'N/A')}\n", "info")
                    self.update_output(f"   Suggestion: {opt.get('suggestion', 'N/A')}\n", "success")
                    self.update_output(f"   Time Saved: {opt.get('time_saved', 'N/A')}\n", "info")
                    self.update_output(f"   Difficulty: {opt.get('difficulty', 'N/A')}\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def smart_template_generator(self):
        """Smart Template Generator interface"""

        def execute():
            self.update_output("\n📋 Smart Template Generator\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            template_type = self.show_input_dialog(
                "Template Type",
                "What type of template?\n1. Code template\n2. Email template\n3. Document template\n\nEnter number (1-3):"
            )

            if template_type == "1":
                language = self.show_input_dialog("Language", "Programming language (e.g., python, javascript):")
                template_kind = self.show_input_dialog("Type", "Template type (e.g., class, function, api):")

                if language and template_kind:
                    self.update_output(f"Generating {language} {template_kind} template...\n", "info")
                    template = self.smart_automation.template_generator.generate_code_template(
                        language, template_kind
                    )
                    self.update_output(f"\n✅ Code Template Generated!\n", "success")
                    self.update_output(f"{template[:500]}...\n", "info")

            elif template_type == "2":
                purpose = self.show_input_dialog("Purpose", "Email purpose (e.g., job application, follow-up):")
                tone = self.show_input_dialog("Tone", "Tone (professional/casual/friendly):", "professional")

                if purpose:
                    self.update_output(f"Generating email template...\n", "info")
                    template = self.smart_automation.template_generator.generate_email_template(
                        purpose, tone if tone else "professional"
                    )
                    self.update_output(f"\n✅ Email Template Generated!\n", "success")
                    self.update_output(f"{template[:400]}...\n", "info")

            elif template_type == "3":
                doc_type = self.show_input_dialog("Document Type", "Document type (e.g., proposal, report):")

                if doc_type:
                    self.update_output(f"Generating document template...\n", "info")
                    template = self.smart_automation.template_generator.generate_document_template(doc_type)
                    self.update_output(f"\n✅ Document Template Generated!\n", "success")
                    self.update_output(f"{template[:400]}...\n", "info")

            templates = self.smart_automation.template_generator.list_templates()
            self.update_output(f"\n📋 Total Templates Created: {len(templates)}\n", "success")

        threading.Thread(target=execute, daemon=True).start()

    def smart_automation_dashboard(self):
        """Show Smart Automation Dashboard"""

        def execute():
            self.update_output("\n📊 Smart Automation Dashboard\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            summary = self.smart_automation.get_dashboard_summary()

            self.update_output(f"\n🐛 Auto-Bug Fixer\n", "success")
            self.update_output(f"Fixes Applied: {summary['auto_bug_fixer']['fixes_applied']}\n", "info")

            self.update_output(f"\n📅 Meeting Scheduler\n", "success")
            self.update_output(f"Upcoming Meetings: {summary['meeting_scheduler']['upcoming_meetings']}\n", "info")

            self.update_output(f"\n📁 File Recommender\n", "success")
            self.update_output(f"Tracked Files: {summary['file_recommender']['tracked_files']}\n", "info")

            self.update_output(f"\n⚡ Command Shortcuts\n", "success")
            self.update_output(f"Shortcuts Created: {summary['command_shortcuts']['shortcuts_created']}\n", "info")

            self.update_output(f"\n🔀 Project Contexts\n", "success")
            self.update_output(f"Saved Contexts: {summary['project_contexts']['saved_contexts']}\n", "info")

            self.update_output(f"\n🎯 Task Prioritizer\n", "success")
            self.update_output(f"Pending Tasks: {summary['task_prioritizer']['pending_tasks']}\n", "info")

            self.update_output(f"\n🔧 Workflow Optimizer\n", "success")
            self.update_output(f"Patterns Detected: {summary['workflow_optimizer']['patterns_detected']}\n", "info")
            self.update_output(f"Efficiency Score: {summary['workflow_optimizer']['efficiency_score']}/100\n", "info")

            self.update_output(f"\n📋 Template Generator\n", "success")
            self.update_output(f"Templates Created: {summary['template_generator']['templates_created']}\n", "info")

            self.update_output("\n" + "=" * 60 + "\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def show_input_dialog(self, title, prompt, default=""):
        """Helper method to show input dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x200")
        dialog.configure(bg="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=prompt,
                 bg="#1a1a2e", fg="#ffffff",
                 font=("Segoe UI", 10),
                 wraplength=450).pack(pady=20, padx=20)

        entry = tk.Entry(dialog, font=("Segoe UI", 11), width=40)
        entry.insert(0, default)
        entry.pack(pady=10)
        entry.focus()

        result: list = [None]

        def on_ok():
            result[0] = entry.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        entry.bind("<Return>", lambda e: on_ok())
        entry.bind("<Escape>", lambda e: on_cancel())

        btn_frame = tk.Frame(dialog, bg="#1a1a2e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="OK", command=on_ok,
                  bg="#89b4fa", fg="#0f0f1e",
                  font=("Segoe UI", 10, "bold"),
                  padx=20, pady=5).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Cancel", command=on_cancel,
                  bg="#313244", fg="#ffffff",
                  font=("Segoe UI", 10),
                  padx=20, pady=5).pack(side="left", padx=5)

        dialog.wait_window()
        return result[0]

    def launch_batch_controller(self):
        """Launch Windows batch file controller"""

        def execute():
            self.update_output("\n🗂️ Desktop File Controller\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            result = self.desktop_controller.launch_batch_controller()

            if result["success"]:
                self.update_output(f"✅ {result['message']}\n", "success")
                self.update_output("The batch file controller window has been opened.\n", "info")
            else:
                self.update_output(f"ℹ️ {result['message']}\n", "info")
                self.update_output("\nYou can use the Python-based buttons below instead:\n", "info")
                self.update_output("• List Desktop Items\n", "info")
                self.update_output("• Create New Folder\n", "info")
                self.update_output("• Organize Desktop\n", "info")
                self.update_output("• Search Desktop Files\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def list_desktop_items(self):
        """List all items on desktop"""

        def execute():
            self.update_output("\n📋 Desktop Contents\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            result = self.desktop_controller.list_items()

            if result["success"]:
                self.update_output(f"📁 Total items: {result['count']}\n\n", "success")

                folders = [item for item in result["items"] if item["type"] == "Folder"]
                files = [item for item in result["items"] if item["type"] == "File"]

                if folders:
                    self.update_output(f"📂 Folders ({len(folders)}):\n", "success")
                    for item in folders[:15]:
                        self.update_output(f"  📁 {item['name']}\n", "info")
                    if len(folders) > 15:
                        self.update_output(f"  ... and {len(folders) - 15} more folders\n", "info")
                    self.update_output("\n", "info")

                if files:
                    self.update_output(f"📄 Files ({len(files)}):\n", "success")
                    for item in files[:15]:
                        self.update_output(f"  📄 {item['name']}\n", "info")
                    if len(files) > 15:
                        self.update_output(f"  ... and {len(files) - 15} more files\n", "info")

                self.update_output(f"\n📊 Desktop Path: {self.desktop_controller.desktop_path}\n", "info")
            else:
                self.update_output(f"❌ {result['message']}\n", "error")

        threading.Thread(target=execute, daemon=True).start()

    def create_desktop_folder(self):
        """Create a new folder on desktop"""

        def execute():
            folder_name = self.show_input_dialog(
                "Create Folder",
                "Enter the name for the new folder:"
            )

            if folder_name:
                self.update_output("\n➕ Creating Folder...\n", "command")
                self.update_output("=" * 60 + "\n", "info")

                result = self.desktop_controller.create_folder(folder_name)

                if result["success"]:
                    self.update_output(f"✅ {result['message']}\n", "success")
                    self.update_output(f"📁 Path: {result['path']}\n", "info")
                else:
                    self.update_output(f"❌ {result['message']}\n", "error")
            else:
                self.update_output("ℹ️ Folder creation cancelled.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    def organize_desktop(self):
        """Organize desktop files by type"""

        def execute():
            self.update_output("\n📁 Organizing Desktop...\n", "command")
            self.update_output("=" * 60 + "\n", "info")
            self.update_output("Sorting files into folders by type...\n", "info")
            self.update_output("• Documents (txt, pdf, doc, xls, ppt)\n", "info")
            self.update_output("• Images (jpg, png, gif, bmp, svg)\n", "info")
            self.update_output("• Videos (mp4, avi, mkv, mov)\n", "info")
            self.update_output("• Music (mp3, wav, flac)\n", "info")
            self.update_output("• Archives (zip, rar, 7z)\n", "info")
            self.update_output("• Programs (exe, msi)\n\n", "info")

            result = self.desktop_controller.organize_by_type()

            if result["success"]:
                self.update_output(f"✅ {result['message']}\n", "success")
                self.update_output("Your desktop is now organized!\n", "info")
            else:
                self.update_output(f"❌ {result['message']}\n", "error")

        threading.Thread(target=execute, daemon=True).start()

    def search_desktop_files(self):
        """Search for files on desktop"""

        def execute():
            search_term = self.show_input_dialog(
                "Search Desktop",
                "Enter search term (filename or part of filename):"
            )

            if search_term:
                self.update_output(f"\n🔍 Searching Desktop for '{search_term}'...\n", "command")
                self.update_output("=" * 60 + "\n", "info")

                result = self.desktop_controller.search_files(search_term)

                if result["success"]:
                    if result["count"] > 0:
                        self.update_output(f"✅ Found {result['count']} matching items:\n\n", "success")

                        for item in result["results"][:20]:
                            icon = "📁" if item["type"] == "Folder" else "📄"
                            self.update_output(f"{icon} {item['name']}\n", "info")
                            self.update_output(f"   Path: {item['path']}\n", "info")

                        if result['count'] > 20:
                            self.update_output(f"\n... and {result['count'] - 20} more results\n", "info")
                    else:
                        self.update_output(f"ℹ️ No files found matching '{search_term}'\n", "info")
                else:
                    self.update_output(f"❌ {result['message']}\n", "error")
            else:
                self.update_output("ℹ️ Search cancelled.\n", "info")

        threading.Thread(target=execute, daemon=True).start()

    # ===== PRODUCTIVITY HUB METHODS =====

    def start_pomodoro_session(self):
        """Start a new Pomodoro session"""
        task_name = self.show_input_dialog("Pomodoro Task", "What are you working on?", "Focused Work")
        if task_name:
            result = self.pomodoro_coach.start_pomodoro(task_name)
            self.update_output(f"\n🍅 Pomodoro Started!\n", "success")
            self.update_output(f"Task: {task_name}\n", "info")
            self.update_output(f"Duration: {result['duration']} minutes\n", "info")
            if result.get('ai_coach'):
                self.update_output(f"\n💬 AI Coach: {result['ai_coach']}\n", "command")

    def start_short_break(self):
        """Start a short break"""
        result = self.pomodoro_coach.start_break(is_long=False)
        self.update_output(f"\n☕ {result['message']}\n", "success")
        if result.get('ai_coach'):
            self.update_output(f"💬 AI Coach: {result['ai_coach']}\n", "info")

    def start_long_break(self):
        """Start a long break"""
        result = self.pomodoro_coach.start_break(is_long=True)
        self.update_output(f"\n🌳 {result['message']}\n", "success")
        if result.get('ai_coach'):
            self.update_output(f"💬 AI Coach: {result['ai_coach']}\n", "info")

    def toggle_pomodoro(self):
        """Pause/resume Pomodoro"""
        result = self.pomodoro_coach.pause_session()
        self.update_output(f"\n⏸️ {result['message']}\n", "info")

    def stop_pomodoro(self):
        """Stop current Pomodoro session"""
        result = self.pomodoro_coach.stop_session()
        self.update_output(f"\n🛑 {result['message']}\n", "info")

    def view_pomodoro_stats(self):
        """View Pomodoro statistics"""
        stats = self.pomodoro_coach.get_statistics()
        self.update_output(f"\n📊 POMODORO STATISTICS\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        self.update_output(f"Total Pomodoros: {stats['total_pomodoros']}\n", "info")
        self.update_output(f"Completed Today: {stats['pomodoros_today']}\n", "info")
        self.update_output(f"Total Work Time: {stats['total_work_hours']:.1f} hours\n", "info")
        self.update_output(f"Completion Rate: {stats['completion_rate']:.1f}%\n", "success")

    def start_task_tracking(self):
        """Start tracking a new task"""
        task_name = self.show_input_dialog("Task Name", "What task are you starting?")
        if task_name:
            category = self.show_input_dialog("Task Category", "Category (coding/meeting/email/documentation/etc):",
                                              "general")
            result = self.task_predictor.start_task(task_name, category or "general")
            self.update_output(f"\n▶️ Task Started: {task_name}\n", "success")
            self.update_output(f"Task ID: #{result['task_id']}\n", "info")
            self.update_output(f"Estimated Time: {result['estimated_minutes']} minutes\n", "info")
            self.update_output(f"Predicted Time: {result['predicted_minutes']} minutes\n", "command")
            self.update_output(f"Confidence: {result['confidence']}\n", "info")

    def complete_task(self):
        """Complete current task"""
        task_id = self.show_input_dialog("Task ID", "Enter task ID to complete:")
        if task_id:
            try:
                result = self.task_predictor.complete_task(int(task_id))
                if result['success']:
                    self.update_output(f"\n✅ Task Completed!\n", "success")
                    self.update_output(f"Task: {result['task_name']}\n", "info")
                    self.update_output(f"Estimated: {result['estimated_minutes']:.0f} min\n", "info")
                    self.update_output(f"Actual: {result['actual_minutes']:.0f} min\n", "info")
                    self.update_output(f"Accuracy: {result['accuracy']:.1f}%\n", "success")
                else:
                    self.update_output(f"❌ {result['message']}\n", "error")
            except ValueError:
                self.update_output("❌ Invalid task ID\n", "error")

    def view_task_predictions(self):
        """View task time predictions"""
        report = self.task_predictor.get_accuracy_report()
        self.update_output(f"\n📈 TASK PREDICTION REPORT\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        self.update_output(f"Total Tasks: {report['total_tasks']}\n", "info")
        self.update_output(f"Average Accuracy: {report['average_accuracy']:.1f}%\n", "success")
        self.update_output(f"Best Category: {report['best_category']}\n", "info")

    def view_task_analytics(self):
        """View task analytics"""
        insights = self.task_predictor.get_insights()
        self.update_output(f"\n📊 TASK ANALYTICS\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        for insight in insights:
            self.update_output(f"• {insight}\n", "info")

    def check_energy_level(self):
        """Check current energy level"""
        energy = self.energy_tracker.get_current_energy()
        self.update_output(f"\n🔋 CURRENT ENERGY LEVEL\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        self.update_output(f"Level: {energy['level']:.0f}/100 {energy['emoji']}\n", "info")
        self.update_output(f"Status: {energy['category']}\n", "success")
        self.update_output(f"Trend: {energy['trend']}\n", "info")
        if energy.get('suggestion'):
            self.update_output(f"\n💡 {energy['suggestion']}\n", "command")

    def view_energy_trends(self):
        """View energy trends"""
        trends = self.energy_tracker.get_daily_summary()
        self.update_output(f"\n📈 ENERGY TRENDS\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        self.update_output(f"Average Energy: {trends['average_energy']:.0f}/100\n", "info")
        self.update_output(f"Peak Time: {trends['peak_hour']}:00\n", "success")
        self.update_output(f"Low Time: {trends['low_hour']}:00\n", "info")

    def get_break_suggestion(self):
        """Get AI break suggestion"""
        suggestion = self.break_suggester.should_take_break()
        self.update_output(f"\n🎯 BREAK SUGGESTION\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        self.update_output(f"{suggestion['message']}\n", "info")
        if suggestion['should_break']:
            self.update_output(f"\n💡 Suggested break type: {suggestion['break_type']}\n", "command")
            self.update_output(f"Duration: {suggestion['duration']} minutes\n", "info")

    def check_distractions(self):
        """Check for distractions"""
        result = self.distraction_detector.detect_distraction()
        self.update_output(f"\n⚠️ DISTRACTION CHECK\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        if result['is_distracted']:
            self.update_output(f"Status: Distracted ⚠️\n", "error")
            self.update_output(f"App: {result['app']}\n", "info")
            self.update_output(f"Category: {result['category']}\n", "info")
        else:
            self.update_output(f"Status: Focused ✅\n", "success")

    def view_focus_report(self):
        """View focus report"""
        report = self.distraction_detector.get_daily_report()
        self.update_output(f"\n📊 FOCUS REPORT\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        self.update_output(f"Distractions Today: {report['distractions_today']}\n", "info")
        self.update_output(f"Focus Time: {report['focus_time']} minutes\n", "success")
        self.update_output(f"Distraction Time: {report['distraction_time']} minutes\n", "error")

    def view_productivity_dashboard(self):
        """View complete productivity dashboard"""
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard()
        self.update_output(f"\n📊 PRODUCTIVITY DASHBOARD\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        self.update_output(f"Period: {dashboard['period']}\n", "info")
        overview = dashboard['overview']
        self.update_output(f"\nWork Sessions: {overview['total_work_sessions']}\n", "info")
        self.update_output(f"Tasks Completed: {overview['total_tasks_completed']}\n", "info")
        self.update_output(f"Productivity Score: {overview['productivity_score']:.0f}/100\n", "success")

    def view_weekly_summary(self):
        """View weekly summary"""
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard(days=7)
        self.update_output(f"\n📅 WEEKLY SUMMARY\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        time_analysis = dashboard['time_analysis']
        if not time_analysis.get('no_data'):
            self.update_output(f"Total Work Time: {time_analysis['total_work_minutes']} minutes\n", "info")
            self.update_output(f"Daily Average: {time_analysis['avg_work_minutes_per_day']:.0f} minutes\n", "info")
            self.update_output(f"Most Productive Hour: {time_analysis['most_productive_hour']}:00\n", "success")

    def view_productivity_trends(self):
        """View productivity trends"""
        self.update_output(f"\n📈 PRODUCTIVITY TRENDS\n", "success")
        self.update_output(f"Analyzing your productivity patterns...\n", "info")
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard(days=30)
        for rec in dashboard['recommendations']:
            self.update_output(f"💡 {rec}\n", "command")

    def get_productivity_recommendations(self):
        """Get productivity recommendations"""
        dashboard = self.productivity_dashboard.get_comprehensive_dashboard()
        self.update_output(f"\n🎯 PRODUCTIVITY RECOMMENDATIONS\n", "success")
        self.update_output(f"{'=' * 60}\n", "info")
        for i, rec in enumerate(dashboard['recommendations'], 1):
            self.update_output(f"{i}. {rec}\n", "info")

    # ===== TOOLS & UTILITIES METHODS =====

    def add_password_dialog(self):
        """Add new password to vault"""
        name = self.show_input_dialog("Service Name", "Service name (e.g., Gmail, GitHub):")
        if name:
            username = self.show_input_dialog("Username", "Username or email:")
            password = self.show_input_dialog("Password", "Password:")
            url = self.show_input_dialog("URL (Optional)", "Service URL:", "")
            if username and password:
                result = self.password_vault.add_password(name, username, password, url)
                self.update_output(result, "success")

    def view_password_dialog(self):
        """View a password from vault"""
        name = self.show_input_dialog("Service Name", "Which service password to view?")
        if name:
            result = self.password_vault.get_password(name)
            self.update_output(result, "info")

    def list_passwords(self):
        """List all saved passwords"""
        result = self.password_vault.list_passwords()
        self.update_output(result, "info")

    def generate_password(self):
        """Generate a secure password"""
        length = self.show_input_dialog("Password Length", "Length (8-32 characters):", "16")
        try:
            length = int(length) if length else 16
            result = self.password_vault.generate_secure_password(length)
            self.update_output(result, "success")
        except:
            self.update_output("❌ Invalid length\n", "error")

    def add_note_dialog(self):
        """Add a new note"""
        content = self.show_input_dialog("Note Content", "Enter your note:")
        if content:
            category = self.show_input_dialog("Category", "Category (optional):", "general")
            result = self.notes.add_note(content, category or "general")
            self.update_output(result, "success")

    def list_notes(self):
        """List all notes"""
        result = self.notes.list_notes()
        self.update_output(result, "info")

    def search_notes_dialog(self):
        """Search notes"""
        query = self.show_input_dialog("Search Notes", "Search term:")
        if query:
            result = self.notes.search_notes(query)
            self.update_output(result, "info")

    def view_pinned_notes(self):
        """View pinned notes"""
        result = self.notes.get_pinned_notes()
        self.update_output(result, "info")

    def add_event_dialog(self):
        """Add a calendar event"""
        title = self.show_input_dialog("Event Title", "Event name:")
        if title:
            date = self.show_input_dialog("Date", "Date (YYYY-MM-DD):")
            time = self.show_input_dialog("Time (Optional)", "Time (HH:MM):", "")
            if date:
                result = self.calendar.add_event(title, date, time)
                self.update_output(result, "success")

    def view_today_events(self):
        """View today's events"""
        result = self.calendar.get_today_events()
        self.update_output(result, "info")

    def view_week_events(self):
        """View this week's events"""
        result = self.calendar.get_week_events()
        self.update_output(result, "info")

    def view_reminders(self):
        """View upcoming reminders"""
        result = self.calendar.get_upcoming_reminders()
        self.update_output(result, "info")

    def get_weather_dialog(self):
        """Get weather for a city"""
        city = self.show_input_dialog("City", "Enter city name:", "New York")
        if city:
            result = self.weather_news.get_weather(city)
            self.update_output(result, "info")

    def get_forecast(self):
        """Get weather forecast"""
        city = self.show_input_dialog("City", "Enter city name:", "New York")
        if city:
            result = self.weather_news.get_forecast(city, days=3)
            self.update_output(result, "info")

    def get_news(self):
        """Get latest news"""
        result = self.weather_news.get_news_headlines("general", 5)
        self.update_output(result, "info")

    def get_tech_news(self):
        """Get tech news"""
        result = self.weather_news.get_news_headlines("technology", 5)
        self.update_output(result, "info")

    def translate_text_dialog(self):
        """Translate text"""
        text = self.show_input_dialog("Text to Translate", "Enter text:")
        if text:
            target = self.show_input_dialog("Target Language", "Language code (e.g., es, fr, de):", "es")
            if target:
                result = self.translator.translate(text, target)
                self.update_output(result, "info")

    def detect_language_dialog(self):
        """Detect text language"""
        text = self.show_input_dialog("Text", "Enter text to detect language:")
        if text:
            result = self.translator.detect_language(text)
            self.update_output(result, "info")

    def show_supported_languages(self):
        """Show supported languages"""
        result = self.translator.get_supported_languages()
        self.update_output(result, "info")

    def auto_desktop_sync(self):
        """Auto-initialize desktop sync on GUI startup - Scans and stores desktop data"""
        import time
        time.sleep(2)  # Wait for GUI to fully load

        try:
            self.update_output("\n" + "=" * 60 + "\n", "info")
            self.update_output("🚀 DESKTOP FILE & FOLDER AUTOMATOR - STARTING\n", "command")
            self.update_output("=" * 60 + "\n", "info")

            # Create Desktop Sync Manager instance
            manager = DesktopSyncManager()

            # Step 1: Scan the desktop
            self.update_output("\n🔍 Scanning your desktop...\n", "command")
            scan_result = manager.scan_desktop()

            if not scan_result["success"]:
                self.update_output(f"❌ Error: {scan_result['message']}\n", "error")
                return

            scan_data = scan_result["data"]
            stats = scan_data["statistics"]

            # Step 2: Display summary in GUI
            self.update_output("\n📊 DESKTOP ANALYSIS SUMMARY\n", "success")
            self.update_output("=" * 60 + "\n", "info")
            self.update_output(f"📂 Desktop Location: {scan_data['desktop_path']}\n", "info")
            self.update_output(
                f"📅 Scanned: {datetime.fromisoformat(scan_data['scan_time']).strftime('%Y-%m-%d %H:%M:%S')}\n\n",
                "info")

            self.update_output(f"📁 Total Folders: {stats['total_folders']}\n", "info")
            self.update_output(f"📄 Total Files: {stats['total_files']}\n", "info")

            # Format file size
            total_size = stats['total_size_bytes']
            size_str = manager.format_size(total_size)
            self.update_output(f"💾 Total Size: {size_str}\n", "info")

            # Show file types
            if stats["file_types"]:
                self.update_output(f"\n📑 File Types Found:\n", "command")
                for ext, count in sorted(stats["file_types"].items(), key=lambda x: x[1], reverse=True)[:10]:
                    ext_display = ext if ext != "no_extension" else "(no extension)"
                    self.update_output(f"   {ext_display}: {count} file(s)\n", "info")

            # Show top folders
            if scan_data["folders"]:
                self.update_output(f"\n📂 Folders on Desktop:\n", "command")
                for folder in scan_data["folders"][:10]:
                    self.update_output(f"   • {folder['name']} ({folder['item_count']} items)\n", "info")
                if len(scan_data["folders"]) > 10:
                    self.update_output(f"   ... and {len(scan_data['folders']) - 10} more folders\n", "info")

            # Step 3: Save the data
            self.update_output("\n💾 Saving desktop data...\n", "command")
            save_result = manager.save_desktop_data(scan_data)

            if save_result["success"]:
                self.update_output(f"✅ Data saved to: {save_result['file']}\n", "success")
            else:
                self.update_output(f"⚠️  Could not save data: {save_result['message']}\n", "error")

            # Step 4: Check batch file
            batch_result = manager.prepare_batch_file_download()
            if batch_result["success"]:
                self.update_output("\n📥 BATCH FILE READY:\n", "success")
                self.update_output(f"   Location: {batch_result['batch_file']}\n", "info")
                if manager.is_windows:
                    self.update_output("   🚀 Double-click to launch desktop automation!\n", "info")
                else:
                    self.update_output("   📥 Download to your Windows PC to use\n", "info")
            else:
                self.update_output("\n📥 BATCH FILE SETUP:\n", "command")
                self.update_output("   Download 'desktop_file_controller.bat' from Replit\n", "info")
                self.update_output(f"   Place in: {manager.script_dir}\n", "info")

            self.update_output("\n" + "=" * 60 + "\n", "info")
            self.update_output("✅ DESKTOP SCAN COMPLETE!\n", "success")
            self.update_output("💡 All desktop data has been analyzed and saved\n", "info")
            self.update_output("🗂️  Use the Desktop tab buttons to manage your files\n", "info")
            self.update_output("=" * 60 + "\n\n", "info")

        except Exception as e:
            self.update_output(f"\n⚠️  Desktop sync error: {str(e)}\n", "error")
            import traceback
            self.update_output(f"Details: {traceback.format_exc()}\n", "error")

    # ==================== Comprehensive Controller Methods ====================

    def load_comprehensive_command(self, command):
        """Load a predefined command into the input"""
        self.comprehensive_input.delete(0, tk.END)
        self.comprehensive_input.insert(0, command)
        self.comprehensive_input.focus()

    def show_quick_actions_menu(self):
        """Show the main quick actions menu"""
        self.quick_feature_view.pack_forget()
        self.quick_menu_view.pack(fill="both", expand=True)

    def toggle_sidebar(self):
        """Toggle sidebar expanded/collapsed state"""
        if self.sidebar_expanded:
            # Collapse sidebar
            self.sidebar.config(width=50)
            self.sidebar_toggle_btn.config(text="▶")
            self.sidebar_title.pack_forget()

            # Update button text to show only icons
            for btn, name, color in self.sidebar_buttons:
                icon = [c for c in self.sidebar_categories if c[1] == name][0][0]
                btn.config(text=icon, width=3)

            self.sidebar_expanded = False
        else:
            # Expand sidebar
            self.sidebar.config(width=120)
            self.sidebar_toggle_btn.config(text="◀")
            self.sidebar_title.pack(pady=(5, 10))

            # Restore full text
            for btn, name, color in self.sidebar_buttons:
                icon = [c for c in self.sidebar_categories if c[1] == name][0][0]
                btn.config(text=f"{icon}\n{name}", width=10)

            self.sidebar_expanded = True

    def scroll_to_category(self, category):
        """Scroll to and highlight a specific category"""
        # Update active category highlighting
        for btn, name, color in self.sidebar_buttons:
            if name == category:
                btn.config(bg="#45475a", relief="solid", bd=2)
                self.active_sidebar_category = category
            else:
                btn.config(bg="#313244", relief="flat", bd=0)

        # Map category names to quick actions headers
        category_map = {
            "SYSTEM": "🖥️ SYSTEM",
            "WEB": "🌐 WEB & APPS",
            "WORK": "📁 PRODUCTIVITY",
            "MEDIA": "🎵 MEDIA"
        }

        target_header = category_map.get(category, "")

        # Scroll to the category header
        if target_header in self.category_headers:
            header_widget = self.category_headers[target_header]
            # Get the y position of the header
            try:
                self.menu_canvas.update_idletasks()
                # Get the widget's bbox
                bbox = self.menu_canvas.bbox("all")
                if bbox:
                    # Calculate position
                    y_pos = header_widget.winfo_y()
                    canvas_height = self.menu_canvas.winfo_height()
                    scroll_region = bbox[3]  # Total height

                    if scroll_region > canvas_height:
                        # Scroll to position
                        fraction = y_pos / scroll_region
                        self.menu_canvas.yview_moveto(fraction)
            except Exception as e:
                print(f"Scroll error: {e}")

    def show_quick_action_feature(self, title, description, color, feature_id):
        """Show the selected quick action feature"""
        # Hide menu, show feature view
        self.quick_menu_view.pack_forget()
        self.quick_feature_view.pack(fill="both", expand=True)

        # Update title
        self.feature_title.config(text=title, fg=color)

        # Clear previous content
        for widget in self.feature_content.winfo_children():
            widget.destroy()

        # Create feature-specific content
        content_inner = tk.Frame(self.feature_content, bg="#181825")
        content_inner.pack(fill="both", expand=True, padx=15, pady=15)

        # Description
        desc_label = tk.Label(content_inner,
                              text=description,
                              bg="#181825",
                              fg="#a6adc8",
                              font=("Segoe UI", 10),
                              wraplength=350)
        desc_label.pack(pady=(0, 20))

        # Feature-specific content
        if feature_id == "screenshot":
            self.create_screenshot_feature(content_inner, color)
        elif feature_id == "lock":
            self.create_lock_feature(content_inner, color)
        elif feature_id == "taskmanager":
            self.create_taskmanager_feature(content_inner, color)
        elif feature_id == "chrome":
            self.create_chrome_feature(content_inner, color)
        elif feature_id == "google":
            self.create_google_feature(content_inner, color)
        elif feature_id == "gmail":
            self.create_gmail_feature(content_inner, color)
        elif feature_id == "whatsapp":
            self.create_whatsapp_feature(content_inner, color)
        elif feature_id == "vscode":
            self.create_vscode_feature(content_inner, color)
        elif feature_id == "explorer":
            self.create_explorer_feature(content_inner, color)
        elif feature_id == "notepad":
            self.create_notepad_feature(content_inner, color)
        elif feature_id == "spotify":
            self.create_spotify_feature(content_inner, color)
        elif feature_id == "youtube":
            self.create_youtube_feature(content_inner, color)
        elif feature_id == "volume":
            self.create_volume_feature(content_inner, color)
        elif feature_id == "workflow_builder":
            self.create_workflow_builder_feature(content_inner, color)
        elif feature_id == "macro_recorder":
            self.create_macro_recorder_feature(content_inner, color)
        elif feature_id == "mobile_control":
            self.create_mobile_control_feature(content_inner, color)

    def create_workflow_builder_feature(self, parent, color):
        """Create workflow builder feature UI"""
        tk.Label(parent, text="💬 Workflow Builder", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        info_text = "Build complex automation workflows using plain English. The AI will convert your descriptions into executable steps."
        tk.Label(parent, text=info_text, bg="#181825", fg="#a6adc8",
                 font=("Segoe UI", 9), wraplength=350, justify="left").pack(pady=(0, 20))

        btn = tk.Button(parent, text="💬 Open Workflow Builder",
                        bg=color, fg="#0f0f1e",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=self.show_workflow_builder,
                        padx=30, pady=12)
        btn.pack(pady=10)

    def create_macro_recorder_feature(self, parent, color):
        """Create macro recorder feature placeholder"""
        tk.Label(parent, text="🎬 Macro Recorder", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))
        tk.Label(parent, text="Record and playback mouse & keyboard actions",
                 bg="#181825", fg="#a6adc8", font=("Segoe UI", 9)).pack(pady=(0, 20))
        tk.Label(parent, text="Use the Macro Recorder tab for full access",
                 bg="#181825", fg="#6c7086", font=("Segoe UI", 9, "italic")).pack()

    def create_mobile_control_feature(self, parent, color):
        """Create mobile control feature placeholder"""
        tk.Label(parent, text="📱 Mobile Control", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))
        tk.Label(parent, text="Control your desktop from mobile devices",
                 bg="#181825", fg="#a6adc8", font=("Segoe UI", 9)).pack(pady=(0, 20))
        tk.Label(parent, text="Use the Mobile Companion tab for full access",
                 bg="#181825", fg="#6c7086", font=("Segoe UI", 9, "italic")).pack()

    def create_screenshot_feature(self, parent, color):
        """Create screenshot feature UI"""
        tk.Label(parent, text="📸 Screenshot Options", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📷 Capture Full Screen", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Take a screenshot"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

        btn2 = tk.Button(parent, text="🖼️ Capture Window", bg="#313244", fg="#cdd6f4",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Take screenshot of active window"),
                         padx=20, pady=12)
        btn2.pack(fill="x", pady=5)
        self.add_hover_effect(btn2, "#313244", "#45475a")

    def create_lock_feature(self, parent, color):
        """Create lock PC feature UI"""
        tk.Label(parent, text="🔒 System Lock", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        tk.Label(parent, text="⚠️ This will lock your computer", bg="#181825", fg="#fab387",
                 font=("Segoe UI", 9)).pack(pady=5)

        btn = tk.Button(parent, text="🔒 Lock Computer Now", bg="#f38ba8", fg="#0f0f1e",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Lock the computer"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=10)
        self.add_hover_effect(btn, "#f38ba8", "#f5c2e7")

    def create_taskmanager_feature(self, parent, color):
        """Create task manager feature UI"""
        tk.Label(parent, text="📊 Task Manager", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📊 Open Task Manager", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Task Manager"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_chrome_feature(self, parent, color):
        """Create Chrome feature UI"""
        tk.Label(parent, text="🌍 Chrome Browser", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="🌍 Open Chrome", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Chrome and go to Google"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_google_feature(self, parent, color):
        """Create Google search feature UI"""
        tk.Label(parent, text="🔍 Google Search", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        search_entry = tk.Entry(parent, bg="#313244", fg="#ffffff", font=("Segoe UI", 10),
                                relief="flat", insertbackground="#f9e2af")
        search_entry.insert(0, "Python tutorials")
        search_entry.pack(fill="x", pady=5, ipady=8)

        btn = tk.Button(parent, text="🔍 Search Google", bg="#a6e3a1", fg="#0f0f1e",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command(f"Search Google for {search_entry.get()}"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=10)
        self.add_hover_effect(btn, "#a6e3a1", "#94e2d5")

    def create_gmail_feature(self, parent, color):
        """Create Gmail feature UI"""
        tk.Label(parent, text="📧 Gmail", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📧 Open Gmail", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Gmail in browser"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_whatsapp_feature(self, parent, color):
        """Create WhatsApp feature UI"""
        tk.Label(parent, text="💬 WhatsApp", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="💬 Open WhatsApp Web", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open WhatsApp Web"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_vscode_feature(self, parent, color):
        """Create VS Code feature UI"""
        tk.Label(parent, text="📝 VS Code", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📝 Launch VS Code", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Launch VS Code"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_explorer_feature(self, parent, color):
        """Create File Explorer feature UI"""
        tk.Label(parent, text="📂 File Explorer", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="📂 Open File Explorer", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open File Explorer"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_notepad_feature(self, parent, color):
        """Create Notepad feature UI"""
        tk.Label(parent, text="🗒️ Notepad", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="🗒️ Open Notepad", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open Notepad"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_spotify_feature(self, parent, color):
        """Create Spotify feature UI"""
        tk.Label(parent, text="🎵 Spotify", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="🎵 Launch Spotify", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Launch Spotify"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_youtube_feature(self, parent, color):
        """Create YouTube feature UI"""
        tk.Label(parent, text="🎬 YouTube", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn = tk.Button(parent, text="🎬 Open YouTube", bg="#313244", fg="#cdd6f4",
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                        command=lambda: self.load_comprehensive_command("Open YouTube"),
                        padx=20, pady=12)
        btn.pack(fill="x", pady=5)
        self.add_hover_effect(btn, "#313244", "#45475a")

    def create_volume_feature(self, parent, color):
        """Create Volume control feature UI"""
        tk.Label(parent, text="🔊 Volume Control", bg="#181825", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        btn1 = tk.Button(parent, text="🔊 Volume Up", bg="#313244", fg="#cdd6f4",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Increase volume by 10%"),
                         padx=20, pady=12)
        btn1.pack(fill="x", pady=5)
        self.add_hover_effect(btn1, "#313244", "#45475a")

        btn2 = tk.Button(parent, text="🔉 Volume Down", bg="#313244", fg="#cdd6f4",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Decrease volume by 10%"),
                         padx=20, pady=12)
        btn2.pack(fill="x", pady=5)
        self.add_hover_effect(btn2, "#313244", "#45475a")

        btn3 = tk.Button(parent, text="🔇 Mute", bg="#f38ba8", fg="#0f0f1e",
                         font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                         command=lambda: self.load_comprehensive_command("Mute system volume"),
                         padx=20, pady=12)
        btn3.pack(fill="x", pady=5)
        self.add_hover_effect(btn3, "#f38ba8", "#f5c2e7")

    def append_comprehensive_output(self, text, tag=None):
        """Append text to the comprehensive output display"""
        self.comprehensive_output.config(state='normal')
        if tag:
            self.comprehensive_output.insert(tk.END, text, tag)
        else:
            self.comprehensive_output.insert(tk.END, text)
        self.comprehensive_output.see(tk.END)
        self.comprehensive_output.config(state='disabled')
        self.root.update_idletasks()

    def clear_comprehensive_output(self):
        """Clear the comprehensive output display"""
        self.comprehensive_output.config(state='normal')
        self.comprehensive_output.delete(1.0, tk.END)
        self.comprehensive_output.config(state='disabled')

        # Reset welcome message
        self.append_comprehensive_output("=" * 60 + "\n", "info")
        self.append_comprehensive_output("🎯 COMPREHENSIVE DESKTOP CONTROLLER\n", "highlight")
        self.append_comprehensive_output("=" * 60 + "\n", "info")
        self.append_comprehensive_output("\n✅ Output cleared. Ready for new command!\n\n", "success")

    def update_comprehensive_phase(self, phase_name, status="active"):
        """Update the visual indicator for current phase"""
        colors = {
            "active": "#f9e2af",
            "complete": "#a6e3a1",
            "inactive": "#6c7086"
        }

        if phase_name in self.phase_labels:
            color = colors.get(status, colors["inactive"])
            self.phase_labels[phase_name].config(fg=color)

    def execute_comprehensive_command(self):
        """Execute a comprehensive desktop control command"""
        command = self.comprehensive_input.get().strip()

        if not command:
            messagebox.showwarning("Empty Command", "Please enter a command first!")
            return

        if not self.comprehensive_controller:
            self.append_comprehensive_output("\n⚠️  Comprehensive Controller not available\n", "error")
            self.append_comprehensive_output("This feature requires local execution with display access.\n", "info")
            self.append_comprehensive_output("Download and run locally for full functionality.\n", "info")
            return

        # Clear previous output
        self.comprehensive_output.config(state='normal')
        self.comprehensive_output.delete(1.0, tk.END)
        self.comprehensive_output.config(state='disabled')

        # Update status
        self.comprehensive_status.config(text="⚙️ Processing...", fg="#f9e2af")

        # Run in thread
        thread = threading.Thread(target=self._execute_comprehensive_task, args=(command,), daemon=True)
        thread.start()

    def _execute_comprehensive_task(self, command):
        """Execute comprehensive task in background thread"""
        try:
            self.append_comprehensive_output("=" * 60 + "\n", "info")
            self.append_comprehensive_output("🎯 COMPREHENSIVE DESKTOP CONTROLLER\n", "highlight")
            self.append_comprehensive_output("=" * 60 + "\n", "info")
            self.append_comprehensive_output(f"Command: {command}\n\n", "info")

            # Phase 1: Understand
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.append_comprehensive_output("🧠 PHASE 1: UNDERSTANDING PROMPT\n", "phase1")
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.update_comprehensive_phase("UNDERSTAND", "active")

            understanding = self.comprehensive_controller.understand_prompt(command)

            self.append_comprehensive_output("\n✅ Prompt Analysis Complete:\n", "success")
            self.append_comprehensive_output(f"   🎯 Goal: {understanding.get('primary_goal', 'N/A')}\n", "info")
            self.append_comprehensive_output(f"   📊 Complexity: {understanding.get('complexity_level', 'N/A')}\n",
                                             "info")
            self.append_comprehensive_output(
                f"   ⏱️  Estimated Time: {understanding.get('estimated_duration', 'N/A')}s\n", "info")
            apps = understanding.get('required_applications', [])
            if apps:
                self.append_comprehensive_output(f"   🔧 Required Apps: {', '.join(apps)}\n", "info")

            self.update_comprehensive_phase("UNDERSTAND", "complete")

            # Phase 2: Break Down
            self.append_comprehensive_output("\n" + "━" * 60 + "\n", "info")
            self.append_comprehensive_output("📋 PHASE 2: BREAKING INTO STEPS\n", "phase2")
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.update_comprehensive_phase("PLAN", "active")

            execution_plan = self.comprehensive_controller.break_into_steps(understanding)
            steps = execution_plan.get("execution_plan", {}).get("steps", [])

            self.append_comprehensive_output("\n✅ Execution Plan Created:\n", "success")
            self.append_comprehensive_output(f"   Total Steps: {len(steps)}\n", "info")
            self.append_comprehensive_output(
                f"   Estimated Time: {execution_plan.get('execution_plan', {}).get('estimated_time', 'N/A')}s\n\n",
                "info")

            self.append_comprehensive_output("📝 Step Breakdown:\n", "highlight")
            for step in steps:
                self.append_comprehensive_output(f"   {step['step_number']}. {step.get('description', 'N/A')}\n",
                                                 "info")
                self.append_comprehensive_output(f"      → Expected: {step.get('expected_outcome', 'N/A')}\n", "info")

            self.update_comprehensive_phase("PLAN", "complete")

            # Phase 3: Monitor & Execute
            self.append_comprehensive_output("\n" + "━" * 60 + "\n", "info")
            self.append_comprehensive_output("👁️  PHASE 3: EXECUTING WITH MONITORING\n", "phase3")
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.update_comprehensive_phase("MONITOR", "active")

            if self.comprehensive_controller.gui.demo_mode:
                self.append_comprehensive_output("\n⚠️  DEMO MODE: Commands will be simulated\n", "error")
                self.append_comprehensive_output("Download and run locally for actual execution\n\n", "info")

            # Execute each step
            for i, step in enumerate(steps, 1):
                self.append_comprehensive_output(f"\nStep {i}/{len(steps)}: {step.get('description', 'N/A')}\n",
                                                 "highlight")

                if self.comprehensive_controller.gui.demo_mode:
                    self.append_comprehensive_output(f"   [DEMO] Would execute: {step.get('action_type', 'N/A')}\n",
                                                     "info")
                    import time
                    time.sleep(0.5)
                    self.append_comprehensive_output("   ✅ Demo step completed\n", "success")
                else:
                    # Real execution with monitoring
                    result = self.comprehensive_controller.monitor_screen_during_execution(step, i)
                    if result.get("success"):
                        self.append_comprehensive_output("   ✅ Step completed successfully\n", "success")
                    else:
                        self.append_comprehensive_output("   ⚠️  Step failed\n", "error")

            self.update_comprehensive_phase("MONITOR", "complete")

            # Summary
            self.append_comprehensive_output("\n" + "━" * 60 + "\n", "info")
            self.append_comprehensive_output("📊 EXECUTION SUMMARY\n", "highlight")
            self.append_comprehensive_output("━" * 60 + "\n", "info")
            self.append_comprehensive_output(f"\n✅ All phases completed!\n", "success")
            self.append_comprehensive_output(f"   Total Steps: {len(steps)}\n", "info")

            if self.comprehensive_controller.gui.demo_mode:
                self.append_comprehensive_output("\n💡 TIP: Download and run locally for full automation\n", "info")

            self.append_comprehensive_output("\n" + "=" * 60 + "\n", "info")

            # Update status
            self.comprehensive_status.config(text="✅ Completed", fg="#a6e3a1")

        except Exception as e:
            self.append_comprehensive_output(f"\n❌ Error: {str(e)}\n", "error")
            self.comprehensive_status.config(text="❌ Error", fg="#f38ba8")

    def show_comprehensive_guide(self):
        """Show comprehensive controller guide"""
        guide_text = """
🎯 COMPREHENSIVE DESKTOP CONTROLLER GUIDE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW IT WORKS:

🧠 Phase 1: UNDERSTAND
   • Analyzes your prompt deeply
   • Identifies intent, complexity, requirements
   • Predicts obstacles and plans mitigation

📋 Phase 2: BREAK DOWN
   • Creates detailed step-by-step execution plan
   • Defines validation checkpoints
   • Plans error recovery strategies

👁️  Phase 3: MONITOR & EXECUTE
   • Takes screenshots before each step
   • Executes the action
   • Takes screenshots after each step
   • AI verifies expected vs actual outcome

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE COMMANDS:

Simple:
  • "Take a screenshot"
  • "Open Chrome"

For full functionality, download and run locally!
"""
        messagebox.showinfo("Comprehensive Controller Guide", guide_text)

    # ==================== Virtual Language Model Methods ====================

    def vlm_append_output(self, text, tag=None):
        """Append text to VLM output display"""
        self.vlm_output.config(state='normal')
        if tag:
            self.vlm_output.insert(tk.END, text, tag)
        else:
            self.vlm_output.insert(tk.END, text)
        self.vlm_output.see(tk.END)
        self.vlm_output.config(state='disabled')
        self.root.update_idletasks()

    def vlm_clear_output(self):
        """Clear VLM output"""
        self.vlm_output.config(state='normal')
        self.vlm_output.delete(1.0, tk.END)
        self.vlm_output.config(state='disabled')

        self.vlm_append_output("=" * 60 + "\n", "info")
        self.vlm_append_output("🧠 Output cleared. Ready for new learning!\n", "success")
        self.vlm_append_output("=" * 60 + "\n", "info")

    def vlm_refresh_stats(self):
        """Refresh and display VLM statistics"""
        if not self.vlm:
            return

        stats = self.vlm.get_stats()

        self.vlm_stats_display.config(state='normal')
        self.vlm_stats_display.delete(1.0, tk.END)

        stats_text = (
            f"📊 Observations: {stats['observations']}\n"
            f"🎨 UI Patterns: {stats['ui_patterns']}\n"
            f"💻 Known Apps: {stats['known_applications']}\n"
            f"📋 Workflows: {stats['learned_workflows']}\n"
            f"✅ Success Rate: {stats['success_rate']:.1f}%"
        )

        self.vlm_stats_display.insert(1.0, stats_text.strip())
        self.vlm_stats_display.config(state='disabled')

        # Update knowledge display
        self.vlm_knowledge_display.config(state='normal')
        self.vlm_knowledge_display.delete(1.0, tk.END)
        self.vlm_knowledge_display.insert(1.0, stats['knowledge_summary'])
        self.vlm_knowledge_display.config(state='disabled')

    def vlm_observe(self):
        """Let VLM observe the current screen"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        self.vlm_status.config(text="👁️ Observing...", fg="#89b4fa")
        self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
        self.vlm_append_output("👁️ OBSERVING SCREEN\n", "highlight")
        self.vlm_append_output("━" * 60 + "\n", "info")

        # Run in thread
        thread = threading.Thread(target=self._vlm_observe_thread, daemon=True)
        thread.start()

    def _vlm_observe_thread(self):
        """Observe in background thread"""
        try:
            result = self.vlm.observe_screen("user requested observation")

            if result.get("demo"):
                self.vlm_append_output("\n⚠️ DEMO MODE\n", "error")
                self.vlm_append_output("Screen observation requires display access.\n", "info")
                self.vlm_append_output("Download and run locally for full functionality.\n\n", "info")
            elif result.get("success"):
                analysis = result.get("analysis", {})

                self.vlm_append_output("\n✅ Observation Complete!\n\n", "success")
                self.vlm_append_output(f"📝 Description: {analysis.get('description', 'N/A')}\n", "info")
                self.vlm_append_output(f"🎨 UI Elements Found: {len(analysis.get('ui_elements', []))}\n", "info")

                apps = analysis.get('visible_applications', [])
                if apps:
                    self.vlm_append_output(f"💻 Applications: {', '.join(apps)}\n", "info")

                self.vlm_append_output(f"\n💡 Learning Insights:\n", "highlight")
                self.vlm_append_output(f"{analysis.get('learning_insights', 'N/A')}\n", "info")
            else:
                self.vlm_append_output("\n❌ Observation failed\n", "error")
                self.vlm_append_output(f"Error: {result.get('message', 'Unknown error')}\n", "info")

            self.vlm_append_output("━" * 60 + "\n", "info")
            self.vlm_refresh_stats()
            self.vlm_status.config(text="✅ Ready to Learn", fg="#a6e3a1")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#f38ba8")

    def vlm_decide(self):
        """Let VLM decide an action"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        goal = self.vlm_goal_input.get().strip()

        if not goal:
            messagebox.showwarning("No Goal", "Please enter a goal first!")
            return

        self.vlm_status.config(text="🤔 Deciding...", fg="#f9e2af")
        self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
        self.vlm_append_output("🤔 MAKING DECISION\n", "decision")
        self.vlm_append_output("━" * 60 + "\n", "info")
        self.vlm_append_output(f"Goal: {goal}\n\n", "info")

        # Run in thread
        thread = threading.Thread(target=self._vlm_decide_thread, args=(goal,), daemon=True)
        thread.start()

    def _vlm_decide_thread(self, goal):
        """Decide in background thread"""
        try:
            decision = self.vlm.decide_action(goal)

            self.vlm_append_output("✅ Decision Made!\n\n", "success")
            self.vlm_append_output(f"🎯 Action: {decision.get('action', 'N/A')}\n", "decision")
            self.vlm_append_output(f"📍 Target: {decision.get('target', 'N/A')}\n", "info")
            self.vlm_append_output(f"💭 Reasoning: {decision.get('reasoning', 'N/A')}\n", "info")
            self.vlm_append_output(f"📊 Confidence: {decision.get('confidence', 0):.2%}\n", "info")

            alternatives = decision.get('alternative_actions', [])
            if alternatives:
                self.vlm_append_output(f"\n🔄 Alternatives: {', '.join(alternatives)}\n", "info")

            self.vlm_append_output("\n💡 Click 'Execute' to perform this action!\n", "highlight")
            self.vlm_append_output("━" * 60 + "\n", "info")

            # Store decision for execution
            self.vlm_last_decision = decision

            self.vlm_status.config(text="✅ Decision Ready", fg="#a6e3a1")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#f38ba8")

    def vlm_execute(self):
        """Execute the last decided action"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        goal = self.vlm_goal_input.get().strip()

        if not goal:
            messagebox.showwarning("No Goal", "Please enter a goal first!")
            return

        self.vlm_status.config(text="▶️ Executing...", fg="#a6e3a1")

        # Run in thread
        thread = threading.Thread(target=self._vlm_execute_thread, args=(goal,), daemon=True)
        thread.start()

    def _vlm_execute_thread(self, goal):
        """Execute in background thread"""
        try:
            self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
            self.vlm_append_output("▶️ EXECUTING LEARNED ACTION\n", "success")
            self.vlm_append_output("━" * 60 + "\n", "info")

            # First decide the action
            self.vlm_append_output("🤔 Analyzing goal and deciding action...\n", "info")
            decision = self.vlm.decide_action(goal)

            self.vlm_append_output(f"✅ Decision: {decision.get('action', 'N/A')}\n", "decision")
            self.vlm_append_output(f"   Confidence: {decision.get('confidence', 0):.2%}\n\n", "info")

            # Execute the action
            self.vlm_append_output("⚙️ Executing action...\n", "info")
            result = self.vlm.execute_learned_action(decision)

            if result.get("demo"):
                self.vlm_append_output("\n⚠️ DEMO MODE\n", "error")
                self.vlm_append_output("Desktop control requires local execution.\n", "info")
                self.vlm_append_output(f"Simulated: {result.get('message', 'N/A')}\n", "info")
            elif result.get("success"):
                self.vlm_append_output("\n✅ Action Executed Successfully!\n", "success")
                self.vlm_append_output(f"Result: {result.get('message', 'N/A')}\n", "info")
            else:
                self.vlm_append_output("\n⚠️ Action Failed\n", "error")
                self.vlm_append_output(f"Error: {result.get('message', 'Unknown error')}\n", "info")

            self.vlm_append_output("━" * 60 + "\n", "info")

            self.vlm_refresh_stats()
            self.vlm_status.config(text="✅ Ready to Learn", fg="#a6e3a1")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#f38ba8")

    def vlm_learn_session(self):
        """Run an autonomous learning session"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        # Ask for duration
        duration = simpledialog.askinteger(
            "Learning Session",
            "How many minutes should the AI explore and learn?",
            initialvalue=3,
            minvalue=1,
            maxvalue=30
        )

        if not duration:
            return

        if messagebox.askyesno(
                "Start Learning Session",
                f"The AI will autonomously explore and learn for {duration} minute(s).\n\n"
                "It will:\n"
                "• Observe the screen\n"
                "• Identify UI patterns\n"
                "• Learn workflows\n"
                "• Make test actions\n\n"
                "Continue?"
        ):
            self.vlm_status.config(text="🧠 Learning...", fg="#cba6f7")
            thread = threading.Thread(target=self._vlm_learn_session_thread, args=(duration,), daemon=True)
            thread.start()

    def _vlm_learn_session_thread(self, duration):
        """Run learning session in background"""
        try:
            self.vlm_append_output("\n" + "=" * 60 + "\n", "info")
            self.vlm_append_output("🧠 AUTONOMOUS LEARNING SESSION STARTING\n", "highlight")
            self.vlm_append_output("=" * 60 + "\n", "info")
            self.vlm_append_output(f"Duration: {duration} minute(s)\n\n", "info")

            self.vlm.autonomous_learning_session(duration)

            self.vlm_append_output("\n✅ Learning session complete!\n", "success")
            self.vlm_append_output("=" * 60 + "\n", "info")

            self.vlm_refresh_stats()
            self.vlm_status.config(text="✅ Learning Complete", fg="#a6e3a1")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#f38ba8")

    def vlm_query(self):
        """Query the learned knowledge"""
        if not self.vlm:
            messagebox.showwarning("VLM Not Available", "Virtual Language Model not initialized")
            return

        question = simpledialog.askstring(
            "Query Knowledge",
            "Ask the AI about what it has learned:"
        )

        if not question:
            return

        self.vlm_status.config(text="💭 Thinking...", fg="#89dceb")

        thread = threading.Thread(target=self._vlm_query_thread, args=(question,), daemon=True)
        thread.start()

    def _vlm_query_thread(self, question):
        """Query in background thread"""
        try:
            self.vlm_append_output("\n" + "━" * 60 + "\n", "info")
            self.vlm_append_output("💬 KNOWLEDGE QUERY\n", "highlight")
            self.vlm_append_output("━" * 60 + "\n", "info")
            self.vlm_append_output(f"Question: {question}\n\n", "info")

            answer = self.vlm.query_knowledge(question)

            self.vlm_append_output("🤖 Answer:\n", "success")
            self.vlm_append_output(f"{answer}\n", "info")
            self.vlm_append_output("━" * 60 + "\n", "info")

            self.vlm_status.config(text="✅ Ready to Learn", fg="#a6e3a1")

        except Exception as e:
            self.vlm_append_output(f"\n❌ Error: {str(e)}\n", "error")
            self.vlm_status.config(text="❌ Error", fg="#f38ba8")

    def show_vlm_help(self):
        """Show VLM help dialog"""
        help_text = (
            "VIRTUAL LANGUAGE MODEL - HOW IT WORKS\n\n"
            "WHAT IS IT?\n\n"
            "A self-learning AI that:\n"
            "  - Observes your screen with AI vision\n"
            "  - Learns UI patterns and workflows\n"
            "  - Builds a knowledge base over time\n"
            "  - Makes intelligent decisions\n"
            "  - Controls your desktop based on learned knowledge\n\n"
            "HOW TO USE:\n\n"
            "1. OBSERVE: Click 'Observe Screen' to let AI see your desktop\n"
            "2. DECIDE: Enter a goal and click 'Decide Action'\n"
            "3. EXECUTE: Click 'Execute' to perform the action\n"
            "4. LEARN: Click 'Learn Session' for autonomous learning\n"
            "5. QUERY: Click 'Query Knowledge' to ask what it learned\n\n"
            "EXAMPLE WORKFLOW:\n\n"
            "1. Click 'Observe Screen' - AI sees your desktop\n"
            "2. Enter goal: 'Search for Python tutorials'\n"
            "3. Click 'Decide Action' - AI plans the steps\n"
            "4. Click 'Execute' - AI performs the search\n"
            "5. AI learns from this experience!\n\n"
            "MEMORY:\n\n"
            "All learned knowledge is saved to vlm_memory.json\n"
            "The AI remembers between sessions!\n\n"
            "For full functionality, download and run locally!"
        )
        messagebox.showinfo("Virtual Language Model Help", help_text)

    def view_comprehensive_screenshots(self):
        """View generated screenshots"""
        import os
        screenshot_files = [f for f in os.listdir('.') if f.startswith('step_') and f.endswith('.png')]

        if not screenshot_files:
            messagebox.showinfo("Screenshots",
                                "No screenshots found.\n\nScreenshots are generated during execution.\nDownload and run locally for full monitoring.")
        else:
            msg = f"Found {len(screenshot_files)} screenshots:\n\n"
            for f in sorted(screenshot_files[:10]):
                msg += f"• {f}\n"
            if len(screenshot_files) > 10:
                msg += f"\n... and {len(screenshot_files) - 10} more"
            messagebox.showinfo("Screenshots", msg)

    def show_comprehensive_stats(self):
        """Show comprehensive controller statistics"""
        if not self.comprehensive_controller:
            messagebox.showinfo("Stats", "Controller not available")
            return

        stats_text = f"""
COMPREHENSIVE CONTROLLER STATS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: {'✅ Ready' if self.comprehensive_controller else '❌ Not Available'}

Features:
  • Deep Prompt Understanding
  • Intelligent Task Breakdown  
  • Real-Time Screen Monitoring
  • AI Vision Verification
  • Adaptive Error Recovery

Executions: {len(self.comprehensive_controller.execution_log) if self.comprehensive_controller else 0}
Screen States: {len(self.comprehensive_controller.screen_states) if self.comprehensive_controller else 0}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 For full desktop control with actual mouse,
keyboard, and screen access:
  1. Download this project
  2. Install: pip install -r requirements.txt
  3. Set API key: GEMINI_API_KEY=your_key
  4. Run: python gui_app.py
"""
        messagebox.showinfo("Comprehensive Controller Stats", stats_text)

    def create_macro_recorder_tab(self, notebook):
        """Macro Recorder Tab - Record and playback automation macros"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="🎬 Macro Recorder")

        # Header
        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="🎬 Macro Recorder & Playback",
                          bg="#1a1a2e",
                          fg="#f5c2e7",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="🎯 Record • 💾 Save • ▶️ Playback • 🔄 Loop • 📱 Remote Control",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Main container
        main_container = tk.Frame(tab, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Controls
        left_column = tk.Frame(main_container, bg="#1e1e2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Recording controls
        record_frame = tk.Frame(left_column, bg="#313244", relief="flat")
        record_frame.pack(fill="x", pady=5)

        record_label = tk.Label(record_frame,
                                text="📹 Recording Controls",
                                bg="#313244",
                                fg="#f5c2e7",
                                font=("Segoe UI", 11, "bold"))
        record_label.pack(pady=10)

        # Record status
        self.macro_record_status = tk.Label(record_frame,
                                            text="⚫ Ready to Record",
                                            bg="#313244",
                                            fg="#a6adc8",
                                            font=("Segoe UI", 10))
        self.macro_record_status.pack(pady=5)

        # Record buttons
        record_btn_frame = tk.Frame(record_frame, bg="#313244")
        record_btn_frame.pack(pady=10)

        self.macro_start_record_btn = tk.Button(record_btn_frame,
                                                text="🔴 Start Recording",
                                                bg="#f38ba8",
                                                fg="#0f0f1e",
                                                font=("Segoe UI", 10, "bold"),
                                                relief="flat",
                                                cursor="hand2",
                                                command=self.start_macro_recording,
                                                padx=20,
                                                pady=10)
        self.macro_start_record_btn.pack(side="left", padx=5)
        self.add_hover_effect(self.macro_start_record_btn, "#f38ba8", "#eba0ac")

        self.macro_stop_record_btn = tk.Button(record_btn_frame,
                                               text="⏹️ Stop & Save",
                                               bg="#89b4fa",
                                               fg="#0f0f1e",
                                               font=("Segoe UI", 10, "bold"),
                                               relief="flat",
                                               cursor="hand2",
                                               command=self.stop_macro_recording,
                                               padx=20,
                                               pady=10,
                                               state="disabled")
        self.macro_stop_record_btn.pack(side="left", padx=5)
        self.add_hover_effect(self.macro_stop_record_btn, "#89b4fa", "#74c7ec")

        # Macro list
        list_frame = tk.Frame(left_column, bg="#313244", relief="flat")
        list_frame.pack(fill="both", expand=True, pady=10)

        list_label = tk.Label(list_frame,
                              text="💾 Saved Macros",
                              bg="#313244",
                              fg="#a6e3a1",
                              font=("Segoe UI", 11, "bold"))
        list_label.pack(pady=10)

        # Macro listbox
        macro_list_container = tk.Frame(list_frame, bg="#313244")
        macro_list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        macro_scrollbar = tk.Scrollbar(macro_list_container)
        macro_scrollbar.pack(side="right", fill="y")

        self.macro_listbox = tk.Listbox(macro_list_container,
                                        bg="#0f0f1e",
                                        fg="#cdd6f4",
                                        font=("Consolas", 10),
                                        relief="flat",
                                        selectbackground="#45475a",
                                        selectforeground="#f5c2e7",
                                        yscrollcommand=macro_scrollbar.set)
        self.macro_listbox.pack(side="left", fill="both", expand=True)
        macro_scrollbar.config(command=self.macro_listbox.yview)

        # Refresh button
        refresh_btn = tk.Button(list_frame,
                                text="🔄 Refresh List",
                                bg="#45475a",
                                fg="#ffffff",
                                font=("Segoe UI", 9),
                                relief="flat",
                                cursor="hand2",
                                command=self.refresh_macro_list,
                                padx=15,
                                pady=8)
        refresh_btn.pack(pady=5)
        self.add_hover_effect(refresh_btn, "#45475a", "#585b70")

        # Right column - Playback & Output
        right_column = tk.Frame(main_container, bg="#1e1e2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Playback controls
        playback_frame = tk.Frame(right_column, bg="#313244", relief="flat")
        playback_frame.pack(fill="x", pady=5)

        playback_label = tk.Label(playback_frame,
                                  text="▶️ Playback Controls",
                                  bg="#313244",
                                  fg="#89dceb",
                                  font=("Segoe UI", 11, "bold"))
        playback_label.pack(pady=10)

        # Repeat and speed controls
        controls_container = tk.Frame(playback_frame, bg="#313244")
        controls_container.pack(fill="x", padx=10, pady=10)

        # Repeat count
        repeat_frame = tk.Frame(controls_container, bg="#313244")
        repeat_frame.pack(fill="x", pady=5)

        tk.Label(repeat_frame,
                 text="🔄 Repeat:",
                 bg="#313244",
                 fg="#a6adc8",
                 font=("Segoe UI", 9)).pack(side="left", padx=5)

        self.macro_repeat_var = tk.StringVar(value="1")
        repeat_spinbox = tk.Spinbox(repeat_frame,
                                    from_=1,
                                    to=100,
                                    textvariable=self.macro_repeat_var,
                                    bg="#0f0f1e",
                                    fg="#ffffff",
                                    font=("Segoe UI", 10),
                                    relief="flat",
                                    width=10)
        repeat_spinbox.pack(side="left", padx=5)

        # Speed control
        speed_frame = tk.Frame(controls_container, bg="#313244")
        speed_frame.pack(fill="x", pady=5)

        tk.Label(speed_frame,
                 text="⚡ Speed:",
                 bg="#313244",
                 fg="#a6adc8",
                 font=("Segoe UI", 9)).pack(side="left", padx=5)

        self.macro_speed_var = tk.StringVar(value="1.0")
        speed_options = ["0.5x", "1.0x", "1.5x", "2.0x", "3.0x"]
        speed_combo = ttk.Combobox(speed_frame,
                                   values=speed_options,
                                   textvariable=self.macro_speed_var,
                                   state="readonly",
                                   font=("Segoe UI", 9),
                                   width=10)
        speed_combo.current(1)
        speed_combo.pack(side="left", padx=5)

        # Playback buttons
        playback_btns = tk.Frame(playback_frame, bg="#313244")
        playback_btns.pack(pady=15)

        play_btn = tk.Button(playback_btns,
                             text="▶️ Play Selected",
                             bg="#a6e3a1",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.play_macro,
                             padx=20,
                             pady=10)
        play_btn.pack(side="left", padx=5)
        self.add_hover_effect(play_btn, "#a6e3a1", "#94e2d5")

        stop_btn = tk.Button(playback_btns,
                             text="⏹️ Stop",
                             bg="#f38ba8",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=self.stop_macro_playback,
                             padx=20,
                             pady=10)
        stop_btn.pack(side="left", padx=5)
        self.add_hover_effect(stop_btn, "#f38ba8", "#eba0ac")

        delete_btn = tk.Button(playback_btns,
                               text="🗑️ Delete",
                               bg="#45475a",
                               fg="#ffffff",
                               font=("Segoe UI", 10, "bold"),
                               relief="flat",
                               cursor="hand2",
                               command=self.delete_macro,
                               padx=20,
                               pady=10)
        delete_btn.pack(side="left", padx=5)
        self.add_hover_effect(delete_btn, "#45475a", "#585b70")

        # Output console
        output_label = tk.Label(right_column,
                                text="📋 Macro Output",
                                bg="#1e1e2e",
                                fg="#a6adc8",
                                font=("Segoe UI", 10, "bold"))
        output_label.pack(anchor="w", padx=5, pady=(10, 5))

        self.macro_output = scrolledtext.ScrolledText(right_column,
                                                      bg="#0f0f1e",
                                                      fg="#cdd6f4",
                                                      font=("Consolas", 9),
                                                      wrap=tk.WORD,
                                                      state='disabled',
                                                      relief="flat",
                                                      padx=10,
                                                      pady=10)
        self.macro_output.pack(fill="both", expand=True, padx=5, pady=5)

        self.macro_output.tag_config("success", foreground="#a6e3a1")
        self.macro_output.tag_config("error", foreground="#f38ba8")
        self.macro_output.tag_config("info", foreground="#89dceb")
        self.macro_output.tag_config("event", foreground="#f9e2af")

        # Initialize macro list
        self.refresh_macro_list()

    def create_mobile_operations_tab(self, notebook):
        """Mobile Operations Tab - Remote control interface"""
        tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(tab, text="📱 Mobile Control")

        # Header
        header_frame = tk.Frame(tab, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(10, 0), padx=10)

        header = tk.Label(header_frame,
                          text="📱 Mobile Companion Control",
                          bg="#1a1a2e",
                          fg="#89dceb",
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=12)

        info = tk.Label(header_frame,
                        text="📡 Remote Access • 🎮 Mobile Commands • 🔔 Notifications • 🎬 Remote Macros",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 12))

        # Main container
        main_container = tk.Frame(tab, bg="#1e1e2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column - Server info and status
        left_column = tk.Frame(main_container, bg="#1e1e2e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Server status
        status_frame = tk.Frame(left_column, bg="#313244", relief="flat")
        status_frame.pack(fill="x", pady=5)

        status_label = tk.Label(status_frame,
                                text="📡 Server Status",
                                bg="#313244",
                                fg="#89dceb",
                                font=("Segoe UI", 11, "bold"))
        status_label.pack(pady=10)

        self.mobile_status = tk.Label(status_frame,
                                      text="✅ Server Running",
                                      bg="#313244",
                                      fg="#a6e3a1",
                                      font=("Segoe UI", 10))
        self.mobile_status.pack(pady=5)

        # Server info
        info_text = tk.Text(status_frame,
                            bg="#0f0f1e",
                            fg="#cdd6f4",
                            font=("Consolas", 9),
                            height=8,
                            relief="flat",
                            padx=10,
                            pady=10,
                            state='disabled',
                            wrap=tk.WORD)
        info_text.pack(fill="x", padx=10, pady=10)

        # Get domain info
        domain = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')

        info_text.config(state='normal')
        info_text.insert("1.0",
                         f"📱 Mobile Interface:\n"
                         f"https://{domain}/mobile\n\n"
                         f"💻 Desktop Dashboard:\n"
                         f"https://{domain}/\n\n"
                         f"🔐 Default PIN: 1234\n"
                         f"📡 WebSocket: Connected\n"
                         f"🔔 Notifications: Enabled")
        info_text.config(state='disabled')

        # Quick actions
        actions_frame = tk.Frame(left_column, bg="#313244", relief="flat")
        actions_frame.pack(fill="both", expand=True, pady=10)

        actions_label = tk.Label(actions_frame,
                                 text="⚡ Quick Actions",
                                 bg="#313244",
                                 fg="#f9e2af",
                                 font=("Segoe UI", 11, "bold"))
        actions_label.pack(pady=10)

        actions = [
            ("📱 Open Mobile Interface", lambda: self.open_mobile_interface()),
            ("💻 Open Desktop Dashboard", lambda: self.open_desktop_dashboard()),
            ("🎬 Trigger Remote Macro", lambda: self.trigger_remote_macro()),
            ("📊 View Connected Clients", lambda: self.view_mobile_clients()),
            ("🔔 Send Test Notification", lambda: self.send_test_notification()),
        ]

        for text, command in actions:
            btn = tk.Button(actions_frame,
                            text=text,
                            bg="#45475a",
                            fg="#ffffff",
                            font=("Segoe UI", 10),
                            relief="flat",
                            cursor="hand2",
                            command=command,
                            anchor="w",
                            padx=15,
                            pady=10)
            btn.pack(fill="x", padx=10, pady=3)
            self.add_hover_effect(btn, "#45475a", "#585b70")

        # Right column - Mobile command history
        right_column = tk.Frame(main_container, bg="#1e1e2e")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Command history
        history_label = tk.Label(right_column,
                                 text="📜 Mobile Command History",
                                 bg="#1e1e2e",
                                 fg="#a6adc8",
                                 font=("Segoe UI", 10, "bold"))
        history_label.pack(anchor="w", padx=5, pady=5)

        self.mobile_history = scrolledtext.ScrolledText(right_column,
                                                        bg="#0f0f1e",
                                                        fg="#cdd6f4",
                                                        font=("Consolas", 9),
                                                        wrap=tk.WORD,
                                                        state='disabled',
                                                        relief="flat",
                                                        padx=10,
                                                        pady=10)
        self.mobile_history.pack(fill="both", expand=True, padx=5, pady=5)

        self.mobile_history.tag_config("timestamp", foreground="#6c7086")
        self.mobile_history.tag_config("command", foreground="#89dceb")
        self.mobile_history.tag_config("success", foreground="#a6e3a1")
        self.mobile_history.tag_config("error", foreground="#f38ba8")

        # Add initial message
        self.mobile_append_history("📱 Mobile Companion Server is running", "success")
        self.mobile_append_history(f"🌐 Access from your phone: https://{domain}/mobile", "info")

    # Macro Recorder Methods
    def start_macro_recording(self):
        """Start recording a macro"""
        if not self.macro_recorder:
            messagebox.showerror("Error", "Macro Recorder not initialized")
            return

        name = simpledialog.askstring("Macro Name", "Enter a name for this macro:")
        if not name:
            return

        self.current_macro_name = name
        self.macro_append_output(f"🔴 Starting macro recording: {name}\n", "info")

        def on_event(event):
            event_type = event.get('type', 'unknown')
            self.macro_append_output(f"  • {event_type}\n", "event")

        result = self.macro_recorder.start_recording(callback=on_event)
        self.macro_append_output(f"{result}\n", "success")

        self.macro_record_status.config(text="🔴 Recording...", fg="#f38ba8")
        self.macro_start_record_btn.config(state="disabled")
        self.macro_stop_record_btn.config(state="normal")
        self.recording_active = True

    def stop_macro_recording(self):
        """Stop recording and save macro"""
        if not self.macro_recorder or not self.recording_active:
            return

        result = self.macro_recorder.stop_recording(name=self.current_macro_name)
        self.macro_append_output(f"{result}\n", "success")

        self.macro_record_status.config(text="⚫ Ready to Record", fg="#a6adc8")
        self.macro_start_record_btn.config(state="normal")
        self.macro_stop_record_btn.config(state="disabled")
        self.recording_active = False

        self.refresh_macro_list()

    def refresh_macro_list(self):
        """Refresh the list of saved macros"""
        if not self.macro_recorder:
            return

        self.macro_listbox.delete(0, tk.END)
        macros = self.macro_recorder.list_macros()

        for macro in macros:
            display_text = f"{macro['name']} ({macro['event_count']} events, {macro['duration']:.1f}s)"
            self.macro_listbox.insert(tk.END, display_text)

        if macros:
            self.macro_append_output(f"📋 Loaded {len(macros)} macro(s)\n", "info")

    def play_macro(self):
        """Play the selected macro"""
        if not self.macro_recorder:
            messagebox.showerror("Error", "Macro Recorder not initialized")
            return

        selection = self.macro_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a macro to play")
            return

        index = selection[0]
        macros = self.macro_recorder.list_macros()
        macro = macros[index]

        repeat = int(self.macro_repeat_var.get())
        speed_str = self.macro_speed_var.get().replace('x', '')
        speed = float(speed_str)

        self.macro_append_output(f"▶️ Playing macro: {macro['name']}\n", "info")
        self.macro_append_output(f"   Repeat: {repeat}x, Speed: {speed}x\n", "info")

        def on_complete(message):
            self.macro_append_output(f"{message}\n", "success")

        result = self.macro_recorder.play_macro(macro_name=macro['name'],
                                                repeat=repeat,
                                                speed=speed,
                                                callback=on_complete)
        self.macro_append_output(f"{result}\n", "success")

    def stop_macro_playback(self):
        """Stop macro playback"""
        if not self.macro_recorder:
            return

        result = self.macro_recorder.stop_playback()
        self.macro_append_output(f"{result}\n", "info")

    def delete_macro(self):
        """Delete the selected macro"""
        if not self.macro_recorder:
            return

        selection = self.macro_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a macro to delete")
            return

        index = selection[0]
        macros = self.macro_recorder.list_macros()
        macro = macros[index]

        if messagebox.askyesno("Confirm Delete", f"Delete macro '{macro['name']}'?"):
            result = self.macro_recorder.delete_macro(macro['name'])
            self.macro_append_output(f"{result}\n", "info")
            self.refresh_macro_list()

    def macro_append_output(self, text, tag=None):
        """Append text to macro output console"""
        if hasattr(self, 'macro_output'):
            self.macro_output.config(state='normal')
            self.macro_output.insert(tk.END, text, tag)
            self.macro_output.see(tk.END)
            self.macro_output.config(state='disabled')

    # Mobile Operations Methods
    def open_mobile_interface(self):
        """Open mobile interface in browser"""
        domain = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
        url = f"https://{domain}/mobile"
        self.mobile_append_history(f"🌐 Opening: {url}", "info")
        messagebox.showinfo("Mobile Interface",
                            f"Mobile interface URL:\n\n{url}\n\nOpen this URL on your mobile device.")

    def open_desktop_dashboard(self):
        """Open desktop dashboard"""
        domain = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
        url = f"https://{domain}/"
        self.mobile_append_history(f"💻 Opening: {url}", "info")
        messagebox.showinfo("Desktop Dashboard", f"Desktop dashboard URL:\n\n{url}")

    def trigger_remote_macro(self):
        """Trigger a macro from mobile interface"""
        if not self.macro_recorder:
            messagebox.showerror("Error", "Macro Recorder not initialized")
            return

        macros = self.macro_recorder.list_macros()
        if not macros:
            messagebox.showinfo("No Macros",
                                "No saved macros available.\n\nRecord a macro first in the Macro Recorder tab.")
            return

        macro_names = [m['name'] for m in macros]

        # Simple selection dialog
        selection = simpledialog.askstring("Remote Macro",
                                           f"Available macros:\n{', '.join(macro_names)}\n\nEnter macro name:")

        if selection and selection in macro_names:
            self.mobile_append_history(f"🎬 Triggered remote macro: {selection}", "command")
            self.mobile_append_history("   (Mobile trigger simulation)", "info")
            messagebox.showinfo("Success",
                                f"Macro '{selection}' triggered!\n\nIn the full version, this would execute from your mobile device.")
        elif selection:
            self.mobile_append_history(f"❌ Macro not found: {selection}", "error")

    def view_mobile_clients(self):
        """View connected mobile clients"""
        self.mobile_append_history("📊 Viewing connected clients...", "info")
        messagebox.showinfo("Connected Clients",
                            "Mobile Companion Server Status:\n\n"
                            "✅ Server Running\n"
                            "📡 WebSocket Enabled\n"
                            "🔔 Notifications Active\n\n"
                            "Connect your mobile device to:\n"
                            f"https://{os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')}/mobile")

    def send_test_notification(self):
        """Send a test notification"""
        self.mobile_append_history("🔔 Sending test notification...", "command")
        messagebox.showinfo("Test Notification", "Test notification sent!\n\nCheck your mobile device if connected.")
        self.mobile_append_history("✅ Test notification sent", "success")

    def mobile_append_history(self, text, tag=None):
        """Append text to mobile history console"""
        if hasattr(self, 'mobile_history'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.mobile_history.config(state='normal')
            self.mobile_history.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.mobile_history.insert(tk.END, f"{text}\n", tag)
            self.mobile_history.see(tk.END)
            self.mobile_history.config(state='disabled')

    def workflow_log(self, message, level="INFO"):
        """Log callback for workflow builder"""
        level_colors = {
            "INFO": "#89b4fa",
            "SUCCESS": "#a6e3a1",
            "ERROR": "#f38ba8",
            "WARNING": "#f9e2af"
        }
        if hasattr(self, 'workflow_output_text'):
            self.workflow_output_text.config(state='normal')
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.workflow_output_text.insert(tk.END, f"[{timestamp}] ", ("timestamp",))
            self.workflow_output_text.insert(tk.END, f"{message}\n", (level.lower(),))
            self.workflow_output_text.see(tk.END)
            self.workflow_output_text.config(state='disabled')

    def show_workflow_builder(self):
        """Open Natural Language Workflow Builder window"""
        if not self.nl_workflow_builder:
            messagebox.showerror("Error", "Workflow Builder not initialized")
            return

        builder_window = tk.Toplevel(self.root)
        builder_window.title("💬 Natural Language Workflow Builder")
        builder_window.geometry("1000x700")
        builder_window.configure(bg="#0f0f1e")

        header_frame = tk.Frame(builder_window, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=20, pady=15)

        header = tk.Label(header_frame,
                          text="💬 Natural Language Workflow Builder",
                          bg="#1a1a2e",
                          fg="#89b4fa",
                          font=("Segoe UI", 16, "bold"))
        header.pack(pady=10)

        info = tk.Label(header_frame,
                        text="🎯 Describe workflows in plain English • 🤖 AI converts to automation • 💬 Test & refine • 💾 Save as templates",
                        bg="#1a1a2e",
                        fg="#a6adc8",
                        font=("Segoe UI", 9, "italic"))
        info.pack(pady=(0, 10))

        main_container = tk.Frame(builder_window, bg="#0f0f1e")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        left_column = tk.Frame(main_container, bg="#0f0f1e")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        examples_frame = tk.Frame(left_column, bg="#313244")
        examples_frame.pack(fill="x", pady=(0, 10))

        examples_label = tk.Label(examples_frame,
                                  text="💡 Example Workflows",
                                  bg="#313244",
                                  fg="#f9e2af",
                                  font=("Segoe UI", 10, "bold"))
        examples_label.pack(pady=10)

        examples_list = tk.Listbox(examples_frame,
                                   bg="#0f0f1e",
                                   fg="#cdd6f4",
                                   font=("Segoe UI", 9),
                                   height=6,
                                   selectmode=tk.SINGLE,
                                   relief="flat")
        examples_list.pack(fill="x", padx=10, pady=(0, 10))

        examples = self.nl_workflow_builder.get_examples()
        for example in examples:
            examples_list.insert(tk.END, example['name'])

        def use_example():
            selection = examples_list.curselection()
            if selection:
                example = examples[selection[0]]
                input_text.delete("1.0", tk.END)
                input_text.insert("1.0", example['description'])

        use_example_btn = tk.Button(examples_frame,
                                    text="📋 Use Selected Example",
                                    bg="#89b4fa",
                                    fg="#0f0f1e",
                                    font=("Segoe UI", 9, "bold"),
                                    relief="flat",
                                    cursor="hand2",
                                    command=use_example,
                                    pady=8)
        use_example_btn.pack(fill="x", padx=10, pady=(0, 10))

        input_label = tk.Label(left_column,
                               text="💬 Describe Your Workflow:",
                               bg="#0f0f1e",
                               fg="#a6e3a1",
                               font=("Segoe UI", 11, "bold"))
        input_label.pack(anchor="w", pady=(10, 5))

        input_text = tk.Text(left_column,
                             bg="#313244",
                             fg="#ffffff",
                             font=("Segoe UI", 11),
                             height=8,
                             wrap=tk.WORD,
                             relief="flat",
                             padx=10,
                             pady=10)
        input_text.pack(fill="both", expand=True, pady=(0, 10))

        button_frame = tk.Frame(left_column, bg="#0f0f1e")
        button_frame.pack(fill="x", pady=10)

        def process_workflow():
            description = input_text.get("1.0", tk.END).strip()
            if not description:
                messagebox.showwarning("Empty Input", "Please describe your workflow")
                return

            self.workflow_log(f"Processing: {description}", "INFO")
            result = self.nl_workflow_builder.describe_workflow(description)

            if result.get("success"):
                if result.get("type") == "workflow":
                    workflow = result["workflow"]
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", f"Workflow: {workflow.get('workflow_name', 'Unnamed')}\n\n")
                    output_text.insert(tk.END, f"Description: {workflow.get('description', '')}\n\n")
                    output_text.insert(tk.END, "Steps:\n")
                    for i, step in enumerate(workflow.get("steps", []), 1):
                        output_text.insert(tk.END, f"{i}. {step.get('action')} - {step.get('parameters')}\n")

                    if workflow.get("suggestions"):
                        output_text.insert(tk.END, f"\n💡 Suggestions: {workflow['suggestions']}\n")

                    self.workflow_log(f"Generated workflow: {workflow.get('workflow_name')}", "SUCCESS")
                else:
                    self.workflow_log(result.get("message", "AI response received"), "INFO")
                    messagebox.showinfo("AI Response", result.get("message", ""))
            else:
                error = result.get("error", "Unknown error")
                self.workflow_log(f"Error: {error}", "ERROR")
                messagebox.showerror("Error", error)

        def save_current_workflow():
            current_draft = self.nl_workflow_builder.get_current_draft()
            if not current_draft:
                messagebox.showwarning("No Workflow", "Create a workflow first")
                return

            result = self.nl_workflow_builder.save_workflow()
            if result.get("success"):
                self.workflow_log(f"Saved workflow: {result.get('name')}", "SUCCESS")
                messagebox.showinfo("Success", result.get("message"))
                refresh_saved_list()
            else:
                self.workflow_log(f"Save failed: {result.get('error')}", "ERROR")
                messagebox.showerror("Error", result.get("error"))

        def clear_conversation():
            self.nl_workflow_builder.clear_conversation()
            self.nl_workflow_builder.clear_draft()
            input_text.delete("1.0", tk.END)
            output_text.delete("1.0", tk.END)
            self.workflow_log("Conversation cleared", "INFO")

        process_btn = tk.Button(button_frame,
                                text="🤖 Build Workflow",
                                bg="#a6e3a1",
                                fg="#0f0f1e",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat",
                                cursor="hand2",
                                command=process_workflow,
                                padx=20,
                                pady=10)
        process_btn.pack(side="left", padx=5)

        save_btn = tk.Button(button_frame,
                             text="💾 Save Workflow",
                             bg="#89b4fa",
                             fg="#0f0f1e",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat",
                             cursor="hand2",
                             command=save_current_workflow,
                             padx=20,
                             pady=10)
        save_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(button_frame,
                              text="🗑️ Clear",
                              bg="#f38ba8",
                              fg="#0f0f1e",
                              font=("Segoe UI", 10, "bold"),
                              relief="flat",
                              cursor="hand2",
                              command=clear_conversation,
                              padx=20,
                              pady=10)
        clear_btn.pack(side="left", padx=5)

        right_column = tk.Frame(main_container, bg="#0f0f1e")
        right_column.pack(side="right", fill="both", expand=True)

        output_label = tk.Label(right_column,
                                text="📋 Generated Workflow:",
                                bg="#0f0f1e",
                                fg="#cba6f7",
                                font=("Segoe UI", 11, "bold"))
        output_label.pack(anchor="w", pady=(0, 5))

        output_text = tk.Text(right_column,
                              bg="#313244",
                              fg="#ffffff",
                              font=("Consolas", 10),
                              wrap=tk.WORD,
                              relief="flat",
                              padx=10,
                              pady=10)
        output_text.pack(fill="both", expand=True, pady=(0, 10))

        saved_frame = tk.Frame(right_column, bg="#313244")
        saved_frame.pack(fill="x", pady=(10, 0))

        saved_label = tk.Label(saved_frame,
                               text="💾 Saved Workflows",
                               bg="#313244",
                               fg="#f9e2af",
                               font=("Segoe UI", 10, "bold"))
        saved_label.pack(pady=10)

        saved_list = tk.Listbox(saved_frame,
                                bg="#0f0f1e",
                                fg="#cdd6f4",
                                font=("Segoe UI", 9),
                                height=8,
                                selectmode=tk.SINGLE,
                                relief="flat")
        saved_list.pack(fill="x", padx=10, pady=(0, 10))

        def refresh_saved_list():
            saved_list.delete(0, tk.END)
            workflows = self.nl_workflow_builder.list_templates()
            for wf in workflows:
                saved_list.insert(tk.END, f"{wf['name']} ({wf['steps_count']} steps)")

        def run_saved_workflow():
            selection = saved_list.curselection()
            if not selection:
                return

            workflows = self.nl_workflow_builder.list_templates()
            workflow = workflows[selection[0]]
            command = f"run workflow: {workflow['name']}"
            self.workflow_log(f"Executing workflow: {workflow['name']}", "INFO")
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, command)
            self.execute_command()

        refresh_btn = tk.Button(saved_frame,
                                text="🔄 Refresh List",
                                bg="#45475a",
                                fg="#ffffff",
                                font=("Segoe UI", 9),
                                relief="flat",
                                cursor="hand2",
                                command=refresh_saved_list,
                                pady=6)
        refresh_btn.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=(0, 10))

        run_btn = tk.Button(saved_frame,
                            text="▶️ Run Selected",
                            bg="#a6e3a1",
                            fg="#0f0f1e",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=run_saved_workflow,
                            pady=6)
        run_btn.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=(0, 10))

        log_frame = tk.Frame(builder_window, bg="#1a1a2e")
        log_frame.pack(fill="x", padx=20, pady=(0, 15))

        log_label = tk.Label(log_frame,
                             text="📊 Activity Log",
                             bg="#1a1a2e",
                             fg="#f9e2af",
                             font=("Segoe UI", 9, "bold"))
        log_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.workflow_output_text = tk.Text(log_frame,
                                            bg="#0f0f1e",
                                            fg="#cdd6f4",
                                            font=("Consolas", 9),
                                            height=6,
                                            state='disabled',
                                            relief="flat",
                                            padx=10,
                                            pady=10)
        self.workflow_output_text.pack(fill="x", padx=10, pady=(0, 10))

        self.workflow_output_text.tag_config("timestamp", foreground="#6c7086")
        self.workflow_output_text.tag_config("info", foreground="#89b4fa")
        self.workflow_output_text.tag_config("success", foreground="#a6e3a1")
        self.workflow_output_text.tag_config("error", foreground="#f38ba8")
        self.workflow_output_text.tag_config("warning", foreground="#f9e2af")

        refresh_saved_list()
        self.workflow_log("Workflow Builder ready!", "SUCCESS")


def main():
    root = tk.Tk()
    app = AutomationControllerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
