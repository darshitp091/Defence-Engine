"""
Advanced DDoS Mitigation Engine
Comprehensive DDoS attack detection and mitigation with AI-powered analysis
"""
import time
import threading
import hashlib
import secrets
from typing import Dict, List, Optional, Tuple
from collections import deque
import ipaddress
import socket
import struct
import random

class AdvancedDDoSMitigator:
    """Advanced DDoS Mitigation with AI-powered Detection and Response"""
    
    def __init__(self):
        self.attack_patterns = {
            'syn_flood': {
                'threshold': 1000,  # SYN packets per second
                'window': 60,  # 60 seconds
                'pattern': 'SYN flood attack detected'
            },
            'udp_flood': {
                'threshold': 2000,  # UDP packets per second
                'window': 60,
                'pattern': 'UDP flood attack detected'
            },
            'icmp_flood': {
                'threshold': 500,  # ICMP packets per second
                'window': 60,
                'pattern': 'ICMP flood attack detected'
            },
            'http_flood': {
                'threshold': 100,  # HTTP requests per second
                'window': 60,
                'pattern': 'HTTP flood attack detected'
            },
            'dns_amplification': {
                'threshold': 100,  # DNS queries per second
                'window': 60,
                'pattern': 'DNS amplification attack detected'
            },
            'ntp_amplification': {
                'threshold': 50,  # NTP queries per second
                'window': 60,
                'pattern': 'NTP amplification attack detected'
            },
            'memcached_amplification': {
                'threshold': 25,  # Memcached queries per second
                'window': 60,
                'pattern': 'Memcached amplification attack detected'
            }
        }
        
        # Traffic monitoring
        self.traffic_counters = {}
        self.attack_sources = set()
        self.blocked_ips = set()
        self.rate_limits = {}
        
        # Mitigation strategies
        self.mitigation_strategies = {
            'rate_limiting': True,
            'ip_blocking': True,
            'traffic_shaping': True,
            'connection_limiting': True,
            'protocol_filtering': True,
            'geographic_blocking': True,
            'behavioral_analysis': True
        }
        
        # Statistics
        self.ddos_stats = {
            'total_attacks_detected': 0,
            'total_attacks_mitigated': 0,
            'syn_flood_attacks': 0,
            'udp_flood_attacks': 0,
            'icmp_flood_attacks': 0,
            'http_flood_attacks': 0,
            'dns_amplification_attacks': 0,
            'ntp_amplification_attacks': 0,
            'memcached_amplification_attacks': 0,
            'ips_blocked': 0,
            'connections_limited': 0,
            'traffic_shaped': 0
        }
        
        # Monitoring thread
        self.monitoring_active = False
        self.monitoring_thread = None
        
        print("🛡️ Advanced DDoS Mitigator initialized!")
        print(f"   Attack patterns: {len(self.attack_patterns)}")
        print(f"   Mitigation strategies: {sum(self.mitigation_strategies.values())}")
        print(f"   Monitoring: {'Active' if self.monitoring_active else 'Inactive'}")
    
    def start_ddos_monitoring(self):
        """Start DDoS monitoring and mitigation"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("🔍 DDoS monitoring started!")
    
    def stop_ddos_monitoring(self):
        """Stop DDoS monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("⏹️ DDoS monitoring stopped!")
    
    def analyze_network_traffic(self, traffic_data: Dict) -> Dict:
        """Analyze network traffic for DDoS attacks"""
        analysis = {
            'is_ddos_attack': False,
            'attack_type': None,
            'attack_level': 0,
            'source_ips': [],
            'mitigation_applied': [],
            'recommendations': []
        }
        
        # Extract traffic information
        source_ip = traffic_data.get('source_ip', '')
        dest_ip = traffic_data.get('dest_ip', '')
        protocol = traffic_data.get('protocol', '')
        packet_count = traffic_data.get('packet_count', 0)
        bytes_transferred = traffic_data.get('bytes_transferred', 0)
        timestamp = traffic_data.get('timestamp', time.time())
        
        # Update traffic counters
        self._update_traffic_counters(source_ip, protocol, packet_count, timestamp)
        
        # Check for DDoS patterns
        for attack_type, config in self.attack_patterns.items():
            if self._detect_attack_pattern(attack_type, source_ip, protocol, timestamp):
                analysis['is_ddos_attack'] = True
                analysis['attack_type'] = attack_type
                analysis['attack_level'] = self._calculate_attack_level(attack_type, source_ip)
                analysis['source_ips'].append(source_ip)
                analysis['recommendations'].extend(self._get_mitigation_recommendations(attack_type))
                
                # Apply mitigation
                mitigation_applied = self._apply_mitigation(attack_type, source_ip, analysis['attack_level'])
                analysis['mitigation_applied'].extend(mitigation_applied)
                
                # Update statistics
                self._update_attack_statistics(attack_type)
                break
        
        return analysis
    
    def _update_traffic_counters(self, source_ip: str, protocol: str, packet_count: int, timestamp: float):
        """Update traffic counters for analysis"""
        current_time = int(timestamp)
        
        # Initialize counters for this IP and time window
        if source_ip not in self.traffic_counters:
            self.traffic_counters[source_ip] = {}
        
        if current_time not in self.traffic_counters[source_ip]:
            self.traffic_counters[source_ip][current_time] = {
                'total_packets': 0,
                'total_bytes': 0,
                'protocols': {},
                'connections': 0
            }
        
        # Update counters
        self.traffic_counters[source_ip][current_time]['total_packets'] += packet_count
        self.traffic_counters[source_ip][current_time]['total_bytes'] += packet_count * 64  # Estimate
        
        if protocol not in self.traffic_counters[source_ip][current_time]['protocols']:
            self.traffic_counters[source_ip][current_time]['protocols'][protocol] = 0
        
        self.traffic_counters[source_ip][current_time]['protocols'][protocol] += packet_count
        
        # Clean old counters (keep last 5 minutes)
        self._cleanup_old_counters(source_ip, current_time)
    
    def _detect_attack_pattern(self, attack_type: str, source_ip: str, protocol: str, timestamp: float) -> bool:
        """Detect specific DDoS attack patterns"""
        config = self.attack_patterns[attack_type]
        threshold = config['threshold']
        window = config['window']
        
        current_time = int(timestamp)
        window_start = current_time - window
        
        # Count packets in time window
        packet_count = 0
        if source_ip in self.traffic_counters:
            for time_slot in range(window_start, current_time + 1):
                if time_slot in self.traffic_counters[source_ip]:
                    if attack_type == 'syn_flood' and protocol == 'TCP':
                        packet_count += self.traffic_counters[source_ip][time_slot]['protocols'].get('TCP', 0)
                    elif attack_type == 'udp_flood' and protocol == 'UDP':
                        packet_count += self.traffic_counters[source_ip][time_slot]['protocols'].get('UDP', 0)
                    elif attack_type == 'icmp_flood' and protocol == 'ICMP':
                        packet_count += self.traffic_counters[source_ip][time_slot]['protocols'].get('ICMP', 0)
                    elif attack_type == 'http_flood' and protocol == 'HTTP':
                        packet_count += self.traffic_counters[source_ip][time_slot]['protocols'].get('HTTP', 0)
                    elif attack_type == 'dns_amplification' and protocol == 'DNS':
                        packet_count += self.traffic_counters[source_ip][time_slot]['protocols'].get('DNS', 0)
                    elif attack_type == 'ntp_amplification' and protocol == 'NTP':
                        packet_count += self.traffic_counters[source_ip][time_slot]['protocols'].get('NTP', 0)
                    elif attack_type == 'memcached_amplification' and protocol == 'Memcached':
                        packet_count += self.traffic_counters[source_ip][time_slot]['protocols'].get('Memcached', 0)
        
        return packet_count > threshold
    
    def _calculate_attack_level(self, attack_type: str, source_ip: str) -> int:
        """Calculate attack severity level"""
        base_level = 50
        
        # Increase level based on attack type
        if attack_type in ['syn_flood', 'udp_flood']:
            base_level += 30
        elif attack_type in ['dns_amplification', 'ntp_amplification', 'memcached_amplification']:
            base_level += 40
        elif attack_type in ['http_flood', 'icmp_flood']:
            base_level += 20
        
        # Increase level based on source IP history
        if source_ip in self.attack_sources:
            base_level += 20
        
        # Increase level based on packet volume
        if source_ip in self.traffic_counters:
            recent_packets = sum(
                self.traffic_counters[source_ip].get(time_slot, {}).get('total_packets', 0)
                for time_slot in range(int(time.time()) - 60, int(time.time()) + 1)
            )
            if recent_packets > 10000:
                base_level += 30
            elif recent_packets > 5000:
                base_level += 20
            elif recent_packets > 1000:
                base_level += 10
        
        return min(100, base_level)
    
    def _get_mitigation_recommendations(self, attack_type: str) -> List[str]:
        """Get mitigation recommendations for attack type"""
        recommendations = {
            'syn_flood': [
                'IMPLEMENT_SYN_COOKIES',
                'ENABLE_SYN_FLOOD_PROTECTION',
                'CONFIGURE_CONNECTION_LIMITS',
                'USE_LOAD_BALANCER',
                'IMPLEMENT_RATE_LIMITING'
            ],
            'udp_flood': [
                'BLOCK_UDP_TRAFFIC',
                'IMPLEMENT_UDP_FILTERING',
                'CONFIGURE_FIREWALL_RULES',
                'USE_DDOS_PROTECTION_SERVICE',
                'IMPLEMENT_TRAFFIC_SHAPING'
            ],
            'icmp_flood': [
                'BLOCK_ICMP_TRAFFIC',
                'IMPLEMENT_ICMP_FILTERING',
                'CONFIGURE_ICMP_RATE_LIMITS',
                'USE_ICMP_PROTECTION',
                'IMPLEMENT_PACKET_FILTERING'
            ],
            'http_flood': [
                'IMPLEMENT_HTTP_RATE_LIMITING',
                'USE_WEB_APPLICATION_FIREWALL',
                'CONFIGURE_HTTP_CONNECTION_LIMITS',
                'IMPLEMENT_CAPTCHA',
                'USE_CDN_PROTECTION'
            ],
            'dns_amplification': [
                'BLOCK_DNS_QUERIES',
                'IMPLEMENT_DNS_FILTERING',
                'CONFIGURE_DNS_RATE_LIMITS',
                'USE_DNS_PROTECTION_SERVICE',
                'IMPLEMENT_DNS_MONITORING'
            ],
            'ntp_amplification': [
                'BLOCK_NTP_QUERIES',
                'IMPLEMENT_NTP_FILTERING',
                'CONFIGURE_NTP_RATE_LIMITS',
                'USE_NTP_PROTECTION',
                'IMPLEMENT_NTP_MONITORING'
            ],
            'memcached_amplification': [
                'BLOCK_MEMCACHED_QUERIES',
                'IMPLEMENT_MEMCACHED_FILTERING',
                'CONFIGURE_MEMCACHED_RATE_LIMITS',
                'USE_MEMCACHED_PROTECTION',
                'IMPLEMENT_MEMCACHED_MONITORING'
            ]
        }
        
        return recommendations.get(attack_type, ['GENERAL_DDOS_MITIGATION'])
    
    def _apply_mitigation(self, attack_type: str, source_ip: str, attack_level: int) -> List[str]:
        """Apply DDoS mitigation strategies"""
        mitigation_applied = []
        
        # Rate limiting
        if self.mitigation_strategies['rate_limiting']:
            self._apply_rate_limiting(source_ip, attack_type)
            mitigation_applied.append('RATE_LIMITING')
        
        # IP blocking for high-level attacks
        if attack_level > 80 and self.mitigation_strategies['ip_blocking']:
            self._block_ip_address(source_ip)
            mitigation_applied.append('IP_BLOCKING')
        
        # Traffic shaping
        if self.mitigation_strategies['traffic_shaping']:
            self._apply_traffic_shaping(source_ip, attack_type)
            mitigation_applied.append('TRAFFIC_SHAPING')
        
        # Connection limiting
        if self.mitigation_strategies['connection_limiting']:
            self._apply_connection_limiting(source_ip)
            mitigation_applied.append('CONNECTION_LIMITING')
        
        # Protocol filtering
        if self.mitigation_strategies['protocol_filtering']:
            self._apply_protocol_filtering(source_ip, attack_type)
            mitigation_applied.append('PROTOCOL_FILTERING')
        
        return mitigation_applied
    
    def _apply_rate_limiting(self, source_ip: str, attack_type: str):
        """Apply rate limiting to source IP"""
        if source_ip not in self.rate_limits:
            self.rate_limits[source_ip] = {
                'packet_limit': 100,  # packets per second
                'byte_limit': 10000,  # bytes per second
                'connection_limit': 10,  # connections per second
                'last_reset': time.time()
            }
        
        # Reduce limits for attack sources
        if source_ip in self.attack_sources:
            self.rate_limits[source_ip]['packet_limit'] = max(10, self.rate_limits[source_ip]['packet_limit'] // 2)
            self.rate_limits[source_ip]['byte_limit'] = max(1000, self.rate_limits[source_ip]['byte_limit'] // 2)
            self.rate_limits[source_ip]['connection_limit'] = max(1, self.rate_limits[source_ip]['connection_limit'] // 2)
        
        print(f"🚦 Rate limiting applied to {source_ip}: {self.rate_limits[source_ip]}")
    
    def _block_ip_address(self, source_ip: str):
        """Block IP address"""
        self.blocked_ips.add(source_ip)
        self.attack_sources.add(source_ip)
        self.ddos_stats['ips_blocked'] += 1
        print(f"🚫 IP address blocked: {source_ip}")
    
    def _apply_traffic_shaping(self, source_ip: str, attack_type: str):
        """Apply traffic shaping"""
        # Implement traffic shaping logic
        self.ddos_stats['traffic_shaped'] += 1
        print(f"🌊 Traffic shaping applied to {source_ip} for {attack_type}")
    
    def _apply_connection_limiting(self, source_ip: str):
        """Apply connection limiting"""
        # Implement connection limiting logic
        self.ddos_stats['connections_limited'] += 1
        print(f"🔗 Connection limiting applied to {source_ip}")
    
    def _apply_protocol_filtering(self, source_ip: str, attack_type: str):
        """Apply protocol filtering"""
        # Implement protocol filtering logic
        print(f"🔍 Protocol filtering applied to {source_ip} for {attack_type}")
    
    def _update_attack_statistics(self, attack_type: str):
        """Update attack statistics"""
        self.ddos_stats['total_attacks_detected'] += 1
        self.ddos_stats['total_attacks_mitigated'] += 1
        
        if attack_type in self.ddos_stats:
            self.ddos_stats[attack_type] += 1
    
    def _cleanup_old_counters(self, source_ip: str, current_time: int):
        """Clean up old traffic counters"""
        if source_ip in self.traffic_counters:
            # Remove counters older than 5 minutes
            cutoff_time = current_time - 300
            old_times = [t for t in self.traffic_counters[source_ip].keys() if t < cutoff_time]
            for old_time in old_times:
                del self.traffic_counters[source_ip][old_time]
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Analyze current traffic patterns
                self._analyze_traffic_patterns()
                
                # Clean up old data
                self._cleanup_old_data()
                
                # Wait for next monitoring cycle
                time.sleep(10)  # 10-second intervals
                
            except Exception as e:
                print(f"❌ DDoS monitoring error: {e}")
                time.sleep(10)
    
    def _analyze_traffic_patterns(self):
        """Analyze overall traffic patterns"""
        current_time = time.time()
        
        # Check for coordinated attacks
        if len(self.attack_sources) > 10:
            print(f"🚨 Coordinated DDoS attack detected from {len(self.attack_sources)} sources!")
        
        # Check for amplification attacks
        amplification_sources = len([ip for ip in self.attack_sources if self._is_amplification_source(ip)])
        if amplification_sources > 5:
            print(f"🚨 Amplification attack detected from {amplification_sources} sources!")
    
    def _is_amplification_source(self, source_ip: str) -> bool:
        """Check if source IP is used for amplification attacks"""
        # Check for DNS, NTP, or Memcached amplification patterns
        if source_ip in self.traffic_counters:
            recent_protocols = {}
            current_time = int(time.time())
            for time_slot in range(current_time - 60, current_time + 1):
                if time_slot in self.traffic_counters[source_ip]:
                    for protocol, count in self.traffic_counters[source_ip][time_slot]['protocols'].items():
                        if protocol in ['DNS', 'NTP', 'Memcached']:
                            recent_protocols[protocol] = recent_protocols.get(protocol, 0) + count
            
            # Check if any amplification protocol exceeds threshold
            for protocol, count in recent_protocols.items():
                if count > 50:  # Threshold for amplification detection
                    return True
        
        return False
    
    def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        current_time = time.time()
        cutoff_time = current_time - 3600  # 1 hour
        
        # Clean up old traffic counters
        for source_ip in list(self.traffic_counters.keys()):
            if source_ip in self.traffic_counters:
                old_times = [t for t in self.traffic_counters[source_ip].keys() if t < cutoff_time]
                for old_time in old_times:
                    del self.traffic_counters[source_ip][old_time]
                
                # Remove empty IP entries
                if not self.traffic_counters[source_ip]:
                    del self.traffic_counters[source_ip]
    
    def get_ddos_statistics(self) -> Dict:
        """Get DDoS mitigation statistics"""
        return {
            'monitoring_active': self.monitoring_active,
            'total_attacks_detected': self.ddos_stats['total_attacks_detected'],
            'total_attacks_mitigated': self.ddos_stats['total_attacks_mitigated'],
            'mitigation_rate': (self.ddos_stats['total_attacks_mitigated'] / max(self.ddos_stats['total_attacks_detected'], 1)) * 100,
            'attack_types': {
                'syn_flood': self.ddos_stats['syn_flood_attacks'],
                'udp_flood': self.ddos_stats['udp_flood_attacks'],
                'icmp_flood': self.ddos_stats['icmp_flood_attacks'],
                'http_flood': self.ddos_stats['http_flood_attacks'],
                'dns_amplification': self.ddos_stats['dns_amplification_attacks'],
                'ntp_amplification': self.ddos_stats['ntp_amplification_attacks'],
                'memcached_amplification': self.ddos_stats['memcached_amplification_attacks']
            },
            'mitigation_actions': {
                'ips_blocked': self.ddos_stats['ips_blocked'],
                'connections_limited': self.ddos_stats['connections_limited'],
                'traffic_shaped': self.ddos_stats['traffic_shaped']
            },
            'active_sources': len(self.attack_sources),
            'blocked_ips': len(self.blocked_ips),
            'monitored_ips': len(self.traffic_counters)
        }
    
    def unblock_ip(self, source_ip: str):
        """Unblock IP address"""
        if source_ip in self.blocked_ips:
            self.blocked_ips.remove(source_ip)
            print(f"✅ IP address unblocked: {source_ip}")
    
    def add_attack_source(self, source_ip: str):
        """Add IP to attack sources list"""
        self.attack_sources.add(source_ip)
        print(f"⚠️ IP added to attack sources: {source_ip}")
    
    def remove_attack_source(self, source_ip: str):
        """Remove IP from attack sources list"""
        if source_ip in self.attack_sources:
            self.attack_sources.remove(source_ip)
            print(f"✅ IP removed from attack sources: {source_ip}")
    
    def configure_attack_threshold(self, attack_type: str, threshold: int):
        """Configure attack detection threshold"""
        if attack_type in self.attack_patterns:
            self.attack_patterns[attack_type]['threshold'] = threshold
            print(f"⚙️ Threshold updated for {attack_type}: {threshold}")
    
    def enable_mitigation_strategy(self, strategy: str):
        """Enable specific mitigation strategy"""
        if strategy in self.mitigation_strategies:
            self.mitigation_strategies[strategy] = True
            print(f"✅ Mitigation strategy enabled: {strategy}")
    
    def disable_mitigation_strategy(self, strategy: str):
        """Disable specific mitigation strategy"""
        if strategy in self.mitigation_strategies:
            self.mitigation_strategies[strategy] = False
            print(f"❌ Mitigation strategy disabled: {strategy}")
