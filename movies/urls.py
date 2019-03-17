from django.urls import path
from . import views
from .views import (
    home,
    search,
    # ShowingsListView,
)

urlpatterns = [
    path('', home, name='movies-home'),
    path('search', search, name='search'),
]
