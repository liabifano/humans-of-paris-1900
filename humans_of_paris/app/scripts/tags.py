import pandas as pd
import re
from itertools import chain

# some manual work

taglist_title_final = ['député', 'ambassade', 'ministre', 'bordas',
                       'compositeur', 'général', 'chinois', 'journaliste',
                       'opéra', 'sculpteur', 'vaudeviliste', 'peintre',
                       'colonel', 'auteur', 'historien', 'comédien', 'amiral',
                       'baretta', 'prince', 'chimiste', 'avocat',
                       'piccolo', 'comédie', 'romancier', 'abbé',
                       'écrivain', 'capitaine', 'navigation', 'vaudeville',
                       'châtelet', 'explorateur', 'aéronaute',
                       'critique', 'cantatrice', 'princesse', 'poète', 'violoniste',
                       'docteur', 'journal', 'marquis',
                       'dessinateur', 'musicien', 'chanteur',
                       'publiciste', 'chef', 'couturier', 'lanthelme', 'famille',
                       'opéra-comique', 'écuyère', 'actrice',
                       'napoléon', 'directeur', 'ecrivain', 'suite', 'anglaise',
                       'palais-royal', 'folies', 'cirque', 'ecuyère',
                       'théâtre-français', 'gymnase', 'frère',
                       'roi', 'folies-dramatiques',
                       'mousquetaires', 'bouffes-parisiens', 'professeur', 'groupe',
                       'littérateur', 'président', 'maison',

                       'lyrique', 'cluny', 'reichemberg', 'folies-dramatiques', 'frères',

                       'chevallier', 'danseuse',
                       'décorateur', 'ambassadeur',
                       'politique', 'saint', 'république',
                       'droit',
                       'marquise',
                       'sénateur',
                       'artiste', 'cloches',
                       'majesté', 'japonaise', 'dramatique',
                       'comique', 'française', 'aérienne', 'conservatoire', 'bourgeois',
                       'italien', 'royal', "l'institut",
                       "d'orchestre", 'comédie-française',
                       'revue', 'bergère', "d'hiver", 'potter', 'dramatiques',
                       'suédoise', "l'académie", 'opéra-comique',
                       'orphée',

                       'folies-dramatiques',
                       'vaudevill', 'odéon', 'phèdre', 'assassin', 'décoré',
                       'saint-martin', 'trouvère', 'vénus', "l'arlésienne",
                       'assommoir',
                       'cantinière', "s'amuse", 'amour', 'opéra', 'serment', 'rouge',

                       'mascotte', 'gymnase',
                       'châtelet',

                       'africaine',
                       'juanita', 'perse', 'musique',
                       'nouveau', 'lettres', 'russe', 'breuil', 'lantelme', 'hanovre',
                       'pyrénées', 'parisienne', 'ventre',

                       'chevalier', 'séville', 'américaine', "l'impératrice",
                       'commune', 'cigale', 'saturnales', 'cendrillonnette', 'tzigane',

                       'camarade', 'marchande', 'bicyclistes',
                       'sans-gêne', 'cousin-cousine', "d'avignon", 'pilules', 'fétiche',
                       'cliquette',
                       'patard', 'patart', 'joyeusetés', 'fantaisies-parisiennes',
                       'dramatiques', 'carreau', 'suzette', 'enfers', 'école',

                       'trèfle',

                       'tambour-major', 'couronne',
                       'diable',
                       'pyrennées', 'christ', 'hussard', 'galles', "l'année", 'chèvres',
                       'seigneur', 'clairette']


def filter_tags(x):
    tag_4 = ['cure', 'chef', 'lord', 'abbé']

    if type(x) != str:
        return False

    if x.find(',') != -1:
        return False

    if len(x) < 3:
        return False

    elif len(x) == 3:
        if x == 'roi':
            return True
        else:
            return False
    elif len(x) == 4:
        if x in tag_4:
            return True
        else:
            return False
    else:
        return True


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


def exclude_title_name(x, names):
    temp = []
    for t in x:
        t = re.sub('[\[\] (".,")]', '', t)

        if t.lower() in names:
            pass
        else:
            temp.append(t.lower())
    return temp


def get_taglist(df, n=10):
    return df[df['tags'].map(df['tags'].value_counts()) > n]


def title_filter(x):
    if type(x) == list:
        x = ''.join(x)

    if type(x) == str:
        try:
            result = x.split(':')[0].strip().strip('[]')
        except:
            result = x
    else:
        result = x

    return result


def name_filter(x):
    return [s.split('--')[0].strip() for s in x]


def is_name(x):
    names = []
    for s in x:
        if '(' not in s and ',' not in s:
            pass
        else:
            names.append(s.split('--')[0].strip())
    return names


def not_name(x):
    words = []
    for s in x:
        if '(' not in s and ',' not in s:
            words.append(s)
        else:
            pass
    return words


def get_tags(gallica_output):
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

    df2 = df2.drop(['dc:subject', 'subject_is_list', 'len_list'], axis=1)

    df2['number_of_subjects'] = df2['subjects'].apply(len)

    df2 = df2[df2.number_of_subjects != 0]

    df2['title'] = df2['dc:title'].apply(title_filter)

    _prenames = df2.subjects.apply(name_filter)

    is_names = _prenames.apply(is_name).tolist()

    is_names = list(set(chain.from_iterable(is_names)))

    names = []
    for n in is_names:
        name_ = n.split('(')[0].strip().lower().split(',')
        names.append(name_)

    names = list(set(chain.from_iterable(names)))
    names = list(set(list(map(lambda x: x.strip(), names))))

    df2['title_broken'] = df2.title.apply(lambda x: re.findall('[\S]+', x))

    tag_df = pd.DataFrame(df2.id)
    tag_df['title'] = df2['title_broken'].apply(lambda x: exclude_title_name(x, names))
    tag_df['subject'] = df2.subjects.apply(name_filter).apply(not_name)

    tags_subject_ = tag_df.subject.apply(pd.Series).merge(tag_df, right_index=True, left_index=True) \
        .drop(['title', 'subject'], axis=1).melt(id_vars=['id'], value_name='tags').drop('variable', axis=1)

    tags_subject_ = tags_subject_[tags_subject_.tags.apply(filter_tags)]

    taglist_subject = list(get_taglist(tags_subject_, n=1).tags.unique())

    tag_df['tags_title'] = tag_df.title.apply(lambda x: list(set(x).intersection(set(taglist_title_final))))
    tag_df['tags_subject'] = tag_df.subject.apply(lambda x: list(set(x).intersection(set(taglist_subject))))

    tag_df['tags'] = tag_df.tags_title + tag_df.tags_subject

    tag_df['len'] = tag_df.tags.apply(lambda x: len(x))

    tag_df = tag_df[tag_df.len > 0]

    tag_id_df = pd.DataFrame(tag_df[['id', 'tags']], columns=['id', 'tags'])

    tag_id_df['id'] = tag_id_df.id.apply(lambda x: x.split('/')[-1])

    tag_id_df = [tuple(x) for x in tag_id_df.values]

    result = []
    for id, tags in tag_id_df:
        for tag in tags:
            result.append({'id': id, 'tag': tag})

    return result
