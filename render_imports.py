"""
Render-optimized app configuration that handles pandas gracefully
"""
import os

# Update import to use render-compatible test generator
def get_test_generator():
    """Get test generator based on environment"""
    try:
        # Try pandas version first
        from test_generator import TestCaseGenerator
        return TestCaseGenerator
    except ImportError:
        # Fallback to render-compatible version
        from test_generator_render import TestCaseGenerator
        return TestCaseGenerator

# Update the app.py import
if os.environ.get('RENDER') or os.environ.get('USE_MINIMAL_DEPS'):
    from test_generator_render import TestCaseGenerator
else:
    from test_generator import TestCaseGenerator
