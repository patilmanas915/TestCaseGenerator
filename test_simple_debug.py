"""
Simple test for debugging feature extraction issues
"""
import os
import sys
sys.path.append('.')

try:
    from gemini_client import GeminiClient
    print("✓ GeminiClient imported successfully")
    
    # Test initialization
    client = GeminiClient()
    print("✓ GeminiClient initialized")
    
    # Check if few-shot examples are loaded
    print(f"Few-shot examples loaded: {len(client.few_shot_examples) if client.few_shot_examples else 0}")
    print(f"Key-value pairs loaded: {len(client.key_value_pairs) if client.key_value_pairs else 0}")
    
    # Test simple feature data structure
    test_feature = {
        "feature_id": "F001",
        "feature_name": "Test Feature",
        "name": "Test Feature Alt",
        "description": "Test description",
        "module": "Test Module"
    }
    
    print(f"\nTest feature data: {test_feature}")
    
    # Test field extraction logic
    feature_name = test_feature.get('feature_name', test_feature.get('name', 'Unknown'))
    feature_id = test_feature.get('feature_id', test_feature.get('id', 'F001'))
    module = test_feature.get('module', 'Unknown')
    
    print(f"Extracted feature_name: {feature_name}")
    print(f"Extracted feature_id: {feature_id}")
    print(f"Extracted module: {module}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
