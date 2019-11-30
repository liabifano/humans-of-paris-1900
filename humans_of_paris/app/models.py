import os
from django.db import models

import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Gallica(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    gallica_url = models.CharField(max_length=50)
    date = models.CharField(max_length=10)


class Wiki(models.Model):
    wiki_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id =  models.CharField(max_length=10)
    gallica = models.ForeignKey(Gallica, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    # description = models.TextField()
    summary_en = models.TextField(blank=True, null=True)
    summary_fr = models.TextField(blank=True, null=True)
    # bnf_name = models.CharField(max_length=55, null=True)


class Tags(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id =  models.CharField(max_length=10)
    gallica =  models.ForeignKey(Gallica, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, null=True)
