from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from airline.models import Passager
from .models import Message
from .forms import MessageAnswerForm
from manage import configure_logger

logger = configure_logger()


# Create your views here.
def registration_request(request):
    context = {}
    if request.method == "POST":
        # Check if user exists
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        current_user = User.objects.filter(username=username).first()
        if current_user is None:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            Passager.objects.create(user=user, first_name=first_name, surname=last_name)

            logger.debug(f"Register user: {username}")
            login(request, user)
            return redirect("airline:main")
        else:
            context["message"] = "User already exists."
    return render(request, "user/user_registration.html", context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            logger.debug(f"Login user: {username} ")
            login(request, user)
            return redirect("airline:main")
        else:
            context["message"] = "Invalid username or password."
    return render(request, "user/user_login.html", context)


def logout_request(request):
    logger.debug(f"Logout user: {request.user.username}")
    logout(request)
    return redirect("airline:main")


