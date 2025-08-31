#!/usr/bin/env python3
"""
🤖 Automated Log Monitor & Issue Creator
Monitors logs, detects errors, creates GitHub issues and PRs automatically
"""

import re
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class LogError:
    """Represents a detected error in logs"""
    timestamp: str
    level: str
    message: str
    file_path: str
    line_number: Optional[int]
    error_type: str
    severity: str
    suggested_fix: str

class LogMonitor:
    """Monitors logs and creates GitHub issues/PRs for detected errors"""
    
    def __init__(self, log_file_path: str, repo_owner: str, repo_name: str):
        self.log_file_path = Path(log_file_path)
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.processed_errors = set()
        
        # Error patterns with suggested fixes
        self.error_patterns = {
            'database_error': {
                'pattern': r'(DatabaseError|IntegrityError|OperationalError)',
                'severity': 'high',
                'labels': ['bug', 'database', 'critical'],
                'fix_template': self._get_database_fix
            },
            'authentication_error': {
                'pattern': r'(AuthenticationFailed|PermissionDenied|Unauthorized)',
                'severity': 'medium',
                'labels': ['bug', 'security', 'auth'],
                'fix_template': self._get_auth_fix
            },
            'validation_error': {
                'pattern': r'(ValidationError|Invalid.*|Bad.*Request)',
                'severity': 'medium',
                'labels': ['bug', 'validation'],
                'fix_template': self._get_validation_fix
            },
            'server_error': {
                'pattern': r'(500|Internal Server Error|AttributeError|KeyError)',
                'severity': 'high',
                'labels': ['bug', 'server-error', 'critical'],
                'fix_template': self._get_server_error_fix
            },
            'performance_issue': {
                'pattern': r'(slow query|timeout|performance)',
                'severity': 'medium',
                'labels': ['performance', 'optimization'],
                'fix_template': self._get_performance_fix
            }
        }
    
    def parse_log_line(self, line: str) -> Optional[LogError]:
        """Parse a log line and extract error information"""
        # Django log format: LEVEL YYYY-MM-DD HH:MM:SS,mmm module PID TID message
        log_pattern = r'(\w+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+(\w+)\s+\d+\s+\d+\s+(.*)'
        
        match = re.match(log_pattern, line.strip())
        if not match:
            return None
            
        level, timestamp, module, message = match.groups()
        
        # Check if this is an error we care about
        if level not in ['ERROR', 'CRITICAL', 'WARNING']:
            return None
            
        # Detect error type
        error_type = self._detect_error_type(message)
        if not error_type:
            return None
            
        # Extract file path if available
        file_path = self._extract_file_path(message)
        
        return LogError(
            timestamp=timestamp,
            level=level,
            message=message,
            file_path=file_path or f"{module}.py",
            line_number=None,
            error_type=error_type,
            severity=self.error_patterns[error_type]['severity'],
            suggested_fix=self.error_patterns[error_type]['fix_template'](message)
        )
    
    def _detect_error_type(self, message: str) -> Optional[str]:
        """Detect the type of error based on message content"""
        for error_type, config in self.error_patterns.items():
            if re.search(config['pattern'], message, re.IGNORECASE):
                return error_type
        return None
    
    def _extract_file_path(self, message: str) -> Optional[str]:
        """Extract file path from error message"""
        # Look for file paths in the message
        path_pattern = r'([a-zA-Z_][a-zA-Z0-9_/\\]*\.py)'
        match = re.search(path_pattern, message)
        return match.group(1) if match else None
    
    def _get_database_fix(self, message: str) -> str:
        """Generate database error fix"""
        return """
# Database Error Fix

## Suggested Solution:
1. Check database connection settings
2. Verify model constraints and relationships
3. Add proper error handling
4. Consider database migration if schema changed

```python
# Add to models.py or views.py
from django.db import transaction
from django.core.exceptions import ValidationError

try:
    with transaction.atomic():
        # Your database operation here
        pass
except IntegrityError as e:
    logger.error(f"Database integrity error: {e}")
    # Handle the error appropriately
```
"""
    
    def _get_auth_fix(self, message: str) -> str:
        """Generate authentication error fix"""
        return """
# Authentication Error Fix

## Suggested Solution:
1. Check user permissions and roles
2. Verify authentication middleware
3. Update login/logout views
4. Review session configuration

```python
# Add to views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def protected_view(request):
    # Your view logic here
    pass
```
"""
    
    def _get_validation_fix(self, message: str) -> str:
        """Generate validation error fix"""
        return """
# Validation Error Fix

## Suggested Solution:
1. Add proper form validation
2. Check model field constraints
3. Implement client-side validation
4. Add user-friendly error messages

```python
# Add to forms.py
from django import forms

class YourForm(forms.Form):
    def clean_field_name(self):
        data = self.cleaned_data['field_name']
        if not data:
            raise forms.ValidationError("This field is required")
        return data
```
"""
    
    def _get_server_error_fix(self, message: str) -> str:
        """Generate server error fix"""
        return """
# Server Error Fix

## Suggested Solution:
1. Add proper exception handling
2. Check for None values and missing attributes
3. Add logging for debugging
4. Implement graceful error responses

```python
# Add to views.py
import logging
logger = logging.getLogger(__name__)

def your_view(request):
    try:
        # Your view logic here
        pass
    except AttributeError as e:
        logger.error(f"Attribute error in view: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
```
"""
    
    def _get_performance_fix(self, message: str) -> str:
        """Generate performance issue fix"""
        return """
# Performance Issue Fix

## Suggested Solution:
1. Add database query optimization
2. Implement caching
3. Use select_related/prefetch_related
4. Add database indexes

```python
# Add to models.py or views.py
from django.core.cache import cache
from django.db import models

# Optimize queries
queryset = Model.objects.select_related('related_field').prefetch_related('many_to_many_field')

# Add caching
def get_cached_data(key):
    data = cache.get(key)
    if data is None:
        data = expensive_operation()
        cache.set(key, data, 300)  # Cache for 5 minutes
    return data
```
"""

    def create_error_signature(self, error: LogError) -> str:
        """Create a unique signature for the error to avoid duplicates"""
        return f"{error.error_type}:{error.file_path}:{hash(error.message[:100])}"
    
    def monitor_logs(self, follow: bool = False) -> List[LogError]:
        """Monitor log file for new errors"""
        errors = []
        
        if not self.log_file_path.exists():
            print(f"❌ Log file not found: {self.log_file_path}")
            return errors
        
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            if follow:
                # Follow mode - tail the file
                f.seek(0, 2)  # Go to end of file
                while True:
                    line = f.readline()
                    if line:
                        error = self.parse_log_line(line)
                        if error:
                            signature = self.create_error_signature(error)
                            if signature not in self.processed_errors:
                                errors.append(error)
                                self.processed_errors.add(signature)
                    else:
                        time.sleep(1)
            else:
                # One-time scan
                for line in f:
                    error = self.parse_log_line(line)
                    if error:
                        signature = self.create_error_signature(error)
                        if signature not in self.processed_errors:
                            errors.append(error)
                            self.processed_errors.add(signature)
        
        return errors

if __name__ == "__main__":
    # Example usage
    monitor = LogMonitor(
        log_file_path="logs/gym_management.log",
        repo_owner="alejandro221996",
        repo_name="DjangoAppointments"
    )
    
    print("🔍 Scanning logs for errors...")
    errors = monitor.monitor_logs()
    
    if errors:
        print(f"📊 Found {len(errors)} errors to process")
        for error in errors:
            print(f"  - {error.error_type}: {error.message[:80]}...")
    else:
        print("✅ No errors found in logs")