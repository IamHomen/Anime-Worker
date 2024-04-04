<b>UPDATE DATA EVERY HOUR</b>

<strong>SUPPORTED SITES</strong>

[GogoAnime](https://https://anitaku.to/home.html)




[AnimePahe](https://animepahe.ru/)

[Anilist](https://anilist.co/)

<strong>Still in Development</strong>

## Documentation

### Get Popular Anime

| parameters   | description       |
| ------------ | ------------------- |
| `route` | select from below and replace the url |

### ROUTES  |   END POINT
 gogoanime |  `recent-sub.json`, `popular.json`, `trending.json`

 animepahe |  `recent-sub.json`

 anilist   |  `popular.json`, `trending.json`

```js
fetch("https://raw.githubusercontent.com/mrcainv1-3128/Homen-Anime-Worker/main/anilist/trending.json")
  .then((response) => response.json())
  .then((animelist) => console.log(animelist));
```
