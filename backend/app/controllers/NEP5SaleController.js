const _                     = require('lodash');
const Checkit               = require('cc-checkit');
const AppController         = require('./AppController');

module.exports = AppController.extends({
  classname: 'NEP5SaleController',

  getKycStatus: function (req, res) {
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
    const address = params.address
    const NEP5SaleService = req.getService('NEP5SaleService');
    NEP5SaleService.getKycStatus(network, scriptHash, address, this.ok.bind(this, req, res));
  },

  KycRegister: function (req, res) {
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
    const address = params.address
    const NEP5SaleService = req.getService('NEP5SaleService');
    NEP5SaleService.KycRegister(network, scriptHash, address, this.ok.bind(this, req, res));
  },

  KycReject: function (req, res) {
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
    const address = params.address
    const NEP5SaleService = req.getService('NEP5SaleService');
    NEP5SaleService.KycReject(network, scriptHash, address, this.ok.bind(this, req, res));
  },

});
