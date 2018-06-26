from ret.token.rettoken import *
from boa.interop.Neo.Storage import *

def get_config(ctx, config_name):
    return storage_get(ctx, config_name, STORAGE_PREFIX_CONFIG)


def set_config(ctx, config_name, config_value):
    return storage_put(ctx, config_name, config_value, STORAGE_PREFIX_CONFIG)


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