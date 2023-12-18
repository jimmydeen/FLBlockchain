import flwr as fl

# Start Flower server
fl.server.start_server(
  server_address="127.0.0.1:7545",
  config=fl.server.ServerConfig(num_rounds=100),
)