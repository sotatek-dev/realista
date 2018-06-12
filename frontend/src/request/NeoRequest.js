import BaseRequest from '../foundation/BaseRequest';

class NeoRequest extends BaseRequest {

  getTokenInfo (params = {}) {
    return this.get('/nep5/info', params);
  }

  getTokenConfig (params = {}) {
    return this.get('/nep5/config', params);
  }

  setTokenConfig (params = {}) {
    return this.post('/nep5/config', params);
  }

}

export default new NeoRequest();