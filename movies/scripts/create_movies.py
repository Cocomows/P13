import json
import requests
from bs4 import BeautifulSoup
from movies.models import Movie


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
    end = request_text[begin:].find(';')
    json_string = json_string[len(keyword):end]
    return json.loads(json_string)


def get_info(url):
    total_pages = get_number_of_pages(url)
    for current_page in range(total_pages, 0, -1):
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

            movie = Movie(allocine_code=allocine_id, title=title, poster_url=poster_link, release_date=release_date)
            movie.save()


def run():
    url_seances = 'http://www.allocine.fr/film/aucinema/date-sortie/'
    get_info(url_seances)

