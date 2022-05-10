from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.welcome, name="welcome"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('feature', views.feature, name="feature"),
    path('about-us', views.about, name="about-us"),
    path('contact-us', views.contact, name="contact-us"),
    path('upload', views.upload, name="upload"),
    # path('token', views.token, name="token"),
]