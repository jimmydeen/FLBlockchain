from main import mnist_test_loader_client2, mnist_train_loader_client2
from flclient import FlowerClient
import flwr as fl
import json

class c2(FlowerClient):
    def __init__(self, _client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi ):
        super().__init__(_client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi)
    def getTrainLoader(self):

        return mnist_train_loader_client2
    def getTestLoader(self):
        return mnist_test_loader_client2
    







if __name__ == "__main__":
    # Start Flower client
    with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'r') as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]

    client = c2("0xea89364668B868Df6B3a691dd3A8DE15E10f2b9c", "493214aaa8692fd9136a161111a25326a4ace382dd378f7a3317e04bf9ac67f5", "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", 11155111, contract_address, contract_abi)
    fl.client.start_numpy_client(server_address="127.0.0.1:7545", client=client)

