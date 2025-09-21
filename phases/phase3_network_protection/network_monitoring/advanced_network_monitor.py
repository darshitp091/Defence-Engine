"""
Advanced Network Monitor
Comprehensive network monitoring with intrusion detection and threat analysis
"""
import time
import threading
import socket
import struct
import hashlib
import json
from typing import Dict, List, Optional, Tuple
from collections import deque
import ipaddress
import psutil

class AdvancedNetworkMonitor:
    """Advanced Network Monitor with Intrusion Detection"""
    
    def __init__(self):
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # Network interfaces
        self.network_interfaces = {}
        self.interface_stats = {}
        
        # Connection monitoring
        self.active_connections = {}
        self.connection_history = deque(maxlen=10000)
        self.suspicious_connections = set()
        self.blocked_connections = set()
        
        # Intrusion detection patterns
        self.intrusion_patterns = {
            'port_scanning': {
                'threshold': 10,  # connections to different ports
                'time_window': 60,  # within 60 seconds
                'pattern': 'Port scanning detected'
            },
            'brute_force': {
                'threshold': 5,  # failed connections
                'time_window': 300,  # within 5 minutes
                'pattern': 'Brute force attack detected'
            },
            'suspicious_ports': {
                'ports': [22, 23, 135, 139, 445, 1433, 3389, 5432, 3306],
                'pattern': 'Suspicious port access detected'
            },
            'unusual_protocols': {
                'protocols': ['ICMP', 'IGMP', 'GRE', 'ESP', 'AH'],
                'pattern': 'Unusual protocol detected'
            },
            'geographic_anomalies': {
                'high_risk_countries': ['CN', 'RU', 'KP', 'IR', 'SY'],
                'pattern': 'High-risk country connection detected'
            }
        }
        
        # Network statistics
        self.network_stats = {
            'total_connections_monitored': 0,
            'suspicious_connections_detected': 0,
            'intrusions_detected': 0,
            'port_scans_detected': 0,
            'brute_force_attempts': 0,
            'suspicious_port_access': 0,
            'unusual_protocol_detected': 0,
            'geographic_anomalies': 0,
            'connections_blocked': 0
        }
        
        # Alert system
        self.alert_callbacks = []
        self.alert_history = deque(maxlen=1000)
        
        print("🌐 Advanced Network Monitor initialized!")
        print(f"   Intrusion patterns: {len(self.intrusion_patterns)}")
        print(f"   Monitoring interfaces: {len(self.network_interfaces)}")
        print(f"   Connection history: {self.connection_history.maxlen}")
    
    def start_network_monitoring(self):
        """Start network monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("🌐 Network monitoring started!")
    
    def stop_network_monitoring(self):
        """Stop network monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("⏹️ Network monitoring stopped!")
    
    def monitor_connection(self, connection_data: Dict) -> Dict:
        """Monitor network connection for intrusions"""
        self.network_stats['total_connections_monitored'] += 1
        
        analysis = {
            'connection_id': connection_data.get('connection_id', ''),
            'source_ip': connection_data.get('source_ip', ''),
            'dest_ip': connection_data.get('dest_ip', ''),
            'source_port': connection_data.get('source_port', 0),
            'dest_port': connection_data.get('dest_port', 0),
            'protocol': connection_data.get('protocol', ''),
            'timestamp': time.time(),
            'is_suspicious': False,
            'intrusion_detected': False,
            'threat_level': 0,
            'threats_detected': [],
            'recommendations': []
        }
        
        # Check for port scanning
        port_scan_analysis = self._detect_port_scanning(connection_data)
        if port_scan_analysis['detected']:
            analysis['is_suspicious'] = True
            analysis['intrusion_detected'] = True
            analysis['threat_level'] = max(analysis['threat_level'], 80)
            analysis['threats_detected'].append('PORT_SCANNING')
            analysis['recommendations'].extend(port_scan_analysis['recommendations'])
            self.network_stats['port_scans_detected'] += 1
        
        # Check for brute force attacks
        brute_force_analysis = self._detect_brute_force(connection_data)
        if brute_force_analysis['detected']:
            analysis['is_suspicious'] = True
            analysis['intrusion_detected'] = True
            analysis['threat_level'] = max(analysis['threat_level'], 90)
            analysis['threats_detected'].append('BRUTE_FORCE')
            analysis['recommendations'].extend(brute_force_analysis['recommendations'])
            self.network_stats['brute_force_attempts'] += 1
        
        # Check for suspicious port access
        suspicious_port_analysis = self._detect_suspicious_ports(connection_data)
        if suspicious_port_analysis['detected']:
            analysis['is_suspicious'] = True
            analysis['threat_level'] = max(analysis['threat_level'], 60)
            analysis['threats_detected'].append('SUSPICIOUS_PORT_ACCESS')
            analysis['recommendations'].extend(suspicious_port_analysis['recommendations'])
            self.network_stats['suspicious_port_access'] += 1
        
        # Check for unusual protocols
        unusual_protocol_analysis = self._detect_unusual_protocols(connection_data)
        if unusual_protocol_analysis['detected']:
            analysis['is_suspicious'] = True
            analysis['threat_level'] = max(analysis['threat_level'], 40)
            analysis['threats_detected'].append('UNUSUAL_PROTOCOL')
            analysis['recommendations'].extend(unusual_protocol_analysis['recommendations'])
            self.network_stats['unusual_protocol_detected'] += 1
        
        # Check for geographic anomalies
        geographic_analysis = self._detect_geographic_anomalies(connection_data)
        if geographic_analysis['detected']:
            analysis['is_suspicious'] = True
            analysis['threat_level'] = max(analysis['threat_level'], 70)
            analysis['threats_detected'].append('GEOGRAPHIC_ANOMALY')
            analysis['recommendations'].extend(geographic_analysis['recommendations'])
            self.network_stats['geographic_anomalies'] += 1
        
        # Update statistics
        if analysis['is_suspicious']:
            self.network_stats['suspicious_connections_detected'] += 1
            self.suspicious_connections.add(analysis['connection_id'])
        
        if analysis['intrusion_detected']:
            self.network_stats['intrusions_detected'] += 1
        
        # Store connection in history
        self.connection_history.append(analysis)
        
        # Generate alert if needed
        if analysis['threat_level'] > 70:
            self._generate_alert(analysis)
        
        return analysis
    
    def _detect_port_scanning(self, connection_data: Dict) -> Dict:
        """Detect port scanning attempts"""
        source_ip = connection_data.get('source_ip', '')
        dest_port = connection_data.get('dest_port', 0)
        timestamp = time.time()
        
        # Initialize tracking for this source IP
        if source_ip not in self.active_connections:
            self.active_connections[source_ip] = {
                'ports_accessed': set(),
                'first_connection': timestamp,
                'last_connection': timestamp,
                'connection_count': 0
            }
        
        # Update connection tracking
        self.active_connections[source_ip]['ports_accessed'].add(dest_port)
        self.active_connections[source_ip]['last_connection'] = timestamp
        self.active_connections[source_ip]['connection_count'] += 1
        
        # Check for port scanning pattern
        time_window = self.intrusion_patterns['port_scanning']['time_window']
        threshold = self.intrusion_patterns['port_scanning']['threshold']
        
        if (timestamp - self.active_connections[source_ip]['first_connection']) <= time_window:
            if len(self.active_connections[source_ip]['ports_accessed']) >= threshold:
                return {
                    'detected': True,
                    'recommendations': [
                        'BLOCK_SOURCE_IP',
                        'LOG_ATTEMPT',
                        'ALERT_SECURITY_TEAM',
                        'INVESTIGATE_SOURCE',
                        'IMPLEMENT_PORT_SCAN_DETECTION'
                    ]
                }
        
        return {'detected': False, 'recommendations': []}
    
    def _detect_brute_force(self, connection_data: Dict) -> Dict:
        """Detect brute force attacks"""
        source_ip = connection_data.get('source_ip', '')
        dest_port = connection_data.get('dest_port', 0)
        timestamp = time.time()
        
        # Check for failed connections to common services
        common_services = [22, 23, 21, 25, 110, 143, 993, 995, 3389, 5432, 3306]
        if dest_port in common_services:
            # This is a simplified check - in reality, you'd track failed authentication attempts
            if source_ip in self.active_connections:
                failed_attempts = self.active_connections[source_ip].get('failed_attempts', 0) + 1
                self.active_connections[source_ip]['failed_attempts'] = failed_attempts
                
                threshold = self.intrusion_patterns['brute_force']['threshold']
                time_window = self.intrusion_patterns['brute_force']['time_window']
                
                if failed_attempts >= threshold:
                    return {
                        'detected': True,
                        'recommendations': [
                            'BLOCK_SOURCE_IP',
                            'LOG_ATTEMPT',
                            'ALERT_SECURITY_TEAM',
                            'INVESTIGATE_SOURCE',
                            'IMPLEMENT_BRUTE_FORCE_PROTECTION'
                        ]
                    }
        
        return {'detected': False, 'recommendations': []}
    
    def _detect_suspicious_ports(self, connection_data: Dict) -> Dict:
        """Detect access to suspicious ports"""
        dest_port = connection_data.get('dest_port', 0)
        suspicious_ports = self.intrusion_patterns['suspicious_ports']['ports']
        
        if dest_port in suspicious_ports:
            return {
                'detected': True,
                'recommendations': [
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'INVESTIGATE_PORT_ACCESS',
                    'REVIEW_FIREWALL_RULES',
                    'IMPLEMENT_PORT_MONITORING'
                ]
            }
        
        return {'detected': False, 'recommendations': []}
    
    def _detect_unusual_protocols(self, connection_data: Dict) -> Dict:
        """Detect unusual protocol usage"""
        protocol = connection_data.get('protocol', '')
        unusual_protocols = self.intrusion_patterns['unusual_protocols']['protocols']
        
        if protocol in unusual_protocols:
            return {
                'detected': True,
                'recommendations': [
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'INVESTIGATE_PROTOCOL_USAGE',
                    'REVIEW_NETWORK_POLICIES',
                    'IMPLEMENT_PROTOCOL_FILTERING'
                ]
            }
        
        return {'detected': False, 'recommendations': []}
    
    def _detect_geographic_anomalies(self, connection_data: Dict) -> Dict:
        """Detect geographic anomalies"""
        source_ip = connection_data.get('source_ip', '')
        country = self._get_country_from_ip(source_ip)
        high_risk_countries = self.intrusion_patterns['geographic_anomalies']['high_risk_countries']
        
        if country in high_risk_countries:
            return {
                'detected': True,
                'recommendations': [
                    'LOG_ATTEMPT',
                    'ALERT_SECURITY_TEAM',
                    'INVESTIGATE_GEOGRAPHIC_SOURCE',
                    'REVIEW_GEOGRAPHIC_POLICIES',
                    'IMPLEMENT_GEOGRAPHIC_FILTERING'
                ]
            }
        
        return {'detected': False, 'recommendations': []}
    
    def _get_country_from_ip(self, ip_address: str) -> str:
        """Get country code from IP address"""
        try:
            # This is a simplified implementation
            # In reality, you'd use a GeoIP database
            ip_obj = ipaddress.ip_address(ip_address)
            
            if ip_obj.is_private:
                return 'PRIVATE'
            else:
                # Simplified country mapping
                first_octet = int(str(ip_obj).split('.')[0])
                if first_octet < 50:
                    return 'US'
                elif first_octet < 100:
                    return 'EU'
                elif first_octet < 150:
                    return 'AS'
                else:
                    return 'OTHER'
        except:
            return 'UNKNOWN'
    
    def _generate_alert(self, analysis: Dict):
        """Generate security alert"""
        alert = {
            'timestamp': time.time(),
            'alert_id': hashlib.md5(f"{analysis['connection_id']}_{time.time()}".encode()).hexdigest(),
            'threat_level': analysis['threat_level'],
            'threats_detected': analysis['threats_detected'],
            'source_ip': analysis['source_ip'],
            'dest_ip': analysis['dest_ip'],
            'dest_port': analysis['dest_port'],
            'protocol': analysis['protocol'],
            'recommendations': analysis['recommendations']
        }
        
        # Store alert
        self.alert_history.append(alert)
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"❌ Alert callback error: {e}")
        
        print(f"🚨 SECURITY ALERT: {analysis['threats_detected']} from {analysis['source_ip']}")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Monitor network interfaces
                self._monitor_network_interfaces()
                
                # Analyze connection patterns
                self._analyze_connection_patterns()
                
                # Clean up old data
                self._cleanup_old_data()
                
                # Wait for next monitoring cycle
                time.sleep(5)  # 5-second intervals
                
            except Exception as e:
                print(f"❌ Network monitoring error: {e}")
                time.sleep(5)
    
    def _monitor_network_interfaces(self):
        """Monitor network interfaces"""
        try:
            # Get network interface statistics
            net_io = psutil.net_io_counters(pernic=True)
            
            for interface, stats in net_io.items():
                if interface not in self.interface_stats:
                    self.interface_stats[interface] = {
                        'bytes_sent': 0,
                        'bytes_recv': 0,
                        'packets_sent': 0,
                        'packets_recv': 0,
                        'last_update': time.time()
                    }
                
                # Calculate interface usage
                prev_stats = self.interface_stats[interface]
                time_diff = time.time() - prev_stats['last_update']
                
                if time_diff > 0:
                    bytes_sent_rate = (stats.bytes_sent - prev_stats['bytes_sent']) / time_diff
                    bytes_recv_rate = (stats.bytes_recv - prev_stats['bytes_recv']) / time_diff
                    
                    # Check for unusual interface activity
                    if bytes_sent_rate > 1000000 or bytes_recv_rate > 1000000:  # 1MB/s
                        print(f"⚠️ High network activity on {interface}: {bytes_sent_rate:.0f} bytes/s sent, {bytes_recv_rate:.0f} bytes/s received")
                
                # Update interface statistics
                self.interface_stats[interface] = {
                    'bytes_sent': stats.bytes_sent,
                    'bytes_recv': stats.bytes_recv,
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv,
                    'last_update': time.time()
                }
                
        except Exception as e:
            print(f"❌ Interface monitoring error: {e}")
    
    def _analyze_connection_patterns(self):
        """Analyze connection patterns for anomalies"""
        if len(self.connection_history) < 100:
            return
        
        # Analyze recent connections
        recent_connections = list(self.connection_history)[-100:]
        
        # Check for coordinated attacks
        source_ips = [c['source_ip'] for c in recent_connections if c['is_suspicious']]
        if len(set(source_ips)) > 10:
            print(f"🚨 Coordinated attack detected from {len(set(source_ips))} sources!")
        
        # Check for port concentration
        dest_ports = [c['dest_port'] for c in recent_connections]
        port_counts = {}
        for port in dest_ports:
            port_counts[port] = port_counts.get(port, 0) + 1
        
        # Check for port scanning patterns
        for port, count in port_counts.items():
            if count > 20:  # 20 connections to same port
                print(f"⚠️ High connection count to port {port}: {count} connections")
    
    def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        current_time = time.time()
        cutoff_time = current_time - 3600  # 1 hour
        
        # Clean up old connections
        old_connections = [ip for ip, data in self.active_connections.items() 
                          if current_time - data['last_connection'] > cutoff_time]
        
        for ip in old_connections:
            del self.active_connections[ip]
    
    def add_alert_callback(self, callback):
        """Add alert callback function"""
        self.alert_callbacks.append(callback)
    
    def get_network_statistics(self) -> Dict:
        """Get network monitoring statistics"""
        return {
            'monitoring_active': self.monitoring_active,
            'total_connections_monitored': self.network_stats['total_connections_monitored'],
            'suspicious_connections_detected': self.network_stats['suspicious_connections_detected'],
            'intrusions_detected': self.network_stats['intrusions_detected'],
            'detection_rate': (self.network_stats['suspicious_connections_detected'] / max(self.network_stats['total_connections_monitored'], 1)) * 100,
            'intrusion_types': {
                'port_scans': self.network_stats['port_scans_detected'],
                'brute_force': self.network_stats['brute_force_attempts'],
                'suspicious_ports': self.network_stats['suspicious_port_access'],
                'unusual_protocols': self.network_stats['unusual_protocol_detected'],
                'geographic_anomalies': self.network_stats['geographic_anomalies']
            },
            'active_connections': len(self.active_connections),
            'suspicious_connections': len(self.suspicious_connections),
            'blocked_connections': len(self.blocked_connections),
            'connection_history_size': len(self.connection_history),
            'alert_history_size': len(self.alert_history),
            'network_interfaces': len(self.interface_stats)
        }
    
    def get_connection_summary(self, time_window: int = 3600) -> Dict:
        """Get connection summary for specified time window"""
        current_time = time.time()
        window_start = current_time - time_window
        
        # Filter connections within time window
        recent_connections = [c for c in self.connection_history if c.get('timestamp', 0) >= window_start]
        
        if not recent_connections:
            return {'error': 'No connection data in specified time window'}
        
        # Calculate summary statistics
        total_connections = len(recent_connections)
        suspicious_connections = sum(1 for c in recent_connections if c.get('is_suspicious'))
        intrusion_connections = sum(1 for c in recent_connections if c.get('intrusion_detected'))
        
        # Source IP distribution
        source_ips = [c['source_ip'] for c in recent_connections]
        unique_sources = len(set(source_ips))
        
        # Port distribution
        dest_ports = [c['dest_port'] for c in recent_connections]
        port_distribution = {}
        for port in dest_ports:
            port_distribution[port] = port_distribution.get(port, 0) + 1
        
        # Protocol distribution
        protocols = [c['protocol'] for c in recent_connections]
        protocol_distribution = {}
        for protocol in protocols:
            protocol_distribution[protocol] = protocol_distribution.get(protocol, 0) + 1
        
        return {
            'time_window': time_window,
            'total_connections': total_connections,
            'suspicious_connections': suspicious_connections,
            'intrusion_connections': intrusion_connections,
            'unique_sources': unique_sources,
            'port_distribution': port_distribution,
            'protocol_distribution': protocol_distribution,
            'suspicious_rate': (suspicious_connections / total_connections) * 100 if total_connections > 0 else 0,
            'intrusion_rate': (intrusion_connections / total_connections) * 100 if total_connections > 0 else 0
        }
    
    def block_connection(self, connection_id: str):
        """Block a specific connection"""
        self.blocked_connections.add(connection_id)
        self.network_stats['connections_blocked'] += 1
        print(f"🚫 Connection blocked: {connection_id}")
    
    def unblock_connection(self, connection_id: str):
        """Unblock a specific connection"""
        if connection_id in self.blocked_connections:
            self.blocked_connections.remove(connection_id)
            print(f"✅ Connection unblocked: {connection_id}")
    
    def get_recent_alerts(self, count: int = 50) -> List[Dict]:
        """Get recent security alerts"""
        return list(self.alert_history)[-count:]
