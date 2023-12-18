import flwr as fl
import matplotlib.pyplot as plt

from demostrategy import DemoStrategy
strategy = DemoStrategy()
# Start Flower server
fl.server.start_server(
  server_address="127.0.0.1:7545",
  config=fl.server.ServerConfig(num_rounds=5), strategy=strategy
)

#plot

#plot loss
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.plot(range(len(strategy.losses)), strategy.losses, label= 'Loss')
plt.legend()
plt.title('Loss over rounds')

# Plot accuracy

plt.subplot(1,2,2)
plt.plot(range(len(strategy.accuracies)), strategy.accuracies, label = 'Accuracy')
plt.legend()
plt.title('Accuracy over rounds')

plt.show()
