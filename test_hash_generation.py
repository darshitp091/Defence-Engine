"""
Test Hash Generation Directly
"""
import sys
import os
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.quantum_hash import QuantumHashEngine

def test_hash_generation():
    print("Testing Quantum Hash Generation...")
    
    # Test with display disabled (like in defence.py)
    engine = QuantumHashEngine(display_hashes=False)
    
    print("Starting hash generation...")
    engine.start_real_time_hashing()
    
    # Wait and check hash patterns
    for i in range(10):
        time.sleep(1)
        hash_count = len(engine.hash_patterns) if hasattr(engine, 'hash_patterns') else 0
        print(f"Second {i+1}: Hashes generated: {hash_count}")
    
    engine.stop_real_time_hashing()
    
    final_count = len(engine.hash_patterns) if hasattr(engine, 'hash_patterns') else 0
    print(f"\nFinal hash count: {final_count}")
    
    if final_count > 0:
        print("✅ Hash generation working correctly!")
        # Show a sample hash
        sample = engine.hash_patterns[0]
        print(f"Sample hash: {sample['quantum'][:50]}...")
    else:
        print("❌ No hashes generated - there's an issue!")

if __name__ == "__main__":
    test_hash_generation()