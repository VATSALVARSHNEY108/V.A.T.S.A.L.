"""
Organize the entire VATSAL AI project into a clean folder structure
"""

import os
import shutil
from pathlib import Path

# Define the organized folder structure
FOLDER_STRUCTURE = {
    "core": [
        "vatsal_ai.py",
        "vatsal_assistant.py",
        "main.py",
        "gui_app.py",
        "command_executor.py",
        "gemini_controller.py",
    ],
    
    "ai_features": [
        "code_generator.py",
        "code_templates.py",
        "screenshot_analysis.py",
        "multimodal_ai_core.py",
        "ai_features.py",
        "advanced_ai_automation.py",
        "advanced_ai_integration.py",
        "virtual_language_model.py",
    ],
    
    "automation": [
        "gui_automation.py",
        "desktop_controller_advanced.py",
        "comprehensive_desktop_controller.py",
        "self_operating_computer.py",
        "self_operating_coordinator.py",
        "self_operating_integrations.py",
        "intelligent_task_automator.py",
        "macro_recorder.py",
        "file_automation.py",
        "download_organizer.py",
    ],
    
    "monitoring": [
        "smart_screen_monitor.py",
        "advanced_smart_screen_monitor.py",
        "ai_screen_monitoring_system.py",
        "chat_monitor.py",
        "visual_chat_monitor.py",
        "activity_monitoring.py",
        "screen_suggester.py",
        "quick_screen_analysis.py",
    ],
    
    "intelligence": [
        "contextual_memory_enhanced.py",
        "correction_learning.py",
        "predictive_actions_engine.py",
        "behavioral_learning.py",
        "conversation_memory.py",
        "desktop_rag.py",
        "data_intelligence.py",
    ],
    
    "communication": [
        "whatsapp_automation.py",
        "email_sender.py",
        "quick_email.py",
        "messaging_service.py",
        "communication_enhancements.py",
        "translation_service.py",
    ],
    
    "utilities": [
        "spotify_automation.py",
        "spotify_desktop_automation.py",
        "youtube_automation.py",
        "weather_news_service.py",
        "advanced_calculator.py",
        "calendar_manager.py",
        "contact_manager.py",
        "password_vault.py",
        "quick_notes.py",
    ],
    
    "web": [
        "web_automation.py",
        "web_automation_advanced.py",
        "selenium_web_automator.py",
        "web_tools_launcher.py",
    ],
    
    "system": [
        "system_control.py",
        "system_monitor.py",
        "quick_system_commands.py",
    ],
    
    "security": [
        "security_dashboard.py",
        "security_enhancements.py",
        "enhanced_biometric_auth.py",
        "two_factor_authentication.py",
        "encrypted_storage_manager.py",
    ],
    
    "productivity": [
        "productivity_dashboard.py",
        "productivity_monitor.py",
        "pomodoro_ai_coach.py",
        "smart_break_suggester.py",
        "task_time_predictor.py",
        "focus_mode.py",
        "energy_level_tracker.py",
        "distraction_detector.py",
    ],
    
    "file_management": [
        "file_manager.py",
        "advanced_file_operations.py",
        "workspace_manager.py",
        "desktop_sync_manager.py",
    ],
    
    "voice": [
        "voice_assistant.py",
        "voice_commander.py",
        "voice_sounds.py",
    ],
    
    "network": [
        "websocket_server.py",
        "websocket_client.py",
        "mobile_companion_server.py",
        "mobile_api.py",
        "mobile_auth.py",
    ],
    
    "smart_features": [
        "smart_automation.py",
        "smart_typing.py",
        "clipboard_text_handler.py",
        "nl_workflow_builder.py",
        "workflow_templates.py",
        "app_scheduler.py",
    ],
    
    "integration": [
        "command_executor_integration.py",
        "desktop_controller_integration.py",
        "vatsal_enhanced_modules.py",
        "cloud_ecosystem.py",
        "ecosystem_manager.py",
        "human_interaction.py",
        "tools_mapper.py",
    ],
    
    "data_analysis": [
        "data_analysis.py",
        "analyze_screenshot.py",
    ],
    
    "development": [
        "code_executor.py",
        "code_snippet_library.py",
        "sandbox_mode.py",
    ],
    
    "misc": [
        "creative_utilities.py",
        "collaboration_tools.py",
        "notification_service.py",
    ],
}

# Files to keep in root
ROOT_FILES = [
    "vatsal_desktop_automator.py",
    "vatsal_chatbot.py",
    "simple_chatbot.py",
    "vnc_web_viewer.py",
    "start_gui_with_vnc.sh",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
    "replit.md",
]

# Test files pattern
TEST_FILES_PATTERN = "test_*.py"

# Documentation files
DOC_EXTENSIONS = [".md", ".txt"]

# Config files
CONFIG_EXTENSIONS = [".json", ".bat", ".html"]

def organize_project():
    """Organize all project files into folders"""
    
    base_path = Path("/home/runner/workspace")
    
    # Create main folders
    folders_to_create = [
        "modules",  # For all organized code
        "tests",
        "docs",
        "config",
        "data",
        "scripts",
    ]
    
    print("📁 Creating folder structure...")
    for folder in folders_to_create:
        folder_path = base_path / folder
        folder_path.mkdir(exist_ok=True)
        print(f"   ✓ Created: {folder}/")
    
    # Create subfolders in modules
    print("\n📦 Creating module subfolders...")
    modules_path = base_path / "modules"
    for category in FOLDER_STRUCTURE.keys():
        category_path = modules_path / category
        category_path.mkdir(exist_ok=True)
        print(f"   ✓ Created: modules/{category}/")
    
    # Move files to their categories
    print("\n📦 Organizing Python modules...")
    moved_count = 0
    for category, files in FOLDER_STRUCTURE.items():
        for filename in files:
            src = base_path / filename
            if src.exists() and src.is_file():
                dst = modules_path / category / filename
                try:
                    shutil.move(str(src), str(dst))
                    print(f"   ✓ Moved: {filename} → modules/{category}/")
                    moved_count += 1
                except Exception as e:
                    print(f"   ✗ Error moving {filename}: {e}")
    
    # Move test files
    print("\n🧪 Organizing test files...")
    test_count = 0
    for test_file in base_path.glob("test_*.py"):
        if test_file.is_file():
            dst = base_path / "tests" / test_file.name
            try:
                shutil.move(str(test_file), str(dst))
                print(f"   ✓ Moved: {test_file.name} → tests/")
                test_count += 1
            except Exception as e:
                print(f"   ✗ Error moving {test_file.name}: {e}")
    
    # Move documentation files
    print("\n📚 Organizing documentation...")
    doc_count = 0
    for doc_ext in DOC_EXTENSIONS:
        for doc_file in base_path.glob(f"*{doc_ext}"):
            if doc_file.is_file() and doc_file.name != "replit.md":
                dst = base_path / "docs" / doc_file.name
                try:
                    shutil.move(str(doc_file), str(dst))
                    print(f"   ✓ Moved: {doc_file.name} → docs/")
                    doc_count += 1
                except Exception as e:
                    print(f"   ✗ Error moving {doc_file.name}: {e}")
    
    # Move config files
    print("\n⚙️  Organizing config files...")
    config_count = 0
    for config_file in base_path.glob("*.json"):
        if config_file.is_file():
            dst = base_path / "config" / config_file.name
            try:
                shutil.move(str(config_file), str(dst))
                print(f"   ✓ Moved: {config_file.name} → config/")
                config_count += 1
            except Exception as e:
                print(f"   ✗ Error moving {config_file.name}: {e}")
    
    for config_file in base_path.glob("*.bat"):
        if config_file.is_file():
            dst = base_path / "scripts" / config_file.name
            try:
                shutil.move(str(config_file), str(dst))
                print(f"   ✓ Moved: {config_file.name} → scripts/")
                config_count += 1
            except Exception as e:
                print(f"   ✗ Error moving {config_file.name}: {e}")
    
    # Move standalone HTML files
    for html_file in base_path.glob("*.html"):
        if html_file.is_file():
            dst = base_path / "scripts" / html_file.name
            try:
                shutil.move(str(html_file), str(dst))
                print(f"   ✓ Moved: {html_file.name} → scripts/")
                config_count += 1
            except Exception as e:
                print(f"   ✗ Error moving {html_file.name}: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("✅ PROJECT ORGANIZATION COMPLETE!")
    print("="*70)
    print(f"   📦 Python modules organized: {moved_count}")
    print(f"   🧪 Test files organized: {test_count}")
    print(f"   📚 Documentation files organized: {doc_count}")
    print(f"   ⚙️  Config/script files organized: {config_count}")
    print("\n📁 New folder structure:")
    print("   ├── modules/        (All organized Python code)")
    print("   ├── tests/          (All test files)")
    print("   ├── docs/           (All documentation)")
    print("   ├── config/         (JSON configs)")
    print("   ├── scripts/        (BAT and HTML scripts)")
    print("   ├── data/           (Runtime data)")
    print("   └── [root files]    (Main entry points)")

if __name__ == "__main__":
    organize_project()
