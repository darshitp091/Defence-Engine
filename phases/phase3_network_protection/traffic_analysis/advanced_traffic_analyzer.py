"""
Advanced Traffic Analysis Engine
Comprehensive network traffic analysis with AI-powered anomaly detection
"""
import time
import threading
import hashlib
import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import deque
import ipaddress
import socket
import struct

class AdvancedTrafficAnalyzer:
    """Advanced Traffic Analysis with AI-powered Anomaly Detection"""
    
    def __init__(self):
        self.traffic_history = deque(maxlen=50000)  # 50k traffic records
        self.baseline_metrics = {}
        self.anomaly_thresholds = {
            'bandwidth': 0.8,  # 80% increase from baseline
            'packet_rate': 0.7,  # 70% increase from baseline
            'connection_count': 0.6,  # 60% increase from baseline
            'protocol_distribution': 0.5,  # 50% change in protocol distribution
            'geographic_distribution': 0.4,  # 40% change in geographic distribution
            'temporal_patterns': 0.6  # 60% change in temporal patterns
        }
        
        # Traffic analysis patterns
        self.analysis_patterns = {
            'bandwidth_anomalies': {
                'sudden_spike': 2.0,  # 200% increase
                'gradual_increase': 1.5,  # 150% increase
                'sustained_high': 1.3  # 130% sustained
            },
            'packet_anomalies': {
                'fragmentation': 0.1,  # 10% fragmented packets
                'large_packets': 0.05,  # 5% large packets
                'small_packets': 0.2,  # 20% small packets
                'retransmissions': 0.15  # 15% retransmissions
            },
            'connection_anomalies': {
                'rapid_connections': 100,  # 100 connections per second
                'long_connections': 3600,  # 1 hour connections
                'incomplete_connections': 0.3,  # 30% incomplete
                'connection_resets': 0.2  # 20% resets
            },
            'protocol_anomalies': {
                'unusual_protocols': 0.05,  # 5% unusual protocols
                'protocol_concentration': 0.8,  # 80% single protocol
                'encrypted_traffic': 0.9,  # 90% encrypted
                'unencrypted_traffic': 0.1  # 10% unencrypted
            }
        }
        
        # Geographic analysis
        self.geographic_data = {}
        self.country_codes = {}
        
        # Temporal analysis
        self.temporal_patterns = {
            'hourly': {},
            'daily': {},
            'weekly': {},
            'monthly': {}
        }
        
        # Statistics
        self.analysis_stats = {
            'total_packets_analyzed': 0,
            'total_bytes_analyzed': 0,
            'anomalies_detected': 0,
            'bandwidth_anomalies': 0,
            'packet_anomalies': 0,
            'connection_anomalies': 0,
            'protocol_anomalies': 0,
            'geographic_anomalies': 0,
            'temporal_anomalies': 0
        }
        
        # Monitoring thread
        self.monitoring_active = False
        self.monitoring_thread = None
        
        print("📊 Advanced Traffic Analyzer initialized!")
        print(f"   Analysis patterns: {len(self.analysis_patterns)}")
        print(f"   Anomaly thresholds: {len(self.anomaly_thresholds)}")
        print(f"   History capacity: {self.traffic_history.maxlen}")
    
    def start_traffic_analysis(self):
        """Start traffic analysis monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("📊 Traffic analysis started!")
    
    def stop_traffic_analysis(self):
        """Stop traffic analysis monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("⏹️ Traffic analysis stopped!")
    
    def analyze_traffic_packet(self, packet_data: Dict) -> Dict:
        """Analyze individual traffic packet"""
        analysis = {
            'timestamp': time.time(),
            'packet_id': packet_data.get('packet_id', ''),
            'source_ip': packet_data.get('source_ip', ''),
            'dest_ip': packet_data.get('dest_ip', ''),
            'protocol': packet_data.get('protocol', ''),
            'packet_size': packet_data.get('packet_size', 0),
            'flags': packet_data.get('flags', {}),
            'anomalies_detected': [],
            'risk_level': 0,
            'recommendations': []
        }
        
        # Update statistics
        self.analysis_stats['total_packets_analyzed'] += 1
        self.analysis_stats['total_bytes_analyzed'] += packet_data.get('packet_size', 0)
        
        # Analyze packet characteristics
        packet_analysis = self._analyze_packet_characteristics(packet_data)
        if packet_analysis['anomalies']:
            analysis['anomalies_detected'].extend(packet_analysis['anomalies'])
            analysis['risk_level'] = max(analysis['risk_level'], packet_analysis['risk_level'])
            analysis['recommendations'].extend(packet_analysis['recommendations'])
        
        # Analyze protocol patterns
        protocol_analysis = self._analyze_protocol_patterns(packet_data)
        if protocol_analysis['anomalies']:
            analysis['anomalies_detected'].extend(protocol_analysis['anomalies'])
            analysis['risk_level'] = max(analysis['risk_level'], protocol_analysis['risk_level'])
            analysis['recommendations'].extend(protocol_analysis['recommendations'])
        
        # Analyze geographic patterns
        geographic_analysis = self._analyze_geographic_patterns(packet_data)
        if geographic_analysis['anomalies']:
            analysis['anomalies_detected'].extend(geographic_analysis['anomalies'])
            analysis['risk_level'] = max(analysis['risk_level'], geographic_analysis['risk_level'])
            analysis['recommendations'].extend(geographic_analysis['recommendations'])
        
        # Analyze temporal patterns
        temporal_analysis = self._analyze_temporal_patterns(packet_data)
        if temporal_analysis['anomalies']:
            analysis['anomalies_detected'].extend(temporal_analysis['anomalies'])
            analysis['risk_level'] = max(analysis['risk_level'], temporal_analysis['risk_level'])
            analysis['recommendations'].extend(temporal_analysis['recommendations'])
        
        # Store in history
        self.traffic_history.append(analysis)
        
        # Update baseline metrics
        self._update_baseline_metrics(packet_data)
        
        return analysis
    
    def _analyze_packet_characteristics(self, packet_data: Dict) -> Dict:
        """Analyze packet characteristics for anomalies"""
        anomalies = []
        risk_level = 0
        recommendations = []
        
        packet_size = packet_data.get('packet_size', 0)
        protocol = packet_data.get('protocol', '')
        flags = packet_data.get('flags', {})
        
        # Check for packet size anomalies
        if packet_size > 1500:  # Jumbo frames
            anomalies.append('LARGE_PACKET_DETECTED')
            risk_level = max(risk_level, 30)
            recommendations.append('INVESTIGATE_LARGE_PACKETS')
        
        if packet_size < 64:  # Small packets
            anomalies.append('SMALL_PACKET_DETECTED')
            risk_level = max(risk_level, 20)
            recommendations.append('INVESTIGATE_SMALL_PACKETS')
        
        # Check for fragmentation
        if flags.get('fragmented', False):
            anomalies.append('FRAGMENTED_PACKET_DETECTED')
            risk_level = max(risk_level, 40)
            recommendations.append('INVESTIGATE_FRAGMENTATION')
        
        # Check for unusual flags
        if flags.get('syn', False) and flags.get('fin', False):
            anomalies.append('SYN_FIN_PACKET_DETECTED')
            risk_level = max(risk_level, 60)
            recommendations.append('INVESTIGATE_SYN_FIN_PACKETS')
        
        if flags.get('urg', False):
            anomalies.append('URGENT_PACKET_DETECTED')
            risk_level = max(risk_level, 50)
            recommendations.append('INVESTIGATE_URGENT_PACKETS')
        
        return {
            'anomalies': anomalies,
            'risk_level': risk_level,
            'recommendations': recommendations
        }
    
    def _analyze_protocol_patterns(self, packet_data: Dict) -> Dict:
        """Analyze protocol patterns for anomalies"""
        anomalies = []
        risk_level = 0
        recommendations = []
        
        protocol = packet_data.get('protocol', '')
        source_ip = packet_data.get('source_ip', '')
        dest_ip = packet_data.get('dest_ip', '')
        
        # Check for unusual protocols
        unusual_protocols = ['ICMP', 'IGMP', 'GRE', 'ESP', 'AH']
        if protocol in unusual_protocols:
            anomalies.append(f'UNUSUAL_PROTOCOL_{protocol}')
            risk_level = max(risk_level, 40)
            recommendations.append(f'INVESTIGATE_{protocol}_TRAFFIC')
        
        # Check for protocol concentration
        if self._is_protocol_concentrated(protocol):
            anomalies.append('PROTOCOL_CONCENTRATION')
            risk_level = max(risk_level, 30)
            recommendations.append('INVESTIGATE_PROTOCOL_CONCENTRATION')
        
        # Check for encrypted traffic patterns
        if self._is_encrypted_traffic(packet_data):
            anomalies.append('ENCRYPTED_TRAFFIC_DETECTED')
            risk_level = max(risk_level, 20)
            recommendations.append('INVESTIGATE_ENCRYPTED_TRAFFIC')
        
        return {
            'anomalies': anomalies,
            'risk_level': risk_level,
            'recommendations': recommendations
        }
    
    def _analyze_geographic_patterns(self, packet_data: Dict) -> Dict:
        """Analyze geographic patterns for anomalies"""
        anomalies = []
        risk_level = 0
        recommendations = []
        
        source_ip = packet_data.get('source_ip', '')
        dest_ip = packet_data.get('dest_ip', '')
        
        # Get geographic information
        source_country = self._get_country_from_ip(source_ip)
        dest_country = self._get_country_from_ip(dest_ip)
        
        # Check for international traffic
        if source_country != dest_country:
            anomalies.append('INTERNATIONAL_TRAFFIC')
            risk_level = max(risk_level, 30)
            recommendations.append('INVESTIGATE_INTERNATIONAL_TRAFFIC')
        
        # Check for high-risk countries
        high_risk_countries = ['CN', 'RU', 'KP', 'IR', 'SY']
        if source_country in high_risk_countries:
            anomalies.append(f'HIGH_RISK_COUNTRY_{source_country}')
            risk_level = max(risk_level, 70)
            recommendations.append(f'INVESTIGATE_TRAFFIC_FROM_{source_country}')
        
        # Check for geographic concentration
        if self._is_geographic_concentrated(source_country):
            anomalies.append('GEOGRAPHIC_CONCENTRATION')
            risk_level = max(risk_level, 40)
            recommendations.append('INVESTIGATE_GEOGRAPHIC_CONCENTRATION')
        
        return {
            'anomalies': anomalies,
            'risk_level': risk_level,
            'recommendations': recommendations
        }
    
    def _analyze_temporal_patterns(self, packet_data: Dict) -> Dict:
        """Analyze temporal patterns for anomalies"""
        anomalies = []
        risk_level = 0
        recommendations = []
        
        timestamp = packet_data.get('timestamp', time.time())
        current_hour = time.localtime(timestamp).tm_hour
        current_day = time.localtime(timestamp).tm_wday
        
        # Check for off-hours traffic
        if current_hour < 6 or current_hour > 22:
            anomalies.append('OFF_HOURS_TRAFFIC')
            risk_level = max(risk_level, 30)
            recommendations.append('INVESTIGATE_OFF_HOURS_TRAFFIC')
        
        # Check for weekend traffic
        if current_day in [5, 6]:  # Saturday, Sunday
            anomalies.append('WEEKEND_TRAFFIC')
            risk_level = max(risk_level, 20)
            recommendations.append('INVESTIGATE_WEEKEND_TRAFFIC')
        
        # Check for unusual time patterns
        if self._is_unusual_time_pattern(timestamp):
            anomalies.append('UNUSUAL_TIME_PATTERN')
            risk_level = max(risk_level, 40)
            recommendations.append('INVESTIGATE_TIME_PATTERNS')
        
        return {
            'anomalies': anomalies,
            'risk_level': risk_level,
            'recommendations': recommendations
        }
    
    def _is_protocol_concentrated(self, protocol: str) -> bool:
        """Check if protocol is concentrated"""
        if len(self.traffic_history) < 100:
            return False
        
        # Count protocol occurrences in recent history
        recent_packets = list(self.traffic_history)[-100:]
        protocol_count = sum(1 for p in recent_packets if p.get('protocol') == protocol)
        
        # Check if protocol represents more than 80% of traffic
        return protocol_count / len(recent_packets) > 0.8
    
    def _is_encrypted_traffic(self, packet_data: Dict) -> bool:
        """Check if traffic appears to be encrypted"""
        # Simple heuristic: check for high entropy in packet data
        packet_size = packet_data.get('packet_size', 0)
        if packet_size > 100:  # Only check larger packets
            # This is a simplified check - in reality, you'd analyze packet content
            return True
        
        return False
    
    def _get_country_from_ip(self, ip_address: str) -> str:
        """Get country code from IP address"""
        try:
            # This is a simplified implementation
            # In reality, you'd use a GeoIP database
            ip_obj = ipaddress.ip_address(ip_address)
            
            # Simple country mapping based on IP ranges
            if ip_obj.is_private:
                return 'PRIVATE'
            elif str(ip_obj).startswith('192.168.'):
                return 'PRIVATE'
            elif str(ip_obj).startswith('10.'):
                return 'PRIVATE'
            elif str(ip_obj).startswith('172.'):
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
    
    def _is_geographic_concentrated(self, country: str) -> bool:
        """Check if traffic is geographically concentrated"""
        if len(self.traffic_history) < 100:
            return False
        
        # Count country occurrences in recent history
        recent_packets = list(self.traffic_history)[-100:]
        country_count = sum(1 for p in recent_packets if self._get_country_from_ip(p.get('source_ip', '')) == country)
        
        # Check if country represents more than 70% of traffic
        return country_count / len(recent_packets) > 0.7
    
    def _is_unusual_time_pattern(self, timestamp: float) -> bool:
        """Check if timestamp represents unusual time pattern"""
        # Check against baseline temporal patterns
        current_hour = time.localtime(timestamp).tm_hour
        
        # Check if traffic is outside normal business hours
        if current_hour < 8 or current_hour > 18:
            return True
        
        return False
    
    def _update_baseline_metrics(self, packet_data: Dict):
        """Update baseline metrics for comparison"""
        current_time = time.time()
        protocol = packet_data.get('protocol', '')
        packet_size = packet_data.get('packet_size', 0)
        
        # Update protocol distribution
        if 'protocols' not in self.baseline_metrics:
            self.baseline_metrics['protocols'] = {}
        
        if protocol not in self.baseline_metrics['protocols']:
            self.baseline_metrics['protocols'][protocol] = 0
        
        self.baseline_metrics['protocols'][protocol] += 1
        
        # Update packet size metrics
        if 'packet_sizes' not in self.baseline_metrics:
            self.baseline_metrics['packet_sizes'] = []
        
        self.baseline_metrics['packet_sizes'].append(packet_size)
        
        # Keep only recent data (last 1000 packets)
        if len(self.baseline_metrics['packet_sizes']) > 1000:
            self.baseline_metrics['packet_sizes'] = self.baseline_metrics['packet_sizes'][-1000:]
    
    def _analysis_loop(self):
        """Main analysis loop"""
        while self.monitoring_active:
            try:
                # Analyze traffic patterns
                self._analyze_traffic_patterns()
                
                # Update anomaly statistics
                self._update_anomaly_statistics()
                
                # Wait for next analysis cycle
                time.sleep(30)  # 30-second intervals
                
            except Exception as e:
                print(f"❌ Traffic analysis error: {e}")
                time.sleep(30)
    
    def _analyze_traffic_patterns(self):
        """Analyze overall traffic patterns"""
        if len(self.traffic_history) < 100:
            return
        
        # Analyze bandwidth patterns
        bandwidth_analysis = self._analyze_bandwidth_patterns()
        if bandwidth_analysis['anomalies']:
            self.analysis_stats['bandwidth_anomalies'] += 1
        
        # Analyze packet patterns
        packet_analysis = self._analyze_packet_patterns()
        if packet_analysis['anomalies']:
            self.analysis_stats['packet_anomalies'] += 1
        
        # Analyze connection patterns
        connection_analysis = self._analyze_connection_patterns()
        if connection_analysis['anomalies']:
            self.analysis_stats['connection_anomalies'] += 1
    
    def _analyze_bandwidth_patterns(self) -> Dict:
        """Analyze bandwidth usage patterns"""
        if len(self.traffic_history) < 100:
            return {'anomalies': []}
        
        recent_packets = list(self.traffic_history)[-100:]
        total_bytes = sum(p.get('packet_size', 0) for p in recent_packets)
        
        # Check against baseline
        if 'packet_sizes' in self.baseline_metrics:
            baseline_avg = np.mean(self.baseline_metrics['packet_sizes'])
            current_avg = total_bytes / len(recent_packets)
            
            if current_avg > baseline_avg * (1 + self.anomaly_thresholds['bandwidth']):
                return {'anomalies': ['BANDWIDTH_SPIKE']}
        
        return {'anomalies': []}
    
    def _analyze_packet_patterns(self) -> Dict:
        """Analyze packet patterns"""
        if len(self.traffic_history) < 100:
            return {'anomalies': []}
        
        recent_packets = list(self.traffic_history)[-100:]
        
        # Check for packet size anomalies
        large_packets = sum(1 for p in recent_packets if p.get('packet_size', 0) > 1500)
        if large_packets / len(recent_packets) > self.analysis_patterns['packet_anomalies']['large_packets']:
            return {'anomalies': ['LARGE_PACKET_CONCENTRATION']}
        
        return {'anomalies': []}
    
    def _analyze_connection_patterns(self) -> Dict:
        """Analyze connection patterns"""
        if len(self.traffic_history) < 100:
            return {'anomalies': []}
        
        recent_packets = list(self.traffic_history)[-100:]
        
        # Check for connection rate
        unique_connections = len(set((p.get('source_ip', ''), p.get('dest_ip', '')) for p in recent_packets))
        if unique_connections > self.analysis_patterns['connection_anomalies']['rapid_connections']:
            return {'anomalies': ['RAPID_CONNECTION_ESTABLISHMENT']}
        
        return {'anomalies': []}
    
    def _update_anomaly_statistics(self):
        """Update anomaly statistics"""
        if len(self.traffic_history) < 100:
            return
        
        recent_packets = list(self.traffic_history)[-100:]
        anomaly_count = sum(1 for p in recent_packets if p.get('anomalies_detected'))
        
        if anomaly_count > 0:
            self.analysis_stats['anomalies_detected'] += anomaly_count
    
    def get_traffic_statistics(self) -> Dict:
        """Get traffic analysis statistics"""
        return {
            'monitoring_active': self.monitoring_active,
            'total_packets_analyzed': self.analysis_stats['total_packets_analyzed'],
            'total_bytes_analyzed': self.analysis_stats['total_bytes_analyzed'],
            'anomalies_detected': self.analysis_stats['anomalies_detected'],
            'anomaly_rate': (self.analysis_stats['anomalies_detected'] / max(self.analysis_stats['total_packets_analyzed'], 1)) * 100,
            'anomaly_types': {
                'bandwidth_anomalies': self.analysis_stats['bandwidth_anomalies'],
                'packet_anomalies': self.analysis_stats['packet_anomalies'],
                'connection_anomalies': self.analysis_stats['connection_anomalies'],
                'protocol_anomalies': self.analysis_stats['protocol_anomalies'],
                'geographic_anomalies': self.analysis_stats['geographic_anomalies'],
                'temporal_anomalies': self.analysis_stats['temporal_anomalies']
            },
            'traffic_history_size': len(self.traffic_history),
            'baseline_metrics': {
                'protocols': len(self.baseline_metrics.get('protocols', {})),
                'packet_sizes': len(self.baseline_metrics.get('packet_sizes', []))
            }
        }
    
    def get_traffic_summary(self, time_window: int = 3600) -> Dict:
        """Get traffic summary for specified time window"""
        current_time = time.time()
        window_start = current_time - time_window
        
        # Filter traffic within time window
        recent_traffic = [t for t in self.traffic_history if t.get('timestamp', 0) >= window_start]
        
        if not recent_traffic:
            return {'error': 'No traffic data in specified time window'}
        
        # Calculate summary statistics
        total_packets = len(recent_traffic)
        total_bytes = sum(t.get('packet_size', 0) for t in recent_traffic)
        unique_sources = len(set(t.get('source_ip', '') for t in recent_traffic))
        unique_destinations = len(set(t.get('dest_ip', '') for t in recent_traffic))
        
        # Protocol distribution
        protocol_dist = {}
        for t in recent_traffic:
            protocol = t.get('protocol', 'UNKNOWN')
            protocol_dist[protocol] = protocol_dist.get(protocol, 0) + 1
        
        # Geographic distribution
        geographic_dist = {}
        for t in recent_traffic:
            country = self._get_country_from_ip(t.get('source_ip', ''))
            geographic_dist[country] = geographic_dist.get(country, 0) + 1
        
        return {
            'time_window': time_window,
            'total_packets': total_packets,
            'total_bytes': total_bytes,
            'unique_sources': unique_sources,
            'unique_destinations': unique_destinations,
            'protocol_distribution': protocol_dist,
            'geographic_distribution': geographic_dist,
            'anomalies_detected': sum(1 for t in recent_traffic if t.get('anomalies_detected')),
            'average_packet_size': total_bytes / total_packets if total_packets > 0 else 0
        }
