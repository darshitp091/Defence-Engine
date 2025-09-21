"""
Simple License Manager - View and Manage All Licenses
Easy access to all generated licenses
"""
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from license.license_manager import LicenseManager

def show_all_licenses():
    """Show all generated licenses in a user-friendly format"""
    print("📋 DEFENCE ENGINE LICENSE MANAGER")
    print("============================================================")
    print("🔍 Viewing All Generated Licenses")
    print("============================================================")
    
    try:
        license_manager = LicenseManager()
        licenses = license_manager.list_all_licenses()
        
        if not licenses:
            print("❌ No licenses found!")
            print("💡 Generate a license first using: python defence_engine.py --mode license")
            return
        
        print(f"📊 Found {len(licenses)} licenses:")
        print("============================================================")
        
        for i, license_data in enumerate(licenses, 1):
            # Determine status
            if not license_data['is_active']:
                status = "❌ REVOKED"
                status_color = ""
            elif license_data['expiry_date']:
                expiry_date = datetime.fromisoformat(license_data['expiry_date'])
                if datetime.now() > expiry_date:
                    status = "⏰ EXPIRED"
                    status_color = ""
                else:
                    status = "✅ ACTIVE"
                    status_color = ""
            else:
                status = "✅ ACTIVE (No Expiry)"
                status_color = ""
            
            # Usage information
            if license_data['max_usage'] > 0:
                usage_info = f"Usage: {license_data['usage_count']}/{license_data['max_usage']}"
                if license_data['usage_count'] >= license_data['max_usage']:
                    usage_info += " (LIMIT REACHED)"
            else:
                usage_info = f"Usage: {license_data['usage_count']}/∞ (Unlimited)"
            
            # Expiry information
            if license_data['expiry_date']:
                expiry_date = datetime.fromisoformat(license_data['expiry_date'])
                days_remaining = (expiry_date - datetime.now()).days
                if days_remaining > 0:
                    expiry_info = f"Expires in {days_remaining} days"
                else:
                    expiry_info = f"Expired {abs(days_remaining)} days ago"
            else:
                expiry_info = "Never expires"
            
            print(f"{i:3d}. {license_data['license_key']}")
            print(f"     User: {license_data['user_id']} | {status}")
            print(f"     Created: {license_data['created_date']}")
            print(f"     {expiry_info}")
            print(f"     {usage_info}")
            print()
        
        # Show statistics
        stats = license_manager.get_license_statistics()
        if stats:
            print("📊 LICENSE STATISTICS")
            print("============================================================")
            print(f"   Total Licenses: {stats.get('total_licenses', 0)}")
            print(f"   Active Licenses: {stats.get('active_licenses', 0)}")
            print(f"   Expired Licenses: {stats.get('expired_licenses', 0)}")
            print(f"   Total Usage: {stats.get('total_usage', 0)}")
            print(f"   Recent Usage (7 days): {stats.get('recent_usage_7days', 0)}")
            print("============================================================")
        
    except Exception as e:
        print(f"❌ Error accessing license database: {e}")
        print("💡 Make sure the license database exists and is accessible.")

def search_license():
    """Search for a specific license"""
    print("🔍 LICENSE SEARCH")
    print("============================================================")
    
    search_term = input("Enter license key or user ID to search: ").strip()
    if not search_term:
        print("❌ No search term provided!")
        return
    
    try:
        license_manager = LicenseManager()
        licenses = license_manager.list_all_licenses()
        
        found_licenses = []
        for license_data in licenses:
            if (search_term.lower() in license_data['license_key'].lower() or 
                search_term.lower() in license_data['user_id'].lower()):
                found_licenses.append(license_data)
        
        if not found_licenses:
            print(f"❌ No licenses found matching '{search_term}'")
            return
        
        print(f"🔍 Found {len(found_licenses)} matching licenses:")
        print("============================================================")
        
        for i, license_data in enumerate(found_licenses, 1):
            status = "✅ Active" if license_data['is_active'] else "❌ Inactive"
            print(f"{i}. {license_data['license_key']}")
            print(f"   User: {license_data['user_id']} | {status}")
            print(f"   Created: {license_data['created_date']}")
            print(f"   Expiry: {license_data['expiry_date'] or 'Never'}")
            print(f"   Usage: {license_data['usage_count']}/{license_data['max_usage'] if license_data['max_usage'] > 0 else '∞'}")
            print()
        
    except Exception as e:
        print(f"❌ Error searching licenses: {e}")

def validate_license():
    """Validate a specific license"""
    print("🔍 LICENSE VALIDATION")
    print("============================================================")
    
    license_key = input("Enter license key to validate: ").strip()
    if not license_key:
        print("❌ No license key provided!")
        return
    
    try:
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
            print(f"🔢 Usage Count: {result['usage_count']}")
            print(f"🔢 Remaining Usage: {result['remaining_usage'] if result['remaining_usage'] != -1 else 'Unlimited'}")
            print("============================================================")
        else:
            print(f"\n❌ LICENSE IS INVALID!")
            print(f"Reason: {result['reason']}")
            print("============================================================")
        
    except Exception as e:
        print(f"❌ Error validating license: {e}")

def export_licenses():
    """Export all licenses to a file"""
    print("📤 LICENSE EXPORT")
    print("============================================================")
    
    filename = input("Enter filename (or press Enter for 'licenses_export.txt'): ").strip()
    if not filename:
        filename = f"licenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        license_manager = LicenseManager()
        success = license_manager.export_licenses(filename)
        
        if success:
            print(f"✅ Licenses exported successfully to: {filename}")
        else:
            print("❌ Failed to export licenses!")
        
    except Exception as e:
        print(f"❌ Error exporting licenses: {e}")

def main():
    """Main license manager menu"""
    while True:
        print("\n📋 DEFENCE ENGINE LICENSE MANAGER")
        print("============================================================")
        print("1. View All Licenses")
        print("2. Search License")
        print("3. Validate License")
        print("4. Export Licenses")
        print("5. Exit")
        print("============================================================")
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            show_all_licenses()
        elif choice == '2':
            search_license()
        elif choice == '3':
            validate_license()
        elif choice == '4':
            export_licenses()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please select 1-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
