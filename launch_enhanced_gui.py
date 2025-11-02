#!/usr/bin/env python3
"""
Launch Enhanced Modern GUI for VATSAL AI
Beautiful, modern interface with animations and better UX
"""

import sys
import os

# Add module paths
workspace_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(workspace_dir, 'modules')
sys.path.insert(0, workspace_dir)
sys.path.insert(0, modules_dir)
sys.path.insert(0, os.path.join(modules_dir, 'core'))


def main():
    """Launch the enhanced GUI"""
    try:
        print("✨ Starting Enhanced VATSAL AI GUI...")
        print("=" * 60)
        print("🎨 Modern Design | 🚀 Fast Performance | 💎 Beautiful UX")
        print("=" * 60)

        from modules.core.enhanced_gui import main as gui_main
        gui_main()

    except ImportError as e:
        print(f"❌ Error: Could not import enhanced GUI - {e}")
        print("\nMake sure tkinter is installed.")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
