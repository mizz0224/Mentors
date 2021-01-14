from django.db import models
from core import models as core_models

# Create your models here.
class Conversation(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="conversations", on_delete=models.CASCADE)
    mentor = models.ForeignKey("users.Mentor", related_name="conversations", on_delete=models.CASCADE)

class Message(core_models.TimeStampedModel):
    conversation = models.ForeignKey("conversations.Conversation", related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()