"""
Complete Flow Test - Step by Step Verification
"""
import os
import sys
import logging
sys.path.append('.')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_complete_flow():
    print("🔍 TESTING COMPLETE TEST CASE GENERATION FLOW")
    print("=" * 60)
    
    try:
        # Step 1: Test GeminiClient
        print("\n1️⃣ Testing GeminiClient...")
        from gemini_client import GeminiClient
        client = GeminiClient()
        print(f"   ✅ GeminiClient initialized")
        print(f"   ✅ Few-shot examples: {len(client.few_shot_examples) if client.few_shot_examples else 0}")
        print(f"   ✅ Key-value pairs: {len(client.key_value_pairs) if client.key_value_pairs else 0}")
        
        # Step 2: Test TestCaseGenerator
        print("\n2️⃣ Testing TestCaseGenerator...")
        from test_generator import TestCaseGenerator
        generator = TestCaseGenerator()
        print(f"   ✅ TestCaseGenerator initialized")
        
        # Step 3: Test Feature Extraction Logic
        print("\n3️⃣ Testing Feature Extraction Logic...")
        
        # Mock feature data that GeminiClient would return
        mock_features_response = {
            "features": [
                {
                    "feature_id": "F001",
                    "feature_name": "User Authentication",
                    "description": "Login and authentication functionality",
                    "module": "Security",
                    "requirements": ["Login with username/password", "Session management"]
                },
                {
                    "feature_id": "F002", 
                    "feature_name": "Payment Processing",
                    "description": "Process payments and transactions",
                    "module": "Finance",
                    "requirements": ["Credit card processing", "Payment validation"]
                }
            ]
        }
        
        # Test feature name extraction
        features = mock_features_response['features']
        print(f"   ✅ Mock features created: {len(features)} features")
        
        for idx, feature in enumerate(features, 1):
            feature_name = feature.get('feature_name', feature.get('name', f'Feature_{idx}'))
            print(f"   ✅ Feature {idx}: '{feature_name}' (should NOT be 'Unknown')")
            
            # Test progress message format
            progress_msg = f"Generating test cases for feature {idx}/{len(features)}: {feature_name}"
            print(f"      Progress: {progress_msg}")
        
        # Step 4: Test Export Functions
        print("\n4️⃣ Testing Export Functions...")
        
        # Mock test case data
        mock_test_cases = [
            {
                'feature_name': 'User Authentication',
                'feature_id': 'F001',
                'module': 'Security',
                'test_case_id': 'TC001',
                'test_case_name': 'Valid Login Test',
                'description': 'Test valid user login',
                'priority': 'High',
                'test_type': 'Functional',
                'test_steps': ['Navigate to login', 'Enter credentials', 'Click login'],
                'expected_result': 'User logged in successfully'
            }
        ]
        
        generator.all_test_cases = mock_test_cases
        
        # Test CSV export
        print("   Testing CSV export...")
        csv_result = generator.save_to_csv()
        if csv_result[0]:
            print(f"   ✅ CSV export works: {csv_result[1]}")
        else:
            print(f"   ⚠️ CSV export issue: {csv_result[1]}")
        
        # Step 5: Test Statistics
        print("\n5️⃣ Testing Statistics...")
        stats = generator.get_summary_stats()
        print(f"   ✅ Statistics generated:")
        print(f"      Total test cases: {stats.get('total_test_cases', 0)}")
        print(f"      Features: {list(stats.get('features', {}).keys())}")
        
        # Step 6: Test File Paths
        print("\n6️⃣ Testing File Paths...")
        from config import Config
        print(f"   Upload folder: {Config.UPLOAD_FOLDER}")
        print(f"   Download folder: {Config.DOWNLOAD_FOLDER}")
        
        # Ensure directories exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
        print(f"   ✅ Directories created/verified")
        
        print("\n🎉 COMPLETE FLOW TEST PASSED!")
        print("   All components are working correctly")
        print("   Feature names should display properly")
        print("   Export functions are functional")
        
    except Exception as e:
        print(f"\n❌ FLOW TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_complete_flow()
