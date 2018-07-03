import React from 'react';
import { Route, Redirect } from 'react-router-dom';

export const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={props => (
    localStorage.getItem('user')
      ? <Component {...props} />
      : <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
  )} />
)

export const Logout = ({ component: Component, ...rest }) => (
  <Route {...rest} render={props => {
    localStorage.removeItem('user')
    return (<Redirect to={{ pathname: '/login', state: { from: props.location } }} />)
  }} />
)