from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

@admin.register(models.Wishlist)
class ListAdmin(admin.ModelAdmin):
    """ List Admin Definition """
    list_display = (
        "name",
        "user",
        "count_mentors",
    )
    
    search_fields = (
        "name",
    )
    
    filter_horizontal = (
        "mentors",
    )
