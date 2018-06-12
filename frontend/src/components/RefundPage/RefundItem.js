import React from 'react';
import {
  Row,
  Col,
} from 'react-bootstrap';

import PropTypes from 'prop-types';

class RefundItem extends React.Component {
  render() {
    return (
      <Row style={{ marginBottom: '5px' }}>
        <Col xs={2}>{this.props.blockNumber}</Col>
        <Col xs={2}>{this.props.blockTimestamp}</Col>
        <Col xs={3}>{this.props.txid}</Col>
        <Col xs={2}>{this.props.address}</Col>
        <Col xs={2}>{this.props.amount}</Col>
        <Col xs={1}>{this.props.isRefunded}</Col>
      </Row>
    )
  }
}

RefundItem.propTypes = {
  blockNumber: PropTypes.number.isRequired,
  blockTimestamp: PropTypes.number.isRequired,
  txid: PropTypes.string.isRequired,
  address: PropTypes.string.isRequired,
  amount: PropTypes.number.isRequired,
  isRefunded: PropTypes.number.isRequired,
};

export default RefundItem;
