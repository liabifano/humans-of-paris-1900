import numpy as np
from scipy.spatial import distance
import pandas as pd
import json

def get_doppelganger(target, k=6):
    """get k most similar persons in facial vectors

        target: vector from openface
        returns reference id
        
    """
    # load face_vectors
    with open('notebooks/faces.json') as f:
        d = f.read()
    face = pd.DataFrame(json.loads(d))

    matrix = face.face.tolist()
    distances = distance.cdist([target], matrix, "cosine")[0]

    idx = np.argpartition(distances, k)
    closest_indices = idx[:k]
    return [x.split('/')[-1] for x in face.iloc[closest_indices].id.tolist()]
