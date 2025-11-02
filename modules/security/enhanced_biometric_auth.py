"""
🔐 Enhanced Biometric Authentication Module
Advanced security features including face recognition and fingerprint authentication
"""

import os
import json
import cv2
import numpy as np
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import hashlib
import base64

class BiometricAuthenticationSystem:
    """
    Enhanced biometric authentication with multiple methods:
    - Face recognition using OpenCV
    - Fingerprint authentication framework
    - Multi-factor biometric verification
    """
    
    def __init__(self):
        self.biometric_data_dir = "biometric_data"
        self.face_data_dir = os.path.join(self.biometric_data_dir, "faces")
        self.fingerprint_data_dir = os.path.join(self.biometric_data_dir, "fingerprints")
        self.config_file = os.path.join(self.biometric_data_dir, "biometric_config.json")
        self.auth_log_file = os.path.join(self.biometric_data_dir, "auth_log.json")
        
        self._create_directories()
        self.config = self._load_config()
        self.auth_log = self._load_auth_log()
        
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        self.authenticated_user = None
        self.last_auth_time = None
        
    def _create_directories(self):
        """Create necessary directories for biometric data storage"""
        os.makedirs(self.biometric_data_dir, exist_ok=True)
        os.makedirs(self.face_data_dir, exist_ok=True)
        os.makedirs(self.fingerprint_data_dir, exist_ok=True)
    
    def _load_config(self) -> Dict:
        """Load biometric authentication configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "face_recognition_enabled": False,
            "fingerprint_enabled": False,
            "require_both": False,
            "session_timeout_minutes": 30,
            "max_failed_attempts": 3,
            "lockout_duration_minutes": 15,
            "confidence_threshold": 70,
            "enrolled_users": []
        }
    
    def _save_config(self):
        """Save biometric configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _load_auth_log(self) -> List:
        """Load authentication attempt log"""
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
    
    def _log_auth_attempt(self, user_id: str, method: str, success: bool, details: str = ""):
        """Log authentication attempt"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "method": method,
            "success": success,
            "details": details
        }
        self.auth_log.append(entry)
        self._save_auth_log()
    
    def enroll_face(self, user_id: str, user_name: str, num_samples: int = 30) -> Dict:
        """
        Enroll a new user's face for recognition
        
        Args:
            user_id: Unique identifier for the user
            user_name: Display name
            num_samples: Number of face samples to capture
        
        Returns:
            Dict with enrollment status and message
        """
        try:
            print(f"\n👤 Enrolling face for: {user_name}")
            print("📸 Please look at the camera...")
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {
                    "success": False,
                    "message": "Cannot access camera"
                }
            
            face_samples = []
            sample_count = 0
            
            user_face_dir = os.path.join(self.face_data_dir, user_id)
            os.makedirs(user_face_dir, exist_ok=True)
            
            print(f"Capturing {num_samples} face samples...")
            
            while sample_count < num_samples:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(100, 100)
                )
                
                for (x, y, w, h) in faces:
                    sample_count += 1
                    face_roi = gray[y:y+h, x:x+w]
                    
                    face_samples.append(face_roi)
                    
                    cv2.imwrite(
                        os.path.join(user_face_dir, f"sample_{sample_count}.jpg"),
                        face_roi
                    )
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"Sample {sample_count}/{num_samples}",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2
                    )
                    
                    if sample_count >= num_samples:
                        break
                
                cv2.imshow('Face Enrollment - Press Q to cancel', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return {
                        "success": False,
                        "message": "Enrollment cancelled by user"
                    }
            
            cap.release()
            cv2.destroyAllWindows()
            
            if user_id not in self.config["enrolled_users"]:
                self.config["enrolled_users"].append({
                    "user_id": user_id,
                    "user_name": user_name,
                    "enrollment_date": datetime.now().isoformat(),
                    "face_enrolled": True,
                    "fingerprint_enrolled": False
                })
                self._save_config()
            
            self._train_face_recognizer()
            
            print(f"✅ Face enrollment successful! {sample_count} samples captured.")
            
            return {
                "success": True,
                "message": f"Face enrolled successfully with {sample_count} samples",
                "samples_captured": sample_count
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during enrollment: {str(e)}"
            }
    
    def _train_face_recognizer(self):
        """Train the face recognizer with all enrolled faces"""
        faces = []
        labels = []
        user_id_map = {}
        
        for idx, user_dir in enumerate(os.listdir(self.face_data_dir)):
            user_path = os.path.join(self.face_data_dir, user_dir)
            if not os.path.isdir(user_path):
                continue
            
            user_id_map[idx] = user_dir
            
            for img_file in os.listdir(user_path):
                if img_file.endswith('.jpg'):
                    img_path = os.path.join(user_path, img_file)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        faces.append(img)
                        labels.append(idx)
        
        if len(faces) > 0:
            self.face_recognizer.train(faces, np.array(labels))
            
            model_path = os.path.join(self.biometric_data_dir, "face_model.yml")
            self.face_recognizer.save(model_path)
            
            with open(os.path.join(self.biometric_data_dir, "user_id_map.pkl"), 'wb') as f:
                pickle.dump(user_id_map, f)
    
    def authenticate_face(self, confidence_threshold: Optional[int] = None) -> Dict:
        """
        Authenticate user using face recognition
        
        Args:
            confidence_threshold: Minimum confidence for successful authentication (lower is better)
        
        Returns:
            Dict with authentication result
        """
        if confidence_threshold is None:
            confidence_threshold = self.config["confidence_threshold"]
        
        try:
            model_path = os.path.join(self.biometric_data_dir, "face_model.yml")
            if not os.path.exists(model_path):
                return {
                    "success": False,
                    "message": "No enrolled faces. Please enroll first."
                }
            
            self.face_recognizer.read(model_path)
            
            with open(os.path.join(self.biometric_data_dir, "user_id_map.pkl"), 'rb') as f:
                user_id_map = pickle.load(f)
            
            print("\n🔐 Face Authentication")
            print("📸 Please look at the camera...")
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {
                    "success": False,
                    "message": "Cannot access camera"
                }
            
            auth_attempts = 0
            max_attempts = 30
            
            while auth_attempts < max_attempts:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(100, 100)
                )
                
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    
                    label, confidence = self.face_recognizer.predict(face_roi)
                    
                    if confidence < confidence_threshold:
                        user_id = user_id_map[label]
                        user_info = next(
                            (u for u in self.config["enrolled_users"] if u["user_id"] == user_id),
                            None
                        )
                        
                        cap.release()
                        cv2.destroyAllWindows()
                        
                        self.authenticated_user = user_id
                        self.last_auth_time = datetime.now()
                        
                        self._log_auth_attempt(
                            user_id,
                            "face_recognition",
                            True,
                            f"Confidence: {confidence:.2f}"
                        )
                        
                        print(f"✅ Authentication successful!")
                        print(f"   User: {user_info['user_name'] if user_info else user_id}")
                        print(f"   Confidence: {confidence:.2f}")
                        
                        return {
                            "success": True,
                            "user_id": user_id,
                            "user_name": user_info["user_name"] if user_info else user_id,
                            "confidence": float(confidence),
                            "method": "face_recognition"
                        }
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(
                        frame,
                        f"Confidence: {confidence:.2f}",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )
                
                cv2.imshow('Face Authentication - Press Q to cancel', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    self._log_auth_attempt("unknown", "face_recognition", False, "Cancelled by user")
                    return {
                        "success": False,
                        "message": "Authentication cancelled by user"
                    }
                
                auth_attempts += 1
            
            cap.release()
            cv2.destroyAllWindows()
            
            self._log_auth_attempt("unknown", "face_recognition", False, "Face not recognized")
            
            return {
                "success": False,
                "message": "Face not recognized or confidence too low"
            }
            
        except Exception as e:
            self._log_auth_attempt("unknown", "face_recognition", False, f"Error: {str(e)}")
            return {
                "success": False,
                "message": f"Authentication error: {str(e)}"
            }
    
    def enroll_fingerprint(self, user_id: str, user_name: str, fingerprint_data: Optional[bytes] = None) -> Dict:
        """
        Enroll fingerprint for a user
        
        Args:
            user_id: Unique user identifier
            user_name: Display name
            fingerprint_data: Binary fingerprint data from sensor or image
        
        Returns:
            Dict with enrollment status
        """
        try:
            if fingerprint_data is None:
                return {
                    "success": False,
                    "message": "No fingerprint sensor detected. Please provide fingerprint image or connect hardware sensor."
                }
            
            fingerprint_hash = hashlib.sha256(fingerprint_data).hexdigest()
            
            user_fingerprint_file = os.path.join(
                self.fingerprint_data_dir,
                f"{user_id}_fingerprint.dat"
            )
            
            with open(user_fingerprint_file, 'wb') as f:
                f.write(fingerprint_data)
            
            user_entry = next(
                (u for u in self.config["enrolled_users"] if u["user_id"] == user_id),
                None
            )
            
            if user_entry:
                user_entry["fingerprint_enrolled"] = True
            else:
                self.config["enrolled_users"].append({
                    "user_id": user_id,
                    "user_name": user_name,
                    "enrollment_date": datetime.now().isoformat(),
                    "face_enrolled": False,
                    "fingerprint_enrolled": True
                })
            
            self._save_config()
            
            return {
                "success": True,
                "message": "Fingerprint enrolled successfully",
                "fingerprint_hash": fingerprint_hash[:16]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Fingerprint enrollment error: {str(e)}"
            }
    
    def authenticate_fingerprint(self, fingerprint_data: bytes) -> Dict:
        """
        Authenticate user using fingerprint
        
        Args:
            fingerprint_data: Binary fingerprint data to verify
        
        Returns:
            Dict with authentication result
        """
        try:
            fingerprint_hash = hashlib.sha256(fingerprint_data).hexdigest()
            
            for user_file in os.listdir(self.fingerprint_data_dir):
                if user_file.endswith('_fingerprint.dat'):
                    user_id = user_file.replace('_fingerprint.dat', '')
                    
                    with open(os.path.join(self.fingerprint_data_dir, user_file), 'rb') as f:
                        stored_fingerprint = f.read()
                    
                    stored_hash = hashlib.sha256(stored_fingerprint).hexdigest()
                    
                    if fingerprint_hash == stored_hash:
                        user_info = next(
                            (u for u in self.config["enrolled_users"] if u["user_id"] == user_id),
                            None
                        )
                        
                        self.authenticated_user = user_id
                        self.last_auth_time = datetime.now()
                        
                        self._log_auth_attempt(user_id, "fingerprint", True, "Hash match")
                        
                        return {
                            "success": True,
                            "user_id": user_id,
                            "user_name": user_info["user_name"] if user_info else user_id,
                            "method": "fingerprint"
                        }
            
            self._log_auth_attempt("unknown", "fingerprint", False, "No match found")
            
            return {
                "success": False,
                "message": "Fingerprint not recognized"
            }
            
        except Exception as e:
            self._log_auth_attempt("unknown", "fingerprint", False, f"Error: {str(e)}")
            return {
                "success": False,
                "message": f"Authentication error: {str(e)}"
            }
    
    def is_session_valid(self) -> bool:
        """Check if current authentication session is still valid"""
        if not self.authenticated_user or not self.last_auth_time:
            return False
        
        timeout = timedelta(minutes=self.config["session_timeout_minutes"])
        return datetime.now() - self.last_auth_time < timeout
    
    def logout(self):
        """Clear authentication session"""
        self.authenticated_user = None
        self.last_auth_time = None
        print("🔓 Logged out successfully")
    
    def get_enrolled_users(self) -> List[Dict]:
        """Get list of all enrolled users"""
        return self.config["enrolled_users"]
    
    def remove_user(self, user_id: str) -> Dict:
        """
        Remove a user's biometric data
        
        Args:
            user_id: User to remove
        
        Returns:
            Dict with removal status
        """
        try:
            user_face_dir = os.path.join(self.face_data_dir, user_id)
            if os.path.exists(user_face_dir):
                import shutil
                shutil.rmtree(user_face_dir)
            
            fingerprint_file = os.path.join(
                self.fingerprint_data_dir,
                f"{user_id}_fingerprint.dat"
            )
            if os.path.exists(fingerprint_file):
                os.remove(fingerprint_file)
            
            self.config["enrolled_users"] = [
                u for u in self.config["enrolled_users"]
                if u["user_id"] != user_id
            ]
            self._save_config()
            
            self._train_face_recognizer()
            
            return {
                "success": True,
                "message": f"User {user_id} removed successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error removing user: {str(e)}"
            }
    
    def get_authentication_stats(self) -> Dict:
        """Get authentication statistics"""
        total_attempts = len(self.auth_log)
        successful_attempts = len([a for a in self.auth_log if a["success"]])
        failed_attempts = total_attempts - successful_attempts
        
        recent_attempts = [
            a for a in self.auth_log
            if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(hours=24)
        ]
        
        return {
            "total_attempts": total_attempts,
            "successful_attempts": successful_attempts,
            "failed_attempts": failed_attempts,
            "success_rate": (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0,
            "recent_24h_attempts": len(recent_attempts),
            "enrolled_users_count": len(self.config["enrolled_users"]),
            "last_successful_auth": max(
                [a["timestamp"] for a in self.auth_log if a["success"]],
                default=None
            )
        }


if __name__ == "__main__":
    print("🔐 Enhanced Biometric Authentication System")
    print("=" * 50)
    
    bio_auth = BiometricAuthenticationSystem()
    
    print("\n📊 System Status:")
    print(f"Enrolled users: {len(bio_auth.get_enrolled_users())}")
    
    stats = bio_auth.get_authentication_stats()
    print(f"Total auth attempts: {stats['total_attempts']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    
    print("\n" + "=" * 50)
    print("✅ Biometric system ready!")
