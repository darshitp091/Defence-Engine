"""
Real-time Hash Stream Display
"""
import sys
import os
import time
import threading
import hashlib
import secrets

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from license.license_manager import LicenseManager

class HashStreamEngine:
    def __init__(self):
        self.is_running = False
        self.hash_counter = 0
        self.seed = secrets.token_bytes(16)
        self.threads = []
        
    def start_hash_stream(self):
        """Start continuous hash stream display"""
        self.is_running = True
        self.hash_counter = 0
        
        # Start multiple hash display threads
        num_threads = 8
        
        for i in range(num_threads):
            thread = threading.Thread(target=self._hash_stream_worker, args=(i,), daemon=True)
            thread.start()
            self.threads.append(thread)
        
        print(f"Hash stream started with {num_threads} workers")
        print("Real-time quantum hashes:")
        print("=" * 100)
        
    def _hash_stream_worker(self, worker_id):
        """Generate and display hashes continuously"""
        local_count = 0
        
        while self.is_running:
            try:
                # Generate hash
                data = f"quantum_defense_{worker_id}_{local_count}_{time.time()}".encode()
                hash_result = hashlib.blake2b(data + self.seed, digest_size=32).hexdigest()
                
                # Display the hash
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] W{worker_id}: {hash_result}")
                
                local_count += 1
                self.hash_counter += 1
                
                # Small delay to make it readable
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
                time.sleep(0.1)
                
    def stop(self):
        """Stop hash stream"""
        self.is_running = False
        
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1)

def main():
    print("Defence Engine - Real-time Hash Stream")
    print("=" * 50)
    
    # License validation
    license_manager = LicenseManager()
    license_key = input("License Key: ").strip()
    
    if not license_key:
        print("Error: License key required")
        return
        
    validation_result = license_manager.validate_license(license_key)
    
    if not validation_result['valid']:
        print(f"Error: {validation_result['reason']}")
        return
        
    print("License validated. Starting hash stream...")
    print()
    
    # Start hash stream
    engine = HashStreamEngine()
    
    try:
        engine.start_hash_stream()
        
        # Run until interrupted
        while engine.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping hash stream...")
        engine.stop()
        print(f"Total hashes generated: {engine.hash_counter:,}")

if __name__ == "__main__":
    main()