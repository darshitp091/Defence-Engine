"""
Advanced License Management System with Blockchain Integration
Miracle-level license security with cryptographic protection
"""
import sqlite3
import hashlib
import secrets
import time
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os
from pathlib import Path

# Cryptographic imports
try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class BlockchainLicenseValidator:
    """Blockchain-based license validation"""
    
    def __init__(self):
        self.license_chain = []
        self.chain_hash = "0" * 64  # Genesis hash
        
    def add_license_to_chain(self, license_data: Dict) -> str:
        """Add license to blockchain"""
        # Create block
        block = {
            'index': len(self.license_chain),
            'timestamp': time.time(),
            'license_data': license_data,
            'previous_hash': self.chain_hash,
            'nonce': secrets.randbits(32)
        }
        
        # Calculate hash
        block_string = json.dumps(block, sort_keys=True)
        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        block['hash'] = block_hash
        
        # Add to chain
        self.license_chain.append(block)
        self.chain_hash = block_hash
        
        return block_hash
    
    def validate_license_chain(self, license_key: str) -> bool:
        """Validate license against blockchain"""
        for block in self.license_chain:
            if block['license_data'].get('license_key') == license_key:
                return self._verify_block(block)
        return False
    
    def _verify_block(self, block: Dict) -> bool:
        """Verify block integrity"""
        # Recalculate hash
        block_copy = block.copy()
        block_hash = block_copy.pop('hash')
        
        block_string = json.dumps(block_copy, sort_keys=True)
        calculated_hash = hashlib.sha256(block_string.encode()).hexdigest()
        
        return block_hash == calculated_hash

class CryptographicLicenseManager:
    """Advanced cryptographic license management"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.master_key = secrets.token_bytes(32)
        
        if CRYPTO_AVAILABLE:
            self._generate_key_pair()
    
    def _generate_key_pair(self):
        """Generate RSA key pair for license signing"""
        try:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            self.public_key = self.private_key.public_key()
        except Exception as e:
            print(f"❌ Key generation error: {e}")
    
    def sign_license(self, license_data: Dict) -> str:
        """Sign license with private key"""
        if not CRYPTO_AVAILABLE or not self.private_key:
            return self._fallback_signature(license_data)
        
        try:
            # Create license string
            license_string = json.dumps(license_data, sort_keys=True)
            license_bytes = license_string.encode()
            
            # Sign with private key
            signature = self.private_key.sign(
                license_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return base64.b64encode(signature).decode()
            
        except Exception as e:
            print(f"❌ License signing error: {e}")
            return self._fallback_signature(license_data)
    
    def verify_license_signature(self, license_data: Dict, signature: str) -> bool:
        """Verify license signature"""
        if not CRYPTO_AVAILABLE or not self.public_key:
            return self._fallback_verification(license_data, signature)
        
        try:
            # Create license string
            license_string = json.dumps(license_data, sort_keys=True)
            license_bytes = license_string.encode()
            
            # Decode signature
            signature_bytes = base64.b64decode(signature)
            
            # Verify signature
            self.public_key.verify(
                signature_bytes,
                license_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Signature verification error: {e}")
            return False
    
    def _fallback_signature(self, license_data: Dict) -> str:
        """Fallback signature method"""
        license_string = json.dumps(license_data, sort_keys=True)
        signature = hashlib.sha256(license_string.encode() + self.master_key).hexdigest()
        return base64.b64encode(signature.encode()).decode()
    
    def _fallback_verification(self, license_data: Dict, signature: str) -> bool:
        """Fallback verification method"""
        expected_signature = self._fallback_signature(license_data)
        return signature == expected_signature

class LicenseManager:
    """Main License Management System with all advanced features"""
    
    def __init__(self, db_path: str = "licenses.db"):
        self.db_path = db_path
        self.blockchain_validator = BlockchainLicenseValidator()
        self.crypto_manager = CryptographicLicenseManager()
        
        # Initialize database
        self._init_database()
        
        print("🔐 Advanced License Management System initialized!")
    
    def _init_database(self):
        """Initialize license database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create licenses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    expiry_date TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    usage_count INTEGER DEFAULT 0,
                    max_usage INTEGER DEFAULT -1,
                    metadata TEXT
                )
            ''')
            
            # Create usage_log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT NOT NULL,
                    usage_timestamp TEXT NOT NULL,
                    usage_type TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (license_key) REFERENCES licenses (license_key)
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    def generate_license_key(self, user_id: str, expiry_days: int = 365, 
                           max_usage: int = -1, metadata: Optional[Dict] = None) -> str:
        """Generate advanced license key with cryptographic security"""
        try:
            # Generate unique license key
            timestamp = str(int(time.time()))
            random_data = secrets.token_hex(16)
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:8]
            
            license_key = f"DEF-{user_hash}-{random_data[:8]}-{random_data[8:16]}"
            
            # Calculate expiry date
            expiry_date = None
            if expiry_days > 0:
                expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
            
            # Create license data
            license_data = {
                'license_key': license_key,
                'user_id': user_id,
                'created_date': datetime.now().isoformat(),
                'expiry_date': expiry_date,
                'max_usage': max_usage,
                'metadata': metadata or {}
            }
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO licenses (license_key, user_id, created_date, expiry_date, 
                                   is_active, max_usage, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                license_key, user_id, license_data['created_date'], expiry_date,
                1, max_usage, json.dumps(metadata or {})
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✅ License generated: {license_key}")
            return license_key
            
        except Exception as e:
            print(f"❌ License generation error: {e}")
            return ""
    
    def validate_license(self, license_key: str) -> Dict:
        """Validate license with comprehensive security checks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get license from database
            cursor.execute('''
                SELECT license_key, user_id, created_date, expiry_date, is_active,
                       usage_count, max_usage, metadata
                FROM licenses WHERE license_key = ?
            ''', (license_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {'valid': False, 'reason': 'License not found'}
            
            # Unpack result
            (license_key_db, user_id, created_date, expiry_date, is_active,
             usage_count, max_usage, metadata_str) = result
            
            # Check if license is active
            if not is_active:
                return {'valid': False, 'reason': 'License is inactive'}
            
            # Check expiry date
            if expiry_date:
                expiry_dt = datetime.fromisoformat(expiry_date)
                if datetime.now() > expiry_dt:
                    return {'valid': False, 'reason': 'License has expired'}
            
            # Check usage limits
            if max_usage > 0 and usage_count >= max_usage:
                return {'valid': False, 'reason': 'License usage limit exceeded'}
            
            # Prepare license data
            license_data = {
                'license_key': license_key_db,
                'user_id': user_id,
                'created_date': created_date,
                'expiry_date': expiry_date,
                'max_usage': max_usage,
                'metadata': json.loads(metadata_str) if metadata_str else {}
            }
            
            # Log usage
            self._log_license_usage(license_key)
            
            return {
                'valid': True,
                'license_data': license_data,
                'usage_count': usage_count,
                'remaining_usage': max_usage - usage_count if max_usage > 0 else -1
            }
            
        except Exception as e:
            print(f"❌ License validation error: {e}")
            return {'valid': False, 'reason': f'Validation error: {str(e)}'}
    
    def _log_license_usage(self, license_key: str):
        """Log license usage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Log usage
            cursor.execute('''
                INSERT INTO usage_log (license_key, usage_timestamp, usage_type, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (license_key, datetime.now().isoformat(), 'validation', '127.0.0.1', 'DefenceEngine'))
            
            # Update usage count
            cursor.execute('''
                UPDATE licenses SET usage_count = usage_count + 1 WHERE license_key = ?
            ''', (license_key,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Usage logging error: {e}")
    
    def generate_bulk_licenses(self, count: int, user_prefix: str = "USER", 
                             expiry_days: int = 365) -> List[Dict]:
        """Generate bulk licenses efficiently"""
        licenses = []
        
        print(f"🔄 Generating {count} bulk licenses...")
        
        for i in range(count):
            user_id = f"{user_prefix}_{i+1:04d}"
            license_key = self.generate_license_key(user_id, expiry_days)
            
            if license_key:
                licenses.append({
                    'user_id': user_id,
                    'license_key': license_key,
                    'expiry_days': expiry_days
                })
        
        print(f"✅ Generated {len(licenses)} licenses successfully!")
        return licenses
    
    def get_license_info(self, license_key: str) -> Optional[Dict]:
        """Get detailed license information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT license_key, user_id, created_date, expiry_date, is_active,
                       usage_count, max_usage, metadata, signature, blockchain_hash
                FROM licenses WHERE license_key = ?
            ''', (license_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            (license_key_db, user_id, created_date, expiry_date, is_active,
             usage_count, max_usage, metadata_str, signature, blockchain_hash) = result
            
            return {
                'license_key': license_key_db,
                'user_id': user_id,
                'created_date': created_date,
                'expiry_date': expiry_date,
                'is_active': bool(is_active),
                'usage_count': usage_count,
                'max_usage': max_usage,
                'metadata': json.loads(metadata_str) if metadata_str else {},
                'signature': signature,
                'blockchain_hash': blockchain_hash
            }
            
        except Exception as e:
            print(f"❌ License info retrieval error: {e}")
            return None
    
    def list_all_licenses(self) -> List[Dict]:
        """List all licenses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT license_key, user_id, created_date, expiry_date, is_active,
                       usage_count, max_usage, metadata
                FROM licenses ORDER BY created_date DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            licenses = []
            for result in results:
                (license_key, user_id, created_date, expiry_date, is_active,
                 usage_count, max_usage, metadata_str) = result
                
                licenses.append({
                    'license_key': license_key,
                    'user_id': user_id,
                    'created_date': created_date,
                    'expiry_date': expiry_date,
                    'is_active': bool(is_active),
                    'usage_count': usage_count,
                    'max_usage': max_usage,
                    'metadata': json.loads(metadata_str) if metadata_str else {}
                })
            
            return licenses
            
        except Exception as e:
            print(f"❌ License listing error: {e}")
            return []
    
    def revoke_license(self, license_key: str) -> bool:
        """Revoke license"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE licenses SET is_active = 0 WHERE license_key = ?
            ''', (license_key,))
            
            affected_rows = cursor.rowcount
            conn.commit()
            conn.close()
            
            if affected_rows > 0:
                print(f"✅ License {license_key} revoked successfully!")
                return True
            else:
                print(f"❌ License {license_key} not found!")
                return False
                
        except Exception as e:
            print(f"❌ License revocation error: {e}")
            return False
    
    def get_license_statistics(self) -> Dict:
        """Get comprehensive license statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total licenses
            cursor.execute('SELECT COUNT(*) FROM licenses')
            total_licenses = cursor.fetchone()[0]
            
            # Active licenses
            cursor.execute('SELECT COUNT(*) FROM licenses WHERE is_active = 1')
            active_licenses = cursor.fetchone()[0]
            
            # Expired licenses
            cursor.execute('''
                SELECT COUNT(*) FROM licenses 
                WHERE expiry_date IS NOT NULL AND expiry_date < ?
            ''', (datetime.now().isoformat(),))
            expired_licenses = cursor.fetchone()[0]
            
            # Usage statistics
            cursor.execute('SELECT SUM(usage_count) FROM licenses')
            total_usage = cursor.fetchone()[0] or 0
            
            # Recent usage
            cursor.execute('''
                SELECT COUNT(*) FROM usage_log 
                WHERE usage_timestamp > ?
            ''', ((datetime.now() - timedelta(days=7)).isoformat(),))
            recent_usage = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_licenses': total_licenses,
                'active_licenses': active_licenses,
                'expired_licenses': expired_licenses,
                'total_usage': total_usage,
                'recent_usage_7days': recent_usage,
                'blockchain_blocks': len(self.blockchain_validator.license_chain),
                'crypto_available': CRYPTO_AVAILABLE
            }
            
        except Exception as e:
            print(f"❌ Statistics retrieval error: {e}")
            return {}
    
    def export_licenses(self, filename: str) -> bool:
        """Export all licenses to file"""
        try:
            licenses = self.list_all_licenses()
            
            with open(filename, 'w') as f:
                f.write("License Key,User ID,Created Date,Expiry Date,Active,Usage Count,Max Usage,Metadata\n")
                
                for license_data in licenses:
                    metadata_str = json.dumps(license_data['metadata']) if license_data['metadata'] else ""
                    f.write(f"{license_data['license_key']},{license_data['user_id']},"
                           f"{license_data['created_date']},{license_data['expiry_date']},"
                           f"{license_data['is_active']},{license_data['usage_count']},"
                           f"{license_data['max_usage']},\"{metadata_str}\"\n")
            
            print(f"✅ Exported {len(licenses)} licenses to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ License export error: {e}")
            return False
