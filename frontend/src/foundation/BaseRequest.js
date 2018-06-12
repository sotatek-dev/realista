import _        from 'lodash';
import axios    from 'axios';

class BaseRequest {
  get(url, params = {}) {
    return this._doRequest('GET', url, { params });
  }

  put(url, data = {}) {
    return this._doRequest('put', url, { data });
  }

  post(url, data = {}) {
    return this._doRequest('post', url, { data });
  }

  _doRequest (method, url, paramsConfig) {
    url = `http://localhost:8001/api${url}`;

    const config = _.assign({
      method,
      url,
      headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        'Authorization': this._getAuthToken(),
      },
    }, paramsConfig);

    return axios(config)
      .then(response => {
        return response.data;
      })
      .catch(err => {
        if (err.response) {
          return Promise.reject(err.response.data.msg);
        }

        if (err.request) {
          return Promise.reject(err.request);
        }

        return Promise.reject(err.message);
      });
  }

  _getAuthToken () {
    return 'Basic YWRtaW46MQ==';
  }

}

export default BaseRequest;
