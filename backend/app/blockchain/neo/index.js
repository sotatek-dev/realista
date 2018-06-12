const Neon  = require('@cityofzion/neon-js').default;
const rpc   = require('@cityofzion/neon-js').rpc;

const privateNetConfig = require('./network/PrivateNet');

Neon.add.network(new rpc.Network({
  name: privateNetConfig.name,
  extra: {
    neoscan: privateNetConfig.neoscan
  }
}));
