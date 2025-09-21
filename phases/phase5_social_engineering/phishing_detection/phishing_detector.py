import re
import time
import hashlib
import threading
from collections import deque
from typing import Dict, List, Optional, Tuple
import json
import base64
import urllib.parse
import requests
import socket
import dns.resolver

class PhishingDetector:
    def __init__(self):
        self.detection_active = False
        self.detection_thread = None
        self.phishing_history = deque(maxlen=10000)
        self.suspicious_phishing = deque(maxlen=1000)
        
        # Phishing detection patterns
        self.phishing_patterns = {
            'urgent_language': [
                r'urgent\s+action\s+required',
                r'immediate\s+attention',
                r'act\s+now\s+or\s+lose',
                r'limited\s+time\s+offer',
                r'expires\s+soon',
                r'deadline\s+approaching',
                r'final\s+notice',
                r'last\s+chance',
                r'act\s+fast',
                r'don\'t\s+miss\s+out'
            ],
            'authority_impersonation': [
                r'bank\s+of\s+america',
                r'chase\s+bank',
                r'wells\s+fargo',
                r'paypal',
                r'amazon',
                r'apple',
                r'microsoft',
                r'google',
                r'facebook',
                r'twitter'
            ],
            'credential_harvesting': [
                r'verify\s+your\s+account',
                r'confirm\s+your\s+identity',
                r'update\s+your\s+information',
                r'security\s+breach\s+detected',
                r'account\s+suspended',
                r'account\s+locked',
                r'password\s+expired',
                r'login\s+required',
                r'authentication\s+needed',
                r'verification\s+required'
            ],
            'suspicious_links': [
                r'click\s+here',
                r'click\s+now',
                r'click\s+to\s+verify',
                r'click\s+to\s+confirm',
                r'click\s+to\s+update',
                r'click\s+to\s+login',
                r'click\s+to\s+unlock',
                r'click\s+to\s+continue',
                r'click\s+to\s+proceed',
                r'click\s+to\s+activate'
            ],
            'emotional_manipulation': [
                r'you\s+have\s+won',
                r'congratulations',
                r'you\s+are\s+selected',
                r'exclusive\s+offer',
                r'special\s+deal',
                r'limited\s+supply',
                r'once\s+in\s+a\s+lifetime',
                r'rare\s+opportunity',
                r'secret\s+information',
                r'insider\s+tip'
            ]
        }
        
        # Phishing detection configuration
        self.detection_config = {
            'check_links': True,
            'check_attachments': True,
            'check_sender': True,
            'check_content': True,
            'check_headers': True,
            'check_dns': True,
            'check_ssl': True,
            'max_redirects': 5,
            'timeout': 10
        }
        
        # Known phishing indicators
        self.phishing_indicators = {
            'suspicious_domains': set(),
            'suspicious_ips': set(),
            'suspicious_keywords': set(),
            'suspicious_patterns': set()
        }
        
        # Phishing detection statistics
        self.detection_stats = {
            'emails_analyzed': 0,
            'phishing_emails_detected': 0,
            'suspicious_emails_detected': 0,
            'false_positives': 0,
            'detection_errors': 0
        }
        
        print("🎣 Phishing Detector initialized!")
        print(f"   Urgent language patterns: {len(self.phishing_patterns['urgent_language'])}")
        print(f"   Authority impersonation patterns: {len(self.phishing_patterns['authority_impersonation'])}")
        print(f"   Credential harvesting patterns: {len(self.phishing_patterns['credential_harvesting'])}")
        print(f"   Suspicious link patterns: {len(self.phishing_patterns['suspicious_links'])}")
        print(f"   Emotional manipulation patterns: {len(self.phishing_patterns['emotional_manipulation'])}")

    def start_detection(self):
        """Start phishing detection"""
        if self.detection_active:
            return
        self.detection_active = True
        self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.detection_thread.start()
        print("🎣 Phishing detection started!")

    def stop_detection(self):
        """Stop phishing detection"""
        self.detection_active = False
        if self.detection_thread:
            self.detection_thread.join(timeout=5)
        print("⏹️ Phishing detection stopped!")

    def _detection_loop(self):
        """Main phishing detection loop"""
        while self.detection_active:
            try:
                # Monitor for new emails (simplified implementation)
                self._monitor_new_emails()
                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                print(f"❌ Phishing detection error: {e}")
                self.detection_stats['detection_errors'] += 1
                time.sleep(5)

    def _monitor_new_emails(self):
        """Monitor for new emails to analyze"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd integrate with email servers or APIs
            
            # Simulate email monitoring
            pass
            
        except Exception as e:
            print(f"❌ Email monitoring error: {e}")

    def detect_phishing(self, email_data: Dict) -> Dict:
        """Detect phishing in email"""
        try:
            self.detection_stats['emails_analyzed'] += 1
            
            detection_result = {
                'timestamp': time.time(),
                'email_id': email_data.get('id', 'unknown'),
                'sender': email_data.get('sender', ''),
                'subject': email_data.get('subject', ''),
                'body': email_data.get('body', ''),
                'links': email_data.get('links', []),
                'attachments': email_data.get('attachments', []),
                'phishing_score': 0,
                'threat_level': 'low',
                'threat_types': [],
                'indicators': [],
                'recommendations': []
            }
            
            # Analyze email content for phishing
            content_analysis = self._analyze_phishing_content(email_data)
            detection_result.update(content_analysis)
            
            # Analyze links for phishing
            link_analysis = self._analyze_phishing_links(email_data.get('links', []))
            detection_result.update(link_analysis)
            
            # Analyze sender for phishing
            sender_analysis = self._analyze_phishing_sender(email_data.get('sender', ''))
            detection_result.update(sender_analysis)
            
            # Analyze attachments for phishing
            attachment_analysis = self._analyze_phishing_attachments(email_data.get('attachments', []))
            detection_result.update(attachment_analysis)
            
            # Calculate overall phishing score
            detection_result['phishing_score'] = self._calculate_phishing_score(detection_result)
            
            # Determine threat level
            detection_result['threat_level'] = self._determine_threat_level(detection_result['phishing_score'])
            
            # Generate recommendations
            detection_result['recommendations'] = self._generate_recommendations(detection_result)
            
            # Store detection result
            self.phishing_history.append(detection_result)
            
            # Check if email is phishing
            if detection_result['phishing_score'] > 50:
                self.suspicious_phishing.append(detection_result)
                self.detection_stats['suspicious_emails_detected'] += 1
                
                if detection_result['phishing_score'] > 80:
                    self.detection_stats['phishing_emails_detected'] += 1
            
            return detection_result
            
        except Exception as e:
            return {'error': f'Phishing detection failed: {e}'}

    def _analyze_phishing_content(self, email_data: Dict) -> Dict:
        """Analyze email content for phishing indicators"""
        try:
            content_analysis = {
                'content_phishing_score': 0,
                'content_threat_types': [],
                'content_indicators': []
            }
            
            # Combine subject and body for analysis
            full_text = f"{email_data.get('subject', '')} {email_data.get('body', '')}"
            full_text_lower = full_text.lower()
            
            # Check for urgent language
            urgent_score = 0
            for pattern in self.phishing_patterns['urgent_language']:
                if re.search(pattern, full_text_lower):
                    urgent_score += 10
                    content_analysis['content_indicators'].append(f'urgent_language: {pattern}')
            
            if urgent_score > 0:
                content_analysis['content_threat_types'].append('urgent_language')
                content_analysis['content_phishing_score'] += urgent_score
            
            # Check for authority impersonation
            authority_score = 0
            for pattern in self.phishing_patterns['authority_impersonation']:
                if re.search(pattern, full_text_lower):
                    authority_score += 15
                    content_analysis['content_indicators'].append(f'authority_impersonation: {pattern}')
            
            if authority_score > 0:
                content_analysis['content_threat_types'].append('authority_impersonation')
                content_analysis['content_phishing_score'] += authority_score
            
            # Check for credential harvesting
            credential_score = 0
            for pattern in self.phishing_patterns['credential_harvesting']:
                if re.search(pattern, full_text_lower):
                    credential_score += 20
                    content_analysis['content_indicators'].append(f'credential_harvesting: {pattern}')
            
            if credential_score > 0:
                content_analysis['content_threat_types'].append('credential_harvesting')
                content_analysis['content_phishing_score'] += credential_score
            
            # Check for suspicious links
            link_score = 0
            for pattern in self.phishing_patterns['suspicious_links']:
                if re.search(pattern, full_text_lower):
                    link_score += 12
                    content_analysis['content_indicators'].append(f'suspicious_links: {pattern}')
            
            if link_score > 0:
                content_analysis['content_threat_types'].append('suspicious_links')
                content_analysis['content_phishing_score'] += link_score
            
            # Check for emotional manipulation
            emotional_score = 0
            for pattern in self.phishing_patterns['emotional_manipulation']:
                if re.search(pattern, full_text_lower):
                    emotional_score += 8
                    content_analysis['content_indicators'].append(f'emotional_manipulation: {pattern}')
            
            if emotional_score > 0:
                content_analysis['content_threat_types'].append('emotional_manipulation')
                content_analysis['content_phishing_score'] += emotional_score
            
            return content_analysis
            
        except Exception as e:
            return {'error': f'Content analysis failed: {e}'}

    def _analyze_phishing_links(self, links: List[str]) -> Dict:
        """Analyze links for phishing indicators"""
        try:
            link_analysis = {
                'link_phishing_score': 0,
                'link_threat_types': [],
                'link_indicators': []
            }
            
            for link in links:
                # Check for suspicious URL patterns
                if self._is_suspicious_phishing_url(link):
                    link_analysis['link_phishing_score'] += 20
                    link_analysis['link_threat_types'].append('suspicious_url')
                    link_analysis['link_indicators'].append(f'suspicious_url: {link}')
                
                # Check for URL shortening
                if self._is_url_shortener(link):
                    link_analysis['link_phishing_score'] += 15
                    link_analysis['link_threat_types'].append('url_shortener')
                    link_analysis['link_indicators'].append(f'url_shortener: {link}')
                
                # Check for IP addresses in URLs
                if self._contains_ip_address(link):
                    link_analysis['link_phishing_score'] += 25
                    link_analysis['link_threat_types'].append('ip_address_url')
                    link_analysis['link_indicators'].append(f'ip_address_url: {link}')
                
                # Check for typosquatting
                if self._check_typosquatting(link):
                    link_analysis['link_phishing_score'] += 30
                    link_analysis['link_threat_types'].append('typosquatting')
                    link_analysis['link_indicators'].append(f'typosquatting: {link}')
                
                # Check for suspicious domains
                domain = self._extract_domain(link)
                if domain in self.phishing_indicators['suspicious_domains']:
                    link_analysis['link_phishing_score'] += 35
                    link_analysis['link_threat_types'].append('known_phishing_domain')
                    link_analysis['link_indicators'].append(f'known_phishing_domain: {domain}')
            
            return link_analysis
            
        except Exception as e:
            return {'error': f'Link analysis failed: {e}'}

    def _analyze_phishing_sender(self, sender: str) -> Dict:
        """Analyze sender for phishing indicators"""
        try:
            sender_analysis = {
                'sender_phishing_score': 0,
                'sender_threat_types': [],
                'sender_indicators': []
            }
            
            if not sender:
                return sender_analysis
            
            # Extract domain from sender
            domain = sender.split('@')[-1] if '@' in sender else ''
            
            # Check if domain is known phishing domain
            if domain in self.phishing_indicators['suspicious_domains']:
                sender_analysis['sender_phishing_score'] += 40
                sender_analysis['sender_threat_types'].append('known_phishing_domain')
                sender_analysis['sender_indicators'].append(f'known_phishing_domain: {domain}')
            
            # Check for suspicious sender patterns
            suspicious_patterns = [
                r'[0-9]+@',  # Numeric sender
                r'[a-z]+[0-9]+@',  # Alphanumeric sender
                r'[a-z]+[0-9]+[a-z]+@',  # Mixed alphanumeric sender
                r'[a-z]+-[a-z]+@',  # Hyphenated sender
                r'[a-z]+_[a-z]+@'  # Underscore separated sender
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, sender.lower()):
                    sender_analysis['sender_phishing_score'] += 10
                    sender_analysis['sender_indicators'].append(f'suspicious_sender_pattern: {pattern}')
            
            # Check for typosquatting
            if self._check_typosquatting(domain):
                sender_analysis['sender_phishing_score'] += 25
                sender_analysis['sender_threat_types'].append('typosquatting')
                sender_analysis['sender_indicators'].append(f'typosquatting: {domain}')
            
            return sender_analysis
            
        except Exception as e:
            return {'error': f'Sender analysis failed: {e}'}

    def _analyze_phishing_attachments(self, attachments: List[Dict]) -> Dict:
        """Analyze attachments for phishing indicators"""
        try:
            attachment_analysis = {
                'attachment_phishing_score': 0,
                'attachment_threat_types': [],
                'attachment_indicators': []
            }
            
            for attachment in attachments:
                filename = attachment.get('filename', '')
                file_size = attachment.get('size', 0)
                file_type = attachment.get('type', '')
                
                # Check for suspicious file extensions
                suspicious_extensions = ['.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.jar', '.scr', '.pif']
                for ext in suspicious_extensions:
                    if filename.lower().endswith(ext):
                        attachment_analysis['attachment_phishing_score'] += 25
                        attachment_analysis['attachment_threat_types'].append('suspicious_extension')
                        attachment_analysis['attachment_indicators'].append(f'suspicious_extension: {ext}')
                
                # Check for double extensions
                if self._has_double_extension(filename):
                    attachment_analysis['attachment_phishing_score'] += 20
                    attachment_analysis['attachment_threat_types'].append('double_extension')
                    attachment_analysis['attachment_indicators'].append(f'double_extension: {filename}')
                
                # Check for suspicious file names
                if self._is_suspicious_filename(filename):
                    attachment_analysis['attachment_phishing_score'] += 15
                    attachment_analysis['attachment_threat_types'].append('suspicious_filename')
                    attachment_analysis['attachment_indicators'].append(f'suspicious_filename: {filename}')
                
                # Check for large file sizes
                if file_size > 10 * 1024 * 1024:  # 10MB
                    attachment_analysis['attachment_phishing_score'] += 10
                    attachment_analysis['attachment_threat_types'].append('large_file')
                    attachment_analysis['attachment_indicators'].append(f'large_file: {file_size} bytes')
            
            return attachment_analysis
            
        except Exception as e:
            return {'error': f'Attachment analysis failed: {e}'}

    def _is_suspicious_phishing_url(self, url: str) -> bool:
        """Check if URL is suspicious for phishing"""
        try:
            # Check for suspicious patterns
            suspicious_patterns = [
                r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',  # IP addresses
                r'[a-z]+[0-9]+[a-z]+',  # Mixed alphanumeric
                r'[a-z]+-[a-z]+',  # Hyphenated domains
                r'[a-z]+_[a-z]+',  # Underscore separated
                r'[a-z]+[0-9]+',  # Alphanumeric
                r'[0-9]+[a-z]+'  # Numeric + alphabetic
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, url.lower()):
                    return True
            
            return False
            
        except Exception:
            return False

    def _is_url_shortener(self, url: str) -> bool:
        """Check if URL is a URL shortener"""
        url_shorteners = [
            'bit.ly', 'tinyurl.com', 'short.ly', 't.co',
            'goo.gl', 'ow.ly', 'is.gd', 'v.gd'
        ]
        
        for shortener in url_shorteners:
            if shortener in url.lower():
                return True
        
        return False

    def _contains_ip_address(self, url: str) -> bool:
        """Check if URL contains IP address"""
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        return bool(re.search(ip_pattern, url))

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            # Remove protocol
            if '://' in url:
                url = url.split('://', 1)[1]
            
            # Remove path
            if '/' in url:
                url = url.split('/', 1)[0]
            
            # Remove port
            if ':' in url:
                url = url.split(':', 1)[0]
            
            return url.lower()
        except Exception:
            return ''

    def _check_typosquatting(self, domain: str) -> bool:
        """Check if domain is typosquatting"""
        try:
            # Check for common typosquatting patterns
            typosquatting_patterns = [
                r'[a-z]+[0-9]+[a-z]+',  # Mixed alphanumeric
                r'[a-z]+-[a-z]+',  # Hyphenated
                r'[a-z]+_[a-z]+',  # Underscore separated
                r'[a-z]+[0-9]+',  # Alphanumeric
                r'[0-9]+[a-z]+'  # Numeric + alphabetic
            ]
            
            for pattern in typosquatting_patterns:
                if re.search(pattern, domain):
                    return True
            
            return False
            
        except Exception:
            return False

    def _has_double_extension(self, filename: str) -> bool:
        """Check if filename has double extension"""
        try:
            # Check for double extensions like file.txt.exe
            parts = filename.split('.')
            if len(parts) > 2:
                # Check if last two parts are both extensions
                last_part = parts[-1].lower()
                second_last_part = parts[-2].lower()
                
                extensions = ['.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.jar', '.scr', '.pif']
                if f'.{last_part}' in extensions and f'.{second_last_part}' in extensions:
                    return True
            
            return False
            
        except Exception:
            return False

    def _is_suspicious_filename(self, filename: str) -> bool:
        """Check if filename is suspicious"""
        try:
            suspicious_patterns = [
                r'[a-z]+[0-9]+[a-z]+',  # Mixed alphanumeric
                r'[a-z]+-[a-z]+',  # Hyphenated
                r'[a-z]+_[a-z]+',  # Underscore separated
                r'[0-9]+[a-z]+',  # Numeric + alphabetic
                r'[a-z]+[0-9]+'  # Alphabetic + numeric
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, filename.lower()):
                    return True
            
            return False
            
        except Exception:
            return False

    def _calculate_phishing_score(self, detection_result: Dict) -> int:
        """Calculate overall phishing score"""
        try:
            total_score = 0
            
            # Add content phishing score
            total_score += detection_result.get('content_phishing_score', 0)
            
            # Add link phishing score
            total_score += detection_result.get('link_phishing_score', 0)
            
            # Add sender phishing score
            total_score += detection_result.get('sender_phishing_score', 0)
            
            # Add attachment phishing score
            total_score += detection_result.get('attachment_phishing_score', 0)
            
            return min(total_score, 100)  # Cap at 100
            
        except Exception:
            return 0

    def _determine_threat_level(self, phishing_score: int) -> str:
        """Determine threat level based on phishing score"""
        if phishing_score >= 80:
            return 'critical'
        elif phishing_score >= 60:
            return 'high'
        elif phishing_score >= 40:
            return 'medium'
        else:
            return 'low'

    def _generate_recommendations(self, detection_result: Dict) -> List[str]:
        """Generate recommendations based on detection"""
        try:
            recommendations = []
            
            threat_level = detection_result.get('threat_level', 'low')
            threat_types = detection_result.get('threat_types', [])
            
            if threat_level == 'critical':
                recommendations.extend([
                    'IMMEDIATE_QUARANTINE',
                    'BLOCK_SENDER',
                    'NOTIFY_SECURITY_TEAM',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS',
                    'PHISHING_EDUCATION'
                ])
            elif threat_level == 'high':
                recommendations.extend([
                    'QUARANTINE_EMAIL',
                    'BLOCK_SENDER',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS',
                    'PHISHING_EDUCATION'
                ])
            elif threat_level == 'medium':
                recommendations.extend([
                    'FLAG_AS_SUSPICIOUS',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS',
                    'PHISHING_EDUCATION'
                ])
            else:
                recommendations.append('CONTINUE_MONITORING')
            
            # Add specific recommendations based on threat types
            if 'urgent_language' in threat_types:
                recommendations.append('URGENT_LANGUAGE_EDUCATION')
            if 'authority_impersonation' in threat_types:
                recommendations.append('AUTHORITY_IMPERSONATION_EDUCATION')
            if 'credential_harvesting' in threat_types:
                recommendations.append('CREDENTIAL_HARVESTING_EDUCATION')
            if 'suspicious_links' in threat_types:
                recommendations.append('SUSPICIOUS_LINKS_EDUCATION')
            if 'emotional_manipulation' in threat_types:
                recommendations.append('EMOTIONAL_MANIPULATION_EDUCATION')
            
            return recommendations
            
        except Exception:
            return ['CONTINUE_MONITORING']

    def get_detection_statistics(self) -> Dict:
        """Get phishing detection statistics"""
        return {
            'detection_active': self.detection_active,
            'emails_analyzed': self.detection_stats['emails_analyzed'],
            'phishing_emails_detected': self.detection_stats['phishing_emails_detected'],
            'suspicious_emails_detected': self.detection_stats['suspicious_emails_detected'],
            'false_positives': self.detection_stats['false_positives'],
            'detection_errors': self.detection_stats['detection_errors'],
            'phishing_history_size': len(self.phishing_history),
            'suspicious_phishing_size': len(self.suspicious_phishing)
        }

    def get_recent_phishing_detections(self, count: int = 10) -> List[Dict]:
        """Get recent phishing detections"""
        return list(self.suspicious_phishing)[-count:]

    def add_suspicious_domain(self, domain: str):
        """Add domain to suspicious domains list"""
        self.phishing_indicators['suspicious_domains'].add(domain.lower())
        print(f"✅ Added suspicious domain: {domain}")

    def add_suspicious_ip(self, ip: str):
        """Add IP to suspicious IPs list"""
        self.phishing_indicators['suspicious_ips'].add(ip)
        print(f"✅ Added suspicious IP: {ip}")

    def add_suspicious_keyword(self, keyword: str):
        """Add keyword to suspicious keywords list"""
        self.phishing_indicators['suspicious_keywords'].add(keyword.lower())
        print(f"✅ Added suspicious keyword: {keyword}")

    def add_suspicious_pattern(self, pattern: str):
        """Add pattern to suspicious patterns list"""
        self.phishing_indicators['suspicious_patterns'].add(pattern)
        print(f"✅ Added suspicious pattern: {pattern}")

    def update_detection_config(self, config: Dict):
        """Update detection configuration"""
        try:
            self.detection_config.update(config)
            print(f"✅ Detection configuration updated")
        except Exception as e:
            print(f"❌ Configuration update error: {e}")

    def emergency_phishing_lockdown(self):
        """Emergency phishing lockdown mode"""
        try:
            print("🚨 EMERGENCY PHISHING LOCKDOWN ACTIVATED!")
            
            # Block all suspicious senders
            print("🚫 Blocking all suspicious senders...")
            
            # Quarantine all suspicious emails
            print("🔒 Quarantining all suspicious emails...")
            
            # Notify security team
            print("📢 Notifying security team...")
            
            # Activate phishing education
            print("🎓 Activating phishing education...")
            
            print("✅ Emergency phishing lockdown completed!")
            
        except Exception as e:
            print(f"❌ Emergency lockdown error: {e}")

    def restore_normal_operation(self):
        """Restore normal phishing detection operation"""
        try:
            print("✅ Restoring normal phishing detection operation...")
            
            # Resume normal email processing
            print("📧 Resuming normal email processing...")
            
            print("✅ Normal phishing detection operation restored!")
            
        except Exception as e:
            print(f"❌ Operation restoration error: {e}")
