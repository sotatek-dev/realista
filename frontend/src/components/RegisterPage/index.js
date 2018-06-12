import React, { Component } from 'react';
import {
  Grid,
  Row,
  Col,
  Button,
  FormControl,
  ControlLabel,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import UserRequest from '../../request/UserRequest';

const initialState = {
  email: '',
  password: '',
  password2: '',
  fullName: '',
  neoAddress: '',
  referrerId: '',
};

class RegisterPage extends Component {
  constructor(props) {
    super(props);

    this.state = initialState;
  }

  handleChange (stateName, event) {
    const data = {};
    data[stateName] = event.target.value;
    this.setState(data);
  }

  submitRegistration () {
    const emailPattern = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    if (!emailPattern.test(this.state.email)) {
      toast.error(`Valid email is required.`);
      return;
    }

    if (this.state.password !== this.state.password2) {
      toast.error(`Password does not match.`);
      return;
    }

    if (!this.state.fullName) {
      toast.error(`Full name is required.`);
      return;
    }

    if (!this.state.neoAddress) {
      toast.error(`NEO address is required.`);
      return;
    }

    UserRequest.register(this.state)
      .then(response => {
        toast.info(`Registration success. User ID is: ${response.id}`);
        this.setState(initialState);
      })
      .catch(err => {
        toast.error(`Registration failed with error: ${err}`);
      });
  }

  render () {
    return (
      <div>
        <h1>User Registration</h1>
        <Grid>
          <Row style={{ marginBottom: '5px' }}>
            <Col xs={3}><ControlLabel>Email</ControlLabel></Col>
            <Col xs={9}>
              <FormControl
                type="text"
                value={this.state.email}
                onChange={this.handleChange.bind(this, 'email')} />
            </Col>
          </Row>
          <Row style={{ marginBottom: '5px' }}>
            <Col xs={3}><ControlLabel>Password</ControlLabel></Col>
            <Col xs={9}>
              <FormControl
                type="password"
                value={this.state.password}
                onChange={this.handleChange.bind(this, 'password')} />
            </Col>
          </Row>
          <Row style={{ marginBottom: '5px' }}>
            <Col xs={3}><ControlLabel>Confirm Password</ControlLabel></Col>
            <Col xs={9}>
              <FormControl
                type="password"
                value={this.state.password2}
                onChange={this.handleChange.bind(this, 'password2')} />
            </Col>
          </Row>
          <Row style={{ marginBottom: '5px' }}>
            <Col xs={3}><ControlLabel>Name</ControlLabel></Col>
            <Col xs={9}>
              <FormControl
                type="text"
                value={this.state.fullName}
                onChange={this.handleChange.bind(this, 'fullName')} />
            </Col>
          </Row>
          <Row style={{ marginBottom: '5px' }}>
            <Col xs={3}><ControlLabel>NEO Address</ControlLabel></Col>
            <Col xs={9}>
              <FormControl
                type="text"
                value={this.state.neoAddress}
                onChange={this.handleChange.bind(this, 'neoAddress')} />
            </Col>
          </Row>
          <Row style={{ marginBottom: '5px' }}>
            <Col xs={3}><ControlLabel>Referrer ID</ControlLabel></Col>
            <Col xs={9}>
              <FormControl
                type="text"
                value={this.state.referrerId}
                onChange={this.handleChange.bind(this, 'referrerId')} />
            </Col>
          </Row>
          <Row>
            <Col xs={12} >
              <Button bsStyle="primary" onClick={this.submitRegistration.bind(this)} block>Register</Button>
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default RegisterPage;