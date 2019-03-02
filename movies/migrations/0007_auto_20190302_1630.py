# Generated by Django 2.1.5 on 2019-03-02 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20190129_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='Showing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='Film diffusé')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Theater', verbose_name='Diffusé à')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='showing',
            unique_together={('theater', 'movie')},
        ),
    ]
