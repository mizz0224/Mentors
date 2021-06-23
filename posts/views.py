from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import FormView
from . import forms, models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Post
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "posts"


class PostDetail(DetailView):

    """ PostDetail Definition """

    model = models.Post
