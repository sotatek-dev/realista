from boa.interop.Neo.Runtime import CheckWitness
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import Get, Put
from boa.builtins import concat
from ret.token.rettoken import *

# OnInvalidKYCAddress = RegisterAction('invalid_registration', 'address')
OnKYCRegister = RegisterAction('kyc_registration', 'address')
OnKYCReject = RegisterAction('kyc_reject', 'address')
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

                kyc_storage_key = concat(STORAGE_KEY_KYC, address)
                Put(ctx, kyc_storage_key, True)

                OnKYCRegister(address)
                ok_count += 1

    return ok_count


def kyc_reject(ctx, args):
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

                kyc_storage_key = concat(STORAGE_KEY_KYC, address)
                Delete(ctx, kyc_storage_key)

                OnKYCReject(address)
                ok_count += 1

    return ok_count


def kyc_status(ctx, args):
    """
    Gets the KYC Status of an address

    :param args:list a list of arguments
    :return:
        bool: Returns the kyc status of an address
    """

    if len(args) > 0:
        addr = args[0]

        kyc_storage_key = concat(STORAGE_KEY_KYC, addr)

        return Get(ctx, kyc_storage_key)

    return False


def get_kyc_status(ctx, address):
    """
    Looks up the KYC status of an address

    :param address:bytearray The address to lookup
    :param storage:StorageAPI A StorageAPI object for storage interaction
    :return:
        bool: KYC Status of address
    """
    kyc_storage_key = concat(STORAGE_KEY_KYC, address)

    return Get(ctx, kyc_storage_key)
