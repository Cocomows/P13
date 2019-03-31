from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .models import Movie
from django.urls import reverse
from users.views import profile


class MovieModelTests(TestCase):

    def test_str(self):
        """
        test str method for the model Movie
        """
        movie = Movie(allocine_code='171198', title='La Grande Aventure Lego',
                      poster_url=
                      'http://fr.web.img5.acsta.net/c_215_290/pictures/210/618/21061838_20131128144957302.jpg',
                      release_date='2014-02-19T00:00:00+01:00')

        self.assertIs(movie.__str__(), "La Grande Aventure Lego")


class ViewsTests(TestCase):

    def test_homepage(self):
        """
        Test access to homepage
        """
        response = self.client.get(reverse('movies-home'))
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Après dernière")

    def test_search(self):
        """
        Test access to search page without search terms
        """
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Malheureusement")

    def test_search_arg(self):
        """
        Test access to search page with search terms
        """
        response = self.client.get(reverse('search'), {'query': 'bonjour'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Résultats de la recherche')


class UserLoggedIn(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='Jean', email='jean@jean.com', password='passw0rd')

    def test_user_saved_page_logged_in(self):
        request = self.factory.get(reverse('saved-movies'))
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jean@jean.com")
