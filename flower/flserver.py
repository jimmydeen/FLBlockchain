import flwr as fl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
sys.path.insert(0, '../integration/')

from coordinatorcontract import CoordinatorContract
 
from demostrategy import DemoStrategy
strategy = DemoStrategy()

# Initialise smart contract components
contract = CoordinatorContract("../integration/SimpleCoordinator.sol", "https://sepolia.infura.io/v3/c0145f17136443228ae9d8ab299d3aac", 11155111, "0x504d73C974b2a9550eBCBFCA78F81AeC01B1c7C6", "2d656220c6b6917ce39055aeace0423d984166c72aa927fd3cea9e147406d072")
contract.deployContract()



# Start Flower server
fl.server.start_server(
  server_address="127.0.0.1:7545",
  config=fl.server.ServerConfig(num_rounds=5), strategy=strategy
)
# Plot
# format percentage
formatPercent = ticker.FuncFormatter(lambda x, _: '{:0.0f}%'.format(x*100))
# Plot loss
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.plot(range(len(strategy.losses)), strategy.losses, label= 'Loss')
# plt.legend()
plt.xlabel('Round')
plt.ylabel('Loss')
plt.title('Loss over rounds')

# Plot accuracy

plt.subplot(1,2,2)
plt.plot(range(len(strategy.accuracies)), strategy.accuracies, label = 'Accuracy')
plt.gca().yaxis.set_major_formatter(formatPercent)
# plt.legend()
plt.title('Accuracy over rounds')
plt.xlabel('Round')
plt.ylabel('Accuracy %')
plt.show()



