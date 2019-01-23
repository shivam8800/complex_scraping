'use strict';

require('dotenv').config()

const Kue = require('kue');
const queue = Kue.createQueue();

queue.on('job enqueue', function () {
    console.log('job submitted in queue')
    process.exit(0);
})

let job = queue.create('scrap', {
    link: process.env.WEBSITE_URL
})
    .attempts(3) //if job fails retry in 3 times
    .backoff({ delay: 60 * 1000 }) // wait 60s before retry
    .save();