import sys
sys.path.append('/Users/jd/Desktop/work/FLBlockchain/blockchain')

from contractABC import ContractABC
from solcx import compile_standard, install_solc
import json


install_solc("v0.8.20")

class CoordinatorContract(ContractABC):

    def __init__(self, contract_path, w3provider, chain_id, sender_address, private_key):
        super().__init__(contract_path, w3provider, chain_id, sender_address)
        self.private_key = private_key
        self.createContractJson(self.compiled_sol, "coordinator_json")

    # Add the abstract methods from ContractABC
    def getBytecode(self, _compiled_sol):
        return _compiled_sol['contracts']['SimpleCoordinator.sol']['SimpleCoordinator']['evm']['bytecode']['object']
    def getAbi(self, _compiled_sol):
        return _compiled_sol['contracts']['SimpleCoordinator.sol']['SimpleCoordinator']['abi']
    def compileSol(self, _contract_path):
        with open(_contract_path, 'r') as file:
            contract_file = file.read()
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"SimpleCoordinator.sol": {"content": contract_file}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version= "0.8.20",
        )

        return compiled_sol

    def createContractJson(self, _compiled_sol, _json_filename):
        with open(_json_filename + ".json", "w") as file:
            json.dump(_compiled_sol, file)
    
    def encodeData(self, data):
        return data.encode()

    # Deploy with a payment of 0.5 ETH
    def deployContract(self, incentive, numberUpdatesRequested, maxDataPoints, stake):
        nonce = self.w3.eth.get_transaction_count(self.sender_address)
        # Build deployment transaction
        deploy_txn = self.contract.constructor(incentive, numberUpdatesRequested, maxDataPoints).build_transaction({
            "chainId": self.chain_id,
            "from": self.sender_address,
            "nonce": nonce,
            "value": self.w3.to_wei(stake, "ether")
        })
        # Sign and send
        signed = self.w3.eth.account.sign_transaction(deploy_txn, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        # Wait for transaction to be mined
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # Set contract address
        self.contractAddress = tx_receipt.contractAddress
        self.deployed = 1
        return tx_receipt