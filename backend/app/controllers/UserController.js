const _                 = require('lodash');
const async             = require('async');
const Checkit           = require('cc-checkit');
const AppController     = require('./AppController');
const AuthController    = require('sota-core').load('controller/AuthController');
const ErrorFactory      = require('sota-core').load('error/ErrorFactory');
const Const             = require('../common/Const')
const logger            = require('sota-core').getLogger('UserController');

module.exports = AuthController.extends({
  classname: 'UserController',

  register: function (req, res) {
    const [err, params] = new Checkit({
      email: ['required', 'email'],
      password: ['required'],
      fullName: ['required', 'string'],
      neoAddress: ['required', 'string'],
      referrerId: ['string'],
    }).validateSync(req.allParams);

    if (err) {
      return res.badRequest(err.toString());
    }

    const UserService = req.getService('UserService');
    UserService.register(params, this.created.bind(this, req, res));
  },

  getListUsers: function (req, res) {
    const [err, params] = new Checkit({
      page: ['natural'],
      limit: ['naturalNonZero']
    }).validateSync(req.allParams);

    if (err) {
      return res.badRequest(err.toString());
    }

    const UserService = req.getService('UserService');
    UserService.getListUsers(params, this.ok.bind(this, req, res));
  },

  getListRefunds: function (req, res) {
    const [err, params] = new Checkit({
      page: ['natural'],
      limit: ['naturalNonZero']
    }).validateSync(req.allParams);

    if (err) {
      return res.badRequest(err.toString());
    }

    const UserService = req.getService('UserService');
    UserService.getListRefunds(params, this.ok.bind(this, req, res));
  },

  login: function ($super, req, res) {
    let UserModel = req.getModel('UserModel');
    let email = req.body.email || '';
    let field = 'email';
    if (email.indexOf('@') < 0) {
      field = 'username';
    }

    UserModel.findOne({
      where: `${field}=?`,
      params: [email.toLowerCase()]
    }, function (err, user) {
      if (err) {
        return res.ok(err);
      }

      if (!user) {
        logger.error(`User not found ${field}=${email}`);
        return res.ok(ErrorFactory.notFound(`User not found: ${field}=${email}`));
      }

      if (user.role !== Const.ROLE.ADMIN) {
        logger.error(`Invalid role for ${field}=${email}`);
        return res.ok(ErrorFactory.badRequest('Wrong role.'));
      }

      return $super(req, res);
    });
  },

  generateAccessToken: function ($super, user, expiredTime) {
    // Default 100 years (never-expired) token.
    return $super(user, expiredTime || 3600 * 24 * 365 * 100);
  },

});
