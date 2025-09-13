"""
Quantum Hash Engine Demonstration
Real-time hash generation with GPU acceleration
"""
import sys
import os
import time
import threading

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.quantum_hash import QuantumHashEngine

def main():
    print("=" * 80)
    print("🔬 DEFENCE ENGINE - QUANTUM HASH DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Initialize quantum engine with display enabled
    quantum_engine = QuantumHashEngine(display_hashes=True)
    
    print("\nChoose demonstration mode:")
    print("1. 🚀 Real-time Hash Generation (Continuous)")
    print("2. 🎯 Single Hash Generation")
    print("3. 🕳️  Hash Trap Demonstration")
    print("4. 🏆 Challenge Mode (Maximum Security)")
    print("5. 📊 System Statistics")
    print("6. ❌ Exit")
    
    while True:
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            real_time_demo(quantum_engine)
        elif choice == "2":
            single_hash_demo(quantum_engine)
        elif choice == "3":
            hash_trap_demo(quantum_engine)
        elif choice == "4":
            challenge_mode_demo(quantum_engine)
        elif choice == "5":
            show_statistics(quantum_engine)
        elif choice == "6":
            quantum_engine.stop_real_time_hashing()
            print("🛡️  Quantum Defense Engine Shutdown Complete!")
            break
        else:
            print("Invalid choice. Please enter 1-6.")

def real_time_demo(quantum_engine):
    """Demonstrate real-time hash generation"""
    print("\n🚀 Starting Real-time Quantum Hash Generation...")
    print("Press Ctrl+C to stop the demonstration")
    print("=" * 60)
    
    try:
        quantum_engine.start_real_time_hashing()
        
        # Let it run and show statistics periodically
        start_time = time.time()
        while quantum_engine.is_running:
            time.sleep(10)  # Show stats every 10 seconds
            
            elapsed = time.time() - start_time
            stats = quantum_engine.get_hash_statistics()
            
            print(f"\n📊 Runtime Statistics (Running for {elapsed:.1f}s):")
            print(f"🔢 Total Patterns Generated: {stats['total_patterns']}")
            print(f"🔄 Pattern Rotations: {stats['rotation_counter']}")
            print(f"🖥️  GPU Acceleration: {'✅' if stats['gpu_enabled'] else '❌'}")
            print(f"🛡️  Security Layers: {stats['obfuscation_layers']}")
            
    except KeyboardInterrupt:
        quantum_engine.stop_real_time_hashing()
        print("\n⏹️  Real-time demonstration stopped by user")

def single_hash_demo(quantum_engine):
    """Demonstrate single hash generation"""
    print("\n🎯 Single Hash Generation Demonstration")
    
    data = input("Enter data to hash (or press Enter for default): ").strip()
    if not data:
        data = f"defence_engine_demo_{time.time()}"
    
    print(f"\n🔬 Generating quantum hashes for: '{data}'")
    print("=" * 60)
    
    # Generate different types of hashes
    start_time = time.time()
    
    quantum_hash = quantum_engine.generate_quantum_hash(data)
    binary_hash = quantum_engine.generate_binary_hash(data)
    encrypted_hash = quantum_engine.generate_encrypted_hash(data)
    
    generation_time = time.time() - start_time
    
    print(f"⚛️  Quantum Hash:")
    print(f"   {quantum_hash}")
    print(f"\n🔢 Binary Hash:")
    print(f"   {binary_hash}")
    print(f"\n🔐 Encrypted Hash:")
    print(f"   {encrypted_hash}")
    
    print(f"\n⏱️  Generation Time: {generation_time:.4f} seconds")
    print(f"🖥️  GPU Acceleration: {'✅ Used' if quantum_engine.use_gpu else '❌ CPU Only'}")

def hash_trap_demo(quantum_engine):
    """Demonstrate hash trap generation"""
    print("\n🕳️  Hash Trap Demonstration")
    
    attacker_data = input("Enter simulated attacker data: ").strip()
    if not attacker_data:
        attacker_data = "simulated_hacker_attempt"
    
    print(f"\n🎯 Deploying hash trap against: '{attacker_data}'")
    print("This will generate thousands of fake hashes to confuse attackers...")
    
    start_time = time.time()
    trap_hashes = quantum_engine.create_hash_trap(attacker_data)
    trap_time = time.time() - start_time
    
    print(f"\n✅ Hash Trap Deployment Complete!")
    print(f"🕳️  Total Trap Hashes: {len(trap_hashes)}")
    print(f"⏱️  Deployment Time: {trap_time:.2f} seconds")
    print(f"🎯 Trap Effectiveness: {len(trap_hashes) * 100} fake hash attempts")
    
    # Show sample trap hashes
    print(f"\n📋 Sample Trap Hashes:")
    for i, trap_hash in enumerate(trap_hashes[:5]):
        print(f"   {i+1}. {trap_hash[:50]}...")

def challenge_mode_demo(quantum_engine):
    """Demonstrate challenge mode"""
    print("\n🏆 CHALLENGE MODE DEMONSTRATION")
    print("Maximum security hash generation - Bring it on, hackers!")
    
    challenge_data = input("Enter challenge data (or press Enter for default): ").strip()
    if not challenge_data:
        challenge_data = "HACKER_CHALLENGE_ACCEPTED"
    
    print(f"\n🔥 Activating Challenge Mode for: '{challenge_data}'")
    print("=" * 60)
    
    start_time = time.time()
    challenge_hashes = quantum_engine.challenge_mode(challenge_data)
    challenge_time = time.time() - start_time
    
    print(f"\n🏆 Challenge Mode Results:")
    print(f"⏱️  Generation Time: {challenge_time:.2f} seconds")
    print(f"🔐 Ultra-Secure Hashes Generated: {len(challenge_hashes)}")
    print(f"🛡️  Security Level: MAXIMUM")
    print(f"💪 Message to Hackers: TRY TO BREAK THIS!")

def show_statistics(quantum_engine):
    """Show detailed system statistics"""
    print("\n📊 QUANTUM HASH ENGINE STATISTICS")
    print("=" * 50)
    
    stats = quantum_engine.get_hash_statistics()
    gpu_info = quantum_engine.gpu_info
    
    print(f"🔢 Hash Patterns Generated: {stats['total_patterns']}")
    print(f"🔄 Pattern Rotations: {stats['rotation_counter']}")
    print(f"⚛️  Quantum States: {stats['quantum_states']}")
    print(f"🛡️  Obfuscation Layers: {stats['obfuscation_layers']}")
    print(f"🏃 Engine Status: {'🟢 Running' if stats['is_running'] else '🔴 Stopped'}")
    
    print(f"\n🖥️  GPU Information:")
    print(f"   Available: {'✅ Yes' if gpu_info['available'] else '❌ No'}")
    print(f"   Type: {gpu_info['type']}")
    print(f"   Name: {gpu_info['name']}")
    
    if gpu_info['available']:
        print(f"   Memory: {gpu_info['memory'] // (1024*1024)} MB")
        print(f"   Cores: {gpu_info['cores']}")
    
    print(f"\n🔐 Security Features:")
    print(f"   ✅ Quantum-inspired hashing")
    print(f"   ✅ Binary hash generation")
    print(f"   ✅ Multi-layer encryption")
    print(f"   ✅ Real-time pattern rotation")
    print(f"   ✅ GPU acceleration support")
    print(f"   ✅ Hash trap deployment")
    print(f"   ✅ Challenge mode protection")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛡️  Quantum Defense Engine demonstration terminated by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure all dependencies are installed correctly")