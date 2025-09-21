"""
Enhanced Session Security Manager
Advanced session management with comprehensive security features
"""
import time
import hashlib
import secrets
import hmac
import base64
import json
from typing import Dict, List, Optional, Tuple
from collections import deque
import threading
import ipaddress

class EnhancedSessionManager:
    """Enhanced Session Manager with Advanced Security Features"""
    
    def __init__(self):
        self.active_sessions = {}
        self.session_history = deque(maxlen=10000)
        self.blocked_sessions = set()
        self.suspicious_sessions = set()
        
        # Session configuration
        self.session_timeout = 1800  # 30 minutes
        self.max_sessions_per_ip = 5
        self.max_sessions_per_user = 3
        self.session_cleanup_interval = 300  # 5 minutes
        
        # Security features
        self.enable_ip_validation = True
        self.enable_user_agent_validation = True
        self.enable_session_fingerprinting = True
        self.enable_concurrent_session_control = True
        
        # Session statistics
        self.session_stats = {
            'total_sessions_created': 0,
            'total_sessions_destroyed': 0,
            'active_sessions': 0,
            'blocked_sessions': 0,
            'suspicious_sessions': 0,
            'session_hijacking_attempts': 0,
            'session_fixation_attempts': 0,
            'concurrent_session_violations': 0,
            'ip_validation_failures': 0,
            'user_agent_validation_failures': 0
        }
        
        # Start session cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_expired_sessions, daemon=True)
        self.cleanup_thread.start()
        
        print("🔐 Enhanced Session Manager initialized!")
        print(f"   Session timeout: {self.session_timeout}s")
        print(f"   Max sessions per IP: {self.max_sessions_per_ip}")
        print(f"   Max sessions per user: {self.max_sessions_per_user}")
        print(f"   Security features: 5 active")
    
    def create_session(self, user_id: str, ip_address: str, user_agent: str, additional_data: Dict = None) -> Dict:
        """Create a new secure session"""
        self.session_stats['total_sessions_created'] += 1
        
        # Generate session ID
        session_id = self._generate_session_id(user_id, ip_address)
        
        # Check session limits
        session_limits = self._check_session_limits(user_id, ip_address)
        if not session_limits['allowed']:
            self.session_stats['concurrent_session_violations'] += 1
            return {
                'success': False,
                'session_id': None,
                'reason': session_limits['reason'],
                'recommendations': session_limits['recommendations']
            }
        
        # Create session data
        session_data = {
            'session_id': session_id,
            'user_id': user_id,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'created_at': time.time(),
            'last_activity': time.time(),
            'expires_at': time.time() + self.session_timeout,
            'is_active': True,
            'security_level': 'high',
            'fingerprint': self._generate_session_fingerprint(ip_address, user_agent),
            'additional_data': additional_data or {},
            'access_count': 0,
            'last_access_ip': ip_address,
            'last_access_user_agent': user_agent
        }
        
        # Store session
        self.active_sessions[session_id] = session_data
        
        # Update statistics
        self.session_stats['active_sessions'] = len(self.active_sessions)
        
        # Log session creation
        self.session_history.append({
            'timestamp': time.time(),
            'action': 'SESSION_CREATED',
            'session_id': session_id,
            'user_id': user_id,
            'ip_address': ip_address
        })
        
        return {
            'success': True,
            'session_id': session_id,
            'expires_at': session_data['expires_at'],
            'security_level': session_data['security_level']
        }
    
    def validate_session(self, session_id: str, ip_address: str, user_agent: str) -> Dict:
        """Validate existing session"""
        validation_result = {
            'is_valid': False,
            'is_hijacking_attempt': False,
            'is_fixation_attempt': False,
            'threat_level': 0,
            'reason': None,
            'recommendations': []
        }
        
        # Check if session exists
        if session_id not in self.active_sessions:
            validation_result['reason'] = 'SESSION_NOT_FOUND'
            validation_result['recommendations'].extend([
                'CREATE_NEW_SESSION',
                'LOG_ATTEMPT',
                'ALERT_SECURITY_TEAM'
            ])
            return validation_result
        
        session_data = self.active_sessions[session_id]
        
        # Check if session is active
        if not session_data['is_active']:
            validation_result['reason'] = 'SESSION_INACTIVE'
            validation_result['recommendations'].extend([
                'REACTIVATE_SESSION',
                'CREATE_NEW_SESSION',
                'LOG_ATTEMPT'
            ])
            return validation_result
        
        # Check if session is expired
        if time.time() > session_data['expires_at']:
            validation_result['reason'] = 'SESSION_EXPIRED'
            validation_result['recommendations'].extend([
                'CREATE_NEW_SESSION',
                'EXTEND_SESSION_TIMEOUT',
                'LOG_ATTEMPT'
            ])
            return validation_result
        
        # Check IP validation
        if self.enable_ip_validation:
            ip_validation = self._validate_ip_address(session_data, ip_address)
            if not ip_validation['is_valid']:
                validation_result['is_hijacking_attempt'] = True
                validation_result['threat_level'] = 90
                validation_result['reason'] = 'IP_VALIDATION_FAILED'
                validation_result['recommendations'].extend([
                    'BLOCK_SESSION',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_SESSION_SECURITY',
                    'IMPLEMENT_IP_VALIDATION'
                ])
                self.session_stats['ip_validation_failures'] += 1
                return validation_result
        
        # Check user agent validation
        if self.enable_user_agent_validation:
            ua_validation = self._validate_user_agent(session_data, user_agent)
            if not ua_validation['is_valid']:
                validation_result['is_hijacking_attempt'] = True
                validation_result['threat_level'] = 80
                validation_result['reason'] = 'USER_AGENT_VALIDATION_FAILED'
                validation_result['recommendations'].extend([
                    'BLOCK_SESSION',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_SESSION_SECURITY',
                    'IMPLEMENT_USER_AGENT_VALIDATION'
                ])
                self.session_stats['user_agent_validation_failures'] += 1
                return validation_result
        
        # Check session fingerprinting
        if self.enable_session_fingerprinting:
            fingerprint_validation = self._validate_session_fingerprint(session_data, ip_address, user_agent)
            if not fingerprint_validation['is_valid']:
                validation_result['is_hijacking_attempt'] = True
                validation_result['threat_level'] = 85
                validation_result['reason'] = 'FINGERPRINT_VALIDATION_FAILED'
                validation_result['recommendations'].extend([
                    'BLOCK_SESSION',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_SESSION_SECURITY',
                    'IMPLEMENT_FINGERPRINT_VALIDATION'
                ])
                return validation_result
        
        # Update session activity
        session_data['last_activity'] = time.time()
        session_data['access_count'] += 1
        session_data['last_access_ip'] = ip_address
        session_data['last_access_user_agent'] = user_agent
        
        # Extend session if needed
        if time.time() - session_data['last_activity'] < 300:  # 5 minutes
            session_data['expires_at'] = time.time() + self.session_timeout
        
        # Session is valid
        validation_result['is_valid'] = True
        validation_result['reason'] = 'SESSION_VALID'
        
        return validation_result
    
    def destroy_session(self, session_id: str, reason: str = 'USER_LOGOUT') -> bool:
        """Destroy a session"""
        if session_id in self.active_sessions:
            session_data = self.active_sessions[session_id]
            
            # Log session destruction
            self.session_history.append({
                'timestamp': time.time(),
                'action': 'SESSION_DESTROYED',
                'session_id': session_id,
                'user_id': session_data['user_id'],
                'ip_address': session_data['ip_address'],
                'reason': reason
            })
            
            # Remove session
            del self.active_sessions[session_id]
            
            # Update statistics
            self.session_stats['total_sessions_destroyed'] += 1
            self.session_stats['active_sessions'] = len(self.active_sessions)
            
            return True
        
        return False
    
    def _generate_session_id(self, user_id: str, ip_address: str) -> str:
        """Generate secure session ID"""
        session_data = f"{user_id}_{ip_address}_{time.time()}_{secrets.token_hex(32)}"
        return hashlib.sha256(session_data.encode()).hexdigest()
    
    def _generate_session_fingerprint(self, ip_address: str, user_agent: str) -> str:
        """Generate session fingerprint"""
        fingerprint_data = f"{ip_address}_{user_agent}_{time.time()}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()
    
    def _check_session_limits(self, user_id: str, ip_address: str) -> Dict:
        """Check session limits"""
        # Check IP limit
        ip_sessions = [s for s in self.active_sessions.values() if s['ip_address'] == ip_address]
        if len(ip_sessions) >= self.max_sessions_per_ip:
            return {
                'allowed': False,
                'reason': 'IP_SESSION_LIMIT_EXCEEDED',
                'recommendations': [
                    'BLOCK_NEW_SESSION',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_SESSION_LIMITS',
                    'IMPLEMENT_IP_SESSION_LIMITS'
                ]
            }
        
        # Check user limit
        user_sessions = [s for s in self.active_sessions.values() if s['user_id'] == user_id]
        if len(user_sessions) >= self.max_sessions_per_user:
            return {
                'allowed': False,
                'reason': 'USER_SESSION_LIMIT_EXCEEDED',
                'recommendations': [
                    'BLOCK_NEW_SESSION',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_SESSION_LIMITS',
                    'IMPLEMENT_USER_SESSION_LIMITS'
                ]
            }
        
        return {'allowed': True, 'reason': 'LIMITS_OK'}
    
    def _validate_ip_address(self, session_data: Dict, current_ip: str) -> Dict:
        """Validate IP address"""
        session_ip = session_data['ip_address']
        
        # Check if IPs are the same
        if session_ip == current_ip:
            return {'is_valid': True, 'reason': 'IP_MATCH'}
        
        # Check if IPs are in same subnet (for mobile users)
        try:
            session_ip_obj = ipaddress.ip_address(session_ip)
            current_ip_obj = ipaddress.ip_address(current_ip)
            
            # Allow same network
            if session_ip_obj.version == current_ip_obj.version:
                if session_ip_obj.version == 4:
                    # Check if same /24 subnet
                    session_network = ipaddress.ip_network(f"{session_ip}/24", strict=False)
                    if current_ip_obj in session_network:
                        return {'is_valid': True, 'reason': 'SAME_SUBNET'}
                elif session_ip_obj.version == 6:
                    # Check if same /64 subnet
                    session_network = ipaddress.ip_network(f"{session_ip}/64", strict=False)
                    if current_ip_obj in session_network:
                        return {'is_valid': True, 'reason': 'SAME_SUBNET'}
        except:
            pass
        
        return {'is_valid': False, 'reason': 'IP_MISMATCH'}
    
    def _validate_user_agent(self, session_data: Dict, current_user_agent: str) -> Dict:
        """Validate user agent"""
        session_user_agent = session_data['user_agent']
        
        # Check if user agents are the same
        if session_user_agent == current_user_agent:
            return {'is_valid': True, 'reason': 'USER_AGENT_MATCH'}
        
        # Check if user agents are similar (for browser updates)
        if self._are_user_agents_similar(session_user_agent, current_user_agent):
            return {'is_valid': True, 'reason': 'USER_AGENT_SIMILAR'}
        
        return {'is_valid': False, 'reason': 'USER_AGENT_MISMATCH'}
    
    def _are_user_agents_similar(self, ua1: str, ua2: str) -> bool:
        """Check if user agents are similar"""
        # Extract browser and version from user agents
        ua1_parts = ua1.split()
        ua2_parts = ua2.split()
        
        # Check if same browser
        if len(ua1_parts) > 0 and len(ua2_parts) > 0:
            if ua1_parts[0] == ua2_parts[0]:  # Same browser
                return True
        
        return False
    
    def _validate_session_fingerprint(self, session_data: Dict, ip_address: str, user_agent: str) -> Dict:
        """Validate session fingerprint"""
        current_fingerprint = self._generate_session_fingerprint(ip_address, user_agent)
        session_fingerprint = session_data['fingerprint']
        
        if current_fingerprint == session_fingerprint:
            return {'is_valid': True, 'reason': 'FINGERPRINT_MATCH'}
        
        return {'is_valid': False, 'reason': 'FINGERPRINT_MISMATCH'}
    
    def _cleanup_expired_sessions(self):
        """Cleanup expired sessions"""
        while True:
            try:
                current_time = time.time()
                expired_sessions = []
                
                for session_id, session_data in self.active_sessions.items():
                    if current_time > session_data['expires_at']:
                        expired_sessions.append(session_id)
                
                for session_id in expired_sessions:
                    self.destroy_session(session_id, 'SESSION_EXPIRED')
                
                if expired_sessions:
                    print(f"🧹 Cleaned up {len(expired_sessions)} expired sessions")
                
                time.sleep(self.session_cleanup_interval)
                
            except Exception as e:
                print(f"❌ Session cleanup error: {e}")
                time.sleep(60)
    
    def get_session_statistics(self) -> Dict:
        """Get session statistics"""
        return {
            'total_sessions_created': self.session_stats['total_sessions_created'],
            'total_sessions_destroyed': self.session_stats['total_sessions_destroyed'],
            'active_sessions': self.session_stats['active_sessions'],
            'blocked_sessions': self.session_stats['blocked_sessions'],
            'suspicious_sessions': self.session_stats['suspicious_sessions'],
            'session_hijacking_attempts': self.session_stats['session_hijacking_attempts'],
            'session_fixation_attempts': self.session_stats['session_fixation_attempts'],
            'concurrent_session_violations': self.session_stats['concurrent_session_violations'],
            'ip_validation_failures': self.session_stats['ip_validation_failures'],
            'user_agent_validation_failures': self.session_stats['user_agent_validation_failures'],
            'session_history_size': len(self.session_history)
        }
    
    def get_active_sessions(self) -> Dict:
        """Get all active sessions"""
        return self.active_sessions.copy()
    
    def get_session_by_id(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        return self.active_sessions.get(session_id)
    
    def get_sessions_by_user(self, user_id: str) -> List[Dict]:
        """Get sessions by user ID"""
        return [s for s in self.active_sessions.values() if s['user_id'] == user_id]
    
    def get_sessions_by_ip(self, ip_address: str) -> List[Dict]:
        """Get sessions by IP address"""
        return [s for s in self.active_sessions.values() if s['ip_address'] == ip_address]
    
    def block_session(self, session_id: str, reason: str = 'SECURITY_VIOLATION'):
        """Block a session"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['is_active'] = False
            self.blocked_sessions.add(session_id)
            self.session_stats['blocked_sessions'] += 1
            print(f"🚫 Session blocked: {session_id} - {reason}")
    
    def unblock_session(self, session_id: str):
        """Unblock a session"""
        if session_id in self.blocked_sessions:
            self.blocked_sessions.remove(session_id)
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['is_active'] = True
            print(f"✅ Session unblocked: {session_id}")
    
    def mark_session_suspicious(self, session_id: str, reason: str = 'SUSPICIOUS_ACTIVITY'):
        """Mark a session as suspicious"""
        if session_id in self.active_sessions:
            self.suspicious_sessions.add(session_id)
            self.session_stats['suspicious_sessions'] += 1
            print(f"⚠️ Session marked suspicious: {session_id} - {reason}")
    
    def extend_session(self, session_id: str, extension_time: int = 1800):
        """Extend session expiry time"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['expires_at'] = time.time() + extension_time
            print(f"⏰ Session extended: {session_id} (+{extension_time}s)")
    
    def regenerate_session_id(self, old_session_id: str) -> Optional[str]:
        """Regenerate session ID"""
        if old_session_id in self.active_sessions:
            session_data = self.active_sessions[old_session_id]
            new_session_id = self._generate_session_id(session_data['user_id'], session_data['ip_address'])
            
            # Update session data
            session_data['session_id'] = new_session_id
            self.active_sessions[new_session_id] = session_data
            del self.active_sessions[old_session_id]
            
            print(f"🔄 Session ID regenerated: {old_session_id} -> {new_session_id}")
            return new_session_id
        
        return None
