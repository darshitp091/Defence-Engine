"""
Quick License Generator for Defence Engine
Fast and easy license generation
"""
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from license.license_manager import LicenseManager

def generate_quick_license():
    """Generate a license quickly with default settings"""
    print("🔐 QUICK LICENSE GENERATOR")
    print("============================================================")
    
    try:
        # Initialize license manager
        license_manager = LicenseManager()
        
        # Generate license with default values
        user_id = "defence_user"
        expiry_days = 365
        max_usage = -1  # Unlimited
        
        print(f"🔄 Generating license for user: {user_id}")
        print(f"   Expiry: {expiry_days} days")
        print(f"   Max Usage: Unlimited")
        
        license_key = license_manager.generate_license_key(
            user_id=user_id,
            expiry_days=expiry_days,
            max_usage=max_usage,
            metadata={'generated_by': 'defence_engine', 'version': '1.0', 'quick_generated': True}
        )
        
        if license_key:
            print(f"\n✅ LICENSE GENERATED SUCCESSFULLY!")
            print("============================================================")
            print(f"🔑 License Key: {license_key}")
            print(f"👤 User ID: {user_id}")
            print(f"📅 Expiry: {expiry_days} days from now")
            print(f"🔢 Max Usage: Unlimited")
            print("============================================================")
            
            # Save to file
            filename = f"license_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                with open(filename, 'w') as f:
                    f.write(f"Defence Engine License\n")
                    f.write(f"=====================\n")
                    f.write(f"License Key: {license_key}\n")
                    f.write(f"User ID: {user_id}\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Expiry: {expiry_days} days\n")
                    f.write(f"Max Usage: Unlimited\n")
                    f.write(f"\nTo use this license:\n")
                    f.write(f"python defence_engine.py --mode service --license-key {license_key}\n")
                print(f"✅ License saved to: {filename}")
            except Exception as e:
                print(f"❌ Error saving license: {e}")
            
            return license_key
        else:
            print("❌ License generation failed!")
            return None
            
    except Exception as e:
        print(f"❌ Error generating license: {e}")
        return None

def show_available_licenses():
    """Show all available licenses"""
    print("\n📋 AVAILABLE LICENSES")
    print("============================================================")
    
    try:
        license_manager = LicenseManager()
        licenses = license_manager.list_all_licenses()
        
        if not licenses:
            print("❌ No licenses found!")
            return
        
        print(f"📊 Found {len(licenses)} licenses:")
        print("============================================================")
        
        for i, license_data in enumerate(licenses, 1):
            status = "✅ Active" if license_data['is_active'] else "❌ Inactive"
            print(f"{i:3d}. {license_data['license_key']}")
            print(f"     User: {license_data['user_id']} | {status}")
            print(f"     Created: {license_data['created_date']}")
            print(f"     Expiry: {license_data['expiry_date'] or 'Never'}")
            print(f"     Usage: {license_data['usage_count']}/{license_data['max_usage'] if license_data['max_usage'] > 0 else '∞'}")
            print()
        
    except Exception as e:
        print(f"❌ Error listing licenses: {e}")

def main():
    """Main function"""
    print("🚀 DEFENCE ENGINE QUICK LICENSE GENERATOR")
    print("============================================================")
    
    # Generate quick license
    license_key = generate_quick_license()
    
    if license_key:
        # Show all licenses
        show_available_licenses()
        
        print("\n🎉 LICENSE GENERATION SUCCESSFUL!")
        print("============================================================")
        print(f"🔑 Your license key: {license_key}")
        print(f"💡 Use this license with: python defence_engine.py --mode service --license-key {license_key}")
        print("============================================================")
    else:
        print("\n❌ LICENSE GENERATION FAILED!")
        print("============================================================")

if __name__ == "__main__":
    main()
