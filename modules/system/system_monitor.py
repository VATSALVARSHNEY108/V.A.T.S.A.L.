"""
System Monitoring Module
Monitor CPU, RAM, disk usage and system health
"""

import psutil
import platform
from datetime import datetime

def get_cpu_usage() -> dict:
    """Get CPU usage information"""
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    return {
        "usage_percent": cpu_percent,
        "cpu_count": cpu_count,
        "current_frequency": f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A",
        "status": "High" if cpu_percent > 80 else "Normal" if cpu_percent > 50 else "Low"
    }

def get_memory_usage() -> dict:
    """Get RAM usage information"""
    mem = psutil.virtual_memory()
    
    return {
        "total_gb": f"{mem.total / (1024**3):.2f} GB",
        "available_gb": f"{mem.available / (1024**3):.2f} GB",
        "used_gb": f"{mem.used / (1024**3):.2f} GB",
        "usage_percent": mem.percent,
        "status": "Critical" if mem.percent > 90 else "High" if mem.percent > 70 else "Normal"
    }

def get_disk_usage() -> dict:
    """Get disk usage information"""
    disk = psutil.disk_usage('/')
    
    return {
        "total_gb": f"{disk.total / (1024**3):.2f} GB",
        "used_gb": f"{disk.used / (1024**3):.2f} GB",
        "free_gb": f"{disk.free / (1024**3):.2f} GB",
        "usage_percent": disk.percent,
        "status": "Critical" if disk.percent > 90 else "High" if disk.percent > 70 else "Normal"
    }

def get_network_info() -> dict:
    """Get network information"""
    net_io = psutil.net_io_counters()
    
    return {
        "bytes_sent_mb": f"{net_io.bytes_sent / (1024**2):.2f} MB",
        "bytes_received_mb": f"{net_io.bytes_recv / (1024**2):.2f} MB",
        "packets_sent": net_io.packets_sent,
        "packets_received": net_io.packets_recv
    }

def get_battery_info() -> dict:
    """Get battery information (if available)"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged_in": battery.power_plugged,
                "time_left": f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m" if battery.secsleft != -1 else "Charging"
            }
    except:
        pass
    return {"available": False}

def get_system_info() -> dict:
    """Get general system information"""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds%3600)//60}m"
    }

def get_running_processes(limit: int = 10) -> list:
    """Get top processes by CPU usage"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:limit]

def get_full_system_report() -> str:
    """Generate comprehensive system health report"""
    cpu = get_cpu_usage()
    mem = get_memory_usage()
    disk = get_disk_usage()
    net = get_network_info()
    sys_info = get_system_info()
    battery = get_battery_info()
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    SYSTEM HEALTH REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

📊 CPU USAGE:
   • Usage: {cpu['usage_percent']}% ({cpu['status']})
   • Cores: {cpu['cpu_count']}
   • Frequency: {cpu['current_frequency']}

💾 MEMORY USAGE:
   • Total: {mem['total_gb']}
   • Used: {mem['used_gb']} ({mem['usage_percent']}%)
   • Available: {mem['available_gb']}
   • Status: {mem['status']}

💿 DISK USAGE:
   • Total: {disk['total_gb']}
   • Used: {disk['used_gb']} ({disk['usage_percent']}%)
   • Free: {disk['free_gb']}
   • Status: {disk['status']}

🌐 NETWORK:
   • Sent: {net['bytes_sent_mb']}
   • Received: {net['bytes_received_mb']}

💻 SYSTEM INFO:
   • Platform: {sys_info['platform']} {sys_info['platform_version']}
   • Processor: {sys_info['processor']}
   • Uptime: {sys_info['uptime']}
"""
    
    if battery.get("available") is not False:
        report += f"""
🔋 BATTERY:
   • Level: {battery['percent']}%
   • Plugged In: {'Yes' if battery['plugged_in'] else 'No'}
   • Time Left: {battery['time_left']}
"""
    
    return report
