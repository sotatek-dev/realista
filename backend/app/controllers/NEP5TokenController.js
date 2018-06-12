const _                     = require('lodash');
const Checkit               = require('cc-checkit');
const AppController         = require('./AppController');

module.exports = AppController.extends({
  classname: 'NEP5TokenController',

  getTokenInfo: function (req, res) {
    const [err, params] = new Checkit({
      network: ['required', 'string'],
      scriptHash: ['required', 'string']
    }).validateSync(req.allParams);

    if (err) {
      res.badRequest(err.toString());
      return;
    }

    const network = params.network;
    const scriptHash = params.scriptHash;
    const NEP5TokenService = req.getService('NEP5TokenService');
    NEP5TokenService.getTokenInfo(network, scriptHash, this.ok.bind(this, req, res));
  },

  getBalance: function (req, res) {
    const [err, params] = new Checkit({
      network: ['required', 'string'],
      scriptHash: ['required', 'string'],
      address: ['required', 'string'],
    }).validateSync(req.allParams);

    if (err) {
      res.badRequest(err.toString());
      return;
    }

    const network = params.network;
    const scriptHash = params.scriptHash;
    const address = params.address;
    const NEP5TokenService = req.getService('NEP5TokenService');
    NEP5TokenService.getTokenBalance(network, scriptHash, address, this.ok.bind(this, req, res));
  },

  getConfigValue: function (req, res) {
    const [err, params] = new Checkit({
      network: ['required', 'string'],
      scriptHash: ['required', 'string'],
      configName: ['required', 'string'],
    }).validateSync(req.allParams);

    if (err) {
      res.badRequest(err.toString());
      return;
    }

    const network = params.network;
    const scriptHash = params.scriptHash;
    const configName = params.configName;
    const NEP5TokenService = req.getService('NEP5TokenService');
    NEP5TokenService.getConfigValue(network, scriptHash, configName, this.ok.bind(this, req, res));
  },

  setConfigValue: function (req, res) {
    const [err, params] = new Checkit({
      network: ['required', 'string'],
      scriptHash: ['required', 'string'],
      configName: ['required', 'string'],
      configValue: ['required'],
    }).validateSync(req.allParams);

    if (err) {
      res.badRequest(err.toString());
      return;
    }

    const network = params.network;
    const scriptHash = params.scriptHash;
    const configName = params.configName;
    const configValue = params.configValue;
    const NEP5TokenService = req.getService('NEP5TokenService');
    NEP5TokenService.setConfigValue(network, scriptHash, configName, configValue, this.ok.bind(this, req, res));
  },

});
