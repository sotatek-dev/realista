from ret.token.kyc import get_kyc_status
from boa.builtins import concat
from boa.interop.Neo.Storage import Get, Put
from boa.interop.Neo.Action import RegisterAction
from ret.common.other import *

OnAffiliate = RegisterAction('affiliate', 'sender_addr', 'referer_addr', 'amount')

AFFILIATE_MAX_CAP = 13625000 * 100000000 # 13.625M
AFFILIATE_RATE = 25 # divide 1000 = 2.5%


def do_affiliate(ctx, sender_addr, amount):

    referrer_addr = get_referrer(ctx, sender_addr)
    if not referrer_addr:
        return False

    if not get_kyc_status(ctx, referrer_addr):
        return False

    amount = amount * AFFILIATE_RATE / 1000

    '''
        Check affiliate tokens
    '''
    if get_balance(ctx, AFFILIATE_FUNDS_ADDRESS) < amount:
        return False

    affiliated_tokens = get_affiliated_tokens(ctx)

    new_affiliated_tokens = amount + affiliated_tokens

    if new_affiliated_tokens > AFFILIATE_MAX_CAP:
        return False

    add_balance(ctx, referrer_addr, amount)
    sub_balance(ctx, AFFILIATE_FUNDS_ADDRESS, amount)
    add_affiliated_tokens(ctx, amount)
    
    OnAffiliate(sender_addr, referrer_addr, amount)
    
    return True
