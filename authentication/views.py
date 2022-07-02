import math
import re
import urllib
from datetime import datetime
from urllib.error import URLError

from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

from authentication.checker import lcs
from authentication.forms import *


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
                    username = user_name,
                    password = password
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Authentication successful')
                    return redirect('welcome')
        else:
            form = UserLoginForm()
            context['login_form'] = form
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url = '/signin')
def welcome(request):
    context = {
        'title': 'Home',
        'active_w': 'active'
    }
    messages.info(request, 'Welcome to the home page, try and upload a file!')
    return render(request, 'homepages/index.html', context)


@login_required(login_url = '/signin')
def feature(request):
    context = {
        'title': 'Feature',
        'active_f': 'active'
    }
    return render(request, 'homepages/features.html', context)


@login_required(login_url = '/signin')
def about(request):
    user_data = TheUsers.objects.filter(is_admin = True)
    context = {
        'title': 'About',
        'active_a': 'active',
        'user_data': user_data,
    }
    return render(request, 'homepages/about-us.html', context)


@login_required(login_url = '/signin')
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


@login_required(login_url = '/signin')
def upload(request):
    form = UploadedDocumentsForm(request.POST, request.FILES)
    if request.POST:
        if form.is_valid():
            form_stack = form.save(commit = False)
            form_stack.serialised_content = "bala"
            form_stack.plagiarism_status = 'Hello'
            tokenizer = request.FILES['document'].read()
            tokenizer_pro = tokenizer.decode('utf-8')
            try:
                form_stack.save()
                messages.success(request, 'Document uploaded successfully')
            except ValueError as e:
                messages.error(request, e)
            except ValidationError as e:
                messages.error(request, e)
            except Exception as e:
                messages.error(request, e)
            # For most common english words check
            universal_set_of_unique_words = []
            lowercase_query = tokenizer_pro.lower()
            query_word_list = re.sub("[\w]", " ", lowercase_query).split()
            for word in query_word_list:
                if word not in universal_set_of_unique_words:
                    universal_set_of_unique_words.append(word)
            try:
                url = "https://plagio-store.s3.eu-west-3.amazonaws.com/dataset/most_common_words.docx"
                fd1 = urllib.request.urlopen(url)
                fdn = fd1.read()
                fd = fdn.decode("utf-8")
            except URLError:
                messages.warning(request, "Error in connecting to the server")
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
            try:
                match_percentage = float(
                    dot_product / (query_vector_magnitude * database_vector_magnitude)) * 100
            except ZeroDivisionError:
                match_percentage = 0
            output = "Input query text matches %0.02f%% with database." % match_percentage
            # Check for Plagiarism status
            try:
                fila = urllib.request.urlopen(
                    'https://plagio-store.s3.eu-west-3.amazonaws.com/dataset/sample.docx'
                ).read()
            except URLError:
                messages.warning(request, 'Network issues caused an error!')
            f = fila.decode("utf-8")

            orig = f.replace("\n", " ")  # tokenizing

            f2 = tokenizer_pro
            plag = f2.replace("\n", " ")  # tokenizer

            tokens_o = word_tokenize(orig)
            tokens_p = word_tokenize(plag)

            # lowerCase
            tokens_o = [token.lower() for token in tokens_o]
            tokens_p = [token.lower() for token in tokens_p]

            # stop word removal
            # punctuation removal
            stop_words = set(stopwords.words('english'))
            punctuations = ['"', '.', '(', ')', ',', '?', ';', ':', "''", '``']
            filtered_tokens_o = [
                w for w in tokens_o if not w in stop_words and not w in punctuations
            ]
            filtered_tokens_p = [
                w for w in tokens_p if not w in stop_words and not w in punctuations
            ]

            # Trigram Similiarity measures
            trigrams_o = []
            for i in range(len(tokens_o) - 2):
                t = (tokens_o[i], tokens_o[i + 1], tokens_o[i + 2])
                trigrams_o.append(t)

            s = 0
            trigrams_p = []
            for i in range(len(tokens_p) - 2):
                t = (tokens_p[i], tokens_p[i + 1], tokens_p[i + 2])
                trigrams_p.append(t)
                if t in trigrams_o:
                    s += 1

            # jaccord coefficient = (S(o)^S(p))/(S(o) U S(p))
            """
            Here, we find the number of overlapping trigrams in
            the two texts, i.e the number of continuous sequences
            of three words which are present in both texts.
            """
            J = s / (len(trigrams_o) + len(trigrams_p))

            # containment measure
            """
            The containment measure C is a better metric for
            or document pairs with varied document lengths.
            Here, we normalize by the trigrams in the suspicious
            """
            try:
                C = s / len(trigrams_p)
            except ZeroDivisionError:
                C = 0

            sent_o = sent_tokenize(orig)
            sent_p = sent_tokenize(plag)

            # maximum length of LCS for a sentence in suspicious text
            max_lcs = 0
            sum_lcs = 0

            for i in sent_p:
                for j in sent_o:
                    l = lcs(i, j)
                    max_lcs = max(max_lcs, l)
                sum_lcs += max_lcs
                max_lcs = 0
            try:
                score = sum_lcs / len(tokens_p)
            except ZeroDivisionError:
                score = 0

            messages.success(request, "Your query has been processed successfully.")
            context = {
                'title': 'Upload',
                'active_u': 'active',
                'output': output,
                'method': request.method == 'POST',
                'match_percentage': math.ceil(match_percentage),
                'rest_percentage': 100 - math.ceil(match_percentage),
                'score': math.ceil(score),
                'jaccard_coeficent': J,
                'containment_measure': C,
                'trigram_similarity': score,
            }
            return redirect('results')
        else:
            context = {
                'form': form
            }
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'homepages/upload.html', context)
    else:
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
                              instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated")
            return redirect('profile')
    else:
        form = UpdateUserForm(instance = request.user)
        context = {
            'title': 'Profile Edit',
            'active': 'active',
            'form': form
        }
        return render(request, 'homepages/profile-edit.html', context)


@login_required
def downloadable(request):
    records = UploadedDocuments.objects.all()
    context = {
        'records': records,
    }
    return render(request, 'homepages/uploads_reords.html', context)
