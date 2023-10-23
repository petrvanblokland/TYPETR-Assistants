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

import numpy as np
import torch
import PIL
from torchvision import transforms
from kernNetClasses import KernNet

hostName = "localhost"
serverPort = 8080
#EM = 2048
EM = 1000

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

        imagePath = f'_imagePredict{self.path}'
        checkPointFilePath = 'lightning_logs/version_16/checkpoints/epoch=49-step=589100.ckpt'
        predicted = self.predict_kern_value(imagePath, checkPointFilePath)
        k = int(round(predicted*EM/1000/self.INCREMENT))*self.INCREMENT
        k = int(round(predicted/self.INCREMENT))*self.INCREMENT
        k = predicted
        print(k, predicted)
        self.wfile.write(bytes(str(k), "utf-8"))
        
    def predict_kern_value(self, image_file_path, checkpoint_file_path):

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

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

