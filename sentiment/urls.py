# sentiment/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_sentiment, name='home'),
]
