from django.urls import path
from .views import *

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('verify/', verify, name='verify'),
]
