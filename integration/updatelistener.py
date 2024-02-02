from listenerABC import EventHandler
from web3 import Web3
import json
import datetime
import fcntl
import sys

class UpdateListener(EventHandler):
    def __init__(self, w3, contract_address, contract_abi):
        super().__init__(w3, contract_address, contract_abi)
        self.event_filter = self.contract_instance.events.UpdateSubmitted.create_filter(fromBlock="latest")

    def handle_event(self, event):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('progresslog.txt', 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # Acquire an exclusive lock
            f.write(f"[{timestamp}] Update Received! \n \n")
            f.write(f"Update received from client: {event.args._trainer}\n")
            f.write(f"Tx Hash: {event.transactionHash.hex()}\n \n \n")
            # f.write(f"Number of data points: {event.args._numDatapoints}\n")
            # f.write(f"Reward amount: {event.args._reward}\n")
            fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock

if __name__ == "__main__":
    web3endpoint = sys.argv[1]
    contract_address = sys.argv[2]
    contract_abi = sys.argv[3]
    listener = UpdateListener(web3endpoint, contract_address, contract_abi)
    listener.listen()