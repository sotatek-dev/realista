const _                   = require('lodash');
const async               = require('async');
const nep5                = require('../blockchain/neo/nep5');
const AppService          = require('./AppService');
const logger              = require('sota-core').getLogger('NEP5SaleService');

const CACHED_DATA = {};

module.exports = AppService.extends({
  classname: 'NEP5SaleService',

  getKycStatus: function (network, scriptHash, address , callback) {
    nep5.getKycStatus(network, scriptHash, address)
      .then((ret) => {
        return callback(null, ret);
      })
      .catch((err) => {
        return callback(err);
      });
  },

  KycReject: function (network, scriptHash, address , callback) {
    nep5.KycReject(network, scriptHash, process.env.OWNER_ACCOUNT_WIF, address)
      .then((ret) => {
        return callback(null, ret);
      })
      .catch((err) => {
        return callback(err);
      });
  },

  KycRegister: function (network, scriptHash, address , callback) {
    nep5.KycRegister(network, scriptHash, process.env.OWNER_ACCOUNT_WIF, address)
      .then((ret) => {
        return callback(null, ret);
      })
      .catch((err) => {
        return callback(err);
      });
  },

});
