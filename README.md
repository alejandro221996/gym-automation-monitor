# 🤖 Gym Automation Monitor

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
