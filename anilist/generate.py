import requests
import json

# Define the GraphQL endpoint
GRAPHQL_URL = 'https://graphql.anilist.co'

favourites = '''
query {
  Page(page: 1, perPage: 50) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(type: ANIME, sort: FAVOURITES_DESC) {
      id
      seasonYear
      episodes
      format
      coverImage {
        extraLarge
      }
      title {
        english
        userPreferred
        romaji
      }
    }
  }
}
'''

def scrape_anilist_most_favourites():
    anime_list = []
    try:
        # Define the request headers
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        # Define the request body
        data = {'query': favourites}

        # Make the request to the AniList GraphQL API
        response = requests.post(GRAPHQL_URL, headers=headers, json=data)
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()

        # Extract the anime data from the response
        for anime in result['data']['Page']['media']:
            anime_list.append({
                'id': anime['id'],
                'title': anime['title']['userPreferred'],
                'cover': anime['coverImage']['extraLarge'],
                'seasonYear': anime['seasonYear'],
                'totalEpisode': anime['episodes'],
                'format': anime['format']
            })

        # Save the data to a JSON file
        with open('./anilist/most-favourites.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to anilist/most-favourites.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}


# Define your GraphQL query
popular = '''
query {
  Page(page: 1, perPage: 50) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(type: ANIME, sort: POPULARITY_DESC) {
      id
      seasonYear
      episodes
      format
      coverImage {
        extraLarge
      }
      title {
        english
        userPreferred
        romaji
      }
    }
  }
}
'''

def scrape_anilist_popular():
    anime_list = []
    try:
        # Define the request headers
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        # Define the request body
        data = {'query': popular}

        # Make the request to the AniList GraphQL API
        response = requests.post(GRAPHQL_URL, headers=headers, json=data)
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()

        # Extract the anime data from the response
        for anime in result['data']['Page']['media']:
            anime_list.append({
                'id': anime['id'],
                'title': anime['title']['userPreferred'],
                'cover': anime['coverImage']['extraLarge'],
                'seasonYear': anime['seasonYear'],
                'totalEpisode': anime['episodes'],
                'format': anime['format']
            })

        # Save the data to a JSON file
        with open('./anilist/popular.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to anilist/popular.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

# Define your GraphQL query
trending = '''
query {
  Page(page: 1, perPage: 50) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(type: ANIME, sort: TRENDING_DESC) {
      id
      seasonYear
      episodes
      format
      coverImage {
        extraLarge
      }
      title {
        english
        userPreferred
        romaji
      }
    }
  }
}
'''

def scrape_anilist_trending():
    anime_list = []
    try:
        # Define the request headers
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        # Define the request body
        data = {'query': trending}

        # Make the request to the AniList GraphQL API
        response = requests.post(GRAPHQL_URL, headers=headers, json=data)
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()

        # Extract the anime data from the response
        for anime in result['data']['Page']['media']:
            anime_list.append({
                'id': anime['id'],
                'title': anime['title']['userPreferred'],
                'cover': anime['coverImage']['extraLarge'],
                'seasonYear': anime['seasonYear'],
                'totalEpisode': anime['episodes'],
                'format': anime['format']
            })

        # Save the data to a JSON file
        with open('./anilist/trending.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to anilist/trending.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

movies = '''
query {
  Page(page: 1, perPage: 50) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(type: ANIME, sort: POPULARITY_DESC, format: MOVIE) {
      id
      seasonYear
      episodes
      format
      coverImage {
        extraLarge
      }
      title {
        english
        userPreferred
        romaji
      }
    }
  }
}
'''

def scrape_anilist_movies():
    anime_list = []
    try:
        # Define the request headers
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        
        # Define the request body
        data = {'query': movies}

        # Make the request to the AniList GraphQL API
        response = requests.post(GRAPHQL_URL, headers=headers, json=data)
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()

        # Extract the anime data from the response
        for anime in result['data']['Page']['media']:
            anime_list.append({
                'id': anime['id'],
                'title': anime['title']['userPreferred'],
                'cover': anime['coverImage']['extraLarge'],
                'seasonYear': anime['seasonYear'],
                'totalEpisode': anime['episodes'],
                'format': anime['format']
            })

        # Save the data to a JSON file
        with open('./anilist/movies.json', 'w') as f:
            json.dump(anime_list, f, indent=2)
        print('Data saved to anilist/movies.json')

        return anime_list
    except Exception as e:
        print(e)
        return {'error': str(e)}

# Call the function to scrape AniList data
scrape_anilist_most_favourites()
scrape_anilist_trending()
scrape_anilist_popular()
scrape_anilist_movies()
