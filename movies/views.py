from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DeleteView
)
from django.core.paginator import Paginator
from .models import Movie, Theater, Save
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.contrib.postgres.search import TrigramSimilarity
import django.contrib.postgres.search
# Create your views here.


def home(request):

    movies_list = Movie.objects.filter(showing__movie__isnull=False).order_by('release_date').distinct()

    paginator = Paginator(movies_list, 12)

    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'movies/pages/home.html', {'movies': movies, 'is_paginated': paginator.num_pages > 1})


def movies_in_theater(request):

    code = request.GET.get('theater')
    theater = Theater.objects.get(theater_code=code)

    movies_list = Movie.objects.filter(showing__theater__theater_code=code).order_by('release_date').distinct()

    paginator = Paginator(movies_list, 12)

    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'movies/pages/theater.html', {'theater': theater, 'movies': movies,
                                                         'is_paginated': paginator.num_pages > 1})


def theaters_view(request):

    theaters_list = Theater.objects.annotate(number_of_showings=Count('showing')).filter(number_of_showings__gte=1).order_by('-number_of_showings')
    paginator = Paginator(theaters_list, 25)

    page = request.GET.get('page')
    theaters = paginator.get_page(page)
    return render(request, 'movies/pages/theaters.html', {'theaters': theaters, 'is_paginated': True})


def search(request):

    query = request.GET.get('query')

    if not query:
        movies_list = Movie.objects.none()
    else:
        search_trigram = Movie.objects.annotate(similarity=TrigramSimilarity('title', query),)\
                 .filter(similarity__gt=0.3).order_by('-similarity')
        search_contain = Movie.objects.filter(title__icontains=query)
        movies_list = search_trigram | search_contain
        movies_list = movies_list.order_by('release_date')
    paginator = Paginator(movies_list, 12)

    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'movies/pages/results.html', {'movies': movies, 'is_paginated':  paginator.num_pages > 1,
                                                         'query': query})


def movie(request):

    code = request.GET.get('movie')
    selected_movie = Movie.objects.get(allocine_code=code)

    theaters_list = Theater.objects.filter(showing__movie__allocine_code=code).distinct()

    paginator = Paginator(theaters_list, 12)

    page = request.GET.get('page')
    theaters = paginator.get_page(page)

    return render(request, 'movies/pages/movie.html', {'movie': selected_movie, 'theaters': theaters})


def about(request):

    return render(request, 'movies/pages/about.html')


@login_required
def save_movie(request):

    code = request.GET.get('code')
    movie_to_save = Movie.objects.get(allocine_code=code)

    try:
        save = Save(saved_by=request.user, saved_movie=movie_to_save)
        save.save()
        messages.success(request, 'Le film {} a bien été enregistré dans votre liste de films sauvegardés'.format(movie_to_save.title))
    except IntegrityError as error:
        print(error)
        messages.warning(request, "Vous avez déjà enregistré ce film précédemment, "
                         "il n'a pas été rajouté à votre liste de films sauvegardés.")

    return redirect('saved-movies')


class SaveDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Save
    template_name = 'movies/pages/save_confirm_delete.html'
    success_url = '/saved-movies'

    def test_func(self):
        save = self.get_object()
        if self.request.user == save.saved_by:
            return True
        return False


class UserSavedMoviesList(ListView):

    model = Save
    template_name = 'movies/pages/saved_movies.html'
    context_object_name = 'saves'
    paginate_by = 12
    ordering = ['-date']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Save.objects.filter(saved_by=user).order_by('-date')
