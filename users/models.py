from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from core import models as core_models
from users import models as user_models

# Create your models here.
class User(AbstractUser):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    
    LOGIN_CHOICES = ((LOGIN_EMAIL, "Email"), (LOGIN_GITHUB, "Github"), (LOGIN_KAKAO, "Kakao"))
    
    image = models.ImageField(upload_to="avatars", blank=True, null=True) # 업로드 폴더 지정 후 사용할 예정
    name = models.CharField(max_length=10, blank=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True) # 관리자 계정 생성후엔 auto_now_add=False로 바꿔줍시다
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True, default=GENDER_MALE)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)
    
    def __str__(self):
        return self.name
    
class Mentor(models.Model):
    user = models.ForeignKey("users.User", related_name="mentor", on_delete=models.CASCADE)
    main_branch = models.ForeignKey("users.MainBranch", related_name="mentor", on_delete=models.SET_NULL, null=True)
    sub_branch = models.ForeignKey("users.SubBranch", related_name="mentor", on_delete=models.SET_NULL, null=True)
    company = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    career = models.TextField()
    is_authorized = models.BooleanField(default=False)
    is_supermento = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.name
    
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"pk": self.pk})
    
    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0
    
    
class MainBranch(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class SubBranch(models.Model):
    name = models.CharField(max_length=50)
    main_branch = models.ForeignKey("users.MainBranch", related_name="sub_branch", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + "(" + self.main_branch.name + ")"
    
    