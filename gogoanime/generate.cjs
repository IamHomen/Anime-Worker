const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs';)

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

const popular_ongoing_url = 'https://ajax.gogocdn.net/ajax/page-recent-release-ongoing.html'; // You need to define this URL

const scrapeTrendingAnime = async () => {
  const list = [];
  try {
    let pageNum = 1;
    const popular_page = await axios.get(`
        ${popular_ongoing_url}?page=${pageNum}
        `);
  const $ = cheerio.load(popular_page.data);

  $('div.added_series_body.popular > ul > li').each((i, el) => {
   let genres = [];
   $(el)
    .find('p.genres > a')
    .each((i, el) => {
     genres.push($(el).attr('title'));
    });
   list.push({
    animeId: $(el).find('a:nth-child(1)').attr('href').split('/')[2],
    animeTitle: $(el).find('a:nth-child(1)').attr('title'),
    animeImg: $(el)
     .find('a:nth-child(1) > div')
     .attr('style')
     .match('(https?://.*.(?:png|jpg))')[0],
    latestEp: $(el).find('p:nth-child(4) > a').text().trim(),
    animeUrl: BASE_URL + $(el).find('a:nth-child(1)').attr('href'),
    genres: genres,
   });
  });

    const jsonList = JSON.stringify(list, null, 2);
    fs.writeFileSync('./gogoanime/trending.json', jsonList);
    console.log('Data saved to gogoanime/trending.json');
    return list;
  } catch (err) {
    console.log(err);
    return { error: err };
  }
};

scrapeTrendingAnime();
scrapePopularAnime();
