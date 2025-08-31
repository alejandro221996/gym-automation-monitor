#!/usr/bin/env python3
"""
🤖 Log Monitor Automation - ALL-IN-ONE Script
Simple, powerful automation system for log monitoring and GitHub integration

Usage:
    python automation.py setup          # Initial setup
    python automation.py scan           # Scan logs once
    python automation.py monitor        # Continuous monitoring
    python automation.py status         # Check status
    python automation.py simulate       # Add test errors
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.append(str(project_root))

class LogMonitorAutomation:
    """All-in-one automation system"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.config_file = self.script_dir / "config.json"
        self.log_file = self.script_dir / "automation.log"
        
        # Load configuration
        self.config = self.load_config()
        self.setup_logging()
        
        # Import components
        try:
            from log_monitor import LogMonitor
            from github_integrator import GitHubIntegrator
            
            self.log_monitor = LogMonitor(
                log_file_path=self.config['log_file_path'],
                repo_owner=self.config['repo_owner'],
                repo_name=self.config['repo_name']
            )
            
            self.github_integrator = GitHubIntegrator(
                repo_owner=self.config['repo_owner'],
                repo_name=self.config['repo_name']
            )
        except ImportError as e:
            print(f"[ERROR] Error importing components: {e}")
            sys.exit(1)
    
    def load_config(self) -> Dict:
        """Load or create configuration"""
        default_config = {
            "repo_owner": "alejandro221996",
            "repo_name": "DjangoAppointments",
            "log_file_path": "logs/gym_management.log",
            "monitor_interval": 60,
            "max_errors_per_batch": 10,
            "environment": "production"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"[WARN] Error loading config, using defaults: {e}")
        
        # Create default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"[CREATED] Default config: {self.config_file}")
        return default_config
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup(self):
        """Initial setup"""
        print("[SETUP] Setting up Log Monitor Automation...")
        
        # Create directories
        dirs = [
            self.script_dir / "logs",
            self.project_root / "logs",
            self.project_root / "fixes"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(exist_ok=True)
            print(f"[CREATED] Directory: {dir_path}")
        
        # Check log file
        log_path = Path(self.config['log_file_path'])
        if not log_path.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.touch()
            print(f"[CREATED] Log file: {log_path}")
        
        # Test components
        try:
            errors = self.log_monitor.monitor_logs(follow=False)
            print(f"[SUCCESS] Log monitor working - found {len(errors)} errors")
        except Exception as e:
            print(f"[ERROR] Log monitor test failed: {e}")
        
        print("[SUCCESS] Setup completed!")
        print(f"[CONFIG] Config file: {self.config_file}")
        print(f"[LOG] Log file: {self.log_file}")
        print("\n[NEXT STEPS]:")
        print("   python automation.py simulate  # Add test errors")
        print("   python automation.py scan      # Scan for errors")
        print("   python automation.py monitor   # Start monitoring")
    
    def simulate_errors(self):
        """Add test errors to log file"""
        print("[SIMULATE] Adding test errors to log file...")
        
        log_path = Path(self.config['log_file_path'])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        test_errors = [
            f"ERROR {datetime.now().strftime('%Y-%m-%d %H:%M:%S,123')} django.db.backends 12345 67890 DatabaseError: UNIQUE constraint failed: clients_client.email",
            f"ERROR {datetime.now().strftime('%Y-%m-%d %H:%M:%S,456')} django.request 12345 67890 Internal Server Error: AttributeError: 'NoneType' object has no attribute 'gym'",
            f"WARNING {datetime.now().strftime('%Y-%m-%d %H:%M:%S,789')} django.security 12345 67890 PermissionDenied: User does not have permission to access /admin/",
            f"ERROR {datetime.now().strftime('%Y-%m-%d %H:%M:%S,012')} django.request 12345 67890 ValidationError: Invalid membership plan selected",
            f"WARNING {datetime.now().strftime('%Y-%m-%d %H:%M:%S,345')} django.db 12345 67890 Slow query detected: SELECT * FROM clients_client took 2.5 seconds"
        ]
        
        with open(log_path, 'a', encoding='utf-8') as f:
            for error in test_errors:
                f.write(error + '\n')
        
        print(f"[SUCCESS] Added {len(test_errors)} test errors to {log_path}")
    
    def scan_logs(self):
        """Scan logs once and process errors"""
        print("[SCAN] Scanning logs for errors...")
        
        try:
            errors = self.log_monitor.monitor_logs(follow=False)
            
            if not errors:
                print("[SUCCESS] No errors found")
                return
            
            print(f"[FOUND] {len(errors)} errors to process")
            
            # Limit batch size
            max_batch = self.config['max_errors_per_batch']
            if len(errors) > max_batch:
                print(f"[LIMIT] Limiting to {max_batch} errors")
                errors = errors[:max_batch]
            
            processed = 0
            for error in errors:
                try:
                    print(f"\n[PROCESS] {error.error_type} in {error.file_path}")
                    
                    # Create issue (simulated)
                    issue_data = self.github_integrator.create_issue_from_error(error)
                    print(f"   [ISSUE] Would create: {issue_data['title']}")
                    
                    # Create PR (simulated)
                    pr_data = self.github_integrator.create_pr_from_error(error, 999)
                    print(f"   [PR] Would create: {pr_data['title']}")
                    
                    processed += 1
                    
                except Exception as e:
                    print(f"   [ERROR] Processing failed: {e}")
            
            print(f"\n[SUMMARY] {processed}/{len(errors)} errors processed")
            
        except Exception as e:
            print(f"[ERROR] Scan failed: {e}")
    
    def monitor_continuous(self):
        """Start continuous monitoring"""
        interval = self.config['monitor_interval']
        print(f"[MONITOR] Starting continuous monitoring (every {interval}s)")
        print("[INFO] Press Ctrl+C to stop")
        
        try:
            while True:
                print(f"\n[SCAN] Scanning at {datetime.now().strftime('%H:%M:%S')}")
                self.scan_logs()
                
                print(f"[WAIT] Waiting {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n[STOP] Monitoring stopped by user")
        except Exception as e:
            print(f"[ERROR] Monitoring error: {e}")
    
    def show_status(self):
        """Show system status"""
        print("[STATUS] Log Monitor Automation Status")
        print("=" * 40)
        
        # Config status
        print(f"[CONFIG] Configuration: {self.config_file}")
        print(f"   Repository: {self.config['repo_owner']}/{self.config['repo_name']}")
        print(f"   Log file: {self.config['log_file_path']}")
        print(f"   Interval: {self.config['monitor_interval']}s")
        
        # Log file status
        log_path = Path(self.config['log_file_path'])
        if log_path.exists():
            size = log_path.stat().st_size
            print(f"[LOG] Log file: {size} bytes")
        else:
            print("[LOG] Log file: NOT FOUND")
        
        # Recent activity
        if self.log_file.exists():
            print(f"[ACTIVITY] Automation log: {self.log_file}")
            try:
                with open(self.log_file) as f:
                    lines = f.readlines()
                    if lines:
                        print("   Recent activity:")
                        for line in lines[-3:]:
                            print(f"   {line.strip()}")
            except Exception:
                pass
        
        # Test scan
        try:
            errors = self.log_monitor.monitor_logs(follow=False)
            print(f"[SCAN] Current errors: {len(errors)} found")
        except Exception as e:
            print(f"[ERROR] Error scanning: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="🤖 Log Monitor Automation - All-in-one system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python automation.py setup      # Initial setup
  python automation.py simulate   # Add test errors
  python automation.py scan       # Scan logs once
  python automation.py monitor    # Continuous monitoring
  python automation.py status     # Show status
        """
    )
    
    parser.add_argument(
        'command',
        choices=['setup', 'simulate', 'scan', 'monitor', 'status'],
        help='Command to execute'
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    try:
        automation = LogMonitorAutomation()
        
        if args.command == 'setup':
            automation.setup()
        elif args.command == 'simulate':
            automation.simulate_errors()
        elif args.command == 'scan':
            automation.scan_logs()
        elif args.command == 'monitor':
            automation.monitor_continuous()
        elif args.command == 'status':
            automation.show_status()
            
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()