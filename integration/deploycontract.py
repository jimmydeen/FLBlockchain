import sys
import json
sys.path.insert(0, '/Users/jd/Desktop/work/FLBlockchain/integration/')

from coordinatorcontract import CoordinatorContract
 



contract = CoordinatorContract("/Users/jd/Desktop/work/FLBlockchain/integration/SimpleCoordinator.sol", "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", 11155111, "0x504d73C974b2a9550eBCBFCA78F81AeC01B1c7C6", "2d656220c6b6917ce39055aeace0423d984166c72aa927fd3cea9e147406d072")
contract.deployContract(10000, 5, 1000, 0.05)

# time.sleep(5)
# Get contract address and abi
contract_address = contract.contractAddress
contract_abi = contract.abi

with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'w') as f:
    json.dump({"address": contract_address, "abi": contract_abi}, f)


print("contract deploy success!")