import requests
from bs4 import BeautifulSoup
import re
from movies.models import Theater

link_theaters = "http://www.allocine.fr/recherche/2/"


def get_paris_theaters(page):
    payload = {'p': page,
               'q': "paris arrondissement"
               }
    r = requests.get(link_theaters, params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')

    all_p = soup.find_all('p', {'class': 'purehtml'})

    for p in all_p:
        theater_name = p.a.get_text()[1:]
        theater_link = p.a.get('href')
        theater_id = re.search('/seance/salle_gen_csalle=(.+?).html', theater_link).group(1)

        p_text = p.get_text()
        address = p_text.replace(theater_name + ' -\n', '')
        address = address.replace("\n", ' ')
        address = address.strip()

        theater = Theater(name=theater_name, theater_code=theater_id, address=address)
        theater.save()

    return


def run():
    total_pages = 6
    for current_page in range(1, total_pages+1):
        get_paris_theaters(current_page)
