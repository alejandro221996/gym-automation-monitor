# Project Structure

## File Organization

### Core Files (7 essential files)
```
automation/
├── automation.py           # Main entry point - handles all operations
├── config.json            # Single configuration file
├── deploy.py              # One-click deployment script
├── log_monitor.py         # Error detection and log parsing
├── github_integrator.py   # GitHub issue/PR creation
├── README.md              # Primary documentation
└── SIMPLE_GUIDE.md        # Quick start guide
```

### Documentation Files
- `README.md`: Main documentation with quick start
- `SIMPLE_GUIDE.md`: Simplified usage guide (Spanish/English)
- `DEPLOYMENT_ARCHITECTURE.md`: Production deployment recommendations

### Configuration
- `config.json`: Single source of truth for all settings
  - Repository information (owner, name)
  - Log file paths
  - Monitoring intervals
  - Environment settings

## Architecture Principles

### Simplification Focus
- **Reduced from 21 files to 7 files** (67% reduction)
- **Single command interface** via `automation.py`
- **One configuration file** instead of multiple configs
- **Centralized functionality** in main script

### Modular Design
- `LogMonitor`: Handles log parsing and error detection
- `GitHubIntegrator`: Manages GitHub API interactions
- `LogMonitorAutomation`: Main orchestrator class

### Deployment Strategy
- **Separate deployment**: Recommended to deploy independently from main Django app
- **Path flexibility**: Configurable log file paths for different environments
- **Environment awareness**: Production vs development configurations

## Naming Conventions

### Files
- Snake_case for Python files
- Descriptive names indicating purpose
- Main entry point always named `automation.py`

### Classes
- PascalCase (e.g., `LogMonitor`, `GitHubIntegrator`)
- Descriptive class names reflecting functionality

### Configuration Keys
- Snake_case in JSON config
- Clear, descriptive parameter names
- Grouped by functionality

## Error Handling Patterns
- Comprehensive logging throughout
- Graceful degradation on failures
- Clear error messages with suggested fixes
- Automatic retry mechanisms where appropriate