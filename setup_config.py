#!/usr/bin/env python3
"""
⚙️ Configuration Setup Script
Copies template files and helps with initial configuration
"""

import json
import shutil
from pathlib import Path

def setup_system_config():
    """Setup system configuration from template"""
    template_file = Path('config.example.json')
    config_file = Path('config.json')
    
    if config_file.exists():
        print("✅ config.json already exists")
        return True
    
    if not template_file.exists():
        print("❌ config.example.json template not found")
        return False
    
    # Copy template
    shutil.copy(template_file, config_file)
    print("✅ Created config.json from template")
    
    # Load and customize
    config = json.loads(config_file.read_text())
    
    print("\n🔧 Please customize config.json with your settings:")
    print(f"   - repo_owner: {config['repo_owner']}")
    print(f"   - repo_name: {config['repo_name']}")
    print(f"   - log_file_path: {config['log_file_path']}")
    
    return True

def setup_mcp_config():
    """Setup MCP configuration from template"""
    template_file = Path('.kiro/settings/mcp.example.json')
    config_file = Path('.kiro/settings/mcp.json')
    
    if config_file.exists():
        print("✅ .kiro/settings/mcp.json already exists")
        return True
    
    if not template_file.exists():
        print("❌ .kiro/settings/mcp.example.json template not found")
        return False
    
    # Ensure directory exists
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy template
    shutil.copy(template_file, config_file)
    print("✅ Created .kiro/settings/mcp.json from template")
    
    print("\n🔑 Please add your GitHub token to .kiro/settings/mcp.json:")
    print("   Replace 'ghp_your_token_here' with your actual GitHub Personal Access Token")
    print("   Make sure you have Node.js installed for the MCP server")
    
    return True

def main():
    """Main setup function"""
    print("⚙️ Configuration Setup")
    print("=" * 30)
    
    success = True
    
    print("\n1. Setting up system configuration...")
    if not setup_system_config():
        success = False
    
    print("\n2. Setting up MCP configuration...")
    if not setup_mcp_config():
        success = False
    
    if success:
        print("\n🎉 Configuration setup completed!")
        print("\n📋 Next steps:")
        print("   1. Edit config.json with your repository details")
        print("   2. Add your GitHub token to .kiro/settings/mcp.json")
        print("   3. Run: python validate_setup.py")
        print("   4. Run: python deploy.py")
    else:
        print("\n❌ Configuration setup failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())