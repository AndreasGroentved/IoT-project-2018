var express = require('express');
var router = express.Router();
var url = require('url');

var domain = require('../domain/Domain');
var path = require("path");
new domain.Domain();

/* GET home page. */
router.get('/', function (req, res, next) {
    domain.Domain.prototype.getAllTemperatures();
    res.sendFile(path.resolve("index.html"));
});

router.get('/test', function (req, res, next) {
    domain.Domain.prototype.getAllTemperatures();
    res.sendFile(path.resolve("test.html"));
});

router.get('/temperature', function (req, res, next) {
    var query = req._parsedUrl.query
    
    var parts = url.parse(req.url, true);
    var query = parts.query;

    var response = null;

    if (query) {
        response = domain.Domain.prototype.getTemperatures(query.from, query.to)
    } else {
        response = domain.Domain.prototype.getAllTemperatures()
    }

    response.then(function (msg) {
        console.log(msg);
        console.log("Promise resolved as " + JSON.stringify(msg));
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(msg));
    });
});

router.post('/temperature', function (req, res, next) {
    console.log(req.body);
    domain.Domain.prototype.saveTemperature(req.body);
    res.status(200).json('success');
});

router.post('/lora', function (req, res, next) {
    var data = req.body.payload_fields;
    console.log(data.res);
    domain.Domain.prototype.saveTemperature(data.res);
    res.status(200).json('success');
});

module.exports = router;
