"""
Pure Supabase License Manager for Defence Engine
Uses only Supabase REST API with proper credentials
"""
import requests
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from supabase_config import supabase_config

class SupabasePureLicenseManager:
    """Pure Supabase-based license management system"""
    
    def __init__(self):
        self.config = supabase_config
        
        print("🔐 Pure Supabase License Management System initialized!")
        
        # Test connection
        if self._test_connection():
            print("✅ Supabase connection successful!")
        else:
            print("⚠️ Warning: Supabase connection failed. Please check configuration.")
    
    def _test_connection(self) -> bool:
        """Test Supabase connection"""
        try:
            response = requests.get(
                f"{self.config.base_url}/{self.config.licenses_table}",
                headers=self.config.get_headers(),
                params={"select": "count"},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Supabase connection test failed: {e}")
            return False
    
    def generate_license_key(self, user_id: str, expiry_days: int = 365, max_usage: int = -1) -> Optional[str]:
        """Generate a new license key and save to Supabase"""
        try:
            # Generate unique license key
            timestamp = str(int(datetime.now().timestamp()))
            random_data = secrets.token_hex(16)
            combined = f"{user_id}{timestamp}{random_data}"
            
            # Create license key with format: DEF-XXXXXXXX-XXXXXXXX-XXXXXXXX
            hash1 = hashlib.sha512(combined.encode()).hexdigest()[:8]
            hash2 = hashlib.sha512((combined + "salt1").encode()).hexdigest()[:8]
            hash3 = hashlib.sha512((combined + "salt2").encode()).hexdigest()[:8]
            
            license_key = f"DEF-{hash1}-{hash2}-{hash3}"
            
            # Calculate expiry date
            expiry_date = datetime.now() + timedelta(days=expiry_days)
            
            # Prepare license data
            license_data = {
                "generated_by": "defence_engine",
                "version": "4.0",
                "features": ["all_phases", "real_time_protection", "ai_detection"]
            }
            
            # Save to Supabase
            response = requests.post(
                f"{self.config.base_url}/{self.config.licenses_table}",
                headers=self.config.get_headers(use_service_key=True),
                json={
                    "license_key": license_key,
                    "user_id": user_id,
                    "created_date": datetime.now().isoformat(),
                    "expiry_date": expiry_date.isoformat(),
                    "is_active": True,
                    "usage_count": 0,
                    "max_usage": max_usage,
                    "metadata": json.dumps(license_data)
                },
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ License saved to Supabase: {license_key}")
                return license_key
            else:
                print(f"❌ Failed to save license to Supabase: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ License generation error: {e}")
            return None
    
    def validate_license(self, license_key: str) -> Dict:
        """Validate license key against Supabase database"""
        try:
            print(f"🔍 Validating license with Supabase cloud database...")
            
            # Query Supabase for license
            response = requests.get(
                f"{self.config.base_url}/{self.config.licenses_table}",
                headers=self.config.get_headers(),
                params={
                    "select": "*",
                    "license_key": f"eq.{license_key}"
                },
                timeout=10
            )
            
            if response.status_code != 200:
                return {'valid': False, 'reason': 'Database connection error'}
            
            licenses = response.json()
            
            if not licenses:
                return {'valid': False, 'reason': 'License not found'}
            
            license_data = licenses[0]
            
            # Check if license is active
            if not license_data.get('is_active', False):
                return {'valid': False, 'reason': 'License is inactive'}
            
            # Check expiry date
            expiry_date_str = license_data.get('expiry_date')
            if expiry_date_str:
                from datetime import timezone
                expiry_date = datetime.fromisoformat(expiry_date_str.replace('Z', '+00:00'))
                current_time = datetime.now(timezone.utc)
                if current_time > expiry_date:
                    return {'valid': False, 'reason': 'License has expired'}
            
            # Check usage limits
            usage_count = license_data.get('usage_count', 0)
            max_usage = license_data.get('max_usage', -1)
            if max_usage != -1 and usage_count >= max_usage:
                return {'valid': False, 'reason': 'License usage limit exceeded'}
            
            # Update usage count
            self._update_usage_count(license_key, usage_count + 1)
            
            return {
                'valid': True,
                'reason': 'License validated successfully',
                'user_id': license_data.get('user_id'),
                'expiry_date': expiry_date_str,
                'usage_count': usage_count + 1,
                'max_usage': max_usage
            }
            
        except Exception as e:
            return {'valid': False, 'reason': f'Validation error: {str(e)}'}
    
    def _update_usage_count(self, license_key: str, new_count: int):
        """Update usage count in Supabase"""
        try:
            response = requests.patch(
                f"{self.config.base_url}/{self.config.licenses_table}",
                headers=self.config.get_headers(use_service_key=True),
                params={"license_key": f"eq.{license_key}"},
                json={"usage_count": new_count},
                timeout=10
            )
            
            if response.status_code not in [200, 204]:
                print(f"⚠️ Warning: Failed to update usage count: {response.text}")
                
        except Exception as e:
            print(f"⚠️ Warning: Usage count update error: {e}")
    
    def get_license_info(self, license_key: str) -> Optional[Dict]:
        """Get license information from Supabase"""
        try:
            response = requests.get(
                f"{self.config.base_url}/{self.config.licenses_table}",
                headers=self.config.get_headers(),
                params={
                    "select": "*",
                    "license_key": f"eq.{license_key}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                licenses = response.json()
                if licenses:
                    return licenses[0]
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting license info: {e}")
            return None
    
    def list_all_licenses(self) -> List[Dict]:
        """List all licenses from Supabase"""
        try:
            response = requests.get(
                f"{self.config.base_url}/{self.config.licenses_table}",
                headers=self.config.get_headers(),
                params={"select": "*"},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to fetch licenses: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error listing licenses: {e}")
            return []
    
    def revoke_license(self, license_key: str) -> bool:
        """Revoke a license in Supabase"""
        try:
            response = requests.patch(
                f"{self.config.base_url}/{self.config.licenses_table}",
                headers=self.config.get_headers(use_service_key=True),
                params={"license_key": f"eq.{license_key}"},
                json={"is_active": False},
                timeout=10
            )
            
            return response.status_code in [200, 204]
            
        except Exception as e:
            print(f"❌ Error revoking license: {e}")
            return False

def main():
    """Test the pure Supabase license manager"""
    print("🧪 TESTING PURE SUPABASE LICENSE MANAGER")
    print("============================================================")
    
    manager = SupabasePureLicenseManager()
    
    # Test connection
    if manager._test_connection():
        print("✅ Supabase connection successful!")
        
        # Generate test license
        license_key = manager.generate_license_key("test_user", 30, 100)
        if license_key:
            print(f"✅ Test license generated: {license_key}")
            
            # Validate license
            result = manager.validate_license(license_key)
            print(f"✅ License validation: {result}")
        else:
            print("❌ Failed to generate test license")
    else:
        print("❌ Supabase connection failed. Please check configuration.")

if __name__ == "__main__":
    main()
