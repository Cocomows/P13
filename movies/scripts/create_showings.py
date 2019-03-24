import json
import requests
import re
from bs4 import BeautifulSoup
from movies.models import Movie, Theater, Showing
from django.db.utils import IntegrityError
# run with :
# python manage.py runscript create_showings


def get_showings(theater_code):
    url_seances = 'http://www.allocine.fr/seance/salle_gen_csalle=' + theater_code + '.html'
    r = requests.get(url_seances)
    soup = BeautifulSoup(r.text, 'html.parser')

    movies_div = soup.findAll("a", {"class": "meta-title-link"})
    for div in movies_div:
        movie_id = re.search('/film/fichefilm_gen_cfilm=(.+?).html', str(div)).group(1)
        print(movie_id)
        try:
            showing = Showing(movie_id=movie_id, theater_id=theater_code)
            showing.save()
            print("showing created")
        except IntegrityError:
            print("movie not in base or showing already present")


def delete_all():
    # Fetch all movies
    showings = Showing.objects.all()
    # Delete movies
    showings.delete()


def run():
    delete_all()
    for theater in Theater.objects.all():
        print(theater)
        print(theater.theater_code)
        get_showings(theater.theater_code)
