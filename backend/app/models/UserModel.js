/* eslint no-multi-spaces: ["error", { exceptions: { "VariableDeclarator": true } }] */
const _                 = require('lodash');
const async             = require('async');
const util              = require('util');
const UserModel         = require('sota-core').load('model/UserModel');
const UserEntity        = require('../entities/UserEntity');

module.exports = UserModel.extends({
  classname: 'UserModel',

  $dsConfig: {
    read: 'mysql-slave',
    write: 'mysql-master'
  },

  $Entity: UserEntity,

});
