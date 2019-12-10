# Description on notebook files

## processing metadata

### get_data : fetch gallica metadata for Nadar dataset
Output : 
- data/named_singles.pkl
- data/id_name.pkl
- data/named_subjects.pkl

### get_bnf : Query data.bnf.fr SPARQL and get data.bnf page link (and some other infos) for each person
read :
- id_name.pkl

Output:
- data/bnf_text_raw.pkl (savepoint)
- data/bnf_summaries.pkl

### get_bnf_table : By using data.bnf.fr link, get data.bnf table for each person
read:
- data/bnf_summaries.pkl

Output:
- data/bnf_table_full.pkl (savepoint)
- data/bnf_table_summaries.pkl 

### bnf_table_tag : Make a list of tags for each person.
read:
- data/bnf_table_summmaries.pkl

output:
- data/bnf_tags.pkl

### get_wiki : fetch wikipedia articles (en/fr) for each person
read :
- data/id_name.pkl
output : 
- data/wiki_en.pkl (savepoint)
- data/wiki_fr.pkl (savepoint)
- data/wiki_en_summaries.pkl 
- data/wiki_fr_summaries.pkl 

### merge_dataframes : merge dataframes into one, sort by rank. 
read:
- data/wiki_en_summaries.pkl 
- data/wiki_fr_summaries.pkl 
- data/bnf_summaries.pkl
- data/named_subjects.pkl (may use id_name.pkl as well)
- age_gender_labeles.json

output:
- data/merged_dataframe.pkl
          
