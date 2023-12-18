from collections import OrderedDict
import warnings

import flwr as fl
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import Compose, ToTensor, Normalize
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10

# #############################################################################
# Regular PyTorch pipeline: nn.Module, train, test, and DataLoader
# #############################################################################

warnings.filterwarnings("ignore", category=UserWarning)
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Net(nn.Module):
  """Model (simple CNN adapted from 'PyTorch: A 60 Minute Blitz')"""

  def __init__(self) -> None:
    super(Net, self).__init__()
    self.conv1 = nn.Conv2d(1, 6, 5)
    self.pool = nn.MaxPool2d(2, 2)
    self.conv2 = nn.Conv2d(6, 16, 5)
    self.fc1 = nn.Linear(16 * 4 * 4, 120)
    self.fc2 = nn.Linear(120, 84)
    self.fc3 = nn.Linear(84, 10)

  def forward(self, x: torch.Tensor) -> torch.Tensor:
    x = self.pool(F.relu(self.conv1(x)))
    x = self.pool(F.relu(self.conv2(x)))
    x = x.view(-1, 16 * 4 * 4)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    return self.fc3(x)

def train(net, trainloader, epochs):
  """Train the model on the training set."""
  criterion = torch.nn.CrossEntropyLoss()
  optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
  total_loss = 0.0
  total_correct = 0
  total_images = 0
  for _ in range(epochs):
    for images, labels in trainloader:
      optimizer.zero_grad()
      outputs = net(images.to(DEVICE))
      loss = criterion(outputs, labels.to(DEVICE))
      loss.backward()
      optimizer.step()

      total_loss += loss.item() * images.size(0)
      _, predicted = torch.max(outputs.data, 1)
      total_correct += (predicted == labels.to(DEVICE)).sum().item()
      total_images += images.size(0)
  average_loss = total_loss / total_images
  accuracy = total_correct / total_images
  return average_loss, accuracy

def test(net, testloader):
  """Validate the model on the test set."""
  criterion = torch.nn.CrossEntropyLoss()
  correct, total, loss = 0, 0, 0.0
  with torch.no_grad():
    for images, labels in testloader:
      outputs = net(images.to(DEVICE))
      loss += criterion(outputs, labels.to(DEVICE)).item()
      total += labels.size(0)
      correct += (torch.max(outputs.data, 1)[1] == labels).sum().item()
  return loss / len(testloader.dataset), correct / total

def load_data():
  """
    Data loader unneeded for demo, returns a tuple of train, test data
  """
  raise NotImplementedError

