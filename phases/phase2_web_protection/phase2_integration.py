"""
Phase 2 - Web Protection Integration
WAF, Input Validation, XSS Protection, CSRF Protection, Session Security
"""
import time
import threading
import sys
import os
from typing import Dict, List, Optional

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Phase 2 modules
from waf_engine.advanced_waf import AdvancedWAF
from input_validation.enhanced_validator import EnhancedInputValidator
from xss_protection.advanced_xss_protector import AdvancedXSSProtector
from csrf_protection.advanced_csrf_protector import AdvancedCSRFProtector
from session_security.enhanced_session_manager import EnhancedSessionManager

class Phase2WebProtection:
    """Phase 2 - Web Protection Integration"""
    
    def __init__(self):
        print("🚀 PHASE 2 - WEB PROTECTION INITIALIZATION")
        print("=" * 60)
        
        # Initialize web protection components
        self.waf_engine = AdvancedWAF()
        self.input_validator = EnhancedInputValidator()
        self.xss_protector = AdvancedXSSProtector()
        self.csrf_protector = AdvancedCSRFProtector()
        self.session_manager = EnhancedSessionManager()
        
        # Integration status
        self.is_active = False
        self.integration_thread = None
        
        # Statistics
        self.total_requests_processed = 0
        self.total_threats_detected = 0
        self.total_requests_blocked = 0
        self.total_sessions_created = 0
        self.total_tokens_generated = 0
        
        print("✅ Phase 2 Web Protection initialized!")
        print("   - Advanced WAF Engine")
        print("   - Enhanced Input Validation")
        print("   - Advanced XSS Protection")
        print("   - Advanced CSRF Protection")
        print("   - Enhanced Session Security")
    
    def start_phase2_protection(self):
        """Start Phase 2 comprehensive web protection"""
        if self.is_active:
            return
        
        self.is_active = True
        
        # Start integration monitoring
        self.integration_thread = threading.Thread(target=self._integration_monitoring_loop, daemon=True)
        self.integration_thread.start()
        
        print("🔒 Phase 2 Web Protection Active!")
        print("   - WAF Engine: ACTIVE")
        print("   - Input Validation: ACTIVE")
        print("   - XSS Protection: ACTIVE")
        print("   - CSRF Protection: ACTIVE")
        print("   - Session Security: ACTIVE")
    
    def stop_phase2_protection(self):
        """Stop Phase 2 comprehensive web protection"""
        self.is_active = False
        if self.integration_thread:
            self.integration_thread.join(timeout=5)
        
        print("⏹️ Phase 2 Web Protection Stopped!")
    
    def process_web_request(self, request_data: Dict) -> Dict:
        """Process web request through all protection layers"""
        self.total_requests_processed += 1
        
        # Initialize response
        response = {
            'request_id': request_data.get('request_id', f"req_{int(time.time())}"),
            'processed': True,
            'blocked': False,
            'threats_detected': [],
            'recommendations': [],
            'session_id': None,
            'csrf_token': None,
            'sanitized_content': None,
            'protection_layers': {
                'waf': {'active': True, 'threats': []},
                'input_validation': {'active': True, 'threats': []},
                'xss_protection': {'active': True, 'threats': []},
                'csrf_protection': {'active': True, 'threats': []},
                'session_security': {'active': True, 'threats': []}
            }
        }
        
        # Layer 1: WAF Analysis
        waf_analysis = self.waf_engine.analyze_request(request_data)
        if waf_analysis['blocked']:
            response['blocked'] = True
            response['threats_detected'].append(f"WAF: {waf_analysis['reason']}")
            response['protection_layers']['waf']['threats'].append(waf_analysis['reason'])
            return response
        
        if waf_analysis['is_threat']:
            response['threats_detected'].append(f"WAF: {waf_analysis['threat_type']}")
            response['protection_layers']['waf']['threats'].append(waf_analysis['threat_type'])
            response['recommendations'].extend(waf_analysis['recommended_actions'])
        
        # Layer 2: Input Validation
        input_data = request_data.get('body', '')
        if input_data:
            input_validation = self.input_validator.validate_input(input_data, 'text')
            if not input_validation['is_valid']:
                response['blocked'] = True
                response['threats_detected'].append("Input Validation: Invalid input")
                response['protection_layers']['input_validation']['threats'].append("Invalid input")
                return response
            
            if input_validation['threat_detected']:
                response['threats_detected'].append("Input Validation: Dangerous patterns detected")
                response['protection_layers']['input_validation']['threats'].append("Dangerous patterns")
                response['recommendations'].extend(input_validation['recommendations'])
            
            if input_validation['sanitization_applied']:
                response['sanitized_content'] = input_validation['sanitized_value']
        
        # Layer 3: XSS Protection
        xss_analysis = self.xss_protector.analyze_xss_threat(request_data)
        if xss_analysis['blocked']:
            response['blocked'] = True
            response['threats_detected'].append(f"XSS: {xss_analysis['reason']}")
            response['protection_layers']['xss_protection']['threats'].append(xss_analysis['reason'])
            return response
        
        if xss_analysis['is_xss_threat']:
            response['threats_detected'].append(f"XSS: {', '.join(xss_analysis['threat_types'])}")
            response['protection_layers']['xss_protection']['threats'].extend(xss_analysis['threat_types'])
            response['recommendations'].extend(xss_analysis['recommendations'])
        
        if xss_analysis['sanitized_content']:
            response['sanitized_content'] = xss_analysis['sanitized_content']
        
        # Layer 4: CSRF Protection
        session_id = request_data.get('session_id')
        csrf_token = request_data.get('csrf_token')
        
        if session_id and csrf_token:
            csrf_validation = self.csrf_protector.validate_csrf_token(csrf_token, session_id, request_data)
            if not csrf_validation['is_valid']:
                response['blocked'] = True
                response['threats_detected'].append(f"CSRF: {csrf_validation['reason']}")
                response['protection_layers']['csrf_protection']['threats'].append(csrf_validation['reason'])
                return response
            
            if csrf_validation['is_csrf_attempt']:
                response['threats_detected'].append(f"CSRF: {csrf_validation['reason']}")
                response['protection_layers']['csrf_protection']['threats'].append(csrf_validation['reason'])
                response['recommendations'].extend(csrf_validation['recommendations'])
        
        # Layer 5: Session Security
        if session_id:
            session_validation = self.session_manager.validate_session(
                session_id,
                request_data.get('ip_address', ''),
                request_data.get('headers', {}).get('User-Agent', '')
            )
            if not session_validation['is_valid']:
                response['blocked'] = True
                response['threats_detected'].append(f"Session: {session_validation['reason']}")
                response['protection_layers']['session_security']['threats'].append(session_validation['reason'])
                return response
            
            if session_validation['is_hijacking_attempt'] or session_validation['is_fixation_attempt']:
                response['threats_detected'].append(f"Session: {session_validation['reason']}")
                response['protection_layers']['session_security']['threats'].append(session_validation['reason'])
                response['recommendations'].extend(session_validation['recommendations'])
        
        # Update statistics
        if response['threats_detected']:
            self.total_threats_detected += 1
        
        if response['blocked']:
            self.total_requests_blocked += 1
        
        return response
    
    def create_secure_session(self, user_id: str, ip_address: str, user_agent: str) -> Dict:
        """Create a secure session with CSRF token"""
        # Create session
        session_result = self.session_manager.create_session(user_id, ip_address, user_agent)
        
        if session_result['success']:
            session_id = session_result['session_id']
            
            # Generate CSRF token
            csrf_token = self.csrf_protector.generate_csrf_token(session_id, user_id)
            
            self.total_sessions_created += 1
            self.total_tokens_generated += 1
            
            return {
                'success': True,
                'session_id': session_id,
                'csrf_token': csrf_token,
                'expires_at': session_result['expires_at'],
                'security_level': session_result['security_level']
            }
        else:
            return {
                'success': False,
                'reason': session_result['reason'],
                'recommendations': session_result['recommendations']
            }
    
    def _integration_monitoring_loop(self):
        """Integration monitoring loop"""
        while self.is_active:
            try:
                # Collect statistics from all components
                self._collect_integration_statistics()
                
                # Perform integration analysis
                self._perform_integration_analysis()
                
                # Wait for next monitoring cycle
                time.sleep(10)  # 10-second intervals
                
            except Exception as e:
                print(f"❌ Integration monitoring error: {e}")
                time.sleep(10)
    
    def _collect_integration_statistics(self):
        """Collect statistics from all components"""
        # Get WAF statistics
        waf_stats = self.waf_engine.get_waf_statistics()
        
        # Get input validation statistics
        input_stats = self.input_validator.get_validation_statistics()
        
        # Get XSS protection statistics
        xss_stats = self.xss_protector.get_xss_statistics()
        
        # Get CSRF protection statistics
        csrf_stats = self.csrf_protector.get_csrf_statistics()
        
        # Get session security statistics
        session_stats = self.session_manager.get_session_statistics()
    
    def _perform_integration_analysis(self):
        """Perform integration analysis"""
        # Analyze overall web protection health
        protection_health = self._assess_protection_health()
        
        # Analyze threat patterns
        threat_patterns = self._analyze_threat_patterns()
        
        # Generate integration report
        if time.time() % 60 < 10:  # Every minute
            self._generate_integration_report(protection_health, threat_patterns)
    
    def _assess_protection_health(self) -> Dict:
        """Assess overall web protection health"""
        health_score = 100
        
        # Check component status
        if not self.is_active:
            health_score -= 50
        
        # Check threat levels
        if self.total_threats_detected > 10:
            health_score -= 30
        if self.total_requests_blocked > 5:
            health_score -= 20
        
        return {
            'health_score': max(0, health_score),
            'status': 'Excellent' if health_score > 80 else 'Good' if health_score > 60 else 'Fair' if health_score > 40 else 'Poor',
            'threats_detected': self.total_threats_detected,
            'requests_blocked': self.total_requests_blocked,
            'sessions_created': self.total_sessions_created,
            'tokens_generated': self.total_tokens_generated
        }
    
    def _analyze_threat_patterns(self) -> Dict:
        """Analyze threat patterns"""
        return {
            'total_requests': self.total_requests_processed,
            'threat_detection_rate': (self.total_threats_detected / max(self.total_requests_processed, 1)) * 100,
            'block_rate': (self.total_requests_blocked / max(self.total_requests_processed, 1)) * 100,
            'session_creation_rate': (self.total_sessions_created / max(self.total_requests_processed, 1)) * 100,
            'token_generation_rate': (self.total_tokens_generated / max(self.total_requests_processed, 1)) * 100
        }
    
    def _generate_integration_report(self, protection_health: Dict, threat_patterns: Dict):
        """Generate integration report"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n📊 PHASE 2 INTEGRATION REPORT [{timestamp}]")
        print("=" * 60)
        print(f"🔒 Protection Health: {protection_health['health_score']}/100 ({protection_health['status']})")
        print(f"📈 Threat Detection Rate: {threat_patterns['threat_detection_rate']:.1f}%")
        print(f"🚫 Block Rate: {threat_patterns['block_rate']:.1f}%")
        print(f"🔐 Sessions Created: {self.total_sessions_created}")
        print(f"🎫 Tokens Generated: {self.total_tokens_generated}")
        print("=" * 60)
    
    def get_phase2_statistics(self) -> Dict:
        """Get Phase 2 comprehensive statistics"""
        return {
            'phase': 'Phase 2 - Web Protection',
            'status': 'Active' if self.is_active else 'Inactive',
            'components': {
                'waf_engine': self.waf_engine.get_waf_statistics(),
                'input_validator': self.input_validator.get_validation_statistics(),
                'xss_protector': self.xss_protector.get_xss_statistics(),
                'csrf_protector': self.csrf_protector.get_csrf_statistics(),
                'session_manager': self.session_manager.get_session_statistics()
            },
            'integration_metrics': {
                'total_requests_processed': self.total_requests_processed,
                'total_threats_detected': self.total_threats_detected,
                'total_requests_blocked': self.total_requests_blocked,
                'total_sessions_created': self.total_sessions_created,
                'total_tokens_generated': self.total_tokens_generated
            }
        }
    
    def test_phase2_components(self):
        """Test Phase 2 components"""
        print("\n🧪 TESTING PHASE 2 COMPONENTS")
        print("=" * 60)
        
        # Test WAF Engine
        print("🛡️ Testing WAF Engine...")
        test_request = {
            'url': 'http://example.com/search?q=test',
            'method': 'GET',
            'headers': {'User-Agent': 'Mozilla/5.0'},
            'body': '',
            'ip_address': '192.168.1.100'
        }
        waf_analysis = self.waf_engine.analyze_request(test_request)
        print(f"   ✅ WAF Analysis: {'Blocked' if waf_analysis['blocked'] else 'Allowed'}")
        
        # Test Input Validation
        print("🔍 Testing Input Validation...")
        input_validation = self.input_validator.validate_input("test@example.com", "email")
        print(f"   ✅ Input Validation: {'Valid' if input_validation['is_valid'] else 'Invalid'}")
        
        # Test XSS Protection
        print("🛡️ Testing XSS Protection...")
        xss_analysis = self.xss_protector.analyze_xss_threat(test_request)
        print(f"   ✅ XSS Analysis: {'Threat' if xss_analysis['is_xss_threat'] else 'Safe'}")
        
        # Test CSRF Protection
        print("🔐 Testing CSRF Protection...")
        session_id = "test_session_123"
        csrf_token = self.csrf_protector.generate_csrf_token(session_id, "test_user")
        csrf_validation = self.csrf_protector.validate_csrf_token(csrf_token, session_id, test_request)
        print(f"   ✅ CSRF Validation: {'Valid' if csrf_validation['is_valid'] else 'Invalid'}")
        
        # Test Session Security
        print("🔐 Testing Session Security...")
        session_result = self.session_manager.create_session("test_user", "192.168.1.100", "Mozilla/5.0")
        print(f"   ✅ Session Creation: {'Success' if session_result['success'] else 'Failed'}")
        
        print("✅ Phase 2 Component Testing Completed!")
        print("=" * 60)

def main():
    """Main function for Phase 2 testing"""
    print("🚀 PHASE 2 - WEB PROTECTION TESTING")
    print("=" * 60)
    
    # Initialize Phase 2
    phase2 = Phase2WebProtection()
    
    # Test components
    phase2.test_phase2_components()
    
    # Start protection
    phase2.start_phase2_protection()
    
    # Test web request processing
    print("\n🌐 Testing Web Request Processing...")
    test_request = {
        'request_id': 'test_req_001',
        'url': 'http://example.com/api/data',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json',
            'Origin': 'http://example.com'
        },
        'body': '{"username": "test", "password": "test123"}',
        'ip_address': '192.168.1.100',
        'session_id': 'test_session_123',
        'csrf_token': 'test_csrf_token_123'
    }
    
    # Process request
    response = phase2.process_web_request(test_request)
    print(f"   ✅ Request Processed: {'Blocked' if response['blocked'] else 'Allowed'}")
    print(f"   ✅ Threats Detected: {len(response['threats_detected'])}")
    print(f"   ✅ Recommendations: {len(response['recommendations'])}")
    
    # Test session creation
    print("\n🔐 Testing Session Creation...")
    session_result = phase2.create_secure_session("test_user", "192.168.1.100", "Mozilla/5.0")
    print(f"   ✅ Session Created: {'Success' if session_result['success'] else 'Failed'}")
    if session_result['success']:
        print(f"   ✅ Session ID: {session_result['session_id']}")
        print(f"   ✅ CSRF Token: {session_result['csrf_token'][:32]}...")
    
    # Get statistics
    stats = phase2.get_phase2_statistics()
    print(f"\n📊 PHASE 2 STATISTICS:")
    print(f"   Requests Processed: {stats['integration_metrics']['total_requests_processed']}")
    print(f"   Threats Detected: {stats['integration_metrics']['total_threats_detected']}")
    print(f"   Requests Blocked: {stats['integration_metrics']['total_requests_blocked']}")
    print(f"   Sessions Created: {stats['integration_metrics']['total_sessions_created']}")
    print(f"   Tokens Generated: {stats['integration_metrics']['total_tokens_generated']}")
    
    # Stop protection
    phase2.stop_phase2_protection()
    
    print("\n✅ Phase 2 Web Protection Testing Completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
