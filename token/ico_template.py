"""
NEX ICO Template
===================================

Author: Thomas Saunders
Email: tom@neonexchange.org

Date: Dec 11 2017

"""
from ret.common.txio import get_asset_attachments
from ret.token.rettoken import *
from ret.token.sale import *
from ret.token.kyc import *
from ret.token.nep5 import *
from ret.common.other import *
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness, GetTime
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import *

ctx = GetContext()
NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']


def Main(operation, args):
    """

    :param operation: str The name of the operation to perform
    :param args: list A list of arguments along with the operation
    :return:
        bytearray: The result of the operation
    """

    trigger = GetTrigger()

    # This is used in the Verification portion of the contract
    # To determine whether a transfer of system assets ( NEO/Gas) involving
    # This contract's address can proceed
    if trigger == Verification():

        # check if the invoker is the owner of this contract
        is_owner = CheckWitness(TOKEN_OWNER)

        # If owner, proceed
        if is_owner:

            return True

        # Otherwise, we need to lookup the assets and determine
        # If attachments of assets is ok
        attachments = get_asset_attachments()
        exchangeables = get_exchangeable(ctx, attachments[1], attachments[2], GetTime())
        return exchangeables[0] > 0

    elif trigger == Application():

        for op in NEP5_METHODS:
            if operation == op:
                return handle_nep51(ctx, operation, args)

        if operation == 'deploy':
            return deploy()

        elif operation == 'circulation':
            return get_circulation(ctx)

        # the following are handled by crowdsale

        elif operation == 'mintTokens':
            return perform_exchange(ctx)

        elif operation == 'kyc_register':
            return kyc_register(ctx, args)

        elif operation == 'kyc_status':
            return kyc_status(ctx, args)

        elif operation == 'get_attachments':
            return get_asset_attachments()

        elif operation == 'get_config':
            if len(args) > 0:
                config_name = args[0]
                return get_config(ctx, config_name)

        elif operation == 'set_config':
            if not CheckWitness(TOKEN_OWNER):
                log = debug_log('Must be owner to update config')
                return False
            
            if len(args) == 2:
                config_name = args[0]
                config_value = args[1]
                set_config(ctx, config_name, config_value)
                return True
            
            return False
        
        elif operation == 'get_referrer':
            if len(args) > 0:
                address = args[0]
                return get_referrer(ctx, address)

            log = debug_log('Invalid arguments')
            return False

        elif operation == 'set_referrer':
            if not CheckWitness(TOKEN_OWNER):
                log = debug_log('Must be owner to update referrer')
                return False

            return set_referrer(ctx, args)

        elif operation == 'get_minted_tokens':
            if len(args) == 1:
                state = args[0]
                if state == IS_WHITELIST_SALE:
                    return get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_WHITELIST)
                if state == IS_PRESALE:
                    return get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_PRESALE)
                if state == IS_CROWDSALE:
                    return get_minted_tokens(ctx, STORAGE_PREFIX_PURCHASED_CROWDSALE)
                return 0
            return 0

        elif operation == 'get_contributed_neo':
            if len(args) == 2:
                state = args[0]
                address = args[1]
                if state == IS_WHITELIST_SALE:
                    return get_contributed_neo(ctx, address, STORAGE_PREFIX_PURCHASED_WHITELIST)
                if state == IS_PRESALE:
                    return get_contributed_neo(ctx, address, STORAGE_PREFIX_PURCHASED_PRESALE)
                if state == IS_CROWDSALE:
                    return get_contributed_neo(ctx, address, STORAGE_PREFIX_PURCHASED_CROWDSALE)
                return 0
            return 0

        elif operation == 'get_affiliated_tokens':
            return get_affiliated_tokens(ctx)

        elif operation == 'get_exchangeable_amount':
            if len(args) == 3:
                sender_addr = args[0]
                sent_amount_neo = args[1]
                sending_time = args[2]
                exchangeables = get_exchangeable(ctx, sender_addr, sent_amount_neo, sending_time)
                return exchangeables[0]

            log = debug_log('Invalid arguments')
            return 0

        return 'unknown operation'

    return False


def deploy():
    """

    :param token: Token The token to deploy
    :return:
        bool: Whether the operation was successful
    """
    if not CheckWitness(TOKEN_OWNER):
        log = debug_log("Must be owner to deploy")
        return False

    if not Get(ctx, 'initialized'):
        # do deploy logic
        Put(ctx, 'initialized', 1)
        Put(ctx, TOKEN_OWNER, TOKEN_INITIAL_AMOUNT)
        Put(ctx, ECOSYSTEM_RESERVE_ADDRESS, TOKEN_ECOSYSTEM_AMOUNT)
        Put(ctx, ADVISOR_FUNDS_ADDRESS, TOKEN_ADVISOR_AMOUNT)
        Put(ctx, EMPLOYEE_FUNDS_ADDRESS1, TOKEN_EMPLOYEES_AMOUNT_1)
        Put(ctx, EMPLOYEE_FUNDS_ADDRESS2 , TOKEN_EMPLOYEES_AMOUNT_2)
        Put(ctx, RESERVE_FUNDS_ADDRESS, TOKEN_RESERVE_AMOUNT)
        Put(ctx, AFFILIATE_FUNDS_ADDRESS, TOKEN_AFFILIATE_AMOUNT)
        Put(ctx, SALE_FUNDS_ADDRESS, TOKEN_SALE_AMOUNT)

        log = set_locked(ctx)

        return add_to_circulation(ctx, TOKEN_TOTAL_SUPPLY)

    return False


def set_locked(ctx):
    """
        This function is for prevent Op Not Converted: EXTENDED_ARG
    """
    now = GetTime()
    set_locked_until(ctx, ECOSYSTEM_RESERVE_ADDRESS, now + 3 * 30 * 86400)
    set_locked_until(ctx, ADVISOR_FUNDS_ADDRESS, now + 3 * 30 * 86400)
    set_locked_until(ctx, EMPLOYEE_FUNDS_ADDRESS1, now + 365 * 86400)
    set_locked_until(ctx, EMPLOYEE_FUNDS_ADDRESS2, now + 2 * 365 * 86400)
    set_locked_until(ctx, RESERVE_FUNDS_ADDRESS, now + 365 * 86400)
