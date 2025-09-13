"""
Ultra-Fast Hash Generation Speed Test
"""
import sys
import os
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.quantum_hash import QuantumHashEngine

def speed_test():
    print("Ultra-Fast Hash Generation Speed Test")
    print("=" * 50)
    
    # Test with display enabled to see performance
    engine = QuantumHashEngine(display_hashes=True)
    
    print("Starting ultra-fast hash generation...")
    print("Target: 200,000-500,000 hashes per minute")
    print("=" * 50)
    
    start_time = time.time()
    engine.start_real_time_hashing()
    
    # Test for 30 seconds
    test_duration = 30
    print(f"Running speed test for {test_duration} seconds...")
    
    for i in range(test_duration):
        time.sleep(1)
        # Use the actual total hash count, not just stored patterns
        current_count = getattr(engine, 'total_hashes_generated', 0)
        elapsed = i + 1
        
        if current_count > 0:
            hashes_per_second = current_count / elapsed
            hashes_per_minute = hashes_per_second * 60
            
            print(f"Second {elapsed:2d}: {current_count:,} hashes | {hashes_per_second:,.0f} h/s | {hashes_per_minute:,.0f} h/min")
    
    engine.stop_real_time_hashing()
    
    # Final results
    total_time = time.time() - start_time
    final_count = getattr(engine, 'total_hashes_generated', 0)
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    print(f"Total hashes generated: {final_count:,}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average speed: {final_count/total_time:.0f} hashes/second")
    print(f"Average speed: {(final_count/total_time)*60:.0f} hashes/minute")
    
    # Check if we hit the target
    target_min = 200000
    target_max = 500000
    actual_per_minute = (final_count/total_time) * 60
    
    if actual_per_minute >= target_min:
        print(f"✅ SUCCESS: Exceeded minimum target of {target_min:,} h/min")
        if actual_per_minute >= target_max:
            print(f"🚀 EXCELLENT: Exceeded maximum target of {target_max:,} h/min")
    else:
        print(f"❌ Below target: Need {target_min:,} h/min, got {actual_per_minute:.0f} h/min")
    
    print("=" * 50)

if __name__ == "__main__":
    speed_test()