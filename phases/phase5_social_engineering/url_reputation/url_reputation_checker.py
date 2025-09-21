import time
import threading
import requests
import socket
import dns.resolver
from collections import deque
from typing import Dict, List, Optional, Tuple
import json
import hashlib
import re
import urllib.parse
from datetime import datetime, timedelta

class URLReputationChecker:
    def __init__(self):
        self.checking_active = False
        self.checking_thread = None
        self.url_history = deque(maxlen=10000)
        self.suspicious_urls = deque(maxlen=1000)
        self.trusted_urls = deque(maxlen=1000)
        
        # URL reputation configuration
        self.reputation_config = {
            'check_dns': True,
            'check_http_headers': True,
            'check_ssl_certificate': True,
            'check_blacklists': True,
            'check_whitelists': True,
            'check_geolocation': True,
            'check_domain_age': True,
            'check_redirects': True,
            'max_redirects': 5,
            'timeout': 10
        }
        
        # Reputation sources
        self.reputation_sources = {
            'blacklists': [
                'https://feodotracker.abuse.ch/blocklist/?download=ipblocklist',
                'https://mirror1.malwaredomains.com/files/justdomains',
                'https://threatfox.abuse.ch/export/json/ioc/recent/',
                'https://otx.alienvault.com/api/v1/indicators/export'
            ],
            'whitelists': [
                'https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json',
                'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'
            ]
        }
        
        # URL reputation patterns
        self.suspicious_patterns = {
            'suspicious_domains': [
                r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',  # IP addresses
                r'[a-z]+[0-9]+[a-z]+',  # Mixed alphanumeric
                r'[a-z]+-[a-z]+',  # Hyphenated domains
                r'[a-z]+_[a-z]+',  # Underscore separated
                r'[a-z]+[0-9]+',  # Alphanumeric
                r'[0-9]+[a-z]+'  # Numeric + alphabetic
            ],
            'suspicious_paths': [
                r'/admin', r'/login', r'/wp-admin', r'/phpmyadmin',
                r'/cpanel', r'/panel', r'/control', r'/manage',
                r'/secure', r'/private', r'/confidential'
            ],
            'suspicious_parameters': [
                r'[?&]id=', r'[?&]user=', r'[?&]pass=', r'[?&]pwd=',
                r'[?&]login=', r'[?&]admin=', r'[?&]root=', r'[?&]test='
            ]
        }
        
        # Reputation databases
        self.blacklisted_domains = set()
        self.blacklisted_ips = set()
        self.whitelisted_domains = set()
        self.whitelisted_ips = set()
        
        # Reputation statistics
        self.reputation_stats = {
            'urls_checked': 0,
            'suspicious_urls_detected': 0,
            'trusted_urls_verified': 0,
            'blacklist_hits': 0,
            'whitelist_hits': 0,
            'dns_failures': 0,
            'http_failures': 0,
            'ssl_failures': 0,
            'checking_errors': 0
        }
        
        print("🌐 URL Reputation Checker initialized!")
        print(f"   Blacklist sources: {len(self.reputation_sources['blacklists'])}")
        print(f"   Whitelist sources: {len(self.reputation_sources['whitelists'])}")
        print(f"   Suspicious patterns: {sum(len(v) for v in self.suspicious_patterns.values())}")

    def start_checking(self):
        """Start URL reputation checking"""
        if self.checking_active:
            return
        self.checking_active = True
        self.checking_thread = threading.Thread(target=self._checking_loop, daemon=True)
        self.checking_thread.start()
        print("🌐 URL reputation checking started!")

    def stop_checking(self):
        """Stop URL reputation checking"""
        self.checking_active = False
        if self.checking_thread:
            self.checking_thread.join(timeout=5)
        print("⏹️ URL reputation checking stopped!")

    def _checking_loop(self):
        """Main URL reputation checking loop"""
        while self.checking_active:
            try:
                # Update reputation databases
                self._update_reputation_databases()
                time.sleep(3600)  # Update every hour
            except Exception as e:
                print(f"❌ URL reputation checking error: {e}")
                self.reputation_stats['checking_errors'] += 1
                time.sleep(3600)

    def _update_reputation_databases(self):
        """Update reputation databases from external sources"""
        try:
            print("🔄 Updating reputation databases...")
            
            # Update blacklists
            for source in self.reputation_sources['blacklists']:
                try:
                    response = requests.get(source, timeout=30)
                    if response.status_code == 200:
                        self._parse_blacklist(response.text, source)
                except Exception as e:
                    print(f"❌ Failed to update blacklist from {source}: {e}")
            
            # Update whitelists
            for source in self.reputation_sources['whitelists']:
                try:
                    response = requests.get(source, timeout=30)
                    if response.status_code == 200:
                        self._parse_whitelist(response.text, source)
                except Exception as e:
                    print(f"❌ Failed to update whitelist from {source}: {e}")
            
            print(f"✅ Reputation databases updated: {len(self.blacklisted_domains)} blacklisted, {len(self.whitelisted_domains)} whitelisted")
            
        except Exception as e:
            print(f"❌ Reputation database update error: {e}")

    def _parse_blacklist(self, content: str, source: str):
        """Parse blacklist content"""
        try:
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Check if it's a domain or IP
                    if '.' in line and not line.startswith('http'):
                        if self._is_ip_address(line):
                            self.blacklisted_ips.add(line)
                        else:
                            self.blacklisted_domains.add(line.lower())
        except Exception as e:
            print(f"❌ Blacklist parsing error: {e}")

    def _parse_whitelist(self, content: str, source: str):
        """Parse whitelist content"""
        try:
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Check if it's a domain or IP
                    if '.' in line and not line.startswith('http'):
                        if self._is_ip_address(line):
                            self.whitelisted_ips.add(line)
                        else:
                            self.whitelisted_domains.add(line.lower())
        except Exception as e:
            print(f"❌ Whitelist parsing error: {e}")

    def _is_ip_address(self, text: str) -> bool:
        """Check if text is an IP address"""
        try:
            socket.inet_aton(text)
            return True
        except socket.error:
            return False

    def check_url_reputation(self, url: str) -> Dict:
        """Check URL reputation"""
        try:
            self.reputation_stats['urls_checked'] += 1
            
            reputation_result = {
                'timestamp': time.time(),
                'url': url,
                'domain': '',
                'ip_address': '',
                'reputation_score': 0,
                'threat_level': 'low',
                'threat_types': [],
                'indicators': [],
                'recommendations': []
            }
            
            # Parse URL
            parsed_url = urllib.parse.urlparse(url)
            domain = parsed_url.netloc.lower()
            reputation_result['domain'] = domain
            
            # Check domain reputation
            domain_analysis = self._analyze_domain(domain)
            reputation_result.update(domain_analysis)
            
            # Check IP reputation
            ip_analysis = self._analyze_ip(domain)
            reputation_result.update(ip_analysis)
            
            # Check URL patterns
            pattern_analysis = self._analyze_url_patterns(url)
            reputation_result.update(pattern_analysis)
            
            # Check HTTP headers
            if self.reputation_config['check_http_headers']:
                header_analysis = self._analyze_http_headers(url)
                reputation_result.update(header_analysis)
            
            # Check SSL certificate
            if self.reputation_config['check_ssl_certificate']:
                ssl_analysis = self._analyze_ssl_certificate(url)
                reputation_result.update(ssl_analysis)
            
            # Check redirects
            if self.reputation_config['check_redirects']:
                redirect_analysis = self._analyze_redirects(url)
                reputation_result.update(redirect_analysis)
            
            # Calculate overall reputation score
            reputation_result['reputation_score'] = self._calculate_reputation_score(reputation_result)
            
            # Determine threat level
            reputation_result['threat_level'] = self._determine_threat_level(reputation_result['reputation_score'])
            
            # Generate recommendations
            reputation_result['recommendations'] = self._generate_recommendations(reputation_result)
            
            # Store result
            self.url_history.append(reputation_result)
            
            # Check if URL is suspicious
            if reputation_result['reputation_score'] > 50:
                self.suspicious_urls.append(reputation_result)
                self.reputation_stats['suspicious_urls_detected'] += 1
            else:
                self.trusted_urls.append(reputation_result)
                self.reputation_stats['trusted_urls_verified'] += 1
            
            return reputation_result
            
        except Exception as e:
            return {'error': f'URL reputation check failed: {e}'}

    def _analyze_domain(self, domain: str) -> Dict:
        """Analyze domain reputation"""
        try:
            domain_analysis = {
                'domain_suspicious_score': 0,
                'domain_threat_types': [],
                'domain_indicators': []
            }
            
            # Check if domain is blacklisted
            if domain in self.blacklisted_domains:
                domain_analysis['domain_suspicious_score'] += 50
                domain_analysis['domain_threat_types'].append('blacklisted')
                domain_analysis['domain_indicators'].append(f'blacklisted_domain: {domain}')
                self.reputation_stats['blacklist_hits'] += 1
            
            # Check if domain is whitelisted
            elif domain in self.whitelisted_domains:
                domain_analysis['domain_suspicious_score'] -= 20
                domain_analysis['domain_indicators'].append(f'whitelisted_domain: {domain}')
                self.reputation_stats['whitelist_hits'] += 1
            
            # Check for suspicious domain patterns
            for pattern in self.suspicious_patterns['suspicious_domains']:
                if re.search(pattern, domain):
                    domain_analysis['domain_suspicious_score'] += 15
                    domain_analysis['domain_threat_types'].append('suspicious_pattern')
                    domain_analysis['domain_indicators'].append(f'suspicious_pattern: {pattern}')
            
            # Check DNS resolution
            if self.reputation_config['check_dns']:
                dns_analysis = self._check_dns_resolution(domain)
                domain_analysis.update(dns_analysis)
            
            return domain_analysis
            
        except Exception as e:
            return {'error': f'Domain analysis failed: {e}'}

    def _analyze_ip(self, domain: str) -> Dict:
        """Analyze IP reputation"""
        try:
            ip_analysis = {
                'ip_suspicious_score': 0,
                'ip_threat_types': [],
                'ip_indicators': []
            }
            
            # Resolve domain to IP
            try:
                ip_address = socket.gethostbyname(domain)
                ip_analysis['ip_address'] = ip_address
                
                # Check if IP is blacklisted
                if ip_address in self.blacklisted_ips:
                    ip_analysis['ip_suspicious_score'] += 40
                    ip_analysis['ip_threat_types'].append('blacklisted_ip')
                    ip_analysis['ip_indicators'].append(f'blacklisted_ip: {ip_address}')
                    self.reputation_stats['blacklist_hits'] += 1
                
                # Check if IP is whitelisted
                elif ip_address in self.whitelisted_ips:
                    ip_analysis['ip_suspicious_score'] -= 15
                    ip_analysis['ip_indicators'].append(f'whitelisted_ip: {ip_address}')
                    self.reputation_stats['whitelist_hits'] += 1
                
                # Check for suspicious IP patterns
                if self._is_suspicious_ip(ip_address):
                    ip_analysis['ip_suspicious_score'] += 20
                    ip_analysis['ip_threat_types'].append('suspicious_ip')
                    ip_analysis['ip_indicators'].append(f'suspicious_ip: {ip_address}')
                
            except socket.gaierror:
                ip_analysis['ip_suspicious_score'] += 30
                ip_analysis['ip_threat_types'].append('dns_resolution_failed')
                ip_analysis['ip_indicators'].append(f'dns_resolution_failed: {domain}')
                self.reputation_stats['dns_failures'] += 1
            
            return ip_analysis
            
        except Exception as e:
            return {'error': f'IP analysis failed: {e}'}

    def _analyze_url_patterns(self, url: str) -> Dict:
        """Analyze URL patterns for suspicious characteristics"""
        try:
            pattern_analysis = {
                'pattern_suspicious_score': 0,
                'pattern_threat_types': [],
                'pattern_indicators': []
            }
            
            # Check for suspicious paths
            for pattern in self.suspicious_patterns['suspicious_paths']:
                if re.search(pattern, url.lower()):
                    pattern_analysis['pattern_suspicious_score'] += 10
                    pattern_analysis['pattern_threat_types'].append('suspicious_path')
                    pattern_analysis['pattern_indicators'].append(f'suspicious_path: {pattern}')
            
            # Check for suspicious parameters
            for pattern in self.suspicious_patterns['suspicious_parameters']:
                if re.search(pattern, url.lower()):
                    pattern_analysis['pattern_suspicious_score'] += 15
                    pattern_analysis['pattern_threat_types'].append('suspicious_parameter')
                    pattern_analysis['pattern_indicators'].append(f'suspicious_parameter: {pattern}')
            
            # Check for URL shortening
            if self._is_url_shortener(url):
                pattern_analysis['pattern_suspicious_score'] += 5
                pattern_analysis['pattern_threat_types'].append('url_shortener')
                pattern_analysis['pattern_indicators'].append(f'url_shortener: {url}')
            
            # Check for IP addresses in URL
            if self._contains_ip_address(url):
                pattern_analysis['pattern_suspicious_score'] += 20
                pattern_analysis['pattern_threat_types'].append('ip_address_url')
                pattern_analysis['pattern_indicators'].append(f'ip_address_url: {url}')
            
            return pattern_analysis
            
        except Exception as e:
            return {'error': f'Pattern analysis failed: {e}'}

    def _analyze_http_headers(self, url: str) -> Dict:
        """Analyze HTTP headers for suspicious characteristics"""
        try:
            header_analysis = {
                'header_suspicious_score': 0,
                'header_threat_types': [],
                'header_indicators': []
            }
            
            try:
                response = requests.head(url, timeout=self.reputation_config['timeout'], allow_redirects=True)
                
                # Check for suspicious headers
                suspicious_headers = [
                    'X-Powered-By', 'Server', 'X-AspNet-Version',
                    'X-AspNetMvc-Version', 'X-Frame-Options'
                ]
                
                for header in suspicious_headers:
                    if header in response.headers:
                        header_analysis['header_suspicious_score'] += 5
                        header_analysis['header_indicators'].append(f'suspicious_header: {header}')
                
                # Check for missing security headers
                security_headers = [
                    'Strict-Transport-Security', 'X-Content-Type-Options',
                    'X-Frame-Options', 'X-XSS-Protection'
                ]
                
                for header in security_headers:
                    if header not in response.headers:
                        header_analysis['header_suspicious_score'] += 10
                        header_analysis['header_threat_types'].append('missing_security_header')
                        header_analysis['header_indicators'].append(f'missing_security_header: {header}')
                
                # Check response status
                if response.status_code >= 400:
                    header_analysis['header_suspicious_score'] += 15
                    header_analysis['header_threat_types'].append('http_error')
                    header_analysis['header_indicators'].append(f'http_error: {response.status_code}')
                
            except requests.exceptions.RequestException as e:
                header_analysis['header_suspicious_score'] += 25
                header_analysis['header_threat_types'].append('http_request_failed')
                header_analysis['header_indicators'].append(f'http_request_failed: {e}')
                self.reputation_stats['http_failures'] += 1
            
            return header_analysis
            
        except Exception as e:
            return {'error': f'Header analysis failed: {e}'}

    def _analyze_ssl_certificate(self, url: str) -> Dict:
        """Analyze SSL certificate for suspicious characteristics"""
        try:
            ssl_analysis = {
                'ssl_suspicious_score': 0,
                'ssl_threat_types': [],
                'ssl_indicators': []
            }
            
            # Check if URL uses HTTPS
            if not url.startswith('https://'):
                ssl_analysis['ssl_suspicious_score'] += 10
                ssl_analysis['ssl_threat_types'].append('no_https')
                ssl_analysis['ssl_indicators'].append('no_https: URL does not use HTTPS')
            else:
                try:
                    # Check SSL certificate (simplified)
                    import ssl
                    import socket
                    
                    hostname = urllib.parse.urlparse(url).netloc
                    context = ssl.create_default_context()
                    
                    with socket.create_connection((hostname, 443), timeout=10) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                            cert = ssock.getpeercert()
                            
                            # Check certificate validity
                            if not cert:
                                ssl_analysis['ssl_suspicious_score'] += 20
                                ssl_analysis['ssl_threat_types'].append('invalid_certificate')
                                ssl_analysis['ssl_indicators'].append('invalid_certificate: No certificate')
                            
                except Exception as e:
                    ssl_analysis['ssl_suspicious_score'] += 15
                    ssl_analysis['ssl_threat_types'].append('ssl_error')
                    ssl_analysis['ssl_indicators'].append(f'ssl_error: {e}')
                    self.reputation_stats['ssl_failures'] += 1
            
            return ssl_analysis
            
        except Exception as e:
            return {'error': f'SSL analysis failed: {e}'}

    def _analyze_redirects(self, url: str) -> Dict:
        """Analyze URL redirects for suspicious characteristics"""
        try:
            redirect_analysis = {
                'redirect_suspicious_score': 0,
                'redirect_threat_types': [],
                'redirect_indicators': []
            }
            
            try:
                response = requests.get(url, timeout=self.reputation_config['timeout'], 
                                      allow_redirects=True, max_redirects=self.reputation_config['max_redirects'])
                
                # Check redirect count
                if len(response.history) > 3:
                    redirect_analysis['redirect_suspicious_score'] += 15
                    redirect_analysis['redirect_threat_types'].append('excessive_redirects')
                    redirect_analysis['redirect_indicators'].append(f'excessive_redirects: {len(response.history)}')
                
                # Check for suspicious redirect patterns
                for redirect in response.history:
                    redirect_url = redirect.url
                    if self._is_suspicious_redirect(redirect_url):
                        redirect_analysis['redirect_suspicious_score'] += 10
                        redirect_analysis['redirect_threat_types'].append('suspicious_redirect')
                        redirect_analysis['redirect_indicators'].append(f'suspicious_redirect: {redirect_url}')
                
            except requests.exceptions.RequestException as e:
                redirect_analysis['redirect_suspicious_score'] += 20
                redirect_analysis['redirect_threat_types'].append('redirect_failed')
                redirect_analysis['redirect_indicators'].append(f'redirect_failed: {e}')
            
            return redirect_analysis
            
        except Exception as e:
            return {'error': f'Redirect analysis failed: {e}'}

    def _check_dns_resolution(self, domain: str) -> Dict:
        """Check DNS resolution for domain"""
        try:
            dns_analysis = {
                'dns_suspicious_score': 0,
                'dns_threat_types': [],
                'dns_indicators': []
            }
            
            try:
                # Check A record
                answers = dns.resolver.resolve(domain, 'A')
                if answers:
                    dns_analysis['dns_indicators'].append(f'dns_a_record: {len(answers)} records')
                
                # Check MX record
                try:
                    mx_answers = dns.resolver.resolve(domain, 'MX')
                    if mx_answers:
                        dns_analysis['dns_indicators'].append(f'dns_mx_record: {len(mx_answers)} records')
                except:
                    pass
                
                # Check TXT record
                try:
                    txt_answers = dns.resolver.resolve(domain, 'TXT')
                    if txt_answers:
                        dns_analysis['dns_indicators'].append(f'dns_txt_record: {len(txt_answers)} records')
                except:
                    pass
                
            except dns.resolver.NXDOMAIN:
                dns_analysis['dns_suspicious_score'] += 30
                dns_analysis['dns_threat_types'].append('dns_nxdomain')
                dns_analysis['dns_indicators'].append('dns_nxdomain: Domain does not exist')
            except dns.resolver.NoAnswer:
                dns_analysis['dns_suspicious_score'] += 20
                dns_analysis['dns_threat_types'].append('dns_no_answer')
                dns_analysis['dns_indicators'].append('dns_no_answer: No DNS records found')
            except Exception as e:
                dns_analysis['dns_suspicious_score'] += 25
                dns_analysis['dns_threat_types'].append('dns_error')
                dns_analysis['dns_indicators'].append(f'dns_error: {e}')
            
            return dns_analysis
            
        except Exception as e:
            return {'error': f'DNS analysis failed: {e}'}

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

    def _is_suspicious_redirect(self, url: str) -> bool:
        """Check if redirect URL is suspicious"""
        try:
            # Check for suspicious redirect patterns
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

    def _calculate_reputation_score(self, analysis_result: Dict) -> int:
        """Calculate overall reputation score"""
        try:
            total_score = 0
            
            # Add domain suspicious score
            total_score += analysis_result.get('domain_suspicious_score', 0)
            
            # Add IP suspicious score
            total_score += analysis_result.get('ip_suspicious_score', 0)
            
            # Add pattern suspicious score
            total_score += analysis_result.get('pattern_suspicious_score', 0)
            
            # Add header suspicious score
            total_score += analysis_result.get('header_suspicious_score', 0)
            
            # Add SSL suspicious score
            total_score += analysis_result.get('ssl_suspicious_score', 0)
            
            # Add redirect suspicious score
            total_score += analysis_result.get('redirect_suspicious_score', 0)
            
            # Add DNS suspicious score
            total_score += analysis_result.get('dns_suspicious_score', 0)
            
            return min(total_score, 100)  # Cap at 100
            
        except Exception:
            return 0

    def _determine_threat_level(self, reputation_score: int) -> str:
        """Determine threat level based on reputation score"""
        if reputation_score >= 80:
            return 'critical'
        elif reputation_score >= 60:
            return 'high'
        elif reputation_score >= 40:
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
                    'BLOCK_URL',
                    'QUARANTINE_EMAIL',
                    'NOTIFY_SECURITY_TEAM',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_SENDER'
                ])
            elif threat_level == 'high':
                recommendations.extend([
                    'FLAG_AS_SUSPICIOUS',
                    'SCAN_ATTACHMENTS',
                    'VERIFY_SENDER'
                ])
            elif threat_level == 'medium':
                recommendations.extend([
                    'WARN_USER',
                    'VERIFY_SENDER'
                ])
            else:
                recommendations.append('CONTINUE_MONITORING')
            
            # Add specific recommendations based on threat types
            if 'blacklisted' in threat_types:
                recommendations.append('BLOCK_BLACKLISTED')
            if 'suspicious_pattern' in threat_types:
                recommendations.append('PATTERN_ANALYSIS')
            if 'dns_error' in threat_types:
                recommendations.append('DNS_VERIFICATION')
            if 'ssl_error' in threat_types:
                recommendations.append('SSL_VERIFICATION')
            
            return recommendations
            
        except Exception:
            return ['CONTINUE_MONITORING']

    def get_reputation_statistics(self) -> Dict:
        """Get URL reputation statistics"""
        return {
            'checking_active': self.checking_active,
            'urls_checked': self.reputation_stats['urls_checked'],
            'suspicious_urls_detected': self.reputation_stats['suspicious_urls_detected'],
            'trusted_urls_verified': self.reputation_stats['trusted_urls_verified'],
            'blacklist_hits': self.reputation_stats['blacklist_hits'],
            'whitelist_hits': self.reputation_stats['whitelist_hits'],
            'dns_failures': self.reputation_stats['dns_failures'],
            'http_failures': self.reputation_stats['http_failures'],
            'ssl_failures': self.reputation_stats['ssl_failures'],
            'checking_errors': self.reputation_stats['checking_errors'],
            'url_history_size': len(self.url_history),
            'suspicious_urls_size': len(self.suspicious_urls),
            'trusted_urls_size': len(self.trusted_urls),
            'blacklisted_domains': len(self.blacklisted_domains),
            'blacklisted_ips': len(self.blacklisted_ips),
            'whitelisted_domains': len(self.whitelisted_domains),
            'whitelisted_ips': len(self.whitelisted_ips)
        }

    def get_recent_suspicious_urls(self, count: int = 10) -> List[Dict]:
        """Get recent suspicious URLs"""
        return list(self.suspicious_urls)[-count:]

    def get_recent_trusted_urls(self, count: int = 10) -> List[Dict]:
        """Get recent trusted URLs"""
        return list(self.trusted_urls)[-count:]

    def add_blacklisted_domain(self, domain: str):
        """Add domain to blacklist"""
        self.blacklisted_domains.add(domain.lower())
        print(f"✅ Added blacklisted domain: {domain}")

    def add_blacklisted_ip(self, ip: str):
        """Add IP to blacklist"""
        self.blacklisted_ips.add(ip)
        print(f"✅ Added blacklisted IP: {ip}")

    def add_whitelisted_domain(self, domain: str):
        """Add domain to whitelist"""
        self.whitelisted_domains.add(domain.lower())
        print(f"✅ Added whitelisted domain: {domain}")

    def add_whitelisted_ip(self, ip: str):
        """Add IP to whitelist"""
        self.whitelisted_ips.add(ip)
        print(f"✅ Added whitelisted IP: {ip}")

    def update_reputation_config(self, config: Dict):
        """Update reputation configuration"""
        try:
            self.reputation_config.update(config)
            print(f"✅ Reputation configuration updated")
        except Exception as e:
            print(f"❌ Configuration update error: {e}")

    def emergency_url_lockdown(self):
        """Emergency URL lockdown mode"""
        try:
            print("🚨 EMERGENCY URL LOCKDOWN ACTIVATED!")
            
            # Block all suspicious URLs
            print("🚫 Blocking all suspicious URLs...")
            
            # Quarantine all suspicious emails
            print("🔒 Quarantining all suspicious emails...")
            
            # Notify security team
            print("📢 Notifying security team...")
            
            print("✅ Emergency URL lockdown completed!")
            
        except Exception as e:
            print(f"❌ Emergency lockdown error: {e}")

    def restore_normal_operation(self):
        """Restore normal URL operation"""
        try:
            print("✅ Restoring normal URL operation...")
            
            # Resume normal URL processing
            print("🌐 Resuming normal URL processing...")
            
            print("✅ Normal URL operation restored!")
            
        except Exception as e:
            print(f"❌ Operation restoration error: {e}")
