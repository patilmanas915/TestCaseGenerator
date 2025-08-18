#!/usr/bin/env python3
"""
Test the CSV download path fixes
"""
import os
import sys
from datetime import datetime

def test_csv_generation():
    """Test CSV generation and path handling"""
    try:
        from test_generator_no_pandas import TestCaseGenerator
        from config import Config
        
        print("🔍 Testing CSV generation and paths...")
        
        # Initialize generator
        generator = TestCaseGenerator()
        
        # Add some test data
        generator.all_test_cases = [
            {
                'test_case_id': 'TC001',
                'test_case_name': 'Test Download Path',
                'feature_name': 'Download Feature',
                'test_type': 'Functional',
                'priority': 'High'
            }
        ]
        
        # Test CSV generation
        csv_path, message = generator.save_to_csv()
        
        if csv_path and os.path.exists(csv_path):
            print(f"✅ CSV generated successfully at: {csv_path}")
            print(f"✅ Message: {message}")
            
            # Check file size
            file_size = os.path.getsize(csv_path)
            print(f"📊 File size: {file_size} bytes")
            
            # Check config paths
            print(f"📂 Config DOWNLOAD_FOLDER: {getattr(Config, 'DOWNLOAD_FOLDER', 'Not set')}")
            print(f"📂 Current working directory: {os.getcwd()}")
            print(f"📂 Absolute download path: {os.path.abspath(Config.DOWNLOAD_FOLDER)}")
            
            return True, csv_path
        else:
            print(f"❌ CSV generation failed: {message}")
            return False, None
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False, None

def test_download_path_search():
    """Test the download path search logic"""
    from config import Config
    
    possible_folders = [
        getattr(Config, 'DOWNLOAD_FOLDER', 'downloads'),
        '/tmp/downloads',
        'downloads',
        os.path.join(os.getcwd(), 'downloads')
    ]
    
    print("\n🔍 Testing download path search...")
    for folder in possible_folders:
        abs_folder = os.path.abspath(folder) if not os.path.isabs(folder) else folder
        exists = os.path.exists(abs_folder)
        print(f"   📁 {folder} -> {abs_folder} (exists: {exists})")
        
        if exists:
            try:
                files = [f for f in os.listdir(abs_folder) if f.endswith('.csv')]
                print(f"      📄 CSV files: {files}")
            except:
                print(f"      ❌ Cannot list files")

if __name__ == '__main__':
    print("🧪 TESTING CSV DOWNLOAD PATH FIXES")
    print("="*50)
    
    success, csv_path = test_csv_generation()
    test_download_path_search()
    
    print("="*50)
    if success:
        print("🎉 CSV generation working correctly!")
        print(f"📄 Test file created: {csv_path}")
        print("\n✅ Download should now work on Render!")
    else:
        print("❌ CSV generation test failed!")
        
    print("\n🔧 Next steps:")
    print("1. Deploy these fixes to Render")
    print("2. Test file upload and download")
    print("3. Check /files endpoint for debugging if needed")
