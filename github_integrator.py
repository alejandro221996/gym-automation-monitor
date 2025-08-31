#!/usr/bin/env python3
"""
🚀 GitHub Integration for Automated Issue & PR Creation
Integrates with MCP GitHub tools to create issues and PRs from log errors
"""

import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from log_monitor import LogMonitor, LogError

class GitHubIntegrator:
    """Integrates log monitoring with GitHub issue/PR creation"""
    
    def __init__(self, repo_owner: str, repo_name: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.created_issues = {}  # Track created issues to avoid duplicates
    
    def create_issue_from_error(self, error: LogError) -> Dict:
        """Create a GitHub issue from a log error"""
        
        # Generate issue title
        title = f"🐛 {error.error_type.replace('_', ' ').title()}: {error.file_path}"
        
        # Generate issue body
        body = f"""## 🚨 Automated Error Detection

**Error Type:** `{error.error_type}`
**Severity:** `{error.severity}`
**File:** `{error.file_path}`
**Timestamp:** `{error.timestamp}`

### 📋 Error Details
```
{error.message}
```

### 🔧 Suggested Fix
{error.suggested_fix}

### 📊 Error Context
- **Log Level:** {error.level}
- **Detection Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Auto-generated:** This issue was created automatically by the log monitoring system

### ✅ Next Steps
1. Review the error details above
2. Implement the suggested fix
3. Test the solution
4. Close this issue when resolved

---
*This issue was automatically created by the Log Monitor system 🤖*"""

        # Determine labels based on error type
        labels = ['automated', 'bug']
        if error.error_type in ['database_error', 'server_error']:
            labels.extend(['critical', 'high-priority'])
        elif error.error_type == 'performance_issue':
            labels.extend(['performance', 'optimization'])
        elif error.error_type == 'authentication_error':
            labels.extend(['security', 'auth'])
        
        return {
            'title': title,
            'body': body,
            'labels': labels,
            'assignees': [],  # Can be configured
        }
    
    def create_pr_from_error(self, error: LogError, issue_number: int) -> Dict:
        """Create a GitHub PR with a fix for the error"""
        
        # Generate branch name
        branch_name = f"fix/{error.error_type}-{error.file_path.replace('/', '-').replace('.py', '')}-{issue_number}"
        
        # Generate PR title
        title = f"🔧 Fix: {error.error_type.replace('_', ' ').title()} in {error.file_path}"
        
        # Generate PR body
        body = f"""## 🔧 Automated Fix for Log Error

**Fixes:** #{issue_number}
**Error Type:** `{error.error_type}`
**File:** `{error.file_path}`

### 📋 Changes Made
This PR implements the suggested fix for the {error.error_type} detected in the logs.

### 🔍 Error Details
- **Timestamp:** {error.timestamp}
- **Message:** {error.message[:200]}...
- **Severity:** {error.severity}

### ✅ Solution Implemented
{error.suggested_fix}

### 🧪 Testing
- [ ] Manual testing completed
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Error no longer appears in logs

### 📊 Impact
- **Risk Level:** Low (automated fix with standard patterns)
- **Affected Areas:** {error.file_path}
- **Breaking Changes:** None expected

---
*This PR was automatically created by the Log Monitor system 🤖*

**Please review carefully before merging!**"""

        return {
            'branch': branch_name,
            'title': title,
            'body': body,
            'head': branch_name,
            'base': 'main'  # or 'master' depending on your default branch
        }
    
    def generate_fix_code(self, error: LogError) -> str:
        """Generate actual code fix based on error type"""
        
        if error.error_type == 'database_error':
            return self._generate_database_fix_code(error)
        elif error.error_type == 'authentication_error':
            return self._generate_auth_fix_code(error)
        elif error.error_type == 'validation_error':
            return self._generate_validation_fix_code(error)
        elif error.error_type == 'server_error':
            return self._generate_server_error_fix_code(error)
        elif error.error_type == 'performance_issue':
            return self._generate_performance_fix_code(error)
        else:
            return self._generate_generic_fix_code(error)
    
    def _generate_database_fix_code(self, error: LogError) -> str:
        """Generate database error fix code"""
        return f'''# Database Error Fix for {error.file_path}
# Added error handling and transaction management

from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

# Original code with added error handling
try:
    with transaction.atomic():
        # Your database operation here
        # This ensures atomicity and proper rollback on errors
        pass
except IntegrityError as e:
    logger.error(f"Database integrity error in {error.file_path}: {{e}}")
    # Handle the error appropriately
    raise ValidationError("Data integrity constraint violated")
except Exception as e:
    logger.error(f"Unexpected database error in {error.file_path}: {{e}}")
    raise
'''
    
    def _generate_auth_fix_code(self, error: LogError) -> str:
        """Generate authentication error fix code"""
        return f'''# Authentication Error Fix for {error.file_path}
# Added proper authentication checks and error handling

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

# For function-based views
@login_required
def your_view(request):
    try:
        # Your view logic here
        pass
    except PermissionDenied as e:
        logger.warning(f"Permission denied in {error.file_path}: {{e}}")
        return JsonResponse({{'error': 'Access denied'}}, status=403)

# For class-based views
class YourView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.warning(f"Unauthenticated access attempt in {error.file_path}")
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
'''
    
    def _generate_validation_fix_code(self, error: LogError) -> str:
        """Generate validation error fix code"""
        return f'''# Validation Error Fix for {error.file_path}
# Added comprehensive validation and error handling

from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class ImprovedForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        
        # Add your validation logic here
        if not cleaned_data.get('required_field'):
            logger.warning(f"Validation failed in {error.file_path}: Missing required field")
            raise forms.ValidationError("Required field is missing")
        
        return cleaned_data
    
    def clean_field_name(self):
        data = self.cleaned_data.get('field_name')
        if data and len(data) < 3:
            logger.warning(f"Validation failed in {error.file_path}: Field too short")
            raise forms.ValidationError("Field must be at least 3 characters long")
        return data

# In your view
def your_view(request):
    if request.method == 'POST':
        form = ImprovedForm(request.POST)
        if form.is_valid():
            # Process valid data
            pass
        else:
            logger.error(f"Form validation errors in {error.file_path}: {{form.errors}}")
            return JsonResponse({{'errors': form.errors}}, status=400)
'''
    
    def _generate_server_error_fix_code(self, error: LogError) -> str:
        """Generate server error fix code"""
        return f'''# Server Error Fix for {error.file_path}
# Added comprehensive error handling and logging

from django.http import JsonResponse
from django.shortcuts import render
import logging
import traceback

logger = logging.getLogger(__name__)

def your_view(request):
    try:
        # Your view logic here
        
        # Check for None values
        if hasattr(request, 'user') and request.user:
            # Safe to access user attributes
            pass
        
        # Safe attribute access
        data = getattr(request, 'data', {{}})
        
        return render(request, 'template.html', context)
        
    except AttributeError as e:
        logger.error(f"Attribute error in {error.file_path}: {{e}}")
        logger.error(f"Traceback: {{traceback.format_exc()}}")
        return JsonResponse({{'error': 'Internal server error'}}, status=500)
    
    except KeyError as e:
        logger.error(f"Key error in {error.file_path}: {{e}}")
        return JsonResponse({{'error': 'Missing required data'}}, status=400)
    
    except Exception as e:
        logger.error(f"Unexpected error in {error.file_path}: {{e}}")
        logger.error(f"Traceback: {{traceback.format_exc()}}")
        return JsonResponse({{'error': 'Internal server error'}}, status=500)
'''
    
    def _generate_performance_fix_code(self, error: LogError) -> str:
        """Generate performance issue fix code"""
        return f'''# Performance Fix for {error.file_path}
# Added query optimization and caching

from django.core.cache import cache
from django.db import models
from django.db.models import Prefetch
import logging

logger = logging.getLogger(__name__)

def optimized_view(request):
    # Cache key for this view
    cache_key = f"view_data_{{request.user.id if request.user.is_authenticated else 'anonymous'}}"
    
    # Try to get from cache first
    data = cache.get(cache_key)
    if data is None:
        logger.info(f"Cache miss in {error.file_path}, fetching from database")
        
        # Optimized database queries
        queryset = YourModel.objects.select_related(
            'related_field'
        ).prefetch_related(
            'many_to_many_field',
            Prefetch('reverse_foreign_key', queryset=RelatedModel.objects.select_related('another_field'))
        ).only(
            'id', 'name', 'created_at'  # Only fetch needed fields
        )
        
        data = list(queryset)
        
        # Cache for 5 minutes
        cache.set(cache_key, data, 300)
        logger.info(f"Data cached in {error.file_path}")
    else:
        logger.info(f"Cache hit in {error.file_path}")
    
    return render(request, 'template.html', {{'data': data}})

# Add database indexes in models.py
class YourModel(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # Add index for frequently queried fields
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name', 'created_at']),  # Composite index
            models.Index(fields=['-created_at']),  # For ordering
        ]
'''
    
    def _generate_generic_fix_code(self, error: LogError) -> str:
        """Generate generic error fix code"""
        return f'''# Generic Error Fix for {error.file_path}
# Added comprehensive error handling and logging

import logging
import traceback
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def improved_function():
    try:
        # Your original code here
        pass
        
    except Exception as e:
        logger.error(f"Error in {error.file_path}: {{e}}")
        logger.error(f"Traceback: {{traceback.format_exc()}}")
        
        # Handle the error appropriately
        # Return error response or re-raise as needed
        raise
'''

    def process_errors_batch(self, errors: List[LogError]) -> Dict:
        """Process a batch of errors and create issues/PRs"""
        results = {
            'issues_created': 0,
            'prs_created': 0,
            'errors_processed': 0,
            'skipped': 0
        }
        
        for error in errors:
            try:
                # Create issue data
                issue_data = self.create_issue_from_error(error)
                
                # Create PR data
                pr_data = self.create_pr_from_error(error, 999)  # Placeholder issue number
                
                # Generate fix code
                fix_code = self.generate_fix_code(error)
                
                print(f"📋 Would create issue: {issue_data['title']}")
                print(f"🔧 Would create PR: {pr_data['title']}")
                print(f"💻 Generated fix code ({len(fix_code)} chars)")
                
                results['errors_processed'] += 1
                
            except Exception as e:
                print(f"❌ Error processing {error.error_type}: {e}")
                results['skipped'] += 1
        
        return results

if __name__ == "__main__":
    # Example usage
    integrator = GitHubIntegrator("alejandro221996", "DjangoAppointments")
    
    # Create a sample error for testing
    from log_monitor import LogError
    
    sample_error = LogError(
        timestamp="2025-01-20 10:30:00",
        level="ERROR",
        message="DatabaseError: UNIQUE constraint failed: clients_client.email",
        file_path="clients/models.py",
        line_number=45,
        error_type="database_error",
        severity="high",
        suggested_fix="Add proper validation and error handling for unique constraints"
    )
    
    results = integrator.process_errors_batch([sample_error])
    print(f"📊 Processing results: {results}")