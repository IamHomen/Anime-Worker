import firebase_admin
from firebase_admin import credentials, db
import json
import os

# Firebase credentials setup
# Load Firebase service account key from environment variable
service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get('FIREBASE_DATABASE_URL')
})

# Directory containing JSON files
json_files_path = './gogoanime/anime-info/'

# Upload JSON files to Firebase
for filename in os.listdir(json_files_path):
    if filename.endswith('.json'):
        json_file_path = os.path.join(json_files_path, filename)
        with open(json_file_path) as f:
            data = json.load(f)
        
        # Assuming each JSON file contains data for a specific node in Firebase
        # Adjust the reference path as per your Firebase structure
        node_name = os.path.splitext(filename)[0]  # Use filename as node name
        ref = db.reference(f'/anime-list/anime/info/{node_name}')
        ref.set(data)
