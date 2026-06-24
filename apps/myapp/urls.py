from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('create/post/', create_post, name='create-post'),
    path('profile/', profile, name='profile'),

]