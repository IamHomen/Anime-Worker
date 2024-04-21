import csv
import requests
import os

# Load environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
CSV_FILE_PATH = '/.gogoamime/csv/recent-release-sub.csv'
TABLE_NAME = 'recent-release-sub'

# Read CSV file
with open(CSV_FILE_PATH, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

# Post data to Supabase
for row in data:
    response = requests.post(
        f'{SUPABASE_URL}/rest/v1/{TABLE_NAME}',
        headers={
            'Content-Type': 'application/json',
            'apikey': SUPABASE_KEY
        },
        json=row
    )
    if response.status_code != 201:
        print(f'Failed to insert row: {row}')
        print(response.text)
    else:
        print(f'Successfully inserted row: {row}')
      
