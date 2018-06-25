from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from ret.token.rettoken import *
from ret.common.txio import get_asset_attachments
from ret.common.time import get_now
from ret.token.affiliate import *

OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnRefund = RegisterAction('refund', 'addr_to', 'amount')

CROWDSALE_OPEN = 1509642040
CROWDSALE_CLOSE = 1509642040 + 86400 * 7 * 4
CROWDSALE_ROUND_KEY = b'in_crowdsale'
CROWDSALE_NEO_PERSONAL_KEY = b'crowdsale_neo'
CROWDSALE_MAX_CAP = 480000000 * 100000000 # 480M
CROWDSALE_WEEK1_RATE = 4000 * 100000000
CROWDSALE_WEEK2_RATE = 3833 * 100000000
CROWDSALE_WEEK3_RATE = 3666 * 100000000
CROWDSALE_WEEK4_RATE = 3500 * 100000000
CROWDSALE_PERSONAL_NEO_CAP = 500 * 100000000 # 500 NEO


def crowdsale_perform_exchange(ctx, args):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """

    attachments = get_asset_attachments()  # [receiver, sender, neo, gas]

    # this looks up whether the exchange can proceed
    exchange_ok = crowdsale_can_exchange(ctx, attachments, False)

    if not exchange_ok:
        # This should only happen in the case that there are a lot of TX on the final
        # block before the total amount is reached.  An amount of TX will get through
        # the verification phase because the total amount cannot be updated during that phase
        # because of this, there should be a process in place to manually refund tokens
        if attachments[2] > 0:
            OnRefund(attachments[1], attachments[2])
        # if you want to exchange gas instead of neo, use this
        # if attachments.gas_attached > 0:
        #    OnRefund(attachments.sender_addr, attachments.gas_attached)
        return False

    # lookup the current balance of the address
    current_balance = Get(ctx, attachments[1])

    personal_neo_key = concat(CROWDSALE_NEO_PERSONAL_KEY, attachments[1])
    round_balance = Get(ctx, CROWDSALE_ROUND_KEY)
    personal_neo_balance = Get(ctx, personal_neo_key)

    # calculate the amount of tokens the attached neo will earn
    exchanged_tokens = crowdsale_get_amount_requested(ctx, attachments[1], attachments[2])

    # if you want to exchange gas instead of neo, use this
    # exchanged_tokens += attachments[3] * TOKENS_PER_GAS / 100000000

    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_tokens + current_balance
    Put(ctx, attachments[1], new_total)

    new_personal_neo_total = attachments[2] + personal_neo_balance
    Put(ctx, personal_neo_key, new_personal_neo_total)

    new_round_total = exchanged_tokens + round_balance
    Put(ctx, CROWDSALE_ROUND_KEY, new_round_total)

    # update the in circulation amount
    result = add_to_circulation(ctx, exchanged_tokens)

    # dispatch transfer event
    OnTransfer(attachments[0], attachments[1], exchanged_tokens)

    if len(args) > 0:
        address = args[0]
        do_affiliate(ctx, exchanged_tokens, attachments[1], address)

    return True


def crowdsale_can_exchange(ctx, attachments, verify_only):
    """
    Determines if the contract invocation meets all requirements for the ICO exchange
    of neo or gas into NEP5 Tokens.
    Note: This method can be called via both the Verification portion of an SC or the Application portion

    When called in the Verification portion of an SC, it can be used to reject TX that do not qualify
    for exchange, thereby reducing the need for manual NEO or GAS refunds considerably

    :param attachments:Attachments An attachments object with information about attached NEO/Gas assets
    :return:
        bool: Whether an invocation meets requirements for exchange
    """

    # if you are accepting gas, use this
#        if attachments[3] == 0:
#            print("no gas attached")
#            return False

    # if youre accepting neo, use this

    if attachments[2] == 0:
        return False

    # caluclate the amount requested
    amount_requested = crowdsale_get_amount_requested(ctx, attachments[1], attachments[2])

    # this would work for accepting gas
    # amount_requested = attachments.gas_attached * token.tokens_per_gas / 100000000

    exchange_ok = crowdsale_calculate_can_exchange(ctx, attachments[2], amount_requested, attachments[1], verify_only)

    return exchange_ok


def crowdsale_calculate_can_exchange(ctx, neo_amount, amount, address, verify_only):
    """
    Perform custom token exchange calculations here.

    :param amount:int Number of tokens to convert from asset to tokens
    :param address:bytearray The address to mint the tokens to
    :return:
        bool: Whether or not an address can exchange a specified amount
    """
    now = get_now()

    current_in_circulation = Get(ctx, TOKEN_CIRC_KEY)
    
    round_balance = Get(ctx, CROWDSALE_ROUND_KEY)

    personal_neo_key = concat(CROWDSALE_NEO_PERSONAL_KEY, address)
    personal_neo_balance = Get(ctx, personal_neo_key)

    new_amount = current_in_circulation + amount
    new_round_amount = round_balance + amount
    new_personal_neo_amount = personal_neo_balance + neo_amount

    if now < CROWDSALE_OPEN:
        return False

    if new_amount > TOKEN_TOTAL_SUPPLY:
        return False

    if new_round_amount > CROWDSALE_MAX_CAP:
        return False

    if new_personal_neo_amount > CROWDSALE_PERSONAL_NEO_CAP:
        return False

    return True


def crowdsale_get_amount_requested(ctx, address, amount):
    now = get_now()
    rate = 0

    if now < CROWDSALE_OPEN:
        rate = 0
    elif now < CROWDSALE_OPEN + 86400 * 7:
        rate = CROWDSALE_WEEK1_RATE
    elif now < CROWDSALE_OPEN + 86400 * 7 * 2:
        rate = CROWDSALE_WEEK2_RATE
    elif now < CROWDSALE_OPEN + 86400 * 7 * 3:
        rate = CROWDSALE_WEEK3_RATE
    elif now <= CROWDSALE_CLOSE:
        rate = CROWDSALE_WEEK4_RATE
    else:
        rate = 0
    
    amount_requested = amount * rate / 100000000

    return amount_requested
