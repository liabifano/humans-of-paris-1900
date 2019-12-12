import os

import pickle

import pandas as pd

from app.models import Gallica, Wiki, Tags, Person


NOTEBOOK_DATA_PATH = os.path.join(os.path.abspath(os.path.join(__file__, '../../../../')),
                                  'notebooks/data')

IMAGES_FOLDER = os.path.join(os.path.abspath(os.path.join(__file__, '../../static/')), 'img_full')


def get_avg_text(x, y):
    x = x if pd.notnull(x) else ''
    y = y if pd.notnull(y) else ''

    return len(x+y) / 2

def get_wiki_text(x, y):
    if pd.notnull(x):
        return x
    elif pd.notnull(y):
        return y

    return ''


def run():
    gallica_metadata = pd.read_pickle(os.path.join(NOTEBOOK_DATA_PATH, 'raw_df.pkl'))
    image_dataframe = pd.DataFrame(gallica_metadata['dc:identifier']
                                   .map(lambda x: x[0] if type(x) == list else x))\
        .rename(columns={'dc:identifier':'identifier'})
    gallica_metadata['gallica_url'] = image_dataframe
    gallica_metadata = gallica_metadata.rename(columns={'dc:date': 'date'})

    images_folder = [x.split('.')[0] for x in os.listdir(IMAGES_FOLDER)]

    pickle_in = open(os.path.join(NOTEBOOK_DATA_PATH, 'merged_dataframe.pkl'), 'rb')
    merged_dataframe = pickle.load(pickle_in)

    merged_dataframe = merged_dataframe.rename(columns={'weight': 'n_images_wiki',
                                                        'url_fr': 'wiki_fr_link',
                                                        'id': 'gallica_url'})
    merged_dataframe['gallica_identifier'] = merged_dataframe.gallica_url.apply(lambda x: x.split('/')[-1] if pd.notnull(x) else '')

    merged_dataframe['summary_size'] = merged_dataframe.apply(lambda x: get_avg_text(x['wiki_en_text'], x['wiki_fr_text']), axis=1)
    merged_dataframe['wiki_text'] = merged_dataframe.apply(lambda x: get_wiki_text(x['wiki_en_text'], x['wiki_fr_text']), axis=1)

    ids_gallica = merged_dataframe.explode('id_list')[['name', 'id_list']].rename(columns={'id_list': 'gallica_url'})
    ids_gallica['gallica_id'] = ids_gallica['gallica_url'].apply(lambda x: x.split('/')[-1] if pd.notnull(x) else '')
    ids_gallica = ids_gallica[ids_gallica['gallica_id']!='']
    ids_gallica = ids_gallica[ids_gallica.gallica_id.apply(lambda x: x in images_folder)]
    ids_gallica = gallica_metadata.merge(ids_gallica)[['gallica_url', 'gallica_id', 'date', 'name']]

    tags = merged_dataframe.explode('tags')[['name', 'tags']].rename(columns={'tags': 'tag'})

    persons = list(merged_dataframe[['name',
                                     'gallica_url',
                                     'bnf_link',
                                     'note',
                                     'gender',
                                     'gender_estimate',
                                     'age_estimate',
                                     'summary_size',
                                     'n_images_wiki',
                                     'gallica_identifier']].T.to_dict().values())

    for person in persons:
        name = person['name']
        p = Person(**person)
        p.save()

        wiki = list(merged_dataframe[merged_dataframe.name == name][['wiki_en_link', 'wiki_fr_link',
                                                                     'wiki_en_text', 'wiki_fr_text', 'wiki_text',
                                                                     'summary_size', 'n_images_wiki']].T.to_dict().values())[0]
        wiki['person'] = p
        w = Wiki(**wiki)
        w.save()

        this_gallicas = ids_gallica[ids_gallica.name == name]
        this_gallicas = list(this_gallicas[['gallica_url', 'gallica_id', 'date']]
                             .T.to_dict().values())

        this_tags = tags[tags.name == name]
        this_tags = [{'tag': t} for t in this_tags[['tag']].values.reshape(len(this_tags, ))]

        for gallica in this_gallicas:
            gallica['person'] = p
            g = Gallica(**gallica)
            g.save()

        for tag in this_tags:
            tag['person'] = p
            t = Tags(**tag)
            t.save()