from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("Mentor/<int:pk>/", views.MentorDetail.as_view(), name="detail"),
    path("Mentor-profile/<int:pk>/", views.MentorProfileView.as_view(), name="mentor-profile"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update-mentor-profile/", views.UpdateMentorProfileView.as_view(), name="mentor-update"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
]