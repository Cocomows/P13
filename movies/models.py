from django.db import models

# Create your models here.


class Movie(models.Model):

    title = models.CharField(verbose_name="Title", max_length=100)
    poster_url = models.URLField(blank=True)
    allocine_code = models.IntegerField(verbose_name="ID allocine", primary_key=True)
    release_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Theater(models.Model):

    name = models.CharField(verbose_name="Name", max_length=100)
    theater_code = models.CharField(max_length=6, primary_key=True)
    address = models.CharField(verbose_name="Address", max_length=200)

    def __str__(self):
        return self.name


class Showing(models.Model):

    class Meta:
        unique_together = (('theater', 'movie'),)

    movie = models.ForeignKey(Movie, to_field='allocine_code', verbose_name="Film diffusé", on_delete=models.CASCADE,)
    theater = models.ForeignKey(Theater, to_field='theater_code', verbose_name="Diffusé à", on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.theater).capitalize()+" diffuse le film "+str(self.movie)

