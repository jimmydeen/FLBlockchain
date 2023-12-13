import json
from contractABC import ContractABC
from solcx import compile_standard, install_solc
install_solc('0.8.9')

class ClientContract(ContractABC):
    def __init__(self, contract_path, w3provider, chain_id, sender_address):
        super().__init__(contract_path, w3provider, chain_id, sender_address)
        self.createContractJson(self.compiled_sol, "client_json")

    # Add the abstract methods from ContractABC
    def getBytecode(self, _compiled_sol):
        return _compiled_sol['contracts']['Client.sol']['Client']['evm']['bytecode']['object']
    def getAbi(self, _compiled_sol):
        return _compiled_sol['contracts']['Client.sol']['Client']['abi']
    def compileSol(self, _contract_file):
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"Client.sol": {"content": _contract_file}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
        )
        return compiled_sol

    def createContractJson(self, _compiled_sol, _json_filename):
        with open(_json_filename + ".json", "w") as file:
            json.dump(_compiled_sol, file)
        
    def encodeData(self, data):
        return data.encode()
