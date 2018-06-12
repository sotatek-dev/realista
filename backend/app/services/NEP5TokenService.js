const _                   = require('lodash');
const async               = require('async');
const nep5                = require('../blockchain/neo/nep5');
const AppService          = require('./AppService');
const logger              = require('sota-core').getLogger('NEP5TokenService');

const CACHED_DATA = {};

module.exports = AppService.extends({
  classname: 'NEP5TokenService',

  getTokenInfo: function (network, scriptHash, callback) {
    nep5.getTokenInfo(network, scriptHash)
      .then((ret) => {
        return callback(null, ret);
      })
      .catch((err) => {
        return callback(err);
      });
  },

  getTokenBalance: function (network, scriptHash, address, callback) {
    nep5.getBalance(network, scriptHash, address)
      .then((balance) => {
        return callback(null, { balance });
      })
      .catch((err) => {
        return callback(err);
      });
  },

  getConfigValue: function (network, scriptHash, configName, callback) {
    if (CACHED_DATA[configName] !== undefined) {
      return callback(null, CACHED_DATA[configName]);
    }

    nep5.getConfigValue(network, scriptHash, configName)
      .then((value) => {
        return callback(null, { value });
      })
      .catch((err) => {
        return callback(err);
      });
  },

  setConfigValue: function (network, scriptHash, configName, configValue, callback) {
    nep5.setConfigValue(network, scriptHash, process.env.OWNER_ACCOUNT_WIF, configName, configValue)
      .then((ret) => {
        return callback(null, ret);
      })
      .catch((err) => {
        return callback(err);
      });
  },

});
