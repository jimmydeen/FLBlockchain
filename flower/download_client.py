from main import mnist_test_loader_client1, mnist_train_loader_client1
from flclient import FlowerClient
import flwr as fl
import json
import sys

class initClient(FlowerClient):
    def __init__(self, _client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi):
        super().__init__(_client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi)
    def getTrainLoader(self):
        return mnist_train_loader_client1
    def getTestLoader(self):
        return mnist_test_loader_client1
    

if __name__ == "__main__":
    # Start Flower client
    
    client = initClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], json.loads(sys.argv[6]))
    input("Press Enter to continue...")
    fl.client.start_numpy_client(server_address=sys.argv[7], client=client)