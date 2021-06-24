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
    path("Mentor/<int:pk>/", views.MentorDetail.as_view(), name="detail"),
    path(
        "Mentor-profile/<int:pk>/",
        views.MentorProfileView.as_view(),
        name="mentor-profile",
    ),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path(
        "update-mentor-profile/",
        views.UpdateMentorProfileView.as_view(),
        name="mentor-update",
    ),
    path("point/", views.UserPointView.as_view(), name="point"),
    path("point/add/", views.ajax_buy_point, name="buy_point"),
    path(
        "update-mentor-profile/",
        views.UpdateMentorProfileView.as_view(),
        name="mentor-update",
    ),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
    path(
        "sms_verfy/",
        views.ajax_sms_verfy,
        name="sms_verfy",
    ),
    path(
        "sms_check/",
        views.ajax_sms_check,
        name="sms_check",
    ),
    path("search_mentor", views.search_mentor, name="search_mentor"),
    path("Mentorsignup/", views.MentorSignUpView.as_view(), name="Mentorsignup"),
    path("Mentorsignup/kakaomap", views.renderkakaomap),
    path("Mentor-list/", views.MentorListView.as_view(), name="MentorList"),
    path("manage/", views.ManageUserView.as_view(), name="manage"),
    path("manage/submit", views.manage_user, name="submit"),
    path("kakao/login/callback/", views.kakao_callback, name="kakao-callback"),
    path("kakao/signup", views.KakaoSignUpView.as_view(), name="kakaosignup"),
    path("kakaologin",views.KakaoLoginTest.as_view(), name = "kakaologin"),
]
