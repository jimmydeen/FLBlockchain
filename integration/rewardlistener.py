# Listener to listen to IncentiveDistrbuted event emitted from simplecoordinator.sol

from listenerABC import EventHandler
from web3 import Web3
import json

class IncentiveListener(EventHandler):
    def __init__(self, w3, contract_address, contract_abi):
        super().__init__(w3, contract_address, contract_abi)
        self.event_filter = self.contract_instance.events.IncentiveDistributed.create_filter(fromBlock="latest")
        # create empty file for logs
        
        with open ('rewardlog.txt', 'w') as f:
            f.write("")
        

    def handle_event(self, event):
        with open ('rewardlog.txt', 'w') as f:
            f.write(f"Tx Hash: {event.transactionHash.hex()} Incentive event received from client: {event.args._trainer} \n. Reward Amount: {event.args._reward} \n.")


if __name__ == "__main__":
    with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'r') as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]
    listener = IncentiveListener("https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", contract_address, contract_abi)
    listener.listen()