from boa.interop.Neo.Blockchain import GetHeight
from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from ret.token.rettoken import *
from ret.common.txio import get_asset_attachments
from ret.common.time import get_now
from ret.common.other import *
from ret.token.kyc import get_kyc_status

# OnInvalidKYCAddress = RegisterAction('invalid_registration', 'address')
OnKYCRegister = RegisterAction('kyc_registration', 'address')
OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnRefund = RegisterAction('refund', 'addr_to', 'amount')

WHITELISTSALE_OPEN = 1509431946
WHITELISTSALE_CLOSE = 1509431946 + 86400 * 3
WHITELISTSALE_ROUND_KEY = b'in_whitelistsale'
WHITELISTSALE_PERSONAL_KEY = b'whitelistsale'
WHITELISTSALE_MAX_CAP = 70000000 * 100000000 # 70M
WHITELISTSALE_RATE = 4666 * 100000000
WHITELISTSALE_UPPER_RATE = 5000 * 100000000
WHITELISTSALE_THRESHOLD = 400 * 4666 * 100000000
WHITELISTSALE_PERSONAL_CAP = 400 * 4666 * 100000000 + 100 * 5000 * 100000000


def whitelist_perform_exchange(ctx):
    """

     :param token:Token The token object with NEP5/sale settings
     :return:
         bool: Whether the exchange was successful
     """

    attachments = get_asset_attachments()  # [receiver, sender, neo, gas]

    # this looks up whether the exchange can proceed
    exchange_ok = whitelist_can_exchange(ctx, attachments, False)

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

    whitelistsale_personal_key = concat(WHITELISTSALE_PERSONAL_KEY, attachments[1])
    whitelistsale_personal_balance = storage_get(ctx, attachments[1], WHITELISTSALE_PERSONAL_KEY)
    whitelistsale_round_balance = Get(ctx, WHITELISTSALE_ROUND_KEY)

    # calculate the amount of tokens the attached neo will earn
    exchanged_tokens = whitelist_get_amount_requested(ctx, attachments[1], attachments[2])

    # if you want to exchange gas instead of neo, use this
    # exchanged_tokens += attachments[3] * TOKENS_PER_GAS / 100000000

    # add it to the the exchanged tokens and persist in storage
    new_total = exchanged_tokens + current_balance
    Put(ctx, attachments[1], new_total)

    new_whitelistsale_personal_total = exchanged_tokens + whitelistsale_personal_balance
    Put(ctx, whitelistsale_personal_key, new_whitelistsale_personal_total)
    
    new_whitelistsale_round_total = exchanged_tokens + whitelistsale_round_balance
    Put(ctx, WHITELISTSALE_ROUND_KEY, new_whitelistsale_round_total)

    # update the in circulation amount
    result = add_to_circulation(ctx, exchanged_tokens)

    # dispatch transfer event
    OnTransfer(attachments[0], attachments[1], exchanged_tokens)

    return True


def whitelist_can_exchange(ctx, attachments, verify_only):
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

    # the following looks up whether an address has been
    # registered with the contract for KYC regulations
    # this is not required for operation of the contract

#        status = get_kyc_status(attachments.sender_addr, storage)
    if not get_kyc_status(ctx, attachments[1]):
        return False

    # caluclate the amount requested
    amount_requested = whitelist_get_amount_requested(ctx, attachments[1], attachments[2])

    # this would work for accepting gas
    # amount_requested = attachments.gas_attached * token.tokens_per_gas / 100000000

    exchange_ok = whitelist_calculate_can_exchange(ctx, amount_requested, attachments[1], verify_only)

    return exchange_ok


def whitelist_calculate_can_exchange(ctx, amount, address, verify_only):
    """
    Perform custom token exchange calculations here.

    :param amount:int Number of tokens to convert from asset to tokens
    :param address:bytearray The address to mint the tokens to
    :return:
        bool: Whether or not an address can exchange a specified amount
    """
    now = get_now()

    current_in_circulation = Get(ctx, TOKEN_CIRC_KEY)
    
    personal_key = concat(WHITELISTSALE_PERSONAL_KEY, address)
    personal_balance = Get(ctx, personal_key)
    round_balance = Get(ctx, WHITELISTSALE_ROUND_KEY)

    new_amount = current_in_circulation + amount
    new_personal_amount = personal_balance + amount
    new_round_amount = round_balance + amount

    if now < WHITELISTSALE_OPEN:
        return False

    if new_amount > TOKEN_TOTAL_SUPPLY:
        return False

    if new_personal_amount > WHITELISTSALE_PERSONAL_CAP:
        return False

    if new_round_amount > WHITELISTSALE_MAX_CAP:
        return False

    return True


def whitelist_get_amount_requested(ctx, address, amount):
    current_personal_key = concat(WHITELISTSALE_PERSONAL_KEY, address)
    current_personal_balance = Get(ctx, current_personal_key)
    amount_requested = amount * WHITELISTSALE_RATE / 100000000

    if current_personal_balance >= WHITELISTSALE_THRESHOLD:
        amount_requested = amount * WHITELISTSALE_UPPER_RATE / 100000000
    else: 
        addition = current_personal_balance + amount_requested - WHITELISTSALE_THRESHOLD
        if addition > 0:
            new_addition = addition / WHITELISTSALE_RATE * WHITELISTSALE_UPPER_RATE
            amount_requested = amount_requested - addition + new_addition

    return amount_requested
