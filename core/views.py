import os
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from users import models

# Create your views here.
class HomeView(ListView):
    model = models.Mentor
    template_name = "home.html"
    context_object_name = "Mentors"
    paginate_by = 10
    def get_queryset(self):
        return models.Mentor.objects.filter(is_authorized=True)