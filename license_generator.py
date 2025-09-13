"""
License Key Generator Tool
"""
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from license.license_manager import LicenseManager

def main():
    print("=" * 60)
    print("Defence Engine - License Key Generator")
    print("=" * 60)
    
    license_manager = LicenseManager()
    
    while True:
        print("\nOptions:")
        print("1. Generate single license")
        print("2. Generate bulk licenses")
        print("3. View license info")
        print("4. List all licenses")
        print("5. Revoke license")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            generate_single_license(license_manager)
        elif choice == "2":
            generate_bulk_licenses(license_manager)
        elif choice == "3":
            view_license_info(license_manager)
        elif choice == "4":
            list_all_licenses(license_manager)
        elif choice == "5":
            revoke_license(license_manager)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def generate_single_license(license_manager):
    """Generate a single license key"""
    print("\n--- Generate Single License ---")
    
    user_id = input("Enter User ID: ").strip()
    if not user_id:
        print("User ID cannot be empty.")
        return
        
    try:
        expiry_days = int(input("Enter expiry days (0 for no expiry): ").strip() or "365")
    except ValueError:
        expiry_days = 365
        
    try:
        max_usage = int(input("Enter max usage count (-1 for unlimited): ").strip() or "-1")
    except ValueError:
        max_usage = -1
        
    metadata = {}
    company = input("Enter company name (optional): ").strip()
    if company:
        metadata['company'] = company
        
    email = input("Enter email (optional): ").strip()
    if email:
        metadata['email'] = email
        
    try:
        license_key = license_manager.generate_license_key(
            user_id=user_id,
            expiry_days=expiry_days,
            max_usage=max_usage,
            metadata=metadata if metadata else None
        )
        
        print(f"\n✅ License generated successfully!")
        print(f"License Key: {license_key}")
        print(f"User ID: {user_id}")
        print(f"Expiry: {'Never' if expiry_days == 0 else f'{expiry_days} days'}")
        print(f"Max Usage: {'Unlimited' if max_usage == -1 else max_usage}")
        
        # Save to file
        with open('generated_licenses.txt', 'a') as f:
            f.write(f"{datetime.now().isoformat()},{license_key},{user_id}\n")
            
    except Exception as e:
        print(f"❌ Error generating license: {str(e)}")

def generate_bulk_licenses(license_manager):
    """Generate bulk license keys"""
    print("\n--- Generate Bulk Licenses ---")
    
    try:
        count = int(input("Enter number of licenses to generate: ").strip())
        if count <= 0:
            print("Count must be positive.")
            return
    except ValueError:
        print("Invalid count.")
        return
        
    user_prefix = input("Enter user ID prefix (default: USER): ").strip() or "USER"
    
    try:
        expiry_days = int(input("Enter expiry days (0 for no expiry): ").strip() or "365")
    except ValueError:
        expiry_days = 365
        
    print(f"\nGenerating {count} licenses...")
    
    try:
        licenses = license_manager.generate_bulk_licenses(
            count=count,
            user_prefix=user_prefix,
            expiry_days=expiry_days
        )
        
        print(f"\n✅ Generated {len(licenses)} licenses successfully!")
        
        # Save to file
        filename = f"bulk_licenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write("User ID,License Key\n")
            for license_data in licenses:
                f.write(f"{license_data['user_id']},{license_data['license_key']}\n")
                
        print(f"Licenses saved to: {filename}")
        
        # Display first few licenses
        print("\nFirst 5 licenses:")
        for i, license_data in enumerate(licenses[:5]):
            print(f"{i+1}. {license_data['user_id']}: {license_data['license_key']}")
            
        if len(licenses) > 5:
            print(f"... and {len(licenses) - 5} more")
            
    except Exception as e:
        print(f"❌ Error generating bulk licenses: {str(e)}")

def view_license_info(license_manager):
    """View license information"""
    print("\n--- View License Info ---")
    
    license_key = input("Enter license key: ").strip()
    if not license_key:
        print("License key cannot be empty.")
        return
        
    try:
        license_info = license_manager.get_license_info(license_key)
        
        if license_info:
            print(f"\n📋 License Information:")
            print(f"License Key: {license_info['license_key']}")
            print(f"User ID: {license_info['user_id']}")
            print(f"Created: {license_info['created_date']}")
            print(f"Expires: {license_info['expiry_date'] or 'Never'}")
            print(f"Active: {'Yes' if license_info['is_active'] else 'No'}")
            print(f"Usage Count: {license_info['usage_count']}")
            print(f"Max Usage: {'Unlimited' if license_info['max_usage'] == -1 else license_info['max_usage']}")
            
            if license_info['metadata']:
                print(f"Metadata: {license_info['metadata']}")
        else:
            print("❌ License not found.")
            
    except Exception as e:
        print(f"❌ Error retrieving license info: {str(e)}")

def list_all_licenses(license_manager):
    """List all licenses"""
    print("\n--- All Licenses ---")
    
    try:
        licenses = license_manager.list_all_licenses()
        
        if not licenses:
            print("No licenses found.")
            return
            
        print(f"\nFound {len(licenses)} licenses:")
        print("-" * 100)
        print(f"{'User ID':<20} {'License Key':<30} {'Active':<8} {'Usage':<10} {'Created':<20}")
        print("-" * 100)
        
        for license_data in licenses:
            usage_str = f"{license_data['usage_count']}"
            if license_data['max_usage'] != -1:
                usage_str += f"/{license_data['max_usage']}"
                
            print(f"{license_data['user_id']:<20} {license_data['license_key']:<30} "
                  f"{'Yes' if license_data['is_active'] else 'No':<8} {usage_str:<10} "
                  f"{license_data['created_date'][:19]:<20}")
                  
    except Exception as e:
        print(f"❌ Error listing licenses: {str(e)}")

def revoke_license(license_manager):
    """Revoke a license"""
    print("\n--- Revoke License ---")
    
    license_key = input("Enter license key to revoke: ").strip()
    if not license_key:
        print("License key cannot be empty.")
        return
        
    # Confirm revocation
    confirm = input(f"Are you sure you want to revoke license {license_key}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Revocation cancelled.")
        return
        
    try:
        success = license_manager.revoke_license(license_key)
        
        if success:
            print(f"✅ License {license_key} has been revoked.")
        else:
            print(f"❌ License {license_key} not found or already revoked.")
            
    except Exception as e:
        print(f"❌ Error revoking license: {str(e)}")

if __name__ == "__main__":
    main()