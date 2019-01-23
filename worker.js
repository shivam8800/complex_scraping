'use strict';

const Kue = require('kue');
const queue = Kue.createQueue();

const rp = require('request-promise');
const otcsv = require('objects-to-csv');
const cheerio = require('cheerio');



queue.process('scrap', function (job, done) {
    console.log(`Working on job ${job.id}`);
    scraping_website(job.data.link, done);
})

const scraping_website = async (link) => {
    const html = await rp(link);
    const businessMap = cheerio('a', html).map(async (i, e) => {
        const second_link = e.attribs.href;
        if (second_link.includes('https://www.giveindia.org/nonprofit/') && second_link.length > 'https://www.giveindia.org/nonprofit/'.length) {

            const innerHtml = await rp(second_link);
            const address = cheerio('#__next > div:nth-child(2) > main > div > div.container > div > div.col-12.col-sm-12.col-md-7.col-lg-8 > div:nth-child(7) > div.w-100.row-margins.row > div.col-12.col-lg-5 > p span', innerHtml).text();

            const email = cheerio('#__next > div:nth-child(2) > main > div > div.container > div > div.col-12.col-sm-12.col-md-7.col-lg-8 > div:nth-child(7) > div.w-100.row-margins.row > div.ml-auto.col-12.col-lg-6 > p:nth-child(2) a', innerHtml).text();

            const phone = cheerio('#__next > div:nth-child(2) > main > div > div.container > div > div.col-12.col-sm-12.col-md-7.col-lg-8 > div:nth-child(7) > div.w-100.row-margins.row > div.ml-auto.col-12.col-lg-6 a').text()

            return {
                "Email": email,
                "Address": address,
                "phone": phone
            }
        }
    }).get();
    Promise.all(businessMap)
        .then((result) => {
            console.log(result, "  final result")
        })
        .catch((err) => {
            console.log("In error", err)
        })
};