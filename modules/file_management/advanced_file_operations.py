"""
Advanced File Operations Module
Search, organize, and manage files intelligently
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import fnmatch

def search_files(pattern: str, directory: str = ".", recursive: bool = True, max_results: int = 50) -> List[str]:
    """
    Search for files matching a pattern
    
    Args:
        pattern: File pattern (e.g., "*.py", "report*")
        directory: Directory to search in
        recursive: Search subdirectories
        max_results: Maximum number of results
    
    Returns:
        List of matching file paths
    """
    matches = []
    search_path = Path(directory)
    
    try:
        if recursive:
            for file_path in search_path.rglob(pattern):
                if file_path.is_file():
                    matches.append(str(file_path))
                    if len(matches) >= max_results:
                        break
        else:
            for file_path in search_path.glob(pattern):
                if file_path.is_file():
                    matches.append(str(file_path))
                    if len(matches) >= max_results:
                        break
    except Exception as e:
        return [f"Error searching: {str(e)}"]
    
    return matches

def find_large_files(directory: str = ".", min_size_mb: float = 10, limit: int = 20) -> List[Dict]:
    """Find large files in directory"""
    large_files = []
    search_path = Path(directory)
    min_size_bytes = min_size_mb * 1024 * 1024
    
    try:
        for file_path in search_path.rglob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size >= min_size_bytes:
                    large_files.append({
                        "path": str(file_path),
                        "size_mb": f"{size / (1024**2):.2f} MB",
                        "size_bytes": size
                    })
        
        large_files.sort(key=lambda x: x["size_bytes"], reverse=True)
        return large_files[:limit]
    
    except Exception as e:
        return [{"error": str(e)}]

def find_duplicate_files(directory: str = ".") -> Dict[str, List[str]]:
    """Find duplicate files based on size and name"""
    files_by_name = {}
    duplicates = {}
    
    try:
        for file_path in Path(directory).rglob("*"):
            if file_path.is_file():
                name = file_path.name
                size = file_path.stat().st_size
                key = f"{name}_{size}"
                
                if key not in files_by_name:
                    files_by_name[key] = []
                files_by_name[key].append(str(file_path))
        
        for key, paths in files_by_name.items():
            if len(paths) > 1:
                duplicates[key] = paths
    
    except Exception as e:
        return {"error": str(e)}
    
    return duplicates

def organize_files_by_extension(source_dir: str, target_dir: str = None) -> Dict:
    """Organize files into folders by extension"""
    if target_dir is None:
        target_dir = source_dir
    
    organized = {}
    errors = []
    
    try:
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        for file_path in source_path.glob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower() or ".no_extension"
                ext_folder = target_path / ext.replace(".", "")
                ext_folder.mkdir(exist_ok=True)
                
                try:
                    dest = ext_folder / file_path.name
                    shutil.move(str(file_path), str(dest))
                    
                    if ext not in organized:
                        organized[ext] = 0
                    organized[ext] += 1
                except Exception as e:
                    errors.append(f"{file_path.name}: {str(e)}")
    
    except Exception as e:
        return {"error": str(e)}
    
    return {
        "organized": organized,
        "errors": errors
    }

def find_old_files(directory: str = ".", days_old: int = 30, limit: int = 50) -> List[Dict]:
    """Find files older than specified days"""
    old_files = []
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    try:
        for file_path in Path(directory).rglob("*"):
            if file_path.is_file():
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < cutoff_date:
                    old_files.append({
                        "path": str(file_path),
                        "modified": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                        "days_old": (datetime.now() - mtime).days
                    })
        
        old_files.sort(key=lambda x: x["days_old"], reverse=True)
        return old_files[:limit]
    
    except Exception as e:
        return [{"error": str(e)}]

def get_directory_size(directory: str = ".") -> Dict:
    """Calculate total size of directory"""
    total_size = 0
    file_count = 0
    
    try:
        for file_path in Path(directory).rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            "total_size_mb": f"{total_size / (1024**2):.2f} MB",
            "total_size_gb": f"{total_size / (1024**3):.2f} GB",
            "file_count": file_count,
            "directory": directory
        }
    
    except Exception as e:
        return {"error": str(e)}

def find_empty_files_and_folders(directory: str = ".") -> Dict:
    """Find empty files and folders"""
    empty_files = []
    empty_folders = []
    
    try:
        for path in Path(directory).rglob("*"):
            if path.is_file() and path.stat().st_size == 0:
                empty_files.append(str(path))
            elif path.is_dir() and not any(path.iterdir()):
                empty_folders.append(str(path))
        
        return {
            "empty_files": empty_files,
            "empty_folders": empty_folders,
            "total_empty": len(empty_files) + len(empty_folders)
        }
    
    except Exception as e:
        return {"error": str(e)}
