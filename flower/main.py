from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import numpy as np


# Transformations
transform = transforms.Compose([transforms.ToTensor()])

# Load MNIST
mnist_train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
mnist_test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)




def split_pytorch_dataset(dataset, num_splits):
    length = len(dataset)
    indices = list(range(length))
    # Shuffle indices
    np.random.shuffle(indices)
    # Split indices into num_splits
    split_len = length // num_splits
    # Create subsets
    return [Subset(dataset, indices[i*split_len:(i+1)*split_len]) for i in range(num_splits)]

# Split MNIST
mnist_train_partitions = split_pytorch_dataset(mnist_train_dataset, 3)
mnist_test_partitions = split_pytorch_dataset(mnist_test_dataset, 3)


batch_size = 128  # Set your batch size- medium size for this demo

# Data loaders for MNIST DEMO ONLY
mnist_train_loader_client1 = DataLoader(mnist_train_partitions[0], batch_size=batch_size, shuffle=True)
mnist_test_loader_client1 = DataLoader(mnist_test_partitions[0], batch_size=batch_size, shuffle=True)
mnist_train_loader_client2 = DataLoader(mnist_train_partitions[1], batch_size=batch_size, shuffle=True)
mnist_test_loader_client2 = DataLoader(mnist_test_partitions[1], batch_size=batch_size, shuffle=True)
mnist_train_loader_client3 = DataLoader(mnist_train_partitions[2], batch_size=batch_size, shuffle=True)
mnist_test_loader_client3 = DataLoader(mnist_test_partitions[2], batch_size=batch_size, shuffle=True)