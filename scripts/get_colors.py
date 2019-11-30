from io import BytesIO
import requests

from PIL import Image
import pandas as pd
import numpy as np
import json

sample = pd.read_csv('identifiers.csv', header=None)

def get_image(doc):
    url = doc+'/f1.highres.jpg'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    img = Image.open(BytesIO(response.content)).convert('RGB')
    img = np.array(img)
    return img


def image_median(img):
    return np.median(np.median(img, axis=1), axis=0)

colors = []

for doc in sample[1]:
    try:
        img = get_image(doc)
    except:
        print('[INFO] failed to fetch {}'.format(doc))
        continue

    h, w, d = img.shape

    #mid left of image
    avg_1 = img[int(w/2): int(w/2)+10, :10, :]
    avg_1 = image_median(avg_1)

    #mid right of image
    avg_2 = img[int(w/2): int(w/2)+10, -10:, :]
    avg_2 = image_median(avg_2)

    #mid top of image
    avg_3 = img[: 10, int(h/2):int(h/2)+10, :]
    avg_3 = image_median(avg_3)

    avg_color = np.median(np.median(img[0:10, 0:10, :], axis=1), axis=0)
    colors.append({'source': doc, 'avg1': list(avg_1), 'avg2': list(avg_2), 'avg3': list(avg_3)})

    with open('colors.json', 'w') as f:
        json.dump(colors, f)
