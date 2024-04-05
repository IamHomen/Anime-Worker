<b>UPDATE DATA EVERY 15 MINUTES</b>

<strong>SUPPORTED SITES</strong>

[GogoAnime](https://https://anitaku.to/home.html)

[AnimePahe](https://animepahe.ru/)

[Anilist](https://anilist.co/)

[MangaDex](https://mangadex.org/)

<strong>ℹ️ Still in Development</strong>
<center></red>WILL SUPPORT MORE IN THE FUTURE</center>

## Documentation

### Get Popular Anime

| parameters   | description       |
| ------------ | ------------------- |
| `gogoanime` `animepahe` `anilist` `mangadex` | select from below and replace the url |

### ROUTES  |   END POINT
 # gogoanime |  
 
 `recent-sub.json`, 
 
 `popular.json`, 

 `trending.json`

 # animepahe |  
 `recent-sub.json`

 # anilist   |  
 
 `popular.json`, 
 
 `trending.json`

 # mangadex  | 

 `latest_manga_updates.json`
 

```js
fetch("https://raw.githubusercontent.com/mrcainv1-3128/Homen-Anime-Worker/main/anilist/trending.json")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```
