#!/usr/bin/env python3
"""
🚀 Simple Deployment Script
One-click deployment for Log Monitor Automation
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Failed: {result.stderr}")
            return False
        print(f"✅ {description} completed")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Log Monitor Automation - Simple Deployment")
    print("=" * 50)
    
    script_dir = Path(__file__).parent
    
    # Check Python
    if not run_command("python --version", "Checking Python"):
        print("❌ Python not found. Please install Python 3.8+")
        return False
    
    # Install dependencies (if requirements.txt exists)
    req_file = script_dir / "requirements.txt"
    if req_file.exists():
        if not run_command("pip install -r requirements.txt", "Installing dependencies"):
            print("⚠️ Some dependencies may have failed to install")
    
    # Run setup
    automation_script = script_dir / "automation.py"
    if automation_script.exists():
        if not run_command(f"python {automation_script} setup", "Running setup"):
            print("❌ Setup failed")
            return False
    else:
        print("❌ automation.py not found")
        return False
    
    print("\n🎉 Deployment completed!")
    print("\n📋 Next steps:")
    print(f"   python {automation_script} simulate  # Add test errors")
    print(f"   python {automation_script} scan      # Scan for errors")
    print(f"   python {automation_script} monitor   # Start monitoring")
    print(f"   python {automation_script} status    # Check status")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)