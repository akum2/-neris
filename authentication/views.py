import math
import os
import re
from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
from plagiarism.settings import BASE_DIR


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
        context = {
            'output': output,
            'val': math.ceil(match_percentage),
            'query': input_query,
        }
        return render(request, 'homepages/upload.html', context)
    else:
        context = {
            'val': 'nothing'
        }
    return render(request, 'homepages/upload.html', context)
