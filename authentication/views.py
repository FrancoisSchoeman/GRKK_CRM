from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'authentication/index.html'