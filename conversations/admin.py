from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "mentor",
        
    )
    
    list_filter = (
        "user",
    )

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "conversation",
        "message",
        "user",
        "created",
    )
    
    list_filter = (
        "conversation",
    )