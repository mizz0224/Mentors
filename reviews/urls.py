from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create/<int:mentor>/", views.create_review, name="create"),
    path("update/<int:pk>/", views.Update_review.as_view(), name="update"),
    path("remove/<int:pk>/", views.remove_review, name="remove"),
]
