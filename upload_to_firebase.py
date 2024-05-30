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

# Load the JSON data from a file (Recent)
with open('./gogoanime/json/recent-release-sub.json', 'r') as f:
    data = json.load(f)

# Specify the reference where you want to upload the data
ref = db.reference('/anime-list/anime/latest-update')

# Upload the data
ref.set(data)

# Load the JSON data from a file (Popular)
with open('./gogoanime/json/popular.json', 'r') as f:
    data2 = json.load(f)

# Specify the reference where you want to upload the data
ref2 = db.reference('/anime-list/anime/anime-list')

# Upload the data
ref2.set(data2)

# Load the JSON data from a file (Popular Day)
with open('./gogoanime/json/top_1.json', 'r') as f:
    data3 = json.load(f)

# Specify the reference where you want to upload the data
ref3 = db.reference('/anime-list/anime/popular/day')

# Upload the data
ref3.set(data3)

# Load the JSON data from a file (Popular Week)
with open('./gogoanime/json/top_2.json', 'r') as f:
    data4 = json.load(f)

# Specify the reference where you want to upload the data
ref4 = db.reference('/anime-list/anime/popular/week')

# Upload the data
ref4.set(data4)

# Load the JSON data from a file (Popular Month)
with open('./gogoanime/json/top_3.json', 'r') as f:
    data5 = json.load(f)

# Specify the reference where you want to upload the data
ref5 = db.reference('/anime-list/anime/popular/month')

# Upload the data
ref5.set(data5)

# Load the JSON data from a file (New Season)
with open('./gogoanime/json/new-season.json', 'r') as f:
    data6 = json.load(f)

# Specify the reference where you want to upload the data
ref6 = db.reference('/anime-list/anime/new-season')

# Upload the data
ref6.set(data6)

# Load the JSON data from a file (Movie)
with open('./gogoanime/json/movie.json', 'r') as f:
    data7 = json.load(f)

# Specify the reference where you want to upload the data
ref7 = db.reference('/anime-list/anime/movie')

# Upload the data
ref7.set(data7)
