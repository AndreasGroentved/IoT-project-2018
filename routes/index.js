var express = require('express');
var router = express.Router();

var domain = require('../domain/Domain');
var path = require("path");
new domain.Domain();

/* GET home page. */
router.get('/', function (req, res, next) {
    domain.Domain.prototype.getAllTemperatures();
    res.sendFile(path.resolve("index.html"));
    // res.render('index', {title: response});
});

router.get('/temperature', function (req, res, next) {
    var response = domain.Domain.prototype.getAllTemperatures();

    response.then(function (msg) {
        console.log(msg);
        console.log("Promise resolved as " + JSON.stringify(msg));
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(msg));
    });
});


router.post('/temperature', function (req, res, next) {
   // console.log(req.body);
    domain.Domain.prototype.saveTemperature(req.body);
    res.status(200).json('success');
});


module.exports = router;