import React, { Component } from 'react';
import {
  Row,
  Col,
  Grid,
} from 'react-bootstrap';
import UserItem from './RefundItem';
import UserRequest from '../../request/UserRequest';

class RefundPage extends Component {

  constructor(props) {
    super(props);

    this.state = {
      items: []
    };
  }

  componentDidMount () {
    UserRequest.getRefundList()
      .then(response => {
        this.setState({
          items: response
        });
      })
      .catch(err => {
        console.error(err);
      })
  }

  render () {
    return (
      <div>
        <h1>Refund Page</h1>
        <Grid>
          <Row style={{ marginBottom: '5px', fontWeight: 'bold' }}>
            <Col xs={2}>Block Number</Col>
            <Col xs={2}>Timestamp</Col>
            <Col xs={3}>TXID</Col>
            <Col xs={2}>Address</Col>
            <Col xs={2}>Amount</Col>
            <Col xs={1}>Refunded</Col>
          </Row>
          {this.state.items.map(item => (
            <UserItem
              key={item.id}
              blockNumber={item.blockNumber}
              blockTimestamp={item.blockTimestamp}
              txid={item.txid}
              address={item.address}
              amount={item.amount}
              isRefunded={item.isRefunded} />
          ))}
        </Grid>
      </div>
    );
  }
}

export default RefundPage;