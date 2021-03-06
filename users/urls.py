from django.urls import path
from . import views

app_name = "users"
namespace = "users"
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),  # login을 위한 url
    path("logout", views.log_out, name="logout"),  # logout을 위한 url
    path("signup", views.SignUpView.as_view(), name="signup"),  # signup를 위한 url
    path(
        "socialsignup", views.SocialSignUpView.as_view(), name="socialsignup"
    ),  # social signup을 위한 url
    path(
        "verify/<str:key>", views.complete_verification, name="complete-verification"
    ),  # 이메일 인증을 위한 url
]
