import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://anitaku.to'

def scrape_popular_anime():
    list = []
    try:
        popular_page = requests.get(f'{BASE_URL}/popular.html')
        soup = BeautifulSoup(popular_page.content, 'html.parser')

        for el in soup.select('div.last_episodes > ul > li'):
            list.append({
                'animeId': el.select_one('p.name > a')['href'].split('/')[2],
                'animeTitle': el.select_one('p.name > a')['title'],
                'animeImg': el.select_one('div > a > img')['src'],
                'releasedDate': el.select_one('p.released').text.replace('Released: ', '').strip(),
                'animeUrl': BASE_URL + el.select_one('p.name > a')['href']
            })

        with open('./gogoanime/popular.json', 'w') as f:
            json.dump(list, f, indent=2)
        print('Data saved to gogoanime/popular.json')

        return list
    except Exception as e:
        print(e)
        return {'error': str(e)}

popular_ongoing_url = 'https://ajax.gogocdn.net/ajax/page-recent-release-ongoing.html'

def scrape_trending_anime():
    list = []
    try:
        pageNum = 1
        popular_page = requests.get(f'{popular_ongoing_url}?page={pageNum}')
        soup = BeautifulSoup(popular_page.content, 'html.parser')

        for el in soup.select('div.added_series_body.popular > ul > li'):
            genres = [a['title'] for a in el.select('p.genres > a')]
            list.append({
                'animeId': el.select_one('a:nth-child(1)')['href'].split('/')[2],
                'animeTitle': el.select_one('a:nth-child(1)')['title'],
                'animeImg': el.select_one('a:nth-child(1) > div')['style'].split('(')[1].split(')')[0],
                'latestEp': el.select_one('p:nth-child(4) > a').text.strip(),
                'animeUrl': BASE_URL + el.select_one('a:nth-child(1)')['href'],
                'genres': genres
            })

        with open('./gogoanime/trending.json', 'w') as f:
            json.dump(list, f, indent=2)
        print('Data saved to gogoanime/trending.json')
        return list
    except Exception as e:
        print(e)
        return {'error': str(e)}

scrape_trending_anime()
scrape_popular_anime()
