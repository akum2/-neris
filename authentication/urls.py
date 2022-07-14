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
    path('logout', views.logout, name="logout"),
    path('results', views.results, name="results"),
    path('uploaded/', views.downloadable, name='uploaded'),
    path('view_doc/<pk>', views.view_doc, name='view_doc')
]
