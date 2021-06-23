import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models

# Create your models here.

class BookedTime(core_models.TimeStampedModel):
    time = models.DateField()
    reservation = models.ForeignKey("reservation", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Booked Time"
        verbose_name_plural = "Booked Times"
        
    def __str__(self):
        return str(self.day)

class BookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey("reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"
        
    def __str__(self):
        return str(self.day)

class Reservation(core_models.TimeStampedModel):
    
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled")
    )
    
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    user = models.ForeignKey("users.User", related_name="reservations", on_delete=models.CASCADE)
    mentor = models.ForeignKey("users.Mentor", related_name="reservations", on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    
    def menteename(self):
        return self.user.name
    
    def mentorname(self):
        return self.mentor.user.name
    
    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out
    in_progress.boolean = True
    
    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished
    is_finished.boolean = True
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(day__range=(start, end)).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)
    
    def count_reservations(self):
        return self.reservations.count()
    count_reservations.short_description = "Number of Reservations"