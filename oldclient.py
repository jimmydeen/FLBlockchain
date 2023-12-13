
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()
install_solc('0.8.9')

with open("./ClientUpdate.sol", "r") as file:
    clientUpdate = file.read()
    # print(simple_storage_file)

# Compile solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"clientUpdate.sol": {"content": clientUpdate}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.9",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)



#get bytecode
bytecode = compiled_sol["contracts"]["clientUpdate.sol"]["ClientUpdate"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["clientUpdate.sol"]["ClientUpdate"]["abi"]

w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac"))
chain_id = 11155111 
my_address = "0x140c8BB040e47123CEF96Cd36005128B1fA72a78"

private_key = os.getenv("PRIVATE_KEY")


#create contract in python
ClientUpdate = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)


# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = ClientUpdate.constructor().build_transaction({"chainId": chain_id, "from": my_address, "nonce": nonce})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send this signed transaction

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Working with the contract

# Contract address
# Contract ABI
update_tx = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#call -> simulate making the call and getting a return value
# transact -> actually make a state change

test_data = "hello world".encode()
store_update = update_tx.functions.submitUpdate(test_data).build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1
})


signed_store_txn = w3.eth.account.sign_transaction(store_update, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(update_tx.functions.retrieve().call())






