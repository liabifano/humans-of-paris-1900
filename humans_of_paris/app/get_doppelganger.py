import numpy as np
from scipy.spatial import distance
import pandas as pd
import json

def get_doppelganger(target, all_ids, k=6):
    """get k most similar persons in facial vectors

        target: vector from openface
        returns reference id
        
    """
    # load face_vectors
    with open('notebooks/data/faces.json') as f:
        d = f.read()
    face = pd.DataFrame(json.loads(d))

    face['gallica_id'] = face['id'].apply(lambda x: x.split('/')[-1])
    face = face[face.gallica_id.apply(lambda x: x in all_ids)]

    matrix = face.face.tolist()
    distances = distance.cdist([target], matrix, "cosine")[0]

    idx = np.argpartition(distances, k)
    first_k_distances = distances[idx[:k]]
    first_k_idx = idx[:k]
    order = np.argsort(first_k_distances)
    first_k_idx = first_k_idx[order]
    first_k_distances = first_k_distances[order]
    ids = [x for x in face.iloc[first_k_idx].gallica_id.tolist()]

    return zip(ids, first_k_distances)
