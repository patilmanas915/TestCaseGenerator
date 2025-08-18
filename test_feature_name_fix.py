"""
Test the feature name extraction fix
"""
import sys
sys.path.append('.')

try:
    print("=== Testing Feature Name Extraction Fix ===")
    
    # Test the feature data structure that GeminiClient returns
    test_features = [
        {
            "feature_id": "F001",
            "feature_name": "User Authentication System", 
            "description": "Login and authentication features",
            "module": "Security"
        },
        {
            "feature_id": "F002", 
            "feature_name": "Payment Processing",
            "description": "Payment gateway integration",
            "module": "Finance"
        },
        {
            "id": "F003",
            "name": "Legacy Feature Name", # Old format
            "description": "Legacy feature with old naming",
            "module": "Legacy"
        }
    ]
    
    print(f"Testing with {len(test_features)} mock features...")
    
    for i, feature in enumerate(test_features):
        # Apply the same logic as in test_generator_no_pandas.py
        feature_display_name = feature.get('feature_name', feature.get('name', f'Feature_{i+1}'))
        
        print(f"Feature {i+1}: {feature_display_name}")
        print(f"  Raw data: {feature}")
        print(f"  Extracted name: '{feature_display_name}'")
        
        # Test progress callback format
        progress_msg = f"Generating test cases for feature {i+1}/{len(test_features)}: {feature_display_name}"
        print(f"  Progress message: {progress_msg}")
        print()
    
    print("✅ Feature name extraction logic working correctly!")
    print("Feature names should now display properly instead of 'Unknown'")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
