"""
Advanced XSS Protection Engine
Comprehensive Cross-Site Scripting protection with AI-powered detection
"""
import re
import html
import urllib.parse
import base64
import hashlib
import json
from typing import Dict, List, Optional, Tuple
from collections import deque
import time

class AdvancedXSSProtector:
    """Advanced XSS Protection with Comprehensive Detection and Prevention"""
    
    def __init__(self):
        self.xss_patterns = {
            'script_tags': [
                r'<script[^>]*>.*?</script>',
                r'<script[^>]*>',
                r'</script>',
                r'<script[^>]*src\s*=\s*["\'][^"\']*["\']',
                r'<script[^>]*type\s*=\s*["\'][^"\']*["\']'
            ],
            'javascript_protocols': [
                r'javascript\s*:',
                r'vbscript\s*:',
                r'data\s*:',
                r'vbscript\s*:',
                r'jscript\s*:',
                r'liveScript\s*:',
                r'mocha\s*:',
                r'ecmascript\s*:'
            ],
            'event_handlers': [
                r'on\w+\s*=\s*["\'][^"\']*["\']',
                r'onload\s*=',
                r'onerror\s*=',
                r'onclick\s*=',
                r'onmouseover\s*=',
                r'onfocus\s*=',
                r'onblur\s*=',
                r'onchange\s*=',
                r'onsubmit\s*=',
                r'onreset\s*=',
                r'onselect\s*=',
                r'onkeydown\s*=',
                r'onkeyup\s*=',
                r'onkeypress\s*=',
                r'onmousedown\s*=',
                r'onmouseup\s*=',
                r'onmouseout\s*=',
                r'onmousemove\s*=',
                r'onmouseenter\s*=',
                r'onmouseleave\s*=',
                r'ondblclick\s*=',
                r'oncontextmenu\s*=',
                r'ondrag\s*=',
                r'ondragstart\s*=',
                r'ondragend\s*=',
                r'ondrop\s*=',
                r'ondragover\s*=',
                r'ondragenter\s*=',
                r'ondragleave\s*=',
                r'onscroll\s*=',
                r'onresize\s*=',
                r'onunload\s*=',
                r'onbeforeunload\s*=',
                r'onhashchange\s*=',
                r'onpopstate\s*=',
                r'onstorage\s*=',
                r'onmessage\s*=',
                r'onerror\s*=',
                r'onabort\s*=',
                r'oncanplay\s*=',
                r'oncanplaythrough\s*=',
                r'ondurationchange\s*=',
                r'onemptied\s*=',
                r'onended\s*=',
                r'onloadeddata\s*=',
                r'onloadedmetadata\s*=',
                r'onloadstart\s*=',
                r'onpause\s*=',
                r'onplay\s*=',
                r'onplaying\s*=',
                r'onprogress\s*=',
                r'onratechange\s*=',
                r'onseeked\s*=',
                r'onseeking\s*=',
                r'onstalled\s*=',
                r'onsuspend\s*=',
                r'ontimeupdate\s*=',
                r'onvolumechange\s*=',
                r'onwaiting\s*='
            ],
            'iframe_objects': [
                r'<iframe[^>]*>',
                r'<object[^>]*>',
                r'<embed[^>]*>',
                r'<applet[^>]*>',
                r'<form[^>]*>',
                r'<input[^>]*>',
                r'<textarea[^>]*>',
                r'<select[^>]*>',
                r'<option[^>]*>',
                r'<button[^>]*>',
                r'<link[^>]*>',
                r'<meta[^>]*>',
                r'<style[^>]*>',
                r'<link[^>]*rel\s*=\s*["\']stylesheet["\']',
                r'<style[^>]*>.*?</style>'
            ],
            'css_expressions': [
                r'expression\s*\(',
                r'url\s*\(',
                r'@import',
                r'@charset',
                r'@media',
                r'@page',
                r'@font-face',
                r'@keyframes',
                r'@supports',
                r'@document',
                r'@namespace',
                r'@viewport',
                r'@counter-style',
                r'@font-feature-values',
                r'@property',
                r'@layer',
                r'@container',
                r'@scope'
            ],
            'html_entities': [
                r'&[^;]+;',
                r'&#\d+;',
                r'&#x[0-9a-fA-F]+;',
                r'&lt;',
                r'&gt;',
                r'&amp;',
                r'&quot;',
                r'&apos;',
                r'&nbsp;',
                r'&copy;',
                r'&reg;',
                r'&trade;',
                r'&hellip;',
                r'&mdash;',
                r'&ndash;',
                r'&lsquo;',
                r'&rsquo;',
                r'&ldquo;',
                r'&rdquo;',
                r'&bull;',
                r'&middot;',
                r'&sect;',
                r'&para;',
                r'&dagger;',
                r'&Dagger;',
                r'&permil;',
                r'&lsaquo;',
                r'&rsaquo;',
                r'&euro;',
                r'&pound;',
                r'&yen;',
                r'&cent;',
                r'&curren;',
                r'&fnof;',
                r'&alpha;',
                r'&beta;',
                r'&gamma;',
                r'&delta;',
                r'&epsilon;',
                r'&zeta;',
                r'&eta;',
                r'&theta;',
                r'&iota;',
                r'&kappa;',
                r'&lambda;',
                r'&mu;',
                r'&nu;',
                r'&xi;',
                r'&omicron;',
                r'&pi;',
                r'&rho;',
                r'&sigma;',
                r'&tau;',
                r'&upsilon;',
                r'&phi;',
                r'&chi;',
                r'&psi;',
                r'&omega;',
                r'&Alpha;',
                r'&Beta;',
                r'&Gamma;',
                r'&Delta;',
                r'&Epsilon;',
                r'&Zeta;',
                r'&Eta;',
                r'&Theta;',
                r'&Iota;',
                r'&Kappa;',
                r'&Lambda;',
                r'&Mu;',
                r'&Nu;',
                r'&Xi;',
                r'&Omicron;',
                r'&Pi;',
                r'&Rho;',
                r'&Sigma;',
                r'&Tau;',
                r'&Upsilon;',
                r'&Phi;',
                r'&Chi;',
                r'&Psi;',
                r'&Omega;'
            ],
            'data_uris': [
                r'data:text/html',
                r'data:text/plain',
                r'data:text/css',
                r'data:text/javascript',
                r'data:application/javascript',
                r'data:application/x-javascript',
                r'data:application/ecmascript',
                r'data:application/x-ecmascript',
                r'data:text/ecmascript',
                r'data:text/x-ecmascript',
                r'data:text/x-javascript'
            ],
            'base64_encoded': [
                r'data:text/html;base64,',
                r'data:text/plain;base64,',
                r'data:text/css;base64,',
                r'data:text/javascript;base64,',
                r'data:application/javascript;base64,',
                r'data:application/x-javascript;base64,',
                r'data:application/ecmascript;base64,',
                r'data:application/x-ecmascript;base64,',
                r'data:text/ecmascript;base64,',
                r'data:text/x-ecmascript;base64,',
                r'data:text/x-javascript;base64,'
            ]
        }
        
        self.xss_stats = {
            'total_requests': 0,
            'xss_attempts_detected': 0,
            'xss_attempts_blocked': 0,
            'script_tag_attempts': 0,
            'javascript_protocol_attempts': 0,
            'event_handler_attempts': 0,
            'iframe_object_attempts': 0,
            'css_expression_attempts': 0,
            'html_entity_attempts': 0,
            'data_uri_attempts': 0,
            'base64_encoded_attempts': 0
        }
        
        self.blocked_ips = set()
        self.suspicious_ips = set()
        self.xss_history = deque(maxlen=10000)
        
        print("🛡️ Advanced XSS Protector initialized!")
        print(f"   XSS patterns: {sum(len(patterns) for patterns in self.xss_patterns.values())}")
        print(f"   Protection levels: 7")
        print(f"   History capacity: {self.xss_history.maxlen}")
    
    def analyze_xss_threat(self, request_data: Dict) -> Dict:
        """Analyze request for XSS threats"""
        self.xss_stats['total_requests'] += 1
        
        analysis = {
            'is_xss_threat': False,
            'threat_level': 0,
            'threat_types': [],
            'blocked': False,
            'reason': None,
            'recommendations': [],
            'sanitized_content': None
        }
        
        # Extract request components
        url = request_data.get('url', '')
        method = request_data.get('method', 'GET')
        headers = request_data.get('headers', {})
        body = request_data.get('body', '')
        ip_address = request_data.get('ip_address', '')
        
        # Combine all input sources
        input_content = f"{url} {body} {json.dumps(headers)}"
        
        # Check for XSS patterns
        xss_detection = self._detect_xss_patterns(input_content)
        if xss_detection['threats_detected']:
            analysis['is_xss_threat'] = True
            analysis['threat_level'] = xss_detection['threat_level']
            analysis['threat_types'] = xss_detection['threat_types']
            analysis['recommendations'] = xss_detection['recommendations']
            
            # Update statistics
            self.xss_stats['xss_attempts_detected'] += 1
            for threat_type in xss_detection['threat_types']:
                if threat_type in self.xss_stats:
                    self.xss_stats[threat_type] += 1
            
            # Block request if high threat level
            if xss_detection['threat_level'] > 70:
                analysis['blocked'] = True
                analysis['reason'] = 'XSS_THREAT_DETECTED'
                self.xss_stats['xss_attempts_blocked'] += 1
                
                # Add IP to suspicious list
                self.suspicious_ips.add(ip_address)
                
                # Block IP if multiple XSS attempts
                if len([r for r in self.xss_history if r.get('ip_address') == ip_address and r.get('xss_detected')]) > 3:
                    self.blocked_ips.add(ip_address)
                    analysis['reason'] += '_IP_BLOCKED'
            
            # Sanitize content
            analysis['sanitized_content'] = self._sanitize_xss_content(input_content)
        
        # Store in history
        self.xss_history.append({
            'timestamp': time.time(),
            'ip_address': ip_address,
            'url': url,
            'method': method,
            'xss_detected': analysis['is_xss_threat'],
            'threat_types': analysis['threat_types'],
            'threat_level': analysis['threat_level']
        })
        
        return analysis
    
    def _detect_xss_patterns(self, content: str) -> Dict:
        """Detect XSS patterns in content"""
        threats_detected = []
        threat_types = []
        threat_level = 0
        recommendations = []
        
        # Check script tags
        for pattern in self.xss_patterns['script_tags']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"Script tag detected: {pattern}")
                threat_types.append('script_tag_attempts')
                threat_level = max(threat_level, 90)
                recommendations.extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'IMPLEMENT_OUTPUT_ENCODING',
                    'USE_CSP_HEADERS'
                ])
        
        # Check JavaScript protocols
        for pattern in self.xss_patterns['javascript_protocols']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"JavaScript protocol detected: {pattern}")
                threat_types.append('javascript_protocol_attempts')
                threat_level = max(threat_level, 85)
                recommendations.extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'VALIDATE_URLS',
                    'IMPLEMENT_URL_FILTERING'
                ])
        
        # Check event handlers
        for pattern in self.xss_patterns['event_handlers']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"Event handler detected: {pattern}")
                threat_types.append('event_handler_attempts')
                threat_level = max(threat_level, 80)
                recommendations.extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REMOVE_EVENT_HANDLERS',
                    'IMPLEMENT_ATTRIBUTE_FILTERING'
                ])
        
        # Check iframe/object tags
        for pattern in self.xss_patterns['iframe_objects']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"Object tag detected: {pattern}")
                threat_types.append('iframe_object_attempts')
                threat_level = max(threat_level, 75)
                recommendations.extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REMOVE_OBJECT_TAGS',
                    'IMPLEMENT_TAG_FILTERING'
                ])
        
        # Check CSS expressions
        for pattern in self.xss_patterns['css_expressions']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"CSS expression detected: {pattern}")
                threat_types.append('css_expression_attempts')
                threat_level = max(threat_level, 70)
                recommendations.extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REMOVE_CSS_EXPRESSIONS',
                    'IMPLEMENT_CSS_FILTERING'
                ])
        
        # Check HTML entities
        for pattern in self.xss_patterns['html_entities']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"HTML entity detected: {pattern}")
                threat_types.append('html_entity_attempts')
                threat_level = max(threat_level, 60)
                recommendations.extend([
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'DECODE_HTML_ENTITIES',
                    'IMPLEMENT_ENTITY_FILTERING'
                ])
        
        # Check data URIs
        for pattern in self.xss_patterns['data_uris']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"Data URI detected: {pattern}")
                threat_types.append('data_uri_attempts')
                threat_level = max(threat_level, 85)
                recommendations.extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'VALIDATE_DATA_URIS',
                    'IMPLEMENT_URI_FILTERING'
                ])
        
        # Check base64 encoded content
        for pattern in self.xss_patterns['base64_encoded']:
            if re.search(pattern, content, re.IGNORECASE):
                threats_detected.append(f"Base64 encoded content detected: {pattern}")
                threat_types.append('base64_encoded_attempts')
                threat_level = max(threat_level, 90)
                recommendations.extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'DECODE_BASE64_CONTENT',
                    'IMPLEMENT_BASE64_FILTERING'
                ])
        
        return {
            'threats_detected': len(threats_detected) > 0,
            'threat_level': threat_level,
            'threat_types': threat_types,
            'recommendations': recommendations
        }
    
    def _sanitize_xss_content(self, content: str) -> str:
        """Sanitize content to remove XSS threats"""
        sanitized = content
        
        # HTML encoding
        sanitized = html.escape(sanitized, quote=True)
        
        # Remove script tags
        for pattern in self.xss_patterns['script_tags']:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove JavaScript protocols
        for pattern in self.xss_patterns['javascript_protocols']:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove event handlers
        for pattern in self.xss_patterns['event_handlers']:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove iframe/object tags
        for pattern in self.xss_patterns['iframe_objects']:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove CSS expressions
        for pattern in self.xss_patterns['css_expressions']:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove data URIs
        for pattern in self.xss_patterns['data_uris']:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove base64 encoded content
        for pattern in self.xss_patterns['base64_encoded']:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Remove control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    def generate_csp_header(self, policy_type: str = 'strict') -> str:
        """Generate Content Security Policy header"""
        if policy_type == 'strict':
            return "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; media-src 'self'; object-src 'none'; child-src 'none'; frame-ancestors 'none'; form-action 'self'; base-uri 'self';"
        elif policy_type == 'moderate':
            return "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https:; media-src 'self' https:; object-src 'none'; child-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self';"
        elif policy_type == 'permissive':
            return "default-src 'self' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https:; media-src 'self' https:; object-src 'self' https:; child-src 'self' https:; frame-ancestors 'self' https:; form-action 'self' https:; base-uri 'self' https:;"
        else:
            return "default-src 'self';"
    
    def get_xss_statistics(self) -> Dict:
        """Get XSS protection statistics"""
        return {
            'total_requests': self.xss_stats['total_requests'],
            'xss_attempts_detected': self.xss_stats['xss_attempts_detected'],
            'xss_attempts_blocked': self.xss_stats['xss_attempts_blocked'],
            'detection_rate': (self.xss_stats['xss_attempts_detected'] / max(self.xss_stats['total_requests'], 1)) * 100,
            'block_rate': (self.xss_stats['xss_attempts_blocked'] / max(self.xss_stats['xss_attempts_detected'], 1)) * 100,
            'attack_types': {
                'script_tag_attempts': self.xss_stats['script_tag_attempts'],
                'javascript_protocol_attempts': self.xss_stats['javascript_protocol_attempts'],
                'event_handler_attempts': self.xss_stats['event_handler_attempts'],
                'iframe_object_attempts': self.xss_stats['iframe_object_attempts'],
                'css_expression_attempts': self.xss_stats['css_expression_attempts'],
                'html_entity_attempts': self.xss_stats['html_entity_attempts'],
                'data_uri_attempts': self.xss_stats['data_uri_attempts'],
                'base64_encoded_attempts': self.xss_stats['base64_encoded_attempts']
            },
            'blocked_ips': len(self.blocked_ips),
            'suspicious_ips': len(self.suspicious_ips),
            'xss_history_size': len(self.xss_history)
        }
    
    def unblock_ip(self, ip_address: str):
        """Unblock an IP address"""
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            print(f"✅ IP {ip_address} unblocked from XSS protection")
    
    def block_ip(self, ip_address: str):
        """Block an IP address"""
        self.blocked_ips.add(ip_address)
        print(f"🚫 IP {ip_address} blocked for XSS protection")
