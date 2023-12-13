import json
from web3 import Web3
import os
from dotenv import load_dotenv
from eth_account import Account
from clientcontract import ClientContract



# load_dotenv()
# install_solc("0.8.9")
class Client:
    def __init__(self, w3_endpoint, _address, private_key, chain_id):
        # Set client params
        self.w3_endpoint = Web3(Web3.HTTPProvider(w3_endpoint))
        self.address = _address
        # Move to Env variable
        self.private_key = private_key
        self.chain_id = chain_id
        self.nonce = self.w3_endpoint.eth.get_transaction_count(self.address)
        # Create contract
        self.contract = self.createContract("./ClientUpdate.sol", w3_endpoint)
    def createContract(self, _contract_path, w3_endpoint):
        """
            Takes contract path as param, compiles and creates the contract, and
            returns reference to contract
        """
        return ClientContract(_contract_path, w3_endpoint, self.chain_id, self.address)
    
    def deployContract(self):
        self.contract.deployContract(self.getNonce(), self.private_key)

    def getNonce(self):
        return self.w3_endpoint.eth.get_transaction_count(self.address)
    def submitUpdate(self, update_data):
        self.contract.submitUpdate(update_data, self.getNonce(), self.private_key)
    
    def isValidPrivateKey(_private_key, _address):
        try:
            address = Account.from_key(_private_key).address
            return address.lower() == _address.lower()
        except ValueError:
            return False




   