from client import Client
import os
from dotenv import load_dotenv
from solcx import install_solc
install_solc("0.8.9")
load_dotenv()

w3 = "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac"
chain_id = 11155111 
my_address = "0x140c8BB040e47123CEF96Cd36005128B1fA72a78"

private_key = os.getenv("PRIVATE_KEY")
testClient = Client(w3, my_address, private_key, chain_id)
testClient.deployContract()
testClient.submitUpdate("test")

    