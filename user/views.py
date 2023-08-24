from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.contrib.auth.models import User
from airline.models import Passager
from utils.logger import configure_logger

logger = configure_logger()


# Create your views here.
def registration_request(request):
    context = {}
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
            logger.debug(f"Register user: {username}")
            context={'message':'Register succesfuly!'}
            return render(request, "airline/main.html", context=context)
        else:
            context={"message" : "User already exists."}
    return render(request, "user/user_registration.html", context=context)


def login_request(request):
    context={}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            logger.debug(f"Login user: {username} ")
            context={"message":"Loggin succesfuly!"}
            return render(request, "airline/main.html", context=context)
        else:
            context={"message":"Invalid username or password."}
    return render(request, "user/user_login.html", context=context)


def logout_request(request):
    logout(request)
    logger.debug(f"Logout user: {request.user.username}")
    context={"message":"Logout Succesfuly!"}
    return render(request, "airline/main.html", context=context)


