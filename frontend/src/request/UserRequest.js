import BaseRequest from '../foundation/BaseRequest';

class UserRequest extends BaseRequest {

  getList (params = {}) {
    return this.get('/users', params);
  }

  register (params = {}) {
    return this.post('/register', params);
  }

  getRefundList (params = {}) {
    return this.get('/refunds', params);
  }

  getKycStatus (params = {}) {
    return this.get('/kyc-status', params)
  }

}

export default new UserRequest();