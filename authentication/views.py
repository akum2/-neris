from datetime import datetime
import docx2txt
import requests, re, math
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.shortcuts import redirect, render
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from authentication.forms import *
from plagiarism.settings import MEDIA_ROOT


def home(request):
    date = datetime.now().year
    context = {
        "date": date,
    }
    return render(request, 'home.html', context)


def signup(request):
    context = {}
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


def results(request):
    context = {
        'title': 'Results',
        'active_r': 'active'
    }
    return render(request, 'homepages/results.html', context)



@login_required(login_url='/signin')
def upload(request):
    form = UploadedDocumentsForm(request.POST, request.FILES)
    if request.POST:
        tokenizer_pro = form.serialised_content = docx2txt.process(
            form.document,
            f'{MEDIA_ROOT}/docs'
        )
        if form.is_valid():
            form.save()
            # For most common english words check
            universal_set_of_unique_words = []
            lowercase_query = tokenizer_pro.lower()
            query_word_list = re.sub("[\w]", " ", lowercase_query).split()
            for word in query_word_list:
                if word not in universal_set_of_unique_words:
                    universal_set_of_unique_words.append(word)
            fd = requests.get("https://plagio-store.s3.eu-west-3.amazonaws.com/dataset/most_common_words.docx")
            database1 = fd.lower()
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

            # Check for Plagiarism status
            f = requests.get('')
            orig=f.read().replace("\n"," ")
            f.close()

            f2=open('hello.docx',"r")
            plag=f2.read().replace("\n"," ")
            f2.close()


            messages.success(request, "Your query has been processed.")
            context ={
                'title': 'Upload',
                'active_u': 'active',
                'output': output,
                'match_percentage': match_percentage,
            }
            return render(request, 'homepages/results.html', context)
    context = {
        'title': 'Upload',
        'active_u': 'active',
        'form': form,
    }
    return render(request, 'homepages/upload.html', context)


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
        form = UpdateUserForm(request.POST, request.FILES,
                              instance=request.user)
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
