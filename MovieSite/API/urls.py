from django.urls import path
from .views import *

from rest_auth.views import LoginView, LogoutView



urlpatterns = [
    path('movie/', movie_list, name='movie-list'),
    path('movie/<int:pk>/', movie_detail)
    
]
