import axios from 'axios';
import cheerio from 'cheerio';
import fs from 'fs';

const BASE_URL = 'https://anitaku.to';

const scrapePopularAnime = async () => {
  let list = [];
  try {
    const popularPage = await axios.get(`${BASE_URL}/popular.html?page=1`);
    const $ = cheerio.load(popularPage.data);

    $('div.last_episodes > ul > li').each((i, el) => {
      list.push({
        animeId: $(el).find('p.name > a').attr('href').split('/')[2],
        animeTitle: $(el).find('p.name > a').attr('title'),
        animeImg: $(el).find('div > a > img').attr('src'),
        releasedDate: $(el).find('p.released').text().replace('Released: ', '').trim(),
        animeUrl: BASE_URL + $(el).find('p.name > a').attr('href'),
      });
    });

    const jsonList = JSON.stringify(list, null, 2);
    fs.writeFileSync('./gogoanime/popular.json', jsonList);
    console.log('Data saved to gogoanime/popular.json');
    
    return list;
  } catch (err) {
    console.error(err);
    return { error: err };
  }
};

scrapePopularAnime();
