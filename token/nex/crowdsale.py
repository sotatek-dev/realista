from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Runtime import CheckWitness, GetTime
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from nex.token import *
from nex.txio import get_asset_attachments

# OnInvalidKYCAddress = RegisterAction('invalid_registration', 'address')
OnKYCRegister = RegisterAction('kyc_registration', 'address')
OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnRefund = RegisterAction('refund', 'addr_to', 'amount')


def kyc_register(ctx, args):
    """

    :param args:list a list of addresses to register
    :param token:Token A token object with your ICO settings
    :return:
        int: The number of addresses to register for KYC
    """
    ok_count = 0

    if CheckWitness(TOKEN_OWNER):

        for address in args:

            if len(address) == 20:

                storage_put(ctx, address, True, STORAGE_PREFIX_KYC)

                OnKYCRegister(address)
                ok_count += 1

    return ok_count


def kyc_status(ctx, address):
    """
    Looks up the KYC status of an address

    :param address:bytearray The address to lookup
    :param storage:StorageAPI A StorageAPI object for storage interaction
    :return:
        bool: KYC Status of address
    """

    return storage_get(ctx, address, STORAGE_PREFIX_KYC)


def perform_exchange(ctx):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """

    attachments = get_asset_attachments()  # [receiver, sender, neo, gas]
    receiver_addr   = attachments[0]
    sender_addr     = attachments[1]
    sent_amount_neo = attachments[2]
    sent_amount_gas = attachments[3]

    # this looks up whether the exchange can proceed
    now = GetTime()
    exchangeables = get_exchangeable(ctx, sender_addr, sent_amount_neo, now)

    # calculate the amount of tokens the attached neo will earn
    exchanged_tokens = exchangeables[0]
    contributed_neos = exchangeables[1]

    if exchanged_tokens == 0:
        # This should only happen in the case that there are a lot of TX on the final
        # block before the total amount is reached.  An amount of TX will get through
        # the verification phase because the total amount cannot be updated during that phase
        # because of this, there should be a process in place to manually refund tokens
        if sent_amount_neo > 0:
            OnRefund(sender_addr, sent_amount_neo)

        return False

    # add tokens to the sender's balance
    add_balance(ctx, sender_addr, exchanged_tokens)

    # update the in circulation amount
    add_minted_tokens(ctx, exchanged_tokens, contributed_neos)

    # dispatch transfer event
    OnTransfer(receiver_addr, sender_addr, exchanged_tokens)

    # add bonus token for the referrer
    referrer_addr = get_referrer(ctx, sender_addr)
    if not referrer_addr:
        return True

    referrer_bonus_tokens = 1000 * exchanged_tokens / AFFILIATE_RATE
    add_affiliated_tokens(ctx, referrer_bonus_tokens)

    add_balance(ctx, referrer_addr, referrer_bonus_tokens)

    # dispatch transfer event
    OnTransfer(receiver_addr, referrer_addr, referrer_bonus_tokens)

    return True


def get_exchangeable(ctx, sender_addr, sent_amount_neo, sending_time):
    """
    Calculate how many NEOs and tokens are exchangeable in this purchase

    :param sender_addr:bytearray    The address of investor
    :param sent_amount_neo:int      Amount of NEO investor is using to purchase tokens
    :param sending_time:int         Timestamp of block that contains the sending action
    :return:
        [int, int]: number of tokens investor will get and number NEOs will be consumed
    """

    if sent_amount_neo == 0:
        debug_log('<get_exchangeable> sending 0 NEO -> got no tokens')
        return [0, 0]

    minted_tokens = get_minted_tokens(ctx)
    requested_token_amount = 0

    """
    # WHITELIST SALE PHASE
    """
    WHITELIST_SALE_BEGIN = get_config(ctx, 'WHITELIST_SALE_BEGIN')
    WHITELIST_SALE_END = get_config(ctx, 'WHITELIST_SALE_END')
    PRESALE_BEGIN = get_config(ctx, 'PRESALE_BEGIN')
    PRESALE_END = get_config(ctx, 'PRESALE_END')
    CROWDSALE_BEGIN = get_config(ctx, 'CROWDSALE_BEGIN')

    WHITELIST_SALE_RATE = get_config(ctx, 'WHITELIST_SALE_RATE')
    WHITELIST_WHOLESALE_RATE = get_config(ctx, 'WHITELIST_WHOLESALE_RATE')
    PRESALE_RATE = get_config(ctx, 'PRESALE_RATE')
    CROWDSALE_WEEK1_RATE = get_config(ctx, 'CROWDSALE_WEEK1_RATE')
    CROWDSALE_WEEK2_RATE = get_config(ctx, 'CROWDSALE_WEEK2_RATE')
    CROWDSALE_WEEK3_RATE = get_config(ctx, 'CROWDSALE_WEEK3_RATE')
    CROWDSALE_WEEK4_RATE = get_config(ctx, 'CROWDSALE_WEEK4_RATE')

    if (WHITELIST_SALE_BEGIN <= sending_time) and (sending_time <= WHITELIST_SALE_END):
        # KYC is required in whitelist sale
        if not kyc_status(ctx, sender_addr):
            debug_log('<get_exchangeable> in whitelist sale but not KYC yet -> got no tokens')
            return [0, 0]

        # Investor purchases exceeds individual limitation
        # In this case we don't let him to get more tokens
        old_accumulation = storage_get(ctx, sender_addr, STORAGE_PREFIX_PURCHASED_WHITELIST)
        new_accumulation = old_accumulation + sent_amount_neo

        if new_accumulation > WHITELIST_PERSONAL_CAP:
            debug_log('<get_exchangeable> in whitelist sale but personal cap is reached -> got no tokens')
            return [0, 0]

        avail_tokens_left = WHITELIST_MAX_CAP - minted_tokens

        # If total invested NEO still doesn't exceed the wholesale threshold
        # The exchange rate is normal bonus for presale phase
        if new_accumulation <= WHITELIST_WHOLESALE_THRESHOLD:
            requested_token_amount = WHITELIST_SALE_RATE * sent_amount_neo / DECIMAL_FACTOR
            if requested_token_amount > avail_tokens_left:
                debug_log('<get_exchangeable> in whitelist sale but not enough tokens left for you (1) -> got no tokens')
                return [0, 0]

            debug_log('<get_exchangeable> get tokens in whitelist sale (1)')
            return [requested_token_amount, sent_amount_neo]

        # Otherwise the threshold-exceeded NEO will get higher exchange rate
        norm_rate_amount_neo = WHITELIST_WHOLESALE_THRESHOLD - old_accumulation
        high_rate_amount_neo = new_accumulation - WHITELIST_WHOLESALE_THRESHOLD
        requested_token_amount = (WHITELIST_WHOLESALE_RATE * high_rate_amount_neo + WHITELIST_SALE_RATE * norm_rate_amount_neo) / DECIMAL_FACTOR

        # The number of left tokens is not enough for sale
        if requested_token_amount > avail_tokens_left:
            debug_log('<get_exchangeable> in whitelist sale but not enough tokens left for you (2) -> got no tokens')
            return [0, 0]

        debug_log('<get_exchangeable> get tokens in whitelist sale (2)')
        return [requested_token_amount, sent_amount_neo]

    """
    # PRESALE PHASE
    """
    if (PRESALE_BEGIN <= sending_time) and (sending_time <= PRESALE_END):
        old_accumulation = storage_get(ctx, sender_addr, STORAGE_PREFIX_PURCHASED_PRESALE)
        new_accumulation = old_accumulation + sent_amount_neo

        # Investor purchases exceeds individual limitation
        # In this case we don't let him to get more tokens
        if new_accumulation > PRESALE_PERSONAL_CAP:
            debug_log('<get_exchangeable> in presale but personal cap is reached -> got no tokens')
            return [0, 0]

        avail_tokens_left = WHITELIST_MAX_CAP + PRESALE_MAX_CAP - minted_tokens
        requested_token_amount = PRESALE_RATE * sent_amount_neo / DECIMAL_FACTOR

        # The number of left tokens is not enough for sale
        if requested_token_amount > avail_tokens_left:
            debug_log('<get_exchangeable> in presale but not enough tokens left for you -> got no tokens')
            return [0, 0]

        debug_log('<get_exchangeable> get tokens in presale')
        return [requested_token_amount, sent_amount_neo]

    """
    # Crowdsale
    """
    if (CROWDSALE_BEGIN <= sending_time) and (sending_time <= CROWDSALE_BEGIN + WEEK_IN_SECONDS * 4):
        old_accumulation = storage_get(ctx, sender_addr, STORAGE_PREFIX_PURCHASED_CROWDSALE)
        new_accumulation = old_accumulation + sent_amount_neo

        # Investor purchases exceeds individual limitation
        # In this case we don't let him to get more tokens
        if new_accumulation > CROWDSALE_PERSONAL_CAP:
            debug_log('<get_exchangeable> in crowdsale but personal cap is reached -> got no tokens')
            return [0, 0]

        crowdsale_exchange_rate = 0

        if (CROWDSALE_BEGIN <= sending_time) and (sending_time <= CROWDSALE_BEGIN + WEEK_IN_SECONDS):
            crowdsale_exchange_rate = CROWDSALE_WEEK1_RATE

        if (CROWDSALE_BEGIN + WEEK_IN_SECONDS <= sending_time) and (sending_time <= CROWDSALE_BEGIN + WEEK_IN_SECONDS * 2):
            crowdsale_exchange_rate = CROWDSALE_WEEK2_RATE

        if (CROWDSALE_BEGIN + WEEK_IN_SECONDS * 2 <= sending_time) and (sending_time <= CROWDSALE_BEGIN + WEEK_IN_SECONDS * 3):
            crowdsale_exchange_rate = CROWDSALE_WEEK3_RATE

        if (CROWDSALE_BEGIN + WEEK_IN_SECONDS * 3 <= sending_time) and (sending_time <= CROWDSALE_BEGIN + WEEK_IN_SECONDS * 4):
            crowdsale_exchange_rate = CROWDSALE_WEEK4_RATE

        avail_tokens_left = CROWDSALE_MAX_CAP + WHITELIST_MAX_CAP + PRESALE_MAX_CAP - minted_tokens
        requested_token_amount = crowdsale_exchange_rate * sent_amount_neo / DECIMAL_FACTOR

        # The number of left tokens is not enough for sale
        if requested_token_amount > avail_tokens_left:
            debug_log('<get_exchangeable> in crowdsale but not enough tokens left for you -> got no tokens')
            return [0, 0]

        debug_log('<get_exchangeable> get tokens in crowdsale')
        return [requested_token_amount, sent_amount_neo]

    debug_log('<get_exchangeable> not in any sale period -> got no tokens')
    return [0]
