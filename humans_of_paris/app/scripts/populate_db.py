import os

import pickle

import pandas as pd
import numpy as np

from app.models import Gallica, Wiki, Tags, Person
from humans_of_paris.settings import STATICFILES_DIRS



RAW_DATA_PATH = os.path.join(os.path.abspath(os.path.join(__file__, '../../../../')),
                             'data/raw_df.pkl')

NOTEBOOK_DATA_PATH = os.path.join(os.path.abspath(os.path.join(__file__, '../../../../')),
                                  'notebooks/data')



def run():
    images_path = os.path.join(STATICFILES_DIRS[0], 'img_full')
    ids_with_images = [x.split('.')[0] for x in os.listdir(images_path)]

    gallica_metadata = pd.read_pickle(RAW_DATA_PATH)
    image_dataframe = pd.DataFrame(gallica_metadata['dc:identifier']
                                   .map(lambda x: x[0] if type(x) == list else x))\
        .rename(columns={'dc:identifier':'identifier'})
    gallica_metadata['id'] = image_dataframe

    pickle_in = open(os.path.join(NOTEBOOK_DATA_PATH, 'bnf_table_full.pkl'), 'rb')
    bnf_table_full = pickle.load(pickle_in)

    pickle_in = open(os.path.join(NOTEBOOK_DATA_PATH, 'named_singles.pkl'), 'rb')
    named_singles = pickle.load(pickle_in)

    pickle_in = open(os.path.join(NOTEBOOK_DATA_PATH, 'tag-id.pkl'), 'rb')
    tag_id = pickle.load(pickle_in)
    tags = tag_id.explode('tags')
    tags = tags[pd.notnull(tags.tags)].rename(columns={'tags': 'tag'})
    tags['id'] = tags['id'].apply(lambda x: x.split('/')[-1])

    pickle_in = open(os.path.join(NOTEBOOK_DATA_PATH, 'wiki_en_summaries.pkl'), 'rb')
    wiki_en = pickle.load(pickle_in)

    pickle_in = open(os.path.join(NOTEBOOK_DATA_PATH, 'wiki_fr_summaries.pkl'), 'rb')
    wiki_fr = pickle.load(pickle_in)


    persons = list(bnf_table_full[['name', 'bnf_link', 'gender',
                                   'note', 'country', 'lang', 'born', 'died']].T.to_dict().values())

    names_gallica = gallica_metadata.merge(named_singles)

    wiki_en = wiki_en.rename(columns={'rank_en': 'rank'})
    wiki_en['english'] = True
    wiki_en['french'] = False

    wiki_fr = wiki_fr.rename(columns={'summary_fr': 'summary', 'weight_fr': 'weight',
                                      'rank_en': 'rank', 'url_fr': 'url'})
    wiki_fr['english'] = False
    wiki_fr['french'] = True

    wiki = wiki_en.append(wiki_fr).drop_duplicates('url')
    wiki = wiki.rename(columns={'url': 'wiki_url', 'weight': 'n_images'})

    for person in persons:
        name = person['name']
        p = Person(**person)
        p.save()
        this_gallica = names_gallica[names_gallica.name == name]
        this_gallica = this_gallica.rename(columns={'id': 'gallica_url', 'dc:date': 'date'})[['gallica_url', 'date']]
        this_gallica['id'] = this_gallica['gallica_url'].apply(lambda x: x.split('/')[-1])
        this_gallica = list(this_gallica.T.to_dict().values())
        this_wiki = list(wiki[wiki.name == name][['wiki_url', 'english', 'french', 'n_images', 'summary', 'rank']].T.to_dict().values())

        p = Person(**person)
        p.save()

        for gg in this_gallica:
            if gg['id'] in ids_with_images:
                this_tag = list(tags[tags.id == gg['id']].T.to_dict().values())
                gg['person'] = p
                gg['n_images_wiki'] = this_wiki[0]['n_images'] if this_wiki else np.nan
                gg['summary_size'] = len(this_wiki[0]['summary']) if this_wiki else np.nan
                gg['gender'] = person['gender']
                g = Gallica(**gg)
                g.save()

                for tt in this_tag:
                    tt['gallica'] = g
                    del tt['id']
                    Tags(**tt).save()

        for ww in this_wiki:
            ww['person'] = p
            Wiki(**ww).save()









