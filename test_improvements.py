"""
Comprehensive test to verify test case generation improvements
"""
import os
import json
import csv
import sys
sys.path.append('.')

try:
    from test_generator_no_pandas import TestGenerator
    from gemini_client import GeminiClient
    
    print("=== Testing Test Case Generation Improvements ===\n")
    
    # Create a test generator
    test_gen = TestGenerator()
    
    # Create mock test cases with proper structure
    mock_test_cases = [
        {
            'feature_name': 'User Authentication',
            'feature_id': 'F001',
            'module': 'Security',
            'test_case_id': 'TC001',
            'test_case_name': 'Valid Login Test',
            'description': 'Test user login with valid credentials',
            'priority': 'High',
            'test_type': 'Functional',
            'complexity': 'Medium',
            'prerequisites': ['User account exists', 'System is running'],
            'test_steps': [
                'Navigate to login page',
                'Enter valid username',
                'Enter valid password', 
                'Click login button'
            ],
            'expected_result': 'User successfully logged in',
            'test_data': 'username: testuser, password: test123',
            'notes': 'Test with different browsers'
        },
        {
            'feature_name': 'Payment Processing',
            'feature_id': 'F002', 
            'module': 'Finance',
            'test_case_id': 'TC002',
            'test_case_name': 'Credit Card Payment',
            'description': 'Test credit card payment processing',
            'priority': 'Critical',
            'test_type': 'Functional',
            'complexity': 'High',
            'prerequisites': ['Valid credit card', 'Shopping cart has items'],
            'test_steps': [
                'Add items to cart',
                'Proceed to checkout',
                'Enter credit card details',
                'Confirm payment'
            ],
            'expected_result': 'Payment processed successfully',
            'test_data': 'Card: 4111111111111111, CVV: 123',
            'notes': 'Test with different card types'
        }
    ]
    
    # Set mock data
    test_gen.all_test_cases = mock_test_cases
    
    print("1. Testing CSV Export...")
    csv_filename, csv_message = test_gen.export_to_csv('./downloads')
    print(f"   CSV Result: {csv_message}")
    
    if csv_filename:
        csv_path = os.path.join('./downloads', csv_filename)
        if os.path.exists(csv_path):
            print(f"   ✓ CSV file created: {csv_filename}")
            
            # Read and display CSV content
            with open(csv_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   CSV Content Preview:\n{content[:500]}...")
        else:
            print(f"   ✗ CSV file not found: {csv_path}")
    
    print("\n2. Testing Excel Export...")
    try:
        excel_filename, excel_message = test_gen.export_to_excel('./downloads')
        print(f"   Excel Result: {excel_message}")
        
        if excel_filename:
            excel_path = os.path.join('./downloads', excel_filename)
            if os.path.exists(excel_path):
                print(f"   ✓ Excel file created: {excel_filename}")
            else:
                print(f"   ✗ Excel file not found: {excel_path}")
    except Exception as e:
        print(f"   Excel test failed: {e}")
    
    print("\n3. Testing Statistics...")
    stats = test_gen.get_statistics()
    print(f"   Statistics: {json.dumps(stats, indent=2)}")
    
    print("\n4. Testing Field Mapping...")
    for tc in mock_test_cases:
        print(f"   Feature: {tc.get('feature_name', 'MISSING')}")
        print(f"   ID: {tc.get('feature_id', 'MISSING')}")
        print(f"   Module: {tc.get('module', 'MISSING')}")
        print(f"   Test Steps: {type(tc.get('test_steps', []))} - {len(tc.get('test_steps', []))} items")
        print()
    
    print("=== Test Complete ===")
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
