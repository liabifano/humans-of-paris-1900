#!/usr/bin/env python3
import os
import cv2
import pandas as pd
import numpy as np
import requests
from PIL import Image
from io import BytesIO

frame = 0
record = False
OUTPUT = '/Users/lguillain/Documents/EPFL2019/FDH/humans-of-paris-1900/humans_of_paris/app/static/img_full/'

def write_frame(img, contours=None, rect=None):
    if not record: return
    global frame
    frame += 1
    if contours:
        img = img.copy()
        cv2.drawContours(img, contours, -1, (0,255,0), 3)
    if rect:
        img = img.copy()
        cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (255, 255, 0), 3)
    cv2.imwrite('frames/frame{:02d}.png'.format(frame), img)

def get_preproc(img):
    img2 = img.astype(np.float)
    cond1 = (img2[:, :, 0] - img2[:, :, 2]) > -15
    cond2 = (img2[:, :, 1] - img2[:, :, 2]) > -15
    if sum(sum(cond1)) > sum(sum(cond2)):
        cond2 = cond1
    return np.where(cond2[:, :, None].repeat(3, axis=2), np.full_like(img, 255), img).astype(np.uint8)

def get_contours(img):
    """Threshold the image and get contours."""
    # First make the image 1-bit and get contours
    imgray = cv2.cvtColor(get_preproc(img), cv2.COLOR_BGR2GRAY)
    #write_frame(imgray)
    # Find the right threshold level
    tl = 250
    ret, thresh = cv2.threshold(imgray, tl, 255, 0)
    # write_frame(thresh)
    while white_percent(thresh) > 0.85:
        tl += 10
        ret, thresh = cv2.threshold(imgray, tl, 255, 0)
        #write_frame(thresh)

    img2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    #write_frame(img, contours=contours)

    # filter contours that are too large or small
    # write_frame(img, contours=contours)
    contours = [cc for cc in contours if contourOK(img, cc)]
    #write_frame(img, contours=contours)
    return contours

def get_size(img):
    """Return the size of the image in pixels."""
    ih, iw = img.shape[:2]
    return iw * ih

def white_percent(img):
    """Return the percentage of the thresholded image that's white."""
    return cv2.countNonZero(img) / get_size(img)

def contourOK(img, cc):
    """Check if the contour is a good predictor of photo location."""
    if near_edge(img, cc): return False # shouldn't be near edges
    x, y, w, h = cv2.boundingRect(cc)

    if w < 100 or h < 100: return False # too narrow or wide is bad
    area = cv2.contourArea(cc)
    if area < (get_size(img) * 0.3): return False
    if area < 200: return False
    return True

def near_edge(img, contour):
    """Check if a contour is near the edge in the given image."""
    x, y, w, h = cv2.boundingRect(contour)
    ih, iw = img.shape[:2]
    mm = 20 # margin in pixels
    return (x < mm
            or x + w > iw - mm
            or y < mm
            or y + h > ih - mm)

def get_boundaries(img, contours):
    """Find the boundaries of the photo in the image using contours."""
    # margin is the minimum distance from the edges of the image, as a fraction
    ih, iw = img.shape[:2]
    minx = iw
    miny = ih
    maxx = 0
    maxy = 0
    for cc in contours:
        x, y, w, h = cv2.boundingRect(cc)
        if x < minx: minx = x
        if y < miny: miny = y
        if x + w > maxx: maxx = x + w
        if y + h > maxy: maxy = y + h

    return (minx, miny, maxx, maxy)

def crop(img, boundaries):
    """Crop the image to the given boundaries."""
    minx, miny, maxx, maxy = boundaries
    return img[miny:maxy, minx:maxx]

def get_image(doc, first_crop=False):
    if first_crop:
        url = doc+'/f1.highres.jpg'
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            return img
        except:
            return

    else:
        img = Image.open(OUTPUT + doc)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img


def autocrop_image(input_file, output_file=None, record_process=True, first_crop=False):
    """Autocrop the photograph from the given image."""

    # global to track if process frames should be written
    global record
    record = record_process
    print(input_file)

    if not output_file:
        parts = input_file.split('/')
        assert len(parts) > 1, "Can't automatically choose output name if there's no file extension!"
        output_file = ''.join(['/Users/lguillain/Documents/EPFL2019/FDH/humans-of-paris-1900/humans_of_paris/app/static/img_full/', parts[-1], '.png' ])

    img = get_image(input_file, first_crop)
    if img is None:
        print("couldn't get image")
        return

    contours = get_contours(img)
    bounds = get_boundaries(img, contours)
    cropped = crop(img, bounds)
    print(bounds)

    if get_size(cropped) < 2000:
        cv2.imwrite(output_file, img)
        print("resulting image too small, skipping output")
        #write_frame(img)
        return # too small

    #resize image
    h, w, d = cropped.shape
    ratio = 500./h
    cropped = cv2.resize(cropped, (int(w*ratio), 500))
    cv2.imwrite(output_file, cropped)

if __name__ == '__main__':
    first_crop = True
    if first_crop:
        sample = pd.read_csv('identifiers.csv', header=None)
        crawled = os.listdir(OUTPUT)
        crawled = [x[:-len('.png')] for x in crawled]
        sample = sample[~sample[1].map(lambda x: x.split('/')[-1]).isin(crawled)]
        to_crop = sample.dropna()[1].tolist()
        faces = []
    else:
        to_crop = ['btv1b53050483x.png']#[x for x in os.listdir(OUTPUT) if x[0] != '.']

    i = 0
    for doc in to_crop:
        autocrop_image(doc, first_crop=first_crop)
        i += 1
        print(i)
