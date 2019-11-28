import os
import re
import pickle
from io import BytesIO
import requests
from multiprocessing import Pool
import numpy as np

import pandas as pd
import wikipedia as wiki
from PIL import Image

from app.models import AllData, Tags
from app.scripts import tags

from humans_of_paris.settings import MEDIA_ROOT


RAW_DATA_PATH = os.path.join(os.path.abspath(os.path.join(__file__, '../../../../')),
                             'data/raw_df.pkl')


def filter_df(df):
    # TODO: filter certains categories
    return df

def get_url(x):
    return x[0] if len(x)==2 else x

def get_id(x):
    return x[0][-9:] if len(x)==2 else x[-9:]

def get_name(x):
    # TODO: improve it and get a list of name instead
    if isinstance(x, str):
        return None

    return ' '.join(re.findall('([\S]* [\S]*|[\S]*|[\S]*\, [\S]*[ \S*]+) \([\d]{2}', x[0]))


def get_wiki_name(x):
    # TODO: improve it by requesting to BNT database
    return x


def get_wiki_info(x):
    empty_return = {
        'wiki_url': None,
        'wiki_n_langs': 0, # TODO: Wikipedia-API has this feature
        'wiki_n_categories': None,
        'wiki_n_links': None,
        'wiki_n_images': None,
        'wiki_n_references': None,
        'wiki_n_content': None
    }
    if x is None:
        return empty_return

    try:
        s = wiki.page(x)
        return {
            'wiki_url': s.url,
            'wiki_n_langs': 0,
            'wiki_n_categories': len(s.categories),
            'wiki_n_links': len(s.links),
            'wiki_n_images': len(s.images),
            'wiki_n_references': len(s.references),
            'wiki_n_content': len(s.content)
        }

    except:
        return empty_return

def get_image_url(url):
    return url + '/f1.lowres'


def get_gallica_image(url):
    # TODO: get better image and crop it
    try:
        response = requests.get(url, stream=True)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((150, 150), Image.LANCZOS)
        img.save(MEDIA_ROOT + '/gallica/{}.JPEG'.format(url.split('/')[-2]), quality=60)
        return img
    except:
        pass


def get_tags(x):
    # TODO: FAKE function for now
    return {
        'tag_sex': np.random.choice(['F','M'], 1)[0],
        'tag_profession': np.random.choice(['artist', 'actor', 'photographer'], 1)[0]
    }


def get_data(gallica_output):
    result = pd.DataFrame()

    filtered = filter_df(gallica_output)

    result['id'] = filtered['dc:identifier'].apply(get_id)
    result['gallica_url'] = filtered['dc:identifier'].apply(get_url)
    result['date'] = filtered['dc:date']
    result['name'] = filtered['dc:subject'].apply(get_name)
    # result['wiki_name'] = result['name'].apply(get_wiki_name)
    # result['gallica_image_url'] = result.gallica_url.apply(get_image_url)
    # result[['tag_sex', 'tag_profession']] = pd.DataFrame([get_tags(x) for x in result.id.values])
    #
    # p = Pool(8)
    # wiki_info = pd.DataFrame(p.map(get_wiki_info, result['wiki_name'].values))
    # p.close()
    # p.join()
    #
    # result[['wiki_url',
    #         'wiki_n_langs',
    #         'wiki_n_categories',
    #         'wiki_n_links',
    #         'wiki_n_images',
    #         'wiki_n_references',
    #         'wiki_n_content']] = wiki_info
    #
    # result = result.where((pd.notnull(result)), None)
    #
    # p = Pool(8)
    # p.map(get_gallica_image, result['gallica_image_url'].values)
    # p.close()
    # p.join()

    return list(result.T.to_dict().values())


def populate(data):
    for d in data:
        r = AllData(**d)
        r.save()


def run():
    print('Preprocessing data...')
    pickle_in = open(RAW_DATA_PATH, 'rb')
    gallica_output = pickle.load(pickle_in)
    all_tags = tags.get_tags(gallica_output)
    [Tags(**t).save() for t in all_tags]

    result = get_data(gallica_output)

    print('Inserting records in database...')
    populate(result)

    print('Done!')
