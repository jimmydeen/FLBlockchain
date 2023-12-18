import flwr as fl

class DemoStrategy(fl.server.strategy.FedAvg):
    def __init__(self):
        super().__init__()
        self.accuracies = []
        self.losses = []
    
    def aggregate_fit(self, rnd, results, failures):
        #Store accuracies and losses
        for result in results:
            self.accuracies.append(result[1].metrics["accuracy"])
            self.losses.append(result[1].metrics["loss"])
        return super().aggregate_fit(rnd, results, failures)