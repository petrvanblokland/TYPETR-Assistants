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
# http://localhost:8080/gName1/gName2/test.png
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
DEVICE_NAME = 'cpu'
#DEVICE_NAME = 'mps'
MODEL_NAME = 'Upgrade-V7'

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
        kernImagePath = f'/tmp/com.typetr_imagePredict/{imageFileName}'

        #print(gName1, gName2, imageFileName)
        # Roman + Italic + black side rectangles
        #checkPointFilePath = 'lightning_logs/version_16/checkpoints/epoch=49-step=589100.ckpt'
        # Roman + Italic + black side rectangles
        #checkPointFilePath = 'lightning_logs/version_17/checkpoints/epoch=49-step=589100.ckpt'
        # Roman + Italic + black side rectangles
        #checkPointFilePath = 'lightning_logs/version_18/checkpoints/epoch=49-step=286250.ckpt'
        # Upgrade Roman + Italic 9m test files
        #checkPointFilePath = 'lightning_logs/version_21/checkpoints/epoch=0-step=102979.ckpt'
        #checkPointFilePath = 'models/Upgrade-V1-testing/Upgrade-V1-testing.tar'
        checkPointFilePath = 'models'
        predicted = self.predict_single_kern_value(MODEL_NAME, kernImagePath, checkPointFilePath)
        #k = int(round(predicted*EM/1000/self.INCREMENT))*self.INCREMENT
        #k = int(round(predicted/self.INCREMENT))*self.INCREMENT
        k = predicted # Answer the whole predicted value as float, by default scaled for unitsPerEm=1000
        # Answer the glyph names with the predicted kerning value, for the caller to check.
        # Since this is a ansynchronic system, calls and answer my be mixed up.
        print(f'... Model {MODEL_NAME} /{gName1} /{gName2} {k} {kernImagePath}')
        self.wfile.write(bytes(f'{gName1}/{gName2}/{str(k)}', "utf-8"))

    def predict_single_kern_value(self, model_identifier,
                                  inference_data_path,
                                  models_directory_path):

        #device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        #device = torch.device('mps')
        device = torch.device(DEVICE_NAME)
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
        #print('=====', np.asarray(a))
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
        device = torch.device(DEVICE_NAME)
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


