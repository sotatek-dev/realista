const _                 = require('lodash');
const async             = require('async');
const Checkit           = require('cc-checkit');
const AppController     = require('./AppController');

module.exports = AppController.extends({
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

});
