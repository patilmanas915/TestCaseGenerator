#!/usr/bin/env python3
"""
Test script to verify Render deployment readiness
"""
import os
import sys
import importlib

def test_imports():
    """Test that all required modules can be imported"""
    required_modules = [
        'flask',
        'flask_cors',
        'google.generativeai',
        'pandas',
        'python-dotenv',
        'PyPDF2',
        'werkzeug',
        'gunicorn',
        'python-docx',
        'openpyxl'
    ]
    
    print("🔍 Testing module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            if module == 'python-dotenv':
                importlib.import_module('dotenv')
            elif module == 'python-docx':
                importlib.import_module('docx')
            elif module == 'PyPDF2':
                importlib.import_module('PyPDF2')
            else:
                importlib.import_module(module.replace('-', '_'))
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_environment():
    """Test environment variables"""
    print("\n🔧 Testing environment variables...")
    
    required_vars = ['GEMINI_API_KEY', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {'*' * min(len(value), 20)}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def test_app_startup():
    """Test that the Flask app can start"""
    print("\n🚀 Testing Flask app startup...")
    
    try:
        # Set test environment
        os.environ['RENDER'] = 'true'
        os.environ['FLASK_ENV'] = 'production'
        
        from app import app
        
        # Test app configuration
        print(f"✅ Flask app created successfully")
        print(f"✅ Upload folder: {app.config['UPLOAD_FOLDER']}")
        print(f"✅ Download folder: {app.config['DOWNLOAD_FOLDER']}")
        print(f"✅ Debug mode: {app.debug}")
        
        # Test health endpoint
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Flask app startup failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Test Case Generator - Render Deployment Test\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Environment Variables", test_environment),
        ("Flask App Startup", test_app_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {test_name}")
        print('='*50)
        result = test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*50}")
    print("TEST RESULTS SUMMARY")
    print('='*50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Ready for Render deployment!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix issues before deploying.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
