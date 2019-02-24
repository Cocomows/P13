from django.urls import path
from . import views
from .views import (
    MovieListView,
)

urlpatterns = [
    path('', MovieListView.as_view(), name='movies-home'),
]
