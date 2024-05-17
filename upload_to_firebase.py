import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Load Firebase service account key from environment variable
service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))

# Initialize the Firebase app
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mrcain-12665-default-rtdb.firebaseio.com'
})

# Load the JSON data from a file
with open('./gogoanime/recent-release-sub.json', 'r') as f:
    data = json.load(f)

# Specify the reference where you want to upload the data
ref = db.reference('/anime-list/anime/latest-update')

# Upload the data
ref.set(data)
