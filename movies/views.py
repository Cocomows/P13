from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator
from .models import Movie, Showing, Theater
from django.db.models import Count
# Create your views here.


def home(request):
    # showings_list = Showing.objects.all()

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
    return render(request, 'movies/pages/theater.html', {'theater': theater, 'movies': movies, 'is_paginated': paginator.num_pages > 1})


def theaters_view(request):
    # theaters_list = Theater.objects.all()
    q = Theater.objects.annotate(number_of_showings=Count('showing')).filter(number_of_showings__gte=1).order_by('-number_of_showings')
    paginator = Paginator(q, 25)

    page = request.GET.get('page')
    theaters = paginator.get_page(page)
    return render(request, 'movies/pages/theaters.html', {'theaters': theaters, 'is_paginated': True})


def search(request):

    query = request.GET.get('query')

    if not query:

        movies = Movie.objects.all()
    else:
        movies = Movie.objects.filter(title__icontains=query)

    return render(request, 'movies/pages/results.html', {'movies': movies, 'is_paginated': True, 'query': query})

#
# class ShowingsListView(ListView):
#     model = Showing
#     template_name = 'movies/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'showings'
#     # ordering = Showing.movie.release_date
#     paginate_by = 8

#
# class MovieListView(ListView):
#     model = Movie
#     template_name = 'movies/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'movies'
#     ordering = ['release_date']
#     paginate_by = 8
