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
    first_k_distances = distances[idx[:k]]
    first_k_idx = idx[:k]
    order = np.argsort(first_k_distances)
    first_k_idx = first_k_idx[order]
    first_k_distances = first_k_distances[order]
    ids = [x.split('/')[-1] for x in face.iloc[first_k_idx].id.tolist()]

    return zip(ids, first_k_distances)
