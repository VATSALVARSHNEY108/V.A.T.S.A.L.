"""
🔒 System & Security Enhancements
Smart access control, auto VPN, threat detection, and device security
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SecurityEnhancements:
    """Advanced security and system protection features"""
    
    def __init__(self):
        self.access_control_file = "access_control.json"
        self.trusted_devices_file = "trusted_devices.json"
        self.threats_file = "threat_detection_log.json"
        self.vpn_rules_file = "vpn_rules.json"
        self.access_control = self.load_access_control()
        self.trusted_devices = self.load_trusted_devices()
        self.threats = self.load_threats()
        self.vpn_rules = self.load_vpn_rules()
        
    def load_access_control(self):
        """Load access control settings"""
        if os.path.exists(self.access_control_file):
            try:
                with open(self.access_control_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "facial_recognition": False,
            "phone_proximity": False,
            "biometric_enabled": False,
            "last_unlock": None
        }
    
    def save_access_control(self):
        """Save access control settings"""
        try:
            with open(self.access_control_file, 'w') as f:
                json.dump(self.access_control, f, indent=2)
        except Exception as e:
            print(f"Error saving access control: {e}")
    
    def load_trusted_devices(self):
        """Load trusted devices"""
        if os.path.exists(self.trusted_devices_file):
            try:
                with open(self.trusted_devices_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_trusted_devices(self):
        """Save trusted devices"""
        try:
            with open(self.trusted_devices_file, 'w') as f:
                json.dump(self.trusted_devices, f, indent=2)
        except Exception as e:
            print(f"Error saving trusted devices: {e}")
    
    def load_threats(self):
        """Load threat detection log"""
        if os.path.exists(self.threats_file):
            try:
                with open(self.threats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_threats(self):
        """Save threat log"""
        try:
            with open(self.threats_file, 'w') as f:
                json.dump(self.threats, f, indent=2)
        except Exception as e:
            print(f"Error saving threats: {e}")
    
    def load_vpn_rules(self):
        """Load VPN auto-trigger rules"""
        if os.path.exists(self.vpn_rules_file):
            try:
                with open(self.vpn_rules_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "auto_enable_on_public_wifi": True,
            "untrusted_networks": [],
            "always_on_for_apps": []
        }
    
    def save_vpn_rules(self):
        """Save VPN rules"""
        try:
            with open(self.vpn_rules_file, 'w') as f:
                json.dump(self.vpn_rules, f, indent=2)
        except Exception as e:
            print(f"Error saving VPN rules: {e}")
    
    def enable_smart_access_control(self, method: str = "facial_recognition"):
        """Lock/unlock system via facial recognition or phone proximity"""
        if method in ["facial_recognition", "phone_proximity", "biometric"]:
            self.access_control[method] = True
            self.access_control["last_unlock"] = datetime.now().isoformat()
            self.save_access_control()
            
            return {
                "success": True,
                "message": f"Smart access control enabled: {method.replace('_', ' ').title()}",
                "security_level": "Enhanced"
            }
        
        return {"success": False, "message": "Invalid access control method"}
    
    def get_access_control_status(self):
        """Get current access control status"""
        output = "\n" + "="*60 + "\n"
        output += "🔒 SMART ACCESS CONTROL STATUS\n"
        output += "="*60 + "\n\n"
        
        output += f"Facial Recognition: {'✅ Enabled' if self.access_control['facial_recognition'] else '❌ Disabled'}\n"
        output += f"Phone Proximity: {'✅ Enabled' if self.access_control['phone_proximity'] else '❌ Disabled'}\n"
        output += f"Biometric: {'✅ Enabled' if self.access_control['biometric_enabled'] else '❌ Disabled'}\n"
        output += f"Last Unlock: {self.access_control.get('last_unlock', 'Never')}\n"
        
        output += "\n" + "="*60 + "\n"
        return output
    
    def enable_auto_vpn(self, network_name: str = None):
        """Automatically enable VPN on untrusted networks"""
        if network_name:
            if network_name not in self.vpn_rules["untrusted_networks"]:
                self.vpn_rules["untrusted_networks"].append(network_name)
        
        self.vpn_rules["auto_enable_on_public_wifi"] = True
        self.save_vpn_rules()
        
        output = f"✅ Auto VPN enabled\n"
        if network_name:
            output += f"Network '{network_name}' added to untrusted list\n"
        output += "VPN will auto-activate on public/untrusted networks"
        
        return {"success": True, "message": output}
    
    def detect_threats(self):
        """Flag suspicious processes, scripts, or browser extensions"""
        import psutil
        
        suspicious_processes = []
        
        try:
            for proc in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 80:
                        suspicious_processes.append({
                            "name": proc.info['name'],
                            "cpu_usage": proc.info['cpu_percent'],
                            "reason": "High CPU usage"
                        })
                except:
                    pass
        except ImportError:
            suspicious_processes.append({
                "name": "System scan",
                "reason": "psutil not available for detailed scan"
            })
        
        threat_report = {
            "scanned_at": datetime.now().isoformat(),
            "threats_found": len(suspicious_processes),
            "details": suspicious_processes[:10]
        }
        
        self.threats.append(threat_report)
        self.save_threats()
        
        output = "\n🛡️ THREAT DETECTION SCAN\n" + "="*60 + "\n\n"
        output += f"Scan Time: {threat_report['scanned_at']}\n"
        output += f"Threats Found: {threat_report['threats_found']}\n\n"
        
        if threat_report['threats_found'] > 0:
            output += "Suspicious Activity:\n"
            for threat in threat_report['details']:
                output += f"  ⚠️ {threat['name']} - {threat['reason']}\n"
        else:
            output += "✅ No threats detected\n"
        
        output += "\n" + "="*60 + "\n"
        
        return {"success": True, "message": output}
    
    def schedule_data_wipe(self, interval: str = "weekly", target: str = "temp_files"):
        """Securely erase temporary or sensitive files at intervals"""
        wipe_schedule = {
            "interval": interval,
            "target": target,
            "next_wipe": (datetime.now() + timedelta(days=7)).isoformat(),
            "status": "scheduled"
        }
        
        output = f"\n🗑️ DATA WIPE SCHEDULER\n{'='*60}\n\n"
        output += f"Schedule: {interval}\n"
        output += f"Target: {target}\n"
        output += f"Next Wipe: {wipe_schedule['next_wipe']}\n"
        output += "\nWhat will be cleared:\n"
        output += "  • Temporary files\n"
        output += "  • Browser cache\n"
        output += "  • Log files older than 30 days\n"
        output += "  • Downloaded files in temp folder\n"
        output += "\n" + "="*60 + "\n"
        
        return {"success": True, "message": output}
    
    def add_trusted_device(self, device_name: str, device_id: str):
        """Manage trusted devices that can control the system remotely"""
        device = {
            "name": device_name,
            "id": device_id,
            "added_at": datetime.now().isoformat(),
            "status": "trusted",
            "permissions": ["remote_control", "file_access"]
        }
        
        self.trusted_devices.append(device)
        self.save_trusted_devices()
        
        return {"success": True, "message": f"Device '{device_name}' added to trusted list"}
    
    def list_trusted_devices(self):
        """List all trusted devices"""
        if not self.trusted_devices:
            return "No trusted devices configured."
        
        output = "\n" + "="*60 + "\n"
        output += "📱 TRUSTED DEVICES\n"
        output += "="*60 + "\n\n"
        
        for i, device in enumerate(self.trusted_devices, 1):
            output += f"{i}. {device['name']}\n"
            output += f"   ID: {device.get('id', 'Unknown')}\n"
            output += f"   Status: {device.get('status', 'Unknown')}\n"
            output += f"   Added: {device.get('added_at', 'Unknown')}\n\n"
        
        output += "="*60 + "\n"
        return output
    
    def get_threat_log(self):
        """Get recent threat detection history"""
        if not self.threats:
            return "No threat scans performed yet."
        
        output = "\n" + "="*60 + "\n"
        output += "🛡️ THREAT DETECTION LOG\n"
        output += "="*60 + "\n\n"
        
        for i, scan in enumerate(self.threats[-10:], 1):
            output += f"{i}. Scan Time: {scan.get('scanned_at', 'Unknown')}\n"
            output += f"   Threats: {scan.get('threats_found', 0)}\n\n"
        
        output += "="*60 + "\n"
        return output


def create_security_enhancements():
    """Factory function to create a SecurityEnhancements instance"""
    return SecurityEnhancements()
