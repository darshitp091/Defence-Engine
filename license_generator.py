"""
Simple License Generator for Defence Engine
Easy-to-use license generation and management
"""
import sys
import os
from datetime import datetime, timedelta

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from license.license_manager import LicenseManager

def generate_single_license():
    """Generate a single license key"""
    print("🔐 DEFENCE ENGINE LICENSE GENERATOR")
    print("============================================================")
    
    # Get user input
    user_id = input("Enter User ID (or press Enter for 'default_user'): ").strip()
    if not user_id:
        user_id = "default_user"
    
    expiry_days = input("Enter expiry days (or press Enter for 365): ").strip()
    try:
        expiry_days = int(expiry_days) if expiry_days else 365
    except ValueError:
        expiry_days = 365
    
    max_usage = input("Enter max usage (-1 for unlimited, or press Enter for unlimited): ").strip()
    try:
        max_usage = int(max_usage) if max_usage else -1
    except ValueError:
        max_usage = -1
    
    # Initialize license manager
    license_manager = LicenseManager()
    
    # Generate license
    print(f"\n🔄 Generating license for user: {user_id}")
    print(f"   Expiry: {expiry_days} days")
    print(f"   Max Usage: {'Unlimited' if max_usage == -1 else max_usage}")
    
    license_key = license_manager.generate_license_key(
        user_id=user_id,
        expiry_days=expiry_days,
        max_usage=max_usage,
        metadata={'generated_by': 'defence_engine', 'version': '1.0'}
    )
    
    if license_key:
        print(f"\n✅ LICENSE GENERATED SUCCESSFULLY!")
        print("============================================================")
        print(f"🔑 License Key: {license_key}")
        print(f"👤 User ID: {user_id}")
        print(f"📅 Expiry: {expiry_days} days from now")
        print(f"🔢 Max Usage: {'Unlimited' if max_usage == -1 else max_usage}")
        print("============================================================")
        
        # Save to file
        save_to_file = input("\nSave license to file? (y/n): ").strip().lower()
        if save_to_file == 'y':
            filename = f"license_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                with open(filename, 'w') as f:
                    f.write(f"Defence Engine License\n")
                    f.write(f"=====================\n")
                    f.write(f"License Key: {license_key}\n")
                    f.write(f"User ID: {user_id}\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Expiry: {expiry_days} days\n")
                    f.write(f"Max Usage: {'Unlimited' if max_usage == -1 else max_usage}\n")
                print(f"✅ License saved to: {filename}")
            except Exception as e:
                print(f"❌ Error saving license: {e}")
        
        return license_key
    else:
        print("❌ License generation failed!")
        return None

def generate_bulk_licenses():
    """Generate multiple licenses"""
    print("🔐 BULK LICENSE GENERATOR")
    print("============================================================")
    
    # Get user input
    count = input("Enter number of licenses to generate: ").strip()
    try:
        count = int(count)
        if count <= 0:
            print("❌ Count must be positive!")
            return
    except ValueError:
        print("❌ Invalid count!")
        return
    
    user_prefix = input("Enter user prefix (or press Enter for 'USER'): ").strip()
    if not user_prefix:
        user_prefix = "USER"
    
    expiry_days = input("Enter expiry days (or press Enter for 365): ").strip()
    try:
        expiry_days = int(expiry_days) if expiry_days else 365
    except ValueError:
        expiry_days = 365
    
    # Initialize license manager
    license_manager = LicenseManager()
    
    print(f"\n🔄 Generating {count} licenses...")
    print(f"   User Prefix: {user_prefix}")
    print(f"   Expiry: {expiry_days} days")
    
    # Generate bulk licenses
    licenses = license_manager.generate_bulk_licenses(
        count=count,
        user_prefix=user_prefix,
        expiry_days=expiry_days
    )
    
    if licenses:
        print(f"\n✅ GENERATED {len(licenses)} LICENSES SUCCESSFULLY!")
        print("============================================================")
        
        # Display licenses
        for i, license_data in enumerate(licenses, 1):
            print(f"{i:3d}. {license_data['license_key']} (User: {license_data['user_id']})")
        
        # Save to file
        save_to_file = input(f"\nSave {len(licenses)} licenses to file? (y/n): ").strip().lower()
        if save_to_file == 'y':
            filename = f"bulk_licenses_{user_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                with open(filename, 'w') as f:
                    f.write(f"Defence Engine Bulk Licenses\n")
                    f.write(f"===========================\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Count: {len(licenses)}\n")
                    f.write(f"User Prefix: {user_prefix}\n")
                    f.write(f"Expiry: {expiry_days} days\n\n")
                    
                    for i, license_data in enumerate(licenses, 1):
                        f.write(f"{i:3d}. License Key: {license_data['license_key']}\n")
                        f.write(f"     User ID: {license_data['user_id']}\n")
                        f.write(f"     Expiry: {license_data['expiry_days']} days\n\n")
                
                print(f"✅ Licenses saved to: {filename}")
            except Exception as e:
                print(f"❌ Error saving licenses: {e}")
        
        return licenses
    else:
        print("❌ Bulk license generation failed!")
        return None

def list_licenses():
    """List all generated licenses"""
    print("📋 LICENSE MANAGER - VIEW ALL LICENSES")
    print("============================================================")
    
    license_manager = LicenseManager()
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        print("❌ No licenses found!")
        return
    
    print(f"📊 Found {len(licenses)} licenses:")
    print("============================================================")
    
    for i, license_data in enumerate(licenses, 1):
        status = "✅ Active" if license_data['is_active'] else "❌ Inactive"
        expiry_info = f"Expires: {license_data['expiry_date']}" if license_data['expiry_date'] else "Never expires"
        usage_info = f"Usage: {license_data['usage_count']}/{license_data['max_usage']}" if license_data['max_usage'] > 0 else f"Usage: {license_data['usage_count']}/∞"
        
        print(f"{i:3d}. {license_data['license_key']}")
        print(f"     User: {license_data['user_id']} | {status}")
        print(f"     Created: {license_data['created_date']}")
        print(f"     {expiry_info} | {usage_info}")
        print()

def validate_license():
    """Validate a license key"""
    print("🔍 LICENSE VALIDATOR")
    print("============================================================")
    
    license_key = input("Enter license key to validate: ").strip()
    if not license_key:
        print("❌ No license key provided!")
        return
    
    license_manager = LicenseManager()
    result = license_manager.validate_license(license_key)
    
    if result['valid']:
        print(f"\n✅ LICENSE IS VALID!")
        print("============================================================")
        license_data = result['license_data']
        print(f"🔑 License Key: {license_data['license_key']}")
        print(f"👤 User ID: {license_data['user_id']}")
        print(f"📅 Created: {license_data['created_date']}")
        print(f"📅 Expiry: {license_data['expiry_date'] or 'Never'}")
        print(f"🔢 Usage: {result['usage_count']}")
        print(f"🔢 Remaining: {result['remaining_usage'] if result['remaining_usage'] != -1 else 'Unlimited'}")
    else:
        print(f"\n❌ LICENSE IS INVALID!")
        print(f"Reason: {result['reason']}")

def show_statistics():
    """Show license statistics"""
    print("📊 LICENSE STATISTICS")
    print("============================================================")
    
    license_manager = LicenseManager()
    stats = license_manager.get_license_statistics()
    
    if stats:
        print(f"📈 License Statistics:")
        print(f"   Total Licenses: {stats.get('total_licenses', 0)}")
        print(f"   Active Licenses: {stats.get('active_licenses', 0)}")
        print(f"   Expired Licenses: {stats.get('expired_licenses', 0)}")
        print(f"   Total Usage: {stats.get('total_usage', 0)}")
        print(f"   Recent Usage (7 days): {stats.get('recent_usage_7days', 0)}")
        print(f"   Blockchain Blocks: {stats.get('blockchain_blocks', 0)}")
        print(f"   Crypto Available: {'Yes' if stats.get('crypto_available', False) else 'No'}")
    else:
        print("❌ Could not retrieve statistics!")

def main():
    """Main license generator menu"""
    while True:
        print("\n🔐 DEFENCE ENGINE LICENSE MANAGER")
        print("============================================================")
        print("1. Generate Single License")
        print("2. Generate Bulk Licenses")
        print("3. List All Licenses")
        print("4. Validate License")
        print("5. Show Statistics")
        print("6. Exit")
        print("============================================================")
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == '1':
            generate_single_license()
        elif choice == '2':
            generate_bulk_licenses()
        elif choice == '3':
            list_licenses()
        elif choice == '4':
            validate_license()
        elif choice == '5':
            show_statistics()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please select 1-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
