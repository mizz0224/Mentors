import os
from django.views.generic import FormView, DetailView, UpdateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from users import models

# Create your views here.
class HomeView(ListView):
    """ HomeView Definition """
    
    model = models.Mentor
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "Mentors"