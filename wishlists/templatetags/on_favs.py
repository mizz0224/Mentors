from django import template
from wishlists import models as wishlist_models
register = template.Library()

@register.simple_tag(takes_context=True)
def on_favs(context, mentor):
    user = context.request.user
    the_wishlist, _ = wishlist_models.Wishlist.objects.get_or_create(user=user, name="My Favorite Mentors")
    return mentor in the_wishlist.mentors.all()