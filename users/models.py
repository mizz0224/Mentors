from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class User(AbstractUser):
    """ User Model Admin """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    is_mentors = models.BooleanField(default=False)