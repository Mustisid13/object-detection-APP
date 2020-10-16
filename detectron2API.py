from flask import Flask,jsonify, request, Response
# from flask_restful import Resource,Api

import detectron2
# from detectron2.utils.logger import setup_logger
# setup_logger()

# import some common libraries
# import matplotlib.pyplot as plt
import pandas as pd
import cv2
import numpy as np

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
# from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

cfg = get_cfg()
cfg.MODEL.DEVICE='cpu'
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

#classes names
classes = MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes

app = Flask(__name__)



def get_predictions(im):
    predictor = DefaultPredictor(cfg)
    outputs = predictor(im)
    return outputs
    
@app.route('/api/test', methods=['POST'])
def api_request():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    out = get_predictions(img)
    pred = out["instances"].pred_classes.tolist()
    preds = list()
    for i in pred:
        preds.append(classes[i])
    
    res = pd.DataFrame()
    res["predictions"] = preds
    response = res.to_json()
    return Response(response=response, status=200, mimetype="application/json")



if __name__ == "__main__":
    app.run(debug = True)
        

        


