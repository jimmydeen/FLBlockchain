from listenerABC import EventHandler
from web3 import Web3
import json

class UpdateListener(EventHandler):
    def __init__(self, w3, contract_address, contract_abi):
        super().__init__(w3, contract_address, contract_abi)
        self.event_filter = self.contract_instance.events.UpdateSubmitted.create_filter(fromBlock="latest")
        # create empty file for logs
        
        with open ('log.txt', 'w') as f:
            f.write("")
        

    def handle_event(self, event):
        with open ('log.txt', 'a') as f:
            f.write(f"Tx Hash: {event.transactionHash.hex()} Update event received from client: {event.args._trainer} \n. Number of data points: {event.args._numDatapoints} \n. Reward amount: {event.args._reward} \n.")

if __name__ == "__main__":
    with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'r') as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]
    listener = UpdateListener("https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", contract_address, contract_abi)
    listener.listen()