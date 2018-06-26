from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from ret.token.rettoken import *
from ret.common.txio import get_asset_attachments
from ret.common.time import get_now
from ret.token.affiliate import *
from ret.common.other import *

OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnRefund = RegisterAction('refund', 'addr_to', 'amount')

CROWDSALE_MAX_CAP = 480000000 * 100000000 # 480M
CROWDSALE_PERSONAL_CAP = 500 * 100000000 # 500 NEO


def crowdsale_perform_exchange(ctx):
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

    minted_tokens = get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_CROWDSALE)
    contributed_neo = get_contributed_neo(ctx, attachments[1], STORAGE_PREFIX_PURCHASED_CROWDSALE)

    # calculate the amount of tokens the attached neo will earn
    exchanged_tokens = crowdsale_get_amount_requested(ctx, attachments[1], attachments[2])

    # if you want to exchange gas instead of neo, use this
    # exchanged_tokens += attachments[3] * TOKENS_PER_GAS / 100000000

    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_tokens + current_balance
    Put(ctx, attachments[1], new_total)

    new_minted_tokens = exchanged_tokens + minted_tokens
    set_minted_token(ctx, STORAGE_PREFIX_PURCHASED_CROWDSALE, new_minted_tokens)
    
    new_contributed_neo = attachments[2] + contributed_neo
    set_contributed_neo(ctx, STORAGE_PREFIX_PURCHASED_CROWDSALE, attachments[1], new_contributed_neo)

    # update the in circulation amount
    result = add_to_circulation(ctx, exchanged_tokens)

    # dispatch transfer event
    OnTransfer(attachments[0], attachments[1], exchanged_tokens)

    affiliate = do_affiliate(ctx, attachments[1], exchanged_tokens)

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

    current_in_circulation = Get(ctx, STORAGE_KEY_CIRCULATION)
    
    minted_tokens = get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_CROWDSALE)
    contributed_neo = get_contributed_neo(ctx, address, STORAGE_PREFIX_PURCHASED_CROWDSALE)

    new_amount = current_in_circulation + amount
    new_minted_tokens = minted_tokens + amount
    new_contributed_neo = contributed_neo + neo_amount

    if new_amount > TOKEN_TOTAL_SUPPLY:
        return False

    if new_minted_tokens > CROWDSALE_MAX_CAP:
        return False

    if new_contributed_neo > CROWDSALE_PERSONAL_CAP:
        return False

    return True


def crowdsale_get_amount_requested(ctx, address, neo_amount):
    now = get_now()
    CROWDSALE_OPEN = get_config(ctx, 'CROWDSALE_OPEN')
    CROWDSALE_CLOSE = CROWDSALE_OPEN + 86400 * 4 * 7
    CROWDSALE_WEEK1_RATE = get_config(ctx, 'CROWDSALE_WEEK1_RATE')
    CROWDSALE_WEEK2_RATE = get_config(ctx, 'CROWDSALE_WEEK2_RATE')
    CROWDSALE_WEEK3_RATE = get_config(ctx, 'CROWDSALE_WEEK3_RATE')
    CROWDSALE_WEEK4_RATE = get_config(ctx, 'CROWDSALE_WEEK4_RATE')
    rate = 1

    if now < CROWDSALE_OPEN:
        rate = 1
    elif now < CROWDSALE_OPEN + 86400 * 7:
        rate = CROWDSALE_WEEK1_RATE
    elif now < CROWDSALE_OPEN + 86400 * 7 * 2:
        rate = CROWDSALE_WEEK2_RATE
    elif now < CROWDSALE_OPEN + 86400 * 7 * 3:
        rate = CROWDSALE_WEEK3_RATE
    elif now <= CROWDSALE_CLOSE:
        rate = CROWDSALE_WEEK4_RATE
    else:
        rate = 1
    
    amount_requested = neo_amount * rate / 100000000

    return amount_requested
