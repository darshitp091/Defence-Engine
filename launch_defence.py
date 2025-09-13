"""
Defence Engine - Easy Launcher
"""
import sys
import os
import subprocess

def main():
    print("=" * 60)
    print("🛡️  Defence Engine - Advanced Security Protection")
    print("=" * 60)
    print()
    print("Choose launch option:")
    print("1. 🖥️  GUI Application (Recommended)")
    print("2. ⚙️  Background Service")
    print("3. 🔑 License Generator")
    print("4. 🔬 Quantum Hash Demo")
    print("5. 🧪 Test Gemini API")
    print("6. 📋 System Information")
    print("7. ❌ Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            launch_gui()
            break
        elif choice == "2":
            launch_service()
            break
        elif choice == "3":
            launch_license_generator()
            break
        elif choice == "4":
            launch_quantum_demo()
            break
        elif choice == "5":
            test_api()
            break
        elif choice == "6":
            show_system_info()
            break
        elif choice == "7":
            print("Goodbye! Stay secure! 🛡️")
            break
        else:
            print("Invalid choice. Please enter 1-7.")

def launch_gui():
    """Launch GUI application"""
    print("\n🖥️ Launching Defence Engine GUI...")
    print("Built-in Gemini API key will be used automatically.")
    print("You only need to enter your license key!")
    
    try:
        subprocess.run([sys.executable, "defence_engine.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
    except KeyboardInterrupt:
        print("\n⚠️ GUI application interrupted by user")

def launch_service():
    """Launch background service"""
    print("\n⚙️ Launching Background Service...")
    
    license_key = input("Enter your license key: ").strip()
    if not license_key:
        print("❌ License key is required for service mode")
        return
        
    use_custom_api = input("Use custom Gemini API key? (y/N): ").strip().lower()
    
    if use_custom_api == 'y':
        api_key = input("Enter Gemini API key: ").strip()
        if api_key:
            cmd = [sys.executable, "defence_engine.py", "--mode", "service", 
                   "--license-key", license_key, "--api-key", api_key]
        else:
            print("❌ API key cannot be empty when using custom key")
            return
    else:
        print("Using built-in Gemini API key...")
        cmd = [sys.executable, "defence_engine.py", "--mode", "service", 
               "--license-key", license_key]
    
    try:
        print("🚀 Starting Defence Engine service...")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching service: {e}")
    except KeyboardInterrupt:
        print("\n⚠️ Service interrupted by user")

def launch_license_generator():
    """Launch license generator"""
    print("\n🔑 Launching License Generator...")
    
    try:
        subprocess.run([sys.executable, "licence_generator.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching license generator: {e}")
    except KeyboardInterrupt:
        print("\n⚠️ License generator interrupted by user")

def launch_quantum_demo():
    """Launch quantum hash demonstration"""
    print("\n🔬 Launching Quantum Hash Demonstration...")
    print("This will show real-time quantum hash generation with GPU acceleration!")
    
    try:
        subprocess.run([sys.executable, "quantum_demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching quantum demo: {e}")
    except KeyboardInterrupt:
        print("\n⚠️ Quantum demo interrupted by user")

def test_api():
    """Test Gemini API"""
    print("\n🧪 Testing Gemini API Integration...")
    
    try:
        subprocess.run([sys.executable, "test_gemini.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running API test: {e}")
    except KeyboardInterrupt:
        print("\n⚠️ API test interrupted by user")

def show_system_info():
    """Show system information"""
    print("\n📋 Defence Engine System Information")
    print("=" * 50)
    
    # Import config to show current settings
    try:
        from config import DefenceConfig
        
        print(f"Built-in API Key: {DefenceConfig.DEFAULT_GEMINI_API_KEY[:20]}...")
        print(f"Monitoring Interval: {DefenceConfig.MONITORING_INTERVAL} seconds")
        print(f"Threat Threshold: {DefenceConfig.THREAT_THRESHOLD}")
        print(f"Pattern Rotation: {DefenceConfig.PATTERN_ROTATION_INTERVAL} seconds")
        print(f"Max Log Size: {DefenceConfig.MAX_LOG_SIZE // (1024*1024)} MB")
        print(f"Hash Obfuscation Layers: {DefenceConfig.OBFUSCATION_LAYERS}")
        
        # Check if logs directory exists
        logs_dir = DefenceConfig.get_logs_dir()
        print(f"Logs Directory: {logs_dir}")
        
        # Check for existing log files
        log_files = list(logs_dir.glob("*.log"))
        if log_files:
            print(f"Existing Log Files: {len(log_files)}")
            for log_file in log_files:
                size_mb = log_file.stat().st_size / (1024 * 1024)
                print(f"  - {log_file.name}: {size_mb:.2f} MB")
        else:
            print("No existing log files")
            
        # Check Python version
        print(f"Python Version: {sys.version}")
        
        # Check if required packages are installed
        try:
            import google.generativeai
            print("✅ Google Generative AI: Installed")
        except ImportError:
            print("❌ Google Generative AI: Not installed")
            
        try:
            import cryptography
            print("✅ Cryptography: Installed")
        except ImportError:
            print("❌ Cryptography: Not installed")
            
        try:
            import psutil
            print("✅ PSUtil: Installed")
        except ImportError:
            print("❌ PSUtil: Not installed")
            
    except Exception as e:
        print(f"❌ Error getting system info: {e}")
    
    print("=" * 50)
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()