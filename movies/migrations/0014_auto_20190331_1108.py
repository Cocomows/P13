# Generated by Django 2.1.5 on 2019-03-31 09:08

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_auto_20190330_1558'),
    ]

    operations = [
        TrigramExtension(),
    ]
