#!/usr/bin/env python3
"""
Comprehensive project scan for ALL potential deployment issues
"""
import os
import re
import sys

def scan_for_issues():
    """Scan for all potential deployment issues"""
    issues = []
    
    print("🔍 COMPREHENSIVE PROJECT SCAN")
    print("="*60)
    
    # 1. Check for pandas imports
    print("\n1️⃣ Checking for pandas imports...")
    pandas_files = []
    for root, dirs, files in os.walk('.'):
        skip_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', 'downloads', 'uploads'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py') and not file.startswith('scan_') and not file.startswith('verify_'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if re.search(r'import\s+pandas|from\s+pandas', content):
                            pandas_files.append(filepath)
                except:
                    pass
    
    if pandas_files:
        issues.append(f"❌ PANDAS IMPORTS FOUND: {pandas_files}")
    else:
        print("   ✅ No pandas imports found")
    
    # 2. Check requirements files
    print("\n2️⃣ Checking requirements files...")
    req_files = ['requirements.txt', 'requirements_render.txt', 'requirements_minimal.txt']
    for req_file in req_files:
        if os.path.exists(req_file):
            try:
                with open(req_file, 'r') as f:
                    content = f.read().lower()
                    if 'pandas' in content or 'numpy' in content:
                        issues.append(f"❌ PANDAS/NUMPY IN {req_file}")
                    else:
                        print(f"   ✅ {req_file} is clean")
            except:
                pass
    
    # 3. Check for required files
    print("\n3️⃣ Checking for required files...")
    required_files = [
        'app.py', 'config.py', '.env', 'templates/index.html',
        'requirements_render.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"   ✅ {file} exists")
    
    if missing_files:
        issues.extend([f"❌ MISSING FILE: {f}" for f in missing_files])
    
    # 4. Check if test_generator_no_pandas.py exists
    print("\n4️⃣ Checking pandas-free generator...")
    if os.path.exists('test_generator_no_pandas.py'):
        print("   ✅ test_generator_no_pandas.py exists")
    elif os.path.exists('test_generator_render.py'):
        print("   ✅ test_generator_render.py exists")
    else:
        issues.append("❌ MISSING: pandas-free test generator file")
    
    # 5. Check .env file
    print("\n5️⃣ Checking .env configuration...")
    if os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if 'GEMINI_API_KEY' not in content:
                    issues.append("❌ GEMINI_API_KEY not in .env")
                else:
                    print("   ✅ GEMINI_API_KEY configured")
        except:
            issues.append("❌ Cannot read .env")
    else:
        print("   ⚠️  .env file missing (but might be OK for Render)")
    
    # 6. Check Python syntax
    print("\n6️⃣ Checking Python syntax...")
    python_files = []
    for root, dirs, files in os.walk('.'):
        skip_dirs = {'.git', '__pycache__', '.venv', 'venv', 'downloads', 'uploads'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file in files:
            if file.endswith('.py') and not file.startswith('scan_'):
                python_files.append(os.path.join(root, file))
    
    syntax_errors = 0
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
                compile(code, filepath, 'exec')
        except SyntaxError as e:
            issues.append(f"❌ SYNTAX ERROR in {filepath}: {e}")
            syntax_errors += 1
        except:
            pass
    
    if syntax_errors == 0:
        print(f"   ✅ All {len(python_files)} Python files have valid syntax")
    
    # 7. Check for hardcoded paths
    print("\n7️⃣ Checking for hardcoded paths...")
    hardcoded_issues = []
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Check for Windows-style hardcoded paths
                if re.search(r'[C-Z]:\\', content):
                    hardcoded_issues.append(filepath)
        except:
            pass
    
    if hardcoded_issues:
        issues.extend([f"❌ HARDCODED PATH in {f}" for f in hardcoded_issues])
    else:
        print("   ✅ No hardcoded paths found")
    
    # 8. Check for large files
    print("\n8️⃣ Checking for large files...")
    large_files = []
    for root, dirs, files in os.walk('.'):
        skip_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', 'downloads', 'uploads'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                if size > 10 * 1024 * 1024:  # 10MB
                    large_files.append(f"{filepath} ({size/1024/1024:.1f}MB)")
            except:
                pass
    
    if large_files:
        issues.extend([f"❌ LARGE FILE: {f}" for f in large_files])
    else:
        print("   ✅ No large files found")
    
    # 9. Check key imports in app.py
    print("\n9️⃣ Checking app.py imports...")
    if os.path.exists('app.py'):
        try:
            with open('app.py', 'r') as f:
                content = f.read()
                if 'from flask import Flask' not in content:
                    issues.append("❌ app.py missing Flask import")
                else:
                    print("   ✅ Flask import found")
                
                if 'test_generator_no_pandas' in content or 'test_generator_render' in content:
                    print("   ✅ Using pandas-free generator")
                else:
                    issues.append("❌ app.py not configured for pandas-free operation")
        except:
            issues.append("❌ Cannot read app.py")
    
    # 10. Check render configuration
    print("\n🔟 Checking Render configuration...")
    render_configs = ['render.yaml', 'render_minimal.yaml', 'render_final.yaml']
    render_found = False
    for config in render_configs:
        if os.path.exists(config):
            render_found = True
            print(f"   ✅ {config} exists")
            break
    
    if not render_found:
        print("   ⚠️  No Render configuration file (will use defaults)")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SCAN COMPLETE")
    print("="*60)
    
    if issues:
        print(f"\n❌ FOUND {len(issues)} ISSUES:")
        for i, issue in enumerate(issues, 1):
            print(f"{i:2d}. {issue}")
        print(f"\n⚠️  FIX THESE ISSUES BEFORE DEPLOYING!")
        return False
    else:
        print("\n🎉 SUCCESS: NO ISSUES FOUND!")
        print("✅ Project is ready for Render deployment!")
        return True

if __name__ == '__main__':
    success = scan_for_issues()
    sys.exit(0 if success else 1)
