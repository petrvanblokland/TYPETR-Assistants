This file goes over the dependencies of KernNet so far.


PyTorch Imports:
- import torch
- from torchvision import transforms
- import torch.nn as nn
- import torch.nn.functional as F
- import pytorch_lightning as pl
- from torch.utils.data import Dataset
- import pytorch_lightning as pl
- from torch.utils.data import Dataset, DataLoader
- from torchvision import transforms

To install PyTorch properly, use the following link:
https://pytorch.org/get-started/locally/

Choose the options based on your system, and for Cuda choose 11.7.
It's possible that Cuda 11.8 also works, but this version was developed on 11.7, so no guarantees.

Once you've selected all the correct options, use the pip / conda commanded wherever you want to run KernNet.

Common Imports:
- from os import path as osp
- import os
- from PIL import Image
- import PIL
- import numpy as np

These imports should be fine to download directly via pip / conda.

How to import KernNet:
- from KernNet import TrainKernNetModel, PredictKernNetModel, KernNetClasses

Once you've imported one of the files, you can do TrainKernNetModel.train_model() to use the functions. See KernNetUsageExample.py for an example.


