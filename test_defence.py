"""
Test Defence Engine
"""
import subprocess
import sys
import time
import threading

def test_defence():
    print("Testing Defence Engine...")
    
    # Start defence engine in background
    process = subprocess.Popen([
        sys.executable, "defence.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Send license key
    license_key = "DEF-89E11FC8-B1E04974-85C583E1\n"
    
    try:
        # Send license key and wait a bit
        stdout, stderr = process.communicate(input=license_key, timeout=5)
        
        print("Defence Engine Output:")
        print(stdout)
        
        if stderr:
            print("Errors:")
            print(stderr)
            
    except subprocess.TimeoutExpired:
        print("Defence Engine started successfully and is running...")
        process.terminate()
        process.wait()
        
    print("Test completed.")

if __name__ == "__main__":
    test_defence()