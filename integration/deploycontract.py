import sys
import json
sys.path.insert(0, '/Users/jd/Desktop/work/FLBlockchain/integration/')

from coordinatorcontract import CoordinatorContract
import os
os.chdir("/Users/jd/Desktop/work/FLBlockchain/")
# web3endpoint = sys.argv[1]
# chainid = int(sys.argv[2])
# sender_address = sys.argv[3]
# sender_pk = sys.argv[4]
# incentive = int(sys.argv[5])
# numberUpdatesRequested = int(sys.argv[6])
# maxDataPoints = int(sys.argv[7])
# stake = float(sys.argv[8])
contract = CoordinatorContract("/Users/jd/Desktop/work/FLBlockchain/integration/SimpleCoordinator.sol", "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", 11155111, "0x504d73C974b2a9550eBCBFCA78F81AeC01B1c7C6", "2d656220c6b6917ce39055aeace0423d984166c72aa927fd3cea9e147406d072")
contract.deployContract(1, 1, 1, 0.0001)

# contract = CoordinatorContract("/Users/jd/Desktop/work/FLBlockchain/integration/SimpleCoordinator.sol", web3endpoint, chainid, sender_address, sender_pk)
# contract.deployContract(incentive, numberUpdatesRequested, maxDataPoints, stake)

# time.sleep(5)
# Get contract address and abi
contract_address = contract.contractAddress
contract_abi = contract.abi

with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'w') as f:
    json.dump({"address": contract_address, "abi": contract_abi}, f)

# Write to SERVER_DATA_FILE for demo
    
server_data_file = '/Users/jd/Desktop/work/FLBlockchain/flask/serverdata.json'

if os.path.exists(server_data_file) and os.stat(server_data_file).st_size != 0:
    with open(server_data_file, 'r') as f:
        server_data = json.load(f)
else:
    server_data = {}

server_data["contract_address"] = contract_address
server_data["contract_abi"] = contract_abi

with open(server_data_file, 'w') as f:
    json.dump(server_data, f)

# with open('/Users/jd/Desktop/work/FLBlockchain/flask/serverdata.json', 'w') as f:
#     json.dump(server_data, f)



print("contract deploy success!")