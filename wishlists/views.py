from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from users import models as user_models
from . import models
# Create your views here.

def toggle_mentor(request, mentor_pk):
    action = request.GET.get('action', None)
    mentor = user_models.Mentor.objects.get_or_none(pk=mentor_pk)
    if mentor is not None and action is not None:
        the_wishlist, _ = models.Wishlist.objects.get_or_create(user=request.user, name="My Favorite Mentors")
        if action == 'add':
            the_wishlist.mentors.add(mentor)
        elif action == 'remove':
            the_wishlist.mentors.remove(mentor)
    return redirect(reverse("users:detail", kwargs={'pk': mentor_pk}))

class SeeFavsView(TemplateView):
    template_name="wishlists/wishlist_detail.html"
    paginate_by = 10