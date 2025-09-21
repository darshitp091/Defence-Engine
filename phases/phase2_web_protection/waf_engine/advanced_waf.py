"""
Advanced Web Application Firewall (WAF)
Comprehensive web application protection with AI-powered threat detection
"""
import re
import time
import hashlib
import json
from typing import Dict, List, Optional, Tuple
from collections import deque
import threading
import ipaddress
import urllib.parse

class AdvancedWAF:
    """Advanced Web Application Firewall with AI-powered protection"""
    
    def __init__(self):
        self.attack_patterns = {
            'sql_injection': [
                r"('|(\\')|(;)|(--)|(/\*)|(\*/)|(\bunion\b)|(\bselect\b)|(\binsert\b)|(\bupdate\b)|(\bdelete\b)|(\bdrop\b)|(\bcreate\b)|(\balter\b))",
                r"(\bOR\b|\bAND\b)\s+\d+\s*=\s*\d+",
                r"(\bUNION\b|\bSELECT\b).*(\bFROM\b|\bWHERE\b)",
                r"(\bINSERT\b|\bUPDATE\b|\bDELETE\b).*(\bINTO\b|\bSET\b|\bFROM\b)",
                r"(\bDROP\b|\bCREATE\b|\bALTER\b).*(\bTABLE\b|\bDATABASE\b|\bINDEX\b)"
            ],
            'xss_attacks': [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe[^>]*>",
                r"<object[^>]*>",
                r"<embed[^>]*>",
                r"<link[^>]*>",
                r"<meta[^>]*>",
                r"<style[^>]*>.*?</style>",
                r"expression\s*\(",
                r"url\s*\(",
                r"@import"
            ],
            'path_traversal': [
                r"\.\./",
                r"\.\.\\",
                r"%2e%2e%2f",
                r"%2e%2e%5c",
                r"\.\.%2f",
                r"\.\.%5c",
                r"\.\.%252f",
                r"\.\.%255c"
            ],
            'command_injection': [
                r"[;&\|`$]",
                r"(\bcat\b|\bls\b|\bdir\b|\btype\b|\bmore\b|\bless\b|\bhead\b|\btail\b)",
                r"(\bwhoami\b|\bid\b|\buname\b|\bhostname\b)",
                r"(\bping\b|\bnslookup\b|\bdig\b|\btraceroute\b)",
                r"(\bwget\b|\bcurl\b|\bfetch\b|\bdownload\b)",
                r"(\brm\b|\bdel\b|\bremove\b|\bdelete\b)",
                r"(\bmkdir\b|\bmd\b|\bcreate\b|\bnew\b)",
                r"(\bchmod\b|\bchown\b|\battrib\b|\bpermissions\b)"
            ],
            'ldap_injection': [
                r"[\(\)=\*!&\|]",
                r"(\bcn\b|\bdc\b|\bou\b|\bobjectClass\b)",
                r"(\buserPassword\b|\bmail\b|\btelephoneNumber\b)",
                r"(\bdistinguishedName\b|\bcn\b|\bsn\b|\bgivenName\b)"
            ],
            'xml_injection': [
                r"<!DOCTYPE",
                r"<!ENTITY",
                r"<!\[CDATA\[",
                r"<\?xml",
                r"&\w+;"
            ]
        }
        
        self.rate_limits = {}
        self.blocked_ips = set()
        self.suspicious_ips = set()
        self.request_history = deque(maxlen=10000)
        
        # WAF Statistics
        self.stats = {
            'total_requests': 0,
            'blocked_requests': 0,
            'sql_injection_attempts': 0,
            'xss_attempts': 0,
            'path_traversal_attempts': 0,
            'command_injection_attempts': 0,
            'ldap_injection_attempts': 0,
            'xml_injection_attempts': 0,
            'rate_limit_blocks': 0
        }
        
        print("🛡️ Advanced WAF Engine initialized!")
        print(f"   Attack patterns: {sum(len(patterns) for patterns in self.attack_patterns.values())}")
        print(f"   Rate limiting: Active")
        print(f"   IP blocking: Active")
    
    def analyze_request(self, request_data: Dict) -> Dict:
        """Analyze HTTP request for threats"""
        self.stats['total_requests'] += 1
        
        analysis = {
            'is_threat': False,
            'threat_type': None,
            'threat_level': 0,
            'blocked': False,
            'reason': None,
            'recommendations': []
        }
        
        # Extract request components
        url = request_data.get('url', '')
        method = request_data.get('method', 'GET')
        headers = request_data.get('headers', {})
        body = request_data.get('body', '')
        ip_address = request_data.get('ip_address', '')
        user_agent = headers.get('User-Agent', '')
        
        # Check if IP is blocked
        if ip_address in self.blocked_ips:
            analysis['blocked'] = True
            analysis['reason'] = 'IP_BLOCKED'
            self.stats['blocked_requests'] += 1
            return analysis
        
        # Rate limiting check
        if self._check_rate_limit(ip_address):
            analysis['blocked'] = True
            analysis['reason'] = 'RATE_LIMIT_EXCEEDED'
            self.stats['rate_limit_blocks'] += 1
            return analysis
        
        # SQL Injection detection
        sql_threat = self._detect_sql_injection(url, body, headers)
        if sql_threat['is_threat']:
            analysis['is_threat'] = True
            analysis['threat_type'] = 'SQL_INJECTION'
            analysis['threat_level'] = max(analysis['threat_level'], sql_threat['threat_level'])
            analysis['recommendations'].extend(sql_threat['recommendations'])
            self.stats['sql_injection_attempts'] += 1
        
        # XSS detection
        xss_threat = self._detect_xss_attack(url, body, headers)
        if xss_threat['is_threat']:
            analysis['is_threat'] = True
            analysis['threat_type'] = 'XSS_ATTACK'
            analysis['threat_level'] = max(analysis['threat_level'], xss_threat['threat_level'])
            analysis['recommendations'].extend(xss_threat['recommendations'])
            self.stats['xss_attempts'] += 1
        
        # Path Traversal detection
        path_threat = self._detect_path_traversal(url, body, headers)
        if path_threat['is_threat']:
            analysis['is_threat'] = True
            analysis['threat_type'] = 'PATH_TRAVERSAL'
            analysis['threat_level'] = max(analysis['threat_level'], path_threat['threat_level'])
            analysis['recommendations'].extend(path_threat['recommendations'])
            self.stats['path_traversal_attempts'] += 1
        
        # Command Injection detection
        cmd_threat = self._detect_command_injection(url, body, headers)
        if cmd_threat['is_threat']:
            analysis['is_threat'] = True
            analysis['threat_type'] = 'COMMAND_INJECTION'
            analysis['threat_level'] = max(analysis['threat_level'], cmd_threat['threat_level'])
            analysis['recommendations'].extend(cmd_threat['recommendations'])
            self.stats['command_injection_attempts'] += 1
        
        # LDAP Injection detection
        ldap_threat = self._detect_ldap_injection(url, body, headers)
        if ldap_threat['is_threat']:
            analysis['is_threat'] = True
            analysis['threat_type'] = 'LDAP_INJECTION'
            analysis['threat_level'] = max(analysis['threat_level'], ldap_threat['threat_level'])
            analysis['recommendations'].extend(ldap_threat['recommendations'])
            self.stats['ldap_injection_attempts'] += 1
        
        # XML Injection detection
        xml_threat = self._detect_xml_injection(url, body, headers)
        if xml_threat['is_threat']:
            analysis['is_threat'] = True
            analysis['threat_type'] = 'XML_INJECTION'
            analysis['threat_level'] = max(analysis['threat_level'], xml_threat['threat_level'])
            analysis['recommendations'].extend(xml_threat['recommendations'])
            self.stats['xml_injection_attempts'] += 1
        
        # Block request if threat detected
        if analysis['is_threat'] and analysis['threat_level'] > 70:
            analysis['blocked'] = True
            analysis['reason'] = f'THREAT_DETECTED_{analysis["threat_type"]}'
            self.stats['blocked_requests'] += 1
            
            # Add IP to suspicious list
            self.suspicious_ips.add(ip_address)
            
            # Block IP if multiple threats
            if len([r for r in self.request_history if r.get('ip_address') == ip_address and r.get('threat_detected')]) > 5:
                self.blocked_ips.add(ip_address)
                analysis['reason'] += '_IP_BLOCKED'
        
        # Store request in history
        self.request_history.append({
            'timestamp': time.time(),
            'ip_address': ip_address,
            'url': url,
            'method': method,
            'threat_detected': analysis['is_threat'],
            'threat_type': analysis['threat_type'],
            'threat_level': analysis['threat_level']
        })
        
        return analysis
    
    def _detect_sql_injection(self, url: str, body: str, headers: Dict) -> Dict:
        """Detect SQL injection attempts"""
        threat_data = {
            'is_threat': False,
            'threat_level': 0,
            'recommendations': []
        }
        
        # Combine all input sources
        input_data = f"{url} {body} {json.dumps(headers)}"
        
        for pattern in self.attack_patterns['sql_injection']:
            if re.search(pattern, input_data, re.IGNORECASE):
                threat_data['is_threat'] = True
                threat_data['threat_level'] = 90
                threat_data['recommendations'].extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_SQL_QUERIES',
                    'IMPLEMENT_PARAMETERIZED_QUERIES'
                ])
                break
        
        return threat_data
    
    def _detect_xss_attack(self, url: str, body: str, headers: Dict) -> Dict:
        """Detect XSS attack attempts"""
        threat_data = {
            'is_threat': False,
            'threat_level': 0,
            'recommendations': []
        }
        
        # Combine all input sources
        input_data = f"{url} {body} {json.dumps(headers)}"
        
        for pattern in self.attack_patterns['xss_attacks']:
            if re.search(pattern, input_data, re.IGNORECASE):
                threat_data['is_threat'] = True
                threat_data['threat_level'] = 85
                threat_data['recommendations'].extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'IMPLEMENT_OUTPUT_ENCODING',
                    'USE_CSP_HEADERS'
                ])
                break
        
        return threat_data
    
    def _detect_path_traversal(self, url: str, body: str, headers: Dict) -> Dict:
        """Detect path traversal attempts"""
        threat_data = {
            'is_threat': False,
            'threat_level': 0,
            'recommendations': []
        }
        
        # Combine all input sources
        input_data = f"{url} {body} {json.dumps(headers)}"
        
        for pattern in self.attack_patterns['path_traversal']:
            if re.search(pattern, input_data, re.IGNORECASE):
                threat_data['is_threat'] = True
                threat_data['threat_level'] = 80
                threat_data['recommendations'].extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'VALIDATE_FILE_PATHS',
                    'IMPLEMENT_PATH_SANITIZATION'
                ])
                break
        
        return threat_data
    
    def _detect_command_injection(self, url: str, body: str, headers: Dict) -> Dict:
        """Detect command injection attempts"""
        threat_data = {
            'is_threat': False,
            'threat_level': 0,
            'recommendations': []
        }
        
        # Combine all input sources
        input_data = f"{url} {body} {json.dumps(headers)}"
        
        for pattern in self.attack_patterns['command_injection']:
            if re.search(pattern, input_data, re.IGNORECASE):
                threat_data['is_threat'] = True
                threat_data['threat_level'] = 95
                threat_data['recommendations'].extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_COMMAND_EXECUTION',
                    'IMPLEMENT_INPUT_VALIDATION'
                ])
                break
        
        return threat_data
    
    def _detect_ldap_injection(self, url: str, body: str, headers: Dict) -> Dict:
        """Detect LDAP injection attempts"""
        threat_data = {
            'is_threat': False,
            'threat_level': 0,
            'recommendations': []
        }
        
        # Combine all input sources
        input_data = f"{url} {body} {json.dumps(headers)}"
        
        for pattern in self.attack_patterns['ldap_injection']:
            if re.search(pattern, input_data, re.IGNORECASE):
                threat_data['is_threat'] = True
                threat_data['threat_level'] = 75
                threat_data['recommendations'].extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_LDAP_QUERIES',
                    'IMPLEMENT_LDAP_SANITIZATION'
                ])
                break
        
        return threat_data
    
    def _detect_xml_injection(self, url: str, body: str, headers: Dict) -> Dict:
        """Detect XML injection attempts"""
        threat_data = {
            'is_threat': False,
            'threat_level': 0,
            'recommendations': []
        }
        
        # Combine all input sources
        input_data = f"{url} {body} {json.dumps(headers)}"
        
        for pattern in self.attack_patterns['xml_injection']:
            if re.search(pattern, input_data, re.IGNORECASE):
                threat_data['is_threat'] = True
                threat_data['threat_level'] = 85
                threat_data['recommendations'].extend([
                    'BLOCK_REQUEST',
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'REVIEW_XML_PROCESSING',
                    'IMPLEMENT_XML_VALIDATION'
                ])
                break
        
        return threat_data
    
    def _check_rate_limit(self, ip_address: str) -> bool:
        """Check if IP has exceeded rate limit"""
        current_time = time.time()
        window_start = current_time - 60  # 1 minute window
        
        # Clean old entries
        if ip_address in self.rate_limits:
            self.rate_limits[ip_address] = [
                req_time for req_time in self.rate_limits[ip_address]
                if req_time > window_start
            ]
        else:
            self.rate_limits[ip_address] = []
        
        # Check rate limit (100 requests per minute)
        if len(self.rate_limits[ip_address]) >= 100:
            return True
        
        # Add current request
        self.rate_limits[ip_address].append(current_time)
        return False
    
    def get_waf_statistics(self) -> Dict:
        """Get WAF statistics"""
        return {
            'total_requests': self.stats['total_requests'],
            'blocked_requests': self.stats['blocked_requests'],
            'block_rate': (self.stats['blocked_requests'] / max(self.stats['total_requests'], 1)) * 100,
            'attack_attempts': {
                'sql_injection': self.stats['sql_injection_attempts'],
                'xss_attacks': self.stats['xss_attempts'],
                'path_traversal': self.stats['path_traversal_attempts'],
                'command_injection': self.stats['command_injection_attempts'],
                'ldap_injection': self.stats['ldap_injection_attempts'],
                'xml_injection': self.stats['xml_injection_attempts']
            },
            'rate_limit_blocks': self.stats['rate_limit_blocks'],
            'blocked_ips': len(self.blocked_ips),
            'suspicious_ips': len(self.suspicious_ips),
            'request_history_size': len(self.request_history)
        }
    
    def unblock_ip(self, ip_address: str):
        """Unblock an IP address"""
        if ip_address in self.blocked_ips:
            self.blocked_ips.remove(ip_address)
            print(f"✅ IP {ip_address} unblocked")
    
    def block_ip(self, ip_address: str):
        """Block an IP address"""
        self.blocked_ips.add(ip_address)
        print(f"🚫 IP {ip_address} blocked")
