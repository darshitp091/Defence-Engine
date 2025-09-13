"""
Git Setup Script for Defence Engine
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def setup_git():
    """Setup Git repository for Defence Engine"""
    print("🛡️ Defence Engine - Git Repository Setup")
    print("=" * 50)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("Please install Git first: https://git-scm.com/downloads")
        return False
    
    # Initialize git repository
    if not os.path.exists('.git'):
        run_command("git init", "Initializing Git repository")
    
    # Configure git user (you can change these)
    run_command('git config user.name "darshitp091"', "Setting Git username")
    run_command('git config user.email "darshitp091@gmail.com"', "Setting Git email")
    
    # Add all files
    run_command("git add .", "Adding all files to Git")
    
    # Create initial commit
    run_command('git commit -m "Initial commit: Defence Engine v1.0 - Ultra-fast quantum security system"', 
                "Creating initial commit")
    
    # Set main branch
    run_command("git branch -M main", "Setting main branch")
    
    print("\n" + "=" * 50)
    print("🎉 Git repository setup completed!")
    print("\nNext steps:")
    print("1. Create a new repository on GitHub named 'defence-engine'")
    print("2. Run these commands to push to GitHub:")
    print("   git remote add origin https://github.com/darshitp091/defence-engine.git")
    print("   git push -u origin main")
    print("\nOr use GitHub CLI:")
    print("   gh repo create defence-engine --public --push")
    
    return True

if __name__ == "__main__":
    setup_git()