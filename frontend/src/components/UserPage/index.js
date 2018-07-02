import React, { Component } from 'react';
import {
  Row,
  Col,
  Grid,
} from 'react-bootstrap';
import UserItem from './UserItem';
import UserRequest from '../../request/UserRequest';

class UserPage extends Component {

  constructor(props) {
    super(props);

    this.state = {
      users: [],
      network: 'PrivateNet',
      scriptHash: 'd4c3af978aa357b1cb77d104d1ac1cde73397aab',
    };
  }

  componentDidMount () {
    UserRequest.getList()
      .then(response => {
        this.setState({
          users: response
        });
      })
      .catch(err => {
        console.error(err);
      })

    UserRequest.getKycStatus({
      network: this.state.network,
      scriptHash: this.state.scriptHash,
      address: 'AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y'
    })
      .then(response => {
        console.log(response)
      })
      .catch(err => {
        console.error(err);
      })
  }

  render () {
    return (
      <div>
        <h1>User Page</h1>
        <Grid>
          <Row style={{ marginBottom: '5px', fontWeight: 'bold' }}>
            <Col xs={1}>{'ID'}</Col>
            <Col xs={2}>{'Full name'}</Col>
            <Col xs={2}>{'Email'}</Col>
            <Col xs={2}>{'NEO Address'}</Col>
            <Col xs={2}>{'Referral ID'}</Col>
            <Col xs={3}>{'Status'}</Col>
          </Row>
          {this.state.users.map(user => (
            <UserItem
              key={user.id}
              id={user.id}
              fullName={user.fullName}
              email={user.email}
              neoAddress={user.neoAddress}
              referralId={user.referralId}
              referrerId={user.referrerId} />
          ))}
        </Grid>
      </div>
    );
  }
}

export default UserPage;