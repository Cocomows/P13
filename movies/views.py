from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Movie, Showing
# Create your views here.


# def home(request):
#     context = {
#         'movies': Movie.objects.all()
#     }
#     return render(request, 'movies/home.html', context=context)
#

class ShowingsListView(ListView):
    model = Showing
    template_name = 'movies/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'showings'
    # ordering = Showing.movie.release_date
    paginate_by = 8

#
# class MovieListView(ListView):
#     model = Movie
#     template_name = 'movies/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'movies'
#     ordering = ['release_date']
#     paginate_by = 8
