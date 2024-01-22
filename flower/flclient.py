"""
    This file contains the abstract class for the Flower client. The client is modified to work with 
    a neural network model, and the MNIST dataset.
"""

import flwr as fl
import torch
from nn import Net, test, train, DEVICE
from collections import OrderedDict
from abc import ABC, abstractmethod
from web3 import Web3



# Define Flower client, base class (abstract)

class FlowerClient(fl.client.NumPyClient, ABC):
  def __init__(self, _client_address, _client_pk, _web3_endpoint, _chainid, _contract_address, _contract_abi):
    super().__init__()
    self.net = Net().to(DEVICE)
    self.address = _client_address
    self.pk = _client_pk
    self.web3 = Web3(Web3.HTTPProvider(_web3_endpoint))
    self.chain_id = _chainid
    assert self.web3.is_connected(), "Web3 connection failed"
    self.contract = self.web3.eth.contract(address=_contract_address, abi=_contract_abi)

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
    loss, accuracy = train(self.net, self.getTrainLoader(), epochs=1)
    print(f"Accuracy: {accuracy}, Loss: {loss}")
    with open('log.txt', 'a') as f:
      f.write(f"Accuracy: {accuracy}, Loss: {loss} \n")
    
    # tx = self.contract.functions.submitUpdate(len(self.getTrainLoader().dataset)).transact({'from': self.address, 'chainId': self.chain_id, "nonce": self.web3.eth.get_transaction_count(self.address)})

    # WHEN METAMASK LINKED NO NEED FOR SIGNING MANUAL
    # Estimate gas cost of submitUpdate function
    gas_estimate = self.contract.functions.submitUpdate(len(self.getTrainLoader().dataset)).estimate_gas({'from': self.address, 'chainId': self.chain_id, "nonce": self.web3.eth.get_transaction_count(self.address)})
    # build transaction
    tx = self.contract.functions.submitUpdate(len(self.getTrainLoader().dataset), gas_estimate).build_transaction({'from': self.address, 'chainId': self.chain_id, "nonce": self.web3.eth.get_transaction_count(self.address)})
    signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.pk)

    tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Return updated model parameters, (config is not used), and length of dataset
    return self.get_parameters(config={}), len(self.getTrainLoader().dataset), {"accuracy": float(accuracy), "loss": float(loss)}

  def evaluate(self, parameters, config):
    # Update the model with the latest parameters
    self.set_parameters(parameters)
    # Test model on dataset
    loss, accuracy = test(self.net, self.getTestLoader())
    return float(loss), len(self.getTestLoader().dataset), {"accuracy": float(accuracy), "loss": float(loss)}

