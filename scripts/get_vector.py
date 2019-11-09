import argparse
import cv2
import itertools
import os
import pandas as pd

import numpy as np
np.set_printoptions(precision=2)

import openface


def get_image(doc):
    url = doc+'/f1.highres.jpg'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    img = Image.open(BytesIO(response.content)).convert('RGB')
    img = np.array(img)
    return img

def getRep(imgPath):

    bgrImg = get_image(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format(imgPath))

    alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))

    rep = net.forward(alignedFace)
    return rep


if __name__ == '__main__':
    sample = pd.read_csv('identifiers.csv', header=None)
    faces = []
    for doc in sample[1].sample(2):
        face = getRep(doc)
        faces.append(face)
        np.save('faces.npy', faces)
