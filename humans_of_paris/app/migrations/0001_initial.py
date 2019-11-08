# Generated by Django 2.2.7 on 2019-11-08 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllData',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('gallica_url', models.CharField(max_length=50)),
                ('date', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=55, null=True)),
                ('wiki_name', models.CharField(max_length=55, null=True)),
                ('wiki_url', models.URLField(null=True)),
                ('wiki_n_langs', models.IntegerField(null=True)),
                ('wiki_n_categories', models.IntegerField(null=True)),
                ('wiki_n_links', models.IntegerField(null=True)),
                ('wiki_n_images', models.IntegerField(null=True)),
                ('wiki_n_references', models.IntegerField(null=True)),
                ('wiki_n_content', models.IntegerField(null=True)),
                ('tag_sex', models.CharField(max_length=2, null=True)),
                ('tag_profession', models.CharField(max_length=20, null=True)),
                ('gallica_image_url', models.URLField()),
            ],
        ),
    ]
