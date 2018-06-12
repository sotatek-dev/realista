const async           = require('async');
const ErrorFactory    = require('sota-core').load('error/ErrorFactory');
const BaseService     = require('sota-core').load('service/UserService');

module.exports = BaseService.extends({
  classname: 'UserService',

  register: function ($super, userInfo, callback) {
    const UserModel = this.getModel('UserModel');

    if (!userInfo.referrerId) {
      $super(userInfo, callback);
      return;
    }

    UserModel.findOne({
      where: 'referral_id = ?',
      params: [userInfo.referrerId]
    }, (err, ret) => {
      if (err) {
        return callback(err);
      }

      if (!ret) {
        return callback(ErrorFactory.badRequest(`Invalid referrer: ${userInfo.referrerId}`));
      }

      $super(userInfo, callback);
    });
  },

  getListUsers: function (params, callback) {
    const page = params.page || 1;
    const limit = params.limit || 10;

    const UserModel = this.getModel('UserModel');
    UserModel.find({
      where: '1=1',
      params: [],
      limit: limit,
      offset: (page - 1) * limit,
      orderBy: 'id DESC'
    }, (err, users) => {
      if (err) {
        return callback(err);
      }

      callback(null, users);
    });
  },

  getListRefunds: function (params, callback) {
    const page = params.page || 1;
    const limit = params.limit || 10;

    const UserModel = this.getModel('RefundModel');
    UserModel.find({
      where: '1=1',
      params: [],
      limit: limit,
      offset: (page - 1) * limit,
      orderBy: 'block_number DESC'
    }, (err, ret) => {
      if (err) {
        return callback(err);
      }

      callback(null, ret);
    });
  },

});
