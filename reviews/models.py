from django.db import models
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="reviews", on_delete=models.CASCADE)
    mentor = models.ForeignKey("users.Mentor", related_name="reviews", on_delete=models.CASCADE)
    scope = models.IntegerField()
    comment = models.TextField()
    
    def menteename(self):
        return self.user.name
    
    def mentorname(self):
        return self.mentor.user.name