from main import mnist_test_loader_client1, mnist_train_loader_client1
from flclient import FlowerClient
import flwr as fl

class c1(FlowerClient):
    def __init__(self, _client_address, _client_pk, _web3_endpoint, _contract_address, _contract_abi):
        super().__init__(_client_address, _client_pk, _web3_endpoint, _contract_address, _contract_abi)
    def getTrainLoader(self):
        return mnist_train_loader_client1
    def getTestLoader(self):
        return mnist_test_loader_client1
    







if __name__ == "__main__":
    # Start Flower client
    client = c1("0x48e26Bb936Cc88347bBb2C0EffaE919C424CfdBF", "0x71823b0a59121f69a3686cfa24c06e8b0e6e980908e0b33a0a09be895297b3fe", "HTTP://127.0.0.1:8545", )
    num_data_points = len(client.getTrainLoader().dataset)
    with open ('log.txt', 'a') as f:
        f.write(f"Number of data points: {num_data_points} from client: 1\n")
    fl.client.start_numpy_client(server_address="127.0.0.1:8545", client=client)