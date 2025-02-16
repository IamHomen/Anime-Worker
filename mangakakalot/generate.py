import requests
from bs4 import BeautifulSoup
import json

LATEST_MANGA_URL = 'https://manganato.com/genre-all/'
BASE_URL = 'https://manganato.com/'
HOT_MANGA_URL = 'https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1'

'''def scrape_latest_update_manga():
    anime_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response = requests.get(LATEST_MANGA_URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.select('div.truyen-list > .list-truyen-item-wrap'):
            anime_list.append({
                'mangaId': el.select_one('a.list-story-item.bookmark_check')['href'],
                'mangaTitle': el.select_one('a.list-story-item.bookmark_check')['title'],
                'mangaImg': el.select_one('a.list-story-item.bookmark_check > img')['src'],
                'chapter': el.select_one('a.list-story-item-wrap-chapter').text.strip(),
                'mangaUrl': el.select_one('a.list-story-item.bookmark_check')['href'],
                'views': el.select_one('span.aye_icon').text.strip()
            })

        with open('./mangakakalot/latest-update.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to mangakakalot/latest-update.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}
'''

def scrape_latest_update_manga():
    anime_list = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        page_number = 1

        while page_number <= 100:
            print(f"Scraping page {page_number}...")
            url = f"{LATEST_MANGA_URL}{page_number}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            manga_items = soup.select('div.content-genres-item')  # Fix selector
            if not manga_items:
                break  # Stop if no more pages

            for el in manga_items:
                title = el.select_one('a.genres-item-img.bookmark_check')['title']
                img = el.select_one('a.genres-item-img.bookmark_check > img')['src']
                chapter = el.select_one('a.genres-item-chap').text.strip()
                chapter_url = el.select_one('a.genres-item-chap')['href'].split("/")[-1]
                manga_url = el.select_one('a.genres-item-img.bookmark_check')['href'].split("/")[-1]
                views = el.select_one('.genres-item-view').text.strip()

                anime_list.append({
                    'mangaTitle': title,
                    'mangaImg': img,
                    'chapter': chapter,
                    'chapterUrl': chapter_url,
                    'mangaUrl': manga_url,
                    'views': views
                })

            page_number += 1

        with open('./mangakakalot/latest-update.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to mangakakalot/latest-update.json')

        return anime_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}
    
def scrape_hot_manga():
    hot_manga_list = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response = requests.get(HOT_MANGA_URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.select('div.truyen-list > .list-truyen-item-wrap'):
            hot_manga_list.append({
                'mangaId': el.select_one('a.list-story-item.bookmark_check')['href'],
                'mangaTitle': el.select_one('a.list-story-item.bookmark_check')['title'],
                'mangaImg': el.select_one('a.list-story-item.bookmark_check > img')['src'],
                'chapter': el.select_one('a.list-story-item-wrap-chapter').text.strip(),
                'mangaUrl': el.select_one('a.list-story-item.bookmark_check')['href'],
                'views': el.select_one('span.aye_icon').text.strip()
            })

        with open('./mangakakalot/hot-manga.json', 'w') as f:
            json.dump(hot_manga_list, f, indent=2)
        print('Data saved to mangakakalot/hot-manga.json')

        return hot_manga_list
    except Exception as e:
        print(e)
        return {'error': str(e)}
    
scrape_latest_update_manga()
scrape_hot_manga()
