from django.db import models


# TODO: improve the data model
# For instance, an record can have multiple names, it should be stored in another table
# The model should be something like GallicaData, NamesData (linked by id with Gallica) and WikipediaData (linked by name in NamesData)
# Next Model: GallicaData > NamesData > WikipediaData

class AllData(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    gallica_url = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=55)
    wiki_name = models.CharField(max_length=55)
    wiki_url = models.CharField(max_length=75)
    wiki_n_langs = models.IntegerField()
    wiki_n_categories = models.IntegerField()
    wiki_n_links = models.IntegerField()
    wiki_n_images = models.IntegerField()
    wiki_n_references = models.IntegerField()
    wiki_n_content = models.IntegerField()
    gallica_url = models.CharField(max_length=60)
    image = models.ImageField()


