"""
Pure Supabase License Generator for Defence Engine
Generates licenses using only Supabase REST API
"""
import argparse
import os
import sys
from datetime import datetime

# Ensure the parent directory is in the path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase_pure_license_manager import SupabasePureLicenseManager

def main():
    """Main function for pure Supabase license generation"""
    parser = argparse.ArgumentParser(description="Defence Engine Pure Supabase License Generator")
    parser.add_argument('--user', type=str, default=None,
                       help="User ID for the license (e.g., 'client_name')")
    parser.add_argument('--expiry', type=int, default=365,
                       help="Number of days until the license expires (default: 365)")
    parser.add_argument('--usage', type=int, default=-1,
                       help="Maximum number of times the license can be used (-1 for unlimited, default: -1)")
    parser.add_argument('--count', type=int, default=1,
                       help="Number of licenses to generate (for bulk generation, default: 1)")
    
    args = parser.parse_args()
    
    print("🚀 DEFENCE ENGINE PURE SUPABASE LICENSE GENERATOR")
    print("=" * 60)
    print("🔐 PURE SUPABASE CLOUD LICENSE GENERATOR")
    print("=" * 60)
    
    license_manager = SupabasePureLicenseManager()
    
    # Test Supabase connection
    if not license_manager._test_connection():
        print("❌ Supabase connection failed. Please check configuration.")
        print("📋 Setup Instructions:")
        print("1. Run the SQL script in Supabase SQL Editor")
        print("2. Check your Supabase credentials")
        return
    
    if args.count > 1:
        print(f"🔄 Generating {args.count} licenses...")
        licenses = []
        for i in range(args.count):
            user_id = args.user if args.user else f"bulk_user_{i+1}"
            license_key = license_manager.generate_license_key(
                user_id=user_id,
                expiry_days=args.expiry,
                max_usage=args.usage
            )
            if license_key:
                licenses.append(license_key)
        print(f"✅ Generated {len(licenses)} licenses successfully!")
        print("\n📋 Generated Licenses:")
        for key in licenses:
            print(f"   - {key}")
    else:
        user_id = args.user
        if not user_id:
            user_id = input("Enter User ID (or press Enter for 'defence_user'): ").strip()
            if not user_id:
                user_id = "defence_user"
        
        expiry_days_input = input(f"Enter expiry days (or press Enter for {args.expiry}): ").strip()
        expiry_days = int(expiry_days_input) if expiry_days_input.isdigit() else args.expiry
        
        max_usage_input = input(f"Enter max usage (-1 for unlimited, or press Enter for {args.usage}): ").strip()
        max_usage = int(max_usage_input) if max_usage_input.lstrip('-').isdigit() else args.usage
        
        print(f"\n🔄 Generating license for user: {user_id}")
        print(f"   Expiry: {expiry_days} days")
        print(f"   Max Usage: {'Unlimited' if max_usage == -1 else max_usage}")
        print("🌐 Saving to Supabase cloud database...")
        
        license_key = license_manager.generate_license_key(
            user_id=user_id,
            expiry_days=expiry_days,
            max_usage=max_usage
        )
        
        if license_key:
            print("\n✅ LICENSE GENERATED SUCCESSFULLY!")
            print("=" * 60)
            print(f"🔑 License Key: {license_key}")
            print(f"👤 User ID: {user_id}")
            print(f"📅 Expiry: {expiry_days} days from now")
            print(f"🔢 Max Usage: {'Unlimited' if max_usage == -1 else max_usage}")
            print("🌐 Database: Supabase Cloud")
            print("=" * 60)
        else:
            print("❌ Failed to generate license.")
    
    print("\n📋 ALL LICENSES IN SUPABASE")
    print("=" * 60)
    all_licenses = license_manager.list_all_licenses()
    if all_licenses:
        print(f"📊 Found {len(all_licenses)} licenses:")
        print("=" * 60)
        for i, lic in enumerate(all_licenses):
            print(f"  {i+1}. {lic['license_key']}")
            print(f"     User: {lic['user_id']} | {'✅ Active' if lic['is_active'] else '❌ Inactive'}")
            print(f"     Created: {lic['created_date']}")
            print(f"     Expiry: {lic['expiry_date'] if lic['expiry_date'] else 'Never'}")
            print(f"     Usage: {lic['usage_count']}/{'∞' if lic['max_usage'] == -1 else lic['max_usage']}")
            print()
    else:
        print("No licenses found in Supabase database.")
    print("=" * 60)

if __name__ == "__main__":
    main()
