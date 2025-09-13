"""
Quick Defence Engine Test
"""
import subprocess
import sys
import time
import signal
import os

def test_defence_with_input():
    print("Testing Defence Engine with license key input...")
    
    # Start the process
    process = subprocess.Popen([
        sys.executable, "defence.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
       text=True, bufsize=1, universal_newlines=True)
    
    try:
        # Send license key
        license_key = "DEF-89E11FC8-B1E04974-85C583E1\n"
        process.stdin.write(license_key)
        process.stdin.flush()
        
        # Read initial output
        time.sleep(2)
        
        # Let it run for a few seconds to generate hashes
        print("Letting Defence Engine run for 10 seconds...")
        time.sleep(10)
        
        # Terminate the process
        if os.name == 'nt':  # Windows
            process.terminate()
        else:  # Unix/Linux
            process.send_signal(signal.SIGINT)
        
        # Get remaining output
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
    test_defence_with_input()