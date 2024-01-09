"""
    This file listens for aggregate events, and handles them by sending update data to server.
"""


from web3 import Web3
from abc import ABC, abstractmethod


class EventHandler(ABC):
    def __init__(self, w3, contract_address, contract_abi):
        self.w3 = Web3(Web3.HTTPProvider(w3))
        if self.w3.isConnected():
            print("Connected to blockchain")
        else:
            print("Failed to connect")

        self.contract_instance = self.w3.eth.contract(address=contract_address, abi=contract_abi)
    
    @abstractmethod
    def handle_event(self, event):
        pass