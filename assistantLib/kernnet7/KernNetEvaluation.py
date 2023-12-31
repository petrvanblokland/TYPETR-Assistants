import random
import sys

import PIL
import numpy
import torch.nn.functional as F
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os
import rasterio
import numpy as np
import datetime
from PIL import Image
import os.path
from torchvision import transforms
from tqdm.auto import tqdm
import pandas as pd

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


def prepare_model_directories(current_model_identifier, models_directory_path):

    current_model_path = os.path.join(models_directory_path, current_model_identifier)

    if os.path.isdir(current_model_path):

        print("Model directory present.")

        return

    else:

        os.mkdir(current_model_path)

        training_report_directory = os.path.join(current_model_path, "training_reports")
        os.mkdir(training_report_directory)

        inference_report_directory = os.path.join(current_model_path, "inference_reports")
        os.mkdir(inference_report_directory)

        print("Created model directory")

        return


def create_training_report(model_identifier, epoch, loss, training_data_path, models_directory_path, training_session):

    if not os.path.isdir(os.path.join(models_directory_path, model_identifier)):

        print("Requested model folder does not exist, exiting.")
        sys.exit()

    report_name = f"{model_identifier}_training_report_{training_session}.txt"

    training_report_path = os.path.join(models_directory_path, model_identifier, "training_reports", report_name)

    if os.path.exists(training_report_path):

        os.remove(training_report_path)

    report_file = open(training_report_path, "a")

    report_file.write(f"{model_identifier} training report {training_session}\n\n")

    report_file.write(f"Trained Epochs: {epoch}\n\n")

    report_file.write(f"Best validation loss: {loss}\n\n")

    report_file.write(f"Training Data root: {training_data_path}\n\n")

    report_file.write("Training Data:\n\n")

    for root, dirs, files in os.walk(training_data_path):

        level = root.replace(training_data_path, '').count(os.sep)

        indent = ' ' * 4 * (level)

        report_file.write('{}{} \n'.format(indent, os.path.basename(root)))


def create_inference_report(model_identifier, models_directory_path, inference_data_path, zipped_predictions):

    split_path_zipped_predictions = [(os.path.normpath(item[0]).split(os.path.sep), item[1]) for item in zipped_predictions]

    split_path_zipped_predictions = [item[0].append(item[1]) or item for item in split_path_zipped_predictions]

    split_path_zipped_predictions = [item[0] for item in split_path_zipped_predictions]

    df = pd.DataFrame(split_path_zipped_predictions)

    df = df.drop(df.nunique()[df.nunique() == 1].index, axis=1)

    df.iloc[:, -2] = df.iloc[:, -2].map(lambda file_name: int(round(float(file_name.replace(".png", "").split("_")[-1]))))

    df.iloc[:, -1] = df.iloc[:, -1].map(lambda kern_value: int(kern_value))

    df["error"] = abs(abs(df.iloc[:, -1]) - abs(df.iloc[:, -2]))

    average_error = round(df["error"].mean())

    # WORK IN PROGRESS
    # This will eventually enable average kerning error per category
    # grouped_average_errors = []
    #
    # for column in df.columns[0:-3]:
    #
    #     grouped_df = df.groupby(column).mean()
    #
    #     grouped_df = grouped_df.reset_index()
    #
    #     grouped_df.iloc[:, -1] = grouped_df.iloc[:, -1].map(lambda averaged_kern_value: int(averaged_kern_value))
    #
    #     grouped_df = grouped_df.drop(grouped_df.columns[[1, 2]], axis=1)
    #
    #     grouped_average_errors.append(list(grouped_df.itertuples(index=False, name=None)))

    if not os.path.isdir(os.path.join(models_directory_path, model_identifier)):

        print("Requested model folder does not exist, exiting.")
        sys.exit()

    inference_reports_directory = os.path.join(models_directory_path, model_identifier, "inference_reports")

    inference_report_count = 0

    for report_file in os.scandir(inference_reports_directory):
        inference_report_count += 1


    report_name = f"{model_identifier}_inference_report_{inference_report_count + 1}.txt"

    inference_report_path = os.path.join(models_directory_path, model_identifier, "inference_reports", report_name)

    report_file = open(inference_report_path, "a")

    report_file.write(f"{model_identifier} Inference report {inference_report_count + 1}\n\n")

    report_file.write(f"Average Kerning Error: {average_error}\n\n")

    report_file.write(f"Inference Data Root: {inference_data_path}\n\n")

    report_file.write("Inference Data:\n\n")

    for root, dirs, files in os.walk(inference_data_path):

        level = root.replace(inference_data_path, '').count(os.sep)

        indent = ' ' * 4 * (level)

        report_file.write('{}{} \n'.format(indent, os.path.basename(root)))


