"""
Advanced CSRF Protection Engine
Comprehensive Cross-Site Request Forgery protection with token validation
"""
import time
import hashlib
import secrets
import hmac
import base64
from typing import Dict, List, Optional, Tuple
from collections import deque
import threading
import json

class AdvancedCSRFProtector:
    """Advanced CSRF Protection with Token Validation and Origin Checking"""
    
    def __init__(self):
        self.csrf_tokens = {}
        self.session_tokens = {}
        self.origin_whitelist = set()
        self.referer_whitelist = set()
        
        # CSRF Statistics
        self.csrf_stats = {
            'total_requests': 0,
            'csrf_attempts_detected': 0,
            'csrf_attempts_blocked': 0,
            'token_validations': 0,
            'token_generations': 0,
            'origin_checks': 0,
            'referer_checks': 0,
            'session_validations': 0
        }
        
        # Token configuration
        self.token_expiry = 3600  # 1 hour
        self.max_tokens_per_session = 10
        self.token_cleanup_interval = 300  # 5 minutes
        
        # Start token cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_expired_tokens, daemon=True)
        self.cleanup_thread.start()
        
        print("🛡️ Advanced CSRF Protector initialized!")
        print(f"   Token expiry: {self.token_expiry}s")
        print(f"   Max tokens per session: {self.max_tokens_per_session}")
        print(f"   Cleanup interval: {self.token_cleanup_interval}s")
    
    def generate_csrf_token(self, session_id: str, user_id: str = None) -> str:
        """Generate CSRF token for session"""
        self.csrf_stats['token_generations'] += 1
        
        # Generate random token
        token_data = f"{session_id}_{user_id}_{time.time()}_{secrets.token_hex(16)}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        
        # Store token with metadata
        self.csrf_tokens[token] = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': time.time(),
            'expires_at': time.time() + self.token_expiry,
            'used': False,
            'ip_address': None,
            'user_agent': None
        }
        
        # Store session token mapping
        if session_id not in self.session_tokens:
            self.session_tokens[session_id] = []
        
        self.session_tokens[session_id].append(token)
        
        # Limit tokens per session
        if len(self.session_tokens[session_id]) > self.max_tokens_per_session:
            oldest_token = self.session_tokens[session_id].pop(0)
            if oldest_token in self.csrf_tokens:
                del self.csrf_tokens[oldest_token]
        
        return token
    
    def validate_csrf_token(self, token: str, session_id: str, request_data: Dict) -> Dict:
        """Validate CSRF token"""
        self.csrf_stats['total_requests'] += 1
        self.csrf_stats['token_validations'] += 1
        
        validation_result = {
            'is_valid': False,
            'is_csrf_attempt': False,
            'threat_level': 0,
            'reason': None,
            'recommendations': []
        }
        
        # Check if token exists
        if token not in self.csrf_tokens:
            validation_result['is_csrf_attempt'] = True
            validation_result['threat_level'] = 90
            validation_result['reason'] = 'INVALID_TOKEN'
            validation_result['recommendations'].extend([
                'BLOCK_REQUEST',
                'LOG_ATTEMPT',
                'ALERT_SECURITY_TEAM',
                'REVIEW_SESSION_MANAGEMENT',
                'IMPLEMENT_TOKEN_VALIDATION'
            ])
            self.csrf_stats['csrf_attempts_detected'] += 1
            return validation_result
        
        token_data = self.csrf_tokens[token]
        
        # Check if token is expired
        if time.time() > token_data['expires_at']:
            validation_result['is_csrf_attempt'] = True
            validation_result['threat_level'] = 80
            validation_result['reason'] = 'EXPIRED_TOKEN'
            validation_result['recommendations'].extend([
                'BLOCK_REQUEST',
                'LOG_ATTEMPT',
                'ALERT_SECURITY_TEAM',
                'REFRESH_TOKEN',
                'IMPLEMENT_TOKEN_REFRESH'
            ])
            self.csrf_stats['csrf_attempts_detected'] += 1
            return validation_result
        
        # Check session ID match
        if token_data['session_id'] != session_id:
            validation_result['is_csrf_attempt'] = True
            validation_result['threat_level'] = 95
            validation_result['reason'] = 'SESSION_MISMATCH'
            validation_result['recommendations'].extend([
                'BLOCK_REQUEST',
                'LOG_ATTEMPT',
                'ALERT_SECURITY_TEAM',
                'REVIEW_SESSION_MANAGEMENT',
                'IMPLEMENT_SESSION_VALIDATION'
            ])
            self.csrf_stats['csrf_attempts_detected'] += 1
            return validation_result
        
        # Check if token is already used
        if token_data['used']:
            validation_result['is_csrf_attempt'] = True
            validation_result['threat_level'] = 85
            validation_result['reason'] = 'TOKEN_REUSE'
            validation_result['recommendations'].extend([
                'BLOCK_REQUEST',
                'LOG_ATTEMPT',
                'ALERT_SECURITY_TEAM',
                'IMPLEMENT_TOKEN_REUSE_PREVENTION',
                'GENERATE_NEW_TOKEN'
            ])
            self.csrf_stats['csrf_attempts_detected'] += 1
            return validation_result
        
        # Check origin
        origin_check = self._check_origin(request_data)
        if not origin_check['is_valid']:
            validation_result['is_csrf_attempt'] = True
            validation_result['threat_level'] = 70
            validation_result['reason'] = 'INVALID_ORIGIN'
            validation_result['recommendations'].extend([
                'BLOCK_REQUEST',
                'LOG_ATTEMPT',
                'ALERT_SECURITY_TEAM',
                'REVIEW_ORIGIN_VALIDATION',
                'IMPLEMENT_ORIGIN_CHECKING'
            ])
            self.csrf_stats['csrf_attempts_detected'] += 1
            return validation_result
        
        # Check referer
        referer_check = self._check_referer(request_data)
        if not referer_check['is_valid']:
            validation_result['is_csrf_attempt'] = True
            validation_result['threat_level'] = 60
            validation_result['reason'] = 'INVALID_REFERER'
            validation_result['recommendations'].extend([
                'BLOCK_REQUEST',
                'LOG_ATTEMPT',
                'ALERT_SECURITY_TEAM',
                'REVIEW_REFERER_VALIDATION',
                'IMPLEMENT_REFERER_CHECKING'
            ])
            self.csrf_stats['csrf_attempts_detected'] += 1
            return validation_result
        
        # Mark token as used
        token_data['used'] = True
        token_data['ip_address'] = request_data.get('ip_address')
        token_data['user_agent'] = request_data.get('headers', {}).get('User-Agent')
        
        # Token is valid
        validation_result['is_valid'] = True
        validation_result['reason'] = 'TOKEN_VALID'
        
        return validation_result
    
    def _check_origin(self, request_data: Dict) -> Dict:
        """Check request origin"""
        self.csrf_stats['origin_checks'] += 1
        
        origin = request_data.get('headers', {}).get('Origin')
        if not origin:
            return {'is_valid': False, 'reason': 'NO_ORIGIN_HEADER'}
        
        # Check against whitelist
        if self.origin_whitelist and origin not in self.origin_whitelist:
            return {'is_valid': False, 'reason': 'ORIGIN_NOT_WHITELISTED'}
        
        # Check origin format
        if not origin.startswith(('http://', 'https://')):
            return {'is_valid': False, 'reason': 'INVALID_ORIGIN_FORMAT'}
        
        return {'is_valid': True, 'reason': 'ORIGIN_VALID'}
    
    def _check_referer(self, request_data: Dict) -> Dict:
        """Check request referer"""
        self.csrf_stats['referer_checks'] += 1
        
        referer = request_data.get('headers', {}).get('Referer')
        if not referer:
            return {'is_valid': False, 'reason': 'NO_REFERER_HEADER'}
        
        # Check against whitelist
        if self.referer_whitelist and referer not in self.referer_whitelist:
            return {'is_valid': False, 'reason': 'REFERER_NOT_WHITELISTED'}
        
        # Check referer format
        if not referer.startswith(('http://', 'https://')):
            return {'is_valid': False, 'reason': 'INVALID_REFERER_FORMAT'}
        
        return {'is_valid': True, 'reason': 'REFERER_VALID'}
    
    def add_origin_to_whitelist(self, origin: str):
        """Add origin to whitelist"""
        self.origin_whitelist.add(origin)
        print(f"✅ Origin added to whitelist: {origin}")
    
    def add_referer_to_whitelist(self, referer: str):
        """Add referer to whitelist"""
        self.referer_whitelist.add(referer)
        print(f"✅ Referer added to whitelist: {referer}")
    
    def remove_origin_from_whitelist(self, origin: str):
        """Remove origin from whitelist"""
        if origin in self.origin_whitelist:
            self.origin_whitelist.remove(origin)
            print(f"✅ Origin removed from whitelist: {origin}")
    
    def remove_referer_from_whitelist(self, referer: str):
        """Remove referer from whitelist"""
        if referer in self.referer_whitelist:
            self.referer_whitelist.remove(referer)
            print(f"✅ Referer removed from whitelist: {referer}")
    
    def _cleanup_expired_tokens(self):
        """Cleanup expired tokens"""
        while True:
            try:
                current_time = time.time()
                expired_tokens = []
                
                for token, token_data in self.csrf_tokens.items():
                    if current_time > token_data['expires_at']:
                        expired_tokens.append(token)
                
                for token in expired_tokens:
                    if token in self.csrf_tokens:
                        session_id = self.csrf_tokens[token]['session_id']
                        if session_id in self.session_tokens:
                            if token in self.session_tokens[session_id]:
                                self.session_tokens[session_id].remove(token)
                        del self.csrf_tokens[token]
                
                if expired_tokens:
                    print(f"🧹 Cleaned up {len(expired_tokens)} expired CSRF tokens")
                
                time.sleep(self.token_cleanup_interval)
                
            except Exception as e:
                print(f"❌ CSRF token cleanup error: {e}")
                time.sleep(60)
    
    def get_csrf_statistics(self) -> Dict:
        """Get CSRF protection statistics"""
        return {
            'total_requests': self.csrf_stats['total_requests'],
            'csrf_attempts_detected': self.csrf_stats['csrf_attempts_detected'],
            'csrf_attempts_blocked': self.csrf_stats['csrf_attempts_blocked'],
            'detection_rate': (self.csrf_stats['csrf_attempts_detected'] / max(self.csrf_stats['total_requests'], 1)) * 100,
            'block_rate': (self.csrf_stats['csrf_attempts_blocked'] / max(self.csrf_stats['csrf_attempts_detected'], 1)) * 100,
            'token_validations': self.csrf_stats['token_validations'],
            'token_generations': self.csrf_stats['token_generations'],
            'origin_checks': self.csrf_stats['origin_checks'],
            'referer_checks': self.csrf_stats['referer_checks'],
            'active_tokens': len(self.csrf_tokens),
            'active_sessions': len(self.session_tokens),
            'origin_whitelist_size': len(self.origin_whitelist),
            'referer_whitelist_size': len(self.referer_whitelist)
        }
    
    def get_session_tokens(self, session_id: str) -> List[str]:
        """Get tokens for a session"""
        return self.session_tokens.get(session_id, [])
    
    def revoke_session_tokens(self, session_id: str):
        """Revoke all tokens for a session"""
        if session_id in self.session_tokens:
            for token in self.session_tokens[session_id]:
                if token in self.csrf_tokens:
                    del self.csrf_tokens[token]
            del self.session_tokens[session_id]
            print(f"✅ Revoked all tokens for session: {session_id}")
    
    def revoke_token(self, token: str):
        """Revoke a specific token"""
        if token in self.csrf_tokens:
            session_id = self.csrf_tokens[token]['session_id']
            if session_id in self.session_tokens:
                if token in self.session_tokens[session_id]:
                    self.session_tokens[session_id].remove(token)
            del self.csrf_tokens[token]
            print(f"✅ Revoked token: {token}")
    
    def generate_csrf_meta_tag(self, token: str) -> str:
        """Generate CSRF meta tag for HTML"""
        return f'<meta name="csrf-token" content="{token}">'
    
    def generate_csrf_hidden_input(self, token: str) -> str:
        """Generate CSRF hidden input for forms"""
        return f'<input type="hidden" name="csrf_token" value="{token}">'
    
    def generate_csrf_header(self, token: str) -> str:
        """Generate CSRF header for AJAX requests"""
        return f'X-CSRF-Token: {token}'
