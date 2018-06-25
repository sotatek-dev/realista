from ret.token.whitelistsale import *
from ret.token.presale import *
from ret.token.kyc import *


def perform_exchange(ctx, args):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """

    # return whitelist_perform_exchange(ctx)
    return presale_perform_exchange(ctx, args)


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

    # return whitelist_can_exchange(ctx, attachments, verify_only)
    return presale_can_exchange(ctx, attachments, verify_only)
