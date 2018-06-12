import React from 'react';
import {
  Row,
  Col,
  Button,
  FormControl,
  ControlLabel,
} from 'react-bootstrap';

import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import NeoRequest from '../../request/NeoRequest';

class TokenConfigItem extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      value: ''
    };
  }

  handleChange (event) {
    this.setState({
      value: event.target.value
    });
  }

  componentDidUpdate (prevProps, prevState, snapshot) {
    if (this.props.network === prevProps.network &&
        this.props.scriptHash === prevProps.scriptHash &&
        this.props.configName === prevProps.configName) {
      return;
    }

    NeoRequest.getTokenConfig({
      network: this.props.network,
      scriptHash: this.props.scriptHash,
      configName: this.props.configName,
    })
    .then(response => {
      this.setState(response);
    })
    .catch(err => {
      console.error(err);
    });
  }

  updateConfig (e) {
    NeoRequest.setTokenConfig({
      network: this.props.network,
      scriptHash: this.props.scriptHash,
      configName: this.props.configName,
      configValue: this.state.value,
    })
    .then(response => {
      if (response.result === true) {
        toast.info(`Update config [${this.props.configName}] successful.`);
      } else {
        toast.error(`Update config [${this.props.configName}] failed.`);
      }
    })
    .catch(err => {
      console.error(err);
    });
  }

  render() {
    return (
      <Row style={{ marginBottom: '5px' }}>
        <Col xs={3}><ControlLabel>{this.props.configName}</ControlLabel></Col>
        <Col xs={4}>
          <FormControl
            type="text"
            value={this.state.value}
            onChange={this.handleChange.bind(this)} />
        </Col>
        <Col xs={4}>
          <FormControl type="text" value={this.props.configValueFormat(this.state.value)} readOnly />
        </Col>
        <Col xs={1}>
          <Button bsStyle="primary" onClick={this.updateConfig.bind(this)} block>Set</Button>
        </Col>
      </Row>
    )
  }
}

TokenConfigItem.propTypes = {
  network: PropTypes.string.isRequired,
  scriptHash: PropTypes.string.isRequired,
  configName: PropTypes.string.isRequired,
  configValueFormat: PropTypes.func.isRequired,
};

export default TokenConfigItem;
