from listenerABC import EventHandler
from web3 import Web3
import json
import datetime
import fcntl
import sys

class UpdateListener(EventHandler):
    def __init__(self, w3, contract_address, contract_abi):
        super().__init__(w3, contract_address, contract_abi)
        self.event_filter = self.contract_instance.events.UpdateSubmitted.create_filter(fromBlock="latest")

    def handle_event(self, event):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "client_id" : event.args._trainer,
            "timestamp": timestamp,
            "type": "update",
            "message": f"Update received from client: {event.args._trainer}\n",
            "txhash": event.transactionHash.hex()
        }
        self.append_to_events(data)
        # with open('progresslog.txt', 'a') as f:
        #     fcntl.flock(f, fcntl.LOCK_EX)  # Acquire an exclusive lock
        #     f.write(f"[{timestamp}] Update Received! \n \n")
        #     f.write(f"Update received from client: {event.args._trainer}\n")
        #     f.write(f"Tx Hash: {event.transactionHash.hex()}\n \n \n")
        #     # f.write(f"Number of data points: {event.args._numDatapoints}\n")
        #     # f.write(f"Reward amount: {event.args._reward}\n")
        #     fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock
    def append_to_events(self, event_json):
        with open("/Users/jd/Desktop/work/FLBlockchain/flask/serverdata.json", "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # Acquire an exclusive lock

            try:
                server_data = json.load(f)

                # If the "events" key doesn't exist, initialize it to an empty list
                if 'events' not in server_data:
                    server_data['events'] = []

                # Append the event_json to the "events" list
                server_data['events'].append(event_json)

                # Write the updated server data back to the file
                f.seek(0)
                json.dump(server_data, f)
                f.truncate()

            except json.JSONDecodeError:
                # If the file is empty (and thus not valid JSON), initialize "events" to a list containing the event_json
                f.seek(0)
                json.dump({'events': [event_json]}, f)
                f.truncate()

            finally:
                fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock


if __name__ == "__main__":
    web3endpoint = sys.argv[1]
    contract_address = sys.argv[2]
    contract_abi = json.loads(sys.argv[3])
    listener = UpdateListener(web3endpoint, contract_address, contract_abi)
    listener.listen()