from django.contrib.auth.models import AbstractUser
from django.db import models

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
    # image = models.ImageField(upload_to=) # 업로드 폴더 지정 후 사용할 예정
    name = models.CharField(max_length=10, blank=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=True, blank=True) # 관리자 계정 생성후엔 auto_now_add=False로 바꿔줍시다
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True, default=GENDER_MALE)
    
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
    
class MainBranch(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class SubBranch(models.Model):
    name = models.CharField(max_length=50)
    main_branch = models.ForeignKey("users.MainBranch", related_name="sub_branch", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + "(" + self.main_branch.name + ")"