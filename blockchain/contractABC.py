from abc import ABC, abstractmethod
import json
from web3 import Web3
import os
from dotenv import load_dotenv
# load_dotenv()

class ContractABC(ABC):

    def __init__(self, contract_path, w3provider, chain_id, sender_address):
        # Create contract 
        self.compiled_sol = self.compileSol(contract_path)
        self.bytecode = self.getBytecode(self.compiled_sol)
        self.abi = self.getAbi(self.compiled_sol)
        self.w3 = Web3(Web3.HTTPProvider(w3provider))
        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        self.chain_id = chain_id
        self.sender_address = sender_address
        self.deployed = 0
        self.contractAddress = None



    @abstractmethod
    def getBytecode(self, _compiled_sol):
        pass

    @abstractmethod
    def getAbi(self, _compiled_sol):
        pass

    @abstractmethod
    def compileSol(self, _contract_file):
        pass

    @abstractmethod
    def createContractJson(self, _compiled_sol, _json_filename):
        pass
    

    def getContract(self):
        return self.contract
    
    @abstractmethod
    def encodeData(self, data):
        pass
    def submitUpdate(self, update_data, nonce, private_key):
        """
            Submits update to blockchain, returning transaction receipt
        """
        if (self.deployed == 0):
            raise Exception("Contract not deployed, try deploy instead!")
        # Build update transaction
        update_tx = self.w3.eth.contract(address = self.contractAddress, abi = self.abi)

        # Encode data for submitting
        data = self.encodeData(update_data)
        store_update = update_tx.functions.submitUpdate(data).build_transaction({
            "chainId": self.chain_id,
            "from": self.sender_address,
            "nonce": nonce
        })

        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(store_update, private_key = private_key)

        # Send transacton
        send_txn = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(send_txn)
        print(f"Successfully sent update!, transaction hash: {tx_receipt.transactionHash.hex()}")
        print(update_tx.functions.retrieve().call())
        return tx_receipt

    def deployContract(self, nonce, private_key):
        """
            Deploys contract to blockchain, returning transaction receipt
        """
        if (self.deployed == 1):
            raise Exception("Contract already deployed, try update instead!")
        # Build transaction
        transaction = self.contract.constructor().build_transaction({"chainId": self.chain_id, "from": self.sender_address, "nonce": nonce})
        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=private_key)
        # Send signed transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # Update attributes
        self.deployed = 1
        self.contractAddress = tx_receipt.contractAddress
        # get abi of contract

        print(f"successfully deployed! \n transaction hash: {tx_receipt.transactionHash.hex()}")
        return tx_receipt