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
      users: []
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
  }

  render () {
    return (
      <div>
        <h1>User Page</h1>
        <Grid>
          <Row style={{ marginBottom: '5px', fontWeight: 'bold' }}>
            <Col xs={1}>{'ID'}</Col>
            <Col xs={3}>{'Full name'}</Col>
            <Col xs={3}>{'Email'}</Col>
            <Col xs={3}>{'NEO Address'}</Col>
            <Col xs={2}>{'Referral ID'}</Col>
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