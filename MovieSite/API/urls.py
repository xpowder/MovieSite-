from django.urls import path
from .views import *


urlpatterns = [
    path('movie/', movie_list, name='movie-list'),
    path('movie/<int:pk>/', movie_detail),
    path('register/', User_profile, name='register'),
    path('login/', Login_profile, name='login-profile'),
    path('logout/', Logout_profile, name='logout-profile')
    
]
