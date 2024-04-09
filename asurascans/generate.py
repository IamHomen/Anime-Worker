import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://asuratoon.com/manga/?order=update'
POPULAR_URL = 'https://asuratoon.com/manga/?status=ongoing&order=popular'
NEWEST_MANGA_URL = 'https://asuratoon.com/manga/?status=ongoing&type=&order=latest'

def scrape_latest_update_manga():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
      
        response = requests.get(BASE_URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.select('div.listupd > .bs'):
            anime_list.append({
                'mangaId': el.select_one('div.bsx > a')['href'],
                'animeTitle': el.select_one('div.bsx > a')['title'],
                'animeImg': el.select_one('div.bsx > a > .limit > img')['src'],
                'episode': el.select_one('div.bsx > a > .bigor > .adds > .epxs').text.strip(),
                'animeUrl': el.select_one('div.bsx > a')['href']
            })

        with open('./asurascans/latest-update.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to asurascans/latest-update.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

def scrape_popular_manga():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
      
        response = requests.get(POPULAR_URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.select('div.listupd > .bs'):
            anime_list.append({
                'mangaId': el.select_one('div.bsx > a')['href'],
                'animeTitle': el.select_one('div.bsx > a')['title'],
                'animeImg': el.select_one('div.bsx > a > .limit > img')['src'],
                'episode': el.select_one('div.bsx > a > .bigor > .adds > .epxs').text.strip(),
                'animeUrl': el.select_one('div.bsx > a')['href']
            })

        with open('./asurascans/popular.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to asurascans/popular.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

def scrape_newest_manga():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
      
        response = requests.get(NEWEST_MANGA_URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.select('div.listupd > .bs'):
            anime_list.append({
                'mangaId': el.select_one('div.bsx > a')['href'],
                'animeTitle': el.select_one('div.bsx > a')['title'],
                'animeImg': el.select_one('div.bsx > a > .limit > img')['src'],
                'episode': el.select_one('div.bsx > a > .bigor > .adds > .epxs').text.strip(),
                'animeUrl': el.select_one('div.bsx > a')['href']
            })

        with open('./asurascans/newest-manga.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to asurascans/newest.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

scrape_latest_update_manga()
scrape_popular_manga()
scrape_newest_manga()
