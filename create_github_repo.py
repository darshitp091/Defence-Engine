"""
GitHub Repository Creation Helper
"""
import subprocess
import sys

def create_github_repo():
    """Create GitHub repository using GitHub CLI"""
    print("🛡️ Defence Engine - GitHub Repository Creation")
    print("=" * 50)
    
    # Check if GitHub CLI is installed
    try:
        result = subprocess.run("gh --version", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ GitHub CLI not found. Please install it from: https://cli.github.com/")
            print("\nAlternatively, create the repository manually:")
            print("1. Go to https://github.com/new")
            print("2. Repository name: defence-engine")
            print("3. Make it Public")
            print("4. Don't initialize with README")
            print("5. Click 'Create repository'")
            print("6. Then run: git push -u origin main")
            return False
    except Exception as e:
        print(f"❌ Error checking GitHub CLI: {e}")
        return False
    
    print("✅ GitHub CLI found")
    
    # Check if user is logged in
    try:
        result = subprocess.run("gh auth status", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not logged in to GitHub CLI")
            print("Please run: gh auth login")
            return False
    except Exception as e:
        print(f"❌ Error checking GitHub auth: {e}")
        return False
    
    print("✅ GitHub CLI authenticated")
    
    # Create repository
    try:
        print("\n🚀 Creating GitHub repository...")
        result = subprocess.run(
            'gh repo create defence-engine --public --description "🛡️ Ultra-fast quantum security system with AI-powered threat detection" --push',
            shell=True, capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("✅ Repository created and pushed successfully!")
            print(f"🌐 Repository URL: https://github.com/darshitp091/defence-engine")
            print("\n🎉 Your Defence Engine is now on GitHub!")
            return True
        else:
            print(f"❌ Failed to create repository: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating repository: {e}")
        return False

def manual_instructions():
    """Provide manual instructions"""
    print("\n📋 MANUAL SETUP INSTRUCTIONS:")
    print("=" * 40)
    print("1. Go to: https://github.com/new")
    print("2. Repository name: defence-engine")
    print("3. Description: 🛡️ Ultra-fast quantum security system with AI-powered threat detection")
    print("4. Make it: Public")
    print("5. Don't check: Initialize with README")
    print("6. Click: Create repository")
    print("\n7. Then run these commands:")
    print("   git push -u origin main")
    print("\n8. Your repository will be available at:")
    print("   https://github.com/darshitp091/defence-engine")

if __name__ == "__main__":
    if not create_github_repo():
        manual_instructions()