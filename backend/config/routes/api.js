module.exports = {
  GET: {
    '/nep5/info'                  : ['NEP5TokenController.getTokenInfo'],
    '/nep5/balance'               : ['NEP5TokenController.getBalance'],
    '/nep5/config'                : ['NEP5TokenController.getConfigValue'],
    '/users'                      : ['UserController.getListUsers', ['basicAuth']],
    '/refunds'                    : ['UserController.getListRefunds', ['basicAuth']],
  },
  POST: {
    '/nep5/config'                : ['NEP5TokenController.setConfigValue', ['basicAuth']],
    '/register'                   : ['UserController.register'],
  },
  PUT: {
    // Implement me.
  },
  DELETE: {
    // Implement me.
  }
};
