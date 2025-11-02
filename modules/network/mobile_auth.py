#!/usr/bin/env python3
"""
Authentication and Security for VATSAL Mobile Companion
"""

import os
import secrets
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()


class MobileAuth:
    def __init__(self):
        self.tokens = {}
        self.api_keys = {}
        self.token_file = Path('mobile_tokens.json')
        self.api_key_file = Path('mobile_api_keys.json')
        self.master_pin = os.getenv('MOBILE_PIN', '1234')
        
        self._load_tokens()
        self._load_api_keys()
    
    def _load_tokens(self):
        """Load active tokens from file"""
        if self.token_file.exists():
            try:
                with open(self.token_file, 'r') as f:
                    self.tokens = json.load(f)
                
                self._cleanup_expired_tokens()
            except:
                self.tokens = {}
    
    def _save_tokens(self):
        """Save tokens to file"""
        try:
            with open(self.token_file, 'w') as f:
                json.dump(self.tokens, f, indent=2)
        except Exception as e:
            print(f"Error saving tokens: {e}")
    
    def _load_api_keys(self):
        """Load API keys from file"""
        if self.api_key_file.exists():
            try:
                with open(self.api_key_file, 'r') as f:
                    self.api_keys = json.load(f)
            except:
                self.api_keys = {}
    
    def _save_api_keys(self):
        """Save API keys to file"""
        try:
            with open(self.api_key_file, 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            print(f"Error saving API keys: {e}")
    
    def _cleanup_expired_tokens(self):
        """Remove expired tokens"""
        current_time = datetime.now().isoformat()
        expired = [
            token for token, data in self.tokens.items()
            if data.get('expires_at', '') < current_time
        ]
        
        for token in expired:
            del self.tokens[token]
        
        if expired:
            self._save_tokens()
    
    def generate_token(self, device_id, pin, duration_hours=24):
        """Generate authentication token"""
        if pin != self.master_pin:
            return None
        
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=duration_hours)
        
        self.tokens[token] = {
            'device_id': device_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'last_used': datetime.now().isoformat()
        }
        
        self._save_tokens()
        
        return {
            'token': token,
            'expires_at': expires_at.isoformat(),
            'device_id': device_id
        }
    
    def validate_token(self, token):
        """Validate authentication token"""
        if not token:
            return False
        
        self._cleanup_expired_tokens()
        
        if token in self.tokens:
            self.tokens[token]['last_used'] = datetime.now().isoformat()
            self._save_tokens()
            return True
        
        return False
    
    def revoke_token(self, token):
        """Revoke a token"""
        if token in self.tokens:
            del self.tokens[token]
            self._save_tokens()
            return True
        return False
    
    def generate_api_key(self, name, description=''):
        """Generate API key"""
        api_key = f"vatsal_{secrets.token_urlsafe(32)}"
        
        self.api_keys[api_key] = {
            'name': name,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'usage_count': 0
        }
        
        self._save_api_keys()
        
        return api_key
    
    def validate_api_key(self, api_key):
        """Validate API key"""
        if not api_key:
            return False
        
        if api_key in self.api_keys:
            self.api_keys[api_key]['last_used'] = datetime.now().isoformat()
            self.api_keys[api_key]['usage_count'] += 1
            self._save_api_keys()
            return True
        
        return False
    
    def revoke_api_key(self, api_key):
        """Revoke API key"""
        if api_key in self.api_keys:
            del self.api_keys[api_key]
            self._save_api_keys()
            return True
        return False
    
    def list_tokens(self):
        """List all active tokens"""
        self._cleanup_expired_tokens()
        return {
            'tokens': [
                {
                    'device_id': data['device_id'],
                    'created_at': data['created_at'],
                    'expires_at': data['expires_at'],
                    'last_used': data['last_used']
                }
                for data in self.tokens.values()
            ]
        }
    
    def list_api_keys(self):
        """List all API keys"""
        return {
            'api_keys': [
                {
                    'name': data['name'],
                    'description': data['description'],
                    'created_at': data['created_at'],
                    'last_used': data['last_used'],
                    'usage_count': data['usage_count']
                }
                for data in self.api_keys.values()
            ]
        }


mobile_auth = MobileAuth()


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'success': False,
                'error': 'No authorization provided',
                'code': 'NO_AUTH'
            }), 401
        
        if auth_header.startswith('Bearer '):
            token = auth_header.replace('Bearer ', '')
            if mobile_auth.validate_token(token):
                return f(*args, **kwargs)
        
        elif auth_header.startswith('ApiKey '):
            api_key = auth_header.replace('ApiKey ', '')
            if mobile_auth.validate_api_key(api_key):
                return f(*args, **kwargs)
        
        return jsonify({
            'success': False,
            'error': 'Invalid or expired credentials',
            'code': 'INVALID_AUTH'
        }), 401
    
    return decorated_function


def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr


if __name__ == '__main__':
    auth = MobileAuth()
    print('🔐 VATSAL Mobile Authentication System')
    print('=' * 50)
    print(f'Master PIN: {auth.master_pin}')
    print('\nTo authenticate:')
    print('1. POST to /api/mobile/auth with PIN')
    print('2. Use returned token in Authorization header')
    print('3. Format: Authorization: Bearer <token>')
