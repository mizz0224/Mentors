from django.urls import path
from . import views
app_name="conversations"

urlpatterns = [
    path("go/<int:user_pk>/<int:mentor_pk>/", views.go_conversation, name="go"),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
    path("list/<int:pk>/", views.MessageListView.as_view(), name="list"),
]
