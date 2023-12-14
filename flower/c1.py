from main import mnist_test_loader_client1, mnist_train_loader_client1
from flclient import FlowerClient
import flwr as fl

class c1(FlowerClient):
    def getTrainLoader(self):
        return mnist_train_loader_client1
    def getTestLoader(self):
        return mnist_test_loader_client1
    







if __name__ == "__main__":
    # Start Flower client
    fl.client.start_numpy_client(server_address="127.0.0.1:7545", client=c1())