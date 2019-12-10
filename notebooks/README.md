# Description on notebook files

## processing metadata

### get_data : fetch gallica metadata for Nadar dataset
Output : 
- data/named_subjects.pkl     : img id, title, subject, name-year (all images with named subjects)
- data/named_singles.pkl      : img id, title, subject, name-year (single-portrait images with named subjects)
- data/id_name.pkl            : name-year, list of image ids

### get_bnf : Query data.bnf.fr SPARQL and get data.bnf page link (and some other infos) for each person (takes hours to run)
read :
- id_name.pkl

Output:
- data/bnf_text_raw.pkl (savepoint)
- data/bnf_summaries.pkl : name-year, short note in bnf, data.bnf link

### get_bnf_table : By using data.bnf.fr link, get data.bnf table for each person
read:
- data/bnf_summaries.pkl

Output:
- data/bnf_table_summaries.pkl : name-year, data.bnf.fr table elements

### bnf_table_tag : Make a list of tags for each person.
read:
- data/bnf_table_summmaries.pkl

output:
- data/bnf_tags.pkl : name-year, list of tags

### get_wiki : fetch wikipedia articles (en/fr) for each person (takes hours to run)
read :
- data/id_name.pkl
output : 
- data/wiki_en.pkl (savepoint)
- data/wiki_fr.pkl (savepoint)
- data/wiki_en_summaries.pkl : name-year, content, # images, url
- data/wiki_fr_summaries.pkl : name-year, content, # images, url

### merge_dataframes : merge dataframes into one, sort by rank. 
read:
- data/wiki_en_summaries.pkl 
- data/wiki_fr_summaries.pkl 
- data/bnf_summaries.pkl
- data/named_subjects.pkl (may use id_name.pkl as well)
- age_gender_labeles.json

output:
- data/merged_dataframe.pkl : chosen id, name-year, list of ids, title, wiki summary contents, rank, age, gender
          
