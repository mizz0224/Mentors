from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("search_mentor", views.search_mentor, name="search_mentor"),
]