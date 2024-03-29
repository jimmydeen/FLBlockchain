from flask import Flask, request, make_response, jsonify, session, send_file
from flask_cors import CORS

import sys
import subprocess
import os
import json

app = Flask(__name__)

CORS(app, always_send = True)
# Global variables for demo

SERVER_DATA_FILE = "/Users/jd/Desktop/work/FLBlockchain/flask/serverdata.json"
app.secret_key = "demo"


@app.route('/download_client', methods=['POST'])
def download_client():
    _client_address = request.json.get('_client_address')
    _client_pk = request.json.get('_client_pk')
    with open(SERVER_DATA_FILE, 'r') as f:
            server_data = json.load(f)
    _web3_endpoint = server_data["w3provider"]
    _chainid = server_data["chain_id"]
    _contract_address = server_data["contract_address"]
    _contract_abi = json.dumps(server_data["contract_abi"])
    server_address = server_data["server_address"]

    script = f"""

    ./download_client {_client_address} {_client_pk} {_web3_endpoint} {_chainid} {_contract_address} {_contract_abi} {server_address} 


    """

    response = make_response(script)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=run_client.sh'

    return response

@app.route('/start_server', methods=['POST'])
def start_server():
    server_address = request.json.get('_server_address')
    
    if os.path.exists(SERVER_DATA_FILE):
        with open(SERVER_DATA_FILE, 'r') as f:
            server_data = json.load(f)
    else:
        raise LookupError("Server data file not found")
    
    server_data["server_started"] = True
    server_data["server_address"] = server_address
    with open(SERVER_DATA_FILE, 'w') as f:
        json.dump(server_data, f)
    # Load parameters from serverdata, to pass into rewardlistener and updatelistener
    # w3provider = server_data.get("w3provider")
    w3provider = "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac"
    contract_address = server_data["contract_address"]
    contract_abi = json.dumps(server_data["contract_abi"])
    
    if w3provider is None or contract_address is None or contract_abi is None:
        raise ValueError("Missing parameters in server data")

    # Start reward listener process with parameters
    subprocess.Popen(["python", "/Users/jd/Desktop/work/FLBlockchain/integration/rewardlistener.py", w3provider, contract_address, contract_abi])

    # Start update listener process with parameters
    subprocess.Popen(["python", "/Users/jd/Desktop/work/FLBlockchain/integration/updatelistener.py", w3provider, contract_address, contract_abi])

    # Start server
    subprocess.run(["python", "/Users/jd/Desktop/work/FLBlockchain/flower/flserver.py", server_address])

    with open (SERVER_DATA_FILE, 'r') as f:
        server_data = json.load(f)
    
    server_data["training_complete"] = True
    with open(SERVER_DATA_FILE, 'w') as f:
        json.dump(server_data, f)
        
    return 'Server started', 200

# Demo Endpoints

@app.route('/start_client1', methods=['POST'])
def start_client_1():
    _client_address = request.json.get('_client_address')
    _client_pk = request.json.get('_client_pk')

    # Save client address to session to identify client
    session['client_id'] = _client_address
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
    # Save client address to session to identify client
    session['client_id'] = _client_address
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
    # Save client address to session to identify client
    session['client_id'] = _client_address
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

    # process = subprocess.run(["python", "/Users/jd/Desktop/work/FLBlockchain/integration/deploycontract.py", w3provider, str(chain_id), sender_address, private_key, str(incentive), str(numberUpdatesRequested), str(maxDataPoints), str(stake)], capture_output=True, text = True)
    process = subprocess.run(["python", "/Users/jd/Desktop/work/FLBlockchain/integration/deploycontract.py"])
    print(process.stdout)
    if process.returncode != 0:
        print(f"Error: deploycontract.py exited with status {process.returncode}")
    else:
        print("contract deploy success!")

    

    return "contract deployed", 200




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

    update_exists = False
    if os.path.exists(SERVER_DATA_FILE):
        with open(SERVER_DATA_FILE, 'r') as f:
            server_data = json.load(f)
            updates = server_data.get("events", "")
            if updates == "":
                update_exists = False
            else:
                update_exists = True
    # check for completion
    if server_data.get("training_complete", False):
        return "Training complete", 201

    if update_exists == True:
        return updates, 200
    else:
        return "No events yet", 202


@app.route('/getClientSummary', methods=['GET'])
def getClientSummary():
    client_id = session.get('client_id')
    if client_id is None:
        return jsonify({"error": "No client summary yet"}), 400

    with open(SERVER_DATA_FILE, 'r') as f:
        server_data = json.load(f)
    events = server_data.get("events", [])
    client_events = [event for event in events if event.get("client_id") == client_id and "client_id" in event]

    if not client_events:
        return jsonify({"message": f"No events for client {client_id} yet"}), 202

    total_incentive = 0
    updates_trained = 0
    client_log = client_events

    # Calculate total incentive and updates trained
    for event in client_events:
        if event.get("type") == "reward":
            total_incentive += event.get("reward", 0)
        elif event.get("type") == "update":
            updates_trained += 1


    response = {
        "client_id": client_id,
        "total_incentive": total_incentive,
        "updates_trained": updates_trained,
        "client_log": client_log
    }

    return jsonify(response), 200

@app.route('/getPlot', methods=['GET'])
def getPlot():
    return send_file('plot.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(port=8000)