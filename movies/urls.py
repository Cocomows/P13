from django.urls import path
from . import views
from .views import (
    home,
    search,
    theaters_view,
    movies_in_theater,
    movie,
    # ShowingsListView,
)

urlpatterns = [
    path('', home, name='movies-home'),
    path('search', search, name='search'),
    path('theaters', theaters_view, name='theaters'),
    path('theater', movies_in_theater, name='theater'),
    path('movie', movie, name='movie')
]
