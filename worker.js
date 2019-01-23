'use strict';

const Kue = require('kue');
const queue = Kue.createQueue();

const rp = require('request-promise');
const cheerio = require('cheerio');
const CsvWriter = require('csv-write-stream');
const fs = require('fs');


queue.process('scrap', function (job, done) {
    console.log(`Working on job ${job.id}`);
    scraping_website(job.data.link, done);
})

const scraping_website = async (link) => {
    const html = await rp(link);
    let filepath = '/tmp/Data.csv';
    let writer = CsvWriter()
    writer.pipe(fs.createWriteStream(filepath))
    cheerio('a', html).map(async (i, e) => {
        let second_link = e.attribs.href;
        if (second_link.includes('https://www.giveindia.org/nonprofit/') && second_link.length > 'https://www.giveindia.org/nonprofit/'.length) {

            let innerHtml = await rp(second_link);
            let address = cheerio('#__next > div:nth-child(2) > main > div > div.container > div > div.col-12.col-sm-12.col-md-7.col-lg-8 > div:nth-child(7) > div.w-100.row-margins.row > div.col-12.col-lg-5 > p span', innerHtml).text();

            let email = cheerio('#__next > div:nth-child(2) > main > div > div.container > div > div.col-12.col-sm-12.col-md-7.col-lg-8 > div:nth-child(7) > div.w-100.row-margins.row > div.ml-auto.col-12.col-lg-6 > p:nth-child(2) a', innerHtml).text();

            let phone = cheerio('#__next > div:nth-child(2) > main > div > div.container > div > div.col-12.col-sm-12.col-md-7.col-lg-8 > div:nth-child(7) > div.w-100.row-margins.row > div.ml-auto.col-12.col-lg-6 > p:nth-child(1) a', innerHtml).text()

            if (email.includes(" ")) {
                email = email.split(" ")[0]
            }
            let csv_row = {
                "Email": email || "",
                "Address": address || "",
                "phone": phone || ""
            }
            writer.write(csv_row)
            return csv_row
        }
    }).get();
};