"""
🔐 Two-Factor Authentication (2FA) Module
TOTP-based 2FA with QR code generation and backup codes
"""

import os
import json
import pyotp
import qrcode
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from io import BytesIO
import base64

class TwoFactorAuthentication:
    """
    Two-Factor Authentication system using TOTP (Time-Based One-Time Password)
    Compatible with Google Authenticator, Authy, Microsoft Authenticator, etc.
    """
    
    def __init__(self, app_name: str = "VATSAL AI Assistant"):
        self.app_name = app_name
        self.data_dir = "2fa_data"
        self.users_file = os.path.join(self.data_dir, "2fa_users.json")
        self.backup_codes_file = os.path.join(self.data_dir, "backup_codes.json")
        self.auth_log_file = os.path.join(self.data_dir, "2fa_auth_log.json")
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.users = self._load_users()
        self.backup_codes = self._load_backup_codes()
        self.auth_log = self._load_auth_log()
    
    def _load_users(self) -> Dict:
        """Load 2FA user data"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_users(self):
        """Save 2FA user data"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _load_backup_codes(self) -> Dict:
        """Load backup codes"""
        if os.path.exists(self.backup_codes_file):
            try:
                with open(self.backup_codes_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_backup_codes(self):
        """Save backup codes"""
        try:
            with open(self.backup_codes_file, 'w') as f:
                json.dump(self.backup_codes, f, indent=2)
        except Exception as e:
            print(f"Error saving backup codes: {e}")
    
    def _load_auth_log(self) -> List:
        """Load authentication log"""
        if os.path.exists(self.auth_log_file):
            try:
                with open(self.auth_log_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_auth_log(self):
        """Save authentication log"""
        try:
            with open(self.auth_log_file, 'w') as f:
                json.dump(self.auth_log[-100:], f, indent=2)
        except Exception as e:
            print(f"Error saving auth log: {e}")
    
    def _log_auth_attempt(self, user_id: str, success: bool, method: str = "totp", details: str = ""):
        """Log 2FA authentication attempt"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "method": method,
            "success": success,
            "details": details
        }
        self.auth_log.append(entry)
        self._save_auth_log()
    
    def _generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup recovery codes"""
        codes = []
        for _ in range(count):
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)
        return codes
    
    def enable_2fa(self, user_id: str, user_email: str) -> Dict:
        """
        Enable 2FA for a user
        
        Args:
            user_id: Unique user identifier
            user_email: User's email address
        
        Returns:
            Dict containing secret, QR code, and backup codes
        """
        try:
            secret = pyotp.random_base32()
            
            totp = pyotp.TOTP(secret)
            
            provisioning_uri = totp.provisioning_uri(
                name=user_email,
                issuer_name=self.app_name
            )
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            qr_image_path = os.path.join(self.data_dir, f"qr_{user_id}.png")
            img.save(qr_image_path)
            
            backup_codes = self._generate_backup_codes()
            
            self.users[user_id] = {
                "secret": secret,
                "email": user_email,
                "enabled": True,
                "enrolled_date": datetime.now().isoformat(),
                "verified": False
            }
            self._save_users()
            
            self.backup_codes[user_id] = {
                "codes": backup_codes,
                "used": []
            }
            self._save_backup_codes()
            
            print(f"✅ 2FA enabled for {user_email}")
            print(f"📱 Scan the QR code with your authenticator app")
            print(f"💾 Backup codes generated: {len(backup_codes)}")
            
            return {
                "success": True,
                "secret": secret,
                "qr_code_base64": qr_code_base64,
                "qr_code_path": qr_image_path,
                "provisioning_uri": provisioning_uri,
                "backup_codes": backup_codes,
                "message": "2FA enabled successfully. Scan QR code and save backup codes."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error enabling 2FA: {str(e)}"
            }
    
    def verify_totp(self, user_id: str, token: str, mark_verified: bool = True) -> Dict:
        """
        Verify a TOTP token
        
        Args:
            user_id: User identifier
            token: 6-digit TOTP code
            mark_verified: Mark user as verified after successful verification
        
        Returns:
            Dict with verification result
        """
        try:
            if user_id not in self.users:
                self._log_auth_attempt(user_id, False, "totp", "User not found")
                return {
                    "success": False,
                    "message": "2FA not enabled for this user"
                }
            
            user_data = self.users[user_id]
            if not user_data.get("enabled", False):
                self._log_auth_attempt(user_id, False, "totp", "2FA not enabled")
                return {
                    "success": False,
                    "message": "2FA is not enabled"
                }
            
            secret = user_data["secret"]
            totp = pyotp.TOTP(secret)
            
            is_valid = totp.verify(token, valid_window=1)
            
            if is_valid:
                if mark_verified and not user_data.get("verified", False):
                    self.users[user_id]["verified"] = True
                    self._save_users()
                
                self.users[user_id]["last_success"] = datetime.now().isoformat()
                self._save_users()
                
                self._log_auth_attempt(user_id, True, "totp", "Token verified")
                
                return {
                    "success": True,
                    "message": "Authentication successful",
                    "verified": True
                }
            else:
                self._log_auth_attempt(user_id, False, "totp", "Invalid token")
                return {
                    "success": False,
                    "message": "Invalid or expired token"
                }
                
        except Exception as e:
            self._log_auth_attempt(user_id, False, "totp", f"Error: {str(e)}")
            return {
                "success": False,
                "message": f"Verification error: {str(e)}"
            }
    
    def verify_backup_code(self, user_id: str, backup_code: str) -> Dict:
        """
        Verify and use a backup code
        
        Args:
            user_id: User identifier
            backup_code: Backup recovery code
        
        Returns:
            Dict with verification result
        """
        try:
            if user_id not in self.backup_codes:
                self._log_auth_attempt(user_id, False, "backup_code", "No backup codes")
                return {
                    "success": False,
                    "message": "No backup codes found"
                }
            
            user_backup_data = self.backup_codes[user_id]
            available_codes = user_backup_data["codes"]
            used_codes = user_backup_data["used"]
            
            backup_code = backup_code.strip().upper()
            
            if backup_code in available_codes and backup_code not in used_codes:
                used_codes.append(backup_code)
                self.backup_codes[user_id]["used"] = used_codes
                self.backup_codes[user_id]["last_used"] = datetime.now().isoformat()
                self._save_backup_codes()
                
                remaining = len(available_codes) - len(used_codes)
                
                self._log_auth_attempt(user_id, True, "backup_code", f"Code used. {remaining} remaining")
                
                return {
                    "success": True,
                    "message": "Backup code verified successfully",
                    "remaining_codes": remaining,
                    "warning": "Consider regenerating backup codes if running low" if remaining < 3 else None
                }
            else:
                self._log_auth_attempt(user_id, False, "backup_code", "Invalid or used code")
                return {
                    "success": False,
                    "message": "Invalid or already used backup code"
                }
                
        except Exception as e:
            self._log_auth_attempt(user_id, False, "backup_code", f"Error: {str(e)}")
            return {
                "success": False,
                "message": f"Verification error: {str(e)}"
            }
    
    def regenerate_backup_codes(self, user_id: str, current_token: str) -> Dict:
        """
        Regenerate backup codes (requires current TOTP verification)
        
        Args:
            user_id: User identifier
            current_token: Current valid TOTP token
        
        Returns:
            Dict with new backup codes
        """
        try:
            verification = self.verify_totp(user_id, current_token, mark_verified=False)
            
            if not verification["success"]:
                return {
                    "success": False,
                    "message": "Please provide valid TOTP token to regenerate backup codes"
                }
            
            new_codes = self._generate_backup_codes()
            
            self.backup_codes[user_id] = {
                "codes": new_codes,
                "used": [],
                "regenerated_date": datetime.now().isoformat()
            }
            self._save_backup_codes()
            
            print(f"🔄 Backup codes regenerated for user: {user_id}")
            
            return {
                "success": True,
                "backup_codes": new_codes,
                "message": "Backup codes regenerated successfully. Save these in a secure location."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error regenerating codes: {str(e)}"
            }
    
    def disable_2fa(self, user_id: str, token: str) -> Dict:
        """
        Disable 2FA for a user (requires TOTP verification)
        
        Args:
            user_id: User identifier
            token: Current valid TOTP token
        
        Returns:
            Dict with disable status
        """
        try:
            verification = self.verify_totp(user_id, token, mark_verified=False)
            
            if not verification["success"]:
                return {
                    "success": False,
                    "message": "Please provide valid TOTP token to disable 2FA"
                }
            
            if user_id in self.users:
                self.users[user_id]["enabled"] = False
                self.users[user_id]["disabled_date"] = datetime.now().isoformat()
                self._save_users()
            
            print(f"⚠️  2FA disabled for user: {user_id}")
            
            return {
                "success": True,
                "message": "2FA disabled successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error disabling 2FA: {str(e)}"
            }
    
    def get_current_totp(self, user_id: str) -> Optional[str]:
        """
        Get current TOTP token (for testing/debugging only)
        
        Args:
            user_id: User identifier
        
        Returns:
            Current 6-digit TOTP token or None
        """
        if user_id not in self.users:
            return None
        
        secret = self.users[user_id]["secret"]
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    def get_user_status(self, user_id: str) -> Dict:
        """
        Get 2FA status for a user
        
        Args:
            user_id: User identifier
        
        Returns:
            Dict with user 2FA status
        """
        if user_id not in self.users:
            return {
                "enabled": False,
                "message": "2FA not enabled"
            }
        
        user_data = self.users[user_id]
        backup_data = self.backup_codes.get(user_id, {})
        
        available_codes = len(backup_data.get("codes", []))
        used_codes = len(backup_data.get("used", []))
        
        return {
            "enabled": user_data.get("enabled", False),
            "verified": user_data.get("verified", False),
            "email": user_data.get("email", ""),
            "enrolled_date": user_data.get("enrolled_date", ""),
            "last_success": user_data.get("last_success", "Never"),
            "backup_codes_available": available_codes - used_codes,
            "total_backup_codes": available_codes
        }
    
    def get_statistics(self) -> Dict:
        """Get 2FA system statistics"""
        total_users = len(self.users)
        enabled_users = len([u for u in self.users.values() if u.get("enabled", False)])
        verified_users = len([u for u in self.users.values() if u.get("verified", False)])
        
        total_attempts = len(self.auth_log)
        successful_attempts = len([a for a in self.auth_log if a["success"]])
        
        recent_attempts = [
            a for a in self.auth_log
            if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(hours=24)
        ]
        
        return {
            "total_users": total_users,
            "enabled_users": enabled_users,
            "verified_users": verified_users,
            "total_auth_attempts": total_attempts,
            "successful_attempts": successful_attempts,
            "success_rate": (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0,
            "recent_24h_attempts": len(recent_attempts),
            "totp_attempts": len([a for a in self.auth_log if a["method"] == "totp"]),
            "backup_code_attempts": len([a for a in self.auth_log if a["method"] == "backup_code"])
        }


if __name__ == "__main__":
    print("🔐 Two-Factor Authentication System")
    print("=" * 50)
    
    tfa = TwoFactorAuthentication()
    
    print("\n📊 System Status:")
    stats = tfa.get_statistics()
    print(f"Total users: {stats['total_users']}")
    print(f"Enabled users: {stats['enabled_users']}")
    print(f"Total attempts: {stats['total_auth_attempts']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    
    print("\n" + "=" * 50)
    print("✅ 2FA system ready!")
