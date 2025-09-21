"""
Enhanced Real-time Monitoring System
Advanced real-time system monitoring with comprehensive metrics and alerting
"""
import time
import threading
import psutil
import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import deque
import json
import hashlib
import secrets
from datetime import datetime, timedelta
import os
import sys
import socket
import subprocess

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class EnhancedRealTimeMonitor:
    """Enhanced Real-time System Monitor with Advanced Metrics"""
    
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.metrics_history = deque(maxlen=10000)  # Increased capacity
        self.alerts_history = deque(maxlen=1000)
        
        # Monitoring configuration
        self.monitoring_interval = 2  # 2-second intervals
        self.alert_thresholds = {
            'cpu_percent': 90,
            'memory_percent': 90,
            'disk_percent': 90,
            'network_bytes_per_second': 10000000,  # 10MB/s
            'process_count': 500,
            'thread_count': 1000
        }
        
        # Enhanced metrics
        self.system_metrics = {}
        self.network_metrics = {}
        self.security_metrics = {}
        self.performance_metrics = {}
        
        # Alert system
        self.alert_callbacks = []
        self.alert_cooldowns = {}
        
        print("📊 Enhanced Real-time Monitor initialized!")
        print(f"   Monitoring interval: {self.monitoring_interval}s")
        print(f"   History capacity: {self.metrics_history.maxlen}")
        print(f"   Alert thresholds: {len(self.alert_thresholds)} metrics")
    
    def start_enhanced_monitoring(self):
        """Start enhanced real-time monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._enhanced_monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("📊 Enhanced real-time monitoring started!")
    
    def stop_enhanced_monitoring(self):
        """Stop enhanced real-time monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("⏹️ Enhanced real-time monitoring stopped!")
    
    def _enhanced_monitoring_loop(self):
        """Enhanced monitoring loop with comprehensive metrics"""
        while self.is_monitoring:
            try:
                # Collect comprehensive metrics
                timestamp = time.time()
                metrics = self._collect_enhanced_metrics()
                
                # Store metrics
                self.metrics_history.append({
                    'timestamp': timestamp,
                    'metrics': metrics
                })
                
                # Analyze metrics for alerts
                self._analyze_metrics_for_alerts(metrics)
                
                # Update system state
                self._update_system_state(metrics)
                
                # Wait for next monitoring cycle
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"❌ Enhanced monitoring error: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_enhanced_metrics(self) -> Dict:
        """Collect comprehensive system metrics"""
        metrics = {
            'timestamp': time.time(),
            'system': self._collect_system_metrics(),
            'network': self._collect_network_metrics(),
            'security': self._collect_security_metrics(),
            'performance': self._collect_performance_metrics(),
            'processes': self._collect_process_metrics(),
            'filesystem': self._collect_filesystem_metrics()
        }
        
        return metrics
    
    def _collect_system_metrics(self) -> Dict:
        """Collect system-level metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Boot time
            boot_time = psutil.boot_time()
            
            return {
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'cpu_freq_current': cpu_freq.current if cpu_freq else 0,
                'cpu_freq_min': cpu_freq.min if cpu_freq else 0,
                'cpu_freq_max': cpu_freq.max if cpu_freq else 0,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'memory_used': memory.used,
                'memory_total': memory.total,
                'swap_percent': swap.percent,
                'swap_used': swap.used,
                'swap_total': swap.total,
                'boot_time': boot_time,
                'uptime': time.time() - boot_time
            }
        except Exception as e:
            print(f"❌ System metrics collection error: {e}")
            return {}
    
    def _collect_network_metrics(self) -> Dict:
        """Collect network metrics"""
        try:
            # Network I/O
            net_io = psutil.net_io_counters()
            
            # Network connections
            connections = psutil.net_connections()
            
            # Network interfaces
            interfaces = psutil.net_if_addrs()
            
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout,
                'connection_count': len(connections),
                'established_connections': len([c for c in connections if c.status == 'ESTABLISHED']),
                'listening_connections': len([c for c in connections if c.status == 'LISTEN']),
                'interface_count': len(interfaces)
            }
        except Exception as e:
            print(f"❌ Network metrics collection error: {e}")
            return {}
    
    def _collect_security_metrics(self) -> Dict:
        """Collect security-related metrics"""
        try:
            # Process analysis
            processes = list(psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']))
            
            # Suspicious processes
            suspicious_processes = []
            for proc in processes:
                try:
                    info = proc.info
                    if info['cpu_percent'] > 50 or info['memory_percent'] > 10:
                        suspicious_processes.append({
                            'pid': info['pid'],
                            'name': info['name'],
                            'username': info['username'],
                            'cpu_percent': info['cpu_percent'],
                            'memory_percent': info['memory_percent']
                        })
                except:
                    pass
            
            # Network security
            connections = psutil.net_connections()
            suspicious_connections = len([c for c in connections if c.raddr and c.status == 'ESTABLISHED'])
            
            return {
                'total_processes': len(processes),
                'suspicious_processes': len(suspicious_processes),
                'suspicious_process_list': suspicious_processes[:10],  # Top 10
                'suspicious_connections': suspicious_connections,
                'established_connections': len([c for c in connections if c.status == 'ESTABLISHED']),
                'listening_ports': len([c for c in connections if c.status == 'LISTEN'])
            }
        except Exception as e:
            print(f"❌ Security metrics collection error: {e}")
            return {}
    
    def _collect_performance_metrics(self) -> Dict:
        """Collect performance metrics"""
        try:
            # Load averages
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            
            # Process performance
            processes = list(psutil.process_iter(['pid', 'cpu_percent', 'memory_percent']))
            total_cpu = sum(p.info['cpu_percent'] for p in processes if p.info['cpu_percent'])
            total_memory = sum(p.info['memory_percent'] for p in processes if p.info['memory_percent'])
            
            return {
                'load_avg_1min': load_avg[0],
                'load_avg_5min': load_avg[1],
                'load_avg_15min': load_avg[2],
                'disk_read_bytes': disk_io.read_bytes if disk_io else 0,
                'disk_write_bytes': disk_io.write_bytes if disk_io else 0,
                'disk_read_count': disk_io.read_count if disk_io else 0,
                'disk_write_count': disk_io.write_count if disk_io else 0,
                'total_process_cpu': total_cpu,
                'total_process_memory': total_memory
            }
        except Exception as e:
            print(f"❌ Performance metrics collection error: {e}")
            return {}
    
    def _collect_process_metrics(self) -> Dict:
        """Collect process-specific metrics"""
        try:
            processes = list(psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'num_threads']))
            
            # Process statistics
            process_stats = {
                'total_processes': len(processes),
                'total_threads': sum(p.info['num_threads'] for p in processes if p.info['num_threads']),
                'unique_users': len(set(p.info['username'] for p in processes if p.info['username'])),
                'unique_names': len(set(p.info['name'] for p in processes if p.info['name']))
            }
            
            # Top processes by CPU
            top_cpu_processes = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
            process_stats['top_cpu_processes'] = [
                {
                    'pid': p.info['pid'],
                    'name': p.info['name'],
                    'cpu_percent': p.info['cpu_percent']
                }
                for p in top_cpu_processes
            ]
            
            # Top processes by memory
            top_memory_processes = sorted(processes, key=lambda p: p.info['memory_percent'], reverse=True)[:5]
            process_stats['top_memory_processes'] = [
                {
                    'pid': p.info['pid'],
                    'name': p.info['name'],
                    'memory_percent': p.info['memory_percent']
                }
                for p in top_memory_processes
            ]
            
            return process_stats
        except Exception as e:
            print(f"❌ Process metrics collection error: {e}")
            return {}
    
    def _collect_filesystem_metrics(self) -> Dict:
        """Collect filesystem metrics"""
        try:
            # Disk usage
            disk_usage = psutil.disk_usage('/')
            
            # Disk partitions
            partitions = psutil.disk_partitions()
            
            # Disk I/O per partition
            partition_io = {}
            for partition in partitions:
                try:
                    io = psutil.disk_io_counters(perdisk=True)
                    if partition.device in io:
                        partition_io[partition.device] = {
                            'read_bytes': io[partition.device].read_bytes,
                            'write_bytes': io[partition.device].write_bytes,
                            'read_count': io[partition.device].read_count,
                            'write_count': io[partition.device].write_count
                        }
                except:
                    pass
            
            return {
                'total_space': disk_usage.total,
                'used_space': disk_usage.used,
                'free_space': disk_usage.free,
                'usage_percent': (disk_usage.used / disk_usage.total) * 100,
                'partition_count': len(partitions),
                'partition_io': partition_io
            }
        except Exception as e:
            print(f"❌ Filesystem metrics collection error: {e}")
            return {}
    
    def _analyze_metrics_for_alerts(self, metrics: Dict):
        """Analyze metrics for alert conditions"""
        alerts = []
        
        # System alerts
        if 'system' in metrics:
            system = metrics['system']
            
            if system.get('cpu_percent', 0) > self.alert_thresholds['cpu_percent']:
                alerts.append({
                    'type': 'CPU_HIGH',
                    'value': system['cpu_percent'],
                    'threshold': self.alert_thresholds['cpu_percent'],
                    'severity': 'HIGH'
                })
            
            if system.get('memory_percent', 0) > self.alert_thresholds['memory_percent']:
                alerts.append({
                    'type': 'MEMORY_HIGH',
                    'value': system['memory_percent'],
                    'threshold': self.alert_thresholds['memory_percent'],
                    'severity': 'HIGH'
                })
        
        # Network alerts
        if 'network' in metrics:
            network = metrics['network']
            
            # Calculate network speed (simplified)
            if len(self.metrics_history) > 1:
                prev_metrics = self.metrics_history[-2]['metrics']
                if 'network' in prev_metrics:
                    time_diff = metrics['timestamp'] - prev_metrics['timestamp']
                    if time_diff > 0:
                        bytes_sent_diff = network['bytes_sent'] - prev_metrics['network']['bytes_sent']
                        bytes_per_second = bytes_sent_diff / time_diff
                        
                        if bytes_per_second > self.alert_thresholds['network_bytes_per_second']:
                            alerts.append({
                                'type': 'NETWORK_HIGH',
                                'value': bytes_per_second,
                                'threshold': self.alert_thresholds['network_bytes_per_second'],
                                'severity': 'MEDIUM'
                            })
        
        # Process alerts
        if 'processes' in metrics:
            processes = metrics['processes']
            
            if processes.get('total_processes', 0) > self.alert_thresholds['process_count']:
                alerts.append({
                    'type': 'PROCESS_COUNT_HIGH',
                    'value': processes['total_processes'],
                    'threshold': self.alert_thresholds['process_count'],
                    'severity': 'MEDIUM'
                })
        
        # Handle alerts
        for alert in alerts:
            self._handle_alert(alert)
    
    def _handle_alert(self, alert: Dict):
        """Handle system alerts"""
        alert_key = f"{alert['type']}_{alert['severity']}"
        
        # Check cooldown
        if alert_key in self.alert_cooldowns:
            if time.time() - self.alert_cooldowns[alert_key] < 60:  # 1-minute cooldown
                return
        
        # Set cooldown
        self.alert_cooldowns[alert_key] = time.time()
        
        # Store alert
        self.alerts_history.append({
            'timestamp': time.time(),
            'alert': alert
        })
        
        # Log alert
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🚨 ALERT [{timestamp}] {alert['type']}: {alert['value']} (threshold: {alert['threshold']})")
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"❌ Alert callback error: {e}")
    
    def _update_system_state(self, metrics: Dict):
        """Update system state based on metrics"""
        # Update system metrics
        if 'system' in metrics:
            self.system_metrics = metrics['system']
        
        # Update network metrics
        if 'network' in metrics:
            self.network_metrics = metrics['network']
        
        # Update security metrics
        if 'security' in metrics:
            self.security_metrics = metrics['security']
        
        # Update performance metrics
        if 'performance' in metrics:
            self.performance_metrics = metrics['performance']
    
    def add_alert_callback(self, callback):
        """Add alert callback function"""
        self.alert_callbacks.append(callback)
    
    def get_enhanced_statistics(self) -> Dict:
        """Get enhanced monitoring statistics"""
        return {
            'monitoring_active': self.is_monitoring,
            'metrics_history_size': len(self.metrics_history),
            'alerts_history_size': len(self.alerts_history),
            'monitoring_interval': self.monitoring_interval,
            'alert_thresholds': self.alert_thresholds,
            'system_metrics': self.system_metrics,
            'network_metrics': self.network_metrics,
            'security_metrics': self.security_metrics,
            'performance_metrics': self.performance_metrics
        }
    
    def get_recent_metrics(self, count: int = 100) -> List[Dict]:
        """Get recent metrics"""
        return list(self.metrics_history)[-count:]
    
    def get_recent_alerts(self, count: int = 50) -> List[Dict]:
        """Get recent alerts"""
        return list(self.alerts_history)[-count:]
