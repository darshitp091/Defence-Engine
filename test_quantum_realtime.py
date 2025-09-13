"""
Test Real-time Quantum Hash Generation
"""
import sys
import os
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.quantum_hash import QuantumHashEngine

def test_realtime_hashing():
    print("🔬 Testing Real-time Quantum Hash Generation")
    print("=" * 60)
    
    # Initialize quantum engine
    quantum_engine = QuantumHashEngine(display_hashes=True)
    
    print("\n🚀 Starting 10-second real-time hash demonstration...")
    
    # Start real-time hashing
    quantum_engine.start_real_time_hashing()
    
    # Let it run for 10 seconds
    time.sleep(10)
    
    # Stop hashing
    quantum_engine.stop_real_time_hashing()
    
    # Show statistics
    stats = quantum_engine.get_hash_statistics()
    print(f"\n📊 Final Statistics:")
    print(f"🔢 Total Patterns Generated: {stats['total_patterns']}")
    print(f"🔄 Pattern Rotations: {stats['rotation_counter']}")
    print(f"🖥️  GPU Acceleration: {'✅' if stats['gpu_enabled'] else '❌'}")
    print(f"🛡️  Security Layers: {stats['obfuscation_layers']}")
    
    print("\n✅ Real-time quantum hash test completed!")

if __name__ == "__main__":
    test_realtime_hashing()