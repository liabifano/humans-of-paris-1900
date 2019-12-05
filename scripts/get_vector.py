import argparse
import cv2
from io import BytesIO
from PIL import Image
import itertools
import os

import numpy as np
np.set_printoptions(precision=2)
import pandas as pd
import requests
import openface
import json



def get_image(doc):
    url = doc+'/f1.highres.jpg'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    img = Image.open(BytesIO(response.content)).convert('RGB')
    img = np.array(img)
    return img

def getRep(imgPath, imgDim=96):

    bgrImg = get_image(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format(imgPath))

    alignedFace = align.align(imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))

    rep = net.forward(alignedFace)
    return rep


if __name__ == '__main__':

    modelDir = 'models'
    print(modelDir)
    dlibModelDir = 'models/dlib'
    print(dlibModelDir)
    openfaceModelDir = 'models/openface'


    dlibFacePredictor = os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat")
    align = openface.AlignDlib(dlibFacePredictor)

    networkModel = os.path.join(openfaceModelDir, 'nn4.small2.v1.t7')
    imgDim = 96
    net = openface.TorchNeuralNet(networkModel, imgDim)

    sample =  pd.read_json('age_gender_labeles.json').T
    faces = []
    for doc in sample.id:

        try:
            print('INFO : parsing ', doc)
            face = getRep(doc, imgDim)
            faces.append({'id': doc, 'face': list(face)})
        except:
            print('Failed on ', doc)
            continue

        with open('faces.json', 'w') as f:
            json.dump(faces, f)
