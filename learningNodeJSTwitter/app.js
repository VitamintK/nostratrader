/*eslint-env node*/

//------------------------------------------------------------------------------
// node.js starter application for Bluemix
//------------------------------------------------------------------------------

// This application uses express as its web server
// for more info, see: http://expressjs.com
var express = require('express');
var request = require('request');
var async   = require('async');

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
app.listen(appEnv.port, function() {

	// print a message when the server starts listening
  console.log("server starting on " + appEnv.url);
});

function getCorrelation(pUrl, nUrl){

    var positive, negative;

    async.map(
        [
            pUrl,
            nUrl
        ],
        makeRequest,
        function(error, results){

            if(error){
                console.log("Shit broke");
            }
            else{

                positive = JSON.parse(results[0]);
                negative = JSON.parse(results[1]);

                console.log("Correlation");
                console.log("Positive: ", positive.search.results);
                console.log("Negative: ",negative.search.results);
                console.log("RESULTS: ", positive.search.results/negative.search.results);

            }

        });

}
getCorrelation(urlConstruct('Obama', 'positive', '2015-10-02T16:00;00Z', '2015-10-02T15:00;00Z'), urlConstruct());

function makeRequest(url, cb){

    request.get( url ,
        function(error, response, body){

            if(error){

                cb(error);

            }
            else{

                cb(error, body)

            }
        });
}

function urlConstruct(subject, sentiment, start, end){

    return "https://163ab45d-44d2-4be8-a963-389217922b17:0E3JTtCiGn@cdeservice.mybluemix.net:443/api/v1/messages/count?q=" + subject + " sentiment:" + sentiment +" posted:" + start + "," + end;

}

function formatDate(date){

    var year = date.getFullYear();
    var month = (date.getMonth() < 9) ? "0" + date.getMonth() + 1: date.getMonth() + 1;
    var day = (date.getDate() < 10) ? "0" + date.getDate(): date.getDate();
    var hours = (date.getHours() < 10) ? "0" + date.getHours(): date.getHours();
    var minutes = (date.getMinutes() < 10) ? "0" + date.getMinutes(): date.getMinutes();

    return year + "-" + month + "-" + day + "T" + hours + ":" + minutes + ":00Z"

}