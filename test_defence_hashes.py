"""
Test Defence Engine with Hash Display
"""
import subprocess
import sys
import time

def test_defence_with_hashes():
    print("Testing Defence Engine with hash display...")
    
    # Start the process
    process = subprocess.Popen([
        sys.executable, "defence.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
       text=True, bufsize=1, universal_newlines=True)
    
    try:
        # Send responses
        inputs = [
            "y\n",  # Show hashes
            "DEF-89E11FC8-B1E04974-85C583E1\n"  # License key
        ]
        
        for input_line in inputs:
            process.stdin.write(input_line)
            process.stdin.flush()
            time.sleep(1)
        
        # Let it run for 10 seconds to see hash generation
        print("Letting Defence Engine run for 10 seconds to show hash generation...")
        time.sleep(10)
        
        # Terminate
        process.terminate()
        
        # Get output
        try:
            stdout, stderr = process.communicate(timeout=5)
            print("Defence Engine Output:")
            print(stdout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            print("Defence Engine Output (forced termination):")
            print(stdout)
            
    except Exception as e:
        print(f"Error during test: {e}")
        process.terminate()
        
    print("Test completed.")

if __name__ == "__main__":
    test_defence_with_hashes()