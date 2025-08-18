#!/usr/bin/env python3
"""
Test script to verify NO pandas imports exist in the codebase
This ensures Render deployment will not try to install pandas
"""
import os
import re
import sys

def check_file_for_pandas(filepath):
    """Check a single file for pandas imports"""
    pandas_patterns = [
        r'^import pandas(?!\s+#.*fallback)',  # Direct import pandas (not in fallback)
        r'from pandas',
        r'^import\s+pandas\s+as\s+pd(?!\s+#.*fallback)',  # import pandas as pd (not in fallback)
    ]
    
    # These are OK - they're in try/except blocks
    allowed_patterns = [
        r'try:',
        r'except',
        r'PANDAS_AVAILABLE',
        r'#.*fallback',
        r'if PANDAS_AVAILABLE',
        r'# Try to import pandas'
    ]
    
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Skip lines that are OK (in try/except blocks or with fallback comments)
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in allowed_patterns):
                    continue
                    
                # Check for problematic pandas patterns
                for pattern in pandas_patterns:
                    if re.search(pattern, line):
                        issues.append(f"Line {line_num}: {line.strip()}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return issues

def scan_project():
    """Scan entire project for pandas references"""
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        skip_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py') and file != 'verify_no_pandas.py':  # Skip this verification script
                python_files.append(os.path.join(root, file))
    
    print(f"🔍 Scanning {len(python_files)} Python files for pandas imports...")
    print("="*60)
    
    total_issues = 0
    files_with_issues = 0
    
    for filepath in python_files:
        issues = check_file_for_pandas(filepath)
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"\n❌ {filepath}:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print(f"✅ {filepath}")
    
    print("\n" + "="*60)
    print(f"📊 SCAN RESULTS:")
    print(f"   Files scanned: {len(python_files)}")
    print(f"   Files with pandas: {files_with_issues}")
    print(f"   Total pandas references: {total_issues}")
    
    if total_issues == 0:
        print("\n🎉 SUCCESS: No problematic pandas imports found!")
        print("   The project is ready for Render deployment!")
        return True
    else:
        print(f"\n⚠️  WARNING: Found {total_issues} pandas references that need fixing!")
        return False

def check_requirements():
    """Check requirements files for pandas"""
    req_files = ['requirements.txt', 'requirements_render.txt', 'requirements_minimal.txt']
    
    print("\n📦 Checking requirements files...")
    print("="*60)
    
    pandas_found = False
    
    for req_file in req_files:
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                content = f.read().lower()
                if 'pandas' in content or 'numpy' in content:
                    print(f"❌ {req_file}: Contains pandas/numpy")
                    pandas_found = True
                else:
                    print(f"✅ {req_file}: Clean (no pandas/numpy)")
        else:
            print(f"⚪ {req_file}: Not found")
    
    return not pandas_found

def main():
    """Main function"""
    print("🚀 AI Test Case Generator - Pandas-Free Verification")
    print("="*60)
    
    # Check Python files
    code_clean = scan_project()
    
    # Check requirements files
    req_clean = check_requirements()
    
    print("\n" + "="*60)
    print("🎯 FINAL VERDICT:")
    
    if code_clean and req_clean:
        print("✅ READY FOR RENDER DEPLOYMENT!")
        print("   No pandas dependencies found anywhere.")
        print("   Deployment should succeed without compilation issues.")
        return 0
    else:
        print("❌ NOT READY - Issues found!")
        if not code_clean:
            print("   → Fix pandas imports in Python files")
        if not req_clean:
            print("   → Remove pandas from requirements files")
        return 1

if __name__ == '__main__':
    sys.exit(main())
