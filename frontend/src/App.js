import React, { Component } from 'react';
import { Nav, NavItem } from 'react-bootstrap';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { LinkContainer } from 'react-router-bootstrap';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';
import Home from './components/Home';
import RegisterPage from './components/RegisterPage';
import LoginPage from './components/LoginPage';
import UserPage from './components/UserPage';
import ContributionPage from './components/ContributionPage';
import RefundPage from './components/RefundPage';
import { PrivateRoute, Logout } from './components/HelperComponent';

const TAB_IDS = {
  HOME              : 1,
  USER_LIST         : 2,
  CONTRIBUTION_LIST : 3,
  REFUND_LIST       : 4,
  REGISTER          : 5,
  LOGOUT            : 6,
};

class App extends Component {

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
        <Router>
          <div>
            <Nav bsStyle="tabs">
              <LinkContainer to="/home">
                <NavItem eventKey={TAB_IDS.HOME}>
                  Home
                </NavItem>
              </LinkContainer>
              <LinkContainer to="/users">
                <NavItem eventKey={TAB_IDS.USER_LIST}>
                  Users
                </NavItem>
              </LinkContainer>
              <LinkContainer to="/contributions">
                <NavItem eventKey={TAB_IDS.CONTRIBUTION_LIST}>
                  Contributions
                </NavItem>
              </LinkContainer>
              <LinkContainer to="/refunds">
                <NavItem eventKey={TAB_IDS.REFUND_LIST}>
                  Refunds
                </NavItem>
              </LinkContainer>
              <LinkContainer to="/register">
                <NavItem eventKey={TAB_IDS.REGISTER}>
                  Register
                </NavItem>
              </LinkContainer>
              <LinkContainer to="/logout">
                <NavItem eventKey={TAB_IDS.LOGOUT}>
                  Logout
                </NavItem>
              </LinkContainer>
            </Nav>

            <PrivateRoute exact path="/" component={Home}/>
            <PrivateRoute path="/home" component={Home}/>
            <PrivateRoute path="/users" component={UserPage}/>
            <PrivateRoute path="/contributions" component={ContributionPage}/>
            <PrivateRoute path="/refunds" component={RefundPage}/>
            <Route path="/register" component={RegisterPage}/>
            <Route path="/login" component={LoginPage}/>
            <PrivateRoute path="/logout" component={Logout}/>
          </div>
        </Router>
      </div>
    );
  }
}


export default App;
