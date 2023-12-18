"""
    This file contains the abstract class for the Flower client. The client is modified to work with 
    a neural network model, and the MNIST dataset.
"""

import flwr as fl
import torch
from nn import Net, test, train, DEVICE
from collections import OrderedDict
from abc import ABC, abstractmethod



# Define Flower client, base class (abstract)

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
    # Gets tensor parameters from the model, and converts them to numpy arrays
    return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

  def set_parameters(self, parameters):
    # Gets parameters and zips them with the state dict keys
    params_dict = zip(self.net.state_dict().keys(), parameters)
    # Converts the parameters to torch tensors
    state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
    # Loads the state dict into the model, replaces current params. strict=true ensures keys in state_dict match keys 
    # in model
    self.net.load_state_dict(state_dict, strict=True)

  def fit(self, parameters, config):
    # Update the model with the latest parameters
    self.set_parameters(parameters)
    # Train model on dataset
    loss, accuracy = train(self.net, self.getTrainLoader(), epochs=10)
    print(f"Accuracy: {accuracy}, Loss: {loss}")
    # Return updated model parameters, (config is not used), and length of dataset
    return self.get_parameters(config={}), len(self.getTrainLoader().dataset), {"accuracy": float(accuracy), "loss": float(loss)}

  def evaluate(self, parameters, config):
    # Update the model with the latest parameters
    self.set_parameters(parameters)
    # Test model on dataset
    loss, accuracy = test(self.net, self.getTestLoader())
    return float(loss), len(self.getTestLoader().dataset), {"accuracy": float(accuracy), "loss": float(loss)}

