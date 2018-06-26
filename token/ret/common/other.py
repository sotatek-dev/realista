from ret.token.rettoken import *
from boa.interop.Neo.Storage import *
from boa.builtins import concat


def get_affiliated_tokens(ctx):
    return storage_get(ctx, STORAGE_KEY_AFFILIATED_TOKENS, STORAGE_PREFIX_OTHER)


def get_referrer(ctx, address):
    return storage_get(ctx, address, STORAGE_PREFIX_REFERRER)


def set_referrer(ctx, args):
    if len(args) == 2:
        address = args[0]
        referrer = args[1]
        storage_put(ctx, address, referrer, STORAGE_PREFIX_REFERRER)
        return True

    return False


def get_affiliated_tokens(ctx):
    return storage_get(ctx, STORAGE_KEY_AFFILIATED_TOKENS, STORAGE_PREFIX_OTHER)


def add_affiliated_tokens(ctx, amount):
    old_total = get_affiliated_tokens(ctx)
    new_total = old_total + amount
    return storage_put(ctx, STORAGE_KEY_AFFILIATED_TOKENS, new_total, STORAGE_PREFIX_OTHER)


def get_contributed_neo(ctx, address, sale_prefix):
    return storage_get(ctx, address, concat(sale_prefix, STORAGE_KEY_CONTRIBUTED_NEO))


def add_contributed_neo(ctx, sale_prefix, address, val):
    current_neo = get_contributed_neo(ctx, address, sale_prefix)
    new_neo = current_neo + val
    return storage_put(ctx, address, new_neo, concat(sale_prefix, STORAGE_KEY_CONTRIBUTED_NEO))


def get_minted_tokens(ctx, sale_prefix):
    return storage_get(ctx, STORAGE_KEY_MINTED_TOKENS, sale_prefix)


def add_minted_tokens(ctx, sale_prefix, val):
    current_tokens = get_minted_tokens(ctx, sale_prefix)
    new_tokens = current_tokens + val
    return storage_put(ctx, STORAGE_KEY_MINTED_TOKENS, new_tokens, sale_prefix)


def get_config(ctx, config_name):
    return storage_get(ctx, config_name, STORAGE_PREFIX_CONFIG)


def set_config(ctx, config_name, config_value):
    return storage_put(ctx, config_name, config_value, STORAGE_PREFIX_CONFIG)


def get_balance(ctx, address):
    return storage_get(ctx, address, STORAGE_PREFIX_BALANCE)


def add_balance(ctx, address, amount):
    current_balance = get_balance(ctx, address)
    new_balance = current_balance + amount
    return storage_put(ctx, address, new_balance, STORAGE_PREFIX_BALANCE)


def sub_balance(ctx, address, amount):
    current_balance = get_balance(ctx, address)
    if current_balance < amount:
        log = debug_log('insufficient funds')
        return False
    if current_balance == amount:
        return storage_delete(ctx, address, STORAGE_PREFIX_BALANCE)
    
    new_balance = current_balance - amount
    return storage_put(ctx, address, new_balance, STORAGE_PREFIX_BALANCE)


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
