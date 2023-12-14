import flwr as fl
import torch
from nn import Net, test, train, DEVICE
from collections import OrderedDict
from abc import ABC, abstractmethod

# #############################################################################
# Federating the pipeline with Flower
# #############################################################################


# Define Flower client
class FlowerClient(fl.client.NumPyClient, ABC):
  def __init__(self):
    super().__init__()
    self.net = Net().to(DEVICE)
  @abstractmethod
  def getTrainLoader(self):
    pass
  
  @abstractmethod
  def getTestLoader(self):
    pass
  
  def get_parameters(self, config):
    return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

  def set_parameters(self, parameters):
    params_dict = zip(self.net.state_dict().keys(), parameters)
    state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
    self.net.load_state_dict(state_dict, strict=True)

  def fit(self, parameters, config):
    self.set_parameters(parameters)
    train(self.net, self.getTrainLoader(), epochs=0)
    return self.get_parameters(config={}), len(self.getTrainLoader().dataset), {}

  def evaluate(self, parameters, config):
    self.set_parameters(parameters)
    loss, accuracy = test(self.net, self.getTestLoader())
    return float(loss), len(self.getTestLoader().dataset), {"accuracy": float(accuracy)}

