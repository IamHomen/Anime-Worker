import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://anitaku.to'

RECENT_SUB_URL = 'https://ajax.gogocdn.net/ajax/page-recent-release.html?page=1&type=1'
LOAD_LIST_EPISODE = 'https://ajax.gogo-load.com/ajax/load-list-episode'

def scrape_recent_sub_anime():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        response = requests.get(RECENT_SUB_URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.select('div.last_episodes.loaddub > ul > li'):
            ids = el.select_one('p.name > a')['href'].split('/')[1].split('-episode-')[0]
            anime_list.append({
                'animeId': el.select_one('p.name > a')['href'].split('/')[1].split('-episode-')[0],
                'animeTitle': el.select_one('p.name > a')['title'],
                'animeImg': el.select_one('div > a > img')['src'],
                'episode': el.select_one('p.episode').text.strip(),
                'animeUrl': BASE_URL + el.select_one('p.name > a')['href']
            })
            scrape_anime_info(ids)

        with open('./gogoanime/recent-sub.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to gogoanime/recent-sub.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

def scrape_anime_info(ids):
    try:
        genres = []
        epList = []

        animePageTest = requests.get(f'https://gogoanime.gg/category/{ids}')
        animePageTest.raise_for_status()

        soup = BeautifulSoup(animePageTest.content, 'html.parser')

        animeTitle = soup.select_one('div.anime_info_body_bg > h1').text.strip()
        animeImage = soup.select_one('div.anime_info_body_bg > img')['src']
        type = soup.select_one('div.anime_info_body_bg > p:nth-child(4) > a').text.strip()
        desc = soup.select_one('div.anime_info_body_bg > p:nth-child(5)').text.replace('Plot Summary: ', '').strip()
        releasedDate = soup.select_one('div.anime_info_body_bg > p:nth-child(7)').text.replace('Released: ', '').strip()
        status = soup.select_one('div.anime_info_body_bg > p:nth-child(8) > a').text.strip()
        otherName = soup.select_one('div.anime_info_body_bg > p:nth-child(9)').text.replace('Other name: ', '').replace(';', ',').strip()

        for genre in soup.select('div.anime_info_body_bg > p:nth-child(6) > a'):
            genres.append(genre['title'].strip())

        ep_start = soup.select_one('#episode_page > li').find('a')['ep_start']
        ep_end = soup.select_one('#episode_page > li:last-child').find('a')['ep_end']
        movie_id = soup.select_one('#movie_id')['value']
        alias = soup.select_one('#alias_anime')['value']

        html = requests.get(f'{list_episodes_url}?ep_start={ep_start}&ep_end={ep_end}&id={movie_id}&default_ep=0&alias={alias}')
        html.raise_for_status()

        for el in episode_soup('#episode_related > li'):
            episodeLocale = el.select_one('div.cate').text.strip().lower()
            epList.append({
                'episodeId': el.find('a')['href'].split('/')[1],
                'episodeNum': el.select_one('div.name').text.replace('EP ', '').strip(),
                'episodeUrl': BASE_URL + el.find('a')['href'].strip(),
                'isSubbed': episodeLocale == "sub",
                'isDubbed': episodeLocale == "dub"
            })

        anime_data = {
            'animeTitle': str(animeTitle),
            'type': str(type),
            'releasedDate': str(releasedDate),
            'status': str(status),
            'genres': genres,
            'otherNames': otherName,
            'synopsis': str(desc),
            'animeImg': str(animeImage),
            'totalEpisodes': ep_end,
            'episodesList': epList,
        }

        with open(f'./gogoanime/anime-info/{ids}.json', 'w') as json_file:
            json.dump(anime_data, json_file, indent=2)

        return anime_data
    except Exception as err:
        print(err)
        return {'error': str(err)}

POPULAR_URL = 'https://anitaku.to/popular.html'

def scrape_popular_anime():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        popular_page = requests.get(POPULAR_URL, headers=headers)
        soup = BeautifulSoup(popular_page.content, 'html.parser')

        for el in soup.select('div.last_episodes > ul > li'):
            anime_list.append({
                'animeId': el.select_one('p.name > a')['href'].split('/')[2],
                'animeTitle': el.select_one('p.name > a')['title'],
                'animeImg': el.select_one('div > a > img')['src'],
                'releasedDate': el.select_one('p.released').text.replace('Released: ', '').strip(),
                'animeUrl': BASE_URL + el.select_one('p.name > a')['href']
            })

        with open('./gogoanime/popular.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to gogoanime/popular.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

popular_ongoing_url = 'https://ajax.gogocdn.net/ajax/page-recent-release-ongoing.html?page=1'

def scrape_trending_anime():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        pageNum = 1
        popular_page = requests.get(popular_ongoing_url, headers=headers)
        soup = BeautifulSoup(popular_page.content, 'html.parser')

        for el in soup.select('div.added_series_body.popular > ul > li'):
            genres = [a['title'] for a in el.select('p.genres > a')]
            anime_list.append({
                'animeId': el.select_one('a:nth-child(1)')['href'].split('/')[2],
                'animeTitle': el.select_one('a:nth-child(1)')['title'],
                'animeImg': el.select_one('a:nth-child(1) > div')['style'].split('(')[1].split(')')[0],
                'latestEp': el.select_one('p:nth-child(4) > a').text.strip(),
                'animeUrl': BASE_URL + el.select_one('a:nth-child(1)')['href'],
                'genres': genres
            })

        with open('./gogoanime/trending.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to gogoanime/trending.json')
        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

scrape_recent_sub_anime()
scrape_trending_anime()
scrape_popular_anime()
