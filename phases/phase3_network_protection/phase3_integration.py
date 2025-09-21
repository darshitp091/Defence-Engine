import time
import threading
from typing import Dict, List, Optional
from datetime import datetime

# Import Phase 3 components
from phases.phase3_network_protection.ddos_mitigation.ddos_protection import DDoSProtectionEngine
from phases.phase3_network_protection.traffic_analysis.traffic_analyzer import AdvancedTrafficAnalyzer
from phases.phase3_network_protection.network_monitoring.network_monitor import NetworkMonitor
from phases.phase3_network_protection.protocol_validation.protocol_validator import ProtocolValidator
from phases.phase3_network_protection.firewall_management.dynamic_firewall import DynamicFirewallManager

class Phase3Integration:
    def __init__(self):
        self.ddos_protection = DDoSProtectionEngine()
        self.traffic_analyzer = AdvancedTrafficAnalyzer()
        self.network_monitor = NetworkMonitor()
        self.protocol_validator = ProtocolValidator()
        self.firewall_manager = DynamicFirewallManager()
        
        print("✅ Phase 3 Network Protection initialized!")
        print("   - DDoS Mitigation Engine")
        print("   - Advanced Traffic Analysis")
        print("   - Network Monitoring")
        print("   - Protocol Validation")
        print("   - Dynamic Firewall Management")

    def start_phase3_protection(self):
        print("\n🌐 Starting Phase 3 Network Protection Components...")
        
        print("   🛡️ Starting DDoS Protection...")
        self.ddos_protection.start_protection()
        
        print("   📊 Starting Traffic Analysis...")
        self.traffic_analyzer.start_analysis()
        
        print("   🔍 Starting Network Monitoring...")
        self.network_monitor.start_monitoring()
        
        print("   ✅ Starting Protocol Validation...")
        self.protocol_validator.start_validation()
        
        print("   🔥 Starting Dynamic Firewall...")
        self.firewall_manager.start_firewall()
        
        print("✅ Phase 3 Network Protection Active!")
        print("   - DDoS Protection: ACTIVE")
        print("   - Traffic Analysis: ACTIVE")
        print("   - Network Monitoring: ACTIVE")
        print("   - Protocol Validation: ACTIVE")
        print("   - Dynamic Firewall: ACTIVE")

    def stop_phase3_protection(self):
        print("\n⏹️ Stopping Phase 3 Network Protection Components...")
        
        self.ddos_protection.stop_protection()
        self.traffic_analyzer.stop_analysis()
        self.network_monitor.stop_monitoring()
        self.protocol_validator.stop_validation()
        self.firewall_manager.stop_firewall()
        
        print("✅ Phase 3 Network Protection Stopped!")

    def get_phase3_report(self) -> Dict:
        """Get comprehensive Phase 3 protection report"""
        ddos_stats = self.ddos_protection.get_protection_statistics()
        traffic_stats = self.traffic_analyzer.get_analysis_statistics()
        network_stats = self.network_monitor.get_monitoring_statistics()
        protocol_stats = self.protocol_validator.get_validation_statistics()
        firewall_stats = self.firewall_manager.get_firewall_statistics()
        
        # Calculate overall network health
        network_health = 100
        if ddos_stats.get('attacks_blocked', 0) > 0:
            network_health -= 10
        if traffic_stats.get('anomalies_detected', 0) > 0:
            network_health -= 15
        if network_stats.get('connection_issues', 0) > 0:
            network_health -= 20
        if protocol_stats.get('invalid_packets', 0) > 0:
            network_health -= 5
        
        network_health = max(0, network_health)
        
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'network_health': network_health,
            'ddos_protection': ddos_stats,
            'traffic_analysis': traffic_stats,
            'network_monitoring': network_stats,
            'protocol_validation': protocol_stats,
            'firewall_management': firewall_stats,
            'total_threats_blocked': (
                ddos_stats.get('attacks_blocked', 0) +
                firewall_stats.get('threats_blocked', 0)
            ),
            'total_anomalies_detected': traffic_stats.get('anomalies_detected', 0),
            'active_protections': sum([
                ddos_stats.get('protection_active', False),
                traffic_stats.get('analysis_active', False),
                network_stats.get('monitoring_active', False),
                protocol_stats.get('validation_active', False),
                firewall_stats.get('is_active', False)
            ])
        }

    def test_phase3_components(self):
        print("\n🧪 TESTING PHASE 3 COMPONENTS")
        print("============================================================")
        
        # Test DDoS Protection
        print("🛡️ Testing DDoS Protection...")
        test_attack = {
            'source_ip': '192.168.1.100',
            'target_ip': '192.168.1.1',
            'packet_count': 1000,
            'attack_type': 'SYN_FLOOD',
            'timestamp': time.time()
        }
        ddos_response = self.ddos_protection.analyze_traffic(test_attack)
        print(f"   ✅ DDoS Analysis: {ddos_response['threat_level']}/100")
        
        # Test Traffic Analysis
        print("📊 Testing Traffic Analysis...")
        test_traffic = {
            'source_ip': '10.0.0.1',
            'destination_ip': '10.0.0.2',
            'protocol': 'TCP',
            'port': 80,
            'packet_size': 1024,
            'timestamp': time.time()
        }
        traffic_analysis = self.traffic_analyzer.analyze_packet(test_traffic)
        print(f"   ✅ Traffic Analysis: {traffic_analysis['anomaly_score']}/100")
        
        # Test Network Monitoring
        print("🔍 Testing Network Monitoring...")
        network_stats = self.network_monitor.get_monitoring_statistics()
        print(f"   ✅ Network Monitoring: {network_stats['monitoring_active']}")
        
        # Test Protocol Validation
        print("✅ Testing Protocol Validation...")
        test_packet = {
            'source_ip': '192.168.1.50',
            'destination_ip': '192.168.1.1',
            'protocol': 'TCP',
            'port': 443,
            'data': b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n',
            'timestamp': time.time()
        }
        protocol_validation = self.protocol_validator.validate_packet(test_packet)
        print(f"   ✅ Protocol Validation: {protocol_validation['is_valid']}")
        
        # Test Firewall Management
        print("🔥 Testing Firewall Management...")
        firewall_stats = self.firewall_manager.get_firewall_statistics()
        print(f"   ✅ Firewall Active: {firewall_stats['is_active']}")
        print(f"   ✅ Active Rules: {firewall_stats['active_rules']}")
        
        print("✅ Phase 3 Component Testing Completed!")
        print("============================================================")

    def simulate_network_attack(self):
        """Simulate various network attacks for testing"""
        print("\n🎯 SIMULATING NETWORK ATTACKS FOR TESTING")
        print("============================================================")
        
        # Simulate DDoS attack
        print("🛡️ Simulating DDoS Attack...")
        for i in range(10):
            attack_packet = {
                'source_ip': f'192.168.1.{100 + i}',
                'target_ip': '192.168.1.1',
                'packet_count': 1000,
                'attack_type': 'SYN_FLOOD',
                'timestamp': time.time()
            }
            response = self.ddos_protection.analyze_traffic(attack_packet)
            print(f"   Attack {i+1}: Threat Level {response['threat_level']}/100")
        
        # Simulate suspicious traffic
        print("📊 Simulating Suspicious Traffic...")
        for i in range(5):
            suspicious_packet = {
                'source_ip': f'10.0.0.{10 + i}',
                'destination_ip': '10.0.0.1',
                'protocol': 'TCP',
                'port': 22,
                'packet_size': 1500,
                'timestamp': time.time()
            }
            analysis = self.traffic_analyzer.analyze_packet(suspicious_packet)
            print(f"   Traffic {i+1}: Anomaly Score {analysis['anomaly_score']}/100")
        
        # Simulate protocol violations
        print("✅ Simulating Protocol Violations...")
        for i in range(3):
            invalid_packet = {
                'source_ip': f'172.16.0.{20 + i}',
                'destination_ip': '172.16.0.1',
                'protocol': 'TCP',
                'port': 80,
                'data': b'INVALID_PROTOCOL_DATA',
                'timestamp': time.time()
            }
            validation = self.protocol_validator.validate_packet(invalid_packet)
            print(f"   Packet {i+1}: Valid = {validation['is_valid']}")
        
        print("✅ Network Attack Simulation Completed!")
        print("============================================================")

def main():
    print("🌐 PHASE 3 - NETWORK PROTECTION TESTING")
    print("============================================================")
    
    print("🌐 PHASE 3 - NETWORK PROTECTION INITIALIZATION")
    print("============================================================")
    
    phase3 = Phase3Integration()
    phase3.test_phase3_components()
    
    phase3.start_phase3_protection()
    print("\n⏱️ Running Phase 3 protection for 30 seconds...")
    time.sleep(30)
    
    phase3.simulate_network_attack()
    
    phase3.stop_phase3_protection()
    
    report = phase3.get_phase3_report()
    print("\n📊 PHASE 3 INTEGRATION REPORT", report['timestamp'])
    print("============================================================")
    print(f"🌐 Network Health: {report['network_health']}/100")
    print(f"🛡️ DDoS Attacks Blocked: {report['ddos_protection']['attacks_blocked']}")
    print(f"📊 Traffic Anomalies Detected: {report['traffic_analysis']['anomalies_detected']}")
    print(f"🔍 Network Issues: {report['network_monitoring']['connection_issues']}")
    print(f"✅ Protocol Violations: {report['protocol_validation']['invalid_packets']}")
    print(f"🔥 Firewall Rules: {report['firewall_management']['active_rules']}")
    print(f"🚨 Total Threats Blocked: {report['total_threats_blocked']}")
    print(f"⚠️ Total Anomalies Detected: {report['total_anomalies_detected']}")
    print(f"🔒 Active Protections: {report['active_protections']}/5")
    print("============================================================")
    
    print("\n📊 PHASE 3 STATISTICS:")
    print(f"   DDoS Protection: {report['ddos_protection']['protection_active']}")
    print(f"   Traffic Analysis: {report['traffic_analysis']['analysis_active']}")
    print(f"   Network Monitoring: {report['network_monitoring']['monitoring_active']}")
    print(f"   Protocol Validation: {report['protocol_validation']['validation_active']}")
    print(f"   Firewall Management: {report['firewall_management']['is_active']}")
    
    print("\n✅ Phase 3 Network Protection Testing Completed!")
    print("============================================================")

if __name__ == "__main__":
    main()
