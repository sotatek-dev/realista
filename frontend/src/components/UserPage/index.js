import React, { Component } from 'react';
import {
  Row,
  Col,
  Grid,
} from 'react-bootstrap';
import UserItem from './UserItem';
import UserRequest from '../../request/UserRequest';
import { toast } from 'react-toastify';

class UserPage extends Component {

  constructor(props) {
    super(props);

    this.state = {
      users: [],
      network: 'PrivateNet',
      scriptHash: 'd4c3af978aa357b1cb77d104d1ac1cde73397aab',
    };

    this.kycRegister = this.kycRegister.bind(this)
    this.kycReject = this.kycReject.bind(this)
  }

  async componentDidMount () {
    let users = await UserRequest.getList()
    
    for(let i = 0; i < users.length; i++) {
      try {
        let kyc = await UserRequest.getKycStatus({
          network: this.state.network,
          scriptHash: this.state.scriptHash,
          address: users[i].neoAddress
        })
        users[i].kyc = kyc.status
      } catch (err) {
        users[i].kyc = false
        continue
      }
    }
    
    this.setState({
      users
    })
  }

  async kycRegister(address) {
    try {
      let response = await UserRequest.kycRegister({
        network: this.state.network,
        scriptHash: this.state.scriptHash,
        address: address
      })
      if (response.result === true) {
        toast.info(`KYC Register [${address}] successful.`);
      }
    } catch (err) {
      toast.error(`KYC Register [${address}] failed.`);
    }
  }

  async kycReject(address) {
    try {
      let response = await UserRequest.kycReject({
        network: this.state.network,
        scriptHash: this.state.scriptHash,
        address: address
      })
      if (response.result === true) {
        toast.info(`KYC Reject [${address}] successful.`);
      }
    } catch (err) {
      toast.error(`KYC Reject [${address}] failed.`);
    }
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
            <Col xs={3}>{'Action'}</Col>
          </Row>
          {this.state.users.map(user => (
            <UserItem
              key={user.id}
              id={user.id}
              fullName={user.fullName}
              email={user.email}
              neoAddress={user.neoAddress}
              referralId={user.referralId}
              referrerId={user.referrerId}
              kyc={user.kyc}
              kycRegister={this.kycRegister}
              kycReject={this.kycReject} />
          ))}
        </Grid>
      </div>
    );
  }
}

export default UserPage;