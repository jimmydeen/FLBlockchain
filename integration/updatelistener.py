from listenerABC import EventHandler
from web3 import Web3
import json
import datetime
import fcntl

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
    with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'r') as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]
    listener = UpdateListener("https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", contract_address, contract_abi)
    listener.listen()