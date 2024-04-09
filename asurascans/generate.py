import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://asuratoon.com/'
UPDATE_PATH = 'manga/?order=update'

def scrape_latest_update_manga():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
      
        response = requests.get({BASE_URL}{UPDATE_PATH}, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.select('div.listupd'):
            anime_list.append({
                'mangaId': el.select_one('div.bs > .bsx > a')['href'],
                'animeTitle': el.select_one('div.bs > .bsx > a')['title'],
                'animeImg': el.select_one('div.bs > .bsx > a > .limit > img')['src'],
                'episode': el.select_one('div.bs > .bsx > a > .bigor > .adds > .epxs').text.strip(),
                'animeUrl': BASE_URL + el.select_one('div.bs > .bsx > a')['href']
            })

        with open('./asurascans/latest-update.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to asurascans/latest-update.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

 scrape_latest_update_manga()
