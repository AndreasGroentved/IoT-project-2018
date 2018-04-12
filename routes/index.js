var express = require('express');
var router = express.Router();

var dbLogic = require('../domain/Domain');
new dbLogic.Domain();

/* GET home page. */
router.get('/', function (req, res, next) {
    var response = dbLogic.Domain.prototype.test();
    dbLogic.Domain.prototype.test2(res);
   // res.render('index', {title: response});

});

module.exports = router;
