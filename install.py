"""
Defence Engine Installation Script
"""
import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing Defence Engine requirements...")
    
    try:
        # Install packages
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'core', 'ai', 'defense', 'license', 'gui', 'service']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        
    print("✅ Directories created successfully!")

def setup_environment():
    """Setup environment"""
    print("Setting up Defence Engine environment...")
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        return False
        
    print("\n" + "="*60)
    print("Defence Engine Installation Complete!")
    print("="*60)
    print("\nUsage:")
    print("1. GUI Mode (default):     python defence_engine.py")
    print("2. Service Mode:           python defence_engine.py --mode service --license-key YOUR_KEY --api-key YOUR_API_KEY")
    print("3. License Generator:      python defence_engine.py --mode license")
    print("\nOr use individual components:")
    print("- License Generator:       python license_generator.py")
    print("- GUI Application:         python gui/main_app.py")
    print("- Background Service:      python service/background_service.py LICENSE_KEY API_KEY")
    
    return True

if __name__ == "__main__":
    if setup_environment():
        print("\n🎉 Installation successful! You can now run Defence Engine.")
    else:
        print("\n❌ Installation failed. Please check the errors above.")
        sys.exit(1)