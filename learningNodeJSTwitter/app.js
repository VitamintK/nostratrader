/*eslint-env node*/

//------------------------------------------------------------------------------
// node.js starter application for Bluemix
//------------------------------------------------------------------------------

// This application uses express as its web server
//var csv = require('csv');
myList = [];
// for more info, see: http://expressjs.com
var express = require('express');
var request = require('request');
var async = require('async');

// cfenv provides access to your Cloud Foundry environment
// for more info, see: https://www.npmjs.com/package/cfenv
var cfenv = require('cfenv');

// create a new express server
var app = express();

// serve the files out of ./public as our main files
app.use(express.static(__dirname + '/public'));

// get the app environment from Cloud Foundry
var appEnv = cfenv.getAppEnv();

// start server on the specified port and binding host
app.listen(appEnv.port, function () {

    // print a message when the server starts listening
    console.log("server starting on " + appEnv.url);
});
console.log("present");
var d = new Date();
d.setDate(d.getDate() - 1);
//console.log(d);
//console.log(d < new Date());
var today = new Date()
    //for (var i = d; i < new Date(); i.setHours(i.getHours() + 1)) {
    //    //console.log(i);
    //    var dateplushour = new Date(i);
    //    dateplushour.setHours(i.getHours() + 1);
    //    //console.log(dateplushour);
    //    getCorrelation(urlConstruct('Obama', 'positive', formatDate(i), formatDate(dateplushour)), urlConstruct('Obama', 'negative', formatDate(i), formatDate(dateplushour)));
    //}

nintydays = new Date(today)
nintydays.setDate(today.getDate() - 90)
for (var i = new Date(nintydays); i < new Date(); i.setDate(i.getDate() + 1)) {
    console.log(i);
    var dateplusday = new Date(i);
    dateplusday.setDate(i.getDate() + 1);
    //console.log("This date is important" + formatDate(i));
    var IHateAsync = new Date(i)
    getCorrelation(urlConstruct('Obama', 'positive', formatDate(i), formatDate(dateplusday)), urlConstruct('Obama', 'negative', formatDate(i), formatDate(dateplusday)), IHateAsync);
}

function getCorrelation(pUrl, nUrl, timestamp) {

    //console.log(nUrl);
    //console.log(nUrl);

    var positive, negative;

    async.map(
        [
            pUrl,
            nUrl
        ],
        makeRequest,
        function (error, results) {

            if (error) {
                console.log("Shit broke");
            } else {

                positive = JSON.parse(results[0]);
                negative = JSON.parse(results[1]);

                //console.log(positive);

                //                console.log("Correlation");
                //                console.log("Positive: ", positive.search.results);
                //                console.log("Negative: ", negative.search.results);
                //                console.log("RESULTS: ", positive.search.results / negative.search.results);
                myList.push([timestamp, positive.search.results / negative.search.results]);
                console.log([timestamp, positive.search.results / negative.search.results]);

            }

        });

}


function makeRequest(url, cb) {

    request.get(url,
        function (error, response, body) {

            if (error) {

                cb(error);

            } else {

                cb(error, body)

            }
        });
}

function urlConstruct(subject, sentiment, start, end) {

    return "https://163ab45d-44d2-4be8-a963-389217922b17:0E3JTtCiGn@cdeservice.mybluemix.net:443/api/v1/messages/count?q=" + subject + " sentiment:" + sentiment + " posted:" + start + "," + end;

}

function formatDate(date) {
    //console.log("This is date:" + date);

    var year = date.getFullYear();
    var month = (date.getMonth() < 9) ? "0" + (date.getMonth() + 1) : date.getMonth() + 1;
    var day = (date.getDate() < 10) ? "0" + date.getDate() : date.getDate();
    var hours = (date.getHours() < 10) ? "0" + date.getHours() : date.getHours();
    var minutes = (date.getMinutes() < 10) ? "0" + date.getMinutes() : date.getMinutes();

    return year + "-" + month + "-" + day + "T" + hours + ":" + minutes + ":00Z"

}