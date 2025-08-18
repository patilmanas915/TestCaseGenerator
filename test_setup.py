#!/usr/bin/env python3
"""
Test script to verify the AI Test Case Generator setup
"""

import os
import sys
from datetime import datetime

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("  ✅ Flask imported successfully")
    except ImportError as e:
        print(f"  ❌ Flask import failed: {e}")
        return False
    
    try:
        # Try to import pandas, but don't fail if not available
        try:
            import pandas
            print("  ✅ Pandas imported successfully")
        except ImportError:
            print("  ⚠️  Pandas not available (OK for Render deployment)")
    except Exception as e:
        print(f"  ⚠️  Pandas check failed: {e}")
        # Don't return False for pandas import failure
    
    try:
        import google.generativeai
        print("  ✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"  ❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("  ✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"  ❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        import docx
        print("  ✅ python-docx imported successfully")
    except ImportError as e:
        print(f"  ❌ python-docx import failed: {e}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\n📁 Testing directories...")
    
    required_dirs = ['uploads', 'downloads', 'templates']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"  ✅ Directory '{dir_name}' exists")
        else:
            print(f"  ❌ Directory '{dir_name}' missing")
            return False
    
    return True

def test_files():
    """Test if required files exist"""
    print("\n📄 Testing files...")
    
    required_files = [
        'app.py',
        'config.py',
        'gemini_client.py',
        'document_processor.py',
        'test_generator.py',
        'requirements.txt',
        'templates/index.html'
    ]
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"  ✅ File '{file_name}' exists")
        else:
            print(f"  ❌ File '{file_name}' missing")
            return False
    
    return True

def test_configuration():
    """Test configuration"""
    print("\n⚙️  Testing configuration...")
    
    if os.path.exists('.env'):
        print("  ✅ .env file exists")
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            if os.getenv('SECRET_KEY'):
                print("  ✅ SECRET_KEY is configured")
            else:
                print("  ⚠️  SECRET_KEY not found in .env")
            
            if os.getenv('GEMINI_API_KEY'):
                print("  ✅ GEMINI_API_KEY is configured")
            else:
                print("  ⚠️  GEMINI_API_KEY not found in .env")
                print("     Please add your Google Gemini API key to .env file")
        
        except ImportError:
            print("  ❌ python-dotenv not installed")
            return False
    else:
        print("  ⚠️  .env file not found")
        print("     Please create .env file with your configuration")
    
    return True

def test_app_import():
    """Test if the main app can be imported"""
    print("\n🚀 Testing app import...")
    
    try:
        from app import app
        print("  ✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Failed to import Flask app: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Test Case Generator - Setup Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version: {sys.version}")
    print(f"Current Directory: {os.getcwd()}")
    print()
    
    tests = [
        test_imports,
        test_directories,
        test_files,
        test_configuration,
        test_app_import
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Configure your .env file with GEMINI_API_KEY")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
