const http = require('http');
const url = require("url");
const statuses = ['pending', 'picking', 'on-way', 'delivered']

const requestListener = function (req, res) {
    res.writeHead(200);
    const queryObject = url.parse(req.url, true).query;
    let status = queryObject['status'];
    if (status && statuses.indexOf(status) >= 0 && statuses.indexOf(status) < 4) {
        let answer = statuses[Math.floor(Math.random() * (4 - statuses.indexOf(status)) + statuses.indexOf(status))]
        console.log("> " + status + " --> " + answer);
        res.end(answer);
    } else
        res.end(statuses[0]);
}

const server = http.createServer(requestListener);
server.listen(6000);
