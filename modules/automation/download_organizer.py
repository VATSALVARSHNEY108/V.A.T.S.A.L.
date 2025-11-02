"""
Download Organizer Module
Auto-organize downloads into categorized folders
"""

import os
import shutil
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class DownloadOrganizer:
    def __init__(self, download_path=None):
        if download_path is None:
            self.download_path = str(Path.home() / "Downloads")
        else:
            self.download_path = download_path
        
        self.categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk"],
            "Code": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".php", ".rb", ".go"],
            "Data": [".json", ".xml", ".csv", ".sql", ".db", ".sqlite"]
        }
        
        self.config_file = "organizer_config.json"
        self.load_config()
    
    def load_config(self):
        """Load organizer configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.auto_organize_enabled = config.get("auto_organize", False)
        else:
            self.auto_organize_enabled = False
            self.save_config()
    
    def save_config(self):
        """Save organizer configuration"""
        with open(self.config_file, 'w') as f:
            json.dump({"auto_organize": self.auto_organize_enabled}, f, indent=2)
    
    def get_category(self, filename):
        """Determine category for a file"""
        ext = os.path.splitext(filename)[1].lower()
        
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
        
        return "Others"
    
    def organize_downloads(self):
        """Organize all files in downloads folder"""
        try:
            if not os.path.exists(self.download_path):
                return f"❌ Download folder not found: {self.download_path}"
            
            organized = []
            
            for filename in os.listdir(self.download_path):
                file_path = os.path.join(self.download_path, filename)
                
                if os.path.isfile(file_path):
                    category = self.get_category(filename)
                    category_folder = os.path.join(self.download_path, category)
                    
                    os.makedirs(category_folder, exist_ok=True)
                    
                    dest_path = os.path.join(category_folder, filename)
                    
                    if os.path.exists(dest_path):
                        base, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(dest_path):
                            dest_path = os.path.join(category_folder, f"{base}_{counter}{ext}")
                            counter += 1
                    
                    shutil.move(file_path, dest_path)
                    organized.append(f"{filename} → {category}")
            
            if organized:
                result = f"✅ Organized {len(organized)} files:\n"
                for item in organized[:10]:
                    result += f"  • {item}\n"
                if len(organized) > 10:
                    result += f"  ... and {len(organized) - 10} more"
                return result
            else:
                return "ℹ️ No files to organize"
        except Exception as e:
            return f"❌ Failed to organize downloads: {str(e)}"
    
    def enable_auto_organize(self):
        """Enable automatic organization of downloads"""
        self.auto_organize_enabled = True
        self.save_config()
        return "✅ Auto-organize enabled. New downloads will be organized automatically."
    
    def disable_auto_organize(self):
        """Disable automatic organization"""
        self.auto_organize_enabled = False
        self.save_config()
        return "✅ Auto-organize disabled"
    
    def add_custom_category(self, category_name, extensions):
        """Add a custom file category"""
        self.categories[category_name] = extensions
        return f"✅ Added category '{category_name}' with {len(extensions)} extensions"
    
    def get_download_stats(self):
        """Get statistics about downloads folder"""
        try:
            stats = {}
            total_size = 0
            total_files = 0
            
            for category in self.categories.keys():
                category_path = os.path.join(self.download_path, category)
                if os.path.exists(category_path):
                    files = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
                    size = sum(os.path.getsize(os.path.join(category_path, f)) for f in files)
                    stats[category] = {"files": len(files), "size_mb": round(size / (1024 * 1024), 2)}
                    total_size += size
                    total_files += len(files)
            
            result = "📊 Downloads Statistics:\n"
            result += f"Total: {total_files} files, {round(total_size / (1024 * 1024), 2)} MB\n\n"
            
            for category, data in sorted(stats.items(), key=lambda x: x[1]['size_mb'], reverse=True):
                result += f"  {category}: {data['files']} files, {data['size_mb']} MB\n"
            
            return result
        except Exception as e:
            return f"❌ Failed to get stats: {str(e)}"

class DownloadWatcher(FileSystemEventHandler):
    """Watch for new downloads and organize them"""
    
    def __init__(self, organizer):
        self.organizer = organizer
    
    def on_created(self, event):
        """Handle new file creation"""
        if not event.is_directory and self.organizer.auto_organize_enabled:
            time.sleep(1)
            filename = os.path.basename(event.src_path)
            category = self.organizer.get_category(filename)
            category_folder = os.path.join(self.organizer.download_path, category)
            
            os.makedirs(category_folder, exist_ok=True)
            
            dest_path = os.path.join(category_folder, filename)
            try:
                shutil.move(event.src_path, dest_path)
                print(f"✅ Auto-organized: {filename} → {category}")
            except:
                pass

def start_auto_organizer():
    """Start the automatic download organizer"""
    organizer = DownloadOrganizer()
    event_handler = DownloadWatcher(organizer)
    observer = Observer()
    observer.schedule(event_handler, organizer.download_path, recursive=False)
    observer.start()
    
    print(f"✅ Auto-organizer started for: {organizer.download_path}")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    organizer = DownloadOrganizer()
    print("Download Organizer Module - Testing")
    print(organizer.get_download_stats())
