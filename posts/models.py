from django.db import models
from core import models as core_models

# Create your models here.
class Post(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    content = models.TextField()
    
    def __str__(self):
        return self.user.name
    
class Comment(core_models.TimeStampedModel):
    post = models.ForeignKey("posts.Post", related_name="comments", on_delete=models.CASCADE)
    mentor = models.ForeignKey("users.Mentor", related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    
    def mentorname(self):
        return self.mentor.user.name