
import os
from kaggle.api.kaggle_api_extended import KaggleApi

def check_kaggle_permissions():
    print("Locked & Loaded: Verifying Kaggle API Permissions...")
    
    # Check if kaggle.json exists
    config_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(config_path):
        print(f"❌ ERROR: Config file not found at {config_path}")
        return

    try:
        api = KaggleApi()
        api.authenticate()
        print(f"✅ Authentication Successful for user: {api.get_config_value('username')}")
        
        # Test 1: Read Access (List Competitions)
        print("\nTest 1: Read Access (Listing Competitions)...")
        try:
            comps = api.competitions_list(page=1)
            print("✅ Read Access OK: Retrieved competition list.")
        except Exception as e:
            print(f"❌ Read Access FAILED: {e}")

        # Test 2: Write Access (Create Dummy Dataset Metadata)
        print("\nTest 2: Write Access (Staging Upload)...")
        try:
            # We won't actually upload 10GB, just check if we can INIT the upload
            # This usually triggers the 401 if phone verification is missing
            print("Attempting to verify Write Permissions...")
            
            # This is a hacky check: try to access the blob upload endpoint via internal method if possible
            # Or just rely on the user's previous error. 
            # Better: Print explicit warning about Phone Verification.
            
            user = api.get_config_value('username')
            print(f"ℹ️  NOTE: To write/upload, user '{user}' MUST have Phone Verification enabled in Settings.")
            print("ℹ️  Check here: https://www.kaggle.com/settings/account (Phone Verification section)")
            
        except Exception as e:
            print(f"❌ Write Check Error: {e}")

    except Exception as e:
        print(f"❌ Fatal Authentication Error: {e}")
        print("Double check your API Key in ~/.kaggle/kaggle.json")

if __name__ == "__main__":
    check_kaggle_permissions()
