import React, { Component } from 'react';
import { Nav, NavItem } from 'react-bootstrap';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { LinkContainer } from 'react-router-bootstrap';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';
import Home from './components/Home';
import RegisterPage from './components/RegisterPage';
import UserPage from './components/UserPage';
import ContributionPage from './components/ContributionPage';
import RefundPage from './components/RefundPage';

const TAB_IDS = {
  HOME              : 1,
  USER_LIST         : 2,
  CONTRIBUTION_LIST : 3,
  REFUND_LIST       : 4,
  REGISTER          : 5,
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
            </Nav>

            <Route exact path="/" component={Home}/>
            <Route path="/home" component={Home}/>
            <Route path="/users" component={UserPage}/>
            <Route path="/contributions" component={ContributionPage}/>
            <Route path="/refunds" component={RefundPage}/>
            <Route path="/register" component={RegisterPage}/>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
