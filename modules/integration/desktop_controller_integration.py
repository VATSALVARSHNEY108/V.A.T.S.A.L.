"""
Desktop File Controller Integration
Provides integration between the batch file and Python GUI application
"""

import os
import subprocess
import platform
import shutil
from pathlib import Path


class DesktopFileController:
    """Manages desktop files and folders with cross-platform support"""
    
    def __init__(self):
        self.desktop_path = self._get_desktop_path()
        self.bat_file = "desktop_file_controller.bat"
        
    def _get_desktop_path(self):
        """Get desktop path for current OS"""
        if platform.system() == "Windows":
            return Path.home() / "Desktop"
        elif platform.system() == "Darwin":
            return Path.home() / "Desktop"
        else:
            return Path.home() / "Desktop"
    
    def launch_batch_controller(self):
        """Launch the Windows batch file controller"""
        if platform.system() != "Windows":
            return {
                "success": False,
                "message": "Batch file controller is Windows-only. Use Python methods instead."
            }
        
        if not os.path.exists(self.bat_file):
            return {
                "success": False,
                "message": f"Batch file not found: {self.bat_file}"
            }
        
        try:
            subprocess.Popen([self.bat_file], shell=True)
            return {
                "success": True,
                "message": "Desktop File Controller launched successfully!"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error launching controller: {str(e)}"
            }
    
    def create_folder(self, folder_name):
        """Create a new folder on desktop"""
        try:
            folder_path = self.desktop_path / folder_name
            folder_path.mkdir(exist_ok=True)
            return {
                "success": True,
                "message": f"Folder '{folder_name}' created successfully!",
                "path": str(folder_path)
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def delete_item(self, item_name):
        """Delete a file or folder from desktop"""
        try:
            item_path = self.desktop_path / item_name
            if not item_path.exists():
                return {"success": False, "message": f"'{item_name}' not found on desktop"}
            
            if item_path.is_dir():
                shutil.rmtree(item_path)
            else:
                item_path.unlink()
            
            return {"success": True, "message": f"'{item_name}' deleted successfully!"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def move_item(self, source, destination):
        """Move file or folder to destination"""
        try:
            src_path = self.desktop_path / source
            dst_path = self.desktop_path / destination
            
            if not src_path.exists():
                return {"success": False, "message": f"'{source}' not found"}
            
            dst_path.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path / source))
            
            return {
                "success": True,
                "message": f"Moved '{source}' to '{destination}'"
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def copy_item(self, source, destination):
        """Copy file or folder to destination"""
        try:
            src_path = self.desktop_path / source
            dst_path = self.desktop_path / destination
            
            if not src_path.exists():
                return {"success": False, "message": f"'{source}' not found"}
            
            dst_path.mkdir(parents=True, exist_ok=True)
            
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path / source, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path / source.name)
            
            return {
                "success": True,
                "message": f"Copied '{source}' to '{destination}'"
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def rename_item(self, old_name, new_name):
        """Rename a file or folder"""
        try:
            old_path = self.desktop_path / old_name
            new_path = self.desktop_path / new_name
            
            if not old_path.exists():
                return {"success": False, "message": f"'{old_name}' not found"}
            
            old_path.rename(new_path)
            return {
                "success": True,
                "message": f"Renamed '{old_name}' to '{new_name}'"
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def list_items(self):
        """List all items on desktop"""
        try:
            items = []
            for item in self.desktop_path.iterdir():
                item_type = "Folder" if item.is_dir() else "File"
                items.append({
                    "name": item.name,
                    "type": item_type,
                    "path": str(item)
                })
            
            return {
                "success": True,
                "items": items,
                "count": len(items)
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def organize_by_type(self):
        """Organize desktop files by type"""
        try:
            categories = {
                'Documents': ['.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx'],
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
                'Music': ['.mp3', '.wav', '.flac'],
                'Archives': ['.zip', '.rar', '.7z'],
                'Programs': ['.exe', '.msi']
            }
            
            moved_count = 0
            for category, extensions in categories.items():
                category_path = self.desktop_path / category
                category_path.mkdir(exist_ok=True)
                
                for ext in extensions:
                    for file in self.desktop_path.glob(f'*{ext}'):
                        if file.is_file():
                            shutil.move(str(file), str(category_path / file.name))
                            moved_count += 1
            
            return {
                "success": True,
                "message": f"Desktop organized! {moved_count} files moved."
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def search_files(self, search_term):
        """Search for files on desktop"""
        try:
            results = []
            for item in self.desktop_path.rglob(f'*{search_term}*'):
                results.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "Folder" if item.is_dir() else "File"
                })
            
            return {
                "success": True,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}


def add_to_gui(gui_instance):
    """
    Helper function to add Desktop Controller button to existing GUI
    
    Example usage in your GUI:
        from desktop_controller_integration import add_to_gui
        add_to_gui(self)
    """
    import tkinter as tk
    import threading
    
    controller = DesktopFileController()
    
    def launch_controller():
        """Launch the desktop file controller"""
        def execute():
            gui_instance.update_output("\n🗂️ Desktop File Controller\n", "command")
            gui_instance.update_output("=" * 60 + "\n", "info")
            
            result = controller.launch_batch_controller()
            
            if result["success"]:
                gui_instance.update_output(f"✅ {result['message']}\n", "success")
            else:
                gui_instance.update_output(f"ℹ️ {result['message']}\n", "info")
                gui_instance.update_output("\nPython alternatives available:\n", "info")
                gui_instance.update_output("• Create Folder\n", "info")
                gui_instance.update_output("• Organize Desktop\n", "info")
                gui_instance.update_output("• Search Files\n", "info")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def organize_desktop():
        """Organize desktop files by type"""
        def execute():
            gui_instance.update_output("\n📁 Organizing Desktop...\n", "command")
            gui_instance.update_output("=" * 60 + "\n", "info")
            
            result = controller.organize_by_type()
            
            if result["success"]:
                gui_instance.update_output(f"✅ {result['message']}\n", "success")
            else:
                gui_instance.update_output(f"❌ {result['message']}\n", "error")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def create_folder_gui():
        """Create folder with GUI dialog"""
        def execute():
            folder_name = gui_instance.show_input_dialog(
                "Create Folder",
                "Enter folder name:"
            )
            
            if folder_name:
                gui_instance.update_output("\n📁 Creating Folder...\n", "command")
                result = controller.create_folder(folder_name)
                
                if result["success"]:
                    gui_instance.update_output(f"✅ {result['message']}\n", "success")
                    gui_instance.update_output(f"Path: {result['path']}\n", "info")
                else:
                    gui_instance.update_output(f"❌ {result['message']}\n", "error")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def list_desktop():
        """List all desktop items"""
        def execute():
            gui_instance.update_output("\n🗂️ Desktop Contents\n", "command")
            gui_instance.update_output("=" * 60 + "\n", "info")
            
            result = controller.list_items()
            
            if result["success"]:
                gui_instance.update_output(f"Total items: {result['count']}\n\n", "success")
                
                for item in result["items"][:20]:
                    icon = "📁" if item["type"] == "Folder" else "📄"
                    gui_instance.update_output(f"{icon} {item['name']}\n", "info")
                
                if result['count'] > 20:
                    gui_instance.update_output(f"\n... and {result['count'] - 20} more items\n", "info")
            else:
                gui_instance.update_output(f"❌ {result['message']}\n", "error")
        
        threading.Thread(target=execute, daemon=True).start()
    
    return {
        "launch_controller": launch_controller,
        "organize_desktop": organize_desktop,
        "create_folder": create_folder_gui,
        "list_desktop": list_desktop
    }


if __name__ == "__main__":
    controller = DesktopFileController()
    
    print("🗂️ Desktop File Controller - Python Version")
    print("=" * 50)
    print(f"Desktop Path: {controller.desktop_path}")
    print("\nAvailable Commands:")
    print("1. List desktop items")
    print("2. Create folder")
    print("3. Organize desktop")
    print("4. Launch Windows Batch Controller")
    
    while True:
        choice = input("\nEnter choice (1-4, 'q' to quit): ").strip()
        
        if choice == 'q':
            break
        elif choice == '1':
            result = controller.list_items()
            if result["success"]:
                print(f"\n📁 Desktop has {result['count']} items:")
                for item in result["items"]:
                    print(f"  {item['type']}: {item['name']}")
        elif choice == '2':
            name = input("Folder name: ")
            result = controller.create_folder(name)
            print(result["message"])
        elif choice == '3':
            result = controller.organize_by_type()
            print(result["message"])
        elif choice == '4':
            result = controller.launch_batch_controller()
            print(result["message"])
