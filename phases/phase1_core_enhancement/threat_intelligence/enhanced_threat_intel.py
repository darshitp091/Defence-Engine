"""
Enhanced Threat Intelligence System
Advanced threat intelligence feeds and analysis with real-time updates
"""
import time
import threading
import requests
import json
import hashlib
import secrets
from typing import Dict, List, Optional, Tuple
from collections import deque
from datetime import datetime, timedelta
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class EnhancedThreatIntelligence:
    """Enhanced Threat Intelligence System with Real-time Feeds"""
    
    def __init__(self):
        self.threat_feeds = {}
        self.threat_database = {
            'malicious_ips': set(),
            'malicious_domains': set(),
            'malicious_urls': set(),
            'malicious_hashes': set(),
            'attack_patterns': {},
            'threat_actors': {},
            'vulnerabilities': {},
            'indicators': {}
        }
        
        # Feed configuration
        self.feed_sources = {
            'abuse_ch': 'https://feeds.abuse.ch/urlhaus/',
            'malware_domains': 'https://malwaredomains.com/',
            'threat_fox': 'https://threatfox.abuse.ch/',
            'otx_alienvault': 'https://otx.alienvault.com/api/v1/',
            'virustotal': 'https://www.virustotal.com/vtapi/v2/'
        }
        
        # Update configuration
        self.update_interval = 3600  # 1 hour
        self.is_updating = False
        self.update_thread = None
        
        # Statistics
        self.update_count = 0
        self.last_update = None
        self.feed_errors = {}
        
        print("🕵️ Enhanced Threat Intelligence initialized!")
        print(f"   Feed sources: {len(self.feed_sources)}")
        print(f"   Update interval: {self.update_interval}s")
    
    def start_threat_intelligence_updates(self):
        """Start threat intelligence updates"""
        if self.is_updating:
            return
        
        self.is_updating = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        
        print("🕵️ Threat intelligence updates started!")
    
    def stop_threat_intelligence_updates(self):
        """Stop threat intelligence updates"""
        self.is_updating = False
        if self.update_thread:
            self.update_thread.join(timeout=10)
        
        print("⏹️ Threat intelligence updates stopped!")
    
    def _update_loop(self):
        """Main update loop for threat intelligence"""
        while self.is_updating:
            try:
                # Update all threat feeds
                self._update_all_feeds()
                
                # Wait for next update cycle
                time.sleep(self.update_interval)
                
            except Exception as e:
                print(f"❌ Threat intelligence update error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def _update_all_feeds(self):
        """Update all threat intelligence feeds"""
        print("🕵️ Updating threat intelligence feeds...")
        
        for feed_name, feed_url in self.feed_sources.items():
            try:
                self._update_feed(feed_name, feed_url)
            except Exception as e:
                print(f"❌ Feed {feed_name} update error: {e}")
                self.feed_errors[feed_name] = str(e)
        
        self.update_count += 1
        self.last_update = time.time()
        
        print(f"✅ Threat intelligence update completed! (Update #{self.update_count})")
    
    def _update_feed(self, feed_name: str, feed_url: str):
        """Update individual threat feed"""
        try:
            # Simulate threat feed update (in real implementation, would fetch from actual feeds)
            if feed_name == 'abuse_ch':
                self._update_abuse_ch_feed()
            elif feed_name == 'malware_domains':
                self._update_malware_domains_feed()
            elif feed_name == 'threat_fox':
                self._update_threat_fox_feed()
            elif feed_name == 'otx_alienvault':
                self._update_otx_feed()
            elif feed_name == 'virustotal':
                self._update_virustotal_feed()
            
            print(f"   ✅ {feed_name} feed updated")
            
        except Exception as e:
            print(f"   ❌ {feed_name} feed update failed: {e}")
            raise
    
    def _update_abuse_ch_feed(self):
        """Update Abuse.ch threat feed"""
        # Simulate malicious URLs from Abuse.ch
        malicious_urls = [
            f"http://malicious-site-{secrets.token_hex(8)}.com",
            f"https://phishing-{secrets.token_hex(6)}.net",
            f"http://malware-{secrets.token_hex(10)}.org"
        ]
        
        for url in malicious_urls:
            self.threat_database['malicious_urls'].add(url)
    
    def _update_malware_domains_feed(self):
        """Update malware domains feed"""
        # Simulate malicious domains
        malicious_domains = [
            f"malware-{secrets.token_hex(8)}.com",
            f"trojan-{secrets.token_hex(6)}.net",
            f"virus-{secrets.token_hex(10)}.org"
        ]
        
        for domain in malicious_domains:
            self.threat_database['malicious_domains'].add(domain)
    
    def _update_threat_fox_feed(self):
        """Update ThreatFox feed"""
        # Simulate malicious IPs
        malicious_ips = [
            f"192.168.{secrets.randbelow(255)}.{secrets.randbelow(255)}",
            f"10.0.{secrets.randbelow(255)}.{secrets.randbelow(255)}",
            f"172.16.{secrets.randbelow(255)}.{secrets.randbelow(255)}"
        ]
        
        for ip in malicious_ips:
            self.threat_database['malicious_ips'].add(ip)
    
    def _update_otx_feed(self):
        """Update OTX AlienVault feed"""
        # Simulate threat indicators
        indicators = [
            {
                'type': 'file_hash',
                'value': hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
                'threat_type': 'malware',
                'confidence': 85
            },
            {
                'type': 'ip_address',
                'value': f"203.0.{secrets.randbelow(255)}.{secrets.randbelow(255)}",
                'threat_type': 'botnet',
                'confidence': 90
            }
        ]
        
        for indicator in indicators:
            self.threat_database['indicators'][indicator['value']] = indicator
    
    def _update_virustotal_feed(self):
        """Update VirusTotal feed"""
        # Simulate malicious hashes
        malicious_hashes = [
            hashlib.md5(secrets.token_bytes(16)).hexdigest(),
            hashlib.sha1(secrets.token_bytes(20)).hexdigest(),
            hashlib.sha256(secrets.token_bytes(32)).hexdigest()
        ]
        
        for hash_value in malicious_hashes:
            self.threat_database['malicious_hashes'].add(hash_value)
    
    def check_threat_indicator(self, indicator: str, indicator_type: str) -> Dict:
        """Check if an indicator is in threat database"""
        result = {
            'is_malicious': False,
            'threat_type': None,
            'confidence': 0,
            'source': None,
            'details': {}
        }
        
        if indicator_type == 'ip_address':
            if indicator in self.threat_database['malicious_ips']:
                result['is_malicious'] = True
                result['threat_type'] = 'malicious_ip'
                result['confidence'] = 90
                result['source'] = 'threat_intelligence'
        
        elif indicator_type == 'domain':
            if indicator in self.threat_database['malicious_domains']:
                result['is_malicious'] = True
                result['threat_type'] = 'malicious_domain'
                result['confidence'] = 85
                result['source'] = 'threat_intelligence'
        
        elif indicator_type == 'url':
            if indicator in self.threat_database['malicious_urls']:
                result['is_malicious'] = True
                result['threat_type'] = 'malicious_url'
                result['confidence'] = 80
                result['source'] = 'threat_intelligence'
        
        elif indicator_type == 'hash':
            if indicator in self.threat_database['malicious_hashes']:
                result['is_malicious'] = True
                result['threat_type'] = 'malicious_hash'
                result['confidence'] = 95
                result['source'] = 'threat_intelligence'
        
        return result
    
    def add_custom_threat(self, threat_data: Dict):
        """Add custom threat to database"""
        threat_type = threat_data.get('type', 'unknown')
        threat_value = threat_data.get('value', '')
        
        if threat_type == 'ip_address':
            self.threat_database['malicious_ips'].add(threat_value)
        elif threat_type == 'domain':
            self.threat_database['malicious_domains'].add(threat_value)
        elif threat_type == 'url':
            self.threat_database['malicious_urls'].add(threat_value)
        elif threat_type == 'hash':
            self.threat_database['malicious_hashes'].add(threat_value)
        
        print(f"✅ Custom threat added: {threat_type} - {threat_value}")
    
    def get_threat_statistics(self) -> Dict:
        """Get threat intelligence statistics"""
        return {
            'malicious_ips': len(self.threat_database['malicious_ips']),
            'malicious_domains': len(self.threat_database['malicious_domains']),
            'malicious_urls': len(self.threat_database['malicious_urls']),
            'malicious_hashes': len(self.threat_database['malicious_hashes']),
            'attack_patterns': len(self.threat_database['attack_patterns']),
            'threat_actors': len(self.threat_database['threat_actors']),
            'vulnerabilities': len(self.threat_database['vulnerabilities']),
            'indicators': len(self.threat_database['indicators']),
            'update_count': self.update_count,
            'last_update': self.last_update,
            'feed_errors': len(self.feed_errors),
            'is_updating': self.is_updating
        }
    
    def get_threat_database_summary(self) -> Dict:
        """Get threat database summary"""
        return {
            'total_indicators': sum([
                len(self.threat_database['malicious_ips']),
                len(self.threat_database['malicious_domains']),
                len(self.threat_database['malicious_urls']),
                len(self.threat_database['malicious_hashes']),
                len(self.threat_database['indicators'])
            ]),
            'database_size_mb': self._calculate_database_size(),
            'last_updated': self.last_update,
            'update_frequency': self.update_interval
        }
    
    def _calculate_database_size(self) -> float:
        """Calculate approximate database size in MB"""
        total_size = 0
        
        for key, value in self.threat_database.items():
            if isinstance(value, (set, dict)):
                total_size += len(str(value))
            else:
                total_size += len(str(value))
        
        return total_size / (1024 * 1024) * 8  # Convert to MB
    
    def search_threats(self, query: str) -> List[Dict]:
        """Search threats in database"""
        results = []
        
        # Search in malicious IPs
        for ip in self.threat_database['malicious_ips']:
            if query.lower() in ip.lower():
                results.append({
                    'type': 'ip_address',
                    'value': ip,
                    'threat_type': 'malicious_ip'
                })
        
        # Search in malicious domains
        for domain in self.threat_database['malicious_domains']:
            if query.lower() in domain.lower():
                results.append({
                    'type': 'domain',
                    'value': domain,
                    'threat_type': 'malicious_domain'
                })
        
        # Search in malicious URLs
        for url in self.threat_database['malicious_urls']:
            if query.lower() in url.lower():
                results.append({
                    'type': 'url',
                    'value': url,
                    'threat_type': 'malicious_url'
                })
        
        return results[:50]  # Limit to 50 results
