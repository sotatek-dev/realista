from ret.token.rettoken import *
from boa.interop.Neo.Storage import *
from boa.builtins import concat


def get_contributed_neo(ctx, address, sale_prefix):
    return storage_get(ctx, address, concat(sale_prefix, STORAGE_KEY_CONTRIBUTED_NEO))


def set_contributed_neo(ctx, sale_prefix, address, val):
    return storage_put(ctx, address, val, concat(sale_prefix, STORAGE_KEY_CONTRIBUTED_NEO))


def get_minted_tokens(ctx, sale_prefix):
    return storage_get(ctx, STORAGE_KEY_MINTED_TOKENS, sale_prefix)


def set_minted_token(ctx, sale_prefix, val):
    return storage_put(ctx, STORAGE_KEY_MINTED_TOKENS, val, sale_prefix)


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
