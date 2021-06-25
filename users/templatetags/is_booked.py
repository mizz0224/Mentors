import datetime
from django import template
from reservations import models as reservation_models
from users import models as users_models

register = template.Library()

@register.simple_tag
def is_booked(user, Mentor, day):
    if day.number == 0:
        return 
    try:
        # user = users_models.User.objects.get(pk=user_pk)
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation = reservation_models.Reservation.objects.get(check_in=date, user=user, mentor=Mentor)
        return True
    except reservation_models.Reservation.DoesNotExist:
        return False