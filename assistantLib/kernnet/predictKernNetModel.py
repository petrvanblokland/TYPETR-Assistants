import torch
import numpy as np
from PIL import Image
import PIL
from torchvision import transforms
try:
    from assistantLib.nernnet.kernNetClasses import KernNet
except ImportError:
    from kernnet.kernNetClasses import KernNet

# This file includes a function that predicts a kerning value for 32x32 pixel image.
# The function is called with two parameters:
#   1. The path to the image.
#   2. The path to the model checkpoint file.
#
# The function returns a single float, representing the predicted kerning value for the input image.
# Kerning is done on a -1000 to 1000 scale.


def predict_kern_value(image_file_path, checkpoint_file_path):

    checkpoint = torch.load(str(checkpoint_file_path), map_location=torch.device('mps'))

    model = KernNet()

    model.load_state_dict(checkpoint["state_dict"])

    image = PIL.Image.open(image_file_path)

    r, g, b, a = image.split()

    image = np.asarray(a)

    convert_to_tensor = transforms.ToTensor()

    x = convert_to_tensor(image.copy())

    y_hat = model(x.unsqueeze(0)).cpu().squeeze().detach().numpy()

    kern_value = y_hat * 1000 - 500

    return kern_value
