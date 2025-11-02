"""
Desktop Sync Manager - Auto-download batch file and sync desktop files
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime


class DesktopSyncManager:
    """Manages desktop file synchronization and batch file distribution"""
    
    def __init__(self):
        # Get script directory for finding batch file
        self.script_dir = Path(__file__).parent.absolute()
        
        # Use actual Windows Desktop
        self.desktop = Path.home() / "Desktop"
        
        # Config files
        self.sync_config_file = "desktop_sync_config.json"
        self.batch_file_name = "desktop_file_controller.bat"
        self.batch_file = self.script_dir / self.batch_file_name
        self.downloads_ready_file = "downloads_ready.txt"
        
        # Detect OS
        self.is_windows = sys.platform.startswith('win')
        
    def prepare_batch_file_download(self):
        """Prepare batch file for local Windows use"""
        try:
            # Check if batch file exists in script directory
            if not self.batch_file.exists():
                # Provide helpful message for Windows users
                current_dir = os.getcwd()
                script_dir = str(self.script_dir)
                
                return {
                    "success": False,
                    "message": f"Batch file '{self.batch_file_name}' not found!\n" + 
                              f"   Current directory: {current_dir}\n" +
                              f"   Script directory: {script_dir}\n" +
                              f"   Looking for: {self.batch_file}\n\n" +
                              f"   💡 Please download '{self.batch_file_name}' from Replit\n" +
                              f"      and place it in: {script_dir}"
                }
            
            # Create ready-to-use instructions for local Windows
            instructions = f"""
╔══════════════════════════════════════════════════════════╗
║        DESKTOP FILE CONTROLLER - READY TO USE            ║
╚══════════════════════════════════════════════════════════╝

✅ Batch file found: {self.batch_file.name}
📂 Location: {self.batch_file}
📦 File size: {self.batch_file.stat().st_size} bytes
💻 System: Windows {'✓' if self.is_windows else '(Running on non-Windows OS)'}

🎯 QUICK START:
  1. Double-click '{self.batch_file.name}' to run
  2. Or run from command prompt:
     cd "{self.script_dir}"
     {self.batch_file.name}

📂 Managing your Desktop:
  - Desktop path: {self.desktop}
  - Use the batch file menu to organize files
  - Options 1-13 available for file management

💡 The batch file will manage YOUR real Windows desktop!

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            with open(self.downloads_ready_file, 'w', encoding='utf-8') as f:
                f.write(instructions)
            
            return {
                "success": True,
                "message": "Batch file ready to use on Windows",
                "instructions_file": self.downloads_ready_file,
                "batch_file": str(self.batch_file),
                "file_size": self.batch_file.stat().st_size
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error preparing batch file: {str(e)}"
            }
    
    def scan_desktop(self):
        """Scan and analyze desktop files and folders"""
        try:
            if not self.desktop.exists():
                return {
                    "success": False,
                    "message": f"Desktop not found at {self.desktop}"
                }
            
            scan_data = {
                "scan_time": datetime.now().isoformat(),
                "desktop_path": str(self.desktop),
                "folders": [],
                "files": [],
                "statistics": {
                    "total_folders": 0,
                    "total_files": 0,
                    "total_size_bytes": 0,
                    "file_types": {}
                }
            }
            
            for item in self.desktop.iterdir():
                item_info = {
                    "name": item.name,
                    "path": str(item),
                    "size": item.stat().st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }
                
                if item.is_dir():
                    # Count items in folder
                    try:
                        item_count = len(list(item.iterdir()))
                        item_info["item_count"] = item_count
                    except:
                        item_info["item_count"] = 0
                    scan_data["folders"].append(item_info)
                    scan_data["statistics"]["total_folders"] += 1
                else:
                    # Get file extension
                    ext = item.suffix.lower() if item.suffix else "no_extension"
                    item_info["extension"] = ext
                    scan_data["files"].append(item_info)
                    scan_data["statistics"]["total_files"] += 1
                    scan_data["statistics"]["total_size_bytes"] += item_info["size"]
                    
                    # Track file types
                    if ext in scan_data["statistics"]["file_types"]:
                        scan_data["statistics"]["file_types"][ext] += 1
                    else:
                        scan_data["statistics"]["file_types"][ext] = 1
            
            return {
                "success": True,
                "data": scan_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error scanning desktop: {str(e)}"
            }
    
    def save_desktop_data(self, scan_data):
        """Save scanned desktop data to JSON file"""
        try:
            json_file = self.script_dir / "desktop_data.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(scan_data, f, indent=2)
            
            return {
                "success": True,
                "file": str(json_file),
                "message": "Desktop data saved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error saving data: {str(e)}"
            }
    
    def load_desktop_data(self):
        """Load previously saved desktop data"""
        try:
            json_file = self.script_dir / "desktop_data.json"
            if not json_file.exists():
                return {
                    "success": False,
                    "message": "No saved desktop data found"
                }
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                "success": True,
                "data": data
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error loading data: {str(e)}"
            }
    
    def display_desktop_summary(self, scan_data):
        """Display a summary of the desktop scan"""
        stats = scan_data["statistics"]
        
        print("\n" + "="*60)
        print("📊 DESKTOP ANALYSIS SUMMARY")
        print("="*60)
        print(f"📂 Desktop Location: {scan_data['desktop_path']}")
        print(f"📅 Scanned: {datetime.fromisoformat(scan_data['scan_time']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n📁 Total Folders: {stats['total_folders']}")
        print(f"📄 Total Files: {stats['total_files']}")
        print(f"💾 Total Size: {self.format_size(stats['total_size_bytes'])}")
        
        if stats["file_types"]:
            print(f"\n📑 File Types Found:")
            for ext, count in sorted(stats["file_types"].items(), key=lambda x: x[1], reverse=True)[:10]:
                ext_display = ext if ext != "no_extension" else "(no extension)"
                print(f"   {ext_display}: {count} file(s)")
        
        if scan_data["folders"]:
            print(f"\n📂 Folders on Desktop:")
            for folder in scan_data["folders"][:15]:
                print(f"   • {folder['name']} ({folder['item_count']} items)")
            if len(scan_data["folders"]) > 15:
                print(f"   ... and {len(scan_data['folders']) - 15} more folders")
        
        print("="*60 + "\n")
    
    def format_size(self, bytes):
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"
    
    def create_desktop_structure_json(self):
        """Create JSON representation of desktop structure (legacy method)"""
        scan_result = self.scan_desktop()
        if not scan_result["success"]:
            return scan_result
        
        save_result = self.save_desktop_data(scan_result["data"])
        
        return {
            "success": True,
            "structure": scan_result["data"],
            "json_file": save_result.get("file", "desktop_data.json"),
            "total_folders": scan_result["data"]["statistics"]["total_folders"],
            "total_files": scan_result["data"]["statistics"]["total_files"]
        }
    
    def setup_sample_desktop(self):
        """Create sample desktop structure for testing"""
        try:
            # Create desktop if it doesn't exist
            self.desktop.mkdir(parents=True, exist_ok=True)
            
            # Create sample folders
            sample_folders = [
                "coding",
                "projects", 
                "documents",
                "downloads",
                "work",
                "personal"
            ]
            
            created = []
            for folder in sample_folders:
                folder_path = self.desktop / folder
                if not folder_path.exists():
                    folder_path.mkdir()
                    created.append(folder)
                    
                    # Add sample files
                    if folder == "coding":
                        (folder_path / "main.py").write_text("# Python code here")
                        (folder_path / "app.js").write_text("// JavaScript code here")
                    elif folder == "documents":
                        (folder_path / "notes.txt").write_text("Sample notes")
                        (folder_path / "report.txt").write_text("Sample report")
            
            return {
                "success": True,
                "created_folders": created,
                "total_folders": len(sample_folders),
                "desktop_path": str(self.desktop)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error setting up desktop: {str(e)}"
            }
    
    def auto_startup_sequence(self):
        """Run automatic startup sequence"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        # Step 1: Setup sample desktop (if empty)
        setup_result = self.setup_sample_desktop()
        results["steps"].append({
            "step": "Setup Desktop Structure",
            "status": "success" if setup_result["success"] else "failed",
            "details": setup_result
        })
        
        # Step 2: Prepare batch file download
        batch_result = self.prepare_batch_file_download()
        results["steps"].append({
            "step": "Prepare Batch File",
            "status": "success" if batch_result["success"] else "failed",
            "details": batch_result
        })
        
        # Step 3: Create desktop structure JSON
        structure_result = self.create_desktop_structure_json()
        results["steps"].append({
            "step": "Create Desktop Structure",
            "status": "success" if structure_result["success"] else "failed",
            "details": structure_result
        })
        
        # Overall success
        results["success"] = all(
            step["status"] == "success" for step in results["steps"]
        )
        
        return results
    
    def get_download_instructions(self):
        """Get formatted download instructions"""
        if os.path.exists(self.downloads_ready_file):
            with open(self.downloads_ready_file, 'r') as f:
                return f.read()
        return "Download instructions not generated yet. Run auto_startup_sequence() first."


def interactive_startup():
    """Interactive startup - scans desktop and asks user what to do"""
    print("\n" + "="*60)
    print("🚀 DESKTOP FILE & FOLDER AUTOMATOR")
    print("="*60)
    
    manager = DesktopSyncManager()
    
    # Step 1: Scan the desktop
    print("\n🔍 Scanning your desktop...")
    scan_result = manager.scan_desktop()
    
    if not scan_result["success"]:
        print(f"❌ Error: {scan_result['message']}")
        return
    
    scan_data = scan_result["data"]
    
    # Step 2: Display summary
    manager.display_desktop_summary(scan_data)
    
    # Step 3: Save the data
    print("💾 Saving desktop data...")
    save_result = manager.save_desktop_data(scan_data)
    if save_result["success"]:
        print(f"✅ Data saved to: {save_result['file']}\n")
    
    # Step 4: Ask user what to do
    print("="*60)
    print("📋 WHAT WOULD YOU LIKE TO DO?")
    print("="*60)
    print("1. 📥 Download/Setup batch file controller")
    print("2. 🗂️  View detailed file analysis")
    print("3. 🔄 Re-scan desktop")
    print("4. 🚀 Launch desktop automation (batch file)")
    print("5. 📊 View saved desktop history")
    print("6. ❌ Exit")
    print("="*60)
    
    try:
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\n🔧 Setting up batch file...")
            batch_result = manager.prepare_batch_file_download()
            if batch_result["success"]:
                print(f"✅ {batch_result['message']}")
                print(f"\n📂 Batch file location: {batch_result['batch_file']}")
                if manager.is_windows:
                    print("\n🚀 You can now run the batch file:")
                    print(f"   Double-click: {manager.batch_file_name}")
                    launch = input("\n🚀 Launch batch file now? (y/n): ").strip().lower()
                    if launch == 'y':
                        os.system(f'start cmd /k "{manager.batch_file}"')
            else:
                print(f"❌ {batch_result['message']}")
        
        elif choice == "2":
            print("\n📊 DETAILED FILE ANALYSIS")
            print("="*60)
            print(f"Total items: {len(scan_data['files']) + len(scan_data['folders'])}")
            if scan_data['files']:
                print(f"\n📄 Files ({len(scan_data['files'])}):")
                for file in scan_data['files'][:20]:
                    size = manager.format_size(file['size'])
                    print(f"   • {file['name']} ({size}) - {file['extension']}")
                if len(scan_data['files']) > 20:
                    print(f"   ... and {len(scan_data['files']) - 20} more files")
        
        elif choice == "3":
            print("\n🔄 Re-scanning desktop...")
            interactive_startup()
            return
        
        elif choice == "4":
            if manager.batch_file.exists():
                print(f"\n🚀 Launching {manager.batch_file_name}...")
                if manager.is_windows:
                    os.system(f'start cmd /k "{manager.batch_file}"')
                else:
                    print("❌ Batch file can only run on Windows")
            else:
                print(f"❌ Batch file not found. Please download it first (option 1)")
        
        elif choice == "5":
            load_result = manager.load_desktop_data()
            if load_result["success"]:
                print("\n📊 SAVED DESKTOP DATA:")
                manager.display_desktop_summary(load_result["data"])
            else:
                print(f"❌ {load_result['message']}")
        
        elif choice == "6":
            print("\n👋 Goodbye!")
            return
        
        else:
            print("\n⚠️  Invalid choice. Please select 1-6.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        return
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    # Ask if user wants to continue
    print("\n" + "="*60)
    continue_choice = input("📋 Continue with another action? (y/n): ").strip().lower()
    if continue_choice == 'y':
        interactive_startup()
    else:
        print("\n✅ Desktop data has been saved.")
        print(f"💡 Run this script anytime to manage your desktop!")
        print(f"🚀 Or double-click '{manager.batch_file_name}' for quick access\n")


def auto_initialize_on_gui_start():
    """Called automatically when GUI starts (legacy function)"""
    print("\n" + "="*60)
    print("🚀 DESKTOP SYNC MANAGER - AUTO STARTUP")
    print("="*60)
    
    manager = DesktopSyncManager()
    results = manager.auto_startup_sequence()
    
    print("\n📊 Startup Sequence Results:")
    print("-"*60)
    
    for step in results["steps"]:
        status_icon = "✅" if step["status"] == "success" else "❌"
        print(f"{status_icon} {step['step']}: {step['status'].upper()}")
        
        if "details" in step:
            details = step["details"]
            if step["status"] == "success":
                if "created_folders" in details and details["created_folders"]:
                    print(f"   Created: {', '.join(details['created_folders'])}")
                if "total_folders" in details:
                    print(f"   Total folders: {details['total_folders']}")
                if "batch_file" in details:
                    print(f"   Batch file: {details['batch_file']}")
            else:
                if "message" in details:
                    for line in details["message"].split('\n'):
                        if line.strip():
                            print(f"   {line}")
    
    print("\n" + "="*60)
    
    if results["success"]:
        print("✅ ALL SYSTEMS READY!")
        if manager.is_windows:
            print(f"\n🚀 READY TO USE: Double-click '{manager.batch_file_name}'")
            print(f"   Location: {manager.batch_file}")
        else:
            print("\n📥 DOWNLOAD YOUR BATCH FILE:")
            print(f"   Right-click '{manager.batch_file_name}' → Download to Windows PC")
        print("\n📂 Desktop synchronized with test folders")
        print(f"   View: {manager.desktop}")
    else:
        print("⚠️  Some steps had issues. Check details above.")
    
    print("="*60 + "\n")
    
    return results


if __name__ == "__main__":
    # Run interactive startup
    interactive_startup()
