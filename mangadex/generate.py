import requests
import json

# Define the API endpoint for getting the latest manga updates
API_URL = 'https://api.mangadex.org/manga'

def get_latest_manga_updates():
    manga_list = []
    try:
        # Define the request headers with your API key
        #headers = {'Authorization': f'Bearer {API_KEY}'}

        params = {
            'order[latestUploadedChapter]': 'desc',
            'limit': 100  # Limit the number of results to 10
        }
      
        # Make the request to the MangaDex API
        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()

        # Extract the manga data from the response
        for manga in result['data']:
            cover_art = manga['relationships']['cover_art']['data']['id'] if 'cover_art' in manga['relationships'] else None
            manga_list.append({
                'mangaId': manga['id'],
                'title': manga['attributes']['title']['en'],
                'updatedAt': manga['attributes']['updatedAt'],
                'coverArt': cover_art,
                'availableChapters': manga['attributes']['chapterCount'] if 'chapterCount' in manga['attributes'] else None,
                'altTitles': manga['attributes']['altTitles'],
                'description': manga['attributes']['description'],
                'status': manga['attributes']['status'],
                'releaseDate': manga['attributes']['year'],
                'contentRating': manga['attributes']['contentRating'],
                'lastVolume': manga['attributes']['lastVolume'],
                'lastChapter': manga['attributes']['lastChapter']
            })

        # Save the data to a JSON file
        with open('./mangadex/latest_manga_updates.json', 'w') as f:
            json.dump(manga_list, f, indent=2)
        print('Data saved to mangadex/latest_manga_updates.json')

        return manga_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

# Call the function to get the latest manga updates
get_latest_manga_updates()
      
