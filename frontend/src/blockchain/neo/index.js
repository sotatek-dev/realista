import Neon, { rpc } from '@cityofzion/neon-js';

const config = {
  name: 'PrivateNet',
  extra: {
    neoscan: 'http://localhost:4000/api/main_net'
  }
};

const privateNet = new rpc.Network(config);
Neon.add.network(privateNet);
