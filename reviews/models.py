from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="reviews", on_delete=models.CASCADE)
    mentor = models.ForeignKey("users.Mentor", related_name="reviews", on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    
    def menteename(self):
        return self.user.name
    
    def mentorname(self):
        return self.mentor.user.name
    
    def rating_average(self):
        avg = self.score
        return round(avg, 2)
    
    rating_average.short_description = "Avg."
    
    class Meta:
        ordering = ("-created",)