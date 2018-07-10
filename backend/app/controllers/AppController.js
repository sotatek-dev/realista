const _                       = require('lodash');
const ExternalServiceAdapter  = require('sota-core').load('external_service/foundation/ExternalServiceAdapter');
const BaseController          = require('sota-core').load('controller/BaseController');
const path                    = require('path');

module.exports = BaseController.extends({
  classname: 'AppController',

  helloWorld: function (req, res) {
    res.sendFile(path.join(__dirname, '../../public', 'index.html'));
  }

});
