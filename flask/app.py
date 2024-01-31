from flask import Flask, request, make_response
import sys
sys.path.append('/Users/jd/Desktop/work/FLBlockchain/integration/')
from coordinatorcontract import CoordinatorContract
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/download_client', methods=['POST'])
def download_client():
    _client_address = request.json.get('_client_address')
    _client_pk = request.json.get('_client_pk')
    _web3_endpoint = request.json.get('_web3_endpoint')
    _chainid = request.json.get('_chainid')
    _contract_address = request.json.get('_contract_address')
    _contract_abi = request.json.get('_contract_abi')
    server_address = request.json.get('server_address')

    script = f"""
from main import mnist_test_loader_client1, mnist_train_loader_client1
from flclient import FlowerClient
import flwr as fl
import json

class c1(FlowerClient):
    def __init__(self):
        super().__init__("{_client_address}", "{_client_pk}", "{_web3_endpoint}", {_chainid}, "{_contract_address}", {_contract_abi})

    def getTrainLoader(self):
        return mnist_train_loader_client1

    def getTestLoader(self):
        return mnist_test_loader_client1

if __name__ == "__main__":
    client = c1()
    fl.client.start_numpy_client(server_address="{server_address}", client=client)
    """

    response = make_response(script)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=client.py'

    return response

@app.route('/start_server', methods=['POST'])
def start_server():
    subprocess.Popen(["python", "flower/flserver.py"])
    return 'Server started', 200

@app.route('/start_client', methods=['POST'])
def start_client():
    _client_address = request.json.get('_client_address')
    _client_pk = request.json.get('_client_pk')
    _web3_endpoint = request.json.get('_web3_endpoint')
    _chainid = request.json.get('_chainid')
    _contract_address = request.json.get('_contract_address')
    _contract_abi = request.json.get('_contract_abi')
    server_address = request.json.get('server_address')

    # Start c1.py with the provided parameters
    subprocess.Popen(['python', 'c1.py', _client_address, _client_pk, _web3_endpoint, str(_chainid), _contract_address, json.dumps(_contract_abi), server_address])

    return 'Client started', 200

@app.route('/deploy_contract', methods=['POST'])
def deploy_contract():
    contract_path = request.json.get('contract_path')
    w3provider = request.json.get('w3provider')
    chain_id = request.json.get('chain_id')
    sender_address = request.json.get('sender_address')
    private_key = request.json.get('private_key')
    incentive = request.json.get('incentive')
    numberUpdatesRequested = request.json.get('numberUpdatesRequested')
    maxDataPoints = request.json.get('maxDataPoints')
    stake = request.json.get('stake')




    # # Instantiate the CoordinatorContract class
    # contract = CoordinatorContract(contract_path, w3provider, chain_id, sender_address, private_key)

    # # Call the deployContract method
    # contract.deployContract(incentive, numberUpdatesRequested, maxDataPoints, stake)

    

    return 'Contract deployed', 200

if __name__ == '__main__':
    app.run(port=5000)