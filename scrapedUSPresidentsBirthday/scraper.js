'use strict';

const rp = require('request-promise');
const $ = require('cheerio');

const presidentDetails = require('./presidentDetail');

const base_url = "https://en.wikipedia.org/",
    search_url = "wiki/List_of_Presidents_of_the_United_States";

rp(base_url + search_url)
    .then(function (html) {
        //extracting all presidents saparate links
        const wikiUrls = [];
        for (let i = 0; i < $('big > a', html).length; i++) {
            wikiUrls.push($('big > a', html)[i].attribs.href);
        }

        //extracting details of every presidents one by one
        return Promise.all(
            wikiUrls.map((url) => presidentDetails.OnePresidentDetail(base_url + url))
        )
    })
    .then((presidents) => {
        console.log(presidents, " finally scraped all presidents")
    })
    .catch(function (err) {
        //handle error
        console.log(err, " In error")
    });


