import random
import sys

import PIL
import numpy
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os
import numpy as np
from PIL import Image
import os.path
from torchvision import transforms
from tqdm.auto import tqdm

from KernNetClasses import KernNet, KernNetTrainingDataloader, KernNetInferenceDataloader
from KernNetEvaluation import prepare_model_directories, create_training_report, create_inference_report

#DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'
#DEVICE = 'mps' 
DEVICE = 'cpu'

BATCH_SIZE = 128

def train_single_epoch(model, training_dataloader, loss_function, optimizer, device, epoch):

    running_loss = 0
    last_loss = 0

    total_data_length = len(training_dataloader)

    tqdm_enumerator = tqdm(training_dataloader)

    for index, data in enumerate(tqdm_enumerator):

        inputs, labels = data

        labels = labels.type(torch.FloatTensor)

        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs).squeeze(1)

        loss = loss_function(outputs, labels)
        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        tqdm_enumerator.set_description(f"EPOCH {epoch} Training")
        tqdm_enumerator.set_postfix(loss=(running_loss / total_data_length))

        if index + 1 == total_data_length:
            last_loss = running_loss / total_data_length  # loss per batch

    return last_loss


def train_model(model_identifier,
                models_directory_path,
                training_data_path,
                epoch_count=50,
                validation_set_fraction=0.3,
                learning_rate=0.001,
                batch_size=BATCH_SIZE,
                ):

    device = torch.device(DEVICE)

    data = discover_training_images(training_data_path)

    dataset = KernNetTrainingDataloader(training_data_path, data, device)

    train_size = int((1 - validation_set_fraction) * len(dataset))
    valid_size = len(dataset) - train_size

    train_set, val_set = torch.utils.data.random_split(dataset, [train_size, valid_size])

    training_dataloader = DataLoader(train_set, batch_size=batch_size, num_workers=5)
    validation_dataloader = DataLoader(val_set, batch_size=batch_size, num_workers=5)

    model = KernNet()

    model.to(device)

    loss_function = torch.nn.MSELoss()

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    current_epoch = 0

    best_loss = 1_000_000

    training_session = 1

    prepare_model_directories(model_identifier, models_directory_path)

    current_model_path = os.path.join(models_directory_path, model_identifier, f"{model_identifier}.tar")

    if os.path.exists(current_model_path):

        checkpoint = torch.load(current_model_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        current_epoch = checkpoint['epoch']
        best_loss = checkpoint['loss']
        training_session = checkpoint['training_session'] + 1

    for epoch in range(epoch_count):

        # print(f"EPOCH {current_epoch} Training", end='\r', flush=True)

        model.train(True)

        average_training_loss = train_single_epoch(model, training_dataloader, loss_function, optimizer, device, epoch)

        running_validation_loss = 0

        model.eval()

        # print(f"EPOCH {current_epoch} Validation", end='\r', flush=True)

        with torch.no_grad():

            tqdm_enumerator = tqdm(validation_dataloader)

            total_validation_data_length = len(validation_dataloader)

            for index, validation_data in enumerate(tqdm_enumerator):

                vinputs, vlabels = validation_data

                vinputs, vlabels = vinputs.to(device), vlabels.to(device)

                voutputs = model(vinputs).squeeze(1)

                vloss = loss_function(voutputs, vlabels)

                running_validation_loss += vloss

                tqdm_enumerator.set_description(f"EPOCH {epoch} Validation")
                tqdm_enumerator.set_postfix(loss=(running_validation_loss.item() / total_validation_data_length))

        average_validation_loss = running_validation_loss / len(validation_dataloader)

        # print('LOSS train {} valid {} \n'.format(average_training_loss, average_validation_loss), flush=True)

        if average_validation_loss < best_loss:
            best_loss = average_validation_loss

            # model_path = rf"models\{model_identifier}_Epoch-{current_epoch}_Loss-{round(best_loss.item(), 6)}.tar"

            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': best_loss,
                'training_session': training_session,
                }, current_model_path)

            create_training_report(model_identifier,
                                   current_epoch,
                                   best_loss,
                                   training_data_path,
                                   models_directory_path,
                                   training_session)

        current_epoch += 1


def predict_single_kern_value(model_identifier,
                              inference_data_path,
                              models_directory_path):

    device = torch.device(DEVICE)

    model = KernNet()

    current_model_path = os.path.join(models_directory_path, model_identifier, f"{model_identifier}.tar")

    checkpoint = torch.load(current_model_path)

    model.load_state_dict(checkpoint["model_state_dict"])

    model.to(device)

    image = PIL.Image.open(inference_data_path)

    r, g, b, a = image.split()

    transformer = transforms.Compose([
        transforms.ToTensor(),
    ])

    data_tensor = transformer(a)

    data_tensor = data_tensor.to(device)

    y_hat = model(data_tensor.unsqueeze(0)).squeeze().cpu().detach().numpy()

    kern_value = y_hat * 1000 - 500

    return kern_value


def predict_mass_kern_values(model_identifier,
                             models_directory_path,
                             inference_data_path,
                             generate_report=True,
                             batch_size=128):

    device = torch.device(DEVICE)

    image_path_list = discover_inference_images(inference_data_path)

    dataset = KernNetInferenceDataloader(inference_data_path, image_path_list, device)

    validation_dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=0)

    model = KernNet()

    current_model_path = os.path.join(models_directory_path, model_identifier, f"{model_identifier}.tar")

    if not os.path.exists(current_model_path):

        print("Requested model doesn't exist, exiting.\n")
        print(f"Path was: {current_model_path}")

        sys.exit()

    checkpoint = torch.load(current_model_path)

    model.load_state_dict(checkpoint["model_state_dict"])

    model.to(device)

    predictions = []

    model.eval()

    with torch.no_grad():

        tqdm_enumerator = tqdm(validation_dataloader)

        for index, inputs in enumerate(tqdm_enumerator):

            inputs = inputs.to(device)

            result = model(inputs).squeeze().cpu().detach().numpy()

            result = result * 1000 - 500

            predictions.append(result)

            tqdm_enumerator.set_description(f"Running Inference")

    torch.cuda.empty_cache()

    predictions = numpy.concatenate(predictions, axis=0)

    zipped_predictions = list(zip(image_path_list, predictions))

    if generate_report:
        create_inference_report(model_identifier, models_directory_path, current_data_selection, zipped_predictions)

    return zipped_predictions


def discover_training_images(data_directory_path):

    data_instances = []

    for root, dirs, files in os.walk(data_directory_path):

        for file_path in files:

            if not file_path.endswith(".png"):
                continue

            current_path = os.path.join(root, file_path)
            current_kern_value = int(round(float(file_path.replace(".png", "").split("_")[-1])))

            data_instances.append((current_path, current_kern_value))

    return data_instances


def discover_inference_images(data_directory_path):

    data_instances = []

    for root, dirs, files in os.walk(data_directory_path):

        for file_path in files:

            if not file_path.endswith(".png"):
                continue

            current_path = os.path.join(root, file_path)

            data_instances.append(current_path)

    return data_instances

if __name__ == '__main__':

    # This path assumes that the models directory remains in the same directory as the current script
    models_directory_path = os.path.join(os.getcwd(), "models")

    # Change this path before use (unless you are Lars van Blokland)
    #data_path = rf"E:\Petr Werk Files\Kerning V1\images_32_32"
    data_path = "/Volumes/Archiv-T1/TYPETR-KernNet-TrainingImages-Italic"
    
    # This identifier tells the script whether to continue training a model, or create a new one.
    # If the model isn't present in the models directory, the script will make a new subdirectory for the new model
    model_identifier = "Upgrade-V1-testing-TEST"

    current_data_selection = data_path

    # The train_model function trains a new model based on supplied parameters and datasets.
    #
    # The train_model function has three required and four optional parameters.
    # Optional parameters are optional because the function is able to supply standard values.
    #
    # Required parameters:
    #
    #   model_identifier: indicates which existing model to re-train, or what to call a new model
    #   models_directory_path: where to find and save models
    #   training_data_path: where to find the data the model will use for training
    #
    # Optional parameters:
    #
    #   epoch_count: how many epochs the model will train for
    #   validation_set_fraction: how much of the training data will be used for validation
    #   learning_rate: how much the weights will be affected by backpropegation
    #   batch_size: how many instances the model will train on per iteration. higher values can be faster, but will consume more memory.
    #
    # Train_model does not return anything.
    # Models are automatically saved, and reports are automatically generated.
    #
    train_model(model_identifier=model_identifier,
                models_directory_path=models_directory_path,
                training_data_path=current_data_selection,
                epoch_count=50,
                validation_set_fraction=0.3,
                learning_rate=0.001,
                batch_size=BATCH_SIZE)

    # The predict_mass_kern_values function takes an existing model, and uses it to evaluate supplied datasets.
    #
    # The predict_mass_kern_values has three required and two optional parameters.
    # Optional parameters are optional because the function is able to supply standard values.
    #
    # Required parameters:
    #
    #   model_identifier: indicates which existing model to re-train, or what to call a new model
    #   models_directory_path: where to find and save models
    #   inference_data_path: where to find the data the model will use for inference
    #
    # Optional parameters:
    #
    #   generate_report: whether the function has to generate a report on the performance of the model
    #   batch_size: how many instances the model will train on per iteration. higher values can be faster, but will consume more memory.
    #
    # The predict_mass_kern_values function returns a list of tuples.
    # Each tuple contains as the first element the path to the image, and as second element the predicted kerning value for that image:
    # Example: ('E:\\Petr Werk Files\\Kerning V1\\images_32_32\\images_32_32\\A.sc_asterisk_-32.png', -43.81067)
    #
    predictions = predict_mass_kern_values(model_identifier=model_identifier,
                                           models_directory_path=models_directory_path,
                                           inference_data_path=current_data_selection,
                                           generate_report=True,
                                           batch_size=BATCH_SIZE)


