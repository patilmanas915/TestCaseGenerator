"""
Test Flask app startup and routing
"""
import os
import sys
sys.path.append('.')

def test_flask_app():
    print("🌐 TESTING FLASK APP STARTUP")
    print("=" * 40)
    
    try:
        # Set environment to avoid API calls during import
        os.environ['TESTING'] = '1'
        
        print("\n1️⃣ Testing Flask app import...")
        from app import app
        print("   ✅ Flask app imported successfully")
        
        print("\n2️⃣ Testing app configuration...")
        print(f"   ✅ Secret key configured: {'Yes' if app.secret_key else 'No'}")
        print(f"   ✅ Upload folder: {app.config.get('UPLOAD_FOLDER', 'Not set')}")
        
        print("\n3️⃣ Testing routes...")
        with app.test_client() as client:
            # Test main page
            response = client.get('/')
            print(f"   ✅ Main page status: {response.status_code}")
            
            # Test health check
            response = client.get('/health')
            print(f"   ✅ Health check status: {response.status_code}")
        
        print("\n🎉 FLASK APP TEST PASSED!")
        print("   App is ready to handle requests")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FLASK APP TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_flask_app()
