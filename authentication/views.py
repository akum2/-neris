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
        universalSetOfUniqueWords = []
        matchPercentage = 0

        ####################################################################################################

        inputQuery = request.POST.get("query")
        print(inputQuery)

        lowercaseQuery = open(inputQuery, "r").read().lower()
        print(lowercaseQuery)
        # lowercaseQuery = inputQuery.lower()

        queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()  # Replace punctuation by space and split
        # queryWordList = map(str, queryWordList)					#This was causing divide by zero error

        for word in queryWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        fd = open(os.path.join(BASE_DIR, "database1.txt"), "r")
        database1 = fd.read().lower()

        databaseWordList = re.sub("[^\w]", " ", database1).split()  # Replace punctuation by space and split
        # databaseWordList = map(str, databaseWordList)			#And this also leads to divide by zero error

        for word in databaseWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        queryTF = []
        databaseTF = []

        for word in universalSetOfUniqueWords:
            queryTfCounter = 0
            databaseTfCounter = 0

            for word2 in queryWordList:
                if word == word2:
                    queryTfCounter += 1
            queryTF.append(queryTfCounter)

            for word2 in databaseWordList:
                if word == word2:
                    databaseTfCounter += 1
            databaseTF.append(databaseTfCounter)

        dotProduct = 0
        for i in range(len(queryTF)):
            dotProduct += queryTF[i] * databaseTF[i]

        queryVectorMagnitude = 0
        for i in range(len(queryTF)):
            queryVectorMagnitude += queryTF[i] ** 2
        queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

        databaseVectorMagnitude = 0
        for i in range(len(databaseTF)):
            databaseVectorMagnitude += databaseTF[i] ** 2
        databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)

        matchPercentage = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100
        output = "Input query text matches %0.02f%% with database." % matchPercentage
        context = {
            'output': output,
            'query': inputQuery,
        }
        return render(request, 'homepages/upload.html', context)
    else:
        context = {
        }
    return render(request, 'homepages/upload.html', context)
