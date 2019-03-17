from django.urls import path
from . import views
from .views import (
    home
    # ShowingsListView,
)

urlpatterns = [
    path('', home, name='movies-home'),
]
