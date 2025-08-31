#!/usr/bin/env python3
"""
🚀 Prepare Deployment Script
Helps you prepare the automation system for production deployment
"""

import os
import shutil
import json
from pathlib import Path

def create_production_structure():
    """Create the recommended production structure"""
    
    print("🏗️ Creating Production Deployment Structure")
    print("=" * 50)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Create deployment directory
    deployment_dir = project_root / "deployment"
    deployment_dir.mkdir(exist_ok=True)
    
    # Create automation-monitor directory
    monitor_dir = deployment_dir / "automation-monitor"
    monitor_dir.mkdir(exist_ok=True)
    
    print(f"📁 Created: {monitor_dir}")
    
    # Essential files to copy
    essential_files = [
        "automation.py",
        "config.json", 
        "deploy.py",
        "log_monitor.py",
        "github_integrator.py",
        "README.md"
    ]
    
    # Copy essential files
    for file_name in essential_files:
        src_file = script_dir / file_name
        if src_file.exists():
            dst_file = monitor_dir / file_name
            shutil.copy2(src_file, dst_file)
            print(f"✅ Copied: {file_name}")
        else:
            print(f"⚠️ Missing: {file_name}")
    
    # Create production config
    prod_config = {
        "repo_owner": "alejandro221996",
        "repo_name": "DjangoAppointments", 
        "log_file_path": "/opt/gym-app/logs/gym_management.log",
        "monitor_interval": 300,
        "max_errors_per_batch": 5,
        "environment": "production"
    }
    
    prod_config_file = monitor_dir / "config.production.json"
    with open(prod_config_file, 'w') as f:
        json.dump(prod_config, f, indent=2)
    
    print(f"✅ Created: config.production.json")
    
    # Create deployment instructions
    instructions = """# 🚀 Production Deployment Instructions

## 1. Upload to Server
```bash
# Upload the automation-monitor directory to your server
scp -r deployment/automation-monitor/ user@server:/opt/
```

## 2. Setup on Server
```bash
# On your server
cd /opt/automation-monitor

# Use production config
cp config.production.json config.json

# Deploy
python deploy.py
```

## 3. Configure Monitoring
```bash
# Edit config if needed
nano config.json

# Start monitoring
python automation.py monitor
```

## 4. Setup as Service (Optional)
```bash
# Create systemd service
sudo nano /etc/systemd/system/gym-automation.service

# Enable and start
sudo systemctl enable gym-automation
sudo systemctl start gym-automation
```
"""
    
    instructions_file = monitor_dir / "DEPLOYMENT_INSTRUCTIONS.md"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ Created: DEPLOYMENT_INSTRUCTIONS.md")
    
    # Create systemd service file
    service_content = """[Unit]
Description=Gym Automation Monitor
After=network.target

[Service]
Type=simple
User=automation
WorkingDirectory=/opt/automation-monitor
ExecStart=/usr/bin/python3 automation.py monitor
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/automation-monitor

[Install]
WantedBy=multi-user.target
"""
    
    service_file = monitor_dir / "gym-automation.service"
    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(service_content)
    
    print(f"✅ Created: gym-automation.service")
    
    print(f"\n🎉 Production structure created!")
    print(f"📁 Location: {monitor_dir}")
    print(f"\n📋 Files created:")
    for item in monitor_dir.iterdir():
        if item.is_file():
            print(f"   ✅ {item.name}")
    
    print(f"\n🚀 Next steps:")
    print(f"1. Review files in: {monitor_dir}")
    print(f"2. Upload to server: scp -r {monitor_dir} user@server:/opt/")
    print(f"3. Follow instructions in: DEPLOYMENT_INSTRUCTIONS.md")

def create_separate_repo_structure():
    """Create structure for separate repository"""
    
    print("📦 Creating Separate Repository Structure")
    print("=" * 50)
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Create separate repo directory
    repo_dir = project_root / "gym-automation-monitor"
    repo_dir.mkdir(exist_ok=True)
    
    print(f"📁 Created: {repo_dir}")
    
    # Essential files to copy
    essential_files = [
        "automation.py",
        "config.json", 
        "deploy.py",
        "log_monitor.py",
        "github_integrator.py"
    ]
    
    # Copy essential files
    for file_name in essential_files:
        src_file = script_dir / file_name
        if src_file.exists():
            dst_file = repo_dir / file_name
            shutil.copy2(src_file, dst_file)
            print(f"✅ Copied: {file_name}")
    
    # Create README for separate repo
    readme_content = """# 🤖 Gym Automation Monitor

Automated log monitoring and GitHub integration system for Django applications.

## 🚀 Quick Start

```bash
# 1. Deploy
python deploy.py

# 2. Configure
nano config.json

# 3. Start monitoring
python automation.py monitor
```

## ⚙️ Configuration

Edit `config.json`:
```json
{
  "repo_owner": "your-username",
  "repo_name": "your-repo",
  "log_file_path": "/path/to/your/django.log",
  "monitor_interval": 300
}
```

## 🎮 Commands

```bash
python automation.py status    # Check status
python automation.py scan      # Scan logs once
python automation.py monitor   # Continuous monitoring
python automation.py simulate  # Add test errors
```

## 📊 What it does

- Monitors Django logs automatically
- Detects 5 types of errors (database, server, auth, validation, performance)
- Creates GitHub issues with error details
- Generates pull requests with automated fixes
- Provides continuous monitoring

## 🔧 Production Setup

See `DEPLOYMENT_INSTRUCTIONS.md` for production deployment guide.
"""
    
    readme_file = repo_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Created: README.md")
    
    # Create .gitignore
    gitignore_content = """# Logs
*.log
logs/

# Config with secrets
config.production.json

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    gitignore_file = repo_dir / ".gitignore"
    with open(gitignore_file, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print(f"✅ Created: .gitignore")
    
    print(f"\n🎉 Separate repository structure created!")
    print(f"📁 Location: {repo_dir}")
    print(f"\n📋 Files created:")
    for item in repo_dir.iterdir():
        if item.is_file():
            print(f"   ✅ {item.name}")
    
    print(f"\n🚀 Next steps:")
    print(f"1. cd {repo_dir}")
    print(f"2. git init")
    print(f"3. git add .")
    print(f"4. git commit -m 'Initial automation system'")
    print(f"5. Create GitHub repo and push")

def main():
    """Main function"""
    print("🚀 Gym Automation - Deployment Preparation")
    print("=" * 50)
    
    print("\nChoose deployment strategy:")
    print("1. Production deployment (same repo)")
    print("2. Separate repository (recommended)")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        create_production_structure()
    elif choice == "2":
        create_separate_repo_structure()
    elif choice == "3":
        create_production_structure()
        print("\n" + "="*50)
        create_separate_repo_structure()
    else:
        print("❌ Invalid choice")
        return
    
    print(f"\n✅ Deployment preparation completed!")

if __name__ == "__main__":
    main()