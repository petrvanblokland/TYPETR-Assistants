# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   trainKernNetModel.py
#
import torch
import pytorch_lightning as pl
from torch.utils.data import Dataset, DataLoader
from os import path as osp
import os
try:
    from assistantLib.kernnet.kernNetClasses import KernNetDataloader, KernNet
except ImportError:
    #from kernnet.kernNetClasses import KernNetDataloader, KernNet
    from kernNetClasses import KernNetDataloader, KernNet


# This file contains a function to train a predictive kerning model using the KernNet class.
# The function is called with four parameters:
#   1. The path to the directory containing the data that the model will be trained on.
#   2. The number of training epochs that PyTorch will train the model for.
#   3. The fraction of training examples that will be used for model validation.
#   4. The batch size used during training.
#
# The script assumes that training images are stored as follows:
#
# Main_Directory (The path to this directory is what the function requires)
#
#   Sub_Directory_1
#       Image_1.png
#       ...
#       Image_X.png
#
#   ...
#
#   Sub_Directory_Y
#       Image_1.png
#       ...
#       Image_Z.png
#
#
# The function will work fine if there is only a single subdirectory.
# The subdirectories do not need to have the same number of images.
#
# Subdirectories currently follow this naming convention: Name_32_32
# Example: PrestiDeck-Book_32_32
#
# Single images follow this naming convention: LeftGlyphName_RightGlyphName_KerningValue
# Example: A.sc_ampersand.sc_-15
#
# The function has default values for training_epochs, validation_split and batch_size that should work in most cases.
#
# If the model isn't performing well, you can increase the number of training epochs.
# This could result in a better model, but will also increase training times.
#
# If the training process fails due to running out of RAM, you can lower the batch size.
# Make sure the batch size is always a power of 2.

W, H = 32, 32
SUB_DIR_PATTERN = f'{W}_{H}'
PATH = '_imageTrainSansItalic/'
PATH = '/Volumes/Archiv-T1/TYPETR-KernNet-TrainingImages-Italic/'

def train_model(data_directory_path, training_epochs=50, validation_split=0.3, batch_size=64):

    directory_list = os.listdir(data_directory_path)

    data = []

    for dir_name in directory_list:

        if not dir_name.endswith(SUB_DIR_PATTERN):
            continue
        #if not 'Italic' in dir_name:
        #    continue
        print('---', dir_name)
            
        for dir_name_sub in os.listdir(osp.join(data_directory_path, dir_name)):

            if not os.path.isdir(osp.join(data_directory_path, dir_name, dir_name_sub)):
                continue

            for file_name in os.listdir(osp.join(data_directory_path, dir_name, dir_name_sub)):

                if not file_name.endswith(".png"):
                    continue

                file_path = osp.join(dir_name, dir_name_sub, file_name)

                kern_value = int(round(float(file_name.replace(".png", "").split("_")[-1])))

                #if not kern_value:
                #    continue

                data_instance = (file_path, kern_value)

                data.append(data_instance)

    dataset = KernNetDataloader(data_directory_path, data)

    train_size = int((1 - validation_split) * len(dataset))
    valid_size = len(dataset) - train_size

    print(f'--- Train size {train_size} Valid size {valid_size}')

    train_set, val_set = torch.utils.data.random_split(dataset, [train_size, valid_size])

    train_loader = DataLoader(train_set, batch_size=batch_size, num_workers=0)
    val_loader = DataLoader(val_set, batch_size=batch_size, num_workers=0)

    model = KernNet()

    trainer = pl.Trainer(
        accelerator="cpu",
        devices=1,
        max_epochs=training_epochs,
        num_sanity_val_steps=0
    )

    trainer.fit(model=model, train_dataloaders=train_loader, val_dataloaders=val_loader)

if __name__ == "__main__":        
    train_model(PATH)
