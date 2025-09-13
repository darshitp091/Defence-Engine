"""
Speed Analysis Tool for Hash Generation
Analyzes current performance and identifies optimization opportunities
"""
import sys
import os
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
import numpy as np
from typing import Dict, List, Tuple

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.quantum_hash import QuantumHashEngine

class SpeedAnalyzer:
    """Analyzes hash generation speed and performance bottlenecks"""
    
    def __init__(self):
        self.quantum_engine = QuantumHashEngine(display_hashes=False)
        self.results = {}
        
    def analyze_current_speed(self) -> Dict:
        """Analyze current hash generation speed"""
        print("🔍 Analyzing Current Hash Generation Speed...")
        print("=" * 60)
        
        # Test different hash types
        test_data = "speed_test_data_12345"
        duration = 5  # seconds
        
        results = {}
        
        # 1. Single hash generation
        print("📊 Testing single hash generation...")
        start_time = time.time()
        hash_result = self.quantum_engine.generate_quantum_hash(test_data)
        single_time = time.time() - start_time
        results['single_hash_time'] = single_time
        print(f"   Single hash time: {single_time*1000:.2f}ms")
        
        # 2. Multiple hash generation (sequential)
        print("📊 Testing sequential hash generation...")
        start_time = time.time()
        for i in range(100):
            self.quantum_engine.generate_quantum_hash(f"{test_data}_{i}")
        sequential_time = time.time() - start_time
        results['sequential_100_hashes'] = sequential_time
        results['sequential_hashes_per_second'] = 100 / sequential_time
        print(f"   Sequential 100 hashes: {sequential_time:.2f}s ({100/sequential_time:.0f} hashes/sec)")
        
        # 3. Threaded hash generation
        print("📊 Testing threaded hash generation...")
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            for i in range(100):
                future = executor.submit(self.quantum_engine.generate_quantum_hash, f"{test_data}_{i}")
                futures.append(future)
            
            # Wait for completion
            for future in futures:
                future.result()
        
        threaded_time = time.time() - start_time
        results['threaded_100_hashes'] = threaded_time
        results['threaded_hashes_per_second'] = 100 / threaded_time
        print(f"   Threaded 100 hashes: {threaded_time:.2f}s ({100/threaded_time:.0f} hashes/sec)")
        
        # 4. Real-time hashing performance
        print("📊 Testing real-time hashing performance...")
        start_time = time.time()
        self.quantum_engine.start_real_time_hashing()
        time.sleep(duration)
        self.quantum_engine.stop_real_time_hashing()
        realtime_time = time.time() - start_time
        
        stats = self.quantum_engine.get_hash_statistics()
        realtime_hashes = stats['total_hashes_generated']
        results['realtime_hashes_per_second'] = realtime_hashes / realtime_time
        results['realtime_total_hashes'] = realtime_hashes
        print(f"   Real-time hashing: {realtime_hashes:,} hashes in {realtime_time:.2f}s ({realtime_hashes/realtime_time:.0f} hashes/sec)")
        
        # 5. System resource analysis
        print("📊 Analyzing system resources...")
        cpu_count = multiprocessing.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        results['cpu_cores'] = cpu_count
        results['memory_gb'] = memory_gb
        print(f"   CPU cores: {cpu_count}")
        print(f"   Memory: {memory_gb:.1f}GB")
        
        # 6. Post-quantum hash performance
        print("📊 Testing post-quantum hash performance...")
        start_time = time.time()
        for i in range(10):
            self.quantum_engine.generate_post_quantum_hash(f"{test_data}_{i}")
        pq_time = time.time() - start_time
        results['post_quantum_10_hashes'] = pq_time
        results['post_quantum_hashes_per_second'] = 10 / pq_time
        print(f"   Post-quantum 10 hashes: {pq_time:.2f}s ({10/pq_time:.0f} hashes/sec)")
        
        self.results = results
        return results
    
    def identify_bottlenecks(self) -> List[str]:
        """Identify performance bottlenecks"""
        print("\n🔍 Identifying Performance Bottlenecks...")
        print("=" * 60)
        
        bottlenecks = []
        
        # Check if threading helps
        if self.results.get('threaded_hashes_per_second', 0) < self.results.get('sequential_hashes_per_second', 0) * 2:
            bottlenecks.append("Threading not providing expected speedup - possible GIL issues")
        
        # Check if real-time is slower than expected
        if self.results.get('realtime_hashes_per_second', 0) < 10000:
            bottlenecks.append("Real-time hashing slower than expected - possible display overhead")
        
        # Check post-quantum performance
        if self.results.get('post_quantum_hashes_per_second', 0) < 100:
            bottlenecks.append("Post-quantum hashing very slow - complex algorithms")
        
        # Check CPU utilization
        if self.results.get('cpu_cores', 0) > 4 and self.results.get('threaded_hashes_per_second', 0) < 50000:
            bottlenecks.append("Not utilizing all CPU cores effectively")
        
        # Check memory usage
        if self.results.get('memory_gb', 0) > 8 and self.results.get('realtime_hashes_per_second', 0) < 100000:
            bottlenecks.append("Not utilizing available memory effectively")
        
        for i, bottleneck in enumerate(bottlenecks, 1):
            print(f"   {i}. {bottleneck}")
        
        return bottlenecks
    
    def calculate_optimization_targets(self) -> Dict:
        """Calculate optimization targets for 2000x improvement"""
        print("\n🎯 Calculating Optimization Targets...")
        print("=" * 60)
        
        current_speed = self.results.get('realtime_hashes_per_second', 1000)
        target_speed = current_speed * 2000
        
        targets = {
            'current_speed': current_speed,
            'target_speed': target_speed,
            'improvement_factor': 2000,
            'optimization_areas': []
        }
        
        print(f"   Current speed: {current_speed:,.0f} hashes/sec")
        print(f"   Target speed: {target_speed:,.0f} hashes/sec")
        print(f"   Required improvement: {2000}x")
        
        # Identify optimization areas
        if current_speed < 10000:
            targets['optimization_areas'].append("Implement vectorized operations")
        if current_speed < 50000:
            targets['optimization_areas'].append("Optimize threading and multiprocessing")
        if current_speed < 100000:
            targets['optimization_areas'].append("Implement GPU acceleration")
        if current_speed < 500000:
            targets['optimization_areas'].append("Use SIMD instructions")
        if current_speed < 1000000:
            targets['optimization_areas'].append("Implement memory pooling")
        if current_speed < 2000000:
            targets['optimization_areas'].append("Use lock-free algorithms")
        
        print("\n   Optimization areas identified:")
        for i, area in enumerate(targets['optimization_areas'], 1):
            print(f"   {i}. {area}")
        
        return targets

def main():
    """Run speed analysis"""
    print("⚡ HASH GENERATION SPEED ANALYSIS")
    print("=" * 60)
    print("Analyzing current performance and identifying optimization opportunities")
    print("=" * 60)
    
    analyzer = SpeedAnalyzer()
    
    # Analyze current speed
    results = analyzer.analyze_current_speed()
    
    # Identify bottlenecks
    bottlenecks = analyzer.identify_bottlenecks()
    
    # Calculate optimization targets
    targets = analyzer.calculate_optimization_targets()
    
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY:")
    print(f"Current Speed: {results.get('realtime_hashes_per_second', 0):,.0f} hashes/sec")
    print(f"Target Speed: {targets['target_speed']:,.0f} hashes/sec")
    print(f"Bottlenecks Found: {len(bottlenecks)}")
    print(f"Optimization Areas: {len(targets['optimization_areas'])}")
    print("=" * 60)

if __name__ == "__main__":
    main()
