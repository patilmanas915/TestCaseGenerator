"""
Test the feature extraction and test case generation to debug formatting issues
"""
import json
import logging
from test_generator_no_pandas import TestGenerator
from gemini_client import GeminiClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_feature_extraction():
    """Test feature extraction functionality"""
    print("Testing feature extraction and test case generation...")
    
    # Create test generator
    test_gen = TestGenerator()
    
    # Test with sample FRD content
    sample_frd = """
    Feature: User Authentication
    Description: The system shall provide secure user authentication
    Requirements:
    - Users must be able to login with username and password
    - System shall validate credentials against database
    - Failed login attempts shall be logged
    
    Feature: Payment Processing
    Description: The system shall process online payments
    Requirements:
    - Support credit card payments
    - Integrate with payment gateway
    - Generate payment receipts
    """
    
    print("\n1. Testing feature extraction...")
    gemini_client = GeminiClient()
    features_data = gemini_client.extract_features_from_frd(sample_frd)
    
    if features_data:
        print(f"✓ Features extracted successfully: {json.dumps(features_data, indent=2)}")
        
        if 'features' in features_data:
            print(f"\n2. Found {len(features_data['features'])} features")
            
            # Test test case generation for first feature
            for i, feature in enumerate(features_data['features'][:1]):  # Test first feature only
                print(f"\n3. Testing test case generation for feature: {feature}")
                test_cases = gemini_client.generate_test_cases_for_feature(feature)
                
                if test_cases:
                    print(f"✓ Test cases generated: {json.dumps(test_cases, indent=2)}")
                    
                    # Test the field mapping
                    if 'test_cases' in test_cases:
                        for tc in test_cases['test_cases']:
                            print(f"\nProcessing test case: {tc}")
                            
                            # Apply the same logic as in test_generator_no_pandas.py
                            feature_name = feature.get('feature_name', feature.get('name', f'Feature_{i+1}'))
                            feature_id = feature.get('feature_id', feature.get('id', f'F{str(i+1).zfill(3)}'))
                            
                            tc['feature_name'] = feature_name
                            tc['feature_id'] = feature_id
                            tc['module'] = feature.get('module', tc.get('module', 'Unknown'))
                            
                            print(f"Final test case: {tc}")
                else:
                    print("✗ No test cases generated")
        else:
            print("✗ No 'features' key in response")
    else:
        print("✗ Feature extraction failed")

if __name__ == "__main__":
    test_feature_extraction()
