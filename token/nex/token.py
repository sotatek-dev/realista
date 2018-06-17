"""
Basic settings for an NEP5 Token and crowdsale
"""

from boa.interop.Neo.Storage import *
from boa.builtins import concat

TOKEN_NAME = 'Realista Token'
TOKEN_SYMBOL = 'RET'
TOKEN_DECIMALS = 8
DECIMAL_FACTOR = 100000000
DEBUG_FLAG = True

# This is the script hash of the address for the owner of the token
TOKEN_OWNER = b'\x9e\x95\xb6\x93\xb8nv\x95TU\xc6*\xea\x01\\}\x17\x1dv\x98'
ECOSYSTEM_RESERVE_ADDRESS = b'\x9e\x95\xb6\x93\xb8nv\x95TU\xc6*\xea\x01\\}\x17\x1dv\x98'
ADVISOR_FUNDS_ADDRESS = b'\x9e\x95\xb6\x93\xb8nv\x95TU\xc6*\xea\x01\\}\x17\x1dv\x98'
EMPLOYEE_FUNDS_ADDRESS1 = b'\x9e\x95\xb6\x93\xb8nv\x95TU\xc6*\xea\x01\\}\x17\x1dv\x98'
EMPLOYEE_FUNDS_ADDRESS2 = b'\x9e\x95\xb6\x93\xb8nv\x95TU\xc6*\xea\x01\\}\x17\x1dv\x98'
RESERVE_FUNDS_ADDRESS = b'\x9e\x95\xb6\x93\xb8nv\x95TU\xc6*\xea\x01\\}\x17\x1dv\x98'

"""
# Fixed parameters, accordings to the whitepaper
"""
TOKEN_TOTAL_SUPPLY = 1000000000 * 100000000 # Total supply is 1 billions

# Pre-minted non-locked tokens for reserves
# Will be granted to token owner at the initialization:
# - 10,000,000 tokens for bounty & bonus programs
# - 10,000,000 tokens for Airdrop programs
TOKEN_INITIAL_AMOUNT = 20000000 * 100000000
# 100M tokens reserved for ecosystem will be locked for 3 months
ECOSYSTEM_RESERVE_AMOUNT = 100000000 * 100000000
# 20M tokens for advisors will be locked for 3 months
ADVISOR_FUNDS_AMOUNT = 20000000 * 100000000
# 22.5M tokens for employees will be locked for 1 year
EMPLOYEE_FUNDS_AMOUNT1 = 22500000 * 100000000
# 22.5M tokens for employees will be locked for 2 years
EMPLOYEE_FUNDS_AMOUNT2 = 22500000 * 100000000
# 186.375M tokens in reserves will be locked for 1 year
RESERVE_FUNDS_AMOUNT = 186375000 * 100000000

# Hard cap for whitelist sale is 70M tokens
WHITELIST_MAX_CAP = 70000000 * 100000000
# Hard cap for presale phase is 65M tokens
PRESALE_MAX_CAP = 65000000 * 100000000
# Hard cap for crowdsale phase is 480M tokens
CROWDSALE_MAX_CAP = 480000000 * 100000000

WHITELIST_WHOLESALE_THRESHOLD = 400 * 100000000
WHITELIST_PERSONAL_CAP = 500 * 100000000
PRESALE_PERSONAL_CAP = 250 * 100000000
CROWDSALE_PERSONAL_CAP = 500 * 100000000

AFFILIATE_RATE = 25 # thousandth

"""
# Constants
"""
DAY_IN_SECONDS = 24 * 3600
WEEK_IN_SECONDS = 7 * 24 * 3600
MONTH_IN_SECONDS = 30 * 24 * 3600
YEAR_IN_SECONDS = 365 * 24 * 3600

"""
Define prefix for different purposes of storage use.
Prevent storage injection
"""
STORAGE_PREFIX_BALANCE = b'b';
STORAGE_PREFIX_CONFIG = b'c';
STORAGE_PREFIX_LOCK = b'l';
STORAGE_PREFIX_KYC = b'k';
STORAGE_PREFIX_PURCHASED_WHITELIST = b'p1'
STORAGE_PREFIX_PURCHASED_PRESALE = b'p2'
STORAGE_PREFIX_PURCHASED_CROWDSALE = b'p3'
STORAGE_PREFIX_REFERRER = b'r'
STORAGE_PREFIX_OTHER = b'o'

STORAGE_KEY_CIRCULATION = b'in_circulation'
STORAGE_KEY_CONTRIBUTED_NEO = b'contributed_neo'
STORAGE_KEY_MINTED_TOKENS = b'minted_tokens'
STORAGE_KEY_AFFILIATED_TOKENS = b'affiliated_tokens'



# maximum amount you can mint in the limited round ( 500 neo/person * 40 Tokens/NEO * 10^8 )
MAX_EXCHANGE_LIMITED_ROUND = 500 * 40 * 100000000

# when to start the crowdsale
BLOCK_SALE_START = 755000

# when to end the initial limited round
LIMITED_ROUND_END = 755000 + 10000

LIMITED_ROUND_KEY = b'r1'



VALID_CONFIGS = ['WHITELIST_SALE_BEGIN', 'WHITELIST_SALE_END', 'WHITELIST_SALE_RATE', 'WHITELIST_WHOLESALE_RATE', 'PRESALE_BEGIN', 'PRESALE_END', 'PRESALE_RATE', 'CROWDSALE_BEGIN', 'CROWDSALE_WEEK1_RATE', 'CROWDSALE_WEEK2_RATE', 'CROWDSALE_WEEK3_RATE', 'CROWDSALE_WEEK4_RATE']

def debug_log(msg):
    if not DEBUG_FLAG:
        return True

    print(msg)
    return True

def get_referrer(ctx, address):
    return storage_get(ctx, address, STORAGE_PREFIX_REFERRER)


def set_referrer(ctx, args):
    if len(args) == 2:
        address = args[0]
        referrer = args[1]
        storage_put(ctx, address, referrer, STORAGE_PREFIX_REFERRER)
        return True

    return False


def get_balance(ctx, address):
    return storage_get(ctx, address, STORAGE_PREFIX_BALANCE)


def set_balance(ctx, address, balance):
    return storage_put(ctx, address, balance, STORAGE_PREFIX_BALANCE)


def add_balance(ctx, address, amount):
    old_balance = get_balance(ctx, address)
    new_balance = old_balance + amount
    return set_balance(address, new_balance)


def del_balance(ctx, address, balance):
    return storage_delete(ctx, address, balance, STORAGE_PREFIX_BALANCE)


def get_config(ctx, config_name):
    return storage_get(ctx, config_name, STORAGE_PREFIX_CONFIG)


def set_config(ctx, config_name, config_value):
    storage_put(ctx, config_name, config_value, STORAGE_PREFIX_CONFIG)
    return True


def storage_get(ctx, key, prefix):
    storage_key = concat(prefix, key)
    return Get(ctx, storage_key)


def storage_put(ctx, key, val, prefix):
    storage_key = concat(prefix, key)
    Put(ctx, storage_key, val)
    return True


def storage_delete(ctx, key, prefix):
    storage_key = concat(prefix, key)
    Delete(ctx, storage_key)
    return True


def get_minted_tokens(ctx):
    return storage_get(ctx, STORAGE_KEY_MINTED_TOKENS, STORAGE_PREFIX_OTHER)


def get_contributed_neo(ctx):
    return storage_get(ctx, STORAGE_KEY_CONTRIBUTED_NEO, STORAGE_PREFIX_OTHER)


def add_minted_tokens(ctx, amount_tokens, amount_neo):
    contributed_neo = get_contributed_neo(ctx)
    contributed_neo += amount_neo
    storage_put(ctx, STORAGE_KEY_CONTRIBUTED_NEO, contributed_neo, STORAGE_PREFIX_OTHER)

    minted_tokens = get_minted_tokens(ctx)
    minted_tokens += amount_tokens
    storage_put(ctx, STORAGE_KEY_MINTED_TOKENS, minted_tokens, STORAGE_PREFIX_OTHER)

    return add_to_circulation(ctx, amount_tokens)


def get_affiliated_tokens(ctx):
    return storage_get(ctx, STORAGE_KEY_AFFILIATED_TOKENS, STORAGE_PREFIX_OTHER)


def add_affiliated_tokens(ctx, amount):
    old_total = get_affiliated_tokens(ctx)
    new_total = old_total + amount
    return storage_put(ctx, STORAGE_KEY_AFFILIATED_TOKENS, new_total, STORAGE_PREFIX_OTHER)


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation

    :param amount: int the amount to add to circulation
    """

    current_supply = get_circulation(ctx)

    current_supply += amount

    storage_put(ctx, STORAGE_KEY_CIRCULATION, current_supply, STORAGE_PREFIX_OTHER)
    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return storage_get(ctx, STORAGE_KEY_CIRCULATION, STORAGE_PREFIX_OTHER)
