
import json
import os
import sys
import subprocess
from typing import List, Optional

# --- Tool Definitions ---

def list_kaggle_kernels(user: str, limit: int = 5):
    """
    Lists the most recent Kaggle kernels for a specific user to check training status.
    Useful for monitoring progress without checking the web UI.
    """
    try:
        # Sort by dateRun to see the active/latest ones first
        cmd = ["kaggle", "kernels", "list", "--user", user, "--sort-by", "dateRun", "--page-size", str(limit)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error listing kernels: {e.stderr}"
    except FileNotFoundError:
        return "Error: 'kaggle' CLI not found. Please install it with 'pip install kaggle'."

def upload_kaggle_dataset(file_path: str, title: str, slug: str):
    """
    Uploads a new dataset to Kaggle.
    
    Args:
        file_path: Absolute path to the file to upload (e.g., .jsonl)
        title: Human-readable title for the dataset
        slug: URL-friendly slug (e.g. 'my-dataset-v1')
    """
    # 1. Prepare Staging Directory
    staging_dir = "kaggle_staging_upload"
    os.makedirs(staging_dir, exist_ok=True)
    
    # 2. Copy File
    filename = os.path.basename(file_path)
    dest_path = os.path.join(staging_dir, filename)
    subprocess.run(["cp", file_path, dest_path], check=True)
    
    # 3. Create Metadata
    metadata = {
        "title": title,
        "id": f"{os.environ.get('KAGGLE_USERNAME', 'unknown')}/{slug}",
        "licenses": [{"name": "CC0-1.0"}]
    }
    with open(os.path.join(staging_dir, "dataset-metadata.json"), "w") as f:
        json.dump(metadata, f)
        
    # 4. Upload
    try:
        cmd = ["kaggle", "datasets", "create", "-p", staging_dir]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"Success: {result.stdout}"
    except subprocess.CalledProcessError as e:
        if "401" in e.stderr:
            return f"Error 401: Unauthorized. Check Phone Verification in Kaggle Settings. Details: {e.stderr}"
        return f"Error uploading dataset: {e.stderr}"

# --- Minimal MCP Server Wrapper (Stdio) ---

def handle_call(request):
    try:
        method = request.get("method")
        params = request.get("params", {}).get("arguments", {})
        
        if method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "list_kaggle_kernels",
                        "description": "List recent kernels to monitor training status",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "user": {"type": "string", "description": "Kaggle username"},
                                "limit": {"type": "integer", "default": 5}
                            },
                            "required": ["user"]
                        }
                    },
                    {
                        "name": "upload_dataset",
                        "description": "Upload a file as a new private Dataset on Kaggle",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_path": {"type": "string"},
                                "title": {"type": "string"},
                                "slug": {"type": "string"}
                            },
                            "required": ["file_path", "title", "slug"]
                        }
                    }
                ]
            }
        
        elif method == "tools/call":
            name = request.get("params", {}).get("name")
            args = request.get("params", {}).get("arguments", {})
            
            if name == "list_kaggle_kernels":
                result = list_kaggle_kernels(args.get("user"), args.get("limit", 5))
                return {"content": [{"type": "text", "text": str(result)}]}
                
            elif name == "upload_dataset":
                result = upload_kaggle_dataset(args.get("file_path"), args.get("title"), args.get("slug"))
                return {"content": [{"type": "text", "text": str(result)}]}
                
            else:
                raise ValueError(f"Unknown tool: {name}")
                
        else:
            return None

    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error: {str(e)}"}], "isError": True}

# --- Main Loop ---
if __name__ == "__main__":
    # If run directly, can be used as a CLI tester or piped to an MCP client
    # For now, just a dummy main to show it's a script.
    # To use as MCP: Connect via stdio adapter config
    pass
