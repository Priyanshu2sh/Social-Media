from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    posts = PostFiles.objects.select_related('post')
    return render(request, 'home.html', {'posts':posts})

