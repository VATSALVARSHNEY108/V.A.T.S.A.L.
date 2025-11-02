#!/usr/bin/env python3
"""
File & Folder Automation Module
Provides automatic file renaming, folder monitoring, and compression automation
"""

import os
import re
import shutil
import zipfile
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileAutomation:
    """Comprehensive file and folder automation system"""
    
    def __init__(self):
        self.monitors = {}
        self.observers = {}
        print("📁 File Automation System initialized")
    
    # ==========================================
    # FEATURE 1: Automatic File Renaming
    # ==========================================
    
    def rename_files_by_pattern(self, directory: str, pattern_type: str = "date", 
                                file_extension: str = "*", prefix: str = "", 
                                suffix: str = "") -> Dict:
        """
        Automatically rename files based on patterns
        
        Args:
            directory: Target directory path
            pattern_type: 'date', 'type', 'project', 'sequential'
            file_extension: File type to rename (e.g., '.jpg', '.pdf', or '*' for all)
            prefix: Optional prefix to add
            suffix: Optional suffix to add
            
        Returns:
            Dictionary with rename statistics
        """
        try:
            if not os.path.exists(directory):
                return {"success": False, "error": "Directory not found"}
            
            renamed_count = 0
            failed_count = 0
            renamed_files = []
            
            # Get all files matching extension
            files = []
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    if file_extension == "*" or file.endswith(file_extension):
                        files.append(file)
            
            # Sort files by modification time for consistent ordering
            files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)))
            
            for index, filename in enumerate(files, start=1):
                old_path = os.path.join(directory, filename)
                name, ext = os.path.splitext(filename)
                
                # Generate new name based on pattern
                if pattern_type == "date":
                    # Use file modification date
                    mod_time = os.path.getmtime(old_path)
                    date_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
                    new_name = f"{prefix}{date_str}_{index:03d}{suffix}{ext}"
                
                elif pattern_type == "type":
                    # Rename by file type/extension
                    file_type = ext[1:].upper() if ext else "FILE"
                    new_name = f"{prefix}{file_type}_{index:03d}{suffix}{ext}"
                
                elif pattern_type == "project":
                    # Use parent folder name as project identifier
                    project_name = os.path.basename(directory)
                    new_name = f"{prefix}{project_name}_{index:03d}{suffix}{ext}"
                
                elif pattern_type == "sequential":
                    # Simple sequential numbering
                    new_name = f"{prefix}{index:03d}{suffix}{ext}"
                
                else:
                    failed_count += 1
                    continue
                
                new_path = os.path.join(directory, new_name)
                
                # Check if file already exists
                if os.path.exists(new_path):
                    # Add timestamp to avoid collision
                    timestamp = datetime.now().strftime("%H%M%S")
                    name_part, ext_part = os.path.splitext(new_name)
                    new_name = f"{name_part}_{timestamp}{ext_part}"
                    new_path = os.path.join(directory, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    renamed_count += 1
                    renamed_files.append({
                        "old": filename,
                        "new": new_name
                    })
                except Exception as e:
                    failed_count += 1
                    print(f"Failed to rename {filename}: {e}")
            
            return {
                "success": True,
                "renamed_count": renamed_count,
                "failed_count": failed_count,
                "renamed_files": renamed_files,
                "pattern_type": pattern_type
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def bulk_rename_with_template(self, directory: str, template: str) -> Dict:
        """
        Rename files using a custom template
        Template variables: {date}, {time}, {ext}, {num}, {name}
        
        Example: "Document_{date}_{num}{ext}"
        """
        try:
            if not os.path.exists(directory):
                return {"success": False, "error": "Directory not found"}
            
            files = [f for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))]
            files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)))
            
            renamed_count = 0
            renamed_files = []
            
            for index, filename in enumerate(files, start=1):
                old_path = os.path.join(directory, filename)
                name, ext = os.path.splitext(filename)
                
                # Get file date
                mod_time = os.path.getmtime(old_path)
                file_date = datetime.fromtimestamp(mod_time).strftime("%Y%m%d")
                file_time = datetime.fromtimestamp(mod_time).strftime("%H%M%S")
                
                # Replace template variables
                new_name = template
                new_name = new_name.replace("{date}", file_date)
                new_name = new_name.replace("{time}", file_time)
                new_name = new_name.replace("{ext}", ext)
                new_name = new_name.replace("{num}", f"{index:03d}")
                new_name = new_name.replace("{name}", name)
                
                new_path = os.path.join(directory, new_name)
                
                # Handle collisions
                counter = 1
                while os.path.exists(new_path):
                    name_part, ext_part = os.path.splitext(new_name)
                    new_name = f"{name_part}_{counter}{ext_part}"
                    new_path = os.path.join(directory, new_name)
                    counter += 1
                
                os.rename(old_path, new_path)
                renamed_count += 1
                renamed_files.append({"old": filename, "new": new_name})
            
            return {
                "success": True,
                "renamed_count": renamed_count,
                "renamed_files": renamed_files
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==========================================
    # FEATURE 2: Real-time Folder Monitoring
    # ==========================================
    
    class FolderEventHandler(FileSystemEventHandler):
        """Handler for folder monitoring events"""
        
        def __init__(self, callback: Callable, file_types: List[str] = None):
            self.callback = callback
            self.file_types = file_types or []
            super().__init__()
        
        def on_created(self, event):
            if not event.is_directory:
                if not self.file_types or any(event.src_path.endswith(ext) for ext in self.file_types):
                    self.callback("created", event.src_path)
        
        def on_modified(self, event):
            if not event.is_directory:
                if not self.file_types or any(event.src_path.endswith(ext) for ext in self.file_types):
                    self.callback("modified", event.src_path)
        
        def on_deleted(self, event):
            if not event.is_directory:
                if not self.file_types or any(event.src_path.endswith(ext) for ext in self.file_types):
                    self.callback("deleted", event.src_path)
        
        def on_moved(self, event):
            if not event.is_directory:
                if not self.file_types or any(event.dest_path.endswith(ext) for ext in self.file_types):
                    self.callback("moved", event.dest_path, event.src_path)
    
    def start_folder_monitor(self, directory: str, callback: Callable, 
                           monitor_name: str = "default",
                           file_types: List[str] = None) -> Dict:
        """
        Start monitoring a folder for changes
        
        Args:
            directory: Folder path to monitor
            callback: Function to call when changes occur
                     Signature: callback(event_type, file_path, old_path=None)
            monitor_name: Unique name for this monitor
            file_types: List of file extensions to monitor (e.g., ['.txt', '.pdf'])
        
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(directory):
                return {"success": False, "error": "Directory not found"}
            
            if monitor_name in self.observers:
                return {"success": False, "error": "Monitor already running with this name"}
            
            event_handler = self.FolderEventHandler(callback, file_types)
            observer = Observer()
            observer.schedule(event_handler, directory, recursive=True)
            observer.start()
            
            self.observers[monitor_name] = observer
            self.monitors[monitor_name] = {
                "directory": directory,
                "file_types": file_types,
                "started": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "message": f"Monitoring started for {directory}",
                "monitor_name": monitor_name
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def stop_folder_monitor(self, monitor_name: str = "default") -> Dict:
        """Stop a running folder monitor"""
        try:
            if monitor_name not in self.observers:
                return {"success": False, "error": "Monitor not found"}
            
            self.observers[monitor_name].stop()
            self.observers[monitor_name].join()
            del self.observers[monitor_name]
            del self.monitors[monitor_name]
            
            return {
                "success": True,
                "message": f"Monitor '{monitor_name}' stopped"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_active_monitors(self) -> Dict:
        """List all active folder monitors"""
        return {
            "success": True,
            "monitors": self.monitors,
            "count": len(self.monitors)
        }
    
    def create_workflow_trigger(self, directory: str, workflow: Callable,
                               trigger_on: str = "created",
                               file_pattern: str = "*") -> Dict:
        """
        Create an automatic workflow trigger when files appear
        
        Args:
            directory: Directory to monitor
            workflow: Function to execute when triggered
            trigger_on: Event type ('created', 'modified', 'deleted')
            file_pattern: File pattern to match (e.g., '*.pdf')
        
        Example workflow: lambda path: print(f"Processing {path}")
        """
        try:
            def trigger_callback(event_type, file_path, old_path=None):
                if event_type == trigger_on:
                    # Check if file matches pattern
                    if file_pattern == "*" or Path(file_path).match(file_pattern):
                        # Execute workflow
                        try:
                            workflow(file_path)
                        except Exception as e:
                            print(f"Workflow execution error: {e}")
            
            monitor_name = f"workflow_{directory}_{trigger_on}"
            return self.start_folder_monitor(directory, trigger_callback, monitor_name)
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==========================================
    # FEATURE 3: Compression/Decompression
    # ==========================================
    
    def compress_folder(self, folder_path: str, output_zip: str = None,
                       compression_level: int = 9) -> Dict:
        """
        Compress a folder into a ZIP file
        
        Args:
            folder_path: Path to folder to compress
            output_zip: Output ZIP file path (optional, auto-generated if not provided)
            compression_level: 0-9, where 9 is maximum compression
        
        Returns:
            Dictionary with compression results
        """
        try:
            if not os.path.exists(folder_path):
                return {"success": False, "error": "Folder not found"}
            
            # Auto-generate output name if not provided
            if output_zip is None:
                folder_name = os.path.basename(folder_path.rstrip(os.sep))
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_zip = f"{folder_name}_{timestamp}.zip"
            
            # Ensure .zip extension
            if not output_zip.endswith('.zip'):
                output_zip += '.zip'
            
            files_added = 0
            total_size = 0
            
            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED, 
                               compresslevel=compression_level) as zipf:
                
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zipf.write(file_path, arcname)
                        files_added += 1
                        total_size += os.path.getsize(file_path)
            
            compressed_size = os.path.getsize(output_zip)
            compression_ratio = (1 - compressed_size / total_size) * 100 if total_size > 0 else 0
            
            return {
                "success": True,
                "output_file": output_zip,
                "files_added": files_added,
                "original_size_mb": round(total_size / (1024 * 1024), 2),
                "compressed_size_mb": round(compressed_size / (1024 * 1024), 2),
                "compression_ratio": round(compression_ratio, 2)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def compress_files(self, file_list: List[str], output_zip: str,
                      compression_level: int = 9) -> Dict:
        """
        Compress multiple files into a ZIP file
        
        Args:
            file_list: List of file paths to compress
            output_zip: Output ZIP file path
            compression_level: 0-9, where 9 is maximum compression
        """
        try:
            if not output_zip.endswith('.zip'):
                output_zip += '.zip'
            
            files_added = 0
            total_size = 0
            missing_files = []
            
            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED,
                               compresslevel=compression_level) as zipf:
                
                for file_path in file_list:
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        arcname = os.path.basename(file_path)
                        zipf.write(file_path, arcname)
                        files_added += 1
                        total_size += os.path.getsize(file_path)
                    else:
                        missing_files.append(file_path)
            
            compressed_size = os.path.getsize(output_zip)
            compression_ratio = (1 - compressed_size / total_size) * 100 if total_size > 0 else 0
            
            return {
                "success": True,
                "output_file": output_zip,
                "files_added": files_added,
                "missing_files": missing_files,
                "original_size_mb": round(total_size / (1024 * 1024), 2),
                "compressed_size_mb": round(compressed_size / (1024 * 1024), 2),
                "compression_ratio": round(compression_ratio, 2)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def decompress_zip(self, zip_path: str, output_dir: str = None) -> Dict:
        """
        Extract a ZIP file
        
        Args:
            zip_path: Path to ZIP file
            output_dir: Directory to extract to (optional, auto-generated if not provided)
        
        Returns:
            Dictionary with extraction results
        """
        try:
            if not os.path.exists(zip_path):
                return {"success": False, "error": "ZIP file not found"}
            
            if not zipfile.is_zipfile(zip_path):
                return {"success": False, "error": "Not a valid ZIP file"}
            
            # Auto-generate output directory if not provided
            if output_dir is None:
                zip_name = os.path.splitext(os.path.basename(zip_path))[0]
                output_dir = f"{zip_name}_extracted"
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            files_extracted = 0
            total_size = 0
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                file_list = zipf.namelist()
                files_extracted = len(file_list)
                
                zipf.extractall(output_dir)
                
                # Calculate total extracted size
                for file_name in file_list:
                    file_path = os.path.join(output_dir, file_name)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)
            
            return {
                "success": True,
                "output_directory": output_dir,
                "files_extracted": files_extracted,
                "extracted_size_mb": round(total_size / (1024 * 1024), 2)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def auto_compress_by_age(self, directory: str, days_old: int = 30,
                            delete_after_compress: bool = False) -> Dict:
        """
        Automatically compress files older than specified days
        
        Args:
            directory: Directory to scan
            days_old: Compress files older than this many days
            delete_after_compress: Delete original files after compression
        """
        try:
            if not os.path.exists(directory):
                return {"success": False, "error": "Directory not found"}
            
            current_time = time.time()
            age_threshold = days_old * 24 * 60 * 60
            old_files = []
            
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > age_threshold:
                        old_files.append(file_path)
            
            if not old_files:
                return {
                    "success": True,
                    "message": "No files found older than specified age",
                    "files_compressed": 0
                }
            
            # Compress old files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_zip = os.path.join(directory, f"archived_{days_old}days_{timestamp}.zip")
            
            result = self.compress_files(old_files, output_zip)
            
            if result["success"] and delete_after_compress:
                deleted_count = 0
                for file_path in old_files:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Could not delete {file_path}: {e}")
                
                result["deleted_files"] = deleted_count
            
            return result
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def cleanup(self):
        """Stop all monitors and cleanup resources"""
        monitor_names = list(self.observers.keys())
        for monitor_name in monitor_names:
            self.stop_folder_monitor(monitor_name)
        
        print("📁 File Automation cleanup complete")


def create_file_automation():
    """Factory function to create FileAutomation instance"""
    return FileAutomation()


# Example usage and demonstrations
if __name__ == "__main__":
    print("\n" + "="*60)
    print("📁 File & Folder Automation - Demo")
    print("="*60 + "\n")
    
    fa = FileAutomation()
    
    # Demo 1: File renaming
    print("Demo 1: Automatic File Renaming")
    print("-" * 40)
    print("Example: Rename files by date pattern")
    print("  fa.rename_files_by_pattern('/path/to/folder', 'date', prefix='Doc_')")
    print()
    
    # Demo 2: Folder monitoring
    print("Demo 2: Real-time Folder Monitoring")
    print("-" * 40)
    print("Example: Monitor downloads folder")
    print("  def on_new_file(event_type, file_path):")
    print("      print(f'New file detected: {file_path}')")
    print("  fa.start_folder_monitor('/downloads', on_new_file)")
    print()
    
    # Demo 3: Compression
    print("Demo 3: Compression/Decompression")
    print("-" * 40)
    print("Example: Compress a folder")
    print("  result = fa.compress_folder('/my/project', 'project_backup.zip')")
    print("  print(f'Compressed {result['files_added']} files')")
    print("  print(f'Compression ratio: {result['compression_ratio']}%')")
    print()
    
    print("="*60)
    print("✅ File Automation System Ready!")
    print("="*60 + "\n")
