"""
Defence Engine - Professional Security Tool
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
from config import DefenceConfig

class DefenceEngine:
    def __init__(self):
        self.license_manager = LicenseManager()
        self.quantum_engine = None
        self.ai_detector = None
        self.reverse_attack = None
        self.is_running = False
        
    def start(self):
        """Start Defence Engine"""
        print("Defence Engine v1.0")
        print("Advanced Security Protection System")
        
        # Ask for hash display option
        show_hashes = input("Show real-time hashes? (y/N): ").strip().lower()
        display_hashes = show_hashes == 'y'
        
        # Get license key
        license_key = input("License Key: ").strip()
        
        if not license_key:
            print("Error: License key required")
            return False
            
        # Validate license
        validation_result = self.license_manager.validate_license(license_key)
        
        if not validation_result['valid']:
            print(f"Error: {validation_result['reason']}")
            return False
            
        print("License validated. Starting protection...")
        
        # Initialize components
        try:
            self.quantum_engine = QuantumHashEngine(display_hashes=display_hashes)
            self.ai_detector = AIThreatDetector()
            self.reverse_attack = ReverseAttackSystem(self.quantum_engine)
            
            # Start all protection systems
            self.quantum_engine.start_real_time_hashing()
            self.ai_detector.start_monitoring()
            self.reverse_attack.is_defending = True
            self.reverse_attack.create_crash_proof_barrier()
            
            self.is_running = True
            
            print("Defence Engine active. System protected.")
            print("Press Ctrl+C to stop.")
            
            # Run protection loop
            self._protection_loop()
            
            return True
            
        except Exception as e:
            print(f"Error: Failed to start protection - {str(e)}")
            return False
            
    def _protection_loop(self):
        """Main protection loop"""
        try:
            while self.is_running:
                time.sleep(5)
                
                # Show hash generation status
                if self.quantum_engine:
                    total_hashes = getattr(self.quantum_engine, 'total_hashes_generated', 0)
                    threat_count = len(self.reverse_attack.active_attacks) if self.reverse_attack else 0
                    
                    status = f"Hashes: {total_hashes:,} | Threats: {threat_count} | Status: Active"
                    print(f"\r{status}", end="", flush=True)
                
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """Stop Defence Engine"""
        self.is_running = False
        
        if self.quantum_engine:
            self.quantum_engine.stop_real_time_hashing()
            
        if self.ai_detector:
            self.ai_detector.stop_monitoring()
            
        if self.reverse_attack:
            self.reverse_attack.is_defending = False
            
        print("\nDefence Engine stopped.")

def main():
    engine = DefenceEngine()
    engine.start()

if __name__ == "__main__":
    main()