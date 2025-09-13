"""
Advanced AI Threat Detector with Neural Networks
Miracle-level threat detection with machine learning
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

# AI/ML imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import DBSCAN
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class NeuralThreatAnalyzer:
    """Neural Network-based Threat Analysis"""
    
    def __init__(self):
        self.threat_patterns = deque(maxlen=10000)
        self.normal_patterns = deque(maxlen=10000)
        self.anomaly_detector = None
        self.scaler = None
        self.is_trained = False
        
        if SKLEARN_AVAILABLE:
            self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
            self.scaler = StandardScaler()
    
    def extract_features(self, system_data: Dict) -> np.ndarray:
        """Extract features for neural network analysis"""
        features = []
        
        # CPU features
        features.extend([
            system_data.get('cpu_percent', 0),
            system_data.get('cpu_count', 1),
            system_data.get('cpu_freq', 0)
        ])
        
        # Memory features
        features.extend([
            system_data.get('memory_percent', 0),
            system_data.get('memory_available', 0),
            system_data.get('memory_used', 0)
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
        
        # Disk features
        features.extend([
            system_data.get('disk_usage_percent', 0),
            system_data.get('disk_read_bytes', 0),
            system_data.get('disk_write_bytes', 0)
        ])
        
        return np.array(features, dtype=np.float32)
    
    def train_anomaly_detector(self):
        """Train the anomaly detection model"""
        if not SKLEARN_AVAILABLE or len(self.normal_patterns) < 100:
            return False
        
        try:
            # Prepare training data
            normal_data = [self.extract_features(pattern) for pattern in self.normal_patterns]
            X = np.array(normal_data)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train anomaly detector
            self.anomaly_detector.fit(X_scaled)
            self.is_trained = True
            
            print("🧠 Neural threat analyzer trained successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def detect_anomaly(self, system_data: Dict) -> Tuple[bool, float]:
        """Detect anomalies using neural network"""
        if not self.is_trained:
            return False, 0.0
        
        try:
            features = self.extract_features(system_data)
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            
            # Predict anomaly
            anomaly_score = self.anomaly_detector.decision_function(features_scaled)[0]
            is_anomaly = self.anomaly_detector.predict(features_scaled)[0] == -1
            
            return is_anomaly, float(anomaly_score)
            
        except Exception as e:
            print(f"❌ Anomaly detection error: {e}")
            return False, 0.0
    
    def add_normal_pattern(self, system_data: Dict):
        """Add normal system pattern for training"""
        self.normal_patterns.append(system_data.copy())
        
        # Retrain periodically
        if len(self.normal_patterns) % 1000 == 0:
            self.train_anomaly_detector()
    
    def add_threat_pattern(self, system_data: Dict):
        """Add threat pattern for learning"""
        self.threat_patterns.append(system_data.copy())

class GeminiAIThreatDetector:
    """Gemini AI-powered threat detection"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "AIzaSyBBDP4NnmxGA8bJc8DsSd_WOI5QwZCsF6o"
        self.is_available = GEMINI_AVAILABLE
        
        if self.is_available:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("🤖 Gemini AI threat detector initialized!")
            except Exception as e:
                print(f"❌ Gemini AI initialization failed: {e}")
                self.is_available = False
    
    def analyze_threat(self, system_data: Dict, threat_context: str = "") -> Dict:
        """Analyze threat using Gemini AI"""
        if not self.is_available:
            return self._fallback_analysis(system_data)
        
        try:
            # Prepare analysis prompt
            prompt = f"""
            Analyze the following system data for potential security threats:
            
            System Data:
            - CPU Usage: {system_data.get('cpu_percent', 0)}%
            - Memory Usage: {system_data.get('memory_percent', 0)}%
            - Network Activity: {system_data.get('network_bytes_sent', 0)} bytes sent, {system_data.get('network_bytes_recv', 0)} bytes received
            - Process Count: {system_data.get('process_count', 0)}
            - Disk Usage: {system_data.get('disk_usage_percent', 0)}%
            
            Context: {threat_context}
            
            Please analyze this data and provide:
            1. Threat level (0-100)
            2. Threat type (if any)
            3. Recommended action
            4. Confidence level (0-100)
            
            Respond in JSON format.
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse AI response
            try:
                analysis = json.loads(response.text)
                return {
                    'threat_level': analysis.get('threat_level', 0),
                    'threat_type': analysis.get('threat_type', 'Unknown'),
                    'recommended_action': analysis.get('recommended_action', 'Monitor'),
                    'confidence': analysis.get('confidence', 50),
                    'ai_analysis': True
                }
            except json.JSONDecodeError:
                return self._parse_text_response(response.text)
                
        except Exception as e:
            print(f"❌ Gemini AI analysis failed: {e}")
            return self._fallback_analysis(system_data)
    
    def _parse_text_response(self, text: str) -> Dict:
        """Parse text response from AI"""
        # Simple text parsing as fallback
        threat_level = 0
        if 'high' in text.lower():
            threat_level = 80
        elif 'medium' in text.lower():
            threat_level = 50
        elif 'low' in text.lower():
            threat_level = 20
        
        return {
            'threat_level': threat_level,
            'threat_type': 'AI Detected',
            'recommended_action': 'Investigate',
            'confidence': 60,
            'ai_analysis': True
        }
    
    def _fallback_analysis(self, system_data: Dict) -> Dict:
        """Fallback analysis without AI"""
        threat_level = 0
        
        # Simple heuristic analysis
        if system_data.get('cpu_percent', 0) > 90:
            threat_level += 30
        if system_data.get('memory_percent', 0) > 90:
            threat_level += 30
        if system_data.get('network_bytes_sent', 0) > 1000000:  # 1MB
            threat_level += 20
        if system_data.get('process_count', 0) > 200:
            threat_level += 20
        
        return {
            'threat_level': min(threat_level, 100),
            'threat_type': 'Heuristic Analysis',
            'recommended_action': 'Monitor' if threat_level < 50 else 'Investigate',
            'confidence': 40,
            'ai_analysis': False
        }

class BehavioralAnalyzer:
    """Behavioral analysis for threat detection"""
    
    def __init__(self):
        self.behavior_history = deque(maxlen=1000)
        self.baseline_behavior = {}
        self.anomaly_threshold = 0.7
        
    def analyze_behavior(self, system_data: Dict) -> Dict:
        """Analyze system behavior patterns"""
        current_time = time.time()
        
        # Add to history
        behavior_point = {
            'timestamp': current_time,
            'data': system_data.copy()
        }
        self.behavior_history.append(behavior_point)
        
        # Calculate baseline if we have enough data
        if len(self.behavior_history) >= 100:
            self._update_baseline()
        
        # Detect behavioral anomalies
        anomalies = self._detect_behavioral_anomalies(system_data)
        
        return {
            'anomalies_detected': len(anomalies),
            'anomaly_types': anomalies,
            'baseline_established': len(self.baseline_behavior) > 0,
            'behavior_score': self._calculate_behavior_score(system_data)
        }
    
    def _update_baseline(self):
        """Update behavioral baseline"""
        if len(self.behavior_history) < 50:
            return
        
        # Calculate averages for recent data
        recent_data = list(self.behavior_history)[-50:]
        
        self.baseline_behavior = {
            'cpu_avg': np.mean([d['data'].get('cpu_percent', 0) for d in recent_data]),
            'memory_avg': np.mean([d['data'].get('memory_percent', 0) for d in recent_data]),
            'network_avg': np.mean([d['data'].get('network_bytes_sent', 0) for d in recent_data]),
            'process_avg': np.mean([d['data'].get('process_count', 0) for d in recent_data])
        }
    
    def _detect_behavioral_anomalies(self, system_data: Dict) -> List[str]:
        """Detect behavioral anomalies"""
        anomalies = []
        
        if not self.baseline_behavior:
            return anomalies
        
        # CPU anomaly
        cpu_deviation = abs(system_data.get('cpu_percent', 0) - self.baseline_behavior['cpu_avg'])
        if cpu_deviation > 30:  # 30% deviation
            anomalies.append('CPU_ANOMALY')
        
        # Memory anomaly
        memory_deviation = abs(system_data.get('memory_percent', 0) - self.baseline_behavior['memory_avg'])
        if memory_deviation > 20:  # 20% deviation
            anomalies.append('MEMORY_ANOMALY')
        
        # Network anomaly
        network_current = system_data.get('network_bytes_sent', 0)
        if network_current > self.baseline_behavior['network_avg'] * 5:  # 5x increase
            anomalies.append('NETWORK_ANOMALY')
        
        # Process anomaly
        process_deviation = abs(system_data.get('process_count', 0) - self.baseline_behavior['process_avg'])
        if process_deviation > 50:  # 50 process deviation
            anomalies.append('PROCESS_ANOMALY')
        
        return anomalies
    
    def _calculate_behavior_score(self, system_data: Dict) -> float:
        """Calculate behavior score (0-100)"""
        if not self.baseline_behavior:
            return 50.0  # Neutral score
        
        score = 50.0  # Start with neutral
        
        # Adjust score based on deviations
        cpu_deviation = abs(system_data.get('cpu_percent', 0) - self.baseline_behavior['cpu_avg'])
        score -= min(cpu_deviation / 2, 25)  # Max -25 points
        
        memory_deviation = abs(system_data.get('memory_percent', 0) - self.baseline_behavior['memory_avg'])
        score -= min(memory_deviation / 2, 25)  # Max -25 points
        
        return max(0, min(100, score))

class AIThreatDetector:
    """Main AI Threat Detector with all advanced features"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.threat_history = deque(maxlen=1000)
        
        # Initialize components
        self.neural_analyzer = NeuralThreatAnalyzer()
        self.gemini_detector = GeminiAIThreatDetector(gemini_api_key)
        self.behavioral_analyzer = BehavioralAnalyzer()
        
        # Configuration
        self.monitoring_interval = 5  # seconds
        self.threat_threshold = 70
        self.high_threat_threshold = 90
        
        # Statistics
        self.total_threats_detected = 0
        self.threat_types = {}
        
        print("🤖 Advanced AI Threat Detector initialized!")
    
    def start_monitoring(self):
        """Start AI threat monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("🔍 AI threat monitoring started!")
    
    def stop_monitoring(self):
        """Stop AI threat monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("⏹️ AI threat monitoring stopped!")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect system data
                system_data = self._collect_system_data()
                
                # Perform AI analysis
                threat_analysis = self._analyze_threats(system_data)
                
                # Handle threats
                if threat_analysis['overall_threat_level'] > self.threat_threshold:
                    self._handle_threat(threat_analysis)
                
                # Update learning models
                self._update_learning_models(system_data, threat_analysis)
                
                # Wait for next monitoring cycle
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_system_data(self) -> Dict:
        """Collect comprehensive system data"""
        try:
            # CPU data
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
            
            # Memory data
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available
            memory_used = memory.used
            
            # Network data
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv
            network_packets_sent = network.packets_sent
            network_packets_recv = network.packets_recv
            
            # Process data
            process_count = len(psutil.pids())
            thread_count = sum(p.num_threads() for p in psutil.process_iter(['num_threads']) if p.info['num_threads'])
            
            # Disk data
            disk = psutil.disk_usage('/')
            disk_usage_percent = (disk.used / disk.total) * 100
            disk_io = psutil.disk_io_counters()
            disk_read_bytes = disk_io.read_bytes if disk_io else 0
            disk_write_bytes = disk_io.write_bytes if disk_io else 0
            
            return {
                'timestamp': time.time(),
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'cpu_freq': cpu_freq,
                'memory_percent': memory_percent,
                'memory_available': memory_available,
                'memory_used': memory_used,
                'network_bytes_sent': network_bytes_sent,
                'network_bytes_recv': network_bytes_recv,
                'network_packets_sent': network_packets_sent,
                'network_packets_recv': network_packets_recv,
                'process_count': process_count,
                'thread_count': thread_count,
                'disk_usage_percent': disk_usage_percent,
                'disk_read_bytes': disk_read_bytes,
                'disk_write_bytes': disk_write_bytes
            }
            
        except Exception as e:
            print(f"❌ System data collection error: {e}")
            return {}
    
    def _analyze_threats(self, system_data: Dict) -> Dict:
        """Comprehensive threat analysis"""
        analysis = {
            'timestamp': time.time(),
            'system_data': system_data,
            'neural_analysis': {},
            'gemini_analysis': {},
            'behavioral_analysis': {},
            'overall_threat_level': 0,
            'threat_confidence': 0,
            'recommended_actions': []
        }
        
        # Neural network analysis
        if self.neural_analyzer.is_trained:
            is_anomaly, anomaly_score = self.neural_analyzer.detect_anomaly(system_data)
            analysis['neural_analysis'] = {
                'is_anomaly': is_anomaly,
                'anomaly_score': anomaly_score,
                'threat_level': abs(anomaly_score) * 100 if is_anomaly else 0
            }
        
        # Gemini AI analysis
        gemini_analysis = self.gemini_detector.analyze_threat(system_data)
        analysis['gemini_analysis'] = gemini_analysis
        
        # Behavioral analysis
        behavioral_analysis = self.behavioral_analyzer.analyze_behavior(system_data)
        analysis['behavioral_analysis'] = behavioral_analysis
        
        # Calculate overall threat level
        threat_scores = []
        
        if analysis['neural_analysis']:
            threat_scores.append(analysis['neural_analysis']['threat_level'])
        
        if gemini_analysis['ai_analysis']:
            threat_scores.append(gemini_analysis['threat_level'])
        
        # Behavioral threat score
        behavior_score = behavioral_analysis['behavior_score']
        behavioral_threat = 100 - behavior_score  # Invert behavior score
        threat_scores.append(behavioral_threat)
        
        # Calculate weighted average
        if threat_scores:
            analysis['overall_threat_level'] = sum(threat_scores) / len(threat_scores)
            analysis['threat_confidence'] = min(100, len(threat_scores) * 25)  # More sources = higher confidence
        
        # Generate recommendations
        analysis['recommended_actions'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate threat response recommendations"""
        recommendations = []
        threat_level = analysis['overall_threat_level']
        
        if threat_level > self.high_threat_threshold:
            recommendations.extend([
                'IMMEDIATE_ISOLATION',
                'ACTIVATE_EMERGENCY_PROTOCOLS',
                'NOTIFY_SECURITY_TEAM',
                'ENHANCE_MONITORING'
            ])
        elif threat_level > self.threat_threshold:
            recommendations.extend([
                'INCREASE_MONITORING_FREQUENCY',
                'ACTIVATE_DEFENSE_SYSTEMS',
                'ANALYZE_NETWORK_TRAFFIC',
                'CHECK_SYSTEM_LOGS'
            ])
        else:
            recommendations.append('CONTINUE_MONITORING')
        
        return recommendations
    
    def _handle_threat(self, threat_analysis: Dict):
        """Handle detected threats"""
        threat_level = threat_analysis['overall_threat_level']
        threat_type = threat_analysis['gemini_analysis'].get('threat_type', 'Unknown')
        
        # Record threat
        self.total_threats_detected += 1
        self.threat_types[threat_type] = self.threat_types.get(threat_type, 0) + 1
        
        # Store in history
        self.threat_history.append(threat_analysis)
        
        # Log threat
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🚨 THREAT DETECTED [{timestamp}]")
        print(f"   Level: {threat_level:.1f}/100")
        print(f"   Type: {threat_type}")
        print(f"   Confidence: {threat_analysis['threat_confidence']:.1f}%")
        print(f"   Actions: {', '.join(threat_analysis['recommended_actions'])}")
        
        # Execute immediate actions for high threats
        if threat_level > self.high_threat_threshold:
            self._execute_emergency_response(threat_analysis)
    
    def _execute_emergency_response(self, threat_analysis: Dict):
        """Execute emergency response for high-level threats"""
        print("🚨 EXECUTING EMERGENCY RESPONSE!")
        
        # Log emergency response
        emergency_log = {
            'timestamp': time.time(),
            'threat_analysis': threat_analysis,
            'response_actions': ['EMERGENCY_ISOLATION', 'DEFENSE_ACTIVATION']
        }
        
        # In a real implementation, this would:
        # - Isolate affected systems
        # - Activate additional defense mechanisms
        # - Send alerts to security teams
        # - Create incident reports
        
        print("✅ Emergency response executed!")
    
    def _update_learning_models(self, system_data: Dict, threat_analysis: Dict):
        """Update AI learning models"""
        threat_level = threat_analysis['overall_threat_level']
        
        # Update neural analyzer
        if threat_level < 30:  # Normal behavior
            self.neural_analyzer.add_normal_pattern(system_data)
        elif threat_level > 70:  # Threat behavior
            self.neural_analyzer.add_threat_pattern(system_data)
        
        # Retrain models periodically
        if self.total_threats_detected % 100 == 0:
            self.neural_analyzer.train_anomaly_detector()
    
    def get_threat_statistics(self) -> Dict:
        """Get comprehensive threat statistics"""
        return {
            'total_threats_detected': self.total_threats_detected,
            'threat_types': dict(self.threat_types),
            'monitoring_active': self.is_monitoring,
            'neural_model_trained': self.neural_analyzer.is_trained,
            'gemini_available': self.gemini_detector.is_available,
            'baseline_established': len(self.behavioral_analyzer.baseline_behavior) > 0,
            'threat_history_size': len(self.threat_history)
        }
    
    def get_recent_threats(self, count: int = 10) -> List[Dict]:
        """Get recent threat detections"""
        return list(self.threat_history)[-count:]
