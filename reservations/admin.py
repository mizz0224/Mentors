from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "menteename",
        "mentorname",
        "when",
        "where",
        "is_confirmed",
    )
    
    list_filter = (
        "user",
        "is_confirmed",
    )