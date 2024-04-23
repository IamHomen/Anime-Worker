import os
import json
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
RECENT_RELEASE_SUB_FILE_PATH = './gogoanime/recent-release-sub.json'
RECENT_TABLE_NAME = 'recent-release-sub'

# Load JSON data from a file
with open(RECENT_RELEASE_SUB_FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

# Update data in the table
response = supabase.table(RECENT_TABLE_NAME).update(data).filter('1', 'eq', '1').execute()

# Check for errors
if response['error'] is not None:
    print(f"Failed to update data: {response['error']}")
else:
    print("Data updated successfully")
