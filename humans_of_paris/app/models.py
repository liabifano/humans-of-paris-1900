import os
from django.db import models

import uuid



class Person(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    gallica_url = models.CharField(max_length=50)
    gallica_identifier = models.CharField(max_length=10)
    bnf_link = models.CharField(max_length=50)
    note = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    gender_estimate = models.FloatField(blank=True, null=True)
    age_estimate = models.FloatField(blank=True, null=True)
    summary_size = models.FloatField(blank=True, null=True)
    n_images_wiki = models.BigIntegerField(blank=True, null=True)


class Gallica(models.Model):
    gallica_id = models.CharField(max_length=10, primary_key=True)
    gallica_url = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Tags(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, null=True)


class Wiki(models.Model):
    wiki_en_link =  models.CharField(max_length=50)
    wiki_fr_link =  models.CharField(max_length=50)
    wiki_en_text =  models.TextField()
    wiki_fr_text =  models.TextField()
    wiki_text = models.TextField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    summary_size = models.FloatField(blank=True, null=True)
    n_images_wiki = models.BigIntegerField(blank=True, null=True)
