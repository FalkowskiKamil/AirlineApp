from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from airline.models import Passager
from .models import Message
from manage import configure_logger

logger = configure_logger()


# Create your views here.
def registration_request(request):
    """
    Handles the user registration request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template or a redirect response.
    """
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
    """
    Handles the user login request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template or a redirect response.
    """
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
    """
    Handles the user logout request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect response.
    """
    logger.debug(f"Logout user: {request.user.username}")
    logout(request)
    return redirect("airline:main")


def message(request):
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(recipient=request.user)
    messages = messages.order_by('-date')[:10]
    context = {
        "messages": messages
    }
    Message.objects.filter(recipient=request.user).update(is_read=True)
    return render(request, template_name="user/message.html", context=context)