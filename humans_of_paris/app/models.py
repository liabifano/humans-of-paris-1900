import os
from django.db import models

import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Person(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    bnf_link = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, blank=True, null=True)
    note = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    lang = models.CharField(max_length=50, blank=True, null=True)
    born = models.CharField(max_length=50, blank=True, null=True)
    died = models.CharField(max_length=50, blank=True, null=True)


class Gallica(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    gallica_url = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    n_images_wiki = models.FloatField(blank=True, null=True)
    summary_size = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

class Tags(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gallica = models.ForeignKey(Gallica, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, null=True)


class Wiki(models.Model):
    wiki_url =  models.CharField(max_length=50)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    english = models.BooleanField(blank=True, null=True)
    french = models.BooleanField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    n_images = models.BigIntegerField(blank=True, null=True)
    rank = models.FloatField(blank=True, null=True)
