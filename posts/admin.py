from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "content",
    )
    
    list_filter = (
        "user",
    )

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "mentorname",
        "content",
    )
    
    list_filter = (
        "post",
    )