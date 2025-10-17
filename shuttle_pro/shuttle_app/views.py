from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AuthLog

def home(request):
    # Show message if redirected from login_required
    if 'next' in request.GET and request.GET['next'] == '/booking/':
        messages.info(request, 'Please login or sign up to access the booking page.')
    return render(request, 'index.html')

@login_required(login_url='home')
def booking(request):
    return render(request, 'booking.html')

def operator(request):
    return render(request,'operator.html')

def track2(request):
    return render(request,'track2.html')

def about(request):
    return render(request,'about.html')

def admin(request):
    return render(request,'admin.html')

# -------------------------------
# Login / Signup with JSON response
# -------------------------------
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({'success': True})

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')

# -------------------------------
# Dashboard
# -------------------------------
@login_required
def auth_dashboard(request):
    logs = AuthLog.objects.all()[:10]
    return render(request, 'auth_dashboard.html', {'logs': logs})
   