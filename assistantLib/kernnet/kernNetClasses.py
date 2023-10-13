# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   kernNetClasses.py
#
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torch.utils.data import Dataset
from torchvision import transforms

from PIL import Image
import PIL



# This file contains the classes for the Dataloader and PyTorch model structure.
# They've been put in a separate file since both PredictKernNetModel and TrainKernNetModel need the classes.
# At the moment the model architecture only allows for input images that are 32x32 pixels.


class KernNetDataloader(Dataset):
    def __init__(self, data_path, data_list):
        self.data_path = data_path
        self.data_list = data_list

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        data = self.data_list[idx]

        pair_name = data[0]
        kerning_value = (data[1] + 500) / 1000

        label = kerning_value

        image = PIL.Image.open(self.data_path + "/" + pair_name)

        r, g, b, a = image.split()

        transformer = transforms.Compose([
            transforms.RandomHorizontalFlip(0.5),
            transforms.RandomVerticalFlip(0.1),
            transforms.ToTensor(),
        ])

        data_tensor = transformer(a)

        return data_tensor, label


class KernNet(pl.LightningModule):

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 1)

    def training_step(self, batch, batch_idx):

        x, y = batch

        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        y_hat = x.squeeze()

        loss = torch.sqrt(nn.functional.mse_loss(y_hat, y.float()))

        return loss

    def validation_step(self, batch, batch_idx):

        x, y = batch

        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        y_hat = x.squeeze()

        loss = torch.sqrt(nn.functional.mse_loss(y_hat, y.float()))

        return loss

    def configure_optimizers(self):
        return [torch.optim.Adam(self.parameters(), lr=0.004)]

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
