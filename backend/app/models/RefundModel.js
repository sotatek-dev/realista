/* eslint no-multi-spaces: ["error", { exceptions: { "VariableDeclarator": true } }] */
const _                 = require('lodash');
const async             = require('async');
const util              = require('util');
const BaseModel         = require('sota-core').load('model/BaseModel');

module.exports = BaseModel.extends({
  classname: 'RefundModel',

  $tableName: 'refund',

  $dsConfig: {
    read: 'mysql-slave',
    write: 'mysql-master'
  },

});
