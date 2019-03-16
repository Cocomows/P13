from django.urls import path
from . import views
from .views import (
    ShowingsListView,
)

urlpatterns = [
    path('', ShowingsListView.as_view(), name='movies-home'),
]
