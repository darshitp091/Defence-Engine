"""
Supabase Configuration for Defence Engine
Cloud database connection with JWT authentication
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
import requests
import jwt

class SupabaseConfig:
    """Supabase configuration and connection management"""
    
    def __init__(self):
        # Supabase configuration
        self.supabase_url = "https://wuzjrpezzqgibkcsxigb.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1empycGV6enFnaWJrY3N4aWdiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg0NTE5MzYsImV4cCI6MjA3NDAyNzkzNn0.NNXNNTEJybLoR7GjKhbCOrY_bVHqohLZBykAh5Fgv-c"
        self.supabase_service_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1empycGV6enFnaWJrY3N4aWdiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODQ1MTkzNiwiZXhwIjoyMDc0MDI3OTM2fQ.gRqvugB-dLKHJjdOi7WVCAkt7U-_NhSy84MJzTKD5Vw"
        
        # PostgreSQL direct connection (URL encoded password)
        self.postgres_url = "postgresql://postgres:Defence%402025@db.wuzjrpezzqgibkcsxigb.supabase.co:5432/postgres"
        
        # JWT configuration
        self.jwt_secret = "defence_engine_jwt_secret_2024"  # Custom JWT secret for Defence Engine
        
        # API endpoints
        self.licenses_table = "licenses"
        self.base_url = f"{self.supabase_url}/rest/v1"
        
    def get_headers(self, use_service_key: bool = False) -> Dict[str, str]:
        """Get headers for Supabase API requests"""
        key = self.supabase_service_key if use_service_key else self.supabase_key
        
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
    
    def generate_jwt_token(self, user_id: str, expires_in_hours: int = 24) -> str:
        """Generate JWT token for user authentication"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow().timestamp() + (expires_in_hours * 3600),
            "iat": datetime.utcnow().timestamp(),
            "iss": "defence-engine"
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def test_connection(self) -> bool:
        """Test Supabase connection"""
        try:
            response = requests.get(
                f"{self.base_url}/{self.licenses_table}",
                headers=self.get_headers(),
                params={"select": "count"},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Supabase connection test failed: {e}")
            return False

# Global Supabase configuration instance
supabase_config = SupabaseConfig()
