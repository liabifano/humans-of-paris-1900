import os
from django.db import models

from django import forms
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# TODO: improve the data model
# For instance, an record can have multiple names, it should be stored in another table
# The model should be something like GallicaData, NamesData (linked by id with Gallica) and WikipediaData (linked by name in NamesData)
# Next Model: GallicaData > NamesData > WikipediaData


class AllData(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    gallica_url = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=55, null=True)
    # wiki_name = models.CharField(max_length=55, null=True)
    # wiki_url = models.URLField(null=True)
    # wiki_n_langs = models.IntegerField(null=True)
    # wiki_n_categories = models.IntegerField(null=True)
    # wiki_n_links = models.IntegerField(null=True)
    # wiki_n_images = models.IntegerField(null=True)
    # wiki_n_references = models.IntegerField(null=True)
    # wiki_n_content = models.IntegerField(null=True)
    # tag_sex = models.CharField(max_length=2, null=True)
    # tag_profession = models.CharField(max_length=20, null=True)
    # gallica_image_url = models.URLField()
    # image = models.ImageField(upload_to='gallica',
    #                           null=True,
    #                           blank=True)


class Tags(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(max_length=10) # id =  models.ForeignKey(AllData, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, null=True)


class UploadImage(models.Model):
    file = models.ImageField()

