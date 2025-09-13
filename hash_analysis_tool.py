"""
Advanced Hash Analysis and Cracking Tool
Analyzes and attempts to crack hashes using quantum techniques
"""
import sys
import os
import time
import hashlib
import secrets
import itertools
import string
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
import threading

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.quantum_hash import QuantumHashEngine

class HashAnalyzer:
    """Advanced hash analysis system"""
    
    def __init__(self):
        self.quantum_engine = QuantumHashEngine(display_hashes=False)
        self.hash_database = {}
        self.cracking_results = {}
        
    def analyze_hash(self, hash_value: str) -> Dict:
        """Analyze hash to determine type and characteristics"""
        print(f"🔍 Analyzing hash: {hash_value[:50]}...")
        
        analysis = {
            'hash_value': hash_value,
            'length': len(hash_value),
            'character_set': self._analyze_character_set(hash_value),
            'entropy': self._calculate_entropy(hash_value),
            'likely_algorithm': self._identify_algorithm(hash_value),
            'crack_difficulty': self._assess_crack_difficulty(hash_value),
            'quantum_resistance': self._assess_quantum_resistance(hash_value)
        }
        
        return analysis
    
    def _analyze_character_set(self, hash_value: str) -> Dict:
        """Analyze character set used in hash"""
        char_counts = {}
        for char in hash_value:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Determine character set type
        if all(c in string.hexdigits for c in hash_value):
            char_set = "hexadecimal"
        elif all(c in string.ascii_letters + string.digits + '+/=' for c in hash_value):
            char_set = "base64"
        elif all(c in '01' for c in hash_value):
            char_set = "binary"
        else:
            char_set = "mixed"
        
        return {
            'type': char_set,
            'unique_chars': len(char_counts),
            'most_common': max(char_counts.items(), key=lambda x: x[1]) if char_counts else None
        }
    
    def _calculate_entropy(self, hash_value: str) -> float:
        """Calculate entropy of hash"""
        char_counts = {}
        for char in hash_value:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0
        length = len(hash_value)
        for count in char_counts.values():
            probability = count / length
            if probability > 0:
                # Use log2 for proper entropy calculation
                import math
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _identify_algorithm(self, hash_value: str) -> str:
        """Identify likely hash algorithm"""
        length = len(hash_value)
        
        # Common hash algorithm lengths
        algorithm_map = {
            32: "MD5",
            40: "SHA-1",
            64: "SHA-256",
            96: "SHA-384",
            128: "SHA-512",
            43: "Base64 encoded",
            44: "Base64 encoded (with padding)"
        }
        
        return algorithm_map.get(length, f"Unknown (length: {length})")
    
    def _assess_crack_difficulty(self, hash_value: str) -> str:
        """Assess difficulty of cracking hash"""
        length = len(hash_value)
        entropy = self._calculate_entropy(hash_value)
        
        if length < 32:
            return "Easy"
        elif length < 64:
            return "Medium"
        elif length < 128:
            return "Hard"
        else:
            return "Very Hard"
    
    def _assess_quantum_resistance(self, hash_value: str) -> str:
        """Assess quantum resistance of hash"""
        length = len(hash_value)
        
        if length < 64:
            return "Not quantum resistant"
        elif length < 128:
            return "Partially quantum resistant"
        else:
            return "Quantum resistant"

class HashCracker:
    """Advanced hash cracking system"""
    
    def __init__(self, quantum_engine: QuantumHashEngine):
        self.quantum_engine = quantum_engine
        self.cracking_active = False
        self.cracked_hashes = {}
        
    def brute_force_attack(self, target_hash: str, charset: str = string.ascii_lowercase, 
                          max_length: int = 6, threads: int = 8) -> Optional[str]:
        """Brute force attack on hash"""
        print(f"🔨 Starting brute force attack on hash: {target_hash[:20]}...")
        print(f"Character set: {charset[:20]}...")
        print(f"Max length: {max_length}, Threads: {threads}")
        
        self.cracking_active = True
        start_time = time.time()
        
        # Use ThreadPoolExecutor for parallel cracking
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for length in range(1, max_length + 1):
                future = executor.submit(self._brute_force_worker, target_hash, charset, length)
                futures.append(future)
            
            # Wait for results
            for future in futures:
                result = future.result()
                if result:
                    self.cracking_active = False
                    elapsed = time.time() - start_time
                    print(f"🎯 HASH CRACKED: {result} (Time: {elapsed:.2f}s)")
                    return result
        
        self.cracking_active = False
        elapsed = time.time() - start_time
        print(f"❌ Hash not cracked (Time: {elapsed:.2f}s)")
        return None
    
    def _brute_force_worker(self, target_hash: str, charset: str, length: int) -> Optional[str]:
        """Brute force worker for specific length"""
        for combination in itertools.product(charset, repeat=length):
            if not self.cracking_active:
                break
                
            candidate = ''.join(combination)
            
            # Test with quantum hash engine
            test_hash = self.quantum_engine.generate_quantum_hash(candidate)
            
            if test_hash == target_hash:
                return candidate
            
            # Also test with standard algorithms
            if hashlib.md5(candidate.encode()).hexdigest() == target_hash:
                return candidate
            if hashlib.sha1(candidate.encode()).hexdigest() == target_hash:
                return candidate
            if hashlib.sha256(candidate.encode()).hexdigest() == target_hash:
                return candidate
        
        return None
    
    def dictionary_attack(self, target_hash: str, wordlist: List[str]) -> Optional[str]:
        """Dictionary attack on hash"""
        print(f"📚 Starting dictionary attack on hash: {target_hash[:20]}...")
        print(f"Wordlist size: {len(wordlist)}")
        
        start_time = time.time()
        
        for word in wordlist:
            # Test with quantum hash engine
            test_hash = self.quantum_engine.generate_quantum_hash(word)
            if test_hash == target_hash:
                elapsed = time.time() - start_time
                print(f"🎯 HASH CRACKED: {word} (Time: {elapsed:.2f}s)")
                return word
            
            # Test with standard algorithms
            if hashlib.md5(word.encode()).hexdigest() == target_hash:
                elapsed = time.time() - start_time
                print(f"🎯 HASH CRACKED: {word} (Time: {elapsed:.2f}s)")
                return word
            if hashlib.sha1(word.encode()).hexdigest() == target_hash:
                elapsed = time.time() - start_time
                print(f"🎯 HASH CRACKED: {word} (Time: {elapsed:.2f}s)")
                return word
            if hashlib.sha256(word.encode()).hexdigest() == target_hash:
                elapsed = time.time() - start_time
                print(f"🎯 HASH CRACKED: {word} (Time: {elapsed:.2f}s)")
                return word
        
        elapsed = time.time() - start_time
        print(f"❌ Hash not cracked (Time: {elapsed:.2f}s)")
        return None
    
    def rainbow_table_attack(self, target_hash: str, table_size: int = 100000) -> Optional[str]:
        """Rainbow table attack on hash"""
        print(f"🌈 Starting rainbow table attack on hash: {target_hash[:20]}...")
        print(f"Table size: {table_size}")
        
        # Generate rainbow table
        rainbow_table = {}
        start_time = time.time()
        
        # Common passwords and variations
        base_passwords = [
            "password", "123456", "admin", "root", "user", "guest",
            "qwerty", "abc123", "password123", "admin123", "root123",
            "letmein", "welcome", "monkey", "dragon", "master", "hello"
        ]
        
        # Generate variations
        variations = []
        for password in base_passwords:
            variations.extend([
                password,
                password.upper(),
                password.lower(),
                password + "123",
                password + "!",
                password + "@",
                "123" + password,
                password + "2024",
                password + "2025",
                password + "0",
                password + "1"
            ])
        
        # Build rainbow table
        for i, variation in enumerate(variations[:table_size]):
            hash_result = self.quantum_engine.generate_quantum_hash(variation)
            rainbow_table[hash_result] = variation
            
            # Check for match
            if hash_result == target_hash:
                elapsed = time.time() - start_time
                print(f"🎯 HASH CRACKED: {variation} (Time: {elapsed:.2f}s)")
                return variation
        
        elapsed = time.time() - start_time
        print(f"❌ Hash not cracked (Time: {elapsed:.2f}s)")
        return None
    
    def stop_cracking(self):
        """Stop all cracking operations"""
        self.cracking_active = False
        print("🛑 Cracking operations stopped!")

class HashComparisonTool:
    """Tool for comparing and analyzing multiple hashes"""
    
    def __init__(self):
        self.quantum_engine = QuantumHashEngine(display_hashes=False)
        
    def compare_hashes(self, hashes: List[str]) -> Dict:
        """Compare multiple hashes for similarities"""
        print(f"🔍 Comparing {len(hashes)} hashes...")
        
        comparison = {
            'total_hashes': len(hashes),
            'unique_hashes': len(set(hashes)),
            'duplicates': len(hashes) - len(set(hashes)),
            'similarities': [],
            'patterns': []
        }
        
        # Find duplicates
        hash_counts = {}
        for hash_val in hashes:
            hash_counts[hash_val] = hash_counts.get(hash_val, 0) + 1
        
        duplicates = {h: c for h, c in hash_counts.items() if c > 1}
        comparison['duplicate_details'] = duplicates
        
        # Find similar hashes (same prefix)
        for i, hash1 in enumerate(hashes):
            for j, hash2 in enumerate(hashes[i+1:], i+1):
                # Check for common prefixes
                common_prefix = 0
                for k in range(min(len(hash1), len(hash2))):
                    if hash1[k] == hash2[k]:
                        common_prefix += 1
                    else:
                        break
                
                if common_prefix > 10:  # Significant similarity
                    comparison['similarities'].append({
                        'hash1': hash1[:20] + "...",
                        'hash2': hash2[:20] + "...",
                        'common_prefix_length': common_prefix
                    })
        
        return comparison
    
    def find_hash_patterns(self, hashes: List[str]) -> Dict:
        """Find patterns in hash collection"""
        print(f"🔍 Analyzing patterns in {len(hashes)} hashes...")
        
        patterns = {
            'length_distribution': {},
            'character_frequency': {},
            'common_prefixes': {},
            'algorithm_guesses': {}
        }
        
        # Length distribution
        for hash_val in hashes:
            length = len(hash_val)
            patterns['length_distribution'][length] = patterns['length_distribution'].get(length, 0) + 1
        
        # Character frequency
        for hash_val in hashes:
            for char in hash_val:
                patterns['character_frequency'][char] = patterns['character_frequency'].get(char, 0) + 1
        
        # Common prefixes
        for hash_val in hashes:
            for length in range(4, min(20, len(hash_val))):
                prefix = hash_val[:length]
                patterns['common_prefixes'][prefix] = patterns['common_prefixes'].get(prefix, 0) + 1
        
        # Filter common prefixes (appearing more than once)
        patterns['common_prefixes'] = {k: v for k, v in patterns['common_prefixes'].items() if v > 1}
        
        return patterns

class HashAnalysisTool:
    """Main Hash Analysis and Cracking Tool"""
    
    def __init__(self):
        self.quantum_engine = QuantumHashEngine(display_hashes=False)
        self.analyzer = HashAnalyzer()
        self.cracker = HashCracker(self.quantum_engine)
        self.comparison_tool = HashComparisonTool()
        
        # Statistics
        self.analysis_count = 0
        self.cracked_count = 0
        self.failed_count = 0
        
        print("🔍 Advanced Hash Analysis and Cracking Tool initialized!")
    
    def analyze_hash(self, hash_value: str) -> Dict:
        """Analyze a single hash"""
        self.analysis_count += 1
        return self.analyzer.analyze_hash(hash_value)
    
    def crack_hash(self, hash_value: str, method: str = "rainbow") -> Optional[str]:
        """Crack a hash using specified method"""
        print(f"🔨 Attempting to crack hash using {method} method...")
        
        if method == "brute_force":
            result = self.cracker.brute_force_attack(hash_value)
        elif method == "dictionary":
            # Use common wordlist
            wordlist = [
                "password", "123456", "admin", "root", "user", "guest",
                "qwerty", "abc123", "password123", "admin123", "root123",
                "letmein", "welcome", "monkey", "dragon", "master", "hello"
            ]
            result = self.cracker.dictionary_attack(hash_value, wordlist)
        elif method == "rainbow":
            result = self.cracker.rainbow_table_attack(hash_value)
        else:
            print(f"❌ Unknown method: {method}")
            return None
        
        if result:
            self.cracked_count += 1
            return result
        else:
            self.failed_count += 1
            return None
    
    def compare_hashes(self, hashes: List[str]) -> Dict:
        """Compare multiple hashes"""
        return self.comparison_tool.compare_hashes(hashes)
    
    def find_patterns(self, hashes: List[str]) -> Dict:
        """Find patterns in hash collection"""
        return self.comparison_tool.find_hash_patterns(hashes)
    
    def get_statistics(self) -> Dict:
        """Get tool statistics"""
        return {
            'analyses_performed': self.analysis_count,
            'hashes_cracked': self.cracked_count,
            'cracking_failures': self.failed_count,
            'success_rate': self.cracked_count / (self.cracked_count + self.failed_count) if (self.cracked_count + self.failed_count) > 0 else 0
        }

def main():
    """Main function for Hash Analysis Tool"""
    print("🔍 HASH ANALYSIS AND CRACKING TOOL")
    print("=" * 60)
    print("Advanced hash analysis and cracking using quantum techniques")
    print("=" * 60)
    
    # Initialize tool
    analysis_tool = HashAnalysisTool()
    
    while True:
        print("\n🔍 Analysis Options:")
        print("1. 🔍 Analyze Single Hash")
        print("2. 🔨 Crack Hash (Brute Force)")
        print("3. 📚 Crack Hash (Dictionary)")
        print("4. 🌈 Crack Hash (Rainbow Table)")
        print("5. 🔍 Compare Multiple Hashes")
        print("6. 🔍 Find Hash Patterns")
        print("7. 📊 View Statistics")
        print("8. ❌ Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == "1":
            hash_value = input("Enter hash to analyze: ").strip()
            if hash_value:
                analysis = analysis_tool.analyze_hash(hash_value)
                print(f"\n📊 Analysis Results:")
                print(f"Length: {analysis['length']}")
                print(f"Character Set: {analysis['character_set']['type']}")
                print(f"Entropy: {analysis['entropy']:.2f}")
                print(f"Likely Algorithm: {analysis['likely_algorithm']}")
                print(f"Crack Difficulty: {analysis['crack_difficulty']}")
                print(f"Quantum Resistance: {analysis['quantum_resistance']}")
        
        elif choice == "2":
            hash_value = input("Enter hash to crack: ").strip()
            if hash_value:
                result = analysis_tool.crack_hash(hash_value, "brute_force")
                if result:
                    print(f"🎯 CRACKED: {result}")
                else:
                    print("❌ Hash not cracked")
        
        elif choice == "3":
            hash_value = input("Enter hash to crack: ").strip()
            if hash_value:
                result = analysis_tool.crack_hash(hash_value, "dictionary")
                if result:
                    print(f"🎯 CRACKED: {result}")
                else:
                    print("❌ Hash not cracked")
        
        elif choice == "4":
            hash_value = input("Enter hash to crack: ").strip()
            if hash_value:
                result = analysis_tool.crack_hash(hash_value, "rainbow")
                if result:
                    print(f"🎯 CRACKED: {result}")
                else:
                    print("❌ Hash not cracked")
        
        elif choice == "5":
            hashes_input = input("Enter hashes (comma-separated): ").strip()
            if hashes_input:
                hashes = [h.strip() for h in hashes_input.split(',') if h.strip()]
                comparison = analysis_tool.compare_hashes(hashes)
                print(f"\n📊 Comparison Results:")
                print(f"Total Hashes: {comparison['total_hashes']}")
                print(f"Unique Hashes: {comparison['unique_hashes']}")
                print(f"Duplicates: {comparison['duplicates']}")
                print(f"Similarities Found: {len(comparison['similarities'])}")
        
        elif choice == "6":
            hashes_input = input("Enter hashes (comma-separated): ").strip()
            if hashes_input:
                hashes = [h.strip() for h in hashes_input.split(',') if h.strip()]
                patterns = analysis_tool.find_patterns(hashes)
                print(f"\n📊 Pattern Analysis:")
                print(f"Length Distribution: {patterns['length_distribution']}")
                print(f"Common Prefixes: {patterns['common_prefixes']}")
        
        elif choice == "7":
            stats = analysis_tool.get_statistics()
            print(f"\n📊 Tool Statistics:")
            print(f"Analyses Performed: {stats['analyses_performed']}")
            print(f"Hashes Cracked: {stats['hashes_cracked']}")
            print(f"Cracking Failures: {stats['cracking_failures']}")
            print(f"Success Rate: {stats['success_rate']:.2%}")
        
        elif choice == "8":
            print("🔍 Hash Analysis Tool shutdown complete!")
            break
            
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🔍 Hash Analysis Tool terminated by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
