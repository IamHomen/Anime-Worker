import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://anitaku.to'

RECENT_SUB_URL = 'https://ajax.gogocdn.net/ajax/page-recent-release.html?page=1&type=1'

def scrape_recent_sub_anime():
    list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        recent_page = requests.get(RECENT_SUB_URL, headers=headers)
        soup = BeautifulSoup(recent_page.content, 'html.parser')

        for el in soup.select('div.last_episodes.loaddub > ul > li'):
            list.append({
                'animeId': el.select_one('p.name > a')['href'].split('/')[2],
                'animeTitle': el.select_one('p.name > a')['title'],
                'animeImg': el.select_one('div > a > img')['src'],
                'episode': el.select_one('p.episode').text(),
                'animeUrl': BASE_URL + el.select_one('p.name > a')['href']
            })

        with open('./gogoanime/recent-sub.json', 'w') as f:
            json.dump(list, f, indent=2)
        print('Data saved to gogoanime/recent-sub.json')

        return list
    except Exception as e:
        print(e)
        return {'error': str(e)}

POPULAR_URL = 'https://anitaku.to/popular.html'

def scrape_popular_anime():
    list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        popular_page = requests.get(POPULAR_URL, headers=headers)
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

popular_ongoing_url = 'https://ajax.gogocdn.net/ajax/page-recent-release-ongoing.html?page=1'

def scrape_trending_anime():
    list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        pageNum = 1
        popular_page = requests.get(popular_ongoing_url, headers=headers)
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

scrape_recent_sub_anime()
scrape_trending_anime()
scrape_popular_anime()
