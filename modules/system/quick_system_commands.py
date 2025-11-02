"""
Quick System Commands - Direct execution without API calls
Use this for instant system control without relying on Gemini API
"""

import sys
from system_control import SystemController

def main():
    controller = SystemController()
    
    if len(sys.argv) < 2:
        print("\n🎮 QUICK SYSTEM COMMANDS")
        print("=" * 50)
        print("Usage: python quick_system_commands.py <command>")
        print("\nAvailable commands:")
        print("  lock         - Lock screen")
        print("  shutdown     - Shutdown computer (10 sec delay)")
        print("  shutdown-now - Shutdown immediately")
        print("  restart      - Restart computer (10 sec delay)")
        print("  restart-now  - Restart immediately")
        print("  cancel       - Cancel shutdown/restart")
        print("\nExample: python quick_system_commands.py lock")
        return
    
    command = sys.argv[1].lower()
    
    if command == "lock":
        print(controller.lock_screen())
    
    elif command == "shutdown":
        print(controller.shutdown_system(10))
    
    elif command == "shutdown-now":
        print(controller.shutdown_system(0))
    
    elif command == "restart":
        print(controller.restart_system(10))
    
    elif command == "restart-now":
        print(controller.restart_system(0))
    
    elif command == "cancel":
        print(controller.cancel_shutdown_restart())
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments to see available commands")

if __name__ == "__main__":
    main()
