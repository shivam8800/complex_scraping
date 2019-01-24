const puppeteer = require('puppeteer');
const url = 'https://www.reddit.com';

const $ = require('cheerio');

puppeteer
    .launch()
    .then(function (browser) {
        return browser.newPage();
    })
    .then(function (page) {
        return page.goto(url).then(function () {
            return page.content();
        });
    })
    .then(function (html) {
        // console.log(html, " meri html");
        $('h2', html).each(function () {
            console.log($(this).text());
        });
    })
    .catch(function (err) {
        //handle error
        console.log(err, " in error")
    });