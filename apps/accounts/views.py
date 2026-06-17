import json
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login   
from django.contrib import messages
import datetime, random
from .utils import send_reset_link, verify_otp_mail

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

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email, username=username, name=name, date_of_birth=date_of_birth)
        user.otp = random.randint(100000, 999999)
        user.set_password(password)
        user.save()

        verify_otp_mail(user)

        return redirect("verify", id=user.id)
        
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

def verify(request, id):
    if request.method == 'POST':
        code = request.POST.get('code')
        
        if id in ['', None]:
            messages.error(request, 'Please create an account.')
            return redirect('register')

        try:
            user = User.objects.get(id=id)
            if user.otp != str(code):
                messages.error(request, 'Invalid code.')
                return redirect('verify', id=id)
            
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('home')
        
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('register')

    return render(request, 'accounts/verify.html', {'id':id})

def re_send_otp(request, id):
    try:
        user = User.objects.get(id=id)
        verify_otp_mail(user)
        messages.info(request, 'OTP resent.')
        return redirect('')
    except User.DoesNotExist:
        messages.error(request, 'Something went wrong. Invalid user identity.')



def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('identifier')
        
        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()

        if user:
            reset_url = user.get_password_reset_url()
            
        send_reset_link(user, reset_url)

        return JsonResponse({"status": 200})

    return render(request, 'accounts/forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'POST':
        newpass = request.POST.get('newpass')

        if user is not None:
            user.set_password(newpass)
            user.save()
            messages.success(request, 'Password reset successfully. Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong. Invalid user identity.')
            return redirect('login')

    return render(request, 'accounts/reset_password.html', {
        'uidb64': uidb64,
        'token': token
    })
