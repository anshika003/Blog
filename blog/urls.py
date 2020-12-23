from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('PostComment', views.PostComment, name='PostComment'),
    path('', views.blogHome, name='blogHome'),
    #API to post commnet
    path('<str:slug>', views.blogPost, name='blogPost'),

]