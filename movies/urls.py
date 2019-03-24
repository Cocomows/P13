from django.urls import path
from . import views
from .views import (
    home,
    search,
    theaters_view
    # ShowingsListView,
)

urlpatterns = [
    path('', home, name='movies-home'),
    path('search', search, name='search'),
    path('theaters', theaters_view, name='theaters')
]
