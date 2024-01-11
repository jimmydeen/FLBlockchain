from listenerABC import EventHandler

class GlobalListener(EventHandler):
    def __init__(self, w3, contract_address, contract_abi):
        super().__init__(w3, contract_address, contract_abi)
        self.event_filter = self.contract_instance.events.GlobalModelUpdated.createFilter(fromBlock='latest')