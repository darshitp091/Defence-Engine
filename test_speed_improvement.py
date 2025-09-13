"""
Test Speed Improvement - Compare original vs optimized hash generation
"""
import sys
import os
import time
from typing import Dict

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_original_engine():
    """Test original quantum hash engine"""
    print("🔬 Testing Original Quantum Hash Engine...")
    print("=" * 50)
    
    try:
        from core.quantum_hash import QuantumHashEngine
        
        # Initialize original engine
        original_engine = QuantumHashEngine(display_hashes=False)
        
        # Test single hash generation
        start_time = time.time()
        test_hash = original_engine.generate_quantum_hash("test_data_12345")
        single_time = time.time() - start_time
        
        print(f"✅ Single hash generation: {single_time*1000:.2f}ms")
        
        # Test batch generation
        start_time = time.time()
        for i in range(100):
            original_engine.generate_quantum_hash(f"test_data_{i}")
        batch_time = time.time() - start_time
        hashes_per_second = 100 / batch_time
        
        print(f"✅ Batch generation (100 hashes): {batch_time:.2f}s")
        print(f"✅ Hashes per second: {hashes_per_second:.0f}")
        
        return {
            'single_hash_time': single_time,
            'batch_time': batch_time,
            'hashes_per_second': hashes_per_second,
            'engine_type': 'original'
        }
        
    except Exception as e:
        print(f"❌ Original engine test failed: {e}")
        return None

def test_optimized_engine():
    """Test optimized quantum hash engine"""
    print("\n🚀 Testing Optimized Quantum Hash Engine...")
    print("=" * 50)
    
    try:
        from core.optimized_quantum_hash import OptimizedQuantumHashEngine
        
        # Initialize optimized engine
        optimized_engine = OptimizedQuantumHashEngine(display_hashes=False)
        
        # Test single hash generation
        start_time = time.time()
        test_hash = optimized_engine.generate_quantum_hash("test_data_12345")
        single_time = time.time() - start_time
        
        print(f"✅ Single hash generation: {single_time*1000:.2f}ms")
        
        # Test batch generation
        start_time = time.time()
        for i in range(100):
            optimized_engine.generate_quantum_hash(f"test_data_{i}")
        batch_time = time.time() - start_time
        hashes_per_second = 100 / batch_time
        
        print(f"✅ Batch generation (100 hashes): {batch_time:.2f}s")
        print(f"✅ Hashes per second: {hashes_per_second:.0f}")
        
        # Get cache statistics
        cache_stats = optimized_engine.optimized_cache.get_cache_stats()
        print(f"✅ Cache hit rate: {cache_stats['hit_rate']:.2%}")
        print(f"✅ Pre-computed hashes: {cache_stats['precomputed_size']:,}")
        
        return {
            'single_hash_time': single_time,
            'batch_time': batch_time,
            'hashes_per_second': hashes_per_second,
            'cache_hit_rate': cache_stats['hit_rate'],
            'precomputed_hashes': cache_stats['precomputed_size'],
            'engine_type': 'optimized'
        }
        
    except Exception as e:
        print(f"❌ Optimized engine test failed: {e}")
        return None

def test_high_cache_hit_scenario():
    """Test optimized engine with high cache hit rate"""
    print("\n🎯 Testing High Cache Hit Scenario...")
    print("=" * 50)
    
    try:
        from core.optimized_quantum_hash import OptimizedQuantumHashEngine
        
        # Initialize optimized engine
        optimized_engine = OptimizedQuantumHashEngine(display_hashes=False)
        
        # Test with high cache hit rate (using pre-computed patterns)
        start_time = time.time()
        for i in range(1000):
            # Use pre-computed patterns for high cache hit rate
            optimized_engine.generate_quantum_hash(f"password_{i % 1000}")
        batch_time = time.time() - start_time
        hashes_per_second = 1000 / batch_time
        
        print(f"✅ High cache hit test (1000 hashes): {batch_time:.2f}s")
        print(f"✅ Hashes per second: {hashes_per_second:.0f}")
        
        # Get cache statistics
        cache_stats = optimized_engine.optimized_cache.get_cache_stats()
        print(f"✅ Cache hit rate: {cache_stats['hit_rate']:.2%}")
        print(f"✅ Cache hits: {cache_stats['cache_hits']:,}")
        print(f"✅ Cache misses: {cache_stats['cache_misses']:,}")
        
        return {
            'batch_time': batch_time,
            'hashes_per_second': hashes_per_second,
            'cache_hit_rate': cache_stats['hit_rate'],
            'cache_hits': cache_stats['cache_hits'],
            'cache_misses': cache_stats['cache_misses'],
            'scenario': 'high_cache_hit'
        }
        
    except Exception as e:
        print(f"❌ High cache hit test failed: {e}")
        return None

def compare_results(original_results: Dict, optimized_results: Dict, cache_results: Dict):
    """Compare test results"""
    print("\n📊 PERFORMANCE COMPARISON")
    print("=" * 60)
    
    if original_results and optimized_results:
        # Calculate improvements
        speed_improvement = optimized_results['hashes_per_second'] / original_results['hashes_per_second']
        time_improvement = original_results['batch_time'] / optimized_results['batch_time']
        
        print(f"Original Engine:")
        print(f"  Hashes per second: {original_results['hashes_per_second']:.0f}")
        print(f"  Batch time (100 hashes): {original_results['batch_time']:.2f}s")
        
        print(f"\nOptimized Engine:")
        print(f"  Hashes per second: {optimized_results['hashes_per_second']:.0f}")
        print(f"  Batch time (100 hashes): {optimized_results['batch_time']:.2f}s")
        print(f"  Cache hit rate: {optimized_results['cache_hit_rate']:.2%}")
        print(f"  Pre-computed hashes: {optimized_results['precomputed_hashes']:,}")
        
        print(f"\n🚀 PERFORMANCE IMPROVEMENT:")
        print(f"  Speed improvement: {speed_improvement:.1f}x faster")
        print(f"  Time improvement: {time_improvement:.1f}x faster")
        
        if cache_results:
            print(f"\n🎯 HIGH CACHE HIT SCENARIO:")
            print(f"  Hashes per second: {cache_results['hashes_per_second']:.0f}")
            print(f"  Cache hit rate: {cache_results['cache_hit_rate']:.2%}")
            print(f"  Cache hits: {cache_results['cache_hits']:,}")
            print(f"  Cache misses: {cache_results['cache_misses']:,}")
            
            # Calculate improvement with high cache hit rate
            cache_speed_improvement = cache_results['hashes_per_second'] / original_results['hashes_per_second']
            print(f"  Cache-optimized speed improvement: {cache_speed_improvement:.1f}x faster")
        
        print("\n" + "=" * 60)
        
        if speed_improvement >= 10:
            print("🎉 EXCELLENT! Significant speed improvement achieved!")
        elif speed_improvement >= 5:
            print("✅ GOOD! Notable speed improvement achieved!")
        else:
            print("⚠️ Moderate speed improvement achieved.")
        
        return {
            'speed_improvement': speed_improvement,
            'time_improvement': time_improvement,
            'cache_hit_rate': optimized_results.get('cache_hit_rate', 0),
            'precomputed_hashes': optimized_results.get('precomputed_hashes', 0)
        }
    
    return None

def main():
    """Run speed improvement tests"""
    print("⚡ DEFENCE ENGINE SPEED IMPROVEMENT TEST")
    print("=" * 60)
    print("Comparing original vs optimized hash generation performance")
    print("=" * 60)
    
    # Test original engine
    original_results = test_original_engine()
    
    # Test optimized engine
    optimized_results = test_optimized_engine()
    
    # Test high cache hit scenario
    cache_results = test_high_cache_hit_scenario()
    
    # Compare results
    comparison = compare_results(original_results, optimized_results, cache_results)
    
    if comparison:
        print(f"\n🏆 FINAL RESULTS:")
        print(f"Speed Improvement: {comparison['speed_improvement']:.1f}x")
        print(f"Cache Hit Rate: {comparison['cache_hit_rate']:.2%}")
        print(f"Pre-computed Hashes: {comparison['precomputed_hashes']:,}")
        
        if comparison['speed_improvement'] >= 50:
            print("🎉 MISSION ACCOMPLISHED! 50x+ speed improvement achieved!")
        elif comparison['speed_improvement'] >= 10:
            print("🚀 EXCELLENT! 10x+ speed improvement achieved!")
        else:
            print("✅ Good speed improvement achieved!")
    
    print("\n" + "=" * 60)
    print("✅ Speed improvement test completed!")

if __name__ == "__main__":
    main()
