from ret.token.rettoken import *
from boa.interop.Neo.Storage import *

STORAGE_PREFIX_BALANCE = b''
STORAGE_PREFIX_CONFIG = b'c'
STORAGE_PREFIX_WHITELIST_SALE = b'p1'
STORAGE_PREFIX_PRESALE = b'p2'
STORAGE_PREFIX_CROWDSALE = b'p3'

STORAGE_KEY_KYC = b'kyc'

VALID_CONFIGS = ['WHITELIST_SALE_BEGIN', 'WHITELIST_SALE_END', 'WHITELIST_SALE_RATE', 'WHITELIST_WHOLESALE_RATE', 'PRESALE_BEGIN', 'PRESALE_END', 'PRESALE_RATE', 'CROWDSALE_BEGIN', 'CROWDSALE_WEEK1_RATE', 'CROWDSALE_WEEK2_RATE', 'CROWDSALE_WEEK3_RATE', 'CROWDSALE_WEEK4_RATE']

def get_config(ctx, config_name):
    return storage_get(ctx, config_name, STORAGE_PREFIX_CONFIG)


def set_config(ctx, config_name, config_value):
    if config_name in VALID_CONFIGS:
        return storage_put(ctx, config_name, config_value, STORAGE_PREFIX_CONFIG)
    return False


def get_balance(ctx, address):
    return storage_get(ctx, address, STORAGE_PREFIX_BALANCE)


def set_balance(ctx, address, balance):
    return storage_put(ctx, address, balance, STORAGE_PREFIX_BALANCE)


def debug_log(msg):
    if not DEBUG_FLAG:
        return True

    print(msg)
    return True


def storage_get(ctx, key, prefix):
    storage_key = concat(prefix, key)
    return Get(ctx, storage_key)


def storage_put(ctx, key, val, prefix):
    storage_key = concat(prefix, key)
    return Put(ctx, storage_key, val)


def storage_delete(ctx, key, prefix):
    storage_key = concat(prefix, key)
    return Delete(ctx, storage_key)
