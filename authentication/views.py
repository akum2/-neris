import math
import os
import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from authentication.forms import *
from plagiarism.settings import BASE_DIR


def home(request):
    date = datetime.now().year
    context = {
        "date": date,
    }
    return render(request, 'home.html', context)


def signup(request):
    form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "register.html", context)


def signin(request):
    context = {}
    # request.session.set_expiry(datetime.day)
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


def signout(request):
    logout(request)
    return redirect('/logout')


@login_required(login_url='/signin')
def welcome(request):
    context = {
        'username': 'yokwejuste'
    }
    return render(request, 'homepages/index.html', context)


@login_required(login_url='/signin')
def feature(request):
    return render(request, 'homepages/features.html')


@login_required(login_url='/signin')
def about(request):
    return render(request, 'homepages/about-us.html')


@login_required(login_url='/signin')
def contact(request):
    return render(request, 'homepages/contact-us.html')


@login_required(login_url='/signin')
def upload(request):
    if request.POST:
        universal_set_of_unique_words = []
        input_query = request.POST.get("hidden")
        lowercase_query = input_query.lower()
        query_word_list = re.sub("[\w]", " ", lowercase_query).split()
        for word in query_word_list:
            if word not in universal_set_of_unique_words:
                universal_set_of_unique_words.append(word)
        fd = open(os.path.join(BASE_DIR, "database1.txt"), "r")
        database1 = fd.read().lower()
        database_word_list = re.sub("[\w]", " ", database1).split()
        for word in database_word_list:
            if word not in universal_set_of_unique_words:
                universal_set_of_unique_words.append(word)
        query_tf = []
        database_tf = []
        for word in universal_set_of_unique_words:
            query_tf_counter = 0
            database_tf_counter = 0
            for word2 in query_word_list:
                if word == word2:
                    query_tf_counter += 1
            query_tf.append(query_tf_counter)
            for word2 in database_word_list:
                if word == word2:
                    database_tf_counter += 1
            database_tf.append(database_tf_counter)
        dot_product = 0
        for i in range(len(query_tf)):
            dot_product += query_tf[i] * database_tf[i]
        query_vector_magnitude = 0
        for i in range(len(query_tf)):
            query_vector_magnitude += query_tf[i] ** 2
        query_vector_magnitude = math.sqrt(query_vector_magnitude)
        database_vector_magnitude = 0
        for i in range(len(database_tf)):
            database_vector_magnitude += database_tf[i] ** 2
        database_vector_magnitude = math.sqrt(database_vector_magnitude)
        match_percentage = float(dot_product / (query_vector_magnitude * database_vector_magnitude)) * 100
        output = "Input query text matches %0.02f%% with database." % match_percentage
        messages.success(request, "Your query has been processed.")
        context = {
            'output': output,
            'val': math.ceil(match_percentage),
            'query': input_query,
        }
        return render(request, 'homepages/upload.html', context)
    else:
        context = {
            'val': 'nothing',
        }
    return render(request, 'homepages/upload.html', context)
