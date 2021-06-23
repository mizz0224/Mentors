from django.urls import path
from . import views
app_name = "wishlists"

urlpatterns = [
    path("toggle/<int:mentor_pk>/", views.toggle_mentor , name="toggle-mentor"),
    path("favs/", views.SeeFavsView.as_view() , name="see-favs")
]

