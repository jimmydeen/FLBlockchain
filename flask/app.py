from flask import Flask, request, make_response, jsonify, session
import sys
sys.path.append('/Users/jd/Desktop/work/FLBlockchain/integration/')
from coordinatorcontract import CoordinatorContract
import subprocess
import os
import json

app = Flask(__name__)
# Global variables for demo

SERVER_DATA_FILE = "/Users/jd/Desktop/work/FLBlockchain//server_data.json"
app.secret_key = "demo"


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


    # global SERVER_STARTED
    # global SERVER_ADDRESS
    server_address = request.json.get('_server_address')
    
    if os.path.exists(SERVER_DATA_FILE):
        with open(SERVER_DATA_FILE, 'r') as f:
            server_data = json.load(f)
    else:
        server_data = {}
   
    server_data["server_started"] = True
    server_data["server_address"] = server_address
    #start reward and update listeners
    subprocess.Popen(["python", "/Users/jd/Desktop/work/FLBlockchain/integration/rewardlistener.py"])
    subprocess.Popen(["python", "/Users/jd/Desktop/work/FLBlockchain/integration/updatelistener.py"])
    subprocess.Popen(["python", "/Users/jd/Desktop/work/FLBlockchain/flower/flserver.py"])
    
    with open(SERVER_DATA_FILE, 'w') as f:
        json.dump(server_data, f)
    return 'Server started', 200

# Demo Endpoints

@app.route('/start_client1', methods=['POST'])
def start_client_1():
    _client_address = request.json.get('_client_address')
    _client_pk = request.json.get('_client_pk')
    # Load data from SERVER_DATA_FILE
    with open(SERVER_DATA_FILE, 'r') as f:
        server_data = json.load(f)
    
    _web3_endpoint = server_data["w3provider"]
    _chainid = server_data["chain_id"]
    _contract_address = server_data["contract_address"]
    _contract_abi = server_data["contract_abi"]
    _server_address = server_data["server_address"]

    # Start c1.py with the provided parameters
    subprocess.Popen(['python', '/Users/jd/Desktop/work/FLBlockchain/flower/c1.py', _client_address, _client_pk, _web3_endpoint, str(_chainid), _contract_address, json.dumps(_contract_abi), _server_address])

    return 'Client 1 started', 200

@app.route('/start_client2', methods=['POST'])
def start_client_2():
    _client_address = request.json.get('_client_address')
    _client_pk = request.json.get('_client_pk')
    with open(SERVER_DATA_FILE, 'r') as f:
        server_data = json.load(f)
    
    _web3_endpoint = server_data["w3provider"]
    _chainid = server_data["chain_id"]
    _contract_address = server_data["contract_address"]
    _contract_abi = server_data["contract_abi"]
    _server_address = server_data["server_address"]

    # Start c1.py with the provided parameters
    subprocess.Popen(['python', '/Users/jd/Desktop/work/FLBlockchain/flower/c2.py', _client_address, _client_pk, _web3_endpoint, str(_chainid), _contract_address, json.dumps(_contract_abi), _server_address])

    return 'Client 2 started', 200

@app.route('/start_client3', methods=['POST'])
def start_client_3():
    _client_address = request.json.get('_client_address')
    _client_pk = request.json.get('_client_pk')
    with open(SERVER_DATA_FILE, 'r') as f:
        server_data = json.load(f)
    
    _web3_endpoint = server_data["w3provider"]
    _chainid = server_data["chain_id"]
    _contract_address = server_data["contract_address"]
    _contract_abi = server_data["contract_abi"]
    _server_address = server_data["server_address"]

    # Start c1.py with the provided parameters
    subprocess.Popen(['python', '/Users/jd/Desktop/work/FLBlockchain/flower/c3.py', _client_address, _client_pk, _web3_endpoint, str(_chainid), _contract_address, json.dumps(_contract_abi), _server_address])

    return 'Client 3 started', 200


@app.route('/deploy_contract', methods=['POST'])
def deploy_contract():
    # contract_path = request.json.get('contract_path')
    w3provider = request.json.get('w3provider')
    chain_id = request.json.get('chain_id')
    sender_address = request.json.get('sender_address')
    private_key = request.json.get('private_key')
    incentive = request.json.get('incentive')
    numberUpdatesRequested = request.json.get('numberUpdatesRequested')
    maxDataPoints = request.json.get('maxDataPoints')
    stake = request.json.get('stake')

    # write the w3provider, chain_id to SERVER_DATA_FILE
    if os.path.exists(SERVER_DATA_FILE):
        with open(SERVER_DATA_FILE, 'r') as f:
            server_data = json.load(f)
    else:
        server_data = {}

    server_data["w3provider"] = w3provider
    server_data["chain_id"] = chain_id

    with open(SERVER_DATA_FILE, 'w') as f:
        json.dump(server_data, f)

    subprocess.run(["python", "/Users/jd/Desktop/work/FLBlockchain/integration/deploycontract.py", w3provider, str(chain_id), sender_address, private_key, str(incentive), str(numberUpdatesRequested), str(maxDataPoints), str(stake)])

    # Load contract data

    with open("/Users/jd/Desktop/work/FLBlockchain/integration/contract_data.json", "r") as f:
        data = json.load(f)
    
    contract_address = data["address"]
    contract_abi = data["abi"]

    return jsonify({
        'contract_address': contract_address,
        'contract_abi': contract_abi
    }), 200


@app.route('/check_server', methods=['GET'])
def check_server():
    server_started = False
    if os.path.exists(SERVER_DATA_FILE):
        with open(SERVER_DATA_FILE, 'r') as f:
            server_data = json.load(f)
        server_started = server_data.get('server_started', False)

    if server_started:
        return 'Server started', 200
    else:
        return 'Server not started', 202

@app.route('/get_events', methods=['GET'])
def get_events():
    if os.path.exists("/Users/jd/Desktop/work/FLBlockchain/progresslog.txt"):
        with open("/Users/jd/Desktop/work/FLBlockchain/progresslog.txt", 'r') as f:
            progress = f.read()
            if progress == "":
                update_exists = False
            else:
                update_exists = True

    if update_exists == True:

        return jsonify({
            "progresslog": progress
        }), 200
    else:
        return "No events yet", 202

if __name__ == '__main__':
    app.run(port=5000)