# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   kernNetClasses.py
#
# Python 3 server example
#
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

import numpy as np
import torch
import PIL
from torchvision import transforms
from KernNetClasses import KernNet

# http://localhost:8080/
hostName = "localhost"
serverPort = 8080
#EM = 2048
EM = 1000

DEVICE = 'cpu'
#DEVICE = 'mps'

class MyServer(BaseHTTPRequestHandler):

    INCREMENT = 4

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        #self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        #self.wfile.write(bytes("<body>", "utf-8"))
        #self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        #self.wfile.write(bytes("</body></html>", "utf-8"))

        # The path is supposed to have this format: glyphName1/glyphName2/imageFileName
        parts = self.path.split('/')
        if len(parts) < 3:
            print('###', parts)
            return
            
        gName1, gName2, imageFileName = parts[-3:]
        imagePath = f'_imagePredict/{imageFileName}'

        #checkPointFilePath = 'models/Upgrade-V1-testing/Upgrade-V1-testing.tar'
        checkPointFilePath = 'models'
        #predicted = self.predict_kern_value(imagePath, checkPointFilePath)
        predicted = self.predict_single_kern_value('Upgrade-V7', imagePath, checkPointFilePath)
        # Answer the whole predicted value as float, by default scaled for unitsPerEm=1000
        #k = int(round(predicted*EM/1000/self.INCREMENT))*self.INCREMENT
        #k = int(round(predicted/self.INCREMENT))*self.INCREMENT
        k = predicted # 

        # Answer the glyph names with the predicted kerning value, for the caller to check.
        # Since this is a ansynchronic system, calls and answer my be mixed up.
        print('===', gName1, gName2, k, imagePath) 
        self.wfile.write(bytes(f'{gName1}/{gName2}/{str(k)}', "utf-8"))
    
    def predict_kern_value(self, image_file_path, checkpoint_file_path):

        #checkpoint = torch.load(str(checkpoint_file_path), map_location=torch.device('mps'))
        checkpoint = torch.load(str(checkpoint_file_path), map_location=torch.device(DEVICE))

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

    def predict_single_kern_value(self, model_identifier,
                                  inference_data_path,
                                  models_directory_path):

        #device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        #device = torch.device('mps')
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

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if 0:

    def predict_single_kern_value(model_identifier,
                                  inference_data_path,
                                  models_directory_path):

        #device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        device = torch.device(DEVICE)

        model = KernNet()

        current_model_path = os.path.join(models_directory_path, model_identifier, f"{model_identifier}.tar")

        checkpoint = torch.load(current_model_path, map_location=device)

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

if 0:
    imageFileName = 'test.png'
    imagePath = f'_imagePredict/{imageFileName}'
    checkPointFilePath = 'models'
    modelName = 'Upgrade-V1-testing'
    #modelName = 'Presti-V2'
    #modelName = 'Upgrade-V2'
    k = predict_single_kern_value(modelName, imagePath, checkPointFilePath)
    print('-----', k)


