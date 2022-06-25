from datetime import datetime

from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from authentication.forms import *


def home(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    date = datetime.now().year
    context = {
        "date": date,
    }
    return render(request, 'home.html', context)


def signup(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('welcome')
    else:
        if request.POST:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('signin')
            context['form'] = form

        else:
            form = UserRegistrationForm()
            context['form'] = form
            return render(request, "register.html", context)
    return render(request, "register.html", context)


def signin(request):
    context = {
        'title': 'signin',
        'active_s': 'active'
    }
    if request.user.is_authenticated:
        return redirect('welcome')
    else:
        if request.POST:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                user_name = request.POST['username']
                password = request.POST['password']
                user = authenticate(
                    request,
                    username=user_name,
                    password=password
                )
                if user is not None:
                    login(request, user)
                    return redirect('welcome')
        else:
            form = UserLoginForm()
            context['login_form'] = form
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='/signin')
def welcome(request):
    context = {
        'title': 'Home',
        'active_w': 'active'
    }
    return render(request, 'homepages/index.html', context)


@login_required(login_url='/signin')
def feature(request):
    context = {
        'title': 'Feature',
        'active_f': 'active'
    }
    return render(request, 'homepages/features.html', context)


@login_required(login_url='/signin')
def about(request):
    user_data = TheUsers.objects.filter(is_admin=True)
    context = {
        'title': 'About',
        'active_a': 'active',
        'user_data': user_data,
    }
    return render(request, 'homepages/about-us.html', context)


@login_required(login_url='/signin')
def contact(request):
    context = {
        'title': 'Contact',
        'active_c': 'active'
    }
    return render(request, 'homepages/contact-us.html', context)


@login_required(login_url='/signin')
def upload(request):
    if request.POST:
        form = UploadedDocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload')


@login_required
def profile(request):
    context = {
        'title': 'Profile',
        'active': 'active'
    }
    return render(request, 'homepages/profile.html', context)


@login_required
def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect("sigin")
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated")
            return redirect('profile')
    else:
        form = UpdateUserForm(instance=request.user)
        context = {
            'title': 'Profile Edit',
            'active': 'active',
            'form': form
        }
        return render(request, 'homepages/profile-edit.html', context)
