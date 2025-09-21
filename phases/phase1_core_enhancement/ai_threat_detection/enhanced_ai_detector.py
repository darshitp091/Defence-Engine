"""
Enhanced AI Threat Detection System
Advanced machine learning-based threat detection with real-time analysis
"""
import time
import threading
import psutil
import numpy as np
import json
import requests
from typing import Dict, List, Optional, Tuple
from collections import deque
import hashlib
import secrets
from datetime import datetime, timedelta
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# AI/ML imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from sklearn.ensemble import IsolationForest, RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import DBSCAN
    from sklearn.neural_network import MLPClassifier
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class EnhancedNeuralThreatAnalyzer:
    """Enhanced Neural Network-based Threat Analysis with Deep Learning"""
    
    def __init__(self):
        self.threat_patterns = deque(maxlen=50000)  # Increased capacity
        self.normal_patterns = deque(maxlen=50000)
        self.anomaly_detector = None
        self.scaler = None
        self.is_trained = False
        
        # Enhanced ML models
        self.isolation_forest = None
        self.random_forest = None
        self.neural_network = None
        self.dbscan_cluster = None
        
        if SKLEARN_AVAILABLE:
            self.isolation_forest = IsolationForest(
                contamination=0.05,  # Reduced contamination for better precision
                random_state=42,
                n_estimators=200
            )
            self.random_forest = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=20
            )
            self.neural_network = MLPClassifier(
                hidden_layer_sizes=(100, 50, 25),
                random_state=42,
                max_iter=1000
            )
            self.dbscan_cluster = DBSCAN(eps=0.5, min_samples=5)
            self.scaler = StandardScaler()
        
        # Threat intelligence
        self.threat_intelligence = {
            'known_threats': set(),
            'threat_signatures': {},
            'attack_patterns': {},
            'malicious_ips': set(),
            'suspicious_domains': set()
        }
        
        print("🧠 Enhanced Neural Threat Analyzer initialized!")
        print(f"   ML Models: {len([m for m in [self.isolation_forest, self.random_forest, self.neural_network] if m is not None])}")
        print(f"   Pattern capacity: {self.threat_patterns.maxlen}")
    
    def extract_enhanced_features(self, system_data: Dict) -> np.ndarray:
        """Extract enhanced features for deep learning analysis"""
        features = []
        
        # System performance features
        features.extend([
            system_data.get('cpu_percent', 0),
            system_data.get('cpu_count', 1),
            system_data.get('cpu_freq', 0),
            system_data.get('memory_percent', 0),
            system_data.get('memory_available', 0),
            system_data.get('memory_used', 0),
            system_data.get('disk_usage_percent', 0)
        ])
        
        # Network features
        features.extend([
            system_data.get('network_bytes_sent', 0),
            system_data.get('network_bytes_recv', 0),
            system_data.get('network_packets_sent', 0),
            system_data.get('network_packets_recv', 0)
        ])
        
        # Process features
        features.extend([
            system_data.get('process_count', 0),
            system_data.get('thread_count', 0),
            system_data.get('file_descriptors', 0)
        ])
        
        # Security features
        features.extend([
            system_data.get('suspicious_connections', 0),
            system_data.get('failed_logins', 0),
            system_data.get('privilege_escalations', 0),
            system_data.get('file_modifications', 0)
        ])
        
        # Time-based features
        current_time = time.time()
        features.extend([
            current_time % 86400,  # Time of day
            current_time % 604800,  # Day of week
            current_time % 31536000  # Day of year
        ])
        
        return np.array(features, dtype=np.float32)
    
    def train_enhanced_models(self):
        """Train enhanced ML models with multiple algorithms"""
        if not SKLEARN_AVAILABLE or len(self.normal_patterns) < 1000:
            return False
        
        try:
            print("🧠 Training enhanced ML models...")
            
            # Prepare training data
            normal_data = [self.extract_enhanced_features(pattern) for pattern in self.normal_patterns]
            threat_data = [self.extract_enhanced_features(pattern) for pattern in self.threat_patterns]
            
            # Combine and scale data
            all_data = normal_data + threat_data
            X = np.array(all_data)
            X_scaled = self.scaler.fit_transform(X)
            
            # Create labels (0 for normal, 1 for threat)
            y = np.array([0] * len(normal_data) + [1] * len(threat_data))
            
            # Train Isolation Forest
            self.isolation_forest.fit(X_scaled)
            
            # Train Random Forest
            self.random_forest.fit(X_scaled, y)
            
            # Train Neural Network
            self.neural_network.fit(X_scaled, y)
            
            # Train DBSCAN for clustering
            self.dbscan_cluster.fit(X_scaled)
            
            self.is_trained = True
            print("✅ Enhanced ML models trained successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Enhanced model training failed: {e}")
            return False
    
    def detect_enhanced_anomaly(self, system_data: Dict) -> Tuple[bool, float, Dict]:
        """Detect anomalies using enhanced ML models"""
        if not self.is_trained:
            return False, 0.0, {}
        
        try:
            features = self.extract_enhanced_features(system_data)
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            
            # Multiple model predictions
            isolation_score = self.isolation_forest.decision_function(features_scaled)[0]
            isolation_anomaly = self.isolation_forest.predict(features_scaled)[0] == -1
            
            # Random Forest prediction
            rf_probability = self.random_forest.predict_proba(features_scaled)[0][1]
            
            # Neural Network prediction
            nn_probability = self.neural_network.predict_proba(features_scaled)[0][1]
            
            # DBSCAN clustering
            cluster_label = self.dbscan_cluster.fit_predict(features_scaled)[0]
            is_outlier = cluster_label == -1
            
            # Combine predictions
            anomaly_score = (abs(isolation_score) + rf_probability + nn_probability) / 3
            is_anomaly = isolation_anomaly or rf_probability > 0.7 or nn_probability > 0.7 or is_outlier
            
            # Detailed analysis
            analysis = {
                'isolation_score': float(isolation_score),
                'isolation_anomaly': bool(isolation_anomaly),
                'random_forest_probability': float(rf_probability),
                'neural_network_probability': float(nn_probability),
                'cluster_label': int(cluster_label),
                'is_outlier': bool(is_outlier),
                'combined_score': float(anomaly_score)
            }
            
            return is_anomaly, anomaly_score, analysis
            
        except Exception as e:
            print(f"❌ Enhanced anomaly detection error: {e}")
            return False, 0.0, {}
    
    def add_threat_intelligence(self, threat_data: Dict):
        """Add threat intelligence data"""
        if 'ip_address' in threat_data:
            self.threat_intelligence['malicious_ips'].add(threat_data['ip_address'])
        
        if 'domain' in threat_data:
            self.threat_intelligence['suspicious_domains'].add(threat_data['domain'])
        
        if 'signature' in threat_data:
            self.threat_intelligence['threat_signatures'][threat_data['signature']] = threat_data
    
    def get_threat_intelligence(self) -> Dict:
        """Get current threat intelligence"""
        return {
            'known_threats': len(self.threat_intelligence['known_threats']),
            'threat_signatures': len(self.threat_intelligence['threat_signatures']),
            'malicious_ips': len(self.threat_intelligence['malicious_ips']),
            'suspicious_domains': len(self.threat_intelligence['suspicious_domains']),
            'models_trained': self.is_trained
        }

class EnhancedGeminiAI:
    """Enhanced Gemini AI with advanced threat analysis capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "AIzaSyBBDP4NnmxGA8bJc8DsSd_WOI5QwZCsF6o"
        self.is_available = GEMINI_AVAILABLE
        
        if self.is_available:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("🤖 Enhanced Gemini AI initialized!")
            except Exception as e:
                print(f"❌ Enhanced Gemini AI initialization failed: {e}")
                self.is_available = False
    
    def analyze_enhanced_threat(self, system_data: Dict, threat_context: str = "") -> Dict:
        """Enhanced threat analysis using Gemini AI"""
        if not self.is_available:
            return self._fallback_enhanced_analysis(system_data)
        
        try:
            # Enhanced analysis prompt
            prompt = f"""
            Perform comprehensive threat analysis on the following system data:
            
            SYSTEM METRICS:
            - CPU Usage: {system_data.get('cpu_percent', 0)}%
            - Memory Usage: {system_data.get('memory_percent', 0)}%
            - Network Activity: {system_data.get('network_bytes_sent', 0)} bytes sent, {system_data.get('network_bytes_recv', 0)} bytes received
            - Process Count: {system_data.get('process_count', 0)}
            - Disk Usage: {system_data.get('disk_usage_percent', 0)}%
            - Thread Count: {system_data.get('thread_count', 0)}
            
            THREAT CONTEXT: {threat_context}
            
            Please provide detailed analysis including:
            1. Threat level (0-100)
            2. Threat type and category
            3. Attack vector analysis
            4. Recommended immediate actions
            5. Long-term security recommendations
            6. Confidence level (0-100)
            7. Risk assessment
            8. Mitigation strategies
            
            Respond in detailed JSON format with comprehensive analysis.
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse enhanced AI response
            try:
                analysis = json.loads(response.text)
                return {
                    'threat_level': analysis.get('threat_level', 0),
                    'threat_type': analysis.get('threat_type', 'Unknown'),
                    'attack_vector': analysis.get('attack_vector', 'Unknown'),
                    'recommended_actions': analysis.get('recommended_actions', ['Monitor']),
                    'confidence': analysis.get('confidence', 50),
                    'risk_assessment': analysis.get('risk_assessment', 'Medium'),
                    'mitigation_strategies': analysis.get('mitigation_strategies', []),
                    'ai_analysis': True
                }
            except json.JSONDecodeError:
                return self._parse_enhanced_text_response(response.text)
                
        except Exception as e:
            print(f"❌ Enhanced Gemini AI analysis failed: {e}")
            return self._fallback_enhanced_analysis(system_data)
    
    def _parse_enhanced_text_response(self, text: str) -> Dict:
        """Parse enhanced text response from AI"""
        threat_level = 0
        threat_type = "AI Detected"
        
        # Enhanced text parsing
        if 'critical' in text.lower() or 'severe' in text.lower():
            threat_level = 90
        elif 'high' in text.lower():
            threat_level = 70
        elif 'medium' in text.lower():
            threat_level = 50
        elif 'low' in text.lower():
            threat_level = 30
        
        return {
            'threat_level': threat_level,
            'threat_type': threat_type,
            'attack_vector': 'AI Analysis',
            'recommended_actions': ['Investigate', 'Monitor'],
            'confidence': 75,
            'risk_assessment': 'Medium',
            'mitigation_strategies': ['Enhanced Monitoring', 'System Analysis'],
            'ai_analysis': True
        }
    
    def _fallback_enhanced_analysis(self, system_data: Dict) -> Dict:
        """Enhanced fallback analysis without AI"""
        threat_level = 0
        
        # Enhanced heuristic analysis
        if system_data.get('cpu_percent', 0) > 95:
            threat_level += 40
        if system_data.get('memory_percent', 0) > 95:
            threat_level += 40
        if system_data.get('network_bytes_sent', 0) > 10000000:  # 10MB
            threat_level += 30
        if system_data.get('process_count', 0) > 500:
            threat_level += 20
        if system_data.get('thread_count', 0) > 1000:
            threat_level += 20
        
        return {
            'threat_level': min(threat_level, 100),
            'threat_type': 'Heuristic Analysis',
            'attack_vector': 'System Resource Analysis',
            'recommended_actions': ['Monitor'] if threat_level < 50 else ['Investigate', 'Isolate'],
            'confidence': 60,
            'risk_assessment': 'High' if threat_level > 70 else 'Medium',
            'mitigation_strategies': ['Resource Monitoring', 'Process Analysis'],
            'ai_analysis': False
        }

class EnhancedAIThreatDetector:
    """Enhanced AI Threat Detector with advanced capabilities"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.threat_history = deque(maxlen=10000)  # Increased capacity
        
        # Initialize enhanced components
        self.neural_analyzer = EnhancedNeuralThreatAnalyzer()
        self.gemini_detector = EnhancedGeminiAI(gemini_api_key)
        
        # Enhanced configuration
        self.monitoring_interval = 3  # Reduced interval for better detection
        self.threat_threshold = 60  # Adjusted threshold
        self.high_threat_threshold = 85
        
        # Enhanced statistics
        self.total_threats_detected = 0
        self.threat_types = {}
        self.attack_vectors = {}
        self.risk_levels = {}
        
        print("🤖 Enhanced AI Threat Detector initialized!")
        print(f"   Monitoring interval: {self.monitoring_interval}s")
        print(f"   Threat threshold: {self.threat_threshold}")
        print(f"   High threat threshold: {self.high_threat_threshold}")
    
    def start_enhanced_monitoring(self):
        """Start enhanced AI threat monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._enhanced_monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("🔍 Enhanced AI threat monitoring started!")
    
    def stop_enhanced_monitoring(self):
        """Stop enhanced AI threat monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("⏹️ Enhanced AI threat monitoring stopped!")
    
    def _enhanced_monitoring_loop(self):
        """Enhanced monitoring loop with advanced analysis"""
        while self.is_monitoring:
            try:
                # Collect enhanced system data
                system_data = self._collect_enhanced_system_data()
                
                # Perform enhanced threat analysis
                threat_analysis = self._analyze_enhanced_threats(system_data)
                
                # Handle threats with enhanced response
                if threat_analysis['overall_threat_level'] > self.threat_threshold:
                    self._handle_enhanced_threat(threat_analysis)
                
                # Update enhanced learning models
                self._update_enhanced_learning_models(system_data, threat_analysis)
                
                # Wait for next monitoring cycle
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"❌ Enhanced monitoring error: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_enhanced_system_data(self) -> Dict:
        """Collect enhanced system data with security metrics"""
        try:
            # Basic system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            network = psutil.net_io_counters()
            disk = psutil.disk_usage('/')
            
            # Enhanced security metrics
            process_count = len(psutil.pids())
            thread_count = sum(p.num_threads() for p in psutil.process_iter(['num_threads']) if p.info['num_threads'])
            
            # Network connections analysis
            connections = psutil.net_connections()
            suspicious_connections = len([c for c in connections if c.status == 'ESTABLISHED' and c.raddr])
            
            return {
                'timestamp': time.time(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'process_count': process_count,
                'thread_count': thread_count,
                'disk_usage_percent': (disk.used / disk.total) * 100,
                'suspicious_connections': suspicious_connections,
                'failed_logins': 0,  # Would be populated from logs
                'privilege_escalations': 0,  # Would be populated from logs
                'file_modifications': 0  # Would be populated from logs
            }
            
        except Exception as e:
            print(f"❌ Enhanced system data collection error: {e}")
            return {}
    
    def _analyze_enhanced_threats(self, system_data: Dict) -> Dict:
        """Enhanced threat analysis with multiple AI models"""
        analysis = {
            'timestamp': time.time(),
            'system_data': system_data,
            'neural_analysis': {},
            'gemini_analysis': {},
            'overall_threat_level': 0,
            'threat_confidence': 0,
            'recommended_actions': [],
            'risk_assessment': 'Low'
        }
        
        # Enhanced neural network analysis
        if self.neural_analyzer.is_trained:
            is_anomaly, anomaly_score, detailed_analysis = self.neural_analyzer.detect_enhanced_anomaly(system_data)
            analysis['neural_analysis'] = {
                'is_anomaly': is_anomaly,
                'anomaly_score': anomaly_score,
                'detailed_analysis': detailed_analysis,
                'threat_level': anomaly_score * 100 if is_anomaly else 0
            }
        
        # Enhanced Gemini AI analysis
        gemini_analysis = self.gemini_detector.analyze_enhanced_threat(system_data)
        analysis['gemini_analysis'] = gemini_analysis
        
        # Calculate enhanced overall threat level
        threat_scores = []
        
        if analysis['neural_analysis']:
            threat_scores.append(analysis['neural_analysis']['threat_level'])
        
        if gemini_analysis['ai_analysis']:
            threat_scores.append(gemini_analysis['threat_level'])
        
        # Enhanced threat level calculation
        if threat_scores:
            analysis['overall_threat_level'] = sum(threat_scores) / len(threat_scores)
            analysis['threat_confidence'] = min(100, len(threat_scores) * 30)
        
        # Enhanced risk assessment
        if analysis['overall_threat_level'] > 80:
            analysis['risk_assessment'] = 'Critical'
        elif analysis['overall_threat_level'] > 60:
            analysis['risk_assessment'] = 'High'
        elif analysis['overall_threat_level'] > 40:
            analysis['risk_assessment'] = 'Medium'
        else:
            analysis['risk_assessment'] = 'Low'
        
        # Generate enhanced recommendations
        analysis['recommended_actions'] = self._generate_enhanced_recommendations(analysis)
        
        return analysis
    
    def _generate_enhanced_recommendations(self, analysis: Dict) -> List[str]:
        """Generate enhanced threat response recommendations"""
        recommendations = []
        threat_level = analysis['overall_threat_level']
        risk_assessment = analysis['risk_assessment']
        
        if risk_assessment == 'Critical':
            recommendations.extend([
                'IMMEDIATE_SYSTEM_ISOLATION',
                'ACTIVATE_EMERGENCY_PROTOCOLS',
                'NOTIFY_SECURITY_TEAM',
                'ENHANCE_MONITORING_FREQUENCY',
                'BLOCK_SUSPICIOUS_NETWORK_TRAFFIC',
                'ANALYZE_SYSTEM_LOGS',
                'BACKUP_CRITICAL_DATA'
            ])
        elif risk_assessment == 'High':
            recommendations.extend([
                'INCREASE_MONITORING_FREQUENCY',
                'ACTIVATE_DEFENSE_SYSTEMS',
                'ANALYZE_NETWORK_TRAFFIC',
                'CHECK_SYSTEM_LOGS',
                'UPDATE_SECURITY_RULES',
                'SCAN_FOR_MALWARE'
            ])
        elif risk_assessment == 'Medium':
            recommendations.extend([
                'CONTINUE_MONITORING',
                'ANALYZE_SYSTEM_PATTERNS',
                'UPDATE_THREAT_INTELLIGENCE',
                'REVIEW_SECURITY_POLICIES'
            ])
        else:
            recommendations.append('CONTINUE_MONITORING')
        
        return recommendations
    
    def _handle_enhanced_threat(self, threat_analysis: Dict):
        """Handle detected threats with enhanced response"""
        threat_level = threat_analysis['overall_threat_level']
        threat_type = threat_analysis['gemini_analysis'].get('threat_type', 'Unknown')
        attack_vector = threat_analysis['gemini_analysis'].get('attack_vector', 'Unknown')
        
        # Record enhanced threat statistics
        self.total_threats_detected += 1
        self.threat_types[threat_type] = self.threat_types.get(threat_type, 0) + 1
        self.attack_vectors[attack_vector] = self.attack_vectors.get(attack_vector, 0) + 1
        
        # Store in enhanced history
        self.threat_history.append(threat_analysis)
        
        # Enhanced threat logging
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🚨 ENHANCED THREAT DETECTED [{timestamp}]")
        print(f"   Level: {threat_level:.1f}/100")
        print(f"   Type: {threat_type}")
        print(f"   Attack Vector: {attack_vector}")
        print(f"   Risk Assessment: {threat_analysis['risk_assessment']}")
        print(f"   Confidence: {threat_analysis['threat_confidence']:.1f}%")
        print(f"   Actions: {', '.join(threat_analysis['recommended_actions'])}")
        
        # Execute enhanced emergency response for critical threats
        if threat_analysis['risk_assessment'] == 'Critical':
            self._execute_enhanced_emergency_response(threat_analysis)
    
    def _execute_enhanced_emergency_response(self, threat_analysis: Dict):
        """Execute enhanced emergency response for critical threats"""
        print("🚨 EXECUTING ENHANCED EMERGENCY RESPONSE!")
        
        # Enhanced emergency response actions
        emergency_actions = [
            'SYSTEM_ISOLATION',
            'NETWORK_SEGMENTATION',
            'DEFENSE_ACTIVATION',
            'THREAT_INTELLIGENCE_UPDATE',
            'SECURITY_TEAM_NOTIFICATION',
            'INCIDENT_RESPONSE_ACTIVATION'
        ]
        
        for action in emergency_actions:
            print(f"   ✅ {action}")
        
        print("✅ Enhanced emergency response executed!")
    
    def _update_enhanced_learning_models(self, system_data: Dict, threat_analysis: Dict):
        """Update enhanced AI learning models"""
        threat_level = threat_analysis['overall_threat_level']
        
        # Update neural analyzer
        if threat_level < 30:  # Normal behavior
            self.neural_analyzer.normal_patterns.append(system_data)
        elif threat_level > 70:  # Threat behavior
            self.neural_analyzer.threat_patterns.append(system_data)
        
        # Retrain models periodically
        if self.total_threats_detected % 500 == 0:
            self.neural_analyzer.train_enhanced_models()
    
    def get_enhanced_statistics(self) -> Dict:
        """Get enhanced threat statistics"""
        return {
            'total_threats_detected': self.total_threats_detected,
            'threat_types': dict(self.threat_types),
            'attack_vectors': dict(self.attack_vectors),
            'monitoring_active': self.is_monitoring,
            'neural_model_trained': self.neural_analyzer.is_trained,
            'gemini_available': self.gemini_detector.is_available,
            'threat_intelligence': self.neural_analyzer.get_threat_intelligence(),
            'threat_history_size': len(self.threat_history)
        }
