import flask
import werkzeug
import time
import predict
import ttt
import threading
import argparse
import os
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
        #ttt.runprog(newname)
        #t1 = threading.Thread(target=predict.appdd, args=(args,newname,))
        #t1.start()
        #t1.join()
        #print("done")
        #reply=predict.appdd(newfilename)
        predict.appdd(args,newname)
    print("\n")
    return "thank you"

app.run(host="0.0.0.0", port=6000, debug=True)
