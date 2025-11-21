#!/usr/bin/env python
# Test import
try:
    from main import app
    print("✅ App imported successfully")
    print(f"✅ App title: {app.title}")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    import traceback
    traceback.print_exc()
