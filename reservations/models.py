from django.db import models
from core import models as core_models

# Create your models here.
class Reservation(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="reservations", on_delete=models.CASCADE)
    mentor = models.ForeignKey("users.Mentor", related_name="reservations", on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now=False, auto_now_add=False)
    where = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    
    def menteename(self):
        return self.user.name
    
    def mentorname(self):
        return self.mentor.user.name