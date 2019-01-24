const puppeteer = require('puppeteer');
const mainUrl = 'https://ngodarpan.gov.in/index.php/home/statewise_membersPAV';

const $ = require('cheerio');
const async = require('async');
const sleep = require('sleep');


puppeteer
    .launch()
    .then((browser) => {
        return browser.newPage()
    })
    .then((page) => {
        console.log(`loading page: ${mainUrl}`);
        return page.goto(mainUrl, {
            waitUntil: 'networkidle0',
            timeout: 120000,
        }).then(() => page.content())

    })
    .then(async (html) => {
        //success
        async.map($('a.bluelink11px', html), function (i, callback) {
            callback(null, i.attribs.href)
        }, async function (e, results) {
            console.log("All done", results)
            const browser = await puppeteer.launch();
            const pdfs = results.map(async (url, i) => {
                const page = await browser.newPage();

                console.log(`loading page: ${url}`);
                // await page.goto(url, {
                //     waitUntil: 'networkidle0',
                //     timeout: 120000,
                // }).then(() => page.content())
                //     .then(async (innerHtml) => {
                //         // console.log(innerHtml, "   mm")
                //         // $('table a[href="javascript:void(0)"]', innerHtml)
                //         await page.click('table a[href="javascript:void(0)"]');
                //         console.log("   mmm   ", $('#ngo_regno', innerHtml))
                //         console.log(`closing page: ${url}`);
                //         await page.close();
                //     })

                const response = await page.goto(url, {
                    waitUntil: 'networkidle0',
                    timeout: 3000000
                })
                // const listHandle =
                //     await page.$('table a[href="javascript:void(0)"]')
                // const hndle = listHandle.asElement()
                // const hndleE = await page.evaluate(() => Array.from(document.querySelectorAll('table a[href="javascript:void(0)"]'), hndle => hndle.textContent));;
                // const hndleE = await page.evaluate(hndle => hndle.textContent, hndle);
                const example = await page.$$('table a[href="javascript:void(0)"]');
                for (let element of example) {
                    let hndle = await element.asElement()
                    let hndleE = await page.evaluate(hndle => hndle.textContent, hndle);
                    // console.log(hndleE, "  hndleE")
                    await element.click();
                    sleep.sleep(10)
                    let data = await page.$('#ngo_regno')
                    let text = await page.evaluate(data => data.textContent, data);
                    console.log(text, " ------jkfjds -----", hndleE)
                    // console.log(element, "hndleE")
                }



                // await page.click('table a[href="javascript:void(0)"]')
                // let data = await page.$('#ngo_regno')
                // const text = await page.evaluate(data => data.textContent, data);

                // console.log("   mmm   ", text)
                console.log(`closing page: ${url}`);
                await page.close();

            });
        })
    })
    .catch((err) => {
        //handle error
        console.log(err, " in error")
    })