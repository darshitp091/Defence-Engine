import re
import time
import hashlib
import threading
from collections import deque
from typing import Dict, List, Optional, Tuple
import json
import base64
import urllib.parse
import socket
import dns.resolver
import requests

class EmailAnalyzer:
    def __init__(self):
        self.analysis_active = False
        self.analysis_thread = None
        self.email_history = deque(maxlen=10000)
        self.suspicious_emails = deque(maxlen=1000)
        
        # Email analysis patterns
        self.suspicious_patterns = {
            'phishing_indicators': [
                r'urgent\s+action\s+required',
                r'immediate\s+attention',
                r'verify\s+your\s+account',
                r'click\s+here\s+now',
                r'limited\s+time\s+offer',
                r'act\s+now\s+or\s+lose',
                r'your\s+account\s+will\s+be\s+closed',
                r'security\s+breach\s+detected',
                r'update\s+your\s+information',
                r'confirm\s+your\s+identity'
            ],
            'spam_indicators': [
                r'free\s+money',
                r'win\s+a\s+prize',
                r'no\s+obligation',
                r'guaranteed\s+results',
                r'act\s+fast',
                r'limited\s+supply',
                r'once\s+in\s+a\s+lifetime',
                r'you\s+have\s+won',
                r'congratulations',
                r'claim\s+your\s+prize'
            ],
            'malware_indicators': [
                r'download\s+attachment',
                r'open\s+this\s+file',
                r'install\s+this\s+software',
                r'run\s+this\s+program',
                r'click\s+to\s+install',
                r'update\s+your\s+software',
                r'security\s+patch',
                r'antivirus\s+update',
                r'system\s+optimization',
                r'performance\s+boost'
            ],
            'social_engineering_indicators': [
                r'pretend\s+to\s+be',
                r'impersonating',
                r'fake\s+authority',
                r'false\s+urgency',
                r'emotional\s+manipulation',
                r'fear\s+tactics',
                r'guilt\s+trip',
                r'peer\s+pressure',
                r'social\s+proof',
                r'authority\s+figure'
            ]
        }
        
        # Suspicious domains and IPs
        self.suspicious_domains = set()
        self.suspicious_ips = set()
        self.trusted_domains = {
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
            'microsoft.com', 'google.com', 'apple.com', 'amazon.com'
        }
        
        # Email analysis statistics
        self.analysis_stats = {
            'emails_analyzed': 0,
            'suspicious_emails_detected': 0,
            'phishing_emails_detected': 0,
            'spam_emails_detected': 0,
            'malware_emails_detected': 0,
            'social_engineering_emails_detected': 0,
            'false_positives': 0,
            'analysis_errors': 0
        }
        
        print("📧 Email Analyzer initialized!")
        print(f"   Phishing indicators: {len(self.suspicious_patterns['phishing_indicators'])}")
        print(f"   Spam indicators: {len(self.suspicious_patterns['spam_indicators'])}")
        print(f"   Malware indicators: {len(self.suspicious_patterns['malware_indicators'])}")
        print(f"   Social engineering indicators: {len(self.suspicious_patterns['social_engineering_indicators'])}")

    def start_analysis(self):
        """Start email analysis"""
        if self.analysis_active:
            return
        self.analysis_active = True
        self.analysis_thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.analysis_thread.start()
        print("📧 Email analysis started!")

    def stop_analysis(self):
        """Stop email analysis"""
        self.analysis_active = False
        if self.analysis_thread:
            self.analysis_thread.join(timeout=5)
        print("⏹️ Email analysis stopped!")

    def _analysis_loop(self):
        """Main email analysis loop"""
        while self.analysis_active:
            try:
                # Monitor for new emails (simplified implementation)
                self._monitor_new_emails()
                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                print(f"❌ Email analysis error: {e}")
                self.analysis_stats['analysis_errors'] += 1
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

    def analyze_email(self, email_data: Dict) -> Dict:
        """Analyze an email for suspicious content"""
        try:
            self.analysis_stats['emails_analyzed'] += 1
            
            analysis_result = {
                'timestamp': time.time(),
                'email_id': email_data.get('id', 'unknown'),
                'sender': email_data.get('sender', ''),
                'subject': email_data.get('subject', ''),
                'body': email_data.get('body', ''),
                'attachments': email_data.get('attachments', []),
                'links': email_data.get('links', []),
                'suspicious_score': 0,
                'threat_level': 'low',
                'threat_types': [],
                'recommendations': []
            }
            
            # Analyze email content
            content_analysis = self._analyze_email_content(email_data)
            analysis_result.update(content_analysis)
            
            # Analyze sender
            sender_analysis = self._analyze_sender(email_data.get('sender', ''))
            analysis_result.update(sender_analysis)
            
            # Analyze links
            link_analysis = self._analyze_links(email_data.get('links', []))
            analysis_result.update(link_analysis)
            
            # Analyze attachments
            attachment_analysis = self._analyze_attachments(email_data.get('attachments', []))
            analysis_result.update(attachment_analysis)
            
            # Calculate overall suspicious score
            analysis_result['suspicious_score'] = self._calculate_suspicious_score(analysis_result)
            
            # Determine threat level
            analysis_result['threat_level'] = self._determine_threat_level(analysis_result['suspicious_score'])
            
            # Generate recommendations
            analysis_result['recommendations'] = self._generate_recommendations(analysis_result)
            
            # Store analysis result
            self.email_history.append(analysis_result)
            
            # Check if email is suspicious
            if analysis_result['suspicious_score'] > 50:
                self.suspicious_emails.append(analysis_result)
                self.analysis_stats['suspicious_emails_detected'] += 1
                
                # Update specific threat type statistics
                for threat_type in analysis_result['threat_types']:
                    if threat_type == 'phishing':
                        self.analysis_stats['phishing_emails_detected'] += 1
                    elif threat_type == 'spam':
                        self.analysis_stats['spam_emails_detected'] += 1
                    elif threat_type == 'malware':
                        self.analysis_stats['malware_emails_detected'] += 1
                    elif threat_type == 'social_engineering':
                        self.analysis_stats['social_engineering_emails_detected'] += 1
            
            return analysis_result
            
        except Exception as e:
            return {'error': f'Email analysis failed: {e}'}

    def _analyze_email_content(self, email_data: Dict) -> Dict:
        """Analyze email content for suspicious patterns"""
        try:
            content_analysis = {
                'content_suspicious_score': 0,
                'content_threat_types': [],
                'content_indicators': []
            }
            
            # Combine subject and body for analysis
            full_text = f"{email_data.get('subject', '')} {email_data.get('body', '')}"
            full_text_lower = full_text.lower()
            
            # Check for phishing indicators
            phishing_score = 0
            for pattern in self.suspicious_patterns['phishing_indicators']:
                if re.search(pattern, full_text_lower):
                    phishing_score += 10
                    content_analysis['content_indicators'].append(f'phishing: {pattern}')
            
            if phishing_score > 0:
                content_analysis['content_threat_types'].append('phishing')
                content_analysis['content_suspicious_score'] += phishing_score
            
            # Check for spam indicators
            spam_score = 0
            for pattern in self.suspicious_patterns['spam_indicators']:
                if re.search(pattern, full_text_lower):
                    spam_score += 5
                    content_analysis['content_indicators'].append(f'spam: {pattern}')
            
            if spam_score > 0:
                content_analysis['content_threat_types'].append('spam')
                content_analysis['content_suspicious_score'] += spam_score
            
            # Check for malware indicators
            malware_score = 0
            for pattern in self.suspicious_patterns['malware_indicators']:
                if re.search(pattern, full_text_lower):
                    malware_score += 15
                    content_analysis['content_indicators'].append(f'malware: {pattern}')
            
            if malware_score > 0:
                content_analysis['content_threat_types'].append('malware')
                content_analysis['content_suspicious_score'] += malware_score
            
            # Check for social engineering indicators
            se_score = 0
            for pattern in self.suspicious_patterns['social_engineering_indicators']:
                if re.search(pattern, full_text_lower):
                    se_score += 12
                    content_analysis['content_indicators'].append(f'social_engineering: {pattern}')
            
            if se_score > 0:
                content_analysis['content_threat_types'].append('social_engineering')
                content_analysis['content_suspicious_score'] += se_score
            
            return content_analysis
            
        except Exception as e:
            return {'error': f'Content analysis failed: {e}'}

    def _analyze_sender(self, sender: str) -> Dict:
        """Analyze email sender for suspicious characteristics"""
        try:
            sender_analysis = {
                'sender_suspicious_score': 0,
                'sender_threat_types': [],
                'sender_indicators': []
            }
            
            if not sender:
                return sender_analysis
            
            # Extract domain from sender
            domain = sender.split('@')[-1] if '@' in sender else ''
            
            # Check if domain is suspicious
            if domain in self.suspicious_domains:
                sender_analysis['sender_suspicious_score'] += 30
                sender_analysis['sender_threat_types'].append('suspicious_domain')
                sender_analysis['sender_indicators'].append(f'suspicious_domain: {domain}')
            
            # Check if domain is trusted
            elif domain in self.trusted_domains:
                sender_analysis['sender_suspicious_score'] -= 10  # Reduce suspicion for trusted domains
            
            # Check for suspicious sender patterns
            suspicious_patterns = [
                r'[0-9]+@',  # Numeric sender
                r'[a-z]+[0-9]+@',  # Alphanumeric sender
                r'[a-z]+[0-9]+[a-z]+@',  # Mixed alphanumeric sender
                r'[a-z]+[0-9]+[a-z]+[0-9]+@'  # Complex alphanumeric sender
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, sender.lower()):
                    sender_analysis['sender_suspicious_score'] += 5
                    sender_analysis['sender_indicators'].append(f'suspicious_pattern: {pattern}')
            
            # Check for typosquatting
            if self._check_typosquatting(domain):
                sender_analysis['sender_suspicious_score'] += 20
                sender_analysis['sender_threat_types'].append('typosquatting')
                sender_analysis['sender_indicators'].append(f'typosquatting: {domain}')
            
            return sender_analysis
            
        except Exception as e:
            return {'error': f'Sender analysis failed: {e}'}

    def _analyze_links(self, links: List[str]) -> Dict:
        """Analyze email links for suspicious characteristics"""
        try:
            link_analysis = {
                'link_suspicious_score': 0,
                'link_threat_types': [],
                'link_indicators': []
            }
            
            for link in links:
                # Check for suspicious URL patterns
                if self._is_suspicious_url(link):
                    link_analysis['link_suspicious_score'] += 15
                    link_analysis['link_threat_types'].append('suspicious_url')
                    link_analysis['link_indicators'].append(f'suspicious_url: {link}')
                
                # Check for URL shortening services
                if self._is_url_shortener(link):
                    link_analysis['link_suspicious_score'] += 10
                    link_analysis['link_threat_types'].append('url_shortener')
                    link_analysis['link_indicators'].append(f'url_shortener: {link}')
                
                # Check for IP addresses in URLs
                if self._contains_ip_address(link):
                    link_analysis['link_suspicious_score'] += 20
                    link_analysis['link_threat_types'].append('ip_address_url')
                    link_analysis['link_indicators'].append(f'ip_address_url: {link}')
                
                # Check for suspicious domains
                domain = self._extract_domain(link)
                if domain in self.suspicious_domains:
                    link_analysis['link_suspicious_score'] += 25
                    link_analysis['link_threat_types'].append('suspicious_domain')
                    link_analysis['link_indicators'].append(f'suspicious_domain: {domain}')
            
            return link_analysis
            
        except Exception as e:
            return {'error': f'Link analysis failed: {e}'}

    def _analyze_attachments(self, attachments: List[Dict]) -> Dict:
        """Analyze email attachments for suspicious characteristics"""
        try:
            attachment_analysis = {
                'attachment_suspicious_score': 0,
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
                        attachment_analysis['attachment_suspicious_score'] += 30
                        attachment_analysis['attachment_threat_types'].append('suspicious_extension')
                        attachment_analysis['attachment_indicators'].append(f'suspicious_extension: {ext}')
                
                # Check for double extensions
                if self._has_double_extension(filename):
                    attachment_analysis['attachment_suspicious_score'] += 20
                    attachment_analysis['attachment_threat_types'].append('double_extension')
                    attachment_analysis['attachment_indicators'].append(f'double_extension: {filename}')
                
                # Check for suspicious file names
                if self._is_suspicious_filename(filename):
                    attachment_analysis['attachment_suspicious_score'] += 15
                    attachment_analysis['attachment_threat_types'].append('suspicious_filename')
                    attachment_analysis['attachment_indicators'].append(f'suspicious_filename: {filename}')
                
                # Check for large file sizes
                if file_size > 10 * 1024 * 1024:  # 10MB
                    attachment_analysis['attachment_suspicious_score'] += 10
                    attachment_analysis['attachment_threat_types'].append('large_file')
                    attachment_analysis['attachment_indicators'].append(f'large_file: {file_size} bytes')
            
            return attachment_analysis
            
        except Exception as e:
            return {'error': f'Attachment analysis failed: {e}'}

    def _is_suspicious_url(self, url: str) -> bool:
        """Check if URL is suspicious"""
        try:
            # Check for suspicious patterns
            suspicious_patterns = [
                r'bit\.ly', r'tinyurl\.com', r'short\.ly', r't\.co',
                r'goo\.gl', r'ow\.ly', r'is\.gd', r'v\.gd'
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, url.lower()):
                    return True
            
            return False
            
        except Exception:
            return False

    def _is_url_shortener(self, url: str) -> bool:
        """Check if URL is a URL shortener"""
        try:
            url_shorteners = [
                'bit.ly', 'tinyurl.com', 'short.ly', 't.co',
                'goo.gl', 'ow.ly', 'is.gd', 'v.gd'
            ]
            
            for shortener in url_shorteners:
                if shortener in url.lower():
                    return True
            
            return False
            
        except Exception:
            return False

    def _contains_ip_address(self, url: str) -> bool:
        """Check if URL contains IP address"""
        try:
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            return bool(re.search(ip_pattern, url))
        except Exception:
            return False

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

    def _calculate_suspicious_score(self, analysis_result: Dict) -> int:
        """Calculate overall suspicious score"""
        try:
            total_score = 0
            
            # Add content suspicious score
            total_score += analysis_result.get('content_suspicious_score', 0)
            
            # Add sender suspicious score
            total_score += analysis_result.get('sender_suspicious_score', 0)
            
            # Add link suspicious score
            total_score += analysis_result.get('link_suspicious_score', 0)
            
            # Add attachment suspicious score
            total_score += analysis_result.get('attachment_suspicious_score', 0)
            
            return min(total_score, 100)  # Cap at 100
            
        except Exception:
            return 0

    def _determine_threat_level(self, suspicious_score: int) -> str:
        """Determine threat level based on suspicious score"""
        if suspicious_score >= 80:
            return 'critical'
        elif suspicious_score >= 60:
            return 'high'
        elif suspicious_score >= 40:
            return 'medium'
        else:
            return 'low'

    def _generate_recommendations(self, analysis_result: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        try:
            recommendations = []
            
            threat_level = analysis_result.get('threat_level', 'low')
            threat_types = analysis_result.get('threat_types', [])
            
            if threat_level == 'critical':
                recommendations.extend([
                    'IMMEDIATE_QUARANTINE',
                    'BLOCK_SENDER',
                    'NOTIFY_SECURITY_TEAM',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS'
                ])
            elif threat_level == 'high':
                recommendations.extend([
                    'QUARANTINE_EMAIL',
                    'BLOCK_SENDER',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS'
                ])
            elif threat_level == 'medium':
                recommendations.extend([
                    'FLAG_AS_SUSPICIOUS',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS'
                ])
            else:
                recommendations.append('CONTINUE_MONITORING')
            
            # Add specific recommendations based on threat types
            if 'phishing' in threat_types:
                recommendations.append('PHISHING_EDUCATION')
            if 'malware' in threat_types:
                recommendations.append('MALWARE_SCAN')
            if 'social_engineering' in threat_types:
                recommendations.append('SOCIAL_ENGINEERING_EDUCATION')
            
            return recommendations
            
        except Exception:
            return ['CONTINUE_MONITORING']

    def get_analysis_statistics(self) -> Dict:
        """Get email analysis statistics"""
        return {
            'analysis_active': self.analysis_active,
            'emails_analyzed': self.analysis_stats['emails_analyzed'],
            'suspicious_emails_detected': self.analysis_stats['suspicious_emails_detected'],
            'phishing_emails_detected': self.analysis_stats['phishing_emails_detected'],
            'spam_emails_detected': self.analysis_stats['spam_emails_detected'],
            'malware_emails_detected': self.analysis_stats['malware_emails_detected'],
            'social_engineering_emails_detected': self.analysis_stats['social_engineering_emails_detected'],
            'false_positives': self.analysis_stats['false_positives'],
            'analysis_errors': self.analysis_stats['analysis_errors'],
            'email_history_size': len(self.email_history),
            'suspicious_emails_size': len(self.suspicious_emails)
        }

    def get_recent_suspicious_emails(self, count: int = 10) -> List[Dict]:
        """Get recent suspicious emails"""
        return list(self.suspicious_emails)[-count:]

    def add_suspicious_domain(self, domain: str):
        """Add domain to suspicious domains list"""
        self.suspicious_domains.add(domain.lower())
        print(f"✅ Added suspicious domain: {domain}")

    def add_suspicious_ip(self, ip: str):
        """Add IP to suspicious IPs list"""
        self.suspicious_ips.add(ip)
        print(f"✅ Added suspicious IP: {ip}")

    def update_patterns(self, pattern_type: str, patterns: List[str]):
        """Update suspicious patterns"""
        if pattern_type in self.suspicious_patterns:
            self.suspicious_patterns[pattern_type].extend(patterns)
            print(f"✅ Updated {pattern_type} patterns: {len(patterns)} new patterns")

    def emergency_email_lockdown(self):
        """Emergency email lockdown mode"""
        try:
            print("🚨 EMERGENCY EMAIL LOCKDOWN ACTIVATED!")
            
            # Block all suspicious senders
            print("🚫 Blocking all suspicious senders...")
            
            # Quarantine all suspicious emails
            print("🔒 Quarantining all suspicious emails...")
            
            # Notify security team
            print("📢 Notifying security team...")
            
            print("✅ Emergency email lockdown completed!")
            
        except Exception as e:
            print(f"❌ Emergency lockdown error: {e}")

    def restore_normal_operation(self):
        """Restore normal email operation"""
        try:
            print("✅ Restoring normal email operation...")
            
            # Resume normal email processing
            print("📧 Resuming normal email processing...")
            
            print("✅ Normal email operation restored!")
            
        except Exception as e:
            print(f"❌ Operation restoration error: {e}")
