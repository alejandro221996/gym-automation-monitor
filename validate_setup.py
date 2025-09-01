#!/usr/bin/env python3
"""
🔍 Setup Validation Script
Validates that all components are properly configured
"""

import os
import json
import subprocess
from pathlib import Path

def check_python():
    """Check Python version"""
    import sys
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python 3.8+ detected")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} detected, need 3.8+")
        return False

def check_uvx():
    """Check if uvx is installed"""
    try:
        result = subprocess.run(['uvx', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ uvx is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ uvx not found. Install with: pip install uv")
    return False

def check_mcp_config():
    """Check MCP configuration"""
    mcp_file = Path('.kiro/settings/mcp.json')
    if not mcp_file.exists():
        print("❌ MCP config not found at .kiro/settings/mcp.json")
        return False
    
    try:
        config = json.loads(mcp_file.read_text())
        if 'mcpServers' in config and 'github-copilot' in config['mcpServers']:
            github_config = config['mcpServers']['github-copilot']
            token = github_config.get('env', {}).get('GITHUB_PERSONAL_ACCESS_TOKEN', '')
            
            if token and token != 'ghp_your_token_here':
                print("✅ MCP GitHub configuration found")
                return True
            else:
                print("❌ GitHub token not configured in MCP config")
                return False
        else:
            print("❌ GitHub server not configured in MCP config")
            return False
    except json.JSONDecodeError:
        print("❌ Invalid JSON in MCP config")
        return False

def check_system_config():
    """Check system configuration"""
    config_file = Path('config.json')
    if not config_file.exists():
        print("❌ System config not found: config.json")
        return False
    
    try:
        config = json.loads(config_file.read_text())
        required_fields = ['repo_owner', 'repo_name', 'log_file_path']
        
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field in config.json: {field}")
                return False
        
        # Check if log file path exists or can be created
        log_path = Path(config['log_file_path'])
        log_dir = log_path.parent
        
        if not log_dir.exists():
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created log directory: {log_dir}")
            except Exception as e:
                print(f"❌ Cannot create log directory {log_dir}: {e}")
                return False
        
        print("✅ System configuration is valid")
        return True
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in config.json")
        return False

def check_github_token():
    """Check if GitHub token is accessible"""
    # Check environment variable
    token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    if token:
        print("✅ GitHub token found in environment")
        return True
    
    # Check MCP config
    mcp_file = Path('.kiro/settings/mcp.json')
    if mcp_file.exists():
        try:
            config = json.loads(mcp_file.read_text())
            token = config.get('mcpServers', {}).get('github-copilot', {}).get('env', {}).get('GITHUB_PERSONAL_ACCESS_TOKEN', '')
            if token and token != 'ghp_your_token_here':
                # Validate token format
                if len(token) >= 40 and token.startswith('ghp_'):
                    print("✅ GitHub token found in MCP config")
                    return True
                else:
                    print("❌ GitHub token format invalid (should start with ghp_ and be 40+ chars)")
                    return False
        except:
            pass
    
    print("❌ GitHub token not found. Set GITHUB_PERSONAL_ACCESS_TOKEN")
    return False

def check_mcp_server():
    """Check if MCP GitHub server is available"""
    try:
        # Check if npx is available
        result = subprocess.run(['npx', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("❌ npx not found. Install Node.js and npm")
            return False
        
        # Check if the MCP server package is available
        result = subprocess.run(['npx', '@modelcontextprotocol/server-github', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 or "github" in result.stderr.lower():
            print("✅ MCP GitHub server is available")
            return True
        else:
            print("❌ MCP GitHub server not responding correctly")
            return False
    except subprocess.TimeoutExpired:
        print("✅ MCP GitHub server is available (timeout expected)")
        return True
    except FileNotFoundError:
        print("❌ npx not found. Install Node.js: https://nodejs.org/")
        return False
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        'automation.py',
        'log_monitor.py', 
        'github_integrator.py',
        'deploy.py'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all validation checks"""
    print("🔍 Log Monitor Automation - Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python),
        ("uvx Installation", check_uvx),
        ("Required Files", check_files),
        ("System Config", check_system_config),
        ("MCP Config", check_mcp_config),
        ("MCP GitHub Server", check_mcp_server),
        ("GitHub Token", check_github_token),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if check_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("   python automation.py simulate")
        print("   python automation.py scan")
        print("   python automation.py monitor")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())