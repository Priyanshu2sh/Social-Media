from django.shortcuts import render, redirect
from .models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login   
from django.contrib import messages
import datetime, random

# Create your views here.
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')
        name = request.POST.get('name')
        username = request.POST.get('username')

        user = User.objects.filter(email=email)
        if user:
            messages.error(request, 'User with this email already exist.')

        user = User.objects.filter(username=username)
        if user:
            messages.error(request, 'Username already exist.')

        date_of_birth = datetime.date(int(year), int(month), int(day))

        user = User(email=email, username=username, name=name, date_of_birth=date_of_birth)
        user.otp = random.randint(100000, 999999)
        user.set_password(password)
        user.save()

        return render(request, 'accounts/verify.html', {'user_id': user.id})

        
    return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        print(identifier, password)

        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()

        if user is None:
            messages.error(request, "Invalid Email/Username ")
            return redirect('/')
        
        user = authenticate(username=user.username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/')
        
        # return render(request, '')

    return render(request, 'accounts/login.html')

def verify(request):
    if request.method == 'POST':
        pass

    return render(request, 'accounts/verify.html')