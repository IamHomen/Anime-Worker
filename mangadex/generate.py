import requests
import json

# Define the API endpoint for getting the latest manga updates
API_URL_LATEST_UPDATE = 'https://api.mangadex.org/manga?includes[]=cover_art&order[latestUploadedChapter]=desc&hasAvailableChapters=true&limit=20'

def get_latest_manga_updates():
    manga_list = []
    try:
        # Make the request to the MangaDex API
        response = requests.get(API_URL_LATEST_UPDATE)
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()

        # Extract the manga data from the response
        for manga in result['data']:
            for relationship in manga['relationships']:
                if relationship['type'] == 'cover_art':
                    cover_art_attributes = relationship['attributes']
                    cover_art_file_name = cover_art_attributes['fileName']
                    break  # Exit the loop once the correct relationship is found

         mangaId = manga['id']
         coverUrl = f"https://mangadex.org/covers/{id}/{cover_art_file_name}"
            manga_list.append({
                'mangaId': mangaId,
                'title': manga['attributes']['title']['en'],
                'updatedAt': manga['attributes']['updatedAt'],
                'coverArt': coverUrl,
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
