from boa.interop.Neo.Runtime import CheckWitness, GetTime
from boa.interop.Neo.Action import RegisterAction
from ret.token.rettoken import *
from ret.common.txio import get_asset_attachments
from ret.token.affiliate import *
from ret.common.other import *

OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnRefund = RegisterAction('refund', 'addr_to', 'amount')

# STATE
IS_NOT_SALE = 0
IS_WHITELIST_SALE = 1
IS_PRESALE = 2
IS_CROWDSALE = 3

# HARD CONFIG
WHITELIST_SALE_MAX_CAP = 70000000 * 100000000 # 70M
WHITELIST_SALE_THRESHOLD = 400 * 100000000 # 400 NEO
WHITELIST_SALE_PERSONAL_CAP = 500 * 100000000 # 500 NEO

PRESALE_MAX_CAP = 65000000 * 100000000 # 65M
PRESALE_PERSONAL_CAP = 250 * 100000000 # 250 NEO

CROWDSALE_MAX_CAP = 480000000 * 100000000 # 480M
CROWDSALE_PERSONAL_CAP = 500 * 100000000 # 500 NEO

def perform_exchange(ctx):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """
    now = GetTime()
    attachments = get_asset_attachments()  # [receiver, sender, neo, gas]

    exchangeables = get_exchangeable(ctx, attachments[1], attachments[2], now)
    exchanged_tokens = exchangeables[0]

    if exchanged_tokens == 0:
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

    add_balance(ctx, attachments[1], exchanged_tokens)

    sale_prefix = None
    if state == IS_WHITELIST_SALE:
        sale_prefix = STORAGE_PREFIX_PURCHASED_WHITELIST
    if state == IS_PRESALE:
        sale_prefix = STORAGE_PREFIX_PURCHASED_PRESALE
    if state == IS_CROWDSALE:
        sale_prefix = STORAGE_PREFIX_PURCHASED_CROWDSALE

    mint_log = add_minted_tokens(ctx, sale_prefix, exchanged_tokens)
    neo_log = add_contributed_neo(ctx, sale_prefix, attachments[1], attachments[2])

    # update the in circulation amount
    result = add_to_circulation(ctx, exchanged_tokens)

    # dispatch transfer event
    OnTransfer(attachments[0], attachments[1], exchanged_tokens)

    affiliate = do_affiliate(ctx, attachments[1], exchanged_tokens)

    return True


def get_exchangeable(ctx, sender_addr, sent_amount_neo, sending_time):
    state = get_state(ctx, sending_time)

    if sent_amount_neo == 0 or state == IS_NOT_SALE:
        return [0, 0]

    if (state == IS_WHITELIST_SALE or state == IS_PRESALE) and not get_kyc_status(ctx, sender_addr):
        return [0, 0]

    exchanged_tokens = get_amount_requested(ctx, sender_addr, sent_amount_neo, state, sending_time)
    if exchanged_tokens == 0:
        return [0, 0]

    '''
        Check CAP
    '''
    if state == IS_WHITELIST_SALE:
        current_tokens = get_balance(ctx, sender_addr)
        current_round_tokens = get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_WHITELIST)
        current_round_neo = get_contributed_neo(ctx, sender_addr, STORAGE_PREFIX_PURCHASED_WHITELIST)

        if current_tokens + exchanged_tokens > TOKEN_TOTAL_SUPPLY or \
            current_round_tokens + exchanged_tokens > WHITELIST_SALE_MAX_CAP or \
            current_round_neo + sent_amount_neo > WHITELIST_SALE_PERSONAL_CAP:
            
            return [0, 0]
    
    if state == IS_PRESALE:
        current_tokens = get_balance(ctx, sender_addr)
        current_round_tokens = get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_PRESALE)
        current_round_neo = get_contributed_neo(ctx, sender_addr, STORAGE_PREFIX_PURCHASED_PRESALE)

        if current_tokens + exchanged_tokens > TOKEN_TOTAL_SUPPLY or \
            current_round_tokens + exchanged_tokens > PRESALE_MAX_CAP or \
            current_round_neo + sent_amount_neo > PRESALE_PERSONAL_CAP:
            
            return [0, 0]
        
    if state == IS_CROWDSALE:
        current_tokens = get_balance(ctx, sender_addr)
        current_round_tokens = get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_CROWDSALE)
        current_round_neo = get_contributed_neo(ctx, sender_addr, STORAGE_PREFIX_PURCHASED_CROWDSALE)

        if current_tokens + exchanged_tokens > TOKEN_TOTAL_SUPPLY or \
            current_round_tokens + exchanged_tokens > CROWDSALE_MAX_CAP or \
            current_round_neo + sent_amount_neo > CROWDSALE_PERSONAL_CAP:
            
            return [0, 0]
    
    return [exchanged_tokens, sent_amount_neo]


def get_amount_requested(ctx, address, neo_amount, state, sending_time):

    '''
        WHITELIST SALE
    '''
    if state == IS_WHITELIST_SALE:
        contributed_neo = get_contributed_neo(ctx, address, STORAGE_PREFIX_PURCHASED_WHITELIST)
        WHITELIST_SALE_RATE = get_config(ctx, 'WHITELIST_SALE_RATE')
        WHITELIST_SALE_UPPER_RATE = get_config(ctx, 'WHITELIST_SALE_UPPER_RATE')
        
        if contributed_neo >= WHITELIST_SALE_THRESHOLD:
            return neo_amount * WHITELIST_SALE_UPPER_RATE / 100000000
        
        if contributed_neo + neo_amount <= WHITELIST_SALE_THRESHOLD:
            return neo_amount * WHITELIST_SALE_RATE / 100000000

        low_rate = (WHITELIST_SALE_THRESHOLD - contributed_neo) * WHITELIST_SALE_RATE / 100000000
        high_rate = (contributed_neo + neo_amount - WHITELIST_SALE_THRESHOLD) * WHITELIST_SALE_UPPER_RATE / 100000000

        return low_rate + high_rate

    '''
        PRESALE
    '''
    if state == IS_PRESALE:
        PRESALE_RATE = get_config(ctx, 'PRESALE_RATE')
        amount_requested = neo_amount * PRESALE_RATE / 100000000
        return amount_requested
    
    '''
        CROWDSALE
    '''
    if state == IS_CROWDSALE:
        CROWDSALE_OPEN = get_config(ctx, 'CROWDSALE_OPEN')
        CROWDSALE_CLOSE = CROWDSALE_OPEN + 86400 * 4 * 7
        CROWDSALE_WEEK1_RATE = get_config(ctx, 'CROWDSALE_WEEK1_RATE')
        CROWDSALE_WEEK2_RATE = get_config(ctx, 'CROWDSALE_WEEK2_RATE')
        CROWDSALE_WEEK3_RATE = get_config(ctx, 'CROWDSALE_WEEK3_RATE')
        CROWDSALE_WEEK4_RATE = get_config(ctx, 'CROWDSALE_WEEK4_RATE')
        rate = 1

        if sending_time < CROWDSALE_OPEN:
            rate = 1
        elif sending_time < CROWDSALE_OPEN + 86400 * 7:
            rate = CROWDSALE_WEEK1_RATE
        elif sending_time < CROWDSALE_OPEN + 86400 * 7 * 2:
            rate = CROWDSALE_WEEK2_RATE
        elif sending_time < CROWDSALE_OPEN + 86400 * 7 * 3:
            rate = CROWDSALE_WEEK3_RATE
        elif sending_time <= CROWDSALE_CLOSE:
            rate = CROWDSALE_WEEK4_RATE
        else:
            rate = 1
        
        amount_requested = neo_amount * rate / 100000000

        return amount_requested
    
    '''
        return 0 when not for sale
    '''
    return 0


def get_state(ctx, sending_time):
    WHITELIST_SALE_OPEN = get_config(ctx, 'WHITELIST_SALE_OPEN')
    WHITELIST_SALE_CLOSE = get_config(ctx, 'WHITELIST_SALE_CLOSE')
    PRESALE_OPEN = get_config(ctx, 'PRESALE_OPEN')
    PRESALE_CLOSE = get_config(ctx, 'PRESALE_CLOSE')
    CROWDSALE_OPEN = get_config(ctx, 'CROWDSALE_OPEN')
    CROWDSALE_CLOSE = CROWDSALE_OPEN + 86400 * 4 * 7

    if sending_time >= WHITELIST_SALE_OPEN and sending_time <= WHITELIST_SALE_CLOSE:
        return IS_WHITELIST_SALE
    if sending_time >= PRESALE_OPEN and sending_time <= PRESALE_CLOSE:
        return IS_PRESALE
    if sending_time >= CROWDSALE_OPEN and sending_time <= CROWDSALE_CLOSE:
        return IS_CROWDSALE
    return IS_NOT_SALE
