# Listener to listen to IncentiveDistrbuted event emitted from simplecoordinator.sol

from listenerABC import EventHandler
from web3 import Web3
import json
import datetime
import fcntl

class IncentiveListener(EventHandler):
    def __init__(self, w3, contract_address, contract_abi):
        super().__init__(w3, contract_address, contract_abi)
        self.event_filter = self.contract_instance.events.IncentiveDistributed.create_filter(fromBlock="latest")
        # create empty file for logs
        
        

    def handle_event(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('progresslog.txt', 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # Acquire an exclusive lock
            f.write(f"[{timestamp}] Reward Sent! \n \n")
            f.write(f"Incentive sent to client: {event.args._trainer}\n")
            f.write(f"Reward Amount: {event.args._reward}\n")
            f.write(f"Tx Hash: {event.transactionHash.hex()}\n \n \n")
            fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock


if __name__ == "__main__":
    with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'r') as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]
    listener = IncentiveListener("https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", contract_address, contract_abi)
    listener.listen()