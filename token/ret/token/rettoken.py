"""
Basic settings for an NEP5 Token and crowdsale
"""

from boa.interop.Neo.Storage import *

TOKEN_NAME = 'Realista'

TOKEN_SYMBOL = 'RET'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the walet open, use ``wallet`` command
TOKEN_OWNER = b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)'
ECOSYSTEM_RESERVE_ADDRESS = b'\xb8\x8b\xb9\xa9Bd\x11\xf3\xc8\x01\x06VR\xf2\x12"\x15z]\xc6'
ADVISOR_FUNDS_ADDRESS = b'\xb8\x8b\xb9\xa9Bd\x11\xf3\xc8\x01\x06VR\xf2\x12"\x15z]\xc6'
EMPLOYEE_FUNDS_ADDRESS1 = b'\xb8\x8b\xb9\xa9Bd\x11\xf3\xc8\x01\x06VR\xf2\x12"\x15z]\xc6'
EMPLOYEE_FUNDS_ADDRESS2 = b'\xb8\x8b\xb9\xa9Bd\x11\xf3\xc8\x01\x06VR\xf2\x12"\x15z]\xc6'
RESERVE_FUNDS_ADDRESS = b'\xb8\x8b\xb9\xa9Bd\x11\xf3\xc8\x01\x06VR\xf2\x12"\x15z]\xc6'

TOKEN_CIRC_KEY = b'in_circulation'

KYC_KEY = b'kyc_ok'

DEBUG_FLAG = True

TOKEN_TOTAL_SUPPLY = 1000000000 * 100000000  # 1b total supply * 10^8 ( decimals)

TOKEN_ECOSYSTEM_AMOUNT = 100000000 * 100000000 # 100m locked for 3 months

TOKEN_INITIAL_AMOUNT = 20000000 * 100000000  # 20m for bounty and airdrop

TOKEN_ADVISOR_AMOUNT = 20000000 * 100000000 # 20m locked for 3 months

TOKEN_EMPLOYEES_AMOUNT_1 = 22500000 * 100000000 # 22.5m locked for 1 year

TOKEN_EMPLOYEES_AMOUNT_2 = 22500000 * 100000000 # 22.5m locked for 2 year

TOKEN_RESERVE_AMOUNT = 186375000 * 100000000 # 186.375m locked for 1 year

VALID_CONFIGS = ['WHITELIST_SALE_BEGIN', 'WHITELIST_SALE_END', 'WHITELIST_SALE_RATE', 'WHITELIST_WHOLESALE_RATE', 'PRESALE_BEGIN', 'PRESALE_END', 'PRESALE_RATE', 'CROWDSALE_BEGIN', 'CROWDSALE_WEEK1_RATE', 'CROWDSALE_WEEK2_RATE', 'CROWDSALE_WEEK3_RATE', 'CROWDSALE_WEEK4_RATE']


def crowdsale_available_amount(ctx):
    """

    :return: int The amount of tokens left for sale in the crowdsale
    """

    in_circ = Get(ctx, TOKEN_CIRC_KEY)

    available = TOKEN_TOTAL_SUPPLY - in_circ

    return available


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation

    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount
    Put(ctx, TOKEN_CIRC_KEY, current_supply)
    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return Get(ctx, TOKEN_CIRC_KEY)
