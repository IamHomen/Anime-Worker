import requests
from bs4 import BeautifulSoup
import json

LATEST_MANGA_URL = 'https://m.manganelo.com/genre-all/'
BASE_URL = 'https://m.manganelo.com/'
MANGA_BASE_URL = 'https://chapmanganelo.com/'
HOT_MANGA_URL = 'https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1'
NEWEST_MANGA_URL = 'https://m.manganelo.com/genre-all/'

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

        while page_number <= 1968:
            print(f"Scraping page {page_number}...")
            url = f"{LATEST_MANGA_URL}{page_number}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            manga_items = soup.select('div.content-genres-item')
            if not manga_items:
                break  # Stop if no more pages

            for el in manga_items:
                title = el.select_one('a.genres-item-img.bookmark_check')['title']
                img = el.select_one('a.genres-item-img.bookmark_check > img')['src']
                
                chapter_element = el.select_one('a.genres-item-chap')
                chapter = chapter_element.text.strip() if chapter_element else "No chapter"
                chapter_url = chapter_element.get('href', 'No URL').split("/")[-1] if chapter_element else "No URL"

                manga_element = el.select_one('a.genres-item-img.bookmark_check')
                manga_url = manga_element.get('href', 'No URL').split("/")[-1] if manga_element else "No URL"

                description_element = el.select_one('.genres-item-description')
                description = description_element.text.strip() if description_element else "Unknown"

                views_element = el.select_one('.genres-item-view')
                views = views_element.text.strip() if views_element else "Unknown"
                
                time_element = el.select_one('.genres-item-time')
                time = time_element.text.strip() if time_element else "Unknown"

                scrape_manga_details(manga_url)

                anime_list.append({
                    'mangaTitle': title,
                    'mangaImg': img,
                    'chapter': chapter,
                    'chapterUrl': chapter_url,
                    'mangaUrl': manga_url,
                    'description': description,
                    'views': views,
                    'time': time
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

def scrape_most_viewed_manga():
    anime_list = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }
        url = "https://manganato.com/"  # Change to the correct URL if needed
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Select the most-viewed manga section inside `.owl-wrapper`
        wrapper = soup.select_one('div.owl-wrapper')
        if not wrapper:
            print("No owl-wrapper found!")
            return {'error': 'No owl-wrapper found'}

        manga_items = wrapper.select('div.owl-item > div.item')  # Selecting items inside `.owl-wrapper`
        if not manga_items:
            print("No most-viewed manga found!")
            return {'error': 'No most-viewed manga found'}

        for el in manga_items:
            title_element = el.select_one('.slide-caption h3 a')
            title = title_element.text.strip() if title_element else "No title"
            manga_url = title_element['href'] if title_element else "No URL"

            img_element = el.select_one('img.img-loading')
            img = img_element['src'] if img_element else "No image"

            chapter_element = el.select_one('.slide-caption > a')
            chapter = chapter_element.text.strip() if chapter_element else "No chapter"
            chapter_url = chapter_element['href'] if chapter_element else "No URL"

            anime_list.append({
                'mangaTitle': title,
                'mangaImg': img,
                'chapter': chapter,
                'chapterUrl': chapter_url,
                'mangaUrl': manga_url
            })

        with open('./mangakakalot/most-viewed.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to mangakakalot/most-viewed.json')

        return anime_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}

def scrape_newest_manga():
    anime_list = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        page_number = 1

        while page_number <= 1968:
            print(f"Scraping page {page_number}...")
            url = f"{NEWEST_MANGA_URL}{page_number}?type=newest"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            manga_items = soup.select('div.content-genres-item')
            if not manga_items:
                break  # Stop if no more pages

            for el in manga_items:
                title = el.select_one('a.genres-item-img.bookmark_check')['title']
                img = el.select_one('a.genres-item-img.bookmark_check > img')['src']
                
                chapter_element = el.select_one('a.genres-item-chap')
                chapter = chapter_element.text.strip() if chapter_element else "chapter-404.php"
                chapter_url = chapter_element.get('href', 'chapter-404.php').split("/")[-1] if chapter_element else "chapter-404.php"

                manga_element = el.select_one('a.genres-item-img.bookmark_check')
                manga_url = manga_element.get('href', 'manga-404.php').split("/")[-1] if manga_element else "manga-404.php"

                description_element = el.select_one('.genres-item-description')
                description = description_element.text.strip() if description_element else "N/A"

                views_element = el.select_one('.genres-item-view')
                views = views_element.text.strip() if views_element else "0"
                
                time_element = el.select_one('.genres-item-time')
                time = time_element.text.strip() if time_element else "Unknown"

                anime_list.append({
                    'mangaTitle': title,
                    'mangaImg': img,
                    'chapter': chapter,
                    'chapterUrl': chapter_url,
                    'mangaUrl': manga_url,
                    'description': description,
                    'views': views,
                    'time': time
                })

            page_number += 1

        with open('./mangakakalot/newest-manga.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to mangakakalot/newest.json')

        return anime_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}

def scrape_manga_details(manga_url):
    manga_details = {}
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        url = f"{MANGA_BASE_URL}{manga_url}"  # Replace with the correct manga URL
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the chapter list
        chapter_list = soup.select('ul#row-content-chapter li')

        # Extracting manga details
        manga_info = soup.select_one('.container-main-left')

        # Title
        title = manga_info.select_one('div.story-info-right h1').text.strip()

        # Image
        img = manga_info.select_one('div.story-info-left .info-image img')['src']

        # Alternative Title
        alternative_title = manga_info.select_one('div.story-info-right .variations-tableInfo .table-value h2').text.strip()

        # Authors
        second_tr = soup.select_one('div.div.story-info-right .variations-tableInfo tbody tr:nth-of-type(2)')
        authors = []
        if second_tr:
           authors = [a.text for a in second_tr.select('.table-value a')]
   
        # Status
        status = manga_info.select_one('div.story-info-right .variations-tableInfo .table-value').text.strip()

        # Genres
        genres = [genre.text for genre in manga_info.select('div.story-info-right .variations-tableInfo .table-value a')]

        # Updated time
        updated_time = manga_info.select_one('div.story-info-right .story-info-right-extent .stre-value').text.strip()

        # Description
        description = manga_info.select_one('div.panel-story-info .panel-story-info-description').text.strip()

        chapters = []
        for chapter in chapter_list:
            # Extract chapter details
            chapter_name = chapter.select_one('a.chapter-name').text.strip()
            chapter_url = chapter.select_one('a.chapter-name')['href']
            views = chapter.select_one('span.chapter-view').text.strip()
            uploaded_time = chapter.select_one('span.chapter-time').text.strip()

            chapters.append({
                'chapter_name': chapter_name,
                'chapter_url': chapter_url,
                'views': views,
                'uploaded_time': uploaded_time
            })

        # Storing data in dictionary
        manga_details = {
            'title': title,
            'img': img,
            'alternative_title': alternative_title,
            'authors': authors,
            'status': status,
            'genres': genres,
            'updated_time': updated_time,
            'description': description,
            'chapters': chapters
        }

        # Saving the data to a JSON file
        with open(f"./mangakakalot/info/{manga_url}.json", 'w') as f:
            json.dump(manga_details, f, indent=2)

        print(f"Manga details saved to {manga_url}.json")

    except Exception as e:
        print(f"An error occurred: {e}")

    return manga_details
    
scrape_latest_update_manga()
scrape_hot_manga()
scrape_most_viewed_manga()
scrape_newest_manga()

