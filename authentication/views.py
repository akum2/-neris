import math
import re
from collections import Counter
import urllib
import urllib.request
from datetime import datetime
from urllib.error import URLError

import nltk
import PyPDF2
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from authentication.checker import lcs
from authentication.compartor import get_result
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
                    username=user_name,
                    password=password
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Authentication successful')
                    messages.info(request, 'Welcome ' + user.username)
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
    messages.info(request, 'Welcome to the home page, try and upload a file!')
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


@login_required
def results(request):
    context = {
        'title': 'Results',
        'active_r': 'active'
    }
    return render(request, 'homepages/results.html', context)


@login_required(login_url='/signin')
def upload(request):
    if request.method == 'POST':
        upload_form = UploadedDocumentsForm(request.POST, request.FILES)
        if upload_form.is_valid():
            nltk.download('punkt')
            nltk.download('stopwords')
            url = request.FILES['document']
            read_pdf = PyPDF2.PdfFileReader(url)
            text = ""
            for page in read_pdf.pages:
                text += page.extract_text() + "\n"
                print(text)
            document_content = text
            tokenizer_pro = text
            universal_set_of_unique_words = []
            lowercase_query = tokenizer_pro.lower()
            query_word_list = re.sub(r"\w", " ", lowercase_query).split()
            for word in query_word_list:
                if word not in universal_set_of_unique_words:
                    universal_set_of_unique_words.append(word)
            url = "https://plagio-store.s3.eu-west-3.amazonaws.com/dataset/most_common_words.docx"
            fd1 = urllib.request.urlopen(url)
            fdn = fd1.read()
            fd = fdn.decode("utf-8")
            database1 = fd.lower()
            database_word_list = re.sub(r"\w", " ", database1).split()
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
                match_percentage = float(dot_product / (query_vector_magnitude * database_vector_magnitude))
            except ZeroDivisionError:
                match_percentage = 0
            # Check for Plagiarism status
            fila = urllib.request.urlopen(
                'https://plagio-store.s3.eu-west-3.amazonaws.com/dataset/sample.docx'
            ).read()
            f = fila.decode("utf-8")

            orig = f.replace("\n", " ")  # tokenizing

            f2 = tokenizer_pro
            plag = f2.replace("\n", " ")  # tokenizer

            tokens_o = word_tokenize(orig)
            tokens_p = word_tokenize(plag)

            # lowerCase
            tokens_o = [token.lower() for token in tokens_o]
            tokens_p = [token.lower() for token in tokens_p]
            # Trigram Similarity measures
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

            # jaccard coefficient = (S(o)^S(p))/(S(o) U S(p))
            """
            Here, we find the number of overlapping trigrams in
            the two texts, i.e the number of continuous sequences
            of three words which are present in both texts.
            """
            jaccard = s / (len(trigrams_o) + len(trigrams_p))

            # containment measure
            """
            The containment measure C is a better metric for
            or document pairs with varied document lengths.
            Here, we normalize by the trigrams in the suspicious
            """
            try:
                containment_measure = s / len(trigrams_p)
            except ZeroDivisionError:
                containment_measure = 0

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
            eng_dict_url = "https://www.cambridgeenglish.org/images/84669-pet-vocabulary-list.pdf"
            eng_dict = PyPDF2.PdfFileReader(eng_dict_url)
            eng_dict_to_text = ""
            if score > 0.1:
                plagiarism_status = True
            else:
                plagiarism_status = False
            for page in eng_dict.pages:
                eng_dict_to_text += page.extract_text() + "\n"
            upload_form.instance.plagiarism_status = plagiarism_status
            upload_form.instance.j_coefficient = jaccard
            upload_form.instance.containment_measure = containment_measure
            upload_form.instance.common_words = match_percentage
            upload_form.instance.difficult_words = 0
            upload_form.instance.wrong_words = 1 - (
                0 if (get_result(eng_dict_to_text, document_content) < 0)
                else get_result(eng_dict_to_text, document_content))
            comparator = 1 - (
                0 if (get_result(eng_dict_to_text, document_content) < 0)
                else get_result(eng_dict_to_text, document_content))
            upload_form.instance.plagiarism_score = score
            upload_form.instance.uploader = request.user
            upload_form.instance.document_content = document_content
            upload_form.save()
            messages.success(
                request,
                'The document was scanned successfully. Here are the plagiarism results.'
            )
            request.session['plagiarism_score'] = score
            request.session['non_plagiarised'] = 1 - score
            request.session['j_coefficient'] = jaccard
            request.session['containment_measure'] = containment_measure
            request.session['common_words'] = match_percentage
            request.session['difficult_words'] = 0
            request.session['wrong_words'] = comparator
            request.session['plagiarism_status'] = plagiarism_status
            return redirect('results')
        else:
            messages.error(
                request,
                'An error occurred, you surely missed out a field'
            )
    upload_form = UploadedDocumentsForm()
    context = {
        'form': upload_form,
        'title': 'Upload',
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


@login_required
def downloadable(request):
    ctx = {
        'sea': 5,
        'title': 'Uploaded Files'
    }
    url_parameter = request.GET.get("q")
    if url_parameter:
        document = UploadedDocuments.objects.filter(document_title__icontains=url_parameter)
    else:
        document = UploadedDocuments.objects.all()
    ctx["document"] = document
    does_req_accept_json = request.accepts("application/json")
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
    if is_ajax_request:
        html = render_to_string(
            template_name="homepages/search_included.html",
            context={
                "document": document,
            }
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return render(request, 'homepages/uploads_records.html', context=ctx)


@login_required
def view_doc(request, pk):
    view = UploadedDocuments.objects.get(id=pk)

    context = {
        'view': view,
        'title': f'{view.document_title}',
    }
    return render(request, 'homepages/view_document.html', context)
