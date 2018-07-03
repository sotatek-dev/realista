module.exports = {
  GET: {
    '/nep5/info'                  : ['NEP5TokenController.getTokenInfo'],
    '/nep5/balance'               : ['NEP5TokenController.getBalance'],
    '/nep5/config'                : ['NEP5TokenController.getConfigValue'],
    '/kyc-status'                 : ['NEP5SaleController.getKycStatus'],
    '/users'                      : ['UserController.getListUsers', ['authenticate']],
    '/refunds'                    : ['UserController.getListRefunds', ['authenticate']],
  },
  POST: {
    '/nep5/config'                : ['NEP5TokenController.setConfigValue', ['authenticate']],
    '/login'                      : ['UserController.login'],
    '/register'                   : ['UserController.register'],
    '/kyc-register'               : ['NEP5SaleController.KycRegister', ['authenticate']],
    '/kyc-reject'                 : ['NEP5SaleController.KycReject', ['authenticate']],
  },
  PUT: {
    // Implement me.
  },
  DELETE: {
    // Implement me.
  }
};
