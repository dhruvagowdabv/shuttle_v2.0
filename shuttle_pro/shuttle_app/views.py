from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Home page
def home(request):
    return render(request, 'index.html')


# Booking page — visible to all
def booking(request):
    return render(request, 'booking.html')


# Operator page
def operator(request):
    return render(request,'operator.html')


# Tracking page
def track2(request):
    return render(request,'track2.html')


# About page
def about(request):
    return render(request,'about.html')


# Admin page
def admin(request):
    return render(request,'admin.html')


# Dashboard (optional)
def auth_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'dashboard.html')


# AJAX Login
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Invalid credentials"})
    return JsonResponse({"success": False, "message": "Invalid request"})


# AJAX Signup
@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Username already taken"})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid request"})


# Logout
def logout_view(request):
    logout(request)
    return redirect('home')
