from django.urls import path
from accountsapp import views


urlpatterns = [
  path('func',views.fun)  
]