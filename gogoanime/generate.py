import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import psycopg2
from dotenv import load_dotenv

BASE_URL = 'https://anitaku.so'
RECENT_SUB_URL = 'https://ajax.gogocdn.net/ajax/page-recent-release.html'
LOAD_LIST_EPISODE = 'https://ajax.gogocdn.net/ajax/load-list-episode'
load_dotenv()

def scrape_recent_sub_anime():
    anime_list = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        page_number = 1
        while page_number <= 10:  # Stop when page_number reaches 10
            response = requests.get(RECENT_SUB_URL + f"?page={page_number}&type=1", headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Check if the page contains anime entries
            if not soup.select('div.last_episodes.loaddub > ul > li'):
                break  # No more pages to scrape

            for el in soup.select('div.last_episodes.loaddub > ul > li'):
                ids = el.select_one('p.name > a')['href'].split('/')[1].split('-episode-')[0]
                anime_list.append({
                    'id': el.select_one('p.name > a')['href'].split('/')[1].split('-episode-')[0],
                    'epId': el.select_one('p.name > a')['href'].split('/')[1],
                    'title': el.select_one('p.name > a')['title'],
                    'img': el.select_one('div > a > img')['src'],
                    'episode': el.select_one('p.episode').text.strip()
                    #'animeUrl': BASE_URL + el.select_one('p.name > a')['href']
                })
               # scrape_anime_info(ids)

            page_number += 1
            
        #updateTable('recent-release-sub')

        with open('./gogoanime/recent-release-sub.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to gogoanime/recent-release-sub.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}      

POPULAR_URL = 'https://anitaku.to/popular.html'

def scrape_popular_anime():
    anime_list = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
        page_number = 1
        while page_number <= 10:  # Stop scraping at page 10
            popular_page = requests.get(POPULAR_URL + f"?page={page_number}", headers=headers)
            soup = BeautifulSoup(popular_page.content, 'html.parser')

            # Check if the page contains anime entries
            if not soup.select('div.last_episodes > ul > li'):
                break  # No more pages to scrape

            for el in soup.select('div.last_episodes > ul > li'):
                ids = el.select_one('p.name > a')['href'].split('/')[2]
                anime_list.append({
                    'animeId': el.select_one('p.name > a')['href'].split('/')[2],
                    'animeTitle': el.select_one('p.name > a')['title'],
                    'animeImg': el.select_one('div > a > img')['src'],
                    'releasedDate': el.select_one('p.released').text.replace('Released: ', '').strip()
                })
                #scrape_anime_info(ids)

            page_number += 1

        #updateTable('popular')
        
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
            ids = el.select_one('a:nth-child(1)')['href'].split('/')[2]
            genres = [a['title'] for a in el.select('p.genres > a')]
            anime_list.append({
                'animeId': el.select_one('a:nth-child(1)')['href'].split('/')[2],
                'animeTitle': el.select_one('a:nth-child(1)')['title'],
                'animeImg': el.select_one('a:nth-child(1) > div')['style'].split('(')[1].split(')')[0],
                'latestEp': el.select_one('p:nth-child(4) > a').text.strip(),
                'animeUrl': BASE_URL + el.select_one('a:nth-child(1)')['href'],
                'genres': genres
            })
            #scrape_anime_info(ids)

        with open('./gogoanime/trending.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to gogoanime/trending.json')
        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

def scrape_anime_info(ids):
    try:
        genres = []
        epList = []

        animePageTest = requests.get(f'https://anitaku.so/category/{ids}')
        animePageTest.raise_for_status()

        soup = BeautifulSoup(animePageTest.content, 'html.parser')

        animeTitle = soup.select_one('div.anime_info_body_bg > h1').text.strip()
        animeImage = soup.select_one('div.anime_info_body_bg > img')['src']
        type = soup.select_one('div.anime_info_body_bg > p.type:-soup-contains("Type: ")').text.replace('Type: ', '').strip()
        desc = soup.select_one('div.anime_info_body_bg > div.description').text.replace('Plot Summary: ', '').strip()
        releasedDate = soup.select_one('div.anime_info_body_bg > p.type:-soup-contains("Released: ")').text.replace('Released: ', '').strip()
        status = soup.select_one('div.anime_info_body_bg > p.type:-soup-contains("Status: ") > a').text.strip()
        otherName = soup.select_one('div.anime_info_body_bg > p.type.other-name > a').text.strip()

        for genre in soup.select('div.anime_info_body_bg > p:nth-child(7) > a'):
            genres.append(genre['title'].strip())

        ep_start = soup.select_one('#episode_page > li').find('a')['ep_start']
        ep_end = soup.select_one('#episode_page > li').find('a')['ep_end']
        movie_id = soup.select_one('#movie_id')['value']
        alias = soup.select_one('#alias_anime')['value']

        html = requests.get(f"{LOAD_LIST_EPISODE}?ep_start={ep_start}&ep_end={ep_end}&id={movie_id}&default_ep=0&alias={alias}")
        html.raise_for_status()

        episode_soup = BeautifulSoup(html.content, 'html.parser')

        for el in episode_soup('#episode_related > li'):
            epList.append({
                'episodeId': el.select_one('a')['href'].split('/')[1],
                'episodeNum': el.select_one('a > .name').text.replace('EP ', 'Episode ').strip(),
                'episodeUrl': BASE_URL + el.select_one('a')['href'].strip()
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

#def updateTable(val):

    # Load JSON data from a file
   # with open(f"./gogoanime/{val}.json", 'r') as json_file:
        #data = json.load(json_file)

    # Specify the CSV file path
  #  csv_file_path = f"./gogoanime/csv/{val}.csv"

    # Extract the keys from the first element to use as headers
  #  keys = data[0].keys()

    # Write the data to a CSV file
#  with open(csv_file_path, 'w', newline='') as csv_file:
        #writer = csv.DictWriter(csv_file, fieldnames=keys)
       # writer.writeheader()
       # writer.writerows(data)

   # print('JSON data converted to CSV successfully.')

scrape_recent_sub_anime()
scrape_trending_anime()
scrape_popular_anime()
scrape_anime_info('tsuki-ga-michibiku-isekai-douchuu-2nd-season')
