from boa_test.tests.boa_test import BoaFixtureTest
from boa.compiler import Compiler
from neo.Core.TX.Transaction import Transaction
from neo.Prompt.Commands.BuildNRun import TestBuild
from neo.EventHub import events
from neo.SmartContract.SmartContractEvent import SmartContractEvent, NotifyEvent
from neo.Settings import settings
from neo.Prompt.Utils import parse_param
from neo.Core.FunctionCode import FunctionCode
from neocore.Fixed8 import Fixed8
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Wallets.utils import to_aes_key

from ret.token.rettoken import *
from ret.token.sale import *
from ret.common.other import *

import shutil
import os

settings.USE_DEBUG_STORAGE = True
settings.DEBUG_STORAGE_PATH = './fixtures/debugstorage'


class TestContract(BoaFixtureTest):

    dispatched_events = []
    dispatched_logs = []

    now_in_test = 1510235265
    WHITELIST_SALE_RATE = 4666 * 100000000
    WHITELIST_SALE_UPPER_RATE = 5000 * 100000000
    PRESALE_RATE = 4333 * 100000000
    CROWDSALE_WEEK1_RATE = 4000 * 100000000
    CROWDSALE_WEEK2_RATE = 3833 * 100000000
    CROWDSALE_WEEK3_RATE = 3666 * 100000000
    CROWDSALE_WEEK4_RATE = 3500 * 100000000
    WHITELIST_SALE_PERSONAL_CAP = 500 * 100000000 # 500 NEO
    PRESALE_PERSONAL_CAP = 250 * 100000000 # 250 NEO
    CROWDSALE_PERSONAL_CAP = 500 * 100000000 # 500 NEO

    wallet = {
        'ECOSYSTEM_RESERVE_ADDRESS': UserWallet.Open('./fixtures/testwallet8.db3', to_aes_key('testwallet'))
    }

    @classmethod
    def tearDownClass(cls):
        super(BoaFixtureTest, cls).tearDownClass()

        try:
            if os.path.exists(settings.DEBUG_STORAGE_PATH):
                shutil.rmtree(settings.DEBUG_STORAGE_PATH)
        except Exception as e:
            print("couldn't remove debug storage %s " % e)

    @classmethod
    def setUpClass(cls):
        super(TestContract, cls).setUpClass()

        cls.dirname = '/'.join(os.path.abspath(__file__).split('/')[:-2])

        def on_notif(evt):
            print(evt)
            cls.dispatched_events.append(evt)
            print("dispatched events %s " % cls.dispatched_events)

        def on_log(evt):
            print(evt)
            cls.dispatched_logs.append(evt)
        events.on(SmartContractEvent.RUNTIME_NOTIFY, on_notif)
        events.on(SmartContractEvent.RUNTIME_LOG, on_log)

    def test_ICOTemplate_1(self):

        output = Compiler.instance().load('%s/ico_template.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['totalSupply', '[]'], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_TOTAL_SUPPLY)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_OPEN', self.now_in_test])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_CLOSE', self.now_in_test + 86400])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_RATE', self.WHITELIST_SALE_RATE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_UPPER_RATE', self.WHITELIST_SALE_UPPER_RATE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_PERSONAL_CAP', self.WHITELIST_SALE_PERSONAL_CAP])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_OPEN', self.now_in_test + 86400 * 2])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_CLOSE', self.now_in_test + 86400 * 3])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_RATE', self.PRESALE_RATE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_PERSONAL_CAP', self.PRESALE_PERSONAL_CAP])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_OPEN', self.now_in_test + 86400 * 4])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_WEEK1_RATE', self.CROWDSALE_WEEK1_RATE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_WEEK2_RATE', self.CROWDSALE_WEEK2_RATE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_WEEK3_RATE', self.CROWDSALE_WEEK3_RATE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_WEEK4_RATE', self.CROWDSALE_WEEK4_RATE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['get_config', parse_param(['CROWDSALE_WEEK4_RATE'])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), self.CROWDSALE_WEEK4_RATE)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_PERSONAL_CAP', self.CROWDSALE_PERSONAL_CAP])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

    def test_ICOTemplate_2_exchangeable(self):

        output = Compiler.instance().load('%s/ico_template.py' % TestContract.dirname).default
        out = output.write()

        # before whitelist
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test - 1])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        # check whitelist rate
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.WHITELIST_SALE_RATE)

        # check with upper rate
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 450 * 100000000, self.now_in_test])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 400 * self.WHITELIST_SALE_RATE + 50 * self.WHITELIST_SALE_UPPER_RATE)

        # check presale rate
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test + 86400 * 2])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.PRESALE_RATE)

        # check crowdsale rate
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test + 86400 * 4])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.CROWDSALE_WEEK1_RATE)

        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test + 86400 * 4 + 86400 * 7])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.CROWDSALE_WEEK2_RATE)

        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test + 86400 * 4 + 86400 * 7 * 2])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.CROWDSALE_WEEK3_RATE)

        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test + 86400 * 4 + 86400 * 7 * 3])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.CROWDSALE_WEEK4_RATE)

        # after crowdsale
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 10 * 100000000, self.now_in_test + 86400 * 4 + 86400 * 7 * 4 + 1])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

    def test_ICOTemplate_3_personal_cap(self):

        output = Compiler.instance().load('%s/ico_template.py' % TestContract.dirname).default
        out = output.write()

        # check whitelist cap
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, self.WHITELIST_SALE_PERSONAL_CAP + 1, self.now_in_test])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        # check presale cap
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, self.PRESALE_PERSONAL_CAP + 1, self.now_in_test + 86400 * 2])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        # check crowdsale cap
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, self.CROWDSALE_PERSONAL_CAP + 1, self.now_in_test + 86400 * 4])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

    def test_ICOTemplate_4_locked_until(self):

        output = Compiler.instance().load('%s/ico_template.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['get_locked_until', parse_param([bytearray(ECOSYSTEM_RESERVE_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), self.now_in_test + 3 * 30 * 86400)

        # cannot transfer to locked account
        test_transfer_amount = 2400000001
        tx, results, total_ops, engine = TestBuild(out, ['transfer', parse_param([bytearray(TOKEN_OWNER), bytearray(ECOSYSTEM_RESERVE_ADDRESS), test_transfer_amount])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        # cannot transfer from locked account
        tx, results, total_ops, engine = TestBuild(out, ['transfer', parse_param([bytearray(ECOSYSTEM_RESERVE_ADDRESS), bytearray(TOKEN_OWNER), test_transfer_amount])], self.wallet['ECOSYSTEM_RESERVE_ADDRESS'], '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

    def test_ICOTemplate_5_affiliate(self):

        output = Compiler.instance().load('%s/ico_template.py' % TestContract.dirname).default
        out = output.write()

        #  reconfig to presale
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_OPEN', 0])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_CLOSE', 0])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_OPEN', self.now_in_test])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_CLOSE', self.now_in_test + 86400])], self.GetWallet1(), '0705', '05')

        # set referer
        tx, results, total_ops, engine = TestBuild(out, ['set_referrer', parse_param([self.wallet_3_script_hash.Data, bytearray(ADVISOR_FUNDS_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        # get referer
        tx, results, total_ops, engine = TestBuild(out, ['get_referrer', parse_param([self.wallet_3_script_hash.Data])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetByteArray(), bytearray(ADVISOR_FUNDS_ADDRESS))

        # test mint tokens, this should return true
        tx, results, total_ops, engine = TestBuild(out, ['mintTokens', '[]', '--attach-neo=10'], self.GetWallet3(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        # balance of address
        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([self.wallet_3_script_hash.Data])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.PRESALE_RATE)

        # sale balance
        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([bytearray(SALE_FUNDS_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_SALE_AMOUNT - 10 * self.PRESALE_RATE)

        # minted_token
        tx, results, total_ops, engine = TestBuild(out, ['get_minted_tokens', parse_param([IS_PRESALE])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.PRESALE_RATE)

        # contributed_neo
        tx, results, total_ops, engine = TestBuild(out, ['get_contributed_neo', parse_param([IS_PRESALE, self.wallet_3_script_hash.Data])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * 100000000)

        tx, results, total_ops, engine = TestBuild(out, ['get_contributed_neo', parse_param([IS_CROWDSALE, self.wallet_3_script_hash.Data])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        # circulation
        tx, results, total_ops, engine = TestBuild(out, ['circulation', parse_param([])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_TOTAL_SUPPLY)

        # referer not kyc
        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([bytearray(ADVISOR_FUNDS_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_ADVISOR_AMOUNT)

        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([bytearray(AFFILIATE_FUNDS_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_AFFILIATE_AMOUNT)

        # referer kyc registered
        tx, results, total_ops, engine = TestBuild(out, ['kyc_register', parse_param([bytearray(ADVISOR_FUNDS_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1)

        tx, results, total_ops, engine = TestBuild(out, ['mintTokens', '[]', '--attach-neo=10'], self.GetWallet3(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([bytearray(ADVISOR_FUNDS_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.PRESALE_RATE * 25 / 1000 + TOKEN_ADVISOR_AMOUNT)

        tx, results, total_ops, engine = TestBuild(out, ['balanceOf', parse_param([bytearray(AFFILIATE_FUNDS_ADDRESS)])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), TOKEN_AFFILIATE_AMOUNT - 10 * self.PRESALE_RATE * 25 / 1000)

        # total affiliate
        tx, results, total_ops, engine = TestBuild(out, ['get_affiliated_tokens', parse_param([])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 10 * self.PRESALE_RATE * 25 / 1000)

        #  revert config
        self.test_ICOTemplate_1()

    def test_ICOTemplate_5_sale_and_kyc(self):

        output = Compiler.instance().load('%s/ico_template.py' % TestContract.dirname).default
        out = output.write()

        # kyc registered in whitelistsale, ok
        tx, results, total_ops, engine = TestBuild(out, ['mintTokens', '[]', '--attach-neo=10'], self.GetWallet3(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        # reject kyc
        tx, results, total_ops, engine = TestBuild(out, ['kyc_reject', parse_param([self.wallet_3_script_hash.Data])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1)

        # kyc rejected, fail
        tx, results, total_ops, engine = TestBuild(out, ['mintTokens', '[]', '--attach-neo=10'], self.GetWallet3(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        #  reconfig to presale
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_OPEN', 0])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_CLOSE', 0])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_OPEN', self.now_in_test])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_CLOSE', self.now_in_test + 86400])], self.GetWallet1(), '0705', '05')

        # kyc rejected, fail
        tx, results, total_ops, engine = TestBuild(out, ['mintTokens', '[]', '--attach-neo=10'], self.GetWallet3(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), False)

        #  reconfig to presale
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_OPEN', 0])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_CLOSE', 0])], self.GetWallet1(), '0705', '05')
        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_OPEN', self.now_in_test])], self.GetWallet1(), '0705', '05')

        # crowdsale not require kyc, success
        tx, results, total_ops, engine = TestBuild(out, ['mintTokens', '[]', '--attach-neo=10'], self.GetWallet3(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        # revert kyc
        tx, results, total_ops, engine = TestBuild(out, ['kyc_register', parse_param([self.wallet_3_script_hash.Data])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 1)

        #  revert config
        self.test_ICOTemplate_1()

    def test_ICOTemplate_6_sale_cap(self):

        output = Compiler.instance().load('%s/ico_template.py' % TestContract.dirname).default
        out = output.write()

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['WHITELIST_SALE_PERSONAL_CAP', 2 * 70000000 * 100000000])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['PRESALE_PERSONAL_CAP', 2 * 65000000 * 100000000])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        tx, results, total_ops, engine = TestBuild(out, ['set_config', parse_param(['CROWDSALE_PERSONAL_CAP', 2 * 480000000 * 100000000])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBoolean(), True)

        # check whitelist cap
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 70000000 * 100000000 / self.WHITELIST_SALE_RATE * 100000000, self.now_in_test])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        # # check presale cap
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 65000000 * 100000000 / self.PRESALE_RATE * 100000000, self.now_in_test + 86400 * 2])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        # # check crowdsale cap
        tx, results, total_ops, engine = TestBuild(out, ['get_exchangeable_amount', parse_param([self.wallet_3_script_hash.Data, 480000000 * 100000000 / self.CROWDSALE_WEEK1_RATE * 100000000, self.now_in_test + 86400 * 4])], self.GetWallet1(), '0705', '05')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].GetBigInteger(), 0)

        #  revert config
        self.test_ICOTemplate_1()
