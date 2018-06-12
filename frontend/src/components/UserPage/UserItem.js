import React from 'react';
import {
  Row,
  Col,
} from 'react-bootstrap';

import PropTypes from 'prop-types';

class UserItem extends React.Component {
  render() {
    return (
      <Row style={{ marginBottom: '5px' }}>
        <Col xs={1}>{this.props.id}</Col>
        <Col xs={3}>{this.props.fullName}</Col>
        <Col xs={3}>{this.props.email}</Col>
        <Col xs={3}>{this.props.neoAddress}</Col>
        <Col xs={2}>{this.props.referralId}</Col>
      </Row>
    )
  }
}

UserItem.propTypes = {
  id: PropTypes.number.isRequired,
  fullName: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
  neoAddress: PropTypes.string.isRequired,
  referralId: PropTypes.string.isRequired,
  referrerId: PropTypes.string,
};

export default UserItem;
