from main import mnist_train_loader_client3, mnist_test_loader_client3
from flclient import FlowerClient
import flwr as fl

class c3(FlowerClient):
    def getTrainLoader(self):
        return mnist_train_loader_client3
    def getTestLoader(self):
        return mnist_test_loader_client3
    







if __name__ == "__main__":
    # Start Flower client
    fl.client.start_numpy_client(server_address="127.0.0.1:7545", client=c3())