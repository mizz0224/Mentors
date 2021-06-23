from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "menteename",
        "mentorname",
        "check_in",
        "check_out",
        "is_confirmed",
    )
    
    list_filter = (
        "user",
        "is_confirmed",
    )
    
@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    list_display = (
        "day",
        "reservation",
    )