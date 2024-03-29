"""
Example of running a NEO node and receiving notifications when events
of a specific smart contract happen.
Events include Runtime.Notify, Runtime.Log, Storage.*, Execution.Success
and several more. See the documentation here:
http://neo-python.readthedocs.io/en/latest/smartcontracts.html
"""
import threading
import os
import MySQLdb
import sys
from time import sleep

from logzero import logger
from twisted.internet import reactor, task

from neo.contrib.smartcontract import SmartContract
from neo.Network.NodeLeader import NodeLeader
from neo.Core.Blockchain import Blockchain
from neo.Implementations.Blockchains.LevelDB.LevelDBBlockchain import LevelDBBlockchain
from neo.Settings import settings
from neocore.Cryptography.Crypto import Crypto, UInt160

from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join('.', '.env')))

# If you want the log messages to also be saved in a logfile, enable the
# next line. This configures a logfile with max 10 MB and 3 rotations:
# settings.set_logfile("/tmp/logfile.log", max_bytes=1e7, backup_count=3)

# Setup the smart contract instance
smart_contract = SmartContract("fdb94040d3578817cc9293f95b8ddae75d87ac57")


# Register an event handler for Runtime.Notify events of the smart contract.
@smart_contract.on_notify
def sc_notify(event):
    logger.info("SmartContract Runtime.Notify event: %s", event)

    # Make sure that the event payload list has at least one element.
    if not len(event.event_payload):
        return

    # The event payload list has at least one element. As developer of the smart contract
    # you should know what data-type is in the bytes, and how to decode it. In this example,
    # it's just a string, so we decode it with utf-8:

    behavior = event.event_payload[0].decode("utf-8")

    if behavior == 'transfer':
        sender = scriptToAddress(event.event_payload[1])
        receiver = scriptToAddress(event.event_payload[2])
        amount = event.event_payload[3]
        logger.info("%s : %s : %s: %s", behavior, sender, receiver, amount)
    if behavior == 'refund':
        addr_to = scriptToAddress(event.event_payload[1])
        amount = event.event_payload[2]
        refund_to_database(event, addr_to, amount)
        logger.info("%s : %s : %s", behavior, addr_to, amount)


def refund_to_database(event, addr_to, amount):
    conn = MySQLdb.connect(host=os.getenv('MYSQL_DB_HOST'), port=int(os.getenv('MYSQL_DB_PORT')), user=os.getenv('MYSQL_USERNAME'), passwd=os.getenv('MYSQL_PASSWORD'), db=os.getenv('MYSQL_DBNAME'))
    x = conn.cursor()

    try:
        x.execute("""INSERT INTO refund (block_number, block_timestamp, txid, address, amount) VALUES (%s, %s, %s, %s, %s)""", (event.block_number, 0, event.tx_hash, addr_to, amount))
        conn.commit()
    except:
        logger.error(sys.exc_info()[0])
        conn.rollback()

    conn.close()


def scriptToAddress(script):
    data = UInt160(data=script)
    return Crypto.ToAddress(data)


def custom_background_code():
    """ Custom code run in a background thread. Prints the current block height.
    This function is run in a daemonized thread, which means it can be instantly killed at any
    moment, whenever the main thread quits. If you need more safety, don't use a  daemonized
    thread and handle exiting this thread in another way (eg. with signals and events).
    """
    while True:
        logger.info("Block %s / %s", str(Blockchain.Default().Height), str(Blockchain.Default().HeaderHeight))
        sleep(15)


def main():
    settings.setup_privnet()

    # Setup the blockchain
    blockchain = LevelDBBlockchain(os.path.join(os.path.dirname(__file__), 'leveldb'))
    Blockchain.RegisterBlockchain(blockchain)
    dbloop = task.LoopingCall(Blockchain.Default().PersistBlocks)
    dbloop.start(.1)
    NodeLeader.Instance().Start()

    # Disable smart contract events for external smart contracts
    settings.set_log_smart_contract_events(False)

    # Start a thread with custom code
    d = threading.Thread(target=custom_background_code)
    d.setDaemon(True)  # daemonizing the thread will kill it when the main thread is quit
    d.start()

    # Run all the things (blocking call)
    logger.info("Everything setup and running. Waiting for events...")
    reactor.run()
    logger.info("Shutting down.")


if __name__ == "__main__":
    main()