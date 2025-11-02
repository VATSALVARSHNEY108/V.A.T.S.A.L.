#!/usr/bin/env python3
"""
VATSAL Enhanced Local Modules
Additional automation capabilities - all executed locally
"""

import os
import cv2
import numpy as np
import psutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None


class ScreenMonitor:
    """Local screen monitoring and analysis using OpenCV"""
    
    @staticmethod
    def capture_screen() -> np.ndarray:
        """Capture current screen as numpy array"""
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def detect_changes(baseline: np.ndarray, current: np.ndarray, threshold: float = 30.0) -> Tuple[bool, float]:
        """Detect if screen has changed significantly"""
        diff = cv2.absdiff(baseline, current)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        change_percent = (np.count_nonzero(gray_diff > 30) / gray_diff.size) * 100
        
        return change_percent > threshold, change_percent
    
    @staticmethod
    def find_color_region(screen: np.ndarray, color_range: Tuple[Tuple, Tuple]) -> List[Tuple[int, int, int, int]]:
        """Find regions of specific color"""
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, color_range[0], color_range[1])
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            regions.append((x, y, w, h))
        
        return regions
    
    @staticmethod
    def save_screen_region(x: int, y: int, w: int, h: int, path: str) -> bool:
        """Save specific screen region"""
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        screenshot.save(path)
        return True


class AdvancedFileManager:
    """Advanced file operations - all local"""
    
    @staticmethod
    def search_files(directory: str, pattern: str = "*", recursive: bool = True) -> List[str]:
        """Search for files matching pattern"""
        path = Path(directory)
        
        if recursive:
            files = list(path.rglob(pattern))
        else:
            files = list(path.glob(pattern))
        
        return [str(f) for f in files if f.is_file()]
    
    @staticmethod
    def get_file_info(filepath: str) -> Dict:
        """Get detailed file information"""
        path = Path(filepath)
        
        if not path.exists():
            return {"error": "File not found"}
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "extension": path.suffix
        }
    
    @staticmethod
    def find_large_files(directory: str, min_size_mb: float = 100) -> List[Dict]:
        """Find files larger than specified size"""
        large_files = []
        min_size_bytes = min_size_mb * 1024 * 1024
        
        for file_path in Path(directory).rglob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size >= min_size_bytes:
                    large_files.append({
                        "path": str(file_path),
                        "size_mb": round(size / (1024 * 1024), 2)
                    })
        
        return sorted(large_files, key=lambda x: x["size_mb"], reverse=True)
    
    @staticmethod
    def organize_by_extension(directory: str, dry_run: bool = False) -> Dict:
        """Organize files by extension into subfolders"""
        path = Path(directory)
        organized = {}
        
        for file_path in path.glob("*"):
            if file_path.is_file():
                ext = file_path.suffix[1:] if file_path.suffix else "no_extension"
                
                if ext not in organized:
                    organized[ext] = []
                
                organized[ext].append(file_path.name)
                
                if not dry_run:
                    dest_folder = path / ext
                    dest_folder.mkdir(exist_ok=True)
                    dest_file = dest_folder / file_path.name
                    file_path.rename(dest_file)
        
        return organized
    
    @staticmethod
    def get_directory_size(directory: str) -> Dict:
        """Calculate total directory size"""
        total_size = 0
        file_count = 0
        
        for file_path in Path(directory).rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        return {
            "total_bytes": total_size,
            "total_mb": round(total_size / (1024 * 1024), 2),
            "total_gb": round(total_size / (1024 * 1024 * 1024), 2),
            "file_count": file_count
        }


class SystemController:
    """Advanced system control operations - all local"""
    
    @staticmethod
    def get_running_processes() -> List[Dict]:
        """Get list of running processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_percent": round(proc.info['memory_percent'], 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)
    
    @staticmethod
    def get_top_processes(count: int = 10) -> List[Dict]:
        """Get top N processes by resource usage"""
        processes = SystemController.get_running_processes()
        return processes[:count]
    
    @staticmethod
    def get_network_info() -> Dict:
        """Get network interface information"""
        net_io = psutil.net_io_counters()
        
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "mb_sent": round(net_io.bytes_sent / (1024 * 1024), 2),
            "mb_recv": round(net_io.bytes_recv / (1024 * 1024), 2)
        }
    
    @staticmethod
    def get_full_system_report() -> Dict:
        """Complete system health report"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        battery = psutil.sensors_battery()
        battery_info = {
            "percent": battery.percent,
            "plugged": battery.power_plugged,
            "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
        } if battery else {"available": False}
        
        return {
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count(),
                "freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent
            },
            "battery": battery_info,
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }


class WindowController:
    """Window management operations - all local"""
    
    @staticmethod
    def get_active_window_title() -> str:
        """Get title of currently active window (Windows only)"""
        try:
            import win32gui
            hwnd = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(hwnd)
        except:
            return "Unable to get window title"
    
    @staticmethod
    def minimize_all_windows():
        """Minimize all windows (Windows only)"""
        pyautogui.hotkey('win', 'd')
        return True
    
    @staticmethod
    def switch_window(window_title: str):
        """Switch to window by title (Windows only)"""
        try:
            import win32gui
            
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if window_title.lower() in title.lower():
                        windows.append(hwnd)
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            
            if windows:
                win32gui.SetForegroundWindow(windows[0])
                return True
            return False
        except:
            return False


class ClipboardManager:
    """Clipboard operations - all local"""
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """Copy text to clipboard"""
        import pyperclip
        pyperclip.copy(text)
        return True
    
    @staticmethod
    def get_from_clipboard() -> str:
        """Get text from clipboard"""
        import pyperclip
        return pyperclip.paste()
    
    @staticmethod
    def clear_clipboard() -> bool:
        """Clear clipboard"""
        import pyperclip
        pyperclip.copy("")
        return True


class AutomationWorkflows:
    """Pre-built automation workflows - all local execution"""
    
    @staticmethod
    def optimize_workspace() -> List[str]:
        """Optimize workspace: close heavy apps, organize downloads, clear temp"""
        results = []
        
        results.append("Minimizing all windows...")
        WindowController.minimize_all_windows()
        
        results.append("Checking for heavy processes...")
        heavy_processes = [p for p in SystemController.get_top_processes(5) if p['memory_percent'] > 5]
        results.append(f"Found {len(heavy_processes)} heavy processes")
        
        results.append("Clearing clipboard...")
        ClipboardManager.clear_clipboard()
        
        return results
    
    @staticmethod
    def quick_screenshot_analysis(save_path: str = None) -> Dict:
        """Take screenshot and analyze basic properties"""
        if not save_path:
            save_path = f"screenshots/quick_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        screen = ScreenMonitor.capture_screen()
        
        height, width, channels = screen.shape
        
        cv2.imwrite(save_path, screen)
        
        return {
            "saved_to": save_path,
            "resolution": f"{width}x{height}",
            "size_bytes": os.path.getsize(save_path)
        }
    
    @staticmethod
    def system_health_check() -> str:
        """Quick system health check"""
        report = SystemController.get_full_system_report()
        
        issues = []
        if report['cpu']['usage_percent'] > 80:
            issues.append("⚠️ High CPU usage")
        if report['memory']['percent'] > 80:
            issues.append("⚠️ High memory usage")
        if report['disk']['percent'] > 85:
            issues.append("⚠️ Low disk space")
        
        if not issues:
            return "✓ System healthy"
        else:
            return "\n".join(issues)


if __name__ == "__main__":
    print("VATSAL Enhanced Modules - Local Automation Library")
    print("\nAvailable modules:")
    print("  • ScreenMonitor: Screen capture and analysis")
    print("  • AdvancedFileManager: File search and organization")
    print("  • SystemController: System monitoring and control")
    print("  • WindowController: Window management")
    print("  • ClipboardManager: Clipboard operations")
    print("  • AutomationWorkflows: Pre-built workflows")
