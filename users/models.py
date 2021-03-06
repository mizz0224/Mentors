import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, gender, birthdate, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=email,
            email=email,
            name=name,
            gender=gender,
            birthdate=birthdate,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, gender, birthdate, password):
        user = self.create_user(
            email=email,
            name=name,
            gender=gender,
            birthdate=birthdate,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


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

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    # image = models.ImageField(upload_to=) # 업로드 폴더 지정 후 사용할 예정
    name = models.CharField(max_length=10, blank=True)
    birthdate = models.DateField(
        auto_now=False, blank=True, null=True
    )  # 관리자 계정 생성후엔 auto_now_add=False로 바꿔줍시다
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True, default=GENDER_MALE
    )
    fake_users = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = UserManager()

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

    def __str__(self):
        return self.name


class Mentor(models.Model):
    user = models.ForeignKey(
        "users.User", related_name="mentor", on_delete=models.CASCADE
    )
    main_branch = models.ForeignKey(
        "users.MainBranch", related_name="mentor", on_delete=models.SET_NULL, null=True
    )
    sub_branch = models.ForeignKey(
        "users.SubBranch", related_name="mentor", on_delete=models.SET_NULL, null=True
    )
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
    main_branch = models.ForeignKey(
        "users.MainBranch", related_name="sub_branch", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name + "(" + self.main_branch.name + ")"