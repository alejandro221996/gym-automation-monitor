# Product Overview

## Log Monitor Automation System

A simplified automation system that monitors Django application logs, automatically detects errors, and creates GitHub issues with suggested fixes and pull requests.

### Core Functionality
- **Automated Log Monitoring**: Continuously monitors Django log files for errors
- **Error Detection**: Identifies 5 types of common errors (database, authentication, validation, server, performance)
- **GitHub Integration**: Automatically creates GitHub issues with detailed error information
- **Fix Generation**: Generates professional code fixes (200+ lines) for detected issues
- **Pull Request Creation**: Creates ready-to-review PRs with automated fixes

### Key Features
- One-click deployment via `deploy.py`
- Single configuration file (`config.json`)
- Continuous monitoring with configurable intervals
- Professional error categorization and severity assessment
- Automatic linking between issues and PRs

### Target Use Case
Designed for Django applications that need automated error detection and resolution, particularly useful for production environments where quick error response is critical.