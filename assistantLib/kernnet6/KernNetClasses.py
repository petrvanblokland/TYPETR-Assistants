import random
import sys

import PIL
import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os
import rasterio
import numpy as np
import datetime
from PIL import Image
from torchvision.transforms import transforms


class KernNet(torch.nn.Module):
    def __init__(self):
        super(KernNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 1)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class KernNetTrainingDataloader(Dataset):
    def __init__(self, data_path, data_list, device):
        self.data_path = data_path
        self.data_list = data_list
        self.device = device

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        data = self.data_list[idx]

        pair_name = data[0]
        label = (data[1] + 500) / 1000

        image = PIL.Image.open(pair_name)

        r, g, b, a = image.split()

        transformer = transforms.Compose([
            transforms.ToTensor(),
        ])

        data_tensor = transformer(a)

        return data_tensor, label


class KernNetInferenceDataloader(Dataset):
    def __init__(self, data_path, data_list, device):
        self.data_path = data_path
        self.data_list = data_list
        self.device = device

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        data = self.data_list[idx]

        pair_name = data

        image = PIL.Image.open(pair_name)

        r, g, b, a = image.split()

        transformer = transforms.Compose([
            transforms.ToTensor(),
        ])

        data_tensor = transformer(a)

        data_tensor = data_tensor.to(self.device)

        return data_tensor


