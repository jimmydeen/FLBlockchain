from main import mnist_train_loader_client3, mnist_test_loader_client3
from flclient import FlowerClient
import flwr as fl
import json

class c3(FlowerClient):
    def __init__(self, _client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi):
        super().__init__(_client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi)
    def getTrainLoader(self):
        return mnist_train_loader_client3
    def getTestLoader(self):
        return mnist_test_loader_client3
    







if __name__ == "__main__":
    # Start Flower client  
    with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'r') as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]
    client = c3("0x7A8ac0fe268eD90643784AF04963071364D8e3B0", "d029a9c29fd6efa1050c788539ae97dcd79754c4f6cfe5f5bf2d459ea63bf179", "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", 11155111, contract_address, contract_abi)
    num_data_points = len(client.getTrainLoader().dataset)
    with open ('log.txt', 'a') as f:
        f.write(f"Number of data points: {num_data_points} from client: 3 \n")
    fl.client.start_numpy_client(server_address="127.0.0.1:7545", client=client)