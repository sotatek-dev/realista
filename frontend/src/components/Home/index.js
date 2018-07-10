import React from 'react';
import TokenInfo from './TokenInfo';
import TokenConfigsList from './TokenConfigsList';

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      network: '',
      scriptHash: 'fdb94040d3578817cc9293f95b8ddae75d87ac57',
    };
  }

  onNetworkSelected (network) {
    this.setState({ network });
  }

  render() {
    return (
      <div>
        <h1>Basic Info</h1>
        <TokenInfo onNetworkSelected={this.onNetworkSelected.bind(this)} scriptHash={this.state.scriptHash} />
        <hr />
        <h1>Update Config</h1>
        <TokenConfigsList network={this.state.network} scriptHash={this.state.scriptHash} />
      </div>
    )
  }
}

export default Home;
