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
ECOSYSTEM_RESERVE_ADDRESS = b'BU\xbbKt\xae\xe6\xb0f\xbc\x08\x80*\xe5\x96%\xcb\x04X0'
ADVISOR_FUNDS_ADDRESS = b'\xa6\xc5\x9d\xeb\xf0\xd7(\xbd\x14\x89\xcd\xb9\xd9{\xd1\x90\xcb\x0b\xdch'
EMPLOYEE_FUNDS_ADDRESS1 = b'\xb8\x8b\xb9\xa9Bd\x11\xf3\xc8\x01\x06VR\xf2\x12"\x15z]\xc6'
EMPLOYEE_FUNDS_ADDRESS2 = b'\x04\x00\xff\xe8I\xfd\x9f\xcep-N\x88\x12\xba\xe9\xa2\x1d\t\x17U'
RESERVE_FUNDS_ADDRESS = b'\xe2\xacd\x1ep)\x1f\xe3V\x88\xdbG\x19\xe6X\\\xe7\xa5\xcfk'
AFFILIATE_FUNDS_ADDRESS = b'\xaaJ\x12\xdf\xf8&U\xd5\xd1\x9e\xe6\xb2V\xe6\x1c\xa5\xe7*\xa10'
SALE_FUNDS_ADDRESS = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'

STORAGE_PREFIX_BALANCE = b'';
STORAGE_PREFIX_CONFIG = b'c';
STORAGE_PREFIX_LOCK = b'l';
STORAGE_PREFIX_PURCHASED_WHITELIST = b'p1'
STORAGE_PREFIX_PURCHASED_PRESALE = b'p2'
STORAGE_PREFIX_PURCHASED_CROWDSALE = b'p3'
STORAGE_PREFIX_REFERRER = b'r'
STORAGE_PREFIX_OTHER = b'o'

STORAGE_KEY_KYC = b'kyc_ok'
STORAGE_KEY_CIRCULATION = b'in_circulation'
STORAGE_KEY_CONTRIBUTED_NEO = b'contributed_neo'
STORAGE_KEY_MINTED_TOKENS = b'minted_tokens'
STORAGE_KEY_AFFILIATED_TOKENS = b'affiliated_tokens'

DEBUG_FLAG = True

TOKEN_TOTAL_SUPPLY = 1000000000 * 100000000  # 1b total supply * 10^8 ( decimals)

TOKEN_ECOSYSTEM_AMOUNT = 100000000 * 100000000 # 100m locked for 3 months

TOKEN_INITIAL_AMOUNT = 20000000 * 100000000  # 20m for bounty and airdrop

TOKEN_ADVISOR_AMOUNT = 20000000 * 100000000 # 20m locked for 3 months

TOKEN_EMPLOYEES_AMOUNT_1 = 22500000 * 100000000 # 22.5m locked for 1 year

TOKEN_EMPLOYEES_AMOUNT_2 = 22500000 * 100000000 # 22.5m locked for 2 year

TOKEN_RESERVE_AMOUNT = 186375000 * 100000000 # 186.375m locked for 1 year

TOKEN_AFFILIATE_AMOUNT = 13625000 * 100000000 # 13.625m for affiliate

TOKEN_SALE_AMOUNT = 615000000 * 100000000 # 615m for sale


def crowdsale_available_amount(ctx):
    """

    :return: int The amount of tokens left for sale in the crowdsale
    """

    in_circ = Get(ctx, STORAGE_KEY_CIRCULATION)

    available = TOKEN_TOTAL_SUPPLY - in_circ

    return available


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation

    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, STORAGE_KEY_CIRCULATION)

    current_supply += amount
    Put(ctx, STORAGE_KEY_CIRCULATION, current_supply)
    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation

    :return:
        int: Total amount in circulation
    """
    return Get(ctx, STORAGE_KEY_CIRCULATION)
