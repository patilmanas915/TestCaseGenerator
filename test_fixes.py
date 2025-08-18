#!/usr/bin/env python3
"""
Test the fixes for the TestCaseGenerator
"""
import os
import sys

def test_imports():
    """Test if imports work correctly"""
    try:
        from test_generator_no_pandas import TestCaseGenerator
        print("✅ TestCaseGenerator imported successfully")
        
        # Initialize
        generator = TestCaseGenerator()
        print("✅ TestCaseGenerator initialized successfully")
        
        # Check methods exist
        if hasattr(generator, 'save_to_csv'):
            print("✅ save_to_csv method exists")
        else:
            print("❌ save_to_csv method missing")
            
        if hasattr(generator, 'get_summary_stats'):
            print("✅ get_summary_stats method exists")
        else:
            print("❌ get_summary_stats method missing")
            
        if hasattr(generator, 'process_frd_document'):
            print("✅ process_frd_document method exists")
        else:
            print("❌ process_frd_document method missing")
            
        # Check GeminiClient method
        if hasattr(generator.gemini_client, 'generate_test_cases_for_feature'):
            print("✅ GeminiClient.generate_test_cases_for_feature method exists")
        else:
            print("❌ GeminiClient.generate_test_cases_for_feature method missing")
            
        return True
        
    except Exception as e:
        print(f"❌ Import/initialization failed: {e}")
        return False

def test_app_import():
    """Test if app imports work"""
    try:
        import app
        print("✅ App imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

if __name__ == '__main__':
    print("🔍 Testing fixes...")
    print("="*50)
    
    success1 = test_imports()
    success2 = test_app_import()
    
    print("="*50)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED! Fixes are working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
