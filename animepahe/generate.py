import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://animepahe.ru/api?m=airing&page=1'

def scrape_recent_sub_anime():
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
        }
        anime_list = requests.get(BASE_URL, headers=headers).json()

        with open('./animepahe/recent-sub.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to animepahe/recent-sub.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

scrape_recent_sub_anime()
