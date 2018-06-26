from ret.token.whitelistsale import *
from ret.token.presale import *
from ret.token.crowdsale import *
from ret.common.other import *
from ret.common.time import *

IS_NOT_SALE = 0
IS_WHITELIST_SALE = 1
IS_PRESALE = 2
IS_CROWDSALE = 3

def perform_exchange(ctx):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """

    state = get_state(ctx)
    if state == IS_WHITELIST_SALE:
        return whitelist_perform_exchange(ctx)
    if state == IS_PRESALE:
        return presale_perform_exchange(ctx)
    if state == IS_CROWDSALE:
        return crowdsale_perform_exchange(ctx)
    return False


def can_exchange(ctx, attachments, verify_only):
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

    state = get_state(ctx)
    if state == IS_WHITELIST_SALE:
        return whitelist_can_exchange(ctx, attachments, verify_only)
    if state == IS_WHITELIST_SALE:
        return whitelist_can_exchange(ctx, attachments, verify_only)
    if state == IS_WHITELIST_SALE:
        return whitelist_can_exchange(ctx, attachments, verify_only)
    return False


def get_state(ctx):
    now = get_now()
    WHITELIST_SALE_OPEN = get_config(ctx, 'WHITELIST_SALE_OPEN')
    WHITELIST_SALE_CLOSE = get_config(ctx, 'WHITELIST_SALE_CLOSE')
    PRESALE_OPEN = get_config(ctx, 'PRESALE_OPEN')
    PRESALE_CLOSE = get_config(ctx, 'PRESALE_CLOSE')
    CROWDSALE_OPEN = get_config(ctx, 'CROWDSALE_OPEN')
    CROWDSALE_CLOSE = CROWDSALE_OPEN + 86400 * 4 * 7

    if now >= WHITELIST_SALE_OPEN and now <= WHITELIST_SALE_CLOSE:
        return IS_WHITELIST_SALE
    if now >= PRESALE_OPEN and now <= PRESALE_CLOSE:
        return IS_PRESALE
    if now >= CROWDSALE_OPEN and now <= CROWDSALE_CLOSE:
        return IS_CROWDSALE
    return IS_NOT_SALE