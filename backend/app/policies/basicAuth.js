const ErrorFactory = require('sota-core').load('error/ErrorFactory');

module.exports = function (req, res, next) {
  const authHeader = req.headers['authorization'];
  if (!authHeader) {
    return next(ErrorFactory.unauthorized(`Authorization header is missing.`));
  }

  const tokens = authHeader.split(' ');
  if (!tokens[0] || tokens[0].toLowerCase() !== 'basic') {
    return next(ErrorFactory.unauthorized(`Not basic authorization header.`));
  }

  if (!tokens[1]) {
    return next(ErrorFactory.unauthorized(`Credentials is missing in Authorization header.`));
  }

  try {
    const buf = new Buffer(tokens[1], 'base64');
    const plainCredentials = buf.toString();
    const creds = plainCredentials.split(':');
    const username = creds[0];
    const password = creds[1];
    if (username.toLowerCase() !== process.env.BASIC_AUTH_USER || password !== process.env.BASIC_AUTH_PASSWORD) {
      return next(ErrorFactory.unauthorized(`Invalid credentials: wrong username or password`));
    }
  } catch (e) {
    return next(ErrorFactory.unauthorized(`Invalid credentials: cannot parse basic auth token.`));
  }

  next();
};
