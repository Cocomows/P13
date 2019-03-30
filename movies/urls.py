from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='movies-home'),
    path('search', views.search, name='search'),
    path('theaters', views.theaters_view, name='theaters'),
    path('theater', views.movies_in_theater, name='theater'),
    path('movie', views.movie, name='movie'),
    path('about', views.about, name='about'),
    path('save', views.save_movie, name='save'),
    path('saved-movies', login_required(views.UserSavedMoviesList.as_view()), name='saved-movies'),
    path('save/<int:pk>/delete/', views.SaveDeleteView.as_view(), name='save-delete'),
]
