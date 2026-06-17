from django.urls import path
from .views import *

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('verify/<int:id>/', verify, name='verify'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', reset_password, name='reset_password'),
]
