from threading import Thread
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from airline.models import Passager
from utils.mongo_connection import connect_to_mongodb
from utils.logger import configure_logger

logger = configure_logger()


# Create your views here.
def registration_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        # Check if user exists
        current_user = User.objects.filter(username=username).first()
        if current_user is None:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            Passager.objects.create(user=user, first_name=first_name, surname=last_name)
            login(request, user)
            logger.debug(request, str(f"Register user: {username}"))
            messages.success(request, "Successfully registered!")
            return redirect(reverse("airline:main"))
        else:
            messages.error(request,"User already exists!")
            return redirect(reverse("user:registration_request"))
    return render(request, "user/user_registration.html")


def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            logger.debug(f"Login user: {username} ")
            messages.success(request, "Successfully logged in!")
            if user == "Staff" or user.is_superuser:
                Thread(target= connect_to_mongodb, daemon=True).start()
            return redirect(reverse("airline:main"))
        else:
            messages.error(request, "Invalid username or password")
            return redirect(reverse("user:login_request"))
    return render(request, "user/user_login.html")


def logout_request(request):
    logout(request)
    logger.debug(f"Logout user: {request.user.username}")
    messages.success(request, "Successfully logged out!")
    return redirect(reverse("airline:main"))


