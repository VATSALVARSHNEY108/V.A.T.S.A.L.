"""
Advanced File Manager Module
Auto-rename, compress old files, auto-backup, advanced file operations
"""

import os
import shutil
import hashlib
import gzip
import json
from datetime import datetime, timedelta
from pathlib import Path
import re

class FileManager:
    def __init__(self):
        self.backup_config_file = "backup_config.json"
        self.load_backup_config()
    
    def load_backup_config(self):
        """Load backup configuration"""
        if os.path.exists(self.backup_config_file):
            with open(self.backup_config_file, 'r') as f:
                self.backup_config = json.load(f)
        else:
            self.backup_config = {
                "enabled": False,
                "folders": [],
                "backup_location": str(Path.home() / "Backups"),
                "schedule": "daily"
            }
            self.save_backup_config()
    
    def save_backup_config(self):
        """Save backup configuration"""
        with open(self.backup_config_file, 'w') as f:
            json.dump(self.backup_config, f, indent=2)
    
    def auto_rename_files(self, folder_path, pattern="clean"):
        """Auto-rename messy files"""
        try:
            renamed = []
            
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                if os.path.isfile(file_path):
                    new_name = filename
                    
                    if pattern == "clean":
                        new_name = re.sub(r'\s*\(\d+\)\s*', '', new_name)
                        new_name = re.sub(r'\s+', '_', new_name)
                        new_name = new_name.lower()
                    
                    elif pattern == "timestamp":
                        name, ext = os.path.splitext(filename)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        new_name = f"{name}_{timestamp}{ext}"
                    
                    elif pattern == "numbered":
                        name, ext = os.path.splitext(filename)
                        counter = 1
                        new_name = f"{counter:03d}_{name}{ext}"
                    
                    if new_name != filename:
                        new_path = os.path.join(folder_path, new_name)
                        
                        if not os.path.exists(new_path):
                            os.rename(file_path, new_path)
                            renamed.append(f"{filename} → {new_name}")
            
            if renamed:
                result = f"✅ Renamed {len(renamed)} files:\n"
                for item in renamed[:10]:
                    result += f"  • {item}\n"
                if len(renamed) > 10:
                    result += f"  ... and {len(renamed) - 10} more"
                return result
            else:
                return "ℹ️ No files to rename"
        except Exception as e:
            return f"❌ Failed to rename files: {str(e)}"
    
    def find_duplicates(self, folder_path):
        """Find duplicate files by hash"""
        try:
            hashes = {}
            duplicates = []
            
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    try:
                        file_hash = self.get_file_hash(file_path)
                        
                        if file_hash in hashes:
                            duplicates.append({
                                "original": hashes[file_hash],
                                "duplicate": file_path,
                                "size": os.path.getsize(file_path)
                            })
                        else:
                            hashes[file_hash] = file_path
                    except:
                        continue
            
            if duplicates:
                total_wasted = sum(d['size'] for d in duplicates)
                result = f"🔍 Found {len(duplicates)} duplicate files (wasting {total_wasted/(1024*1024):.2f} MB):\n"
                
                for dup in duplicates[:10]:
                    result += f"  • {os.path.basename(dup['duplicate'])} ({dup['size']/(1024*1024):.2f} MB)\n"
                    result += f"    Original: {dup['original']}\n"
                
                if len(duplicates) > 10:
                    result += f"  ... and {len(duplicates) - 10} more"
                
                return result
            else:
                return "✅ No duplicate files found"
        except Exception as e:
            return f"❌ Failed to find duplicates: {str(e)}"
    
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def compress_old_files(self, folder_path, days_old=90):
        """Compress files older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            compressed = []
            
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    if filename.endswith('.gz'):
                        continue
                    
                    file_path = os.path.join(root, filename)
                    
                    try:
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        if mtime < cutoff_date:
                            original_size = os.path.getsize(file_path)
                            
                            with open(file_path, 'rb') as f_in:
                                with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                            
                            compressed_size = os.path.getsize(f"{file_path}.gz")
                            os.remove(file_path)
                            
                            saved = original_size - compressed_size
                            compressed.append(f"{filename} (saved {saved/(1024*1024):.2f} MB)")
                    except:
                        continue
            
            if compressed:
                result = f"✅ Compressed {len(compressed)} old files:\n"
                for item in compressed[:10]:
                    result += f"  • {item}\n"
                if len(compressed) > 10:
                    result += f"  ... and {len(compressed) - 10} more"
                return result
            else:
                return f"ℹ️ No files older than {days_old} days found"
        except Exception as e:
            return f"❌ Failed to compress files: {str(e)}"
    
    def backup_folder(self, source_folder, destination=None):
        """Backup a folder to destination"""
        try:
            if destination is None:
                destination = self.backup_config["backup_location"]
            
            os.makedirs(destination, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{os.path.basename(source_folder)}_backup_{timestamp}"
            backup_path = os.path.join(destination, backup_name)
            
            shutil.copytree(source_folder, backup_path)
            
            total_size = sum(
                os.path.getsize(os.path.join(dirpath, filename))
                for dirpath, _, filenames in os.walk(backup_path)
                for filename in filenames
            )
            
            return f"✅ Backup created: {backup_path} ({total_size/(1024*1024):.2f} MB)"
        except Exception as e:
            return f"❌ Backup failed: {str(e)}"
    
    def add_backup_folder(self, folder_path):
        """Add folder to auto-backup list"""
        if folder_path not in self.backup_config["folders"]:
            self.backup_config["folders"].append(folder_path)
            self.save_backup_config()
            return f"✅ Added to backup list: {folder_path}"
        return f"ℹ️ Already in backup list: {folder_path}"
    
    def enable_auto_backup(self):
        """Enable automatic backups"""
        self.backup_config["enabled"] = True
        self.save_backup_config()
        return "✅ Auto-backup enabled"
    
    def run_backups(self):
        """Run backups for all configured folders"""
        if not self.backup_config["enabled"]:
            return "ℹ️ Auto-backup is disabled"
        
        results = []
        for folder in self.backup_config["folders"]:
            if os.path.exists(folder):
                result = self.backup_folder(folder)
                results.append(result)
        
        return "\n".join(results) if results else "ℹ️ No folders to backup"
    
    def list_backups(self):
        """List all available backups"""
        try:
            backup_location = self.backup_config["backup_location"]
            
            if not os.path.exists(backup_location):
                return "ℹ️ No backups found"
            
            backups = []
            for item in os.listdir(backup_location):
                item_path = os.path.join(backup_location, item)
                if os.path.isdir(item_path):
                    size = sum(
                        os.path.getsize(os.path.join(dirpath, filename))
                        for dirpath, _, filenames in os.walk(item_path)
                        for filename in filenames
                    )
                    mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
                    backups.append({
                        "name": item,
                        "size_mb": round(size / (1024 * 1024), 2),
                        "date": mtime.strftime("%Y-%m-%d %H:%M")
                    })
            
            if backups:
                result = "💾 Available Backups:\n"
                for backup in sorted(backups, key=lambda x: x['date'], reverse=True):
                    result += f"  • {backup['name']} - {backup['size_mb']} MB ({backup['date']})\n"
                return result
            else:
                return "ℹ️ No backups found"
        except Exception as e:
            return f"❌ Failed to list backups: {str(e)}"

if __name__ == "__main__":
    manager = FileManager()
    print("File Manager Module - Testing")
    print(manager.list_backups())
