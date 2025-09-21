"""
Pure Supabase Build Script for Defence Engine
Creates standalone executable that connects to Supabase cloud database only
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_pure_supabase_executable():
    """Build pure Supabase standalone executable"""
    print("🔨 BUILDING PURE SUPABASE DEFENCE ENGINE EXECUTABLE")
    print("============================================================")
    
    try:
        # Clean previous builds
        build_dir = Path("build")
        dist_dir = Path("dist")
        spec_file = Path("defence_engine_pure_supabase.spec")
        
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        if spec_file.exists():
            spec_file.unlink()
        
        print("🔄 Building pure Supabase executable with PyInstaller...")
        
        # Build command with all necessary data files
        build_cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--console",
            "--name=DefenceEngine_Cloud",
            "--add-data=phases;phases",  # Include phases directory
            "--add-data=core;core",  # Include core directory
            "--add-data=ai;ai",  # Include ai directory
            "--add-data=service;service",  # Include service directory
            "--add-data=gui;gui",  # Include gui directory
            "--hidden-import=tkinter",
            "--hidden-import=threading",
            "--hidden-import=hashlib",
            "--hidden-import=json",
            "--hidden-import=datetime",
            "--hidden-import=random",
            "--hidden-import=time",
            "--hidden-import=os",
            "--hidden-import=sys",
            "--hidden-import=argparse",
            "--hidden-import=pathlib",
            "--hidden-import=requests",
            "--hidden-import=jwt",
            "--hidden-import=secrets",
            "--clean",
            "defence_engine_pure_supabase.py"
        ]
        
        print(f"Running: {' '.join(build_cmd)}")
        
        # Run build
        result = subprocess.run(build_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Pure Supabase executable built successfully!")
            
            # Check if executable exists
            exe_path = dist_dir / "DefenceEngine_Cloud.exe"
            if exe_path.exists():
                print(f"📁 Output: {exe_path}")
                print(f"📊 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
                
                # Create pure Supabase distribution package
                create_pure_supabase_distribution_package()
                return True
            else:
                print("❌ Executable not found after build")
                return False
        else:
            print("❌ Build failed!")
            print(f"Error: {result.stderr}")
            print(f"Output: {result.stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_pure_supabase_distribution_package():
    """Create pure Supabase distribution package"""
    print("\n📦 CREATING PURE SUPABASE DISTRIBUTION PACKAGE")
    print("============================================================")
    
    try:
        # Create distribution directory
        dist_package = Path("DefenceEngine_PureSupabase_Distribution")
        if dist_package.exists():
            shutil.rmtree(dist_package)
        dist_package.mkdir()
        
        # Copy executable
        exe_source = Path("dist/DefenceEngine_Cloud.exe")
        exe_dest = dist_package / "DefenceEngine_Cloud.exe"
        shutil.copy2(exe_source, exe_dest)
        
        # Create README for pure Supabase distribution
        readme_content = """# Defence Engine Pure Supabase - Cloud Version

## 🛡️ Advanced Security Protection System with Pure Cloud Database

This is the pure Supabase cloud version of the Defence Engine with real-time license validation.

## 🚀 How to Use

### 1. Interactive Mode (Default)
```
DefenceEngine_Cloud.exe
```

### 2. License Mode
```
DefenceEngine_Cloud.exe --mode license --license-key YOUR_LICENSE_KEY
```

## 🔑 License System

This version connects to Supabase cloud database only:
- **Pure Cloud License Validation** - Uses Supabase REST API only
- **No Local Database** - No SQLite or local files required
- **Real-time Validation** - Instant cloud checking
- **Professional Quality** - Enterprise cloud infrastructure

## 🛡️ Features

- **6 Phases of Protection**: Comprehensive security coverage
- **Real-time Threat Detection**: AI-powered analysis
- **Cloud License Validation**: Supabase REST API only
- **Background Protection**: Continuous monitoring
- **Professional Interface**: Easy to use

## 📊 Protection Phases

1. **Core Enhancement** - SHA-512, AI Detection, Behavioral Analysis
2. **Web Protection** - WAF, XSS, CSRF, Session Security
3. **Network Protection** - DDoS, Traffic Analysis, Firewall
4. **Malware Protection** - Real-time Scanning, Sandboxing
5. **Social Engineering Protection** - Email, Phishing, Education
6. **Advanced Protection** - AI, Mobile, Industrial, Quantum

## ⚠️ Important Notes

- This version connects to Supabase cloud database only
- Generate fresh licenses using the Supabase license generator
- No demo licenses included - only real cloud licenses work
- Full source code and commercial rights available for purchase

## 🎯 Testing Instructions

1. Generate a fresh license using Supabase license generator
2. Run the executable
3. Enter your fresh license key
4. Start protection
5. Observe real-time threat detection
6. Test all 6 phases of protection

## 📞 Contact

For commercial licensing and full source code access, please contact:
- Email: defence.engine@security.com
- Website: www.defenceengine.com
- License: Commercial use requires proper licensing

---
Defence Engine Pure Supabase v6.0 Professional
© 2024 Defence Engine Security Systems
"""
        
        with open(dist_package / "README.txt", "w", encoding='utf-8') as f:
            f.write(readme_content)
        
        # Create Supabase setup instructions
        setup_content = """DEFENCE ENGINE PURE SUPABASE - SETUP INSTRUCTIONS

## 🌐 Supabase Setup Required

### Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Create a new project
3. Get your project URL and API keys

### Step 2: Create Licenses Table
Run the SQL script in your Supabase SQL Editor:

```sql
-- Copy and paste the entire SUPABASE_SQL_SETUP.sql file
-- This creates the licenses table with proper permissions
```

### Step 3: Update Configuration
Edit supabase_config.py with your credentials:
- supabase_url: Your Supabase project URL
- supabase_key: Your Supabase anon key
- supabase_service_key: Your Supabase service key
- jwt_secret: Your JWT secret key

### Step 4: Generate Licenses
```
python supabase_pure_license_generator.py
```

### Step 5: Run Executable
```
DefenceEngine_PureSupabase.exe --mode license --license-key YOUR_LICENSE
```

## ✅ Benefits of Pure Supabase Version

- **Pure Cloud Database** - No local database issues
- **Real-time Validation** - Instant license checking
- **Scalable** - Handles multiple users
- **Secure** - REST API with proper authentication
- **Reliable** - Cloud infrastructure
- **Professional** - Enterprise-grade system

## 🎯 Perfect for Business Strategy

- **Testing Phase** - Professional cloud system for community testing
- **Sales Phase** - Enterprise-grade cloud infrastructure
- **Scalable** - Handles growth and multiple users
- **Secure** - REST API with proper authentication

© 2024 Defence Engine Security Systems
"""
        
        with open(dist_package / "SUPABASE_SETUP.txt", "w", encoding='utf-8') as f:
            f.write(setup_content)
        
        print("✅ Pure Supabase distribution package created!")
        print(f"📁 Package location: {dist_package}")
        print(f"📄 Files included:")
        print(f"   - DefenceEngine_PureSupabase.exe")
        print(f"   - README.txt")
        print(f"   - SUPABASE_SETUP.txt")
        
    except Exception as e:
        print(f"❌ Package creation error: {e}")

def main():
    """Main build function"""
    print("🚀 DEFENCE ENGINE PURE SUPABASE BUILDER")
    print("============================================================")
    print("🛡️ Creating pure Supabase standalone executable")
    print("============================================================")
    
    if build_pure_supabase_executable():
        print("\n🎉 PURE SUPABASE BUILD COMPLETED SUCCESSFULLY!")
        print("============================================================")
        print("✅ Pure Supabase standalone executable created")
        print("✅ Cloud database connection included")
        print("✅ No local database required")
        print("✅ Ready for cloud-based testing")
        print("============================================================")
        print("📁 Output files:")
        print("   - dist/DefenceEngine_PureSupabase.exe")
        print("   - DefenceEngine_PureSupabase_Distribution/ (Complete package)")
        print("============================================================")
    else:
        print("\n❌ PURE SUPABASE BUILD FAILED!")
        print("============================================================")

if __name__ == "__main__":
    main()
