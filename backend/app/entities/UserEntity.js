const BaseUserEntity    = require('sota-core').load('entity/UserEntity');

module.exports = BaseUserEntity.extends({
  classname: 'UserEntity',

  save: function ($super, callback) {
    this.generateReferralId((err, referralId) => {
      if (err) {
        return callback(err);
      }

      this.setData({ referralId });
      $super(callback);
    });
  },

  generateReferralId: function (callback) {
    let referralId;
    while (!referralId) {
      referralId = Math.random().toString(36).substring(2, 8).toUpperCase();
    }

    this.findByReferralId(referralId, (err, ret) => {
      if (err) {
        return callback(err);
      }

      // If the referralId is not existed, return it
      if (!ret) {
        return callback(null, referralId);
      }

      // Otherwise try to generate another one
      this.generateReferralId(callback);
    });
  },

  findByReferralId: function (referralId, callback) {
    this._model.findOne({
      where: 'referral_id=?',
      params: [referralId]
    }, callback);
  },

});
