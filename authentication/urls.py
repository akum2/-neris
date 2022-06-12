from django.contrib.auth import logout
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.welcome, name="welcome"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('profile', views.profile, name="profile"),
    path('profile-edit', views.profile_edit, name="profile-edit"),
    path('feature', views.feature, name="feature"),
    path('about-us', views.about, name="about-us"),
    path('contact-us', views.contact, name="contact-us"),
    path('upload', views.upload, name="upload"),
    path('logout', logout, name="logout"),
]