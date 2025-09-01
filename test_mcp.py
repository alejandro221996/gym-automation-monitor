#!/usr/bin/env python3
"""
🧪 MCP GitHub Tools Test
Tests MCP GitHub integration to verify it's working correctly
"""

import json
import os
from pathlib import Path

def test_mcp_config():
    """Test MCP configuration"""
    print("🔍 Testing MCP Configuration...")
    
    mcp_file = Path('.kiro/settings/mcp.json')
    if not mcp_file.exists():
        print("❌ MCP config file not found")
        return False
    
    try:
        config = json.loads(mcp_file.read_text())
        github_config = config.get('mcpServers', {}).get('github-copilot', {})
        
        if not github_config:
            print("❌ GitHub-copilot server not configured")
            return False
        
        # Check command
        command = github_config.get('command')
        args = github_config.get('args', [])
        
        print(f"✅ Command: {command}")
        print(f"✅ Args: {args}")
        
        # Check token
        token = github_config.get('env', {}).get('GITHUB_PERSONAL_ACCESS_TOKEN', '')
        if token == 'ghp_your_token_here':
            print("⚠️  GitHub token is still placeholder - needs to be updated")
            return False
        elif token.startswith('ghp_'):
            print("✅ GitHub token configured (starts with ghp_)")
        else:
            print("❌ Invalid GitHub token format")
            return False
        
        # Check auto-approve
        auto_approve = github_config.get('autoApprove', [])
        required_tools = ['create_issue', 'create_pull_request', 'get_file_contents', 'search_repositories']
        
        for tool in required_tools:
            if tool in auto_approve:
                print(f"✅ {tool} is auto-approved")
            else:
                print(f"⚠️  {tool} not in auto-approve list")
        
        return True
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in MCP config")
        return False

def test_github_token():
    """Test GitHub token validity"""
    print("\n🔑 Testing GitHub Token...")
    
    # Try to get token from MCP config
    mcp_file = Path('.kiro/settings/mcp.json')
    if mcp_file.exists():
        try:
            config = json.loads(mcp_file.read_text())
            token = config.get('mcpServers', {}).get('github-copilot', {}).get('env', {}).get('GITHUB_PERSONAL_ACCESS_TOKEN', '')
            
            if token and token != 'ghp_your_token_here':
                print(f"✅ Token found: {token[:10]}...")
                
                # Basic format validation
                if len(token) >= 40 and token.startswith('ghp_'):
                    print("✅ Token format looks valid")
                    return True
                else:
                    print("❌ Token format invalid (should be 40+ chars, start with ghp_)")
                    return False
            else:
                print("❌ No valid token found")
                return False
                
        except Exception as e:
            print(f"❌ Error reading token: {e}")
            return False
    
    return False

def main():
    """Main test function"""
    print("🧪 MCP GitHub Integration Test")
    print("=" * 40)
    
    tests = [
        ("MCP Configuration", test_mcp_config),
        ("GitHub Token", test_github_token),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        if test_func():
            passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All MCP tests passed!")
        print("\n🚀 Next steps:")
        print("   1. Restart Kiro to reload MCP config")
        print("   2. Check MCP Server status in Kiro")
        print("   3. Try using GitHub MCP tools")
    else:
        print("❌ Some MCP tests failed.")
        print("\n🔧 To fix:")
        print("   1. Update your GitHub token in .kiro/settings/mcp.json")
        print("   2. Ensure token has repo, issues, and PR permissions")
        print("   3. Restart Kiro MCP servers")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())