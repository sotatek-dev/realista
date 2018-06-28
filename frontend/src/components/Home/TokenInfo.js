import React from 'react';
import {
  Grid,
  Row,
  Col,
  FormControl,
  ControlLabel
} from 'react-bootstrap';
import PropTypes from 'prop-types';

import NeoRequest from '../../request/NeoRequest';

class TokenInfo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      network: '',
      tokenName: '',
      tokenSymbol: '',
      totalSupply: '',
      // circulation: '',
    };
  }

  onNetworkSelected (event) {
    const selectedNetwork = event.target.value;
    this.changeNetwork(selectedNetwork);
  }

  changeNetwork (network) {
    this.props.onNetworkSelected(network);
    this.setState({
      network,
    });

    NeoRequest
      .getTokenInfo({
        network,
        scriptHash: this.props.scriptHash,
      })
      .then(tokenInfo => {
        this.setState({
          tokenName: tokenInfo.name,
          tokenSymbol: tokenInfo.symbol,
          totalSupply: tokenInfo.totalSupply,
          // circulation: tokenInfo.circulation
        });
      })
      .catch(err => {
        console.error(err);
      });
  }

  componentDidMount () {
    this.changeNetwork('PrivateNet');
  }

  render() {
    return (
      <Grid>
        <Row style={{ marginBottom: '5px' }}>
          <Col xs={2}><ControlLabel>Network</ControlLabel></Col>
          <Col xs={10}>
            <FormControl componentClass="select" value={this.state.network} onChange={this.onNetworkSelected.bind(this)}>
              <option value="MainNet">Main Net</option>
              <option value="TestNet">Test Net</option>
              <option value="PrivateNet">Private Net</option>
            </FormControl>
          </Col>
        </Row>

        <Row style={{ marginBottom: '5px' }}>
          <Col xs={2}><ControlLabel>Script Hash</ControlLabel></Col>
          <Col xs={10}>
            <FormControl type="text" value={this.props.scriptHash} readOnly />
          </Col>
        </Row>

        <Row style={{ marginBottom: '5px' }}>
          <Col xs={2}><ControlLabel>Token Name</ControlLabel></Col>
          <Col xs={4}>
            <FormControl type="text" value={this.state.tokenName} readOnly />
          </Col>
          <Col xs={2}><ControlLabel>Token Symbol</ControlLabel></Col>
          <Col xs={4}>
            <FormControl type="text" value={this.state.tokenSymbol} readOnly />
          </Col>
        </Row>

        <Row style={{ marginBottom: '5px' }}>
          <Col xs={2}><ControlLabel>Total Supply</ControlLabel></Col>
          <Col xs={4}>
            <FormControl type="text" value={this.state.totalSupply} readOnly />
          </Col>
          {/* <Col xs={2}><ControlLabel>Circulation</ControlLabel></Col>
          <Col xs={4}>
            <FormControl type="text" value={this.state.circulation} readOnly />
          </Col> */}
        </Row>
      </Grid>
    )
  }
}

TokenInfo.propTypes = {
  onNetworkSelected: PropTypes.func.isRequired,
  scriptHash: PropTypes.string.isRequired,
};

export default TokenInfo;
