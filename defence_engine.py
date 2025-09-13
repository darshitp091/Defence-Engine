"""
Defence Engine - Main Application Launcher
"""
import sys
import os
import argparse
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='Defence Engine - Advanced Security Protection System')
    parser.add_argument('--mode', choices=['gui', 'service', 'license'], default='gui',
                       help='Run mode: gui (default), service, or license generator')
    parser.add_argument('--license-key', help='License key for service mode')
    parser.add_argument('--api-key', help='Gemini API key for service mode (optional - uses built-in if not provided)')
    
    args = parser.parse_args()
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    
    if args.mode == 'gui':
        print("Starting Defence Engine GUI...")
        from gui.main_app import DefenceEngineGUI
        app = DefenceEngineGUI()
        app.run()
        
    elif args.mode == 'service':
        if not args.license_key:
            print("Error: Service mode requires --license-key argument")
            print("API key is optional - will use built-in key if not provided")
            sys.exit(1)
            
        print("Starting Defence Engine Background Service...")
        if args.api_key:
            print("Using custom Gemini API key")
        else:
            print("Using built-in Gemini API key")
            
        from service.background_service import DefenceBackgroundService
        service = DefenceBackgroundService(args.license_key, args.api_key)
        service.run_forever()
        
    elif args.mode == 'license':
        print("Starting License Generator...")
        from license_generator import main as license_main
        license_main()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()