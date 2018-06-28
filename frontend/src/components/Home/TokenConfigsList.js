import React from 'react';
import {
  Grid,
} from 'react-bootstrap';
import moment from 'moment';
import PropTypes from 'prop-types';

import TokenConfigItem from './TokenConfigItem';

class TokenConfigsList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      WHITELIST_SALE_OPEN: '',
      WHITELIST_SALE_CLOSE: '',
    };
  }

  handleChange (configName, event) {
    const newState = {};
    newState[configName] = event.target.value;
    this.setState(newState);
  }

  formatTime (time) {
    if (isNaN(time)) {
      return 'Invalid timestamp';
    }

    return moment.unix(parseInt(time, 10)).format();
  }

  render() {
    return (
      <Grid>

        <TokenConfigItem
          configName={'WHITELIST_SALE_OPEN'}
          configValueFormat={this.formatTime}
          network={this.props.network}
          scriptHash={this.props.scriptHash} />
        <TokenConfigItem
          configName={'WHITELIST_SALE_CLOSE'}
          configValueFormat={this.formatTime}
          network={this.props.network}
          scriptHash={this.props.scriptHash} />

      </Grid>
    )
  }
}

TokenConfigsList.propTypes = {
  network: PropTypes.string.isRequired,
  scriptHash: PropTypes.string.isRequired,
};

export default TokenConfigsList;
