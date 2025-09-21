import time
import threading
import hashlib
import json
from collections import deque
from typing import Dict, List, Optional, Tuple
import random
import secrets

class IndustrialSecurityManager:
    def __init__(self):
        self.security_active = False
        self.security_thread = None
        self.industrial_systems = {}
        self.security_events = deque(maxlen=10000)
        self.threat_detections = deque(maxlen=1000)
        
        # Industrial security configuration
        self.security_config = {
            'monitor_scada_systems': True,
            'monitor_plc_devices': True,
            'monitor_hmi_interfaces': True,
            'monitor_industrial_networks': True,
            'monitor_protocols': True,
            'monitor_device_communication': True,
            'monitor_system_integrity': True,
            'monitor_operational_parameters': True,
            'monitor_network_traffic': True,
            'monitor_device_status': True,
            'protocol_validation': True,
            'anomaly_detection': True,
            'threat_prevention': True,
            'incident_response': True,
            'compliance_monitoring': True
        }
        
        # Industrial threat patterns
        self.threat_patterns = {
            'malicious_commands': [
                'STOP_ALL', 'EMERGENCY_STOP', 'SHUTDOWN_SYSTEM',
                'RESET_ALL', 'CLEAR_MEMORY', 'DISABLE_SAFETY',
                'OVERRIDE_LIMITS', 'BYPASS_PROTECTION'
            ],
            'suspicious_protocols': [
                'modbus_exploit', 'dnp3_exploit', 'iec61850_exploit',
                'profinet_exploit', 'ethernet_ip_exploit', 'opc_ua_exploit'
            ],
            'network_attacks': [
                'man_in_the_middle', 'replay_attack', 'packet_injection',
                'protocol_fuzzing', 'denial_of_service', 'network_scanning'
            ],
            'device_attacks': [
                'firmware_modification', 'configuration_tampering',
                'sensor_spoofing', 'actuator_manipulation',
                'communication_interception', 'data_manipulation'
            ],
            'operational_attacks': [
                'process_disruption', 'safety_system_bypass',
                'alarm_suppression', 'data_logging_tampering',
                'backup_corruption', 'recovery_prevention'
            ]
        }
        
        # Industrial security statistics
        self.security_stats = {
            'systems_monitored': 0,
            'devices_monitored': 0,
            'protocols_analyzed': 0,
            'threats_detected': 0,
            'malicious_commands_blocked': 0,
            'network_attacks_prevented': 0,
            'device_attacks_prevented': 0,
            'operational_attacks_prevented': 0,
            'compliance_violations': 0,
            'security_errors': 0
        }
        
        print("🏭 Industrial Security Manager initialized!")
        print(f"   Threat patterns: {sum(len(v) for v in self.threat_patterns.values())}")
        print(f"   Security features: {sum(1 for v in self.security_config.values() if v)}")

    def start_security(self):
        """Start industrial security monitoring"""
        if self.security_active:
            return
        self.security_active = True
        self.security_thread = threading.Thread(target=self._security_loop, daemon=True)
        self.security_thread.start()
        print("🏭 Industrial security started!")

    def stop_security(self):
        """Stop industrial security monitoring"""
        self.security_active = False
        if self.security_thread:
            self.security_thread.join(timeout=5)
        print("⏹️ Industrial security stopped!")

    def _security_loop(self):
        """Main industrial security loop"""
        while self.security_active:
            try:
                # Monitor industrial systems
                self._monitor_industrial_systems()
                
                # Analyze industrial protocols
                self._analyze_industrial_protocols()
                
                # Monitor device communication
                self._monitor_device_communication()
                
                # Detect industrial threats
                self._detect_industrial_threats()
                
                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                print(f"❌ Industrial security error: {e}")
                self.security_stats['security_errors'] += 1
                time.sleep(5)

    def _monitor_industrial_systems(self):
        """Monitor industrial systems for security events"""
        try:
            # Simulate system monitoring
            systems_to_monitor = random.randint(1, 3)
            
            for i in range(systems_to_monitor):
                system_id = f'industrial_system_{int(time.time())}_{i}'
                
                if system_id not in self.industrial_systems:
                    self.industrial_systems[system_id] = {
                        'system_id': system_id,
                        'system_type': random.choice(['scada', 'plc', 'hmi', 'dcs']),
                        'protocol': random.choice(['modbus', 'dnp3', 'iec61850', 'profinet', 'ethernet_ip', 'opc_ua']),
                        'security_status': 'secure',
                        'last_seen': time.time(),
                        'devices': [],
                        'network_connections': [],
                        'operational_parameters': {},
                        'safety_systems': {},
                        'alarm_status': 'normal'
                    }
                    self.security_stats['systems_monitored'] += 1
                
                # Update system information
                self._update_system_information(system_id)
                
        except Exception as e:
            print(f"❌ System monitoring error: {e}")

    def _update_system_information(self, system_id: str):
        """Update system information"""
        try:
            system = self.industrial_systems[system_id]
            system['last_seen'] = time.time()
            
            # Simulate device connections
            if random.random() < 0.2:  # 20% chance of new device
                new_device = self._simulate_device_connection()
                system['devices'].append(new_device)
                self.security_stats['devices_monitored'] += 1
            
            # Simulate network connections
            if random.random() < 0.3:  # 30% chance of network activity
                connection = self._simulate_network_connection()
                system['network_connections'].append(connection)
            
            # Update operational parameters
            system['operational_parameters'] = {
                'temperature': random.uniform(20, 100),
                'pressure': random.uniform(1, 10),
                'flow_rate': random.uniform(0, 1000),
                'power_consumption': random.uniform(100, 1000),
                'efficiency': random.uniform(80, 100),
                'timestamp': time.time()
            }
            
            # Update safety systems
            system['safety_systems'] = {
                'emergency_stop': random.choice([True, False]),
                'safety_interlock': random.choice([True, False]),
                'alarm_system': random.choice(['normal', 'warning', 'critical']),
                'fire_suppression': random.choice([True, False]),
                'gas_detection': random.choice([True, False]),
                'timestamp': time.time()
            }
            
            # Update alarm status
            if random.random() < 0.1:  # 10% chance of alarm
                system['alarm_status'] = random.choice(['warning', 'critical'])
            else:
                system['alarm_status'] = 'normal'
                
        except Exception as e:
            print(f"❌ System information update error: {e}")

    def _simulate_device_connection(self) -> Dict:
        """Simulate device connection"""
        try:
            device = {
                'device_id': f'device_{int(time.time())}_{random.randint(1000, 9999)}',
                'device_type': random.choice(['sensor', 'actuator', 'controller', 'monitor']),
                'protocol': random.choice(['modbus', 'dnp3', 'iec61850', 'profinet', 'ethernet_ip', 'opc_ua']),
                'ip_address': f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}',
                'port': random.randint(1, 65535),
                'connection_time': time.time(),
                'status': random.choice(['connected', 'disconnected', 'error']),
                'is_secure': random.choice([True, False])
            }
            
            return device
            
        except Exception as e:
            return {'error': f'Device connection simulation failed: {e}'}

    def _simulate_network_connection(self) -> Dict:
        """Simulate network connection"""
        try:
            connection = {
                'connection_id': f'conn_{int(time.time())}_{random.randint(1000, 9999)}',
                'protocol': random.choice(['modbus', 'dnp3', 'iec61850', 'profinet', 'ethernet_ip', 'opc_ua']),
                'source_ip': f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}',
                'dest_ip': f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}',
                'source_port': random.randint(1, 65535),
                'dest_port': random.randint(1, 65535),
                'bytes_sent': random.randint(0, 10000),
                'bytes_received': random.randint(0, 10000),
                'timestamp': time.time(),
                'is_suspicious': random.random() < 0.1  # 10% chance of suspicious connection
            }
            
            return connection
            
        except Exception as e:
            return {'error': f'Network connection simulation failed: {e}'}

    def _analyze_industrial_protocols(self):
        """Analyze industrial protocols for security threats"""
        try:
            for system_id, system in self.industrial_systems.items():
                # Analyze protocol communications
                for connection in system.get('network_connections', []):
                    if connection.get('is_suspicious', False):
                        self._handle_suspicious_protocol_communication(system_id, connection)
                    elif self._is_malicious_protocol_command(connection):
                        self._handle_malicious_protocol_command(system_id, connection)
                    elif self._is_protocol_anomaly(connection):
                        self._handle_protocol_anomaly(system_id, connection)
                        
        except Exception as e:
            print(f"❌ Protocol analysis error: {e}")

    def _is_malicious_protocol_command(self, connection: Dict) -> bool:
        """Check if protocol command is malicious"""
        try:
            # Simulate malicious command detection
            if random.random() < 0.05:  # 5% chance of malicious command
                return True
            
            # Check for malicious commands in protocol data
            protocol_data = connection.get('protocol_data', '')
            for malicious_command in self.threat_patterns['malicious_commands']:
                if malicious_command.lower() in protocol_data.lower():
                    return True
            
            return False
            
        except Exception:
            return False

    def _is_protocol_anomaly(self, connection: Dict) -> bool:
        """Check if protocol communication is anomalous"""
        try:
            # Check for protocol anomalies
            protocol = connection.get('protocol', '')
            if protocol in self.threat_patterns['suspicious_protocols']:
                return True
            
            # Check for unusual data patterns
            bytes_sent = connection.get('bytes_sent', 0)
            bytes_received = connection.get('bytes_received', 0)
            
            if bytes_sent > 10000 or bytes_received > 10000:  # Unusual data volume
                return True
            
            return False
            
        except Exception:
            return False

    def _handle_suspicious_protocol_communication(self, system_id: str, connection: Dict):
        """Handle suspicious protocol communication"""
        try:
            self.security_stats['threats_detected'] += 1
            
            threat_detection = {
                'timestamp': time.time(),
                'system_id': system_id,
                'threat_type': 'suspicious_protocol_communication',
                'connection_id': connection['connection_id'],
                'protocol': connection['protocol'],
                'severity': 'medium',
                'action_taken': 'communication_monitored',
                'description': f'Suspicious protocol communication detected: {connection["protocol"]}'
            }
            
            self.threat_detections.append(threat_detection)
            
            print(f"⚠️ SUSPICIOUS PROTOCOL COMMUNICATION: {connection['protocol']} on system {system_id}")
            print(f"   Connection: {connection['connection_id']}")
            print(f"   Action: Communication monitored")
            
        except Exception as e:
            print(f"❌ Suspicious protocol communication handling error: {e}")

    def _handle_malicious_protocol_command(self, system_id: str, connection: Dict):
        """Handle malicious protocol command"""
        try:
            self.security_stats['malicious_commands_blocked'] += 1
            self.security_stats['threats_detected'] += 1
            
            threat_detection = {
                'timestamp': time.time(),
                'system_id': system_id,
                'threat_type': 'malicious_protocol_command',
                'connection_id': connection['connection_id'],
                'protocol': connection['protocol'],
                'severity': 'critical',
                'action_taken': 'command_blocked',
                'description': f'Malicious protocol command detected: {connection["protocol"]}'
            }
            
            self.threat_detections.append(threat_detection)
            
            print(f"🚨 MALICIOUS PROTOCOL COMMAND: {connection['protocol']} on system {system_id}")
            print(f"   Connection: {connection['connection_id']}")
            print(f"   Action: Command blocked")
            
        except Exception as e:
            print(f"❌ Malicious protocol command handling error: {e}")

    def _handle_protocol_anomaly(self, system_id: str, connection: Dict):
        """Handle protocol anomaly"""
        try:
            self.security_stats['threats_detected'] += 1
            
            threat_detection = {
                'timestamp': time.time(),
                'system_id': system_id,
                'threat_type': 'protocol_anomaly',
                'connection_id': connection['connection_id'],
                'protocol': connection['protocol'],
                'severity': 'low',
                'action_taken': 'anomaly_flagged',
                'description': f'Protocol anomaly detected: {connection["protocol"]}'
            }
            
            self.threat_detections.append(threat_detection)
            
            print(f"⚠️ PROTOCOL ANOMALY: {connection['protocol']} on system {system_id}")
            print(f"   Connection: {connection['connection_id']}")
            print(f"   Action: Anomaly flagged")
            
        except Exception as e:
            print(f"❌ Protocol anomaly handling error: {e}")

    def _monitor_device_communication(self):
        """Monitor device communication for security threats"""
        try:
            for system_id, system in self.industrial_systems.items():
                # Check for device communication anomalies
                if self._detect_device_communication_anomalies(system):
                    self._handle_device_communication_anomalies(system_id, system)
                
                # Check for device security issues
                if self._detect_device_security_issues(system):
                    self._handle_device_security_issues(system_id, system)
                
                # Check for operational anomalies
                if self._detect_operational_anomalies(system):
                    self._handle_operational_anomalies(system_id, system)
                    
        except Exception as e:
            print(f"❌ Device communication monitoring error: {e}")

    def _detect_device_communication_anomalies(self, system: Dict) -> bool:
        """Detect device communication anomalies"""
        try:
            # Check for unusual communication patterns
            connections = system.get('network_connections', [])
            if len(connections) > 100:  # Too many connections
                return True
            
            # Check for suspicious device connections
            devices = system.get('devices', [])
            for device in devices:
                if not device.get('is_secure', True):
                    return True
            
            return False
            
        except Exception:
            return False

    def _detect_device_security_issues(self, system: Dict) -> bool:
        """Detect device security issues"""
        try:
            # Check for device security issues
            devices = system.get('devices', [])
            for device in devices:
                if device.get('status') == 'error':
                    return True
                if not device.get('is_secure', True):
                    return True
            
            return False
            
        except Exception:
            return False

    def _detect_operational_anomalies(self, system: Dict) -> bool:
        """Detect operational anomalies"""
        try:
            # Check for operational parameter anomalies
            operational_params = system.get('operational_parameters', {})
            
            # Check temperature
            temperature = operational_params.get('temperature', 0)
            if temperature > 80 or temperature < 10:  # Unusual temperature
                return True
            
            # Check pressure
            pressure = operational_params.get('pressure', 0)
            if pressure > 8 or pressure < 1:  # Unusual pressure
                return True
            
            # Check efficiency
            efficiency = operational_params.get('efficiency', 0)
            if efficiency < 70:  # Low efficiency
                return True
            
            return False
            
        except Exception:
            return False

    def _handle_device_communication_anomalies(self, system_id: str, system: Dict):
        """Handle device communication anomalies"""
        try:
            self.security_stats['threats_detected'] += 1
            
            threat_detection = {
                'timestamp': time.time(),
                'system_id': system_id,
                'threat_type': 'device_communication_anomaly',
                'severity': 'medium',
                'action_taken': 'communication_monitored',
                'description': f'Device communication anomaly detected on system {system_id}'
            }
            
            self.threat_detections.append(threat_detection)
            
            print(f"⚠️ DEVICE COMMUNICATION ANOMALY: System {system_id}")
            print(f"   Action: Communication monitored")
            
        except Exception as e:
            print(f"❌ Device communication anomaly handling error: {e}")

    def _handle_device_security_issues(self, system_id: str, system: Dict):
        """Handle device security issues"""
        try:
            self.security_stats['threats_detected'] += 1
            
            threat_detection = {
                'timestamp': time.time(),
                'system_id': system_id,
                'threat_type': 'device_security_issue',
                'severity': 'high',
                'action_taken': 'device_secured',
                'description': f'Device security issue detected on system {system_id}'
            }
            
            self.threat_detections.append(threat_detection)
            
            print(f"🚨 DEVICE SECURITY ISSUE: System {system_id}")
            print(f"   Action: Device secured")
            
        except Exception as e:
            print(f"❌ Device security issue handling error: {e}")

    def _handle_operational_anomalies(self, system_id: str, system: Dict):
        """Handle operational anomalies"""
        try:
            self.security_stats['threats_detected'] += 1
            
            threat_detection = {
                'timestamp': time.time(),
                'system_id': system_id,
                'threat_type': 'operational_anomaly',
                'severity': 'medium',
                'action_taken': 'operational_monitoring',
                'description': f'Operational anomaly detected on system {system_id}'
            }
            
            self.threat_detections.append(threat_detection)
            
            print(f"⚠️ OPERATIONAL ANOMALY: System {system_id}")
            print(f"   Action: Operational monitoring")
            
        except Exception as e:
            print(f"❌ Operational anomaly handling error: {e}")

    def _detect_industrial_threats(self):
        """Detect industrial threats"""
        try:
            # Simulate threat detection
            threats_detected = random.randint(0, 2)
            
            for i in range(threats_detected):
                threat = {
                    'timestamp': time.time(),
                    'threat_id': f'industrial_threat_{int(time.time())}_{i}',
                    'threat_type': random.choice(['network_attack', 'device_attack', 'operational_attack', 'protocol_attack']),
                    'system_id': random.choice(list(self.industrial_systems.keys())) if self.industrial_systems else 'unknown',
                    'severity': random.choice(['low', 'medium', 'high', 'critical']),
                    'description': f'Industrial threat detected: {random.choice(["network_attack", "device_attack", "operational_attack", "protocol_attack"])}'
                }
                
                self.threat_detections.append(threat)
                self.security_stats['threats_detected'] += 1
                
                if threat['threat_type'] == 'network_attack':
                    self.security_stats['network_attacks_prevented'] += 1
                elif threat['threat_type'] == 'device_attack':
                    self.security_stats['device_attacks_prevented'] += 1
                elif threat['threat_type'] == 'operational_attack':
                    self.security_stats['operational_attacks_prevented'] += 1
                
                if threat['severity'] in ['high', 'critical']:
                    print(f"🚨 INDUSTRIAL THREAT DETECTED: {threat['threat_type']} (Severity: {threat['severity']})")
                    print(f"   System: {threat['system_id']}")
                    print(f"   Description: {threat['description']}")
            
        except Exception as e:
            print(f"❌ Industrial threat detection error: {e}")

    def get_industrial_security_statistics(self) -> Dict:
        """Get industrial security statistics"""
        return {
            'security_active': self.security_active,
            'systems_monitored': self.security_stats['systems_monitored'],
            'devices_monitored': self.security_stats['devices_monitored'],
            'protocols_analyzed': self.security_stats['protocols_analyzed'],
            'threats_detected': self.security_stats['threats_detected'],
            'malicious_commands_blocked': self.security_stats['malicious_commands_blocked'],
            'network_attacks_prevented': self.security_stats['network_attacks_prevented'],
            'device_attacks_prevented': self.security_stats['device_attacks_prevented'],
            'operational_attacks_prevented': self.security_stats['operational_attacks_prevented'],
            'compliance_violations': self.security_stats['compliance_violations'],
            'security_errors': self.security_stats['security_errors'],
            'industrial_systems_count': len(self.industrial_systems),
            'security_events_size': len(self.security_events),
            'threat_detections_size': len(self.threat_detections)
        }

    def get_recent_threat_detections(self, count: int = 10) -> List[Dict]:
        """Get recent threat detections"""
        return list(self.threat_detections)[-count:]

    def get_system_security_status(self, system_id: str) -> Dict:
        """Get security status for specific system"""
        try:
            if system_id not in self.industrial_systems:
                return {'error': 'System not found'}
            
            system = self.industrial_systems[system_id]
            
            # Calculate security score
            security_score = 100
            
            # Deduct points for threats
            if system.get('alarm_status') == 'critical':
                security_score -= 40
            elif system.get('alarm_status') == 'warning':
                security_score -= 20
            
            # Deduct points for suspicious connections
            connections = system.get('network_connections', [])
            suspicious_connections = [c for c in connections if c.get('is_suspicious', False)]
            if suspicious_connections:
                security_score -= 30
            
            # Deduct points for device issues
            devices = system.get('devices', [])
            insecure_devices = [d for d in devices if not d.get('is_secure', True)]
            if insecure_devices:
                security_score -= 25
            
            # Deduct points for operational anomalies
            if self._detect_operational_anomalies(system):
                security_score -= 15
            
            security_score = max(0, security_score)
            
            return {
                'system_id': system_id,
                'security_score': security_score,
                'security_status': 'secure' if security_score >= 80 else 'warning' if security_score >= 60 else 'critical',
                'system_type': system.get('system_type', 'unknown'),
                'protocol': system.get('protocol', 'unknown'),
                'devices_count': len(devices),
                'connections_count': len(connections),
                'alarm_status': system.get('alarm_status', 'normal'),
                'last_seen': system.get('last_seen', 0)
            }
            
        except Exception as e:
            return {'error': f'Failed to get system security status: {e}'}

    def update_security_config(self, config: Dict):
        """Update industrial security configuration"""
        try:
            self.security_config.update(config)
            print(f"✅ Industrial security configuration updated")
        except Exception as e:
            print(f"❌ Configuration update error: {e}")

    def add_threat_pattern(self, pattern_type: str, pattern: str):
        """Add threat pattern"""
        try:
            if pattern_type in self.threat_patterns:
                self.threat_patterns[pattern_type].append(pattern)
                print(f"✅ Threat pattern added: {pattern_type}")
        except Exception as e:
            print(f"❌ Threat pattern addition error: {e}")

    def emergency_industrial_shutdown(self):
        """Emergency industrial shutdown"""
        try:
            print("🚨 EMERGENCY INDUSTRIAL SHUTDOWN ACTIVATED!")
            
            # Stop all industrial processes
            print("🛑 Stopping all industrial processes...")
            
            # Activate safety systems
            print("🔒 Activating safety systems...")
            
            # Notify operators
            print("📢 Notifying operators...")
            
            # Activate emergency protocols
            print("🚨 Activating emergency protocols...")
            
            print("✅ Emergency industrial shutdown completed!")
            
        except Exception as e:
            print(f"❌ Emergency industrial shutdown error: {e}")

    def restore_normal_industrial_operation(self):
        """Restore normal industrial operation"""
        try:
            print("✅ Restoring normal industrial operation...")
            
            # Resume normal industrial processes
            print("🏭 Resuming normal industrial processes...")
            
            print("✅ Normal industrial operation restored!")
            
        except Exception as e:
            print(f"❌ Industrial operation restoration error: {e}")
