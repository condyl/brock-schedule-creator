from django.urls import path
from . import views

urlpatterns = [
    path('homepage', views.home, name='home'),
    path('about', views.about, name='about')
]