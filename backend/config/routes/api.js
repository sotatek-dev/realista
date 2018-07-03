module.exports = {
  GET: {
    '/nep5/info'                  : ['NEP5TokenController.getTokenInfo'],
    '/nep5/balance'               : ['NEP5TokenController.getBalance'],
    '/nep5/config'                : ['NEP5TokenController.getConfigValue'],
    '/kyc-status'                 : ['NEP5SaleController.getKycStatus'],
    '/users'                      : ['UserController.getListUsers', ['basicAuth']],
    '/refunds'                    : ['UserController.getListRefunds', ['basicAuth']],
  },
  POST: {
    '/nep5/config'                : ['NEP5TokenController.setConfigValue', ['basicAuth']],
    '/login'                      : ['UserController.login'],
    '/register'                   : ['UserController.register'],
    '/kyc-register'               : ['NEP5SaleController.KycRegister', ['basicAuth']],
    '/kyc-reject'                 : ['NEP5SaleController.KycReject', ['basicAuth']],
  },
  PUT: {
    // Implement me.
  },
  DELETE: {
    // Implement me.
  }
};
