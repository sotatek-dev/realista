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
import { ToastContainer } from 'react-toastify';

import UserRequest from '../../request/UserRequest';
import store from '../../store'
import { logIn } from '../../actions'

const initialState = {
  email: '',
  password: '',
};

class LoginPage extends Component {
  constructor(props) {
    super(props);

    this.state = initialState;
  }

  handleChange (stateName, event) {
    const data = {};
    data[stateName] = event.target.value;
    this.setState(data);
  }

  submitLogin () {
    // const emailPattern = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    // if (!emailPattern.test(this.state.email)) {
    //   toast.error(`Valid email is required.`);
    //   return;
    // }

    UserRequest.login(this.state)
      .then(response => {
        this.setState(initialState);
        let user = response
        if(user && user.token) {
          localStorage.setItem('user', JSON.stringify(user))
          store.dispatch(logIn())
          this.props.history.push('/home')
        }
      })
      .catch(err => {
        toast.error(`Login failed with error: ${err}`);
      });
  }

  render () {
    return (
      <div>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnVisibilityChange
          draggable
          pauseOnHover
        />
        <h1>User Login</h1>
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
          <Row>
            <Col xs={12} >
              <Button bsStyle="primary" onClick={this.submitLogin.bind(this)} block>Login</Button>
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default LoginPage;