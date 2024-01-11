from listenerABC import EventHandler
import time
class AggregateListener(EventHandler):
    def __init__(self, w3, contract_address, contract_abi):
        super().__init__(w3, contract_address, contract_abi)
        self.event_filter = self.contract_instance.events.AggregationRequired.createFilter(fromBlock='latest')

    def startListener(self):
        while True:
            for event in self.event_filter.get_new_entries():
                self.handle_event(event)
            time.sleep(10)
            
    def handle_event(self, event):
        newModelNumber = event.args.modelNumber + 1

        # Aggregate the data using weighted averaging (FedAvg)

        

