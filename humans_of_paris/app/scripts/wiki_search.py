import pandas as pd

import pickle


def subject_filter(x, subjects_to_exclude):
    if type(x) == str:
        if x in subjects_to_exclude:
            result = ''
        else:
            result = [x]
    elif type(x) == list:
        temp = []
        for s in x:
            if s not in subjects_to_exclude:
                # x.remove(s)
                temp.append(s)
        result = temp
    else:
        result = type(x)
    return result

def is_name(x):
    names = []
    for s in x:
        if '(' not in s and ',' not in s:
            pass
        else:
            names.append(s.split('--')[0].strip())
    return names


def get_wiki(gallica_output):
    pickle_in = open('notebooks/data/wiki_summaries.pkl', 'rb')
    wiki_summaries = pickle.load(pickle_in)

    pickle_in = open('notebooks/data/bnf_description.pkl', 'rb')
    bnf_description = pickle.load(pickle_in)


    image_dataframe = pd.DataFrame(gallica_output['dc:identifier'] \
                                   .map(lambda x: x[0] if type(x) == list else x)) \
        .rename(columns={'dc:identifier': 'identifier'})

    gallica_output['id'] = image_dataframe
    gallica_output['subject_is_list'] = gallica_output['dc:subject'].map(lambda x: type(x) == list)
    gallica_output['len_list'] = gallica_output[gallica_output.subject_is_list]['dc:subject'].map(len)
    df2 = gallica_output[['id', 'dc:subject', 'dc:title', 'subject_is_list', 'len_list']]
    subject1 = df2['dc:subject'][~df2.subject_is_list].unique().tolist()

    subjects_to_exclude = list(set(subject1) - set(['Luco, François (18..-1882) -- Portraits',
                                                'Figuet, Gabrielle (1862-1889) -- Portraits',
                                                'Cham (1818-1879) -- Oeuvres -- Dessin',
                                                'Delmas, Jean-François (1861-1933) -- Portraits',
                                                'Carvalho, Léon (1825-1897) -- Tombes',
                                                'Sand, George (1804-1876) -- Statues']))
    df2['subjects'] = df2['dc:subject'].apply(lambda x: subject_filter(x, subjects_to_exclude))
    wiki_df = pd.DataFrame(df2[['id','subjects']])
    wiki_df['names'] = wiki_df.subjects.apply(is_name)
    wiki_explode = wiki_df.explode('names').rename(columns={'names': 'name'})


    partial_result = wiki_summaries.merge(wiki_explode) # losing records here! 1201 to 1198. why?
    # print(result.name.nunique())
    # print(result.id.nunique())
    partial_result['id'] = partial_result['id'].apply(lambda x: x.split('/')[-1])
    partial_result = partial_result.rename(columns={'summary': 'summary_en'})

    partial_result = partial_result[['id', 'name', 'summary_en', 'summary_fr']]

    # how should I merge with bnf? query again?

    result = [{'id': x[0], 'name': x[1], 'summary_en': x[2], 'summary_fr': x[3]}
                      for x in [tuple(x) for x in partial_result.values]]

    return result

