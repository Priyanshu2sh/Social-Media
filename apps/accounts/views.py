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

        user = User.objects.filter(email=email, is_verified=True)
        if user:
            messages.error(request, 'Email already exist.')
            return redirect('register')

        user = User.objects.filter(username=username, is_verified=True)
        if user:
            messages.error(request, 'Username already exist.')
            return redirect('register')

        date_of_birth = datetime.date(int(year), int(month), int(day))

        user, _ = User.objects.get_or_create(email=email, username=username, name=name, date_of_birth=date_of_birth)
        user.otp = random.randint(100000, 999999)
        user.set_password(password)
        user.save()

        return render(request, 'accounts/verify.html', {'user_id': user.id, 'user_email': user.email})
        
    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        print(identifier, password)

        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()

        if user is None:
            messages.error(request, "Invalid Email/Username ")
            return redirect('/')

        user = authenticate(username=user.username, password=password)

        if not user:
            messages.error(request, "Invalid Password")
            return redirect('/')
        
        login(request, user)
        return redirect('home')

    return render(request, 'accounts/login.html')

def verify(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        code = request.POST.get('code')
        
        if user_id in ['', None]:
            messages.error(request, 'Please create an account.')
            return redirect('register')

        try:
            user = User.objects.get(id=user_id)
            if user.otp != str(code):
                messages.error(request, 'Invalid code.')
                return render(request, 'accounts/verify.html', {'user_id': user.id, 'user_email': user.email})
            
            login(request, user)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('register')

    return render(request, 'accounts/verify.html')