import sys
import json
sys.path.insert(0, '/Users/jd/Desktop/work/FLBlockchain/integration/')

from coordinatorcontract import CoordinatorContract
 
web3endpoint = sys.argv[1]
chainid = int(sys.argv[2])
sender_address = sys.argv[3]
sender_pk = sys.argv[4]
incentive = int(sys.argv[5])
numberUpdatesRequested = int(sys.argv[6])
maxDataPoints = int(sys.argv[7])
stake = float(sys.argv[8])


contract = CoordinatorContract("/Users/jd/Desktop/work/FLBlockchain/integration/SimpleCoordinator.sol", web3endpoint, chainid, sender_address, sender_pk)
contract.deployContract(incentive, numberUpdatesRequested, maxDataPoints, stake)

# time.sleep(5)
# Get contract address and abi
contract_address = contract.contractAddress
contract_abi = contract.abi

with open('/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json', 'w') as f:
    json.dump({"address": contract_address, "abi": contract_abi}, f)

# Write to SERVER_DATA_FILE for demo
    
with open('/Users/jd/Desktop/work/FLBlockchain/flask/serverdata.json', 'r') as f:
    server_data = json.load(f)

server_data["contract_address"] = contract_address
server_data["contract_abi"] = contract_abi

with open('/Users/jd/Desktop/work/FLBlockchain/flask/serverdata.json', 'w') as f:
    json.dump(server_data, f)



print("contract deploy success!")