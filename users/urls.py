"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from enum import verify
from django.contrib import admin
from django.urls import path, include
from . views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('',index, name="home"),
    path('single/<str:content>/',single, name="single"),
    path('contact/',contact, name="contact"),
    path('about/',about, name="about"),              
    path('search/',search, name="search"),                                                                                                                     
    path('signin/',signin, name="signin"),
    path('signup/',signup, name="signup"),
    path('sendcomment/',sendcomment, name="sendcomment"),
    path('logout/',logoutpage, name="logout"),
    path('editusername/',editusername, name="editusername"),
    path('verify/<str:token>/', verify, name='verify_email'),
    path('forgotpassword/', forgotpassword, name='forgotpassword'),
]
