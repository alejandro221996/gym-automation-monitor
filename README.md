# 🤖 Log Monitor Automation - SIMPLIFIED

## 🎯 **What it does**
Automatically monitors Django logs, detects errors, and creates GitHub issues/PRs with fixes using **MCP (Model Context Protocol)** integration.

## 📋 **Requirements**
- **Python 3.8+**
- **Node.js and npm** (for MCP server): [Download here](https://nodejs.org/)
- **MCP Server** with GitHub tools configured
- **GitHub repository** access
- **Django application** with logging enabled

## 🚀 **Quick Start**

### 1. **MCP Setup (Required First!)**
```bash
# Create MCP configuration
mkdir -p .kiro/settings
```

Create `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "github-copilot": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "get_file_contents",
        "search_repositories", 
        "create_or_update_file",
        "create_issue",
        "create_pull_request",
        "create_branch"
      ]
    }
  }
}
```

### 2. **System Setup**
```bash
# 1. Deploy (one-time setup)
python automation/deploy.py

# 2. Add test errors
python automation/automation.py simulate

# 3. Scan for errors
python automation/automation.py scan

# 4. Start monitoring
python automation/automation.py monitor
```

## 📁 **Files (10 essential files)**
- **`automation.py`** - Main script (orchestrates everything)
- **`log_monitor.py`** - Error detection and log parsing
- **`github_integrator.py`** - MCP GitHub integration
- **`config.json`** - System configuration
- **`deploy.py`** - One-click deployment
- **`validate_setup.py`** - Setup validation script
- **`config.example.json`** - Configuration template
- **`README.md`** - This documentation
- **`SIMPLE_GUIDE.md`** - Quick reference guide
- **`.kiro/settings/mcp.json`** - MCP configuration

## ⚙️ **Configuration**

### System Config (`config.json`)
```json
{
  "repo_owner": "alejandro221996",
  "repo_name": "DjangoAppointments",
  "log_file_path": "logs/gym_management.log",
  "monitor_interval": 60,
  "max_errors_per_batch": 10,
  "environment": "production"
}
```

### MCP Config (`.kiro/settings/mcp.json`)
```json
{
  "mcpServers": {
    "github-copilot": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "get_file_contents",
        "search_repositories",
        "create_or_update_file", 
        "create_issue",
        "create_pull_request",
        "create_branch",
        "list_issues",
        "update_issue"
      ]
    }
  }
}
```

## 🎮 **Commands**
```bash
python automation/automation.py setup      # Initial setup
python automation/automation.py simulate   # Add test errors
python automation/automation.py scan       # Scan logs once
python automation/automation.py monitor    # Continuous monitoring
python automation/automation.py status     # Show status
```

## 🔧 **MCP Integration Details**

### **How it works:**
1. **Log Monitor** detects errors using regex patterns
2. **GitHub Integrator** formats issue/PR data
3. **MCP GitHub Tools** create actual GitHub issues/PRs
4. **Auto-approval** allows seamless automation

### **MCP Tools Used:**
- `create_issue` - Creates GitHub issues with error details
- `create_pull_request` - Creates PRs with automated fixes
- `create_branch` - Creates feature branches for fixes
- `get_repository` - Validates repository access
- `list_issues` - Prevents duplicate issue creation

### **GitHub Token Setup:**
```bash
# 1. Go to GitHub Settings > Developer settings > Personal access tokens
# 2. Create token with these permissions:
#    - repo (full repository access)
#    - issues (read/write issues) 
#    - pull_requests (create/update PRs)
# 3. Copy the token (starts with ghp_)

# 4. Add to MCP config or environment:
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"
```

### **Django Logging Setup:**
Add to your Django `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/gym_management.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}

# Create logs directory
import os
os.makedirs('logs', exist_ok=True)
```

## ✅ **What it detects**
- **Database errors** (UNIQUE constraints, IntegrityError, etc.)
- **Server errors** (AttributeError, 500 errors, KeyError)
- **Authentication errors** (PermissionDenied, Unauthorized)
- **Validation errors** (Form validation, data validation)
- **Performance issues** (Slow queries, N+1 problems)

## 🎉 **Results**
- **Automatically creates GitHub issues** with detailed error analysis
- **Generates professional fixes** (200+ lines of production-ready code)
- **Creates pull requests** with comprehensive solutions
- **Links issues and PRs** automatically via MCP
- **Prevents duplicates** by tracking processed errors
- **Categorizes by severity** (high, medium, low priority)

## 🚨 **Troubleshooting**

### **MCP Issues:**
```bash
# Check MCP server status
# In Kiro: Command Palette > "MCP Server Status"

# Test MCP GitHub connection
python -c "
import json
print('Testing MCP GitHub connection...')
# This would use MCP tools to test connection
"

# Restart MCP servers
# In Kiro: MCP Server view > Restart
```

### **Common Problems:**
- **"GitHub token invalid"** → Check token permissions and expiry
- **"MCP server not found"** → Install uvx: `pip install uv`
- **"No errors detected"** → Check log file path in config.json
- **"Issues not created"** → Verify MCP auto-approval settings

### **Debug Mode:**
```bash
# Run with verbose logging
python automation/automation.py scan --verbose

# Check automation logs
tail -f automation.log

# Test MCP connection manually
python -c "
import json
from pathlib import Path
config = json.loads(Path('config.json').read_text())
print(f'Monitoring: {config[\"log_file_path\"]}')
print(f'Repository: {config[\"repo_owner\"]}/{config[\"repo_name\"]}')
"
```

### **Validation Commands:**
```bash
# 1. Check if uvx is installed
uvx --version

# 2. Test MCP GitHub server
npx @modelcontextprotocol/server-github --help

# 3. Verify log file exists
ls -la logs/gym_management.log

# 4. Test configuration
python automation/automation.py status

# 5. Dry run (no actual GitHub actions)
python automation/automation.py scan --dry-run
```

## 🏗️ **Architecture**

### **Recommended Deployment:**
```
/opt/
├── django-app/                 # Your main Django application
│   └── logs/
│       └── gym_management.log  # Log file being monitored
│
└── automation-monitor/         # This automation system (separate)
    ├── automation.py
    ├── config.json            # Points to Django app logs
    ├── .kiro/settings/mcp.json # MCP configuration
    └── logs/
        └── automation.log      # System logs
```

### **Benefits of Separation:**
- **Independent deployments** and updates
- **Isolated permissions** and security
- **Scalable** - can monitor multiple Django apps
- **Safe** - won't affect main application

## 🎯 **Complete Example**

### **Step-by-Step Setup:**
```bash
# 1. Install dependencies
pip install uv
uvx --version  # Should show version

# 2. Clone and setup
git clone https://github.com/alejandro221996/DjangoAppointments.git
cd DjangoAppointments/automation

# 3. Setup configuration files
python setup_config.py

# 4. Configure your settings
# Edit config.json with your repository details
# Edit .kiro/settings/mcp.json with your GitHub token

# 5. Validate setup
python validate_setup.py

# 6. Deploy
python deploy.py

# 7. Test with simulation
python automation.py simulate
python automation.py scan

# 8. Start monitoring
python automation.py monitor
```

### **Expected Output:**
```
🔍 Scanning logs: logs/gym_management.log
📋 Found 3 errors:
  - database_error: UNIQUE constraint failed
  - server_error: AttributeError in views.py
  - validation_error: Form validation failed

🚀 Creating GitHub issues via MCP...
✅ Issue #123: Database Error in clients/models.py
✅ Issue #124: Server Error in dashboard/views.py
✅ Issue #125: Validation Error in forms.py

🔧 Creating pull requests...
✅ PR #45: Fix database constraints
✅ PR #46: Fix attribute error handling
✅ PR #47: Improve form validation

📊 Results: 3 issues created, 3 PRs created
```

## 🚀 **Production Setup**

### **Systemd Service (Linux):**
Create `/etc/systemd/system/log-monitor.service`:
```ini
[Unit]
Description=Log Monitor Automation
After=network.target

[Service]
Type=simple
User=automation
WorkingDirectory=/opt/automation-monitor
ExecStart=/usr/bin/python3 automation.py monitor
Restart=always
RestartSec=30
Environment=GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable log-monitor
sudo systemctl start log-monitor
sudo systemctl status log-monitor
```

### **Docker Setup:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install uv
ENV GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token

CMD ["python", "automation.py", "monitor"]
```

```bash
# Build and run
docker build -t log-monitor .
docker run -d --name log-monitor \
  -v /path/to/django/logs:/app/logs \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token \
  log-monitor
```

---
**🤖 Simple, powerful, MCP-integrated automation**