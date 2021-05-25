import os
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from users import models

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"
    