import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apresderniere.settings")
import django
django.setup()
from django.test import TestCase
from movies.scripts.create_movies import (
    get_number_of_pages,
    get_img_links,
    get_movies_json,
    )


class TestScriptMovies(TestCase):
    def setUp(self):
        self.url = 'http://www.allocine.fr/film/aucinema/date-sortie/'
        self.html_mock_up = """
        <figure class="thumbnail ">
            <span class="ACrL3ZACrpZGVvL3BsYXllcl9nZW5fY21lZGlhPTE5NTgzMDc0JmNmaWxtPTI3MTcyMy5odG1s thumbnail-container thumbnail-link"
             title="Bande-annonce Le Je&ucirc;ne, &agrave; la crois&eacute;e des chemins">
                <img class="thumbnail-img" src="data:image/gif;base64,R0lGODlhAwAEAIAAAAAAAAAAACH5BAEAAAAALAAAAAADAAQAAAIDhI9WADs=" 
                data-src="http://fr.web.img3.acsta.net/c_215_290/pictures/19/03/20/14/13/1332979.jpg" 
                alt="Bande-annonce Le Jeûne, à la croisée des chemins" width="216" height="288" />
                <span class="ico-play ico-play-yellow">
                    <span class="ico-play-inner"></span>
                    <i class="ico-play-arrow">
                    <i class="arrow"></i>
                    </i>
                </span>
            </span>
        </figure>"""
        self.jsEntities_mockup = """"var jsEntities = {"Movie_260416":{"id":260416,"qualifiedId":"Movie_260416",
        "type":"Movie","title":"Papillons","social":{"fan_count":1,"user_note_i_want_to_see_count":4},
        "flags":{"isComingSoon":false},"genre":[{"id":"13005","name":"Com\u00e9die"}],
        "releaseDate":"2019-03-30T00:00:00+01:00","poster":{"added_at":{"date":"2018-03-12 00:00:00.000000",
        "timezone_type":3,"timezone":"Europe\/Paris"},"description":"Papillons : Affiche",
        "file_name":"\/pictures\/18\/03\/12\/07\/30\/4563094.jpg","file_type":"poster","id":21492747,
        "id_type":31001,"metas":{"id_main_movie":260416,"image_main_movie":"\/pictures\/18\/03\/12\/07\/30\/4563094.jpg",
        "name_main_movie":"Papillons"}}}};"""

    def test_return_type_get_number_of_pages(self):
        nb = get_number_of_pages(self.url)
        self.assertIsInstance(nb, int)

    def test_return_type_get_img_links(self):
        img_links = get_img_links(self.html_mock_up)
        self.assertIsInstance(img_links, list)

    def test_results_get_img_links(self):
        img_links = get_img_links(self.html_mock_up)
        for link in img_links:
            self.assertTrue("http://" in link or "data:image" in link)

    def test_results_get_movies_json(self):
        returned_json = get_movies_json(self.jsEntities_mockup)
        self.assertTrue('Movie_260416' in returned_json)


