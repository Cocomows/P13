from django.db import models

# Create your models here.


class Movie(models.Model):

    title = models.CharField(verbose_name="Title", max_length=100)
    poster_url = models.URLField(blank=True)
    allocine_code = models.IntegerField(verbose_name="ID allocine", default="0")
    release_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Theater(models.Model):

    name = models.CharField(verbose_name="Name", max_length=100)
    theater_code = models.CharField(max_length=6)
    address = models.CharField(verbose_name="Address", max_length=200)

    def __str__(self):
        return self.name
