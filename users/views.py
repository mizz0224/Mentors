import os
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms, mixins
# Create your views here.
    
class MentorDetail(DetailView):
    """ MentorDetail Definition """

    model = models.Mentor
    context_object_name = "Mentor"
    
class MentorProfileView(DetailView):
    
    model = models.Mentor
    context_object_name = "Mentor"
    template_name = "users/mentor_profile.html"
    
class UserProfileView(DetailView):
    
    model = models.User
    context_object_name = "users"
    
class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "name",
        "birthdate",
        "gender",
    )
    success_message = "Profile updated"
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['name'].widget.attrs ={'placeholder': "name"}
        form.fields['birthdate'].widget.attrs ={'placeholder': "Birthdate"}
        form.fields['gender'].widget.attrs ={'placeholder': "Gender"}
        return form
    

class UpdateMentorProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Mentor
    template_name = "users/update_Mentor_profile.html"
    fields = (
        "user",
        "main_branch",
        "sub_branch",
        "company",
        "department",
        "career",
        "is_authorized",
        "is_supermento",
    )
    success_message = "Profile updated"
    
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['user'].widget.attrs ={'placeholder': "user"}
        form.fields['main_branch'].widget.attrs ={'placeholder': "main_branch"}
        form.fields['sub_branch'].widget.attrs ={'placeholder': "sub_branch"}
        form.fields['company'].widget.attrs ={'placeholder': "company"}
        form.fields['department'].widget.attrs ={'placeholder': "department"}
        form.fields['career'].widget.attrs ={'placeholder': "career"}
        form.fields['is_authorized'].widget.attrs ={'placeholder': "is_authorized"}
        form.fields['is_supermento'].widget.attrs ={'placeholder': "is_supermento"}
        
        return form
    
    
class UpdatePasswordView(mixins.LoggedInOnlyView, mixins.EmailLoginOnlyView, SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update_password.html"
    success_message = "Password updated"
    
    def get_success_url(self):
        return self.request.user.get_absolute_url()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['old_password'].widget.attrs ={'placeholder': "Currnet password"}
        form.fields['new_password1'].widget.attrs ={'placeholder': "New password"}
        form.fields['new_password2'].widget.attrs ={'placeholder': "Confirmed new passowrd"}
        return form
    
class mentorsign():
    pass
    
def search(request):
    pass
