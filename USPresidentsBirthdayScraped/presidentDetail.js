'use strict';

const rp = require('request-promise');
const $ = require('cheerio');

exports.OnePresidentDetail = async (url) => {
    let pr = (resolve, reject) => {
        rp(url)
            .then(function (html) {
                //exporting birthday and name
                return resolve({
                    name: $('.firstHeading', html).text(),
                    birthday: $('.bday', html).text()
                });
            })
            .catch(function (err) {
                //handle error
                console.log(err, " In error")
                return reject(err)
            });
    }
    return new Promise(pr)
}


