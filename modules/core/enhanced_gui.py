#!/usr/bin/env python3
"""
Enhanced Modern GUI for VATSAL AI Desktop Automation
Features: Modern design, animations, gradients, better UX
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from datetime import datetime
from pathlib import Path


class ModernGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ VATSAL - AI Desktop Automation")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#000000")

        # Sleek Black & White color palette
        self.colors = {
            'bg_primary': '#000000',  # Pure black
            'bg_secondary': '#0a0a0a',  # Slightly lighter black
            'bg_tertiary': '#1a1a1a',  # Dark gray
            'border_white': '#ffffff',  # Pure white borders
            'border_gray': '#808080',  # Gray borders
            'accent_blue': '#00d4ff',  # Cyan blue
            'accent_purple': '#b19cd9',  # Light purple
            'accent_green': '#00ff88',  # Neon green
            'accent_pink': '#ff0080',  # Hot pink
            'text_primary': '#ffffff',  # White text
            'text_secondary': '#cccccc',  # Light gray text
            'text_muted': '#808080',  # Muted gray
            'success': '#00ff88',  # Neon green
            'warning': '#ffaa00',  # Orange
            'error': '#ff0055',  # Red
            'card_bg': '#0f0f0f',  # Very dark gray
            'prompt_bg': '#1a1a1a',  # Prompt bar background
        }

        # State variables
        self.processing = False
        self.current_view = "dashboard"
        self.stats = {
            'commands_today': 0,
            'time_saved': 0,
            'tasks_completed': 0,
            'success_rate': 98.5
        }

        self.setup_modern_ui()

    def setup_modern_ui(self):
        """Setup the modern enhanced UI"""

        # Top Navigation Bar
        self.create_top_navbar()

        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=0, pady=0)

        # Sidebar
        self.create_sidebar(main_container)

        # Main content area with white border
        self.content_area = tk.Frame(
            main_container,
            bg=self.colors['bg_primary'],
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        self.content_area.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        # Show dashboard by default
        self.show_dashboard()

        # Command Prompt Bar at bottom
        self.create_prompt_bar()

    def create_top_navbar(self):
        """Create modern top navigation bar with white border"""
        navbar = tk.Frame(
            self.root,
            bg=self.colors['bg_secondary'],
            height=70,
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        navbar.pack(fill="x", side="top", padx=2, pady=(2, 0))
        navbar.pack_propagate(False)

        # Left side - Logo and title
        left_frame = tk.Frame(navbar, bg=self.colors['bg_secondary'])
        left_frame.pack(side="left", padx=30, pady=15)

        logo_label = tk.Label(
            left_frame,
            text="✨",
            font=("Segoe UI Emoji", 32),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_green']
        )
        logo_label.pack(side="left", padx=(0, 15))

        title_frame = tk.Frame(left_frame, bg=self.colors['bg_secondary'])
        title_frame.pack(side="left")

        title_label = tk.Label(
            title_frame,
            text="V.A.T.S.A.L.",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            title_frame,
            text="AI Desktop Automation",
            font=("Segoe UI", 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor="w")

        # Right side - Status and controls
        right_frame = tk.Frame(navbar, bg=self.colors['bg_secondary'])
        right_frame.pack(side="right", padx=30, pady=15)

        # Time display
        self.time_label = tk.Label(
            right_frame,
            text="",
            font=("Segoe UI", 12),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.time_label.pack(side="left", padx=20)
        self.update_time()

        # Status indicator
        status_frame = tk.Frame(right_frame, bg=self.colors['bg_secondary'])
        status_frame.pack(side="left", padx=10)

        status_dot = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 16),
            bg=self.colors['bg_secondary'],
            fg=self.colors['success']
        )
        status_dot.pack(side="left", padx=5)

        status_text = tk.Label(
            status_frame,
            text="Online",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['success']
        )
        status_text.pack(side="left")

    def create_sidebar(self, parent):
        """Create modern sidebar with white border"""
        sidebar = tk.Frame(
            parent,
            bg=self.colors['bg_secondary'],
            width=280,
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        sidebar.pack(side="left", fill="y", padx=(2, 0), pady=2)
        sidebar.pack_propagate(False)

        # Sidebar title
        sidebar_title = tk.Label(
            sidebar,
            text="NAVIGATION",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted'],
            pady=20
        )
        sidebar_title.pack(fill="x", padx=20)

        # Navigation buttons
        nav_items = [
            ("🏠", "Dashboard", "dashboard"),
            ("🎯", "Quick Actions", "actions"),
            ("💬", "AI Chat", "chat"),
            ("🤖", "Automation", "automation"),
            ("📊", "Analytics", "analytics"),
            ("⚙️", "Settings", "settings"),
        ]

        self.nav_buttons = {}

        for icon, name, view_id in nav_items:
            btn = self.create_nav_button(sidebar, icon, name, view_id)
            self.nav_buttons[view_id] = btn

        # Highlight dashboard by default
        self.highlight_nav_button("dashboard")

    def create_nav_button(self, parent, icon, name, view_id):
        """Create a modern navigation button with white border"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        btn_frame.pack(fill="x", padx=15, pady=5)

        btn = tk.Button(
            btn_frame,
            text=f"{icon}  {name}",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            activebackground=self.colors['accent_blue'],
            activeforeground=self.colors['text_primary'],
            relief="solid",
            borderwidth=2,
            cursor="hand2",
            anchor="w",
            padx=20,
            pady=12,
            command=lambda: self.switch_view(view_id),
            highlightbackground=self.colors['border_white'],
            highlightthickness=1
        )
        btn.pack(fill="both", expand=True)

        # Hover effects
        btn.bind("<Enter>", lambda e: btn.configure(
            bg=self.colors['bg_tertiary'] if self.current_view != view_id else self.colors['accent_blue'],
            fg=self.colors['text_primary']
        ))
        btn.bind("<Leave>", lambda e: btn.configure(
            bg=self.colors['accent_blue'] if self.current_view == view_id else self.colors['bg_tertiary'],
            fg=self.colors['text_primary'] if self.current_view == view_id else self.colors['text_secondary']
        ))

        return btn

    def highlight_nav_button(self, view_id):
        """Highlight the active navigation button"""
        for vid, btn in self.nav_buttons.items():
            if vid == view_id:
                btn.configure(bg=self.colors['accent_blue'], fg=self.colors['text_primary'])
            else:
                btn.configure(bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'])

    def switch_view(self, view_id):
        """Switch between different views"""
        self.current_view = view_id
        self.highlight_nav_button(view_id)

        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Show the selected view
        if view_id == "dashboard":
            self.show_dashboard()
        elif view_id == "actions":
            self.show_quick_actions()
        elif view_id == "chat":
            self.show_ai_chat()
        elif view_id == "automation":
            self.show_automation()
        elif view_id == "analytics":
            self.show_analytics()
        elif view_id == "settings":
            self.show_settings()

    def show_dashboard(self):
        """Show modern dashboard with stats and quick access"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Dashboard container with padding
        dashboard = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        dashboard.pack(fill="both", expand=True, padx=30, pady=20)

        # Header
        header = tk.Label(
            dashboard,
            text="Dashboard Overview",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        header.pack(anchor="w", pady=(0, 20))

        # Stats cards row
        stats_frame = tk.Frame(dashboard, bg=self.colors['bg_primary'])
        stats_frame.pack(fill="x", pady=(0, 30))

        # Create stats cards
        stats_cards = [
            ("📋", "Commands Today", self.stats['commands_today'], self.colors['accent_blue']),
            ("⏱️", "Time Saved", f"{self.stats['time_saved']}h", self.colors['accent_green']),
            ("✅", "Tasks Completed", self.stats['tasks_completed'], self.colors['accent_purple']),
            ("📈", "Success Rate", f"{self.stats['success_rate']}%", self.colors['success']),
        ]

        for icon, title, value, color in stats_cards:
            self.create_stat_card(stats_frame, icon, title, value, color)

        # Quick action buttons
        quick_actions_header = tk.Label(
            dashboard,
            text="⚡ Quick Actions",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        quick_actions_header.pack(anchor="w", pady=(10, 15))

        actions_container = tk.Frame(dashboard, bg=self.colors['bg_primary'])
        actions_container.pack(fill="both", expand=True)

        # Create quick action buttons in grid
        quick_actions = [
            ("💻", "Screenshot", "#667eea"),
            ("🔒", "Lock PC", "#f093fb"),
            ("📂", "File Explorer", "#4facfe"),
            ("🌐", "Open Chrome", "#43e97b"),
            ("📝", "Notepad", "#fa709a"),
            ("📧", "Gmail", "#fee140"),
            ("📺", "YouTube", "#f38ba8"),
            ("🎵", "Spotify", "#1db954"),
        ]

        row_frame = None
        for idx, (icon, name, color) in enumerate(quick_actions):
            if idx % 4 == 0:
                row_frame = tk.Frame(actions_container, bg=self.colors['bg_primary'])
                row_frame.pack(fill="x", pady=8)

            self.create_action_button(row_frame, icon, name, color)

    def create_stat_card(self, parent, icon, title, value, color):
        """Create a modern stats card with white border"""
        card_frame = tk.Frame(
            parent,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        card_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Card content with padding
        content = tk.Frame(card_frame, bg=self.colors['card_bg'])
        content.pack(fill="both", expand=True, padx=25, pady=20)

        # Icon
        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI Emoji", 36),
            bg=self.colors['card_bg'],
            fg=color
        )
        icon_label.pack(anchor="w")

        # Value
        value_label = tk.Label(
            content,
            text=str(value),
            font=("Segoe UI", 32, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary']
        )
        value_label.pack(anchor="w", pady=(5, 0))

        # Title
        title_label = tk.Label(
            content,
            text=title,
            font=("Segoe UI", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text_muted']
        )
        title_label.pack(anchor="w")

    def create_action_button(self, parent, icon, name, color):
        """Create a modern action button with white border"""
        btn_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        btn_container.pack(side="left", fill="both", expand=True, padx=8)

        btn = tk.Button(
            btn_container,
            text=f"{icon}\n{name}",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            activebackground=color,
            activeforeground=self.colors['text_primary'],
            relief="solid",
            borderwidth=2,
            cursor="hand2",
            padx=20,
            pady=20,
            command=lambda: self.execute_quick_action(name.lower()),
            highlightbackground=self.colors['border_white'],
            highlightthickness=1
        )
        btn.pack(fill="both", expand=True)

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.configure(bg=color))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.colors['card_bg']))

    def show_quick_actions(self):
        """Show comprehensive quick actions view"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        container = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Label(
            container,
            text="⚡ Quick Actions Center",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        header.pack(anchor="w", pady=(0, 20))

        # Scrollable canvas for actions
        canvas = tk.Canvas(container, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Action categories
        categories = {
            "🖥️ System Control": [
                ("💻", "Screenshot", "Take a screenshot"),
                ("🔒", "Lock Computer", "Lock your PC"),
                ("🔋", "Battery Info", "Check battery status"),
                ("📊", "Task Manager", "Open Task Manager"),
            ],
            "🌐 Web & Browsers": [
                ("🌍", "Chrome", "Open Google Chrome"),
                ("🔍", "Google Search", "Search on Google"),
                ("📧", "Gmail", "Open Gmail"),
                ("📺", "YouTube", "Open YouTube"),
            ],
            "📁 Productivity": [
                ("📂", "File Explorer", "Open Explorer"),
                ("📝", "Notepad", "Open Notepad"),
                ("💻", "VS Code", "Launch VS Code"),
                ("📊", "Excel", "Open Excel"),
            ],
            "🎵 Media & Entertainment": [
                ("🎵", "Spotify", "Launch Spotify"),
                ("🎬", "VLC Player", "Open VLC"),
                ("🔊", "Volume Control", "Adjust volume"),
                ("🎧", "Sound Settings", "Sound settings"),
            ],
        }

        for category, actions in categories.items():
            # Category header
            cat_label = tk.Label(
                scrollable_frame,
                text=category,
                font=("Segoe UI", 18, "bold"),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']
            )
            cat_label.pack(anchor="w", pady=(20, 10))

            # Actions grid
            actions_grid = tk.Frame(scrollable_frame, bg=self.colors['bg_primary'])
            actions_grid.pack(fill="x", pady=(0, 10))

            for idx, (icon, name, desc) in enumerate(actions):
                if idx % 4 == 0:
                    row = tk.Frame(actions_grid, bg=self.colors['bg_primary'])
                    row.pack(fill="x", pady=5)

                self.create_detailed_action_card(row, icon, name, desc)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_detailed_action_card(self, parent, icon, name, description):
        """Create detailed action card with white border"""
        card = tk.Frame(
            parent,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        card.pack(side="left", fill="both", expand=True, padx=8)

        content = tk.Frame(card, bg=self.colors['card_bg'])
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Icon
        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI Emoji", 28),
            bg=self.colors['card_bg'],
            fg=self.colors['accent_blue']
        )
        icon_label.pack(anchor="w")

        # Name
        name_label = tk.Label(
            content,
            text=name,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary']
        )
        name_label.pack(anchor="w", pady=(5, 2))

        # Description
        desc_label = tk.Label(
            content,
            text=description,
            font=("Segoe UI", 9),
            bg=self.colors['card_bg'],
            fg=self.colors['text_muted'],
            wraplength=150
        )
        desc_label.pack(anchor="w", pady=(0, 10))

        # Execute button
        exec_btn = tk.Button(
            content,
            text="Execute",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary'],
            relief="solid",
            borderwidth=1,
            cursor="hand2",
            command=lambda: self.execute_quick_action(name.lower()),
            padx=15,
            pady=5,
            highlightbackground=self.colors['border_white']
        )
        exec_btn.pack(fill="x")

        # Hover effect
        card.bind("<Enter>", lambda e: card.configure(bg=self.colors['bg_tertiary']))
        card.bind("<Leave>", lambda e: card.configure(bg=self.colors['card_bg']))

    def show_ai_chat(self):
        """Show AI Chat interface"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        container = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Label(
            container,
            text="💬 AI Chat Assistant",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        header.pack(anchor="w", pady=(0, 20))

        # Chat area with white border
        chat_frame = tk.Frame(
            container,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        chat_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            font=("Consolas", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_green'],
            relief="flat",
            padx=20,
            pady=15,
            wrap=tk.WORD
        )
        self.chat_display.pack(fill="both", expand=True)

        # Input area
        input_frame = tk.Frame(container, bg=self.colors['bg_primary'])
        input_frame.pack(fill="x")

        self.chat_input = tk.Entry(
            input_frame,
            font=("Consolas", 12),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_green'],
            relief="solid",
            borderwidth=2,
            highlightbackground=self.colors['border_white'],
            highlightcolor=self.colors['accent_green']
        )
        self.chat_input.pack(side="left", fill="both", expand=True, ipady=12, padx=(0, 10))
        self.chat_input.bind("<Return>", lambda e: self.send_chat_message())

        send_btn = tk.Button(
            input_frame,
            text="Send  ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary'],
            relief="solid",
            borderwidth=2,
            cursor="hand2",
            command=self.send_chat_message,
            padx=25,
            pady=12,
            highlightbackground=self.colors['border_white']
        )
        send_btn.pack(side="right")

        # Welcome message
        self.chat_display.insert("1.0", "🤖 VATSAL AI: Hello! How can I help you automate your tasks today?\n\n")
        self.chat_display.configure(state="disabled")

    def show_automation(self):
        """Show automation tools"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        container = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Label(
            container,
            text="🤖 Automation Center",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        header.pack(anchor="w", pady=(0, 20))

        # Automation features
        features = [
            ("🎬", "Macro Recorder", "Record and playback your actions", self.colors['accent_purple']),
            ("📝", "Script Builder", "Build custom automation scripts", self.colors['accent_blue']),
            ("⏰", "Task Scheduler", "Schedule automated tasks", self.colors['accent_green']),
            ("🔄", "Workflow Creator", "Create complex workflows", self.colors['accent_pink']),
        ]

        for icon, title, desc, color in features:
            feature_card = tk.Frame(
                container,
                bg=self.colors['card_bg'],
                highlightbackground=self.colors['border_white'],
                highlightthickness=2
            )
            feature_card.pack(fill="x", pady=10)

            content = tk.Frame(feature_card, bg=self.colors['card_bg'])
            content.pack(fill="both", padx=25, pady=20)

            # Icon and text on same line
            top_row = tk.Frame(content, bg=self.colors['card_bg'])
            top_row.pack(fill="x")

            icon_label = tk.Label(
                top_row,
                text=icon,
                font=("Segoe UI Emoji", 32),
                bg=self.colors['card_bg'],
                fg=color
            )
            icon_label.pack(side="left", padx=(0, 15))

            text_frame = tk.Frame(top_row, bg=self.colors['card_bg'])
            text_frame.pack(side="left", fill="both", expand=True)

            title_label = tk.Label(
                text_frame,
                text=title,
                font=("Segoe UI", 18, "bold"),
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary'],
                anchor="w"
            )
            title_label.pack(anchor="w")

            desc_label = tk.Label(
                text_frame,
                text=desc,
                font=("Segoe UI", 11),
                bg=self.colors['card_bg'],
                fg=self.colors['text_muted'],
                anchor="w"
            )
            desc_label.pack(anchor="w")

            # Launch button
            btn = tk.Button(
                top_row,
                text="Launch",
                font=("Segoe UI", 11, "bold"),
                bg=color,
                fg=self.colors['text_primary'],
                relief="solid",
                borderwidth=2,
                cursor="hand2",
                padx=20,
                pady=8,
                highlightbackground=self.colors['border_white']
            )
            btn.pack(side="right", padx=10)

    def show_analytics(self):
        """Show analytics dashboard"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        container = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Label(
            container,
            text="📊 Analytics & Insights",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        header.pack(anchor="w", pady=(0, 20))

        # Analytics placeholder
        placeholder = tk.Label(
            container,
            text="📈 Analytics dashboard coming soon...",
            font=("Segoe UI", 16),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_muted']
        )
        placeholder.pack(pady=50)

    def show_settings(self):
        """Show settings panel"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        container = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        container.pack(fill="both", expand=True, padx=30, pady=20)

        header = tk.Label(
            container,
            text="⚙️ Settings",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        header.pack(anchor="w", pady=(0, 20))

        # Settings options with white border
        settings_card = tk.Frame(
            container,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        settings_card.pack(fill="both", expand=True, padx=0, pady=0)

        settings_content = tk.Frame(settings_card, bg=self.colors['card_bg'])
        settings_content.pack(fill="both", expand=True, padx=30, pady=25)

        # Theme setting
        theme_label = tk.Label(
            settings_content,
            text="🎨 Theme",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary']
        )
        theme_label.pack(anchor="w", pady=(0, 10))

        theme_btn = tk.Button(
            settings_content,
            text="Dark Mode (Current)",
            font=("Segoe UI", 11),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=10
        )
        theme_btn.pack(anchor="w", pady=(0, 20))

        # Voice setting
        voice_label = tk.Label(
            settings_content,
            text="🎤 Voice Control",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary']
        )
        voice_label.pack(anchor="w", pady=(0, 10))

        voice_btn = tk.Button(
            settings_content,
            text="Enable Voice Commands",
            font=("Segoe UI", 11),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=10
        )
        voice_btn.pack(anchor="w")

    def send_chat_message(self):
        """Send a chat message"""
        message = self.chat_input.get().strip()
        if not message:
            return

        # Display user message
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n👤 You: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

        self.chat_input.delete(0, "end")

        # Simulate AI response
        threading.Thread(target=self.simulate_ai_response, args=(message,), daemon=True).start()

    def simulate_ai_response(self, message):
        """Simulate AI response"""
        import time
        time.sleep(1)

        response = f"I understand you want to: {message}. I'm processing that now..."

        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n🤖 VATSAL: {response}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def execute_quick_action(self, action_name):
        """Execute a quick action"""
        messagebox.showinfo(
            "Action Executed",
            f"Executing: {action_name.title()}\n\nThis would trigger the actual automation."
        )

        # Update stats
        self.stats['commands_today'] += 1
        self.stats['tasks_completed'] += 1

    def create_prompt_bar(self):
        """Create command prompt bar at the bottom"""
        prompt_container = tk.Frame(
            self.root,
            bg=self.colors['prompt_bg'],
            highlightbackground=self.colors['border_white'],
            highlightthickness=2
        )
        prompt_container.pack(fill="x", side="bottom", padx=2, pady=2)

        # Prompt frame
        prompt_frame = tk.Frame(prompt_container, bg=self.colors['prompt_bg'])
        prompt_frame.pack(fill="x", padx=15, pady=12)

        # Prompt label
        prompt_label = tk.Label(
            prompt_frame,
            text=">>>",
            font=("Consolas", 14, "bold"),
            bg=self.colors['prompt_bg'],
            fg=self.colors['accent_green']
        )
        prompt_label.pack(side="left", padx=(0, 10))

        # Command input
        self.prompt_entry = tk.Entry(
            prompt_frame,
            font=("Consolas", 13),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_green'],
            relief="solid",
            borderwidth=2,
            highlightbackground=self.colors['border_white'],
            highlightcolor=self.colors['accent_green'],
            highlightthickness=1
        )
        self.prompt_entry.pack(side="left", fill="both", expand=True, ipady=8)
        self.prompt_entry.bind("<Return>", lambda e: self.execute_prompt_command())

        # Execute button
        exec_btn = tk.Button(
            prompt_frame,
            text="⚡ Execute",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['accent_green'],
            fg=self.colors['bg_primary'],
            activebackground=self.colors['accent_blue'],
            activeforeground=self.colors['text_primary'],
            relief="solid",
            borderwidth=2,
            cursor="hand2",
            command=self.execute_prompt_command,
            padx=20,
            pady=8,
            highlightbackground=self.colors['border_white']
        )
        exec_btn.pack(side="right", padx=(10, 0))

        # Status label
        self.prompt_status = tk.Label(
            prompt_container,
            text="Ready to execute commands...",
            font=("Consolas", 9),
            bg=self.colors['prompt_bg'],
            fg=self.colors['text_muted'],
            anchor="w"
        )
        self.prompt_status.pack(fill="x", padx=15, pady=(0, 8))

    def execute_prompt_command(self):
        """Execute command from prompt bar"""
        command = self.prompt_entry.get().strip()
        if not command:
            return

        # Update status
        self.prompt_status.configure(
            text=f"Executing: {command}",
            fg=self.colors['accent_blue']
        )

        # Simulate command execution
        threading.Thread(target=self.process_prompt_command, args=(command,), daemon=True).start()

        # Clear input
        self.prompt_entry.delete(0, "end")

    def process_prompt_command(self, command):
        """Process the prompt command"""
        import time
        time.sleep(0.5)

        # Update status with success
        self.prompt_status.configure(
            text=f"✓ Executed: {command}",
            fg=self.colors['success']
        )

        # Update stats
        self.stats['commands_today'] += 1
        self.stats['tasks_completed'] += 1

        # Reset status after 3 seconds
        time.sleep(3)
        self.prompt_status.configure(
            text="Ready to execute commands...",
            fg=self.colors['text_muted']
        )

    def update_time(self):
        """Update the time display"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%B %d, %Y")
        self.time_label.configure(text=f"🕐 {time_str} • {date_str}")
        self.root.after(1000, self.update_time)


def main():
    """Launch the enhanced modern GUI"""
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
