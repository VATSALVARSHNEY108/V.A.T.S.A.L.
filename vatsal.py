#!/usr/bin/env python3
"""
VATSAL AI Desktop Automation - Startup Script
Properly configures Python paths and launches the GUI
"""

import sys
import os

# Add all module directories to Python path
workspace_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(workspace_dir, 'modules')

# Add modules and all subdirectories to path
sys.path.insert(0, workspace_dir)
sys.path.insert(0, modules_dir)
sys.path.insert(0, os.path.join(modules_dir, 'core'))
sys.path.insert(0, os.path.join(modules_dir, 'automation'))
sys.path.insert(0, os.path.join(modules_dir, 'ai_features'))
sys.path.insert(0, os.path.join(modules_dir, 'utilities'))
sys.path.insert(0, os.path.join(modules_dir, 'communication'))
sys.path.insert(0, os.path.join(modules_dir, 'monitoring'))
sys.path.insert(0, os.path.join(modules_dir, 'web'))
sys.path.insert(0, os.path.join(modules_dir, 'system'))
sys.path.insert(0, os.path.join(modules_dir, 'productivity'))
sys.path.insert(0, os.path.join(modules_dir, 'security'))
sys.path.insert(0, os.path.join(modules_dir, 'file_management'))
sys.path.insert(0, os.path.join(modules_dir, 'development'))
sys.path.insert(0, os.path.join(modules_dir, 'voice'))
sys.path.insert(0, os.path.join(modules_dir, 'integration'))
sys.path.insert(0, os.path.join(modules_dir, 'intelligence'))
sys.path.insert(0, os.path.join(modules_dir, 'network'))
sys.path.insert(0, os.path.join(modules_dir, 'data_analysis'))
sys.path.insert(0, os.path.join(modules_dir, 'smart_features'))
sys.path.insert(0, os.path.join(modules_dir, 'misc'))

def main():
    """Launch the GUI application"""
    print("🚀 Starting VATSAL AI Desktop Automation...")
    print("=" * 60)
    
    try:
        # Import and run the GUI
        from modules.core.gui_app import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
