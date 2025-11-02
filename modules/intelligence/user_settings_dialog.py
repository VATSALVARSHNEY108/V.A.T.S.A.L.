#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from user_profile_manager import get_user_profile_manager
from datetime import datetime


class UserSettingsDialog:
    """
    GUI Dialog for User Profile and Settings Management
    """

    def __init__(self, parent):
        self.parent = parent
        self.profile_manager = get_user_profile_manager()
        self.window = tk.Toplevel(parent)
        self.window.title("⚙️ User Profile & Settings")
        self.window.geometry("800x650")
        self.window.configure(bg="#1a1a2e")

        # Make dialog modal
        self.window.transient(parent)
        self.window.grab_set()

        self._create_ui()
        self._load_current_values()

    def _create_ui(self):
        """Create the UI components"""

        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2a2a3e', foreground='white',
                        padding=[20, 10], font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#3a3a5e')])

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.tab_user_info = self._create_user_info_tab(notebook)
        self.tab_preferences = self._create_preferences_tab(notebook)
        self.tab_custom = self._create_custom_settings_tab(notebook)
        self.tab_things = self._create_things_to_change_tab(notebook)
        self.tab_stats = self._create_stats_tab(notebook)

        notebook.add(self.tab_user_info, text='👤 User Info')
        notebook.add(self.tab_preferences, text='⚙️ Preferences')
        notebook.add(self.tab_custom, text='🔧 Custom Settings')
        notebook.add(self.tab_things, text='📝 Things to Change')
        notebook.add(self.tab_stats, text='📊 Statistics')

        # Bottom buttons
        button_frame = tk.Frame(self.window, bg="#1a1a2e")
        button_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(button_frame, text="💾 Save All", command=self._save_all,
                  bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'),
                  padx=20, pady=8).pack(side='left', padx=5)

        tk.Button(button_frame, text="🔄 Reload", command=self._load_current_values,
                  bg="#2196F3", fg="white", font=('Arial', 12, 'bold'),
                  padx=20, pady=8).pack(side='left', padx=5)

        tk.Button(button_frame, text="❌ Close", command=self.window.destroy,
                  bg="#f44336", fg="white", font=('Arial', 12, 'bold'),
                  padx=20, pady=8).pack(side='right', padx=5)

    def _create_user_info_tab(self, parent):
        """Create user information tab"""
        frame = tk.Frame(parent, bg="#1a1a2e")

        # Create input fields
        fields = [
            ("Full Name:", "name"),
            ("Nickname:", "nickname"),
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Timezone:", "timezone")
        ]

        self.user_info_entries = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label, bg="#1a1a2e", fg="white",
                     font=('Arial', 11, 'bold')).grid(row=i, column=0, sticky='w',
                                                      padx=20, pady=10)

            entry = tk.Entry(frame, font=('Arial', 11), bg="#2a2a3e", fg="white",
                             insertbackground="white", width=40)
            entry.grid(row=i, column=1, sticky='ew', padx=20, pady=10)
            self.user_info_entries[key] = entry

        frame.columnconfigure(1, weight=1)
        return frame

    def _create_preferences_tab(self, parent):
        """Create preferences tab"""
        frame = tk.Frame(parent, bg="#1a1a2e")

        self.pref_entries = {}

        # Theme
        row = 0
        tk.Label(frame, text="Theme:", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                  padx=20, pady=10)
        theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(frame, textvariable=theme_var,
                                   values=['dark', 'light'], state='readonly', width=37)
        theme_combo.grid(row=row, column=1, sticky='w', padx=20, pady=10)
        self.pref_entries['theme'] = theme_var

        # Notification Style
        row += 1
        tk.Label(frame, text="Notification Style:", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                  padx=20, pady=10)
        notif_var = tk.StringVar()
        notif_combo = ttk.Combobox(frame, textvariable=notif_var,
                                   values=['polite', 'brief', 'detailed'], state='readonly', width=37)
        notif_combo.grid(row=row, column=1, sticky='w', padx=20, pady=10)
        self.pref_entries['notification_style'] = notif_var

        # Voice Enabled
        row += 1
        voice_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Voice Enabled", variable=voice_var,
                       bg="#1a1a2e", fg="white", selectcolor="#2a2a3e",
                       font=('Arial', 11, 'bold')).grid(row=row, column=0, columnspan=2,
                                                        sticky='w', padx=20, pady=10)
        self.pref_entries['voice_enabled'] = voice_var

        # Voice Speed
        row += 1
        tk.Label(frame, text="Voice Speed:", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                  padx=20, pady=10)
        speed_entry = tk.Entry(frame, font=('Arial', 11), bg="#2a2a3e", fg="white",
                               insertbackground="white", width=40)
        speed_entry.grid(row=row, column=1, sticky='w', padx=20, pady=10)
        self.pref_entries['voice_speed'] = speed_entry

        # Voice Volume
        row += 1
        tk.Label(frame, text="Voice Volume (0.0-1.0):", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                  padx=20, pady=10)
        volume_entry = tk.Entry(frame, font=('Arial', 11), bg="#2a2a3e", fg="white",
                                insertbackground="white", width=40)
        volume_entry.grid(row=row, column=1, sticky='w', padx=20, pady=10)
        self.pref_entries['voice_volume'] = volume_entry

        # Wake Time
        row += 1
        tk.Label(frame, text="Wake Time (HH:MM):", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                  padx=20, pady=10)
        wake_entry = tk.Entry(frame, font=('Arial', 11), bg="#2a2a3e", fg="white",
                              insertbackground="white", width=40)
        wake_entry.grid(row=row, column=1, sticky='w', padx=20, pady=10)
        self.pref_entries['wake_time'] = wake_entry

        # Sleep Time
        row += 1
        tk.Label(frame, text="Sleep Time (HH:MM):", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                  padx=20, pady=10)
        sleep_entry = tk.Entry(frame, font=('Arial', 11), bg="#2a2a3e", fg="white",
                               insertbackground="white", width=40)
        sleep_entry.grid(row=row, column=1, sticky='w', padx=20, pady=10)
        self.pref_entries['sleep_time'] = sleep_entry

        # Language
        row += 1
        tk.Label(frame, text="Language:", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w',
                                                  padx=20, pady=10)
        lang_entry = tk.Entry(frame, font=('Arial', 11), bg="#2a2a3e", fg="white",
                              insertbackground="white", width=40)
        lang_entry.grid(row=row, column=1, sticky='w', padx=20, pady=10)
        self.pref_entries['language'] = lang_entry

        return frame

    def _create_custom_settings_tab(self, parent):
        """Create custom settings tab"""
        frame = tk.Frame(parent, bg="#1a1a2e")

        # Instructions
        tk.Label(frame, text="Add your own custom settings here:",
                 bg="#1a1a2e", fg="white", font=('Arial', 11, 'bold')).pack(pady=10)

        # Input frame
        input_frame = tk.Frame(frame, bg="#1a1a2e")
        input_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(input_frame, text="Key:", bg="#1a1a2e", fg="white",
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
        self.custom_key_entry = tk.Entry(input_frame, font=('Arial', 10),
                                         bg="#2a2a3e", fg="white", width=20)
        self.custom_key_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Value:", bg="#1a1a2e", fg="white",
                 font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5)
        self.custom_value_entry = tk.Entry(input_frame, font=('Arial', 10),
                                           bg="#2a2a3e", fg="white", width=30)
        self.custom_value_entry.grid(row=0, column=3, padx=5)

        tk.Button(input_frame, text="➕ Add", command=self._add_custom_setting,
                  bg="#4CAF50", fg="white", font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=5)

        # List of custom settings
        tk.Label(frame, text="Current Custom Settings:", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).pack(pady=(20, 5))

        self.custom_settings_listbox = tk.Listbox(frame, font=('Arial', 10),
                                                  bg="#2a2a3e", fg="white",
                                                  height=12)
        self.custom_settings_listbox.pack(fill='both', expand=True, padx=20, pady=5)

        btn_frame = tk.Frame(frame, bg="#1a1a2e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🗑️ Remove Selected", command=self._remove_custom_setting,
                  bg="#f44336", fg="white", font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        tk.Button(btn_frame, text="🔄 Refresh List", command=self._refresh_custom_settings_list,
                  bg="#2196F3", fg="white", font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        return frame

    def _create_things_to_change_tab(self, parent):
        """Create things to change tab"""
        frame = tk.Frame(parent, bg="#1a1a2e")

        # Instructions
        tk.Label(frame, text="Keep track of things you want to change or remember:",
                 bg="#1a1a2e", fg="white", font=('Arial', 11, 'bold')).pack(pady=10)

        # Input frame
        input_frame = tk.Frame(frame, bg="#1a1a2e")
        input_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(input_frame, text="Item:", bg="#1a1a2e", fg="white",
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
        self.thing_entry = tk.Entry(input_frame, font=('Arial', 10),
                                    bg="#2a2a3e", fg="white", width=40)
        self.thing_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Priority:", bg="#1a1a2e", fg="white",
                 font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5)
        self.priority_var = tk.StringVar(value="medium")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                      values=['low', 'medium', 'high'], state='readonly', width=10)
        priority_combo.grid(row=0, column=3, padx=5)

        tk.Button(input_frame, text="➕ Add", command=self._add_thing_to_change,
                  bg="#4CAF50", fg="white", font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=5)

        # List of things to change
        tk.Label(frame, text="Things to Change/Remember:", bg="#1a1a2e", fg="white",
                 font=('Arial', 11, 'bold')).pack(pady=(20, 5))

        self.things_listbox = tk.Listbox(frame, font=('Arial', 10),
                                         bg="#2a2a3e", fg="white",
                                         height=12)
        self.things_listbox.pack(fill='both', expand=True, padx=20, pady=5)

        btn_frame = tk.Frame(frame, bg="#1a1a2e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="✅ Mark Done", command=self._mark_thing_done,
                  bg="#4CAF50", fg="white", font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        tk.Button(btn_frame, text="🗑️ Remove", command=self._remove_thing,
                  bg="#f44336", fg="white", font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        tk.Button(btn_frame, text="🔄 Refresh", command=self._refresh_things_list,
                  bg="#2196F3", fg="white", font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        return frame

    def _create_stats_tab(self, parent):
        """Create statistics tab"""
        frame = tk.Frame(parent, bg="#1a1a2e")

        self.stats_text = scrolledtext.ScrolledText(frame, font=('Courier', 10),
                                                    bg="#2a2a3e", fg="white",
                                                    height=25, width=70)
        self.stats_text.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Button(frame, text="🔄 Refresh Stats", command=self._refresh_stats,
                  bg="#2196F3", fg="white", font=('Arial', 11, 'bold'),
                  padx=20, pady=8).pack(pady=10)

        return frame

    def _load_current_values(self):
        """Load current values from profile manager"""
        # Load user info
        user_info = self.profile_manager.get_user_info()
        for key, entry in self.user_info_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, user_info.get(key, ""))

        # Load preferences
        prefs = self.profile_manager.get_all_preferences()
        for key, widget in self.pref_entries.items():
            value = prefs.get(key, "")
            if isinstance(widget, tk.StringVar):
                widget.set(value)
            elif isinstance(widget, tk.BooleanVar):
                widget.set(value)
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, str(value))

        # Refresh lists
        self._refresh_custom_settings_list()
        self._refresh_things_list()
        self._refresh_stats()

    def _save_all(self):
        """Save all changes"""
        try:
            # Save user info
            user_info_updates = {}
            for key, entry in self.user_info_entries.items():
                user_info_updates[key] = entry.get()
            self.profile_manager.update_user_info(**user_info_updates)

            # Save preferences
            pref_updates = {}
            for key, widget in self.pref_entries.items():
                if isinstance(widget, tk.StringVar):
                    pref_updates[key] = widget.get()
                elif isinstance(widget, tk.BooleanVar):
                    pref_updates[key] = widget.get()
                elif isinstance(widget, tk.Entry):
                    value = widget.get()
                    # Try to convert to appropriate type
                    if key in ['voice_speed']:
                        pref_updates[key] = int(value) if value else 150
                    elif key in ['voice_volume']:
                        pref_updates[key] = float(value) if value else 1.0
                    else:
                        pref_updates[key] = value

            self.profile_manager.update_preferences(**pref_updates)

            messagebox.showinfo("Success", "✅ All settings saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"❌ Error saving settings: {e}")

    def _add_custom_setting(self):
        """Add a custom setting"""
        key = self.custom_key_entry.get().strip()
        value = self.custom_value_entry.get().strip()

        if not key:
            messagebox.showwarning("Warning", "Please enter a key!")
            return

        self.profile_manager.set_custom_setting(key, value)
        self.custom_key_entry.delete(0, tk.END)
        self.custom_value_entry.delete(0, tk.END)
        self._refresh_custom_settings_list()
        messagebox.showinfo("Success", f"✅ Added custom setting: {key}")

    def _remove_custom_setting(self):
        """Remove selected custom setting"""
        selection = self.custom_settings_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a setting to remove!")
            return

        item_text = self.custom_settings_listbox.get(selection[0])
        key = item_text.split(':')[0].strip()

        self.profile_manager.remove_custom_setting(key)
        self._refresh_custom_settings_list()
        messagebox.showinfo("Success", f"✅ Removed custom setting: {key}")

    def _refresh_custom_settings_list(self):
        """Refresh the custom settings list"""
        self.custom_settings_listbox.delete(0, tk.END)
        settings = self.profile_manager.get_all_custom_settings()
        for key, value in settings.items():
            self.custom_settings_listbox.insert(tk.END, f"{key}: {value}")

    def _add_thing_to_change(self):
        """Add a thing to change"""
        item = self.thing_entry.get().strip()
        priority = self.priority_var.get()

        if not item:
            messagebox.showwarning("Warning", "Please enter an item!")
            return

        self.profile_manager.add_thing_to_change(item, priority=priority)
        self.thing_entry.delete(0, tk.END)
        self._refresh_things_list()
        messagebox.showinfo("Success", f"✅ Added: {item}")

    def _mark_thing_done(self):
        """Mark selected thing as done"""
        selection = self.things_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to mark as done!")
            return

        index = selection[0]
        self.profile_manager.mark_thing_done(index)
        self._refresh_things_list()
        messagebox.showinfo("Success", "✅ Item marked as done!")

    def _remove_thing(self):
        """Remove selected thing"""
        selection = self.things_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove!")
            return

        index = selection[0]
        self.profile_manager.remove_thing_to_change(index)
        self._refresh_things_list()
        messagebox.showinfo("Success", "✅ Item removed!")

    def _refresh_things_list(self):
        """Refresh the things to change list"""
        self.things_listbox.delete(0, tk.END)
        things = self.profile_manager.get_things_to_change()
        for i, thing in enumerate(things):
            status = "✅" if thing['status'] == 'done' else "⏳"
            priority = thing.get('priority', 'medium').upper()
            item_text = f"{status} [{priority}] {thing['item']}"
            self.things_listbox.insert(tk.END, item_text)

    def _refresh_stats(self):
        """Refresh statistics display"""
        self.stats_text.delete('1.0', tk.END)

        # Get profile summary
        summary = self.profile_manager.get_profile_summary()
        self.stats_text.insert('1.0', summary)

        # Add favorite commands
        self.stats_text.insert(tk.END, "\n\n📊 TOP 10 FAVORITE COMMANDS:\n")
        self.stats_text.insert(tk.END, "═" * 50 + "\n")

        fav_commands = self.profile_manager.get_favorite_commands(10)
        for i, (command, count) in enumerate(fav_commands, 1):
            self.stats_text.insert(tk.END, f"{i:2}. {command:<30} ({count} times)\n")


def open_user_settings(parent):
    """Open the user settings dialog"""
    UserSettingsDialog(parent)
