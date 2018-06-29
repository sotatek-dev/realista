require('./index');

const _             = require('lodash');
const Neon          = require('@cityofzion/neon-js').default;
const api           = require('@cityofzion/neon-js').api;
const rpc           = require('@cityofzion/neon-js').rpc;
const sc            = require('@cityofzion/neon-js').sc;
const tx            = require('@cityofzion/neon-js').tx;
const wallet        = require('@cityofzion/neon-js').wallet;
const utils         = require('@cityofzion/neon-js').u;
const CONST         = require('@cityofzion/neon-js').CONST;
const settings      = require('@cityofzion/neon-js').settings;
const networkConfig = require('./network');
const logger        = require('sota-core').getLogger('nep5');

/**
 * Extract utility functions from modules
 */
const ScriptBuilder = sc.ScriptBuilder;
const getScriptHashFromAddress = wallet.getScriptHashFromAddress;
const Account = wallet.Account;
const Query = rpc.Query;
const VMZip = rpc.VMZip;
const reverseHex = utils.reverseHex;
const str2hexstring = utils.str2hexstring;
const hexstring2str = utils.hexstring2str;
const ab2hexstring = utils.ab2hexstring;
const num2hexstring = utils.num2hexstring;
const str2ab = utils.str2ab;
const Transaction = tx.Transaction;
const ASSET_ID = CONST.ASSET_ID;

/**
 * Parses the VM output for decimals.
 * The VM returns an integer for most cases
 * but it can be an empty string for zero.
 */
const parseDecimals = (_vmOutput) => {
  if (_vmOutput === '') {
    return 0;
  }

  return parseInt(_vmOutput, 10);
}

/**
 * Convert hex number to integer
 */
const parseHexNumber = (hex) => {
  if (!hex) {
    return 0;
  }

  return parseInt(reverseHex(hex), 16);
}

const parseBoolean = (hex) => {
  if (!hex) {
    return false;
  }

  logger.info(hex)

  return parseInt(reverseHex(hex), 16) > 0;
}

const parseTokenInfoAndBalance = VMZip(hexstring2str, hexstring2str, parseDecimals, parseHexNumber, parseHexNumber)

const getTokenInfo = (network, scriptHash) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);

  sb.emitAppCall(scriptHash, 'name')
    .emitAppCall(scriptHash, 'symbol')
    .emitAppCall(scriptHash, 'decimals')
    .emitAppCall(scriptHash, 'totalSupply')
    // .emitAppCall(scriptHash, 'circulation');

  return Query
    .invokeScript(sb.str, false)
    .parseWith(VMZip(hexstring2str, hexstring2str, parseDecimals, parseHexNumber))
    .execute(rpcUrl)
    .then((res) => {
      return {
        name: res[0],
        symbol: res[1],
        decimals: res[2],
        totalSupply: res[3] / Math.pow(10, res[2]),
        // circulation: res[4] / Math.pow(10, res[2]),
      }
    })
    .catch((err) => {
      logger.error(`nep5.getTokenInfo failed with error: ${err.message}`);
      throw err;
    });
}

const getBalance = (network, scriptHash, address) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);
  const addrScriptHash = reverseHex(getScriptHashFromAddress(address));

  sb.emitAppCall(scriptHash, 'decimals')
    .emitAppCall(scriptHash, 'balanceOf', [addrScriptHash]);

  return Query.invokeScript(sb.str, false)
    .execute(rpcUrl)
    .then((res) => {
      try {
        const decimals = parseDecimals(res.result.stack[0].value);
        return parseHexNumber(res.result.stack[1].value) / Math.pow(10, decimals);
      } catch (err) {
        logger.error(`nep5.getBalance parse number error: ${err}`);
        return 0;
      }
    })
    .catch((err) => {
      logger.error(`nep5.getBalance failed with error: ${err.message}`);
      throw err;
    });
}

const getConfigValue = (network, scriptHash, configName) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);
  const hexedConfigName = ab2hexstring(str2ab(configName));

  sb.emitAppCall(scriptHash, 'get_config', [hexedConfigName]);

  return Query
    .invokeScript(sb.str, false)
    .parseWith(VMZip(parseHexNumber))
    .execute(rpcUrl)
    .then((res) => {
      return res[0];
    })
    .catch((err) => {
      logger.error(`nep5.getConfigValue failed with error: ${err.message}`);
      throw err;
    });
}

const setConfigValue = (network, scriptHash, wif, configName, configValue) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);
  const hexedConfigName = ab2hexstring(str2ab(configName));
  const hexedConfigValue = utils.num2hexstring(parseInt(configValue), 8, true); // little endian
  const account = new Account(wif);

  const script = Neon.create.script({
    scriptHash: scriptHash,
    operation: 'set_config',
    args: [hexedConfigName, hexedConfigValue]
  });

  return Neon.doInvoke({
    net: network,
    script,
    address: account.address,
    privateKey: account.privateKey,
    gas: 0
  }).then(res => {
    logger.fatal(res.response);
    return res.response;
  });
}

const setConfigValue2 = (network, scriptHash, wif, configName, configValue) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);
  const hexedConfigName = ab2hexstring(str2ab(configName));
  const hexedConfigValue = utils.num2hexstring(parseInt(configValue));
  const account = new Account(wif);

  return api.neoscan.getBalance(network, account.address)
    .then(balances => {

      const operation = 'set_config';
      const args = [hexedConfigName, hexedConfigValue];
      const invoke = {
        scriptHash,
        operation,
        args,
      };

      const ownerScriptHash = wallet.getScriptHashFromAddress(account.address);
      const intents = [
        { assetId: CONST.ASSET_ID.GAS, value: 0.00000001, scriptHash: ownerScriptHash }
      ];

      const unsignedTx = Transaction.createInvocationTx(balances, intents, invoke, 0, { version: 1 });
      return unsignedTx.sign(account.privateKey);
    })
    .then(signedTx => {
      return Query.sendRawTransaction(signedTx).execute(rpcUrl);
    })
    .then(ret => {
      logger.info(`nep5.setConfigValue [${configName}:${configValue}] result: ${JSON.stringify(ret)}`);
      return ret;
    });
}

const doTransfer = (network, scriptHash, fromWif, toAddress, amount) => {
  // Implement me
}

const getKycStatus = (network, scriptHash, address) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);
  const addrScriptHash = reverseHex(getScriptHashFromAddress(address));

  sb.emitAppCall(scriptHash, 'kyc_status', [addrScriptHash]);

  return Query
    .invokeScript(sb.str, false)
    .parseWith(VMZip(parseBoolean))
    .execute(rpcUrl)
    .then((res) => {
      return {
        status: res[0]
      }
    })
    .catch((err) => {
      logger.error(`nep5.getKycStatus failed with error: ${err.message}`);
      throw err;
    });
}

const KycReject = (network, scriptHash, wif, address) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);
  const addrScriptHash = reverseHex(getScriptHashFromAddress(address));
  const account = new Account(wif);

  const script = Neon.create.script({
    scriptHash: scriptHash,
    operation: 'kyc_reject',
    args: [addrScriptHash]
  });

  return Neon.doInvoke({
    net: network,
    script,
    address: account.address,
    privateKey: account.privateKey,
    gas: 0
  }).then(res => {
    logger.fatal(res.response);
    return res.response;
  });
}

const KycRegister = (network, scriptHash, wif, address) => {
  const sb = new ScriptBuilder();
  const rpcUrl = _.sample(networkConfig[network].rpcEndpoints);
  const addrScriptHash = reverseHex(getScriptHashFromAddress(address));
  const account = new Account(wif);

  const script = Neon.create.script({
    scriptHash: scriptHash,
    operation: 'kyc_register',
    args: [addrScriptHash]
  });

  return Neon.doInvoke({
    net: network,
    script,
    address: account.address,
    privateKey: account.privateKey,
    gas: 0
  }).then(res => {
    logger.fatal(res.response);
    return res.response;
  });
}

module.exports = {
  getTokenInfo,
  getBalance,
  doTransfer,
  getConfigValue,
  setConfigValue,
  getKycStatus,
  KycRegister,
  KycReject
};
