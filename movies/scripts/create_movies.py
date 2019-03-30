import json
import requests
import time
from bs4 import BeautifulSoup
from movies.models import Movie
from datetime import datetime, timedelta

# run with :
# python manage.py runscript create_movies


def get_number_of_pages(url):
    page = 99
    payload = {'page': str(page),
               }
    r = requests.get(url, params=payload)
    return int(r.url[-2:])


def get_img_links(request_text):
    soup = BeautifulSoup(request_text, 'html.parser')
    img_links = []
    for img in soup.find_all('img'):
        img_links.append(img.get('data-src'))
        img_links.append(img.get('src'))
    img_links = list(filter(None, img_links))
    return img_links


def get_movies_json(request_text):
    keyword = 'jsEntities = '
    begin = request_text.find(keyword)
    json_string = request_text[begin:]
    end = request_text[begin:].find('};')
    json_string = json_string[len(keyword):end+1]
    print(json_string)
    return json.loads(json_string)


def get_info(url):
    total_pages = get_number_of_pages(url)
    for current_page in range(total_pages, 0, -1):
        time.sleep(2)
        print("page : "+str(current_page))
        payload = {'page': str(current_page),
                   }
        r = requests.get(url, params=payload)

        img_links = get_img_links(r.text)

        movies = get_movies_json(r.text)

        for movie in movies:
            release_date = movies[movie]['releaseDate']
            title = movies[movie]['title']
            allocine_id = movies[movie]['id']
            poster_link = ''
            if movies[movie]['poster']:
                partial_poster_link = movies[movie]['poster']['file_name']
            else:
                partial_poster_link = 'error'

            for link in img_links:
                if partial_poster_link in link:
                    poster_link = link
            today = datetime.now()

            release_date_cut = release_date[:-6]

            datetime_release = datetime.strptime(release_date_cut, "%Y-%m-%dT%H:%M:%S")

            date_N_days_ago = today - timedelta(days=180)

            if datetime_release < date_N_days_ago:
                print(release_date+" - "+str(datetime_release)+" - "+title)
                movie = Movie(allocine_code=allocine_id, title=title, poster_url=poster_link, release_date=release_date)
                movie.save()
            else:
                return


def delete_all():
    # Fetch all movies
    movies = Movie.objects.all()
    # Delete movies
    movies.delete()


def run():
    # delete_all()
    url_seances = 'http://www.allocine.fr/film/aucinema/date-sortie/'
    get_info(url_seances)

