from django.db import models
from core import models as core_models

class Wishlist(core_models.TimeStampedModel):
    """ List Model Definition """
    
    name = models.CharField(max_length=80)
    user = models.OneToOneField("users.User", related_name="wishlist", on_delete=models.CASCADE)
    mentors = models.ManyToManyField("users.Mentor", related_name="wishlists", blank=True)
    
    def __str__(self):
        return self.name
    
    def count_mentors(self):
        return self.mentors.count()
    count_mentors.short_description = "Number of Mentors"