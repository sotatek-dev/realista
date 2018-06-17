from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat

from nex.token import *


OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')


def handle_nep51(ctx, operation, args):

    if operation == 'name':
        return TOKEN_NAME

    elif operation == 'decimals':
        return TOKEN_DECIMALS

    elif operation == 'symbol':
        return TOKEN_SYMBOL

    elif operation == 'totalSupply':
        return get_circulation(ctx)

    elif operation == 'balanceOf':
        if len(args) == 1:
            return get_balance(ctx, args[0])

    elif operation == 'transfer':
        if len(args) == 3:
            return do_transfer(ctx, args[0], args[1], args[2])

    elif operation == 'transferFrom':
        if len(args) == 3:
            return do_transfer_from(ctx, args[0], args[1], args[2])

    elif operation == 'approve':
        if len(args) == 3:
            return do_approve(ctx, args[0], args[1], args[2])

    elif operation == 'allowance':
        if len(args) == 2:
            return do_allowance(ctx, args[0], args[1])

    return False


def do_transfer(ctx, t_from, t_to, amount):

    if amount <= 0:
        return False

    if len(t_to) != 20:
        return False

    if CheckWitness(t_from):

        if t_from == t_to:
            debug_log("transfer to self!")
            return True

        from_val = get_balance(ctx, t_from)

        if from_val < amount:
            debug_log("insufficient funds")
            return False

        if from_val == amount:
            del_balance(ctx, t_from)

        else:
            difference = from_val - amount
            set_balance(ctx, t_from, difference)

        to_value = get_balance(ctx, t_to)

        to_total = to_value + amount

        set_balance(ctx, t_to, to_total)

        OnTransfer(t_from, t_to, amount)

        return True
    else:
        debug_log("from address is not the tx sender")

    return False


def do_transfer_from(ctx, t_from, t_to, amount):

    if amount <= 0:
        return False

    available_key = concat(t_from, t_to)

    if len(available_key) != 40:
        return False

    available_to_to_addr = get_balance(ctx, available_key)

    if available_to_to_addr < amount:
        debug_log("Insufficient funds approved")
        return False

    from_balance = get_balance(ctx, t_from)

    if from_balance < amount:
        debug_log("Insufficient tokens in from balance")
        return False

    to_balance = get_balance(ctx, t_to)

    new_from_balance = from_balance - amount

    new_to_balance = to_balance + amount

    set_balance(ctx, t_to, new_to_balance)
    set_balance(ctx, t_from, new_from_balance)

    debug_log("transfer complete")

    new_allowance = available_to_to_addr - amount

    if new_allowance == 0:
        debug_log("removing all balance")
        del_balance(ctx, available_key)
    else:
        debug_log("updating allowance to new allowance")
        set_balance(ctx, available_key, new_allowance)

    OnTransfer(t_from, t_to, amount)

    return True


def do_approve(ctx, t_owner, t_spender, amount):

    if not CheckWitness(t_owner):
        return False

    if amount < 0:
        return False

    # cannot approve an amount that is
    # currently greater than the from balance
    if get_balance(ctx, t_owner) >= amount:

        approval_key = concat(t_owner, t_spender)

        if amount == 0:
            del_balance(ctx, approval_key)
        else:
            set_balance(ctx, approval_key, amount)

        OnApprove(t_owner, t_spender, amount)

        return True

    return False


def do_allowance(ctx, t_owner, t_spender):

    return get_balance(ctx, concat(t_owner, t_spender))
