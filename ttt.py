import flask
import werkzeug
import time
import argparse
import os
import threading
import cv2
import numpy as np
from tqdm import tqdm
from preprocessing import parse_annotation
from utils import draw_boxes
from frontend import YOLO
import json

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

argparser = argparse.ArgumentParser(
    description='Train and validate YOLO_v2 model on any dataset')

#argparser.add_argument(
 #   '-c',
 #   '--conf',
 #   help='path to configuration file')

#argparser.add_argument(
#    '-w',
#    '--weights',
#    help='path to pretrained weights')

#argparser.add_argument(
#    '-i',
#    '--input',
#   help='path to an image or an video (mp4 format)')

config_path  = "config.json"
weights_path = "trained_wts.h5"
image_path   = "m.jpg"

with open(config_path) as config_buffer:    
    config = json.load(config_buffer)

    ###############################
    #   Make the model 
    ###############################

yolo = YOLO(backend             = config['model']['backend'],
            input_size          = config['model']['input_size'], 
            labels              = config['model']['labels'], 
            max_box_per_image   = config['model']['max_box_per_image'],
            anchors             = config['model']['anchors'])

    ###############################
    #   Load trained weights
    ###############################    
yolo.load_weights(weights_path)

    ###############################
    #   Predict bounding boxes 
    ###############################

app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    files_ids = list(flask.request.files)
    print("\nNumber of Received Images : ", len(files_ids))
    image_num = 1
    for file_id in files_ids:
        print("\nSaving Image ", str(image_num), "/", len(files_ids))
        imagefile = flask.request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)  
        timestr = time.strftime("%Y%m%d-%H%M%S")
        newfilename=timestr+'_'+filename
        imagefile.save(newfilename)
        image_num = image_num + 1
        print("Image Filename : "+newfilename)
        args = argparser.parse_args()
        newname=str(timestr+'_'+filename)
        image = cv2.imread(image_path)
        boxes = yolo.predict(image)
        image = draw_boxes(image, boxes, config['model']['labels'])
        print(len(boxes), 'boxes are found')
        cv2.imwrite(image_path[:-4] + '_detected' + image_path[-4:], image)
    print("\n")
    return "thank you"

app.run(host="0.0.0.0", port=6000, debug=True)
 