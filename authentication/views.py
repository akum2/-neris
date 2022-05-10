from datetime import datetime
from django import views
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.
def home(request):
    date = datetime.now().year
    context = {
        "date": date,
    }
    return render(request, 'home.html', context)


def signup(request):
    # full_name = request.POST.get("name")
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    if request.POST:
        User.objects.create_user(username, email, password)
        return redirect('signin')
    return render(request, "register.html")


def signin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user_login = authenticate(username=username, password=password)
    if user_login is not None:
        return redirect('/home')

    return render(request, "login.html")


def signout(request):
    pass


def welcome(request):
    context = {
        'username': 'yokwejuste'
    }
    return render(request, 'homepages/index.html', context)


def feature(request):
    return render(request, 'homepages/features.html')


def about(request):
    return render(request, 'homepages/about-us.html')


def contact(request):
    return render(request, 'homepages/contact-us.html')


def upload(request):
    return render(request, 'homepages/upload.html')
