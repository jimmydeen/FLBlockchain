import json

from solcx import compile_standard
from contractABC import ContractABC

class ClientContract(ContractABC):
    def __init__(self, contract_path, w3provider, chain_id, sender_address):
        super().__init__(contract_path, w3provider, chain_id, sender_address)
        self.createContractJson(self.compiled_sol, "client_json")

    # Add the abstract methods from ContractABC
    def getBytecode(self, _compiled_sol):
        return _compiled_sol['contracts']['Client.sol']['ClientUpdate']['evm']['bytecode']['object']
    def getAbi(self, _compiled_sol):
        return _compiled_sol['contracts']['Client.sol']['ClientUpdate']['abi']
    def compileSol(self, _contract_path):
        with open(_contract_path, 'r') as file:
            contract_file = file.read()
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"Client.sol": {"content": contract_file}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version= "0.8.9",
        )
        return compiled_sol

    def createContractJson(self, _compiled_sol, _json_filename):
        with open(_json_filename + ".json", "w") as file:
            json.dump(_compiled_sol, file)
        
    def encodeData(self, data):
        return data.encode()
