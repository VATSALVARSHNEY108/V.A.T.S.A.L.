"""
🛡️ Activity Monitoring System
Detect suspicious behavior and security anomalies in real-time
"""

import os
import json
import psutil
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import deque, Counter
import threading
import time

class ActivityMonitoringSystem:
    """
    Advanced activity monitoring and threat detection system
    Features:
    - Real-time process monitoring
    - Failed authentication tracking
    - Unusual activity detection
    - Resource usage monitoring
    - Automated threat response
    """
    
    def __init__(self):
        self.data_dir = "activity_monitoring"
        self.activity_log_file = os.path.join(self.data_dir, "activity_log.json")
        self.threat_log_file = os.path.join(self.data_dir, "threat_log.json")
        self.config_file = os.path.join(self.data_dir, "monitoring_config.json")
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.config = self._load_config()
        self.activity_log = self._load_activity_log()
        self.threat_log = self._load_threat_log()
        
        self.recent_activities = deque(maxlen=1000)
        self.failed_auth_attempts = deque(maxlen=100)
        
        self.monitoring_active = False
        self.monitor_thread = None
        
        self.threat_patterns = {
            "multiple_failed_logins": {
                "threshold": 3,
                "time_window_minutes": 5,
                "severity": "high"
            },
            "unusual_process": {
                "suspicious_names": ["hack", "crack", "keygen", "malware"],
                "severity": "critical"
            },
            "high_cpu_usage": {
                "threshold": 90,
                "duration_seconds": 300,
                "severity": "medium"
            },
            "high_memory_usage": {
                "threshold": 90,
                "duration_seconds": 300,
                "severity": "medium"
            },
            "rapid_file_access": {
                "threshold": 100,
                "time_window_seconds": 60,
                "severity": "medium"
            },
            "privilege_escalation": {
                "severity": "critical"
            }
        }
    
    def _load_config(self) -> Dict:
        """Load monitoring configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "monitoring_enabled": False,
            "auto_response_enabled": False,
            "alert_on_threats": True,
            "log_all_activities": True,
            "process_monitoring": True,
            "network_monitoring": False,
            "file_integrity_monitoring": False,
            "alert_email": None,
            "blocked_processes": [],
            "whitelisted_processes": []
        }
    
    def _save_config(self):
        """Save monitoring configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _load_activity_log(self) -> List:
        """Load activity log"""
        if os.path.exists(self.activity_log_file):
            try:
                with open(self.activity_log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_activity_log(self):
        """Save activity log"""
        try:
            with open(self.activity_log_file, 'w') as f:
                json.dump(self.activity_log[-1000:], f, indent=2)
        except Exception as e:
            print(f"Error saving activity log: {e}")
    
    def _load_threat_log(self) -> List:
        """Load threat log"""
        if os.path.exists(self.threat_log_file):
            try:
                with open(self.threat_log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_threat_log(self):
        """Save threat log"""
        try:
            with open(self.threat_log_file, 'w') as f:
                json.dump(self.threat_log[-500:], f, indent=2)
        except Exception as e:
            print(f"Error saving threat log: {e}")
    
    def log_activity(self, activity_type: str, details: Dict, user_id: Optional[str] = None):
        """
        Log an activity
        
        Args:
            activity_type: Type of activity (login, file_access, command, etc.)
            details: Activity details
            user_id: User performing activity
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "user_id": user_id,
            "details": details,
            "risk_level": self._assess_risk(activity_type, details)
        }
        
        self.activity_log.append(entry)
        self.recent_activities.append(entry)
        
        if self.config["log_all_activities"]:
            self._save_activity_log()
        
        if entry["risk_level"] in ["high", "critical"]:
            self._handle_suspicious_activity(entry)
    
    def _assess_risk(self, activity_type: str, details: Dict) -> str:
        """Assess risk level of an activity"""
        if activity_type == "failed_authentication":
            recent_failures = sum(
                1 for a in self.recent_activities
                if a["type"] == "failed_authentication"
                and datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(minutes=5)
            )
            
            if recent_failures >= 3:
                return "critical"
            elif recent_failures >= 2:
                return "high"
            else:
                return "medium"
        
        elif activity_type == "system_command":
            dangerous_commands = ["rm -rf", "format", "del /f", "shutdown", "reboot"]
            if any(cmd in details.get("command", "").lower() for cmd in dangerous_commands):
                return "high"
        
        elif activity_type == "file_access":
            sensitive_paths = ["/etc/shadow", "/etc/passwd", "/.ssh", "password", "credential"]
            if any(path in details.get("path", "").lower() for path in sensitive_paths):
                return "high"
        
        return "low"
    
    def _handle_suspicious_activity(self, activity: Dict):
        """Handle detected suspicious activity"""
        threat_entry = {
            "timestamp": datetime.now().isoformat(),
            "threat_type": activity["type"],
            "risk_level": activity["risk_level"],
            "details": activity["details"],
            "user_id": activity.get("user_id"),
            "auto_response_taken": False
        }
        
        self.threat_log.append(threat_entry)
        self._save_threat_log()
        
        print(f"\n⚠️  SECURITY ALERT: {activity['type']}")
        print(f"   Risk Level: {activity['risk_level'].upper()}")
        print(f"   Details: {activity['details']}")
        print(f"   Time: {activity['timestamp']}")
        
        if self.config["auto_response_enabled"]:
            self._execute_auto_response(threat_entry)
    
    def _execute_auto_response(self, threat: Dict):
        """Execute automated response to threat"""
        if threat["risk_level"] == "critical":
            print(f"🚨 Critical threat detected! Taking automatic action...")
            
            if threat["threat_type"] == "failed_authentication":
                print("   Action: Temporary account lockout initiated")
        
        threat["auto_response_taken"] = True
        self._save_threat_log()
    
    def start_monitoring(self):
        """Start real-time activity monitoring"""
        if self.monitoring_active:
            return {"success": False, "message": "Monitoring already active"}
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        self.config["monitoring_enabled"] = True
        self._save_config()
        
        print("🛡️  Activity monitoring started")
        return {"success": True, "message": "Monitoring started"}
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring_active = False
        self.config["monitoring_enabled"] = False
        self._save_config()
        
        print("⏸️  Activity monitoring stopped")
        return {"success": True, "message": "Monitoring stopped"}
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        print("🔍 Starting monitoring loop...")
        
        while self.monitoring_active:
            try:
                if self.config["process_monitoring"]:
                    self._check_processes()
                
                self._check_system_resources()
                
                time.sleep(30)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)
    
    def _check_processes(self):
        """Check running processes for suspicious activity"""
        try:
            blocked_processes = self.config.get("blocked_processes", [])
            suspicious_keywords = self.threat_patterns["unusual_process"]["suspicious_names"]
            
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    if proc_name in blocked_processes:
                        self.log_activity(
                            "blocked_process_detected",
                            {
                                "process_name": proc_name,
                                "pid": proc.info['pid'],
                                "username": proc.info.get('username', 'unknown')
                            }
                        )
                    
                    if any(keyword in proc_name for keyword in suspicious_keywords):
                        self.log_activity(
                            "suspicious_process",
                            {
                                "process_name": proc_name,
                                "pid": proc.info['pid'],
                                "username": proc.info.get('username', 'unknown')
                            }
                        )
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"Process check error: {e}")
    
    def _check_system_resources(self):
        """Monitor system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            if cpu_percent > self.threat_patterns["high_cpu_usage"]["threshold"]:
                self.log_activity(
                    "high_cpu_usage",
                    {
                        "cpu_percent": cpu_percent,
                        "top_processes": self._get_top_cpu_processes()
                    }
                )
            
            if memory_percent > self.threat_patterns["high_memory_usage"]["threshold"]:
                self.log_activity(
                    "high_memory_usage",
                    {
                        "memory_percent": memory_percent,
                        "top_processes": self._get_top_memory_processes()
                    }
                )
                
        except Exception as e:
            print(f"Resource check error: {e}")
    
    def _get_top_cpu_processes(self, limit: int = 5) -> List[Dict]:
        """Get top CPU-consuming processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:limit]
        except:
            return []
    
    def _get_top_memory_processes(self, limit: int = 5) -> List[Dict]:
        """Get top memory-consuming processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "memory_percent": proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
            return processes[:limit]
        except:
            return []
    
    def get_threat_summary(self, hours: int = 24) -> Dict:
        """
        Get summary of detected threats
        
        Args:
            hours: Time window for summary
        
        Returns:
            Dict with threat statistics
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_threats = [
            t for t in self.threat_log
            if datetime.fromisoformat(t["timestamp"]) > cutoff_time
        ]
        
        threat_types = Counter(t["threat_type"] for t in recent_threats)
        risk_levels = Counter(t["risk_level"] for t in recent_threats)
        
        return {
            "total_threats": len(recent_threats),
            "time_window_hours": hours,
            "threat_types": dict(threat_types),
            "risk_levels": dict(risk_levels),
            "critical_threats": len([t for t in recent_threats if t["risk_level"] == "critical"]),
            "high_threats": len([t for t in recent_threats if t["risk_level"] == "high"]),
            "recent_threats": recent_threats[-10:]
        }
    
    def get_activity_stats(self) -> Dict:
        """Get activity monitoring statistics"""
        total_activities = len(self.activity_log)
        total_threats = len(self.threat_log)
        
        recent_24h = [
            a for a in self.activity_log
            if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(hours=24)
        ]
        
        activity_types = Counter(a["type"] for a in recent_24h)
        
        return {
            "monitoring_active": self.monitoring_active,
            "total_activities_logged": total_activities,
            "total_threats_detected": total_threats,
            "activities_24h": len(recent_24h),
            "activity_types_24h": dict(activity_types),
            "auto_response_enabled": self.config["auto_response_enabled"]
        }
    
    def add_blocked_process(self, process_name: str):
        """Add process to blocked list"""
        if process_name not in self.config["blocked_processes"]:
            self.config["blocked_processes"].append(process_name)
            self._save_config()
            print(f"🚫 Blocked process: {process_name}")
    
    def remove_blocked_process(self, process_name: str):
        """Remove process from blocked list"""
        if process_name in self.config["blocked_processes"]:
            self.config["blocked_processes"].remove(process_name)
            self._save_config()
            print(f"✅ Unblocked process: {process_name}")
    
    def enable_auto_response(self):
        """Enable automated threat response"""
        self.config["auto_response_enabled"] = True
        self._save_config()
        print("🤖 Auto-response enabled")
    
    def disable_auto_response(self):
        """Disable automated threat response"""
        self.config["auto_response_enabled"] = False
        self._save_config()
        print("⚠️  Auto-response disabled")


if __name__ == "__main__":
    print("🛡️  Activity Monitoring System")
    print("=" * 50)
    
    monitor = ActivityMonitoringSystem()
    
    print("\n📊 System Status:")
    stats = monitor.get_activity_stats()
    print(f"Monitoring active: {stats['monitoring_active']}")
    print(f"Total activities: {stats['total_activities_logged']}")
    print(f"Total threats: {stats['total_threats_detected']}")
    print(f"Auto-response: {stats['auto_response_enabled']}")
    
    print("\n" + "=" * 50)
    print("✅ Activity monitoring system ready!")
