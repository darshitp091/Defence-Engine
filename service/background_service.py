"""
Background Service for Defence Engine
Silent operation with comprehensive monitoring
"""
import sys
import os
import time
import threading
import logging
from typing import Optional
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.quantum_hash import QuantumHashEngine
from ai.threat_detector import AIThreatDetector
from defense.reverse_attack import ReverseAttackSystem
from license.license_manager import LicenseManager
from config import DefenceConfig

class DefenceBackgroundService:
    """Background service for Defence Engine"""
    
    def __init__(self, license_key: str, gemini_api_key: Optional[str] = None):
        self.license_key = license_key
        self.gemini_api_key = gemini_api_key
        
        # Initialize components
        self.license_manager = LicenseManager()
        self.quantum_engine = None
        self.ai_detector = None
        self.reverse_attack = None
        
        # Service state
        self.is_running = False
        self.service_thread = None
        
        # Setup logging
        self._setup_logging()
        
        # Statistics
        self.start_time = None
        self.total_uptime = 0
        self.restart_count = 0
        
        print("🔧 Defence Engine Background Service initialized!")
    
    def _setup_logging(self):
        """Setup logging for the service"""
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/defence_service.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('DefenceService')
        self.logger.info("Defence Engine Background Service started")
    
    def run_forever(self):
        """Run the service forever with auto-restart"""
        print("🚀 Starting Defence Engine Background Service...")
        print("Press Ctrl+C to stop the service")
        
        try:
            while True:
                try:
                    self._run_service_cycle()
                except Exception as e:
                    self.logger.error(f"Service cycle error: {e}")
                    self.restart_count += 1
                    print(f"⚠️ Service error, restarting... (restart #{self.restart_count})")
                    time.sleep(10)  # Wait before restart
                    
        except KeyboardInterrupt:
            print("\n🛑 Service shutdown requested by user")
            self._shutdown_service()
        except Exception as e:
            self.logger.error(f"Fatal service error: {e}")
            print(f"❌ Fatal error: {e}")
        finally:
            self._cleanup()
    
    def _run_service_cycle(self):
        """Run a single service cycle"""
        # Validate license
        if not self._validate_license():
            raise Exception("License validation failed")
        
        # Initialize components
        self._initialize_components()
        
        # Start service
        self._start_service()
        
        # Keep running
        while self.is_running:
            try:
                self._monitor_service_health()
                time.sleep(30)  # Health check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                time.sleep(10)
    
    def _validate_license(self) -> bool:
        """Validate the license key"""
        try:
            validation_result = self.license_manager.validate_license(self.license_key)
            
            if not validation_result['valid']:
                self.logger.error(f"License validation failed: {validation_result['reason']}")
                return False
            
            self.logger.info(f"License validated for user: {validation_result['license_data']['user_id']}")
            return True
            
        except Exception as e:
            self.logger.error(f"License validation error: {e}")
            return False
    
    def _initialize_components(self):
        """Initialize all Defence Engine components"""
        try:
            self.logger.info("Initializing Defence Engine components...")
            
            # Initialize quantum hash engine (silent mode)
            self.quantum_engine = QuantumHashEngine(display_hashes=False)
            self.logger.info("✅ Quantum Hash Engine initialized")
            
            # Initialize AI threat detector
            self.ai_detector = AIThreatDetector(self.gemini_api_key)
            self.logger.info("✅ AI Threat Detector initialized")
            
            # Initialize reverse attack system
            self.reverse_attack = ReverseAttackSystem(self.quantum_engine)
            self.logger.info("✅ Reverse Attack System initialized")
            
            self.logger.info("All components initialized successfully!")
            
        except Exception as e:
            self.logger.error(f"Component initialization error: {e}")
            raise
    
    def _start_service(self):
        """Start the Defence Engine service"""
        try:
            self.logger.info("Starting Defence Engine service...")
            
            # Start quantum hash engine
            self.quantum_engine.start_real_time_hashing()
            self.logger.info("✅ Quantum Hash Engine started")
            
            # Start AI threat detection
            self.ai_detector.start_monitoring()
            self.logger.info("✅ AI Threat Detection started")
            
            # Start reverse attack system
            self.reverse_attack.create_crash_proof_barrier()
            self.logger.info("✅ Reverse Attack System activated")
            
            # Set service state
            self.is_running = True
            self.start_time = time.time()
            
            self.logger.info("🛡️ Defence Engine service is now active and protecting the system!")
            
            # Log service statistics
            self._log_service_statistics()
            
        except Exception as e:
            self.logger.error(f"Service start error: {e}")
            raise
    
    def _monitor_service_health(self):
        """Monitor service health and performance"""
        try:
            # Check component health
            if not self.quantum_engine or not self.quantum_engine.is_running:
                self.logger.warning("⚠️ Quantum Hash Engine not running")
                return
            
            if not self.ai_detector or not self.ai_detector.is_monitoring:
                self.logger.warning("⚠️ AI Threat Detector not monitoring")
                return
            
            if not self.reverse_attack or not self.reverse_attack.is_defending:
                self.logger.warning("⚠️ Reverse Attack System not defending")
                return
            
            # Log periodic statistics
            if int(time.time()) % 300 == 0:  # Every 5 minutes
                self._log_periodic_statistics()
            
        except Exception as e:
            self.logger.error(f"Health monitoring error: {e}")
    
    def _log_service_statistics(self):
        """Log service startup statistics"""
        try:
            # Get system information
            import psutil
            
            stats = {
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'disk_total': psutil.disk_usage('/').total,
                'license_key': self.license_key[:20] + "...",
                'gemini_api_available': self.gemini_api_key is not None
            }
            
            self.logger.info(f"Service Statistics: {stats}")
            
        except Exception as e:
            self.logger.error(f"Statistics logging error: {e}")
    
    def _log_periodic_statistics(self):
        """Log periodic service statistics"""
        try:
            # Get component statistics
            quantum_stats = self.quantum_engine.get_hash_statistics()
            threat_stats = self.ai_detector.get_threat_statistics()
            defense_stats = self.reverse_attack.get_defense_statistics()
            
            # Calculate uptime
            uptime = time.time() - self.start_time if self.start_time else 0
            
            stats = {
                'uptime_seconds': int(uptime),
                'total_hashes': quantum_stats.get('total_hashes_generated', 0),
                'threats_detected': threat_stats.get('total_threats_detected', 0),
                'active_attacks': defense_stats.get('active_attacks', 0),
                'honeypot_connections': defense_stats.get('honeypot_network', {}).get('total_connections', 0)
            }
            
            self.logger.info(f"Periodic Statistics: {stats}")
            
        except Exception as e:
            self.logger.error(f"Periodic statistics error: {e}")
    
    def _shutdown_service(self):
        """Shutdown the service gracefully"""
        self.logger.info("🛑 Shutting down Defence Engine service...")
        
        self.is_running = False
        
        # Stop components
        if self.quantum_engine:
            try:
                self.quantum_engine.stop_real_time_hashing()
                self.logger.info("✅ Quantum Hash Engine stopped")
            except Exception as e:
                self.logger.error(f"Quantum engine stop error: {e}")
        
        if self.ai_detector:
            try:
                self.ai_detector.stop_monitoring()
                self.logger.info("✅ AI Threat Detector stopped")
            except Exception as e:
                self.logger.error(f"AI detector stop error: {e}")
        
        if self.reverse_attack:
            try:
                self.reverse_attack.stop_defense()
                self.logger.info("✅ Reverse Attack System stopped")
            except Exception as e:
                self.logger.error(f"Reverse attack stop error: {e}")
        
        self.logger.info("🛡️ Defence Engine service shutdown complete")
    
    def _cleanup(self):
        """Cleanup resources"""
        try:
            # Log final statistics
            if self.start_time:
                total_uptime = time.time() - self.start_time
                self.logger.info(f"Total service uptime: {int(total_uptime)} seconds")
            
            self.logger.info(f"Service restarts: {self.restart_count}")
            
            # Close logging
            logging.shutdown()
            
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    def get_service_status(self) -> dict:
        """Get current service status"""
        try:
            status = {
                'is_running': self.is_running,
                'start_time': self.start_time,
                'uptime': time.time() - self.start_time if self.start_time else 0,
                'restart_count': self.restart_count,
                'license_key': self.license_key[:20] + "...",
                'components': {
                    'quantum_engine': self.quantum_engine is not None and self.quantum_engine.is_running,
                    'ai_detector': self.ai_detector is not None and self.ai_detector.is_monitoring,
                    'reverse_attack': self.reverse_attack is not None and self.reverse_attack.is_defending
                }
            }
            
            # Add component statistics if available
            if self.quantum_engine:
                status['quantum_stats'] = self.quantum_engine.get_hash_statistics()
            
            if self.ai_detector:
                status['threat_stats'] = self.ai_detector.get_threat_statistics()
            
            if self.reverse_attack:
                status['defense_stats'] = self.reverse_attack.get_defense_statistics()
            
            return status
            
        except Exception as e:
            self.logger.error(f"Status retrieval error: {e}")
            return {'error': str(e)}
