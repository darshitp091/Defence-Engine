"""
Defence Engine - Silent Background Protection
"""
import sys
import os
import time
import threading

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.optimized_quantum_hash import OptimizedQuantumHashEngine as QuantumHashEngine
from ai.threat_detector import AIThreatDetector
from defense.reverse_attack import ReverseAttackSystem
from license.license_manager import LicenseManager

class SilentDefenceEngine:
    def __init__(self, license_key):
        self.license_key = license_key
        self.license_manager = LicenseManager()
        self.quantum_engine = None
        self.ai_detector = None
        self.reverse_attack = None
        self.is_running = False
        
    def start(self):
        """Start silent protection"""
        # Validate license
        validation_result = self.license_manager.validate_license(self.license_key)
        
        if not validation_result['valid']:
            return False
            
        # Initialize components silently
        try:
            self.quantum_engine = QuantumHashEngine(display_hashes=False)
            self.ai_detector = AIThreatDetector()
            self.reverse_attack = ReverseAttackSystem(self.quantum_engine)
            
            # Start all protection systems
            self.quantum_engine.start_real_time_hashing()
            self.ai_detector.start_monitoring()
            self.reverse_attack.is_defending = True
            self.reverse_attack.create_crash_proof_barrier()
            
            self.is_running = True
            
            # Run silently
            while self.is_running:
                time.sleep(60)  # Check every minute
                
            return True
            
        except:
            return False
            
    def stop(self):
        """Stop protection"""
        self.is_running = False
        
        if self.quantum_engine:
            self.quantum_engine.stop_real_time_hashing()
            
        if self.ai_detector:
            self.ai_detector.stop_monitoring()
            
        if self.reverse_attack:
            self.reverse_attack.is_defending = False

def main():
    if len(sys.argv) != 2:
        print("Usage: python defence_silent.py <license_key>")
        sys.exit(1)
        
    license_key = sys.argv[1]
    engine = SilentDefenceEngine(license_key)
    
    try:
        engine.start()
    except KeyboardInterrupt:
        engine.stop()

if __name__ == "__main__":
    main()