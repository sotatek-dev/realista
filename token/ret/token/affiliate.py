from ret.token.kyc import get_kyc_status
from boa.builtins import concat
from boa.interop.Neo.Storage import Get, Put
from boa.interop.Neo.Action import RegisterAction

OnAffiliate = RegisterAction('affiliate', 'addr_from', 'addr_to', 'amount')

AFFILIATE_MAX_CAP = 13625000 * 100000000 # 13.625M
AFFILIATE_RATE = 25 # divide 1000 = 2.5%
AFFILIATE_KEY = b'affiliate'


def do_affiliate(ctx, amount, sender, address):
    if len(address) != 20:
        return False

    if not get_kyc_status(ctx, address):
        return False

    amount = amount * AFFILIATE_RATE / 1000

    current_balance = Get(ctx, address)
    current_affiliate_balance = Get(ctx, AFFILIATE_KEY)

    new_amount = amount + current_affiliate_balance
    new_balance = amount + current_balance

    if new_amount > AFFILIATE_MAX_CAP:
        return False

    Put(ctx, AFFILIATE_KEY, new_amount)
    Put(ctx, address, new_balance)
    OnAffiliate(sender, address, amount)
    return True


def get_affiliate(ctx, address):
    return Get(ctx, AFFILIATE_KEY)
