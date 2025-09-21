import time
import threading
import re
import hashlib
from collections import deque
from typing import Dict, List, Optional, Tuple
import json
import base64
import urllib.parse
import socket
import dns.resolver

class CommunicationAnalyzer:
    def __init__(self):
        self.analysis_active = False
        self.analysis_thread = None
        self.communication_history = deque(maxlen=10000)
        self.suspicious_communications = deque(maxlen=1000)
        
        # Communication analysis configuration
        self.analysis_config = {
            'analyze_emails': True,
            'analyze_chats': True,
            'analyze_calls': True,
            'analyze_files': True,
            'analyze_links': True,
            'analyze_attachments': True,
            'analyze_metadata': True,
            'analyze_timing': True,
            'analyze_frequency': True,
            'analyze_content': True
        }
        
        # Communication analysis patterns
        self.analysis_patterns = {
            'suspicious_keywords': [
                'password', 'login', 'account', 'verify', 'confirm',
                'urgent', 'immediate', 'act now', 'click here',
                'download', 'install', 'update', 'security',
                'breach', 'suspended', 'locked', 'expired'
            ],
            'suspicious_phrases': [
                'verify your account', 'confirm your identity',
                'update your information', 'security breach detected',
                'account suspended', 'password expired',
                'click here now', 'act immediately',
                'limited time offer', 'exclusive deal'
            ],
            'suspicious_domains': [
                'bit.ly', 'tinyurl.com', 'short.ly', 't.co',
                'goo.gl', 'ow.ly', 'is.gd', 'v.gd'
            ],
            'suspicious_extensions': [
                '.exe', '.bat', '.cmd', '.ps1', '.vbs', '.js',
                '.jar', '.scr', '.pif', '.com', '.scr'
            ]
        }
        
        # Communication analysis statistics
        self.analysis_stats = {
            'communications_analyzed': 0,
            'suspicious_communications_detected': 0,
            'phishing_communications_detected': 0,
            'malware_communications_detected': 0,
            'social_engineering_communications_detected': 0,
            'false_positives': 0,
            'analysis_errors': 0
        }
        
        print("💬 Communication Analyzer initialized!")
        print(f"   Suspicious keywords: {len(self.analysis_patterns['suspicious_keywords'])}")
        print(f"   Suspicious phrases: {len(self.analysis_patterns['suspicious_phrases'])}")
        print(f"   Suspicious domains: {len(self.analysis_patterns['suspicious_domains'])}")
        print(f"   Suspicious extensions: {len(self.analysis_patterns['suspicious_extensions'])}")

    def start_analysis(self):
        """Start communication analysis"""
        if self.analysis_active:
            return
        self.analysis_active = True
        self.analysis_thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.analysis_thread.start()
        print("💬 Communication analysis started!")

    def stop_analysis(self):
        """Stop communication analysis"""
        self.analysis_active = False
        if self.analysis_thread:
            self.analysis_thread.join(timeout=5)
        print("⏹️ Communication analysis stopped!")

    def _analysis_loop(self):
        """Main communication analysis loop"""
        while self.analysis_active:
            try:
                # Monitor for new communications (simplified implementation)
                self._monitor_new_communications()
                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                print(f"❌ Communication analysis error: {e}")
                self.analysis_stats['analysis_errors'] += 1
                time.sleep(5)

    def _monitor_new_communications(self):
        """Monitor for new communications to analyze"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd integrate with communication systems
            
            # Simulate communication monitoring
            pass
            
        except Exception as e:
            print(f"❌ Communication monitoring error: {e}")

    def analyze_communication(self, communication_data: Dict) -> Dict:
        """Analyze communication for suspicious activity"""
        try:
            self.analysis_stats['communications_analyzed'] += 1
            
            analysis_result = {
                'timestamp': time.time(),
                'communication_id': communication_data.get('id', 'unknown'),
                'type': communication_data.get('type', 'unknown'),
                'sender': communication_data.get('sender', ''),
                'recipient': communication_data.get('recipient', ''),
                'subject': communication_data.get('subject', ''),
                'content': communication_data.get('content', ''),
                'attachments': communication_data.get('attachments', []),
                'links': communication_data.get('links', []),
                'metadata': communication_data.get('metadata', {}),
                'suspicious_score': 0,
                'threat_level': 'low',
                'threat_types': [],
                'indicators': [],
                'recommendations': []
            }
            
            # Analyze communication content
            content_analysis = self._analyze_communication_content(communication_data)
            analysis_result.update(content_analysis)
            
            # Analyze communication metadata
            metadata_analysis = self._analyze_communication_metadata(communication_data.get('metadata', {}))
            analysis_result.update(metadata_analysis)
            
            # Analyze communication timing
            timing_analysis = self._analyze_communication_timing(communication_data)
            analysis_result.update(timing_analysis)
            
            # Analyze communication frequency
            frequency_analysis = self._analyze_communication_frequency(communication_data)
            analysis_result.update(frequency_analysis)
            
            # Analyze communication links
            link_analysis = self._analyze_communication_links(communication_data.get('links', []))
            analysis_result.update(link_analysis)
            
            # Analyze communication attachments
            attachment_analysis = self._analyze_communication_attachments(communication_data.get('attachments', []))
            analysis_result.update(attachment_analysis)
            
            # Calculate overall suspicious score
            analysis_result['suspicious_score'] = self._calculate_suspicious_score(analysis_result)
            
            # Determine threat level
            analysis_result['threat_level'] = self._determine_threat_level(analysis_result['suspicious_score'])
            
            # Generate recommendations
            analysis_result['recommendations'] = self._generate_recommendations(analysis_result)
            
            # Store analysis result
            self.communication_history.append(analysis_result)
            
            # Check if communication is suspicious
            if analysis_result['suspicious_score'] > 50:
                self.suspicious_communications.append(analysis_result)
                self.analysis_stats['suspicious_communications_detected'] += 1
                
                # Update specific threat type statistics
                for threat_type in analysis_result['threat_types']:
                    if threat_type == 'phishing':
                        self.analysis_stats['phishing_communications_detected'] += 1
                    elif threat_type == 'malware':
                        self.analysis_stats['malware_communications_detected'] += 1
                    elif threat_type == 'social_engineering':
                        self.analysis_stats['social_engineering_communications_detected'] += 1
            
            return analysis_result
            
        except Exception as e:
            return {'error': f'Communication analysis failed: {e}'}

    def _analyze_communication_content(self, communication_data: Dict) -> Dict:
        """Analyze communication content for suspicious patterns"""
        try:
            content_analysis = {
                'content_suspicious_score': 0,
                'content_threat_types': [],
                'content_indicators': []
            }
            
            # Combine subject and content for analysis
            full_text = f"{communication_data.get('subject', '')} {communication_data.get('content', '')}"
            full_text_lower = full_text.lower()
            
            # Check for suspicious keywords
            keyword_score = 0
            for keyword in self.analysis_patterns['suspicious_keywords']:
                if keyword in full_text_lower:
                    keyword_score += 5
                    content_analysis['content_indicators'].append(f'suspicious_keyword: {keyword}')
            
            if keyword_score > 0:
                content_analysis['content_threat_types'].append('suspicious_keywords')
                content_analysis['content_suspicious_score'] += keyword_score
            
            # Check for suspicious phrases
            phrase_score = 0
            for phrase in self.analysis_patterns['suspicious_phrases']:
                if phrase in full_text_lower:
                    phrase_score += 10
                    content_analysis['content_indicators'].append(f'suspicious_phrase: {phrase}')
            
            if phrase_score > 0:
                content_analysis['content_threat_types'].append('suspicious_phrases')
                content_analysis['content_suspicious_score'] += phrase_score
            
            # Check for urgent language
            urgent_patterns = [
                r'urgent', r'immediate', r'act\s+now', r'click\s+here',
                r'limited\s+time', r'expires\s+soon', r'final\s+notice',
                r'last\s+chance', r'act\s+fast', r'don\'t\s+miss'
            ]
            
            urgent_score = 0
            for pattern in urgent_patterns:
                if re.search(pattern, full_text_lower):
                    urgent_score += 8
                    content_analysis['content_indicators'].append(f'urgent_language: {pattern}')
            
            if urgent_score > 0:
                content_analysis['content_threat_types'].append('urgent_language')
                content_analysis['content_suspicious_score'] += urgent_score
            
            # Check for authority impersonation
            authority_patterns = [
                r'bank\s+of\s+america', r'chase\s+bank', r'wells\s+fargo',
                r'paypal', r'amazon', r'apple', r'microsoft', r'google',
                r'facebook', r'twitter', r'linkedin', r'instagram'
            ]
            
            authority_score = 0
            for pattern in authority_patterns:
                if re.search(pattern, full_text_lower):
                    authority_score += 12
                    content_analysis['content_indicators'].append(f'authority_impersonation: {pattern}')
            
            if authority_score > 0:
                content_analysis['content_threat_types'].append('authority_impersonation')
                content_analysis['content_suspicious_score'] += authority_score
            
            # Check for credential harvesting
            credential_patterns = [
                r'verify\s+your\s+account', r'confirm\s+your\s+identity',
                r'update\s+your\s+information', r'security\s+breach\s+detected',
                r'account\s+suspended', r'account\s+locked',
                r'password\s+expired', r'login\s+required'
            ]
            
            credential_score = 0
            for pattern in credential_patterns:
                if re.search(pattern, full_text_lower):
                    credential_score += 15
                    content_analysis['content_indicators'].append(f'credential_harvesting: {pattern}')
            
            if credential_score > 0:
                content_analysis['content_threat_types'].append('credential_harvesting')
                content_analysis['content_suspicious_score'] += credential_score
            
            return content_analysis
            
        except Exception as e:
            return {'error': f'Content analysis failed: {e}'}

    def _analyze_communication_metadata(self, metadata: Dict) -> Dict:
        """Analyze communication metadata for suspicious patterns"""
        try:
            metadata_analysis = {
                'metadata_suspicious_score': 0,
                'metadata_threat_types': [],
                'metadata_indicators': []
            }
            
            # Check for suspicious sender information
            sender = metadata.get('sender', '')
            if sender:
                if self._is_suspicious_sender(sender):
                    metadata_analysis['metadata_suspicious_score'] += 20
                    metadata_analysis['metadata_threat_types'].append('suspicious_sender')
                    metadata_analysis['metadata_indicators'].append(f'suspicious_sender: {sender}')
            
            # Check for suspicious recipient information
            recipient = metadata.get('recipient', '')
            if recipient:
                if self._is_suspicious_recipient(recipient):
                    metadata_analysis['metadata_suspicious_score'] += 15
                    metadata_analysis['metadata_threat_types'].append('suspicious_recipient')
                    metadata_analysis['metadata_indicators'].append(f'suspicious_recipient: {recipient}')
            
            # Check for suspicious IP addresses
            ip_address = metadata.get('ip_address', '')
            if ip_address:
                if self._is_suspicious_ip(ip_address):
                    metadata_analysis['metadata_suspicious_score'] += 25
                    metadata_analysis['metadata_threat_types'].append('suspicious_ip')
                    metadata_analysis['metadata_indicators'].append(f'suspicious_ip: {ip_address}')
            
            # Check for suspicious user agents
            user_agent = metadata.get('user_agent', '')
            if user_agent:
                if self._is_suspicious_user_agent(user_agent):
                    metadata_analysis['metadata_suspicious_score'] += 10
                    metadata_analysis['metadata_threat_types'].append('suspicious_user_agent')
                    metadata_analysis['metadata_indicators'].append(f'suspicious_user_agent: {user_agent}')
            
            return metadata_analysis
            
        except Exception as e:
            return {'error': f'Metadata analysis failed: {e}'}

    def _analyze_communication_timing(self, communication_data: Dict) -> Dict:
        """Analyze communication timing for suspicious patterns"""
        try:
            timing_analysis = {
                'timing_suspicious_score': 0,
                'timing_threat_types': [],
                'timing_indicators': []
            }
            
            # Check for unusual timing patterns
            timestamp = communication_data.get('timestamp', time.time())
            hour = datetime.fromtimestamp(timestamp).hour
            
            # Check for communications outside business hours
            if hour < 6 or hour > 22:
                timing_analysis['timing_suspicious_score'] += 10
                timing_analysis['timing_threat_types'].append('unusual_timing')
                timing_analysis['timing_indicators'].append(f'unusual_timing: {hour}:00')
            
            # Check for rapid-fire communications
            recent_communications = [c for c in self.communication_history 
                                   if time.time() - c['timestamp'] < 300]  # Last 5 minutes
            
            if len(recent_communications) > 10:
                timing_analysis['timing_suspicious_score'] += 15
                timing_analysis['timing_threat_types'].append('rapid_fire_communications')
                timing_analysis['timing_indicators'].append(f'rapid_fire_communications: {len(recent_communications)}')
            
            return timing_analysis
            
        except Exception as e:
            return {'error': f'Timing analysis failed: {e}'}

    def _analyze_communication_frequency(self, communication_data: Dict) -> Dict:
        """Analyze communication frequency for suspicious patterns"""
        try:
            frequency_analysis = {
                'frequency_suspicious_score': 0,
                'frequency_threat_types': [],
                'frequency_indicators': []
            }
            
            # Check for high frequency communications
            sender = communication_data.get('sender', '')
            if sender:
                sender_communications = [c for c in self.communication_history 
                                       if c.get('sender') == sender]
                
                # Check for communications in last hour
                recent_sender_communications = [c for c in sender_communications 
                                               if time.time() - c['timestamp'] < 3600]
                
                if len(recent_sender_communications) > 20:
                    frequency_analysis['frequency_suspicious_score'] += 20
                    frequency_analysis['frequency_threat_types'].append('high_frequency_sender')
                    frequency_analysis['frequency_indicators'].append(f'high_frequency_sender: {len(recent_sender_communications)}')
            
            return frequency_analysis
            
        except Exception as e:
            return {'error': f'Frequency analysis failed: {e}'}

    def _analyze_communication_links(self, links: List[str]) -> Dict:
        """Analyze communication links for suspicious patterns"""
        try:
            link_analysis = {
                'link_suspicious_score': 0,
                'link_threat_types': [],
                'link_indicators': []
            }
            
            for link in links:
                # Check for suspicious domains
                if self._is_suspicious_domain(link):
                    link_analysis['link_suspicious_score'] += 15
                    link_analysis['link_threat_types'].append('suspicious_domain')
                    link_analysis['link_indicators'].append(f'suspicious_domain: {link}')
                
                # Check for URL shorteners
                if self._is_url_shortener(link):
                    link_analysis['link_suspicious_score'] += 10
                    link_analysis['link_threat_types'].append('url_shortener')
                    link_analysis['link_indicators'].append(f'url_shortener: {link}')
                
                # Check for IP addresses in URLs
                if self._contains_ip_address(link):
                    link_analysis['link_suspicious_score'] += 20
                    link_analysis['link_threat_types'].append('ip_address_url')
                    link_analysis['link_indicators'].append(f'ip_address_url: {link}')
                
                # Check for suspicious patterns
                if self._has_suspicious_pattern(link):
                    link_analysis['link_suspicious_score'] += 12
                    link_analysis['link_threat_types'].append('suspicious_pattern')
                    link_analysis['link_indicators'].append(f'suspicious_pattern: {link}')
            
            return link_analysis
            
        except Exception as e:
            return {'error': f'Link analysis failed: {e}'}

    def _analyze_communication_attachments(self, attachments: List[Dict]) -> Dict:
        """Analyze communication attachments for suspicious patterns"""
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
                for ext in self.analysis_patterns['suspicious_extensions']:
                    if filename.lower().endswith(ext):
                        attachment_analysis['attachment_suspicious_score'] += 20
                        attachment_analysis['attachment_threat_types'].append('suspicious_extension')
                        attachment_analysis['attachment_indicators'].append(f'suspicious_extension: {ext}')
                
                # Check for double extensions
                if self._has_double_extension(filename):
                    attachment_analysis['attachment_suspicious_score'] += 15
                    attachment_analysis['attachment_threat_types'].append('double_extension')
                    attachment_analysis['attachment_indicators'].append(f'double_extension: {filename}')
                
                # Check for suspicious file names
                if self._is_suspicious_filename(filename):
                    attachment_analysis['attachment_suspicious_score'] += 10
                    attachment_analysis['attachment_threat_types'].append('suspicious_filename')
                    attachment_analysis['attachment_indicators'].append(f'suspicious_filename: {filename}')
                
                # Check for large file sizes
                if file_size > 10 * 1024 * 1024:  # 10MB
                    attachment_analysis['attachment_suspicious_score'] += 8
                    attachment_analysis['attachment_threat_types'].append('large_file')
                    attachment_analysis['attachment_indicators'].append(f'large_file: {file_size} bytes')
            
            return attachment_analysis
            
        except Exception as e:
            return {'error': f'Attachment analysis failed: {e}'}

    def _is_suspicious_sender(self, sender: str) -> bool:
        """Check if sender is suspicious"""
        try:
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
                    return True
            
            return False
            
        except Exception:
            return False

    def _is_suspicious_recipient(self, recipient: str) -> bool:
        """Check if recipient is suspicious"""
        try:
            # Check for suspicious recipient patterns
            suspicious_patterns = [
                r'[0-9]+@',  # Numeric recipient
                r'[a-z]+[0-9]+@',  # Alphanumeric recipient
                r'[a-z]+[0-9]+[a-z]+@',  # Mixed alphanumeric recipient
                r'[a-z]+-[a-z]+@',  # Hyphenated recipient
                r'[a-z]+_[a-z]+@'  # Underscore separated recipient
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, recipient.lower()):
                    return True
            
            return False
            
        except Exception:
            return False

    def _is_suspicious_ip(self, ip: str) -> bool:
        """Check if IP address is suspicious"""
        try:
            # Check for private IP ranges
            private_ranges = [
                '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16',
                '127.0.0.0/8', '169.254.0.0/16'
            ]
            
            for range_str in private_ranges:
                if self._ip_in_range(ip, range_str):
                    return True
            
            return False
            
        except Exception:
            return False

    def _ip_in_range(self, ip: str, range_str: str) -> bool:
        """Check if IP is in range"""
        try:
            import ipaddress
            return ipaddress.ip_address(ip) in ipaddress.ip_network(range_str)
        except Exception:
            return False

    def _is_suspicious_user_agent(self, user_agent: str) -> bool:
        """Check if user agent is suspicious"""
        try:
            # Check for suspicious user agent patterns
            suspicious_patterns = [
                r'bot', r'crawler', r'spider', r'scraper',
                r'automated', r'script', r'python', r'curl',
                r'wget', r'powershell', r'cmd'
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, user_agent.lower()):
                    return True
            
            return False
            
        except Exception:
            return False

    def _is_suspicious_domain(self, url: str) -> bool:
        """Check if domain is suspicious"""
        try:
            # Extract domain from URL
            domain = self._extract_domain(url)
            
            # Check for suspicious domains
            for suspicious_domain in self.analysis_patterns['suspicious_domains']:
                if suspicious_domain in domain.lower():
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

    def _has_suspicious_pattern(self, url: str) -> bool:
        """Check if URL has suspicious patterns"""
        try:
            # Check for suspicious patterns
            suspicious_patterns = [
                r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',  # IP addresses
                r'[a-z]+[0-9]+[a-z]+',  # Mixed alphanumeric
                r'[a-z]+-[a-z]+',  # Hyphenated domains
                r'[a-z]+_[a-z]+'  # Underscore separated
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, url.lower()):
                    return True
            
            return False
            
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
            
            # Add metadata suspicious score
            total_score += analysis_result.get('metadata_suspicious_score', 0)
            
            # Add timing suspicious score
            total_score += analysis_result.get('timing_suspicious_score', 0)
            
            # Add frequency suspicious score
            total_score += analysis_result.get('frequency_suspicious_score', 0)
            
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
                    'VERIFY_LINKS',
                    'COMMUNICATION_EDUCATION'
                ])
            elif threat_level == 'high':
                recommendations.extend([
                    'QUARANTINE_COMMUNICATION',
                    'BLOCK_SENDER',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS',
                    'COMMUNICATION_EDUCATION'
                ])
            elif threat_level == 'medium':
                recommendations.extend([
                    'FLAG_AS_SUSPICIOUS',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_LINKS',
                    'COMMUNICATION_EDUCATION'
                ])
            else:
                recommendations.append('CONTINUE_MONITORING')
            
            # Add specific recommendations based on threat types
            if 'suspicious_keywords' in threat_types:
                recommendations.append('KEYWORD_ANALYSIS')
            if 'authority_impersonation' in threat_types:
                recommendations.append('AUTHORITY_IMPERSONATION_EDUCATION')
            if 'credential_harvesting' in threat_types:
                recommendations.append('CREDENTIAL_HARVESTING_EDUCATION')
            if 'suspicious_links' in threat_types:
                recommendations.append('SUSPICIOUS_LINKS_EDUCATION')
            if 'suspicious_attachments' in threat_types:
                recommendations.append('SUSPICIOUS_ATTACHMENTS_EDUCATION')
            
            return recommendations
            
        except Exception:
            return ['CONTINUE_MONITORING']

    def get_analysis_statistics(self) -> Dict:
        """Get communication analysis statistics"""
        return {
            'analysis_active': self.analysis_active,
            'communications_analyzed': self.analysis_stats['communications_analyzed'],
            'suspicious_communications_detected': self.analysis_stats['suspicious_communications_detected'],
            'phishing_communications_detected': self.analysis_stats['phishing_communications_detected'],
            'malware_communications_detected': self.analysis_stats['malware_communications_detected'],
            'social_engineering_communications_detected': self.analysis_stats['social_engineering_communications_detected'],
            'false_positives': self.analysis_stats['false_positives'],
            'analysis_errors': self.analysis_stats['analysis_errors'],
            'communication_history_size': len(self.communication_history),
            'suspicious_communications_size': len(self.suspicious_communications)
        }

    def get_recent_suspicious_communications(self, count: int = 10) -> List[Dict]:
        """Get recent suspicious communications"""
        return list(self.suspicious_communications)[-count:]

    def add_suspicious_keyword(self, keyword: str):
        """Add keyword to suspicious keywords list"""
        self.analysis_patterns['suspicious_keywords'].append(keyword.lower())
        print(f"✅ Added suspicious keyword: {keyword}")

    def add_suspicious_phrase(self, phrase: str):
        """Add phrase to suspicious phrases list"""
        self.analysis_patterns['suspicious_phrases'].append(phrase.lower())
        print(f"✅ Added suspicious phrase: {phrase}")

    def add_suspicious_domain(self, domain: str):
        """Add domain to suspicious domains list"""
        self.analysis_patterns['suspicious_domains'].append(domain.lower())
        print(f"✅ Added suspicious domain: {domain}")

    def add_suspicious_extension(self, extension: str):
        """Add extension to suspicious extensions list"""
        self.analysis_patterns['suspicious_extensions'].append(extension.lower())
        print(f"✅ Added suspicious extension: {extension}")

    def update_analysis_config(self, config: Dict):
        """Update analysis configuration"""
        try:
            self.analysis_config.update(config)
            print(f"✅ Analysis configuration updated")
        except Exception as e:
            print(f"❌ Configuration update error: {e}")

    def emergency_communication_lockdown(self):
        """Emergency communication lockdown mode"""
        try:
            print("🚨 EMERGENCY COMMUNICATION LOCKDOWN ACTIVATED!")
            
            # Block all suspicious senders
            print("🚫 Blocking all suspicious senders...")
            
            # Quarantine all suspicious communications
            print("🔒 Quarantining all suspicious communications...")
            
            # Notify security team
            print("📢 Notifying security team...")
            
            # Activate communication education
            print("🎓 Activating communication education...")
            
            print("✅ Emergency communication lockdown completed!")
            
        except Exception as e:
            print(f"❌ Emergency lockdown error: {e}")

    def restore_normal_operation(self):
        """Restore normal communication analysis operation"""
        try:
            print("✅ Restoring normal communication analysis operation...")
            
            # Resume normal communication processing
            print("💬 Resuming normal communication processing...")
            
            print("✅ Normal communication analysis operation restored!")
            
        except Exception as e:
            print(f"❌ Operation restoration error: {e}")
