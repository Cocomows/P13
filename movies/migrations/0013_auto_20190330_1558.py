# Generated by Django 2.1.5 on 2019-03-30 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_auto_20190330_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theater',
            name='address',
            field=models.CharField(max_length=500, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='theater',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
    ]
