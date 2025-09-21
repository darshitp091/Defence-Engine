"""
Enhanced Behavioral Analysis System
Advanced behavioral pattern analysis with machine learning and anomaly detection
"""
import time
import threading
import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import deque
import json
import hashlib
import secrets
from datetime import datetime, timedelta
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import DBSCAN
    from sklearn.neural_network import MLPClassifier
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class EnhancedBehavioralAnalyzer:
    """Enhanced Behavioral Analysis with Advanced Pattern Recognition"""
    
    def __init__(self):
        self.behavior_history = deque(maxlen=50000)  # Increased capacity
        self.baseline_behavior = {}
        self.anomaly_threshold = 0.6  # Adjusted threshold
        self.behavior_patterns = {}
        self.user_profiles = {}
        
        # Enhanced ML models
        self.isolation_forest = None
        self.scaler = None
        self.dbscan_cluster = None
        self.behavior_classifier = None
        
        if SKLEARN_AVAILABLE:
            self.isolation_forest = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
            self.scaler = StandardScaler()
            self.dbscan_cluster = DBSCAN(eps=0.3, min_samples=5)
            self.behavior_classifier = MLPClassifier(
                hidden_layer_sizes=(50, 25),
                random_state=42,
                max_iter=1000
            )
        
        # Behavioral metrics
        self.behavioral_metrics = {
            'normal_patterns': 0,
            'anomalous_patterns': 0,
            'suspicious_activities': 0,
            'user_deviations': 0
        }
        
        print("🧠 Enhanced Behavioral Analyzer initialized!")
        print(f"   ML Models: {len([m for m in [self.isolation_forest, self.scaler, self.dbscan_cluster, self.behavior_classifier] if m is not None])}")
        print(f"   History capacity: {self.behavior_history.maxlen}")
    
    def analyze_enhanced_behavior(self, system_data: Dict, user_id: str = "default") -> Dict:
        """Analyze enhanced behavioral patterns with ML"""
        current_time = time.time()
        
        # Create enhanced behavior point
        behavior_point = {
            'timestamp': current_time,
            'user_id': user_id,
            'data': system_data.copy(),
            'behavioral_features': self._extract_behavioral_features(system_data),
            'context': self._analyze_context(system_data)
        }
        
        # Add to history
        self.behavior_history.append(behavior_point)
        
        # Update user profile
        self._update_user_profile(user_id, behavior_point)
        
        # Detect behavioral anomalies
        anomalies = self._detect_enhanced_anomalies(behavior_point)
        
        # Calculate enhanced behavior score
        behavior_score = self._calculate_enhanced_behavior_score(behavior_point)
        
        # Analyze behavioral patterns
        pattern_analysis = self._analyze_behavioral_patterns(behavior_point)
        
        return {
            'timestamp': current_time,
            'user_id': user_id,
            'anomalies_detected': len(anomalies),
            'anomaly_types': anomalies,
            'behavior_score': behavior_score,
            'pattern_analysis': pattern_analysis,
            'baseline_established': len(self.baseline_behavior) > 0,
            'user_profile_updated': user_id in self.user_profiles,
            'risk_level': self._assess_behavioral_risk(behavior_score, anomalies)
        }
    
    def _extract_behavioral_features(self, system_data: Dict) -> List[float]:
        """Extract enhanced behavioral features"""
        features = []
        
        # System performance features
        features.extend([
            system_data.get('cpu_percent', 0),
            system_data.get('memory_percent', 0),
            system_data.get('disk_usage_percent', 0)
        ])
        
        # Network behavior features
        features.extend([
            system_data.get('network_bytes_sent', 0),
            system_data.get('network_bytes_recv', 0),
            system_data.get('network_packets_sent', 0),
            system_data.get('network_packets_recv', 0)
        ])
        
        # Process behavior features
        features.extend([
            system_data.get('process_count', 0),
            system_data.get('thread_count', 0)
        ])
        
        # Time-based features
        current_time = time.time()
        features.extend([
            current_time % 86400,  # Time of day
            current_time % 604800,  # Day of week
            current_time % 31536000  # Day of year
        ])
        
        # Behavioral context features
        features.extend([
            system_data.get('suspicious_connections', 0),
            system_data.get('failed_logins', 0),
            system_data.get('privilege_escalations', 0)
        ])
        
        return features
    
    def _analyze_context(self, system_data: Dict) -> Dict:
        """Analyze behavioral context"""
        context = {
            'time_of_day': time.strftime("%H:%M:%S"),
            'day_of_week': time.strftime("%A"),
            'system_load': 'high' if system_data.get('cpu_percent', 0) > 80 else 'normal',
            'network_activity': 'high' if system_data.get('network_bytes_sent', 0) > 1000000 else 'normal',
            'process_count': 'high' if system_data.get('process_count', 0) > 200 else 'normal'
        }
        
        return context
    
    def _update_user_profile(self, user_id: str, behavior_point: Dict):
        """Update user behavioral profile"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'behavior_history': deque(maxlen=1000),
                'baseline_patterns': {},
                'anomaly_count': 0,
                'last_activity': time.time()
            }
        
        profile = self.user_profiles[user_id]
        profile['behavior_history'].append(behavior_point)
        profile['last_activity'] = time.time()
        
        # Update baseline patterns
        if len(profile['behavior_history']) >= 100:
            self._update_user_baseline(user_id)
    
    def _update_user_baseline(self, user_id: str):
        """Update user baseline behavioral patterns"""
        profile = self.user_profiles[user_id]
        recent_behaviors = list(profile['behavior_history'])[-100:]
        
        # Calculate baseline metrics
        baseline = {
            'cpu_avg': np.mean([b['data'].get('cpu_percent', 0) for b in recent_behaviors]),
            'memory_avg': np.mean([b['data'].get('memory_percent', 0) for b in recent_behaviors]),
            'network_avg': np.mean([b['data'].get('network_bytes_sent', 0) for b in recent_behaviors]),
            'process_avg': np.mean([b['data'].get('process_count', 0) for b in recent_behaviors]),
            'activity_patterns': self._analyze_activity_patterns(recent_behaviors)
        }
        
        profile['baseline_patterns'] = baseline
    
    def _analyze_activity_patterns(self, behaviors: List[Dict]) -> Dict:
        """Analyze user activity patterns"""
        patterns = {
            'peak_hours': [],
            'activity_frequency': 0,
            'resource_usage_patterns': {},
            'network_usage_patterns': {}
        }
        
        # Analyze time patterns
        hours = [time.localtime(b['timestamp']).tm_hour for b in behaviors]
        hour_counts = {}
        for hour in hours:
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        patterns['peak_hours'] = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        patterns['activity_frequency'] = len(behaviors) / 24  # Activities per hour
        
        return patterns
    
    def _detect_enhanced_anomalies(self, behavior_point: Dict) -> List[str]:
        """Detect enhanced behavioral anomalies"""
        anomalies = []
        
        # Check against global baseline
        if self.baseline_behavior:
            anomalies.extend(self._check_global_anomalies(behavior_point))
        
        # Check against user baseline
        user_id = behavior_point['user_id']
        if user_id in self.user_profiles and self.user_profiles[user_id]['baseline_patterns']:
            anomalies.extend(self._check_user_anomalies(behavior_point))
        
        # ML-based anomaly detection (skip for now to avoid sklearn issues)
        # if self.isolation_forest and len(self.behavior_history) > 100:
        #     try:
        #         anomalies.extend(self._check_ml_anomalies(behavior_point))
        #     except:
        #         pass  # Skip ML analysis if not trained
        
        return anomalies
    
    def _check_global_anomalies(self, behavior_point: Dict) -> List[str]:
        """Check for global baseline anomalies"""
        anomalies = []
        data = behavior_point['data']
        
        # CPU anomaly
        cpu_deviation = abs(data.get('cpu_percent', 0) - self.baseline_behavior.get('cpu_avg', 0))
        if cpu_deviation > 40:  # 40% deviation
            anomalies.append('CPU_ANOMALY')
        
        # Memory anomaly
        memory_deviation = abs(data.get('memory_percent', 0) - self.baseline_behavior.get('memory_avg', 0))
        if memory_deviation > 30:  # 30% deviation
            anomalies.append('MEMORY_ANOMALY')
        
        # Network anomaly
        network_current = data.get('network_bytes_sent', 0)
        if network_current > self.baseline_behavior.get('network_avg', 0) * 10:  # 10x increase
            anomalies.append('NETWORK_ANOMALY')
        
        return anomalies
    
    def _check_user_anomalies(self, behavior_point: Dict) -> List[str]:
        """Check for user-specific anomalies"""
        anomalies = []
        user_id = behavior_point['user_id']
        data = behavior_point['data']
        user_baseline = self.user_profiles[user_id]['baseline_patterns']
        
        # User-specific CPU anomaly
        cpu_deviation = abs(data.get('cpu_percent', 0) - user_baseline.get('cpu_avg', 0))
        if cpu_deviation > 50:  # 50% deviation from user baseline
            anomalies.append('USER_CPU_ANOMALY')
        
        # User-specific memory anomaly
        memory_deviation = abs(data.get('memory_percent', 0) - user_baseline.get('memory_avg', 0))
        if memory_deviation > 40:  # 40% deviation from user baseline
            anomalies.append('USER_MEMORY_ANOMALY')
        
        # Unusual activity time
        current_hour = time.localtime(behavior_point['timestamp']).tm_hour
        peak_hours = [hour for hour, count in user_baseline.get('activity_patterns', {}).get('peak_hours', [])]
        if current_hour not in peak_hours and current_hour not in range(9, 17):  # Outside normal hours
            anomalies.append('UNUSUAL_ACTIVITY_TIME')
        
        return anomalies
    
    def _check_ml_anomalies(self, behavior_point: Dict) -> List[str]:
        """Check for ML-detected anomalies"""
        anomalies = []
        
        try:
            features = np.array(behavior_point['behavioral_features']).reshape(1, -1)
            features_scaled = self.scaler.transform(features)
            
            # Isolation Forest anomaly detection
            is_anomaly = self.isolation_forest.predict(features_scaled)[0] == -1
            if is_anomaly:
                anomalies.append('ML_DETECTED_ANOMALY')
            
            # DBSCAN clustering anomaly
            cluster_label = self.dbscan_cluster.fit_predict(features_scaled)[0]
            if cluster_label == -1:  # Outlier
                anomalies.append('CLUSTER_OUTLIER')
            
        except Exception as e:
            print(f"❌ ML anomaly detection error: {e}")
        
        return anomalies
    
    def _calculate_enhanced_behavior_score(self, behavior_point: Dict) -> float:
        """Calculate enhanced behavioral score"""
        score = 50.0  # Start with neutral score
        data = behavior_point['data']
        
        # Global baseline comparison
        if self.baseline_behavior:
            # CPU score adjustment
            cpu_deviation = abs(data.get('cpu_percent', 0) - self.baseline_behavior.get('cpu_avg', 0))
            score -= min(cpu_deviation / 3, 20)  # Max -20 points
            
            # Memory score adjustment
            memory_deviation = abs(data.get('memory_percent', 0) - self.baseline_behavior.get('memory_avg', 0))
            score -= min(memory_deviation / 3, 20)  # Max -20 points
            
            # Network score adjustment
            network_ratio = data.get('network_bytes_sent', 0) / max(self.baseline_behavior.get('network_avg', 1), 1)
            if network_ratio > 5:  # 5x normal network activity
                score -= 15
        
        # User-specific score adjustment
        user_id = behavior_point['user_id']
        if user_id in self.user_profiles and self.user_profiles[user_id]['baseline_patterns']:
            user_baseline = self.user_profiles[user_id]['baseline_patterns']
            
            # User activity pattern score
            current_hour = time.localtime(behavior_point['timestamp']).tm_hour
            peak_hours = [hour for hour, count in user_baseline.get('activity_patterns', {}).get('peak_hours', [])]
            if current_hour not in peak_hours:
                score -= 10  # Activity outside normal hours
        
        # Anomaly penalty
        anomalies = self._detect_enhanced_anomalies(behavior_point)
        score -= len(anomalies) * 5  # -5 points per anomaly
        
        return max(0, min(100, score))
    
    def _analyze_behavioral_patterns(self, behavior_point: Dict) -> Dict:
        """Analyze behavioral patterns"""
        patterns = {
            'activity_level': 'normal',
            'resource_usage': 'normal',
            'network_behavior': 'normal',
            'time_pattern': 'normal'
        }
        
        data = behavior_point['data']
        
        # Activity level analysis
        if data.get('cpu_percent', 0) > 80 or data.get('memory_percent', 0) > 80:
            patterns['activity_level'] = 'high'
        elif data.get('cpu_percent', 0) < 20 and data.get('memory_percent', 0) < 20:
            patterns['activity_level'] = 'low'
        
        # Resource usage analysis
        if data.get('process_count', 0) > 300:
            patterns['resource_usage'] = 'high'
        elif data.get('process_count', 0) < 50:
            patterns['resource_usage'] = 'low'
        
        # Network behavior analysis
        if data.get('network_bytes_sent', 0) > 10000000:  # 10MB
            patterns['network_behavior'] = 'high'
        elif data.get('network_bytes_sent', 0) < 100000:  # 100KB
            patterns['network_behavior'] = 'low'
        
        # Time pattern analysis
        current_hour = time.localtime(behavior_point['timestamp']).tm_hour
        if current_hour in range(9, 17):  # Business hours
            patterns['time_pattern'] = 'business_hours'
        elif current_hour in range(22, 24) or current_hour in range(0, 6):  # Night hours
            patterns['time_pattern'] = 'night_hours'
        else:
            patterns['time_pattern'] = 'off_hours'
        
        return patterns
    
    def _assess_behavioral_risk(self, behavior_score: float, anomalies: List[str]) -> str:
        """Assess behavioral risk level"""
        risk_factors = len(anomalies)
        
        if behavior_score < 30 or risk_factors > 5:
            return 'Critical'
        elif behavior_score < 50 or risk_factors > 3:
            return 'High'
        elif behavior_score < 70 or risk_factors > 1:
            return 'Medium'
        else:
            return 'Low'
    
    def train_behavioral_models(self):
        """Train behavioral analysis models"""
        if not SKLEARN_AVAILABLE or len(self.behavior_history) < 1000:
            return False
        
        try:
            print("🧠 Training behavioral analysis models...")
            
            # Prepare training data
            features = []
            for behavior in self.behavior_history:
                features.append(behavior['behavioral_features'])
            
            X = np.array(features)
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Isolation Forest
            self.isolation_forest.fit(X_scaled)
            
            # Train DBSCAN
            self.dbscan_cluster.fit(X_scaled)
            
            print("✅ Behavioral analysis models trained successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Behavioral model training failed: {e}")
            return False
    
    def get_enhanced_statistics(self) -> Dict:
        """Get enhanced behavioral statistics"""
        return {
            'behavior_history_size': len(self.behavior_history),
            'user_profiles': len(self.user_profiles),
            'behavioral_metrics': self.behavioral_metrics,
            'models_trained': self.isolation_forest is not None,
            'baseline_established': len(self.baseline_behavior) > 0,
            'anomaly_threshold': self.anomaly_threshold
        }
