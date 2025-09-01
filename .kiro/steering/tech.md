# Technology Stack

## Core Technologies
- **Python 3.8+**: Main programming language
- **Standard Library**: Uses built-in modules (json, os, sys, pathlib, datetime, logging, subprocess)
- **MCP (Model Context Protocol)**: GitHub integration via MCP tools
- **No External Dependencies**: Designed to work with Python standard library + MCP

## Key Libraries Used
- `pathlib`: Modern file path handling
- `json`: Configuration and data serialization
- `logging`: Comprehensive logging system
- `subprocess`: System command execution
- `asyncio`: Asynchronous operations for GitHub integration
- `re`: Regular expression pattern matching for log parsing
- `dataclasses`: Structured data representation

## Architecture Patterns
- **Modular Design**: Separate classes for LogMonitor, GitHubIntegrator, and main automation
- **Configuration-Driven**: Single JSON config file controls all behavior
- **MCP Integration**: Uses MCP GitHub tools for issue/PR creation
- **Error Pattern Matching**: Regex-based error detection with categorization
- **Template-Based Fix Generation**: Structured approach to generating code fixes
- **Auto-Approval Workflow**: MCP tools are pre-approved for seamless automation

## Common Commands

### Setup and Deployment
```bash
# One-time deployment
python deploy.py

# Initial setup
python automation.py setup
```

### Daily Operations
```bash
# Check system status
python automation.py status

# Single scan of logs
python automation.py scan

# Continuous monitoring
python automation.py monitor

# Add test errors for validation
python automation.py simulate
```

### Development and Testing
```bash
# Run with verbose logging
python automation.py scan --verbose

# Test configuration
python automation.py status
```

## File Structure Conventions
- Main entry point: `automation.py`
- Configuration: `config.json`
- Deployment: `deploy.py`
- Modular components: `log_monitor.py`, `github_integrator.py`
- Documentation: Markdown files with emoji prefixes for clarity
##
 MCP Configuration

### Required MCP Server
- **GitHub MCP Server**: `mcp-server-github` via uvx
- **Auto-Approval**: Pre-configured for automation tools
- **Token Requirements**: GitHub Personal Access Token with repo, issues, and PR permissions

### MCP Tools Used
- `create_issue`: Creates GitHub issues from detected errors
- `create_pull_request`: Creates PRs with automated fixes
- `create_branch`: Creates feature branches for fixes
- `get_repository`: Validates repository access
- `list_issues`: Prevents duplicate issue creation
- `update_issue`: Updates existing issues with new information

### Configuration Files
- **System Config**: `config.json` (repository and monitoring settings)
- **MCP Config**: `.kiro/settings/mcp.json` (MCP server and GitHub integration)
- **Auto-Approval**: All GitHub tools pre-approved for seamless operation