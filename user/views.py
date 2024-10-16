from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import profile as user_profile
import re
# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        passwordconfirm = request.POST.get("password_confirm")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html")
        
        if password != passwordconfirm:
            messages.error(request, "password doesnt match")
            return render(request, "register.html")
        
        if len(password) < 6 or not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
            messages.error(request, "Password must be at least 6 characters long and contain at least one uppercase letter and one digit.")
            return render(request, "register.html")
        
        user = User.objects.create_user(username= username, email= email, password= password)
        user.save()
        messages.success(request, "account was created successfully please login")
        return redirect("login")
        
    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "succefully logged in as " + username )
            return redirect("home")
        else:
            messages.error(request, "error logging in")
    return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return redirect("login")

def profile(request):
    return render(request, "profile.html")

def editprofile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        profile_picture = request.FILES.get("profile_picture")
        user = User.objects.get(id = request.user.id)
        profile = user_profile.objects.get(user = user)

        #check if image is provided
        if profile_picture:
            profile.image = profile_picture
        profile.save()
        if User.objects.filter(username=username).exists() and request.user.username != username:
            messages.error(request, "Username already exists.")
            return redirect("editprofile")
        user.username = username
        user.save()
        messages.success(request, "successfully updated profile")
        return redirect("profile")
        
    return render(request, "editprofile.html")