import React from 'react';
import {
  Row,
  Col,
  Button
} from 'react-bootstrap';

import PropTypes from 'prop-types';

class UserItem extends React.Component {
  render() {
    return (
      <Row style={{ marginBottom: '5px' }}>
        <Col xs={1}>{this.props.id}</Col>
        <Col xs={2}>{this.props.fullName}</Col>
        <Col xs={2}>{this.props.email}</Col>
        <Col xs={2}>{this.props.neoAddress}</Col>
        <Col xs={2}>{this.props.referralId}</Col>
        <Col xs={3}>
          {this.button(this.props.kyc)}
        </Col>
      </Row>
    )
  }

  button(kyc) {
    if(!kyc) {
      return (<Button bsStyle="success" onClick={() => this.props.kycRegister(this.props.neoAddress)}>KYC Register</Button>)
    }
    return (<Button bsStyle="danger" onClick={() => this.props.kycReject(this.props.neoAddress)}>KYC Reject</Button>)
  }
}

UserItem.propTypes = {
  id: PropTypes.number.isRequired,
  fullName: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
  neoAddress: PropTypes.string.isRequired,
  referralId: PropTypes.string.isRequired,
  referrerId: PropTypes.string,
  kyc: PropTypes.bool
};

export default UserItem;
