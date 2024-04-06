<p align="center">
  <a href="https://github.com/mrcainv1-3128/Homen-Anime-Worker">
    <img src="img/gogo.png" alt="Logo" width="85" height="85">
  </a>
<a href="https://github.com/mrcainv1-3128/Homen-Anime-Worker">
    <img src="img/anilist.png" alt="Logo" width="85" height="85">
  </a>

  <a href="https://github.com/mrcainv1-3128/Homen-Anime-Worker">
    <img src="img/mangadex.svg" alt="Logo" width="85" height="85">
  </a>

  <a href="https://github.com/mrcainv1-3128/Homen-Anime-Worker">
    <img src="img/animepahe.svg" alt="Logo" width="85" height="85">
  </a>

  <h3 align="center">Homen Anime Worker</h3>

<b>UPDATE DATA EVERY 15 MINUTES</b>

<strong>SUPPORTED SITES</strong>

[GogoAnime](https://https://anitaku.to/home.html)

[AnimePahe](https://animepahe.ru/)

[Anilist](https://anilist.co/)

[MangaDex](https://mangadex.org/)

<strong>ℹ️ Still in Development</strong>

<center>WILL SUPPORT MORE IN THE FUTURE</center>

## Documentation

### Get Popular Anime

| parameters   | description       |
| ------------ | ------------------- |
| `gogoanime` `animepahe` `anilist` `mangadex` | select filename from below and replace the url |

### ROUTES  |   END POINT
 # gogoanime |  
 
 `recent-sub.json`, 
 
 `popular.json`, 

 `trending.json`

 # animepahe |  
 `recent-sub.json`

 # anilist   |  
 
 `popular.json`, 
 
 `trending.json`,
 
 `most-favourites.json`

 # mangadex  | 

 `latest_manga_updates.json`
 

```js
fetch("https://raw.githubusercontent.com/mrcainv1-3128/Homen-Anime-Worker/main/anilist/trending.json")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```



<center>MADE PURELY ON PYTHON</center>
