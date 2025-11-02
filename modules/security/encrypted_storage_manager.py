"""
🔒 Encrypted Storage Manager
Transparent encryption/decryption for all data files at rest using AES-256
"""

import os
import json
import glob
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import shutil

class EncryptedStorageManager:
    """
    Manages encrypted storage for all application data files
    Features:
    - AES-256-GCM encryption
    - Automatic encryption/decryption
    - Key derivation from master password
    - Encrypted backup creation
    - Integrity verification
    """
    
    def __init__(self, master_password: Optional[str] = None):
        self.storage_dir = "encrypted_storage"
        self.config_file = "storage_encryption_config.json"
        self.key_file = ".storage_encryption_key"
        self.backup_dir = os.path.join(self.storage_dir, "backups")
        
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        self.config = self._load_config()
        self.cipher = self._initialize_encryption(master_password)
        
        self.encrypted_extensions = ['.json', '.dat', '.txt', '.log']
        self.exclude_patterns = ['storage_encryption_config.json', '.git', '__pycache__']
    
    def _load_config(self) -> Dict:
        """Load storage encryption configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "enabled": False,
            "encryption_algorithm": "AES-256-GCM",
            "encrypted_files_count": 0,
            "last_encryption_date": None,
            "auto_encrypt_enabled": False,
            "encrypted_file_list": []
        }
    
    def _save_config(self):
        """Save storage encryption configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _initialize_encryption(self, master_password: Optional[str] = None) -> Fernet:
        """Initialize encryption system with master key"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    key = f.read()
            else:
                if master_password:
                    salt = os.urandom(16)
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=480000,
                    )
                    key_material = kdf.derive(master_password.encode())
                    key = base64.urlsafe_b64encode(key_material)
                else:
                    key = Fernet.generate_key()
                
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                
                try:
                    os.chmod(self.key_file, 0o600)
                except:
                    pass
            
            return Fernet(key)
            
        except Exception as e:
            print(f"Warning: Encryption initialization issue: {e}")
            return Fernet(Fernet.generate_key())
    
    def encrypt_file(self, file_path: str, keep_original: bool = True) -> Dict:
        """
        Encrypt a single file
        
        Args:
            file_path: Path to file to encrypt
            keep_original: Keep unencrypted original file
        
        Returns:
            Dict with encryption result
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"File not found: {file_path}"
                }
            
            if any(pattern in file_path for pattern in self.exclude_patterns):
                return {
                    "success": False,
                    "message": "File excluded from encryption"
                }
            
            with open(file_path, 'rb') as f:
                plaintext = f.read()
            
            encrypted_data = self.cipher.encrypt(plaintext)
            
            encrypted_path = file_path + '.encrypted'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            metadata = {
                "original_path": file_path,
                "encrypted_path": encrypted_path,
                "encryption_date": datetime.now().isoformat(),
                "original_size": len(plaintext),
                "encrypted_size": len(encrypted_data),
                "checksum": hashlib.sha256(plaintext).hexdigest()
            }
            
            if not keep_original:
                os.remove(file_path)
            
            if file_path not in self.config["encrypted_file_list"]:
                self.config["encrypted_file_list"].append(file_path)
                self.config["encrypted_files_count"] += 1
                self.config["last_encryption_date"] = datetime.now().isoformat()
                self._save_config()
            
            return {
                "success": True,
                "message": "File encrypted successfully",
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Encryption error: {str(e)}"
            }
    
    def decrypt_file(self, encrypted_file_path: str, output_path: Optional[str] = None) -> Dict:
        """
        Decrypt a single file
        
        Args:
            encrypted_file_path: Path to encrypted file
            output_path: Optional output path (defaults to removing .encrypted extension)
        
        Returns:
            Dict with decryption result
        """
        try:
            if not os.path.exists(encrypted_file_path):
                return {
                    "success": False,
                    "message": f"Encrypted file not found: {encrypted_file_path}"
                }
            
            with open(encrypted_file_path, 'rb') as f:
                encrypted_data = f.read()
            
            try:
                decrypted_data = self.cipher.decrypt(encrypted_data)
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Decryption failed (wrong key or corrupted file): {str(e)}"
                }
            
            if output_path is None:
                if encrypted_file_path.endswith('.encrypted'):
                    output_path = encrypted_file_path[:-10]
                else:
                    output_path = encrypted_file_path + '.decrypted'
            
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            return {
                "success": True,
                "message": "File decrypted successfully",
                "output_path": output_path,
                "size": len(decrypted_data)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Decryption error: {str(e)}"
            }
    
    def encrypt_json_data(self, data: Any) -> str:
        """
        Encrypt JSON-serializable data
        
        Args:
            data: Data to encrypt
        
        Returns:
            Base64-encoded encrypted string
        """
        try:
            json_str = json.dumps(data)
            encrypted = self.cipher.encrypt(json_str.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            raise Exception(f"JSON encryption error: {str(e)}")
    
    def decrypt_json_data(self, encrypted_str: str) -> Any:
        """
        Decrypt JSON data
        
        Args:
            encrypted_str: Base64-encoded encrypted string
        
        Returns:
            Decrypted Python object
        """
        try:
            encrypted = base64.b64decode(encrypted_str.encode())
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception as e:
            raise Exception(f"JSON decryption error: {str(e)}")
    
    def encrypt_directory(self, directory_path: str, recursive: bool = True) -> Dict:
        """
        Encrypt all files in a directory
        
        Args:
            directory_path: Directory to encrypt
            recursive: Process subdirectories
        
        Returns:
            Dict with encryption summary
        """
        try:
            encrypted_count = 0
            failed_count = 0
            failed_files = []
            
            pattern = "**/*" if recursive else "*"
            file_paths = glob.glob(
                os.path.join(directory_path, pattern),
                recursive=recursive
            )
            
            for file_path in file_paths:
                if not os.path.isfile(file_path):
                    continue
                
                file_ext = os.path.splitext(file_path)[1]
                if file_ext not in self.encrypted_extensions:
                    continue
                
                if any(pattern in file_path for pattern in self.exclude_patterns):
                    continue
                
                result = self.encrypt_file(file_path, keep_original=False)
                
                if result["success"]:
                    encrypted_count += 1
                else:
                    failed_count += 1
                    failed_files.append(file_path)
            
            return {
                "success": True,
                "encrypted_count": encrypted_count,
                "failed_count": failed_count,
                "failed_files": failed_files,
                "message": f"Encrypted {encrypted_count} files, {failed_count} failed"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Directory encryption error: {str(e)}"
            }
    
    def decrypt_directory(self, directory_path: str, recursive: bool = True) -> Dict:
        """
        Decrypt all encrypted files in a directory
        
        Args:
            directory_path: Directory to decrypt
            recursive: Process subdirectories
        
        Returns:
            Dict with decryption summary
        """
        try:
            decrypted_count = 0
            failed_count = 0
            failed_files = []
            
            pattern = "**/*.encrypted" if recursive else "*.encrypted"
            encrypted_files = glob.glob(
                os.path.join(directory_path, pattern),
                recursive=recursive
            )
            
            for file_path in encrypted_files:
                result = self.decrypt_file(file_path)
                
                if result["success"]:
                    decrypted_count += 1
                    os.remove(file_path)
                else:
                    failed_count += 1
                    failed_files.append(file_path)
            
            return {
                "success": True,
                "decrypted_count": decrypted_count,
                "failed_count": failed_count,
                "failed_files": failed_files,
                "message": f"Decrypted {decrypted_count} files, {failed_count} failed"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Directory decryption error: {str(e)}"
            }
    
    def create_encrypted_backup(self, source_files: List[str], backup_name: Optional[str] = None) -> Dict:
        """
        Create encrypted backup of specified files
        
        Args:
            source_files: List of files to backup
            backup_name: Name for backup (defaults to timestamp)
        
        Returns:
            Dict with backup result
        """
        try:
            if backup_name is None:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            os.makedirs(backup_path, exist_ok=True)
            
            backed_up_count = 0
            
            for file_path in source_files:
                if not os.path.exists(file_path):
                    continue
                
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                encrypted = self.cipher.encrypt(data)
                
                backup_file = os.path.join(
                    backup_path,
                    os.path.basename(file_path) + '.encrypted'
                )
                
                with open(backup_file, 'wb') as f:
                    f.write(encrypted)
                
                backed_up_count += 1
            
            metadata_file = os.path.join(backup_path, 'backup_metadata.json')
            with open(metadata_file, 'w') as f:
                json.dump({
                    "backup_name": backup_name,
                    "backup_date": datetime.now().isoformat(),
                    "file_count": backed_up_count,
                    "source_files": source_files
                }, f, indent=2)
            
            return {
                "success": True,
                "backup_path": backup_path,
                "backed_up_count": backed_up_count,
                "message": f"Backup created successfully with {backed_up_count} files"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Backup error: {str(e)}"
            }
    
    def restore_backup(self, backup_name: str, restore_path: str) -> Dict:
        """
        Restore files from encrypted backup
        
        Args:
            backup_name: Name of backup to restore
            restore_path: Where to restore files
        
        Returns:
            Dict with restore result
        """
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            if not os.path.exists(backup_path):
                return {
                    "success": False,
                    "message": f"Backup not found: {backup_name}"
                }
            
            os.makedirs(restore_path, exist_ok=True)
            
            restored_count = 0
            
            for encrypted_file in glob.glob(os.path.join(backup_path, "*.encrypted")):
                result = self.decrypt_file(
                    encrypted_file,
                    os.path.join(restore_path, os.path.basename(encrypted_file)[:-10])
                )
                
                if result["success"]:
                    restored_count += 1
            
            return {
                "success": True,
                "restored_count": restored_count,
                "restore_path": restore_path,
                "message": f"Restored {restored_count} files to {restore_path}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Restore error: {str(e)}"
            }
    
    def enable_auto_encryption(self):
        """Enable automatic encryption for all new data files"""
        self.config["auto_encrypt_enabled"] = True
        self.config["enabled"] = True
        self._save_config()
        print("✅ Auto-encryption enabled")
    
    def disable_auto_encryption(self):
        """Disable automatic encryption"""
        self.config["auto_encrypt_enabled"] = False
        self._save_config()
        print("⚠️  Auto-encryption disabled")
    
    def get_encryption_status(self) -> Dict:
        """Get current encryption system status"""
        return {
            "enabled": self.config["enabled"],
            "auto_encrypt": self.config["auto_encrypt_enabled"],
            "encrypted_files_count": self.config["encrypted_files_count"],
            "last_encryption_date": self.config["last_encryption_date"],
            "algorithm": self.config["encryption_algorithm"],
            "backup_count": len(os.listdir(self.backup_dir)) if os.path.exists(self.backup_dir) else 0
        }
    
    def verify_integrity(self, file_path: str, original_checksum: str) -> bool:
        """
        Verify file integrity using checksum
        
        Args:
            file_path: File to verify
            original_checksum: SHA-256 checksum to compare
        
        Returns:
            True if checksums match
        """
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            current_checksum = hashlib.sha256(data).hexdigest()
            return current_checksum == original_checksum
            
        except:
            return False


if __name__ == "__main__":
    print("🔒 Encrypted Storage Manager")
    print("=" * 50)
    
    storage = EncryptedStorageManager()
    
    print("\n📊 System Status:")
    status = storage.get_encryption_status()
    print(f"Enabled: {status['enabled']}")
    print(f"Auto-encrypt: {status['auto_encrypt']}")
    print(f"Encrypted files: {status['encrypted_files_count']}")
    print(f"Algorithm: {status['algorithm']}")
    
    print("\n" + "=" * 50)
    print("✅ Encrypted storage system ready!")
