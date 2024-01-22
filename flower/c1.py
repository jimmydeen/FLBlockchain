from main import mnist_test_loader_client1, mnist_train_loader_client1
from flclient import FlowerClient
import flwr as fl
import json

class c1(FlowerClient):
    def __init__(self, _client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi):
        super().__init__(_client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi)
    def getTrainLoader(self):
        return mnist_train_loader_client1
    def getTestLoader(self):
        return mnist_test_loader_client1
    







if __name__ == "__main__":
    # Start Flower client
    with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'r') as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]
    client = c1("0xA358910B8b245EC4B8EB558114e926C3F9b3d43D", "752227f65cd5e27e746c2ef7a414568962f7d2957352ea1b0ab0a37b55754ce9", "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", 11155111, contract_address, contract_abi)
    
    fl.client.start_numpy_client(server_address="127.0.0.1:7545", client=client)